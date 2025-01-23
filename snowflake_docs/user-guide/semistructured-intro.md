# Introduction to Loading Semi-structured Data¶

This topic describes semi-structured data and provides information about how
to load and store it in Snowflake.

## What is Semi-structured Data?¶

Semi-structured data is data that does not conform to the standards of
traditional structured data, but contains tags (labels) or other types of
mark-up that identify individual, distinct entities within the data.

Two of the key attributes that distinguish semi-structured data from
structured data are nested data structures and the lack of a fixed schema:

  * Structured data requires a fixed schema that is defined before the data can be loaded and queried in a relational database system. Semi-structured data does not require a prior definition of a schema and can constantly evolve (i.e. new attributes can be added at any time).

In addition, entities within the same class may have different attributes even
though they are grouped together, and the order of the attributes is not
important.

  * Unlike structured data, which represents data as a flat table, semi-structured data can contain N-level hierarchies of nested information.

## What is Hierarchical Data?¶

Semi-structured data is usually organized hierarchically. Complex data
structures can be built by nesting simpler data types, such as
[arrays](../sql-reference/data-types-semistructured.html#label-data-type-
array) and [objects](../sql-reference/data-types-semistructured.html#label-
data-type-object). (Note: a Snowflake OBJECT corresponds to a “dictionary” or
a “map”. A Snowflake object is not an “object” in the sense of “object-
oriented programming”.)

For example, JSON data can contain an object that contains an array. Each cell
of that array might itself contain a nested object or array.

