# Considerations for Semi-structured Data Stored in VARIANT¶

This topic provides best practices, general guidelines, and important
considerations for loading and working with [VARIANT](../sql-reference/data-
types-semistructured.html#label-data-type-variant) values that contain semi-
structured data. This can be explicitly-constructed [hierarchical
data](semistructured-intro.html#label-hierarchical-data) or data that you have
loaded from semi-structured data formats such as JSON, Avro, ORC, and Parquet.
The information in this topic does not necessarily apply to XML data.

## Data Size Limitations¶

A VARIANT value can have a maximum size of up to 16 MB of uncompressed data.
However, in practice, the maximum size is usually smaller due to internal
overhead. The maximum size is also dependent on the object being stored.

For more information, see [VARIANT](../sql-reference/data-types-
semistructured.html#label-data-type-variant).

For information about preparing data that is larger than 16 MB for loading,
see [Reducing the size of objects larger than 16 MB before loading](data-load-
considerations-prepare.html#label-reduce-size-of-objects-larger-than-16-mb).

## Storing Semi-structured Data in a VARIANT Column vs. Flattening the Nested
Structure¶

If you are not sure yet what types of operations you want to perform on your
semi-structured data, Snowflake recommends storing the data in a VARIANT
column for now.

For data that is mostly regular and uses only data types that are native to
the semi-structured format you are using (e.g. strings and integers for JSON
format), the storage requirements and query performance for operations on
relational data and data in a VARIANT column is very similar.

For better pruning and less storage consumption, we recommend flattening your
OBJECT and key data into separate relational columns if your semi-structured
data includes:

  * Dates and timestamps, especially non-[ISO 8601](http://www.iso.org/iso/home/standards/iso8601.htm) dates and timestamps, as string values

  * Numbers within strings

  * Arrays

Non-native values (such as dates and timestamps in JSON) are stored as strings
when loaded into a VARIANT column, so operations on these values could be
slower and also consume more space than when stored in a relational column
with the corresponding data type.

If you know your use cases for the data, perform tests on a typical data set.
Load the data set into a VARIANT column in a table. Use the [FLATTEN](../sql-
reference/functions/flatten) function to extract the OBJECTs and keys you plan
to query into a separate table. Run a typical set of queries against both
tables to see which structure provides the best performance.

## NULL Values¶

Snowflake supports two types of NULL values in semi-structured data:

  * SQL NULL: SQL NULL means the same thing for semi-structured data types as it means for structured data types: the value is missing or unknown.

  * JSON null (sometimes called “VARIANT NULL”): In a VARIANT column, JSON null values are stored as a string containing the word “null” to distinguish them from SQL NULL values.

The following example contrasts SQL NULL and JSON null:

>
>     SELECT
>       PARSE_JSON(NULL) AS "SQL NULL",
>       PARSE_JSON('null') AS "JSON NULL",
>       PARSE_JSON('[ null ]') AS "JSON NULL",
>       PARSE_JSON('{ "a": null }'):a AS "JSON NULL",
>       PARSE_JSON('{ "a": null }'):b AS "ABSENT VALUE";
>     +----------+-----------+-----------+-----------+--------------+
>     | SQL NULL | JSON NULL | JSON NULL | JSON NULL | ABSENT VALUE |
>     |----------+-----------+-----------+-----------+--------------|
>     | NULL     | null      | [         | null      | NULL         |
>     |          |           |   null    |           |              |
>     |          |           | ]         |           |              |
>     +----------+-----------+-----------+-----------+--------------+
>  
>
> Copy

To convert a VARIANT `"null"` value to SQL NULL, cast it as a string. For
example:

>
>     SELECT
>       PARSE_JSON('{ "a": null }'):a,
>       TO_CHAR(PARSE_JSON('{ "a": null }'):a);
>
> +-------------------------------+----------------------------------------+
>     | PARSE_JSON('{ "A": NULL }'):A | TO_CHAR(PARSE_JSON('{ "A": NULL }'):A) |
>
> |-------------------------------+----------------------------------------|
>     | null                          | NULL                                   |
>
> +-------------------------------+----------------------------------------+
>  
>
> Copy

## Semi-structured Data Files and Columnarization¶

When semi-structured data is inserted into a VARIANT column, Snowflake uses
certain rules to extract as much of the data as possible to a columnar form.
The rest of the data is stored as a single column in a parsed semi-structured
structure.

By default, Snowflake extracts a maximum of 200 elements per partition, per
table. To increase this limit, contact [Snowflake
Support](https://docs.snowflake.com/user-guide/contacting-support).

### Elements that are not extracted¶

Elements with the following characteristics are not extracted into a column:

  * Elements that contain even a single “null” value are not extracted into a column. This applies to elements with “null” values and not to elements with missing values, which are represented in columnar form.

This rule ensures that no information is lost (that is, that the difference
between VARIANT “null” values and SQL NULL values is not lost).

  * Elements that contain multiple data types. For example:

The `foo` element in one row contains a number:

    
        {"foo":1}
    

Copy

The same element in another row contains a string:

    
        {"foo":"1"}
    

Copy

### How extraction impacts queries¶

When you query a semi-structured element, Snowflake’s execution engine behaves
differently according to whether an element was extracted.

  * If the element was extracted into a column, the engine scans only the extracted column.

  * If the element was not extracted into a column, the engine must scan the entire JSON structure, and then for each row traverse the structure to output values. This impacts performance.

To avoid the performance impact for elements that were not extracted, do the
following:

  * Extract semi-structured data elements containing “null” values into relational columns before you load them.

Alternatively, if the “null” values in your files indicate missing values and
have no other special meaning, we recommend setting the [file format
option](../sql-reference/sql/create-file-format) STRIP_NULL_VALUES to TRUE
when you load the semi-structured data files. This option removes OBJECT
elements or ARRAY elements containing “null” values.

  * Ensure each unique element stores values of a single data type that is native to the format (for example, string or number for JSON).

### Parsing NULL Values¶

To output a SQL NULL value from a VARIANT `"null"` key-value, use the [TO_CHAR
, TO_VARCHAR](../sql-reference/functions/to_char) function to cast the value
as a string, e.g.:

    
    
    SELECT column1
      , TO_VARCHAR(PARSE_JSON(column1):a)
    FROM
      VALUES('{"a" : null}')
    , ('{"b" : "hello"}')
    , ('{"a" : "world"}');
    
    +-----------------+-----------------------------------+
    | COLUMN1         | TO_VARCHAR(PARSE_JSON(COLUMN1):A) |
    |-----------------+-----------------------------------|
    | {"a" : null}    | NULL                              |
    | {"b" : "hello"} | NULL                              |
    | {"a" : "world"} | world                             |
    +-----------------+-----------------------------------+
    

Copy