You can use Snowflake data types to construct a hierarchy to hold your semi-
structured data by using the following properties of data types:

  * A [VARIANT](../sql-reference/data-types-semistructured.html#label-data-type-variant) can hold a value of any other data type, including an ARRAY or an OBJECT.

  * An ARRAY or OBJECT holds a value of type VARIANT.

For example, suppose that you want to store the dates on which different types
of natural disasters occurred. You might create an OBJECT that contains the
keys ‘Hurricane’, ‘Earthquake’, ‘Flood’, etc. The value associated with each
of those keys can be an ARRAY that contains the dates on which each type of
disaster occurred. Because the value in each key-value pair must be a VARIANT,
each array of dates would be stored as an ARRAY wrapped inside a VARIANT
inside the corresponding OBJECT. The top level of the hierarchy would look
similar to the following (the curly braces indicate an OBJECT, which contains
key-value pairs):

    
    
    {
        "Flood": flood_date_array::VARIANT,
        "Earthquake": earthquake_date_array::VARIANT,
        ...
    }
    

Copy

As another example, suppose that you want to store a single list of disasters
in chronological order. In that case, your outer data type might be ARRAY.
Each cell of that ARRAY might contain an OBJECT (wrapped in a VARIANT) that
contains key-value pairs with information about the event. For example, each
OBJECT that describes an earthquake might have keys like ‘Timestamp’,
‘Location’, and ‘Magnitude’. Each OBJECT that describes a tornado might have
keys like ‘Timestamp’ and ‘Maximum_wind_speed’.

    
    
    [
        {
            "Event_ID": 54::VARIANT,
            "Type": "Earthquake"::VARIANT,
            "Magnitude": 7.4::VARIANT,
            "Timestamp": "2018-06-09 12:32:15"::TIMESTAMP_LTZ::VARIANT
            ...
        }::VARIANT,
        {
            "Event_ID": 55::VARIANT,
            "Type": "Tornado"::VARIANT,
            "Maximum_wind_speed": 186::VARIANT,
            "Timestamp": "2018-07-01 09:42:55"::TIMESTAMP_LTZ::VARIANT
            ...
        }::VARIANT
    ]
    

Copy

You can create data hierarchies of almost any depth or breadth (up to the
limit of storage for each data type). For example, an OBJECT that contains
information about a tornado might need information about the wind speed at
different times during the tornado, so your data structure might look like the
following:

  1. The top level is an ARRAY.

  2. Each cell of that ARRAY contains one OBJECT that describes one tornado.

  3. Each OBJECT contains an ARRAY of windspeed data.

  4. Each cell of that inner ARRAY is an OBJECT that contains data with keys such as:

     * Timestamp of the windspeed.

     * Location of the windspeed.

     * The windspeed in KPH (kilometers per hour).

In some cases, data might be incomplete. For example, if the windspeed at a
particular location was estimated based on the damage visible after the
tornado (rather than measured directly during the tornado), then the data
might include location and windspeed, but not a timestamp.

## Loading Semi-structured Data¶

Snowflake can import semi-structured data from JSON, Avro, ORC, Parquet, and
XML formats and store it in [Snowflake data types designed specifically to
support semi-structured data](../sql-reference/data-types-semistructured).

Depending upon the structure of the data, the size of the data, and the way
that the user chooses to import the data, semi-structured data can be stored
in a single column or split into multiple columns.

The steps for loading semi-structured data into tables are similar to those
for loading structured data into tables. However, when you load and store
semi-structured data, you can also explicitly specify all, some, or none of
the structure:

  * If your data is a set of key-value pairs, you can load it into a column of type OBJECT.

  * If your data is an array, you can load it into a column of type ARRAY.

  * If you have hierarchical data, you may do either of the following:

    * Split the data across multiple columns. You may:

      * Explicitly [extract and transform](data-load-transform) columns from semi-structured data into separate columns in target tables.

      * Use Snowflake to automatically [detect and retrieve](data-load-overview.html#label-detect-column-definitions-in-semi-structured-data-files) the column definitions from staged semi-structured data files. Create Snowflake tables, external tables, or views from the column definitions. To save time, create tables with the column definitions automatically retrieved from the staged files.

    * Store the data in a single column of type VARIANT. You may:

      * Specify the structure explicitly (e.g. specify a hierarchy of VARIANT, ARRAY, and OBJECT data types).

      * Load the data without explicitly specifying the structure. If you specify a data format that Snowflake recognizes and parses (JSON, Avro, Parquet, or ORC), the data is converted to an internal data format that uses Snowflake VARIANT, ARRAY, and OBJECT data types.

If the data is complex or an individual value requires more than about 16 MB
of storage space, then you can use more than one of the preceding techniques.
For example, you can split the data into multiple columns, and some of those
columns can contain an explicitly-specified hierarchy of data types. For
information about preparing data that is larger than 16 MB for loading, see
[Reducing the size of objects larger than 16 MB before loading](data-load-
considerations-prepare.html#label-reduce-size-of-objects-larger-than-16-mb).

You can load semi-structured data the following ways:

  * Specify the input data format and the Snowflake data type while creating the table and loading the data. For example, in the code below, the VARIANT data type is specified in the CREATE TABLE statement, while the JSON input data format is specified in the `TYPE = <data_format>` clause of the [COPY INTO <table>](../sql-reference/sql/copy-into-table) command:
    
        CREATE TABLE my_table (my_variant_column VARIANT);
    COPY INTO my_table ... FILE FORMAT = (TYPE = 'JSON') ...
    

Copy

  * Specify the input data format and the Snowflake data type by calling an appropriate function to convert the data. For example, to convert JSON-formatted data to a VARIANT value, call [PARSE_JSON](../sql-reference/functions/parse_json), as shown below:
    
        INSERT INTO my_table (my_variant_column) SELECT PARSE_JSON('{...}');
    

Copy

When data is stored in ARRAY, OBJECT, or VARIANT data types, or a hierarchy of
those types, you can [query it](querying-semistructured).

## Storing Semi-structured Data¶

Semi-structured data is typically stored in the following Snowflake data
types:

  * [ARRAY](../sql-reference/data-types-semistructured.html#label-data-type-array): similar to an array in other languages.

  * [OBJECT](../sql-reference/data-types-semistructured.html#label-data-type-object): similar to a JSON object, also called a “dictionary”, “hash”, or “map” in many languages. This contains key-value pairs.

  * [VARIANT](../sql-reference/data-types-semistructured.html#label-data-type-variant): a data type that can hold a value of any other data type (including ARRAY and OBJECT). VARIANT is used to build and store hierarchical data.

(If imported data is split into multiple columns before it is stored, then
some or all of those columns can be simple data types, such as FLOAT, VARCHAR,
etc.)

The ARRAY, OBJECT, and VARIANT data types can be used individually, or nested
to build a hierarchy.

If the data is imported in JSON, Avro, ORC, or Parquet format, then Snowflake
can build the hierarchy for you and store it in a VARIANT. You can also create
a hierarchy manually.

Regardless of how the hierarchy was constructed, Snowflake converts the data
to an optimized internal storage format that uses ARRAY, OBJECT, and VARIANT.
This internal storage format supports fast and efficient SQL querying.

More information about [ARRAY](../sql-reference/data-types-
semistructured.html#label-data-type-array), [OBJECT](../sql-reference/data-
types-semistructured.html#label-data-type-object), and [VARIANT](../sql-
reference/data-types-semistructured.html#label-data-type-variant) data types
is in [Semi-structured data types](../sql-reference/data-types-
semistructured).

## Querying Semi-structured Data¶

Snowflake supports operators for:

  * [Accessing an element in an array.](../sql-reference/data-types-semistructured.html#label-accessing-array-by-index)

  * [Retrieving a specified value from a key-value pair in an OBJECT.](../sql-reference/data-types-semistructured.html#label-accessing-object-by-key)

  * [Traversing the levels of a hierarchy stored in a VARIANT.](querying-semistructured.html#label-traversing-semistructured-data)

More information about querying semi-structured data is in [Querying Semi-
structured Data](querying-semistructured).

For information about querying XML by specifying XML tags, see the
documentation of the [XMLGET](../sql-reference/functions/xmlget) function.

