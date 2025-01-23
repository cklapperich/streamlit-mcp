# Transforming data during a load¶

Snowflake supports transforming data while loading it into a table using the
[COPY INTO <table>](../sql-reference/sql/copy-into-table) command,
dramatically simplifying your ETL pipeline for basic transformations. This
feature helps you avoid the use of temporary tables to store pre-transformed
data when reordering columns during a data load. This feature applies to both
bulk loading and Snowpipe.

The COPY command supports:

  * Column reordering, column omission, and casts using a [SELECT](../sql-reference/sql/select) statement. There is no requirement for your data files to have the same number and ordering of columns as your target table.

  * The ENFORCE_LENGTH | TRUNCATECOLUMNS option, which can truncate text strings that exceed the target column length.

For general information about querying staged data files, see [Querying Data
in Staged Files](querying-stage).

## Usage notes¶

This section provides usage information for transforming staged data files
during a load.

### Supported file formats¶

The following file format types are supported for COPY transformations:

  * CSV

  * JSON

  * Avro

  * ORC

  * Parquet

  * XML

To parse a staged data file, it is necessary to describe its file format:

CSV:

    

The default format is character-delimited UTF-8 text. The default field
delimiter is a comma character (`,`). The default record delimiter is the new
line character. If the source data is in another format, specify the file
format type and options.

When querying staged data files, the `ERROR_ON_COLUMN_COUNT_MISMATCH` option
is ignored. There is no requirement for your data files to have the same
number and ordering of columns as your target table.

All other file format types:

    

Specify the format type and options that match your data files.

To explicitly specify file format options, set them in one of the following
ways:

**Querying staged data files using a SELECT statement:** | 

  * As file format options specified for a named file format or stage object. The named file format/stage object can then be referenced in the SELECT statement.

  
---|---  
**Loading columns from staged data files using a COPY INTO** _< table>_ **statement:** | 

  * As file format options specified directly in the COPY INTO _< table>_ statement.
  * As file format options specified for a named file format or stage object. The named file format/stage object can then be referenced in the COPY INTO _< table>_ statement.

  
  
### Supported functions¶

Snowflake currently supports the following subset of functions for COPY
transformations:

  * [ARRAY_CONSTRUCT](../sql-reference/functions/array_construct)

  * [ARRAY_SIZE](../sql-reference/functions/array_size)

  * [ASCII](../sql-reference/functions/ascii)

  * [CASE](../sql-reference/functions/case)

  * [CAST , ::](../sql-reference/functions/cast)

  * [CEIL](../sql-reference/functions/ceil)

  * [CHECK_JSON](../sql-reference/functions/check_json)

  * [CHECK_XML](../sql-reference/functions/check_xml)

  * [CHR , CHAR](../sql-reference/functions/chr)

  * [CONCAT , ||](../sql-reference/functions/concat)

  * [CONVERT_TIMEZONE](../sql-reference/functions/convert_timezone)

  * [ENDSWITH](../sql-reference/functions/endswith)

  * [EQUAL_NULL](../sql-reference/functions/equal_null)

  * [FLOOR](../sql-reference/functions/floor)

  * [GET](../sql-reference/functions/get)

  * [GET_PATH , :](../sql-reference/functions/get_path)

  * [HEX_DECODE_STRING](../sql-reference/functions/hex_decode_string)

  * [HEX_ENCODE](../sql-reference/functions/hex_encode)

  * [IFF](../sql-reference/functions/iff)

  * [IFNULL](../sql-reference/functions/ifnull)

  * [[ NOT ] ILIKE](../sql-reference/functions/ilike)

  * [[ NOT ] IN](../sql-reference/functions/in)

  * [IS_ARRAY](../sql-reference/functions/is_array)

  * [IS_BOOLEAN](../sql-reference/functions/is_boolean)

  * [IS_DECIMAL](../sql-reference/functions/is_decimal)

  * [IS_INTEGER](../sql-reference/functions/is_integer)

  * [IS_NULL_VALUE](../sql-reference/functions/is_null_value)

  * [IS_OBJECT](../sql-reference/functions/is_object)

  * [IS_TIME](../sql-reference/functions/is_time)

  * [IS_TIMESTAMP_*](../sql-reference/functions/is_timestamp)

  * [LENGTH, LEN](../sql-reference/functions/length)

  * [[ NOT ] LIKE](../sql-reference/functions/like)

  * [LPAD](../sql-reference/functions/lpad)

  * [LTRIM](../sql-reference/functions/ltrim)

  * [MD5 , MD5_HEX](../sql-reference/functions/md5)

  * [NULLIF](../sql-reference/functions/nullif)

  * [NVL](../sql-reference/functions/nvl)

  * [NVL2](../sql-reference/functions/nvl2)

  * [OBJECT_CONSTRUCT](../sql-reference/functions/object_construct)

  * [PARSE_IP](../sql-reference/functions/parse_ip)

  * [PARSE_JSON](../sql-reference/functions/parse_json)

  * [PARSE_URL](../sql-reference/functions/parse_url)

  * [PARSE_XML](../sql-reference/functions/parse_xml)

  * [RANDOM](../sql-reference/functions/random)

  * [REGEXP_REPLACE](../sql-reference/functions/regexp_replace)

  * [REGEXP_SUBSTR](../sql-reference/functions/regexp_substr)

  * [REPLACE](../sql-reference/functions/replace)

  * [REVERSE](../sql-reference/functions/reverse)

  * [RPAD](../sql-reference/functions/rpad)

  * [RTRIM](../sql-reference/functions/rtrim)

  * [SPLIT](../sql-reference/functions/split)

  * [SPLIT_PART](../sql-reference/functions/split_part)

  * [STARTSWITH](../sql-reference/functions/startswith)

  * [SUBSTR , SUBSTRING](../sql-reference/functions/substr)

  * [TO_ARRAY](../sql-reference/functions/to_array)

  * [TO_BINARY](../sql-reference/functions/to_binary)

  * [TO_BOOLEAN](../sql-reference/functions/to_boolean)

  * [TO_CHAR , TO_VARCHAR](../sql-reference/functions/to_char)

  * [TO_DATE , DATE](../sql-reference/functions/to_date)

Note that when this function is used to explicitly cast a value, neither the
DATE_FORMAT file format option nor the [DATE_INPUT_FORMAT](../sql-
reference/parameters.html#label-date-input-format) parameter is applied.

  * [TO_DECIMAL , TO_NUMBER , TO_NUMERIC](../sql-reference/functions/to_decimal)

  * [TO_DOUBLE](../sql-reference/functions/to_double)

  * [TO_OBJECT](../sql-reference/functions/to_object)

  * [TO_TIME , TIME](../sql-reference/functions/to_time)

Note that when this function is used to explicitly cast a value, neither the
TIME_FORMAT file format option nor the [TIME_INPUT_FORMAT](../sql-
reference/parameters.html#label-time-input-format) parameter is applied.

  * [TO_TIMESTAMP / TO_TIMESTAMP_*](../sql-reference/functions/to_timestamp)

Note that when this function is used to explicitly cast a value, neither the
TIMESTAMP_FORMAT file format option nor the [TIMESTAMP_INPUT_FORMAT](../sql-
reference/parameters.html#label-timestamp-input-format) parameter is applied.

  * [TO_VARIANT](../sql-reference/functions/to_variant)

  * [TRIM](../sql-reference/functions/trim)

  * [TRY_CAST](../sql-reference/functions/try_cast)

  * [TRY_HEX_DECODE_STRING](../sql-reference/functions/try_hex_decode_string)

  * [TRY_TO_BINARY](../sql-reference/functions/try_to_binary)

  * [TRY_TO_BOOLEAN](../sql-reference/functions/try_to_boolean)

  * [TRY_TO_DATE](../sql-reference/functions/try_to_date)

Note that the COPY INTO _< table>_ command does not support the optional
`_format_` argument for this function.

  * [TRY_TO_DECIMAL, TRY_TO_NUMBER, TRY_TO_NUMERIC](../sql-reference/functions/try_to_decimal)

  * [TRY_TO_DOUBLE](../sql-reference/functions/try_to_double)

  * [TRY_TO_TIME](../sql-reference/functions/try_to_time)

Note that the COPY INTO _< table>_ command does not support the optional
`_format_` argument for this function.

  * [TRY_TO_TIMESTAMP / TRY_TO_TIMESTAMP_*](../sql-reference/functions/try_to_timestamp)

Note that the COPY INTO _< table>_ command does not support the optional
`_format_` argument for this function.

  * [UNICODE](../sql-reference/functions/unicode)

  * [UUID_STRING](../sql-reference/functions/uuid_string)

  * [XMLGET](../sql-reference/functions/xmlget)

Note in particular that the [VALIDATE](../sql-reference/functions/validate)
function ignores the SELECT list in a COPY INTO _< table>_ statement. The
function parses the files referenced in the statement and returns any parsing
errors. This behavior can be surprising if you expect the function to evaluate
the files in the context of the COPY INTO _< table>_ expressions.

Note that COPY transformations do not support the [FLATTEN](../sql-
reference/functions/flatten) function, or [JOIN](../sql-
reference/constructs/join) or [GROUP BY](../sql-reference/constructs/group-by)
(aggregate) syntax.

The list of supported functions might expand over time.

The following categories of functions are also supported:

  * Scalar [SQL UDFs](../developer-guide/udf/sql/udf-sql-introduction).

Note

For Scalar SQL UDFs, Snowflake has limited support for transformation error
handling, and you may encounter inconsistent or unexpected ON_ERROR copy
option behavior.

### Filtering results¶

Filtering the results of a [FROM](../sql-reference/constructs/from) clause
using a [WHERE](../sql-reference/constructs/where) clause is not supported.
The ORDER BY, LIMIT,FETCH,TOP keywords in SELECT statements are also not
supported.

The DISTINCT keyword in SELECT statements is not fully supported. Specifying
the keyword can lead to inconsistent or unexpected ON_ERROR copy option
behavior.

### VALIDATION_MODE parameter¶

The VALIDATION_MODE parameter does not support COPY statements that transform
data during a load.

### CURRENT_TIME, CURRENT_TIMESTAMP default column values¶

Instead of using CURRENT_TIME, CURRENT_TIMESTAMP default column values to
capture load time, we recommend that you query METADATA$START_SCAN_TIME to get
an accurate time value of record loading. For more information, refer to
[Querying Metadata for Staged Files](querying-metadata).

### The MATCH_BY_COLUMN_NAME copy option¶

You are not allowed to use the MATCH_BY_COLUMN_NAME copy option with a SELECT
statement for transforming data during a load in all cases. These two options
can still be used separately, but cannot be used together. Any attempt to do
so will result in the following error: `SQL compilation error:
match_by_column_name is not supported with copy transform`.

## Transforming CSV data¶

### Load a subset of table data¶

Load a subset of data into a table. For any missing columns, Snowflake inserts
the default values. The following example loads data from columns 1, 2, 6, and
7 of a staged CSV file:

>
>     copy into home_sales(city, zip, sale_date, price)
>        from (select t.$1, t.$2, t.$6, t.$7 from @mystage/sales.csv.gz t)
>        FILE_FORMAT = (FORMAT_NAME = mycsvformat);
>  
>
> Copy

### Reorder CSV columns during a load¶

The following example reorders the column data from a staged CSV file before
loading it into a table. Additionally, the COPY statement uses the [SUBSTR ,
SUBSTRING](../sql-reference/functions/substr) function to remove the first few
characters of a string before inserting it:

>
>     copy into home_sales(city, zip, sale_date, price)
>        from (select SUBSTR(t.$2,4), t.$1, t.$5, t.$4 from @mystage t)
>        FILE_FORMAT = (FORMAT_NAME = mycsvformat);
>  
>
> Copy

### Convert data types during a load¶

Convert staged data into other data types during a data load. All [conversion
functions](../sql-reference/functions-conversion) are supported.

For example, convert strings as binary values, decimals, or timestamps using
the [TO_BINARY](../sql-reference/functions/to_binary), [TO_DECIMAL , TO_NUMBER
, TO_NUMERIC](../sql-reference/functions/to_decimal), and [TO_TIMESTAMP /
TO_TIMESTAMP_*](../sql-reference/functions/to_timestamp) functions,
respectively.

Sample CSV file:

>
>     snowflake,2.8,2016-10-5
>     warehouse,-12.3,2017-01-23
>  
>
> Copy

SQL statements:

>
>     -- Stage a data file in the internal user stage
>     PUT file:///tmp/datafile.csv @~;
>  
>     -- Query the staged data file
>     select t.$1,t.$2,t.$3 from @~/datafile.csv.gz t;
>  
>     -- Create the target table
>     create or replace table casttb (
>       col1 binary,
>       col2 decimal,
>       col3 timestamp_ntz
>       );
>  
>     -- Convert the staged CSV column data to the specified data types before
> loading it into the destination table
>     copy into casttb(col1, col2, col3)
>     from (
>       select to_binary(t.$1, 'utf-8'),to_decimal(t.$2, '99.9', 9,
> 5),to_timestamp_ntz(t.$3)
>       from @~/datafile.csv.gz t
>     )
>     file_format = (type = csv);
>  
>     -- Query the target table
>     select * from casttb;
>  
>     +--------------------+------+-------------------------+
>     | COL1               | COL2 | COL3                    |
>     |--------------------+------+-------------------------|
>     | 736E6F77666C616B65 |    3 | 2016-10-05 00:00:00.000 |
>     | 77617265686F757365 |  -12 | 2017-01-23 00:00:00.000 |
>     +--------------------+------+-------------------------+
>  
>
> Copy

### Include sequence columns in loaded data¶

Create a sequence object using [CREATE SEQUENCE](../sql-reference/sql/create-
sequence). When loading data into a table using the COPY command, access the
object using a `NEXTVAL` expression to sequence the data in a target number
column. For more information about using sequences in queries, see [Using
Sequences](querying-sequences).

>
>     -- Create a sequence
>     create sequence seq1;
>  
>     -- Create the target table
>     create or replace table mytable (
>       col1 number default seq1.nextval,
>       col2 varchar,
>       col3 varchar
>       );
>  
>     -- Stage a data file in the internal user stage
>     PUT file:///tmp/myfile.csv @~;
>  
>     -- Query the staged data file
>     select $1, $2 from @~/myfile.csv.gz t;
>  
>     +-----+-----+
>     | $1  | $2  |
>     |-----+-----|
>     | abc | def |
>     | ghi | jkl |
>     | mno | pqr |
>     | stu | vwx |
>     +-----+-----+
>  
>     -- Include the sequence nextval expression in the COPY statement
>     copy into mytable (col1, col2, col3)
>     from (
>       select seq1.nextval, $1, $2
>       from @~/myfile.csv.gz t
>     )
>     ;
>  
>     select * from mytable;
>  
>     +------+------+------+
>     | COL1 | COL2 | COL3 |
>     |------+------+------|
>     |    1 | abc  | def  |
>     |    2 | ghi  | jkl  |
>     |    3 | mno  | pqr  |
>     |    4 | stu  | vwx  |
>     +------+------+------+
>  
>
> Copy

### Include AUTOINCREMENT / IDENTITY columns in loaded data¶

Set the AUTOINCREMENT or IDENTITY default value for a number column. When
loading data into a table using the COPY command, omit the column in the
SELECT statement. The statement automatically populates the column.

>
>     -- Create the target table
>     create or replace table mytable (
>       col1 number autoincrement start 1 increment 1,
>       col2 varchar,
>       col3 varchar
>       );
>  
>     -- Stage a data file in the internal user stage
>     PUT file:///tmp/myfile.csv @~;
>  
>     -- Query the staged data file
>     select $1, $2 from @~/myfile.csv.gz t;
>  
>     +-----+-----+
>     | $1  | $2  |
>     |-----+-----|
>     | abc | def |
>     | ghi | jkl |
>     | mno | pqr |
>     | stu | vwx |
>     +-----+-----+
>  
>     -- Omit the sequence column in the COPY statement
>     copy into mytable (col2, col3)
>     from (
>       select $1, $2
>       from @~/myfile.csv.gz t
>     )
>     ;
>  
>     select * from mytable;
>  
>     +------+------+------+
>     | COL1 | COL2 | COL3 |
>     |------+------+------|
>     |    1 | abc  | def  |
>     |    2 | ghi  | jkl  |
>     |    3 | mno  | pqr  |
>     |    4 | stu  | vwx  |
>     +------+------+------+
>  
>
> Copy

## Transforming semi-structured data¶

The examples in this section apply to any semi-structured data type except
where noted.

### Load semi-structured data into separate columns¶

The following example loads repeating elements from a staged semi-structured
file into separate table columns with different data types.

This example loads the following semi-structured data into separate columns in
a relational table, with the `location` object values loaded into a VARIANT
column and the remaining values loaded into relational columns:

    
    
    -- Sample data:
    {"location": {"city": "Lexington","zip": "40503"},"dimensions": {"sq_ft": "1000"},"type": "Residential","sale_date": "4-25-16","price": "75836"},
    {"location": {"city": "Belmont","zip": "02478"},"dimensions": {"sq_ft": "1103"},"type": "Residential","sale_date": "6-18-16","price": "92567"},
    {"location": {"city": "Winchester","zip": "01890"},"dimensions": {"sq_ft": "1122"},"type": "Condo","sale_date": "1-31-16","price": "89921"}
    

Copy

The following SQL statements load the file `sales.json` from the internal
stage `mystage`:

Note

This example loads JSON data, but the SQL statements are similar when loading
semi-structured data of other types (e.g. Avro, ORC, etc.).

For an additional example using Parquet data, see Load Parquet Data into
Separate Columns (in this topic).

    
    
     -- Create an internal stage with the file type set as JSON.
     CREATE OR REPLACE STAGE mystage
       FILE_FORMAT = (TYPE = 'json');
    
     -- Stage a JSON data file in the internal stage.
     PUT file:///tmp/sales.json @mystage;
    
     -- Query the staged data. The data file comprises three objects in NDJSON format.
     SELECT t.$1 FROM @mystage/sales.json.gz t;
    
     +------------------------------+
     | $1                           |
     |------------------------------|
     | {                            |
     |   "dimensions": {            |
     |     "sq_ft": "1000"          |
     |   },                         |
     |   "location": {              |
     |     "city": "Lexington",     |
     |     "zip": "40503"           |
     |   },                         |
     |   "price": "75836",          |
     |   "sale_date": "2022-08-25", |
     |   "type": "Residential"      |
     | }                            |
     | {                            |
     |   "dimensions": {            |
     |     "sq_ft": "1103"          |
     |   },                         |
     |   "location": {              |
     |     "city": "Belmont",       |
     |     "zip": "02478"           |
     |   },                         |
     |   "price": "92567",          |
     |   "sale_date": "2022-09-18", |
     |   "type": "Residential"      |
     | }                            |
     | {                            |
     |   "dimensions": {            |
     |     "sq_ft": "1122"          |
     |   },                         |
     |   "location": {              |
     |     "city": "Winchester",    |
     |     "zip": "01890"           |
     |   },                         |
     |   "price": "89921",          |
     |   "sale_date": "2022-09-23", |
     |   "type": "Condo"            |
     | }                            |
     +------------------------------+
    
     -- Create a target table for the data.
     CREATE OR REPLACE TABLE home_sales (
       CITY VARCHAR,
       POSTAL_CODE VARCHAR,
       SQ_FT NUMBER,
       SALE_DATE DATE,
       PRICE NUMBER
     );
    
     -- Copy elements from the staged file into the target table.
     COPY INTO home_sales(city, postal_code, sq_ft, sale_date, price)
     FROM (select
     $1:location.city::varchar,
     $1:location.zip::varchar,
     $1:dimensions.sq_ft::number,
     $1:sale_date::date,
     $1:price::number
     FROM @mystage/sales.json.gz t);
    
     -- Query the target table.
     SELECT * from home_sales;
    
    +------------+-------------+-------+------------+-------+
    | CITY       | POSTAL_CODE | SQ_FT | SALE_DATE  | PRICE |
    |------------+-------------+-------+------------+-------|
    | Lexington  | 40503       |  1000 | 2022-08-25 | 75836 |
    | Belmont    | 02478       |  1103 | 2022-09-18 | 92567 |
    | Winchester | 01890       |  1122 | 2022-09-23 | 89921 |
    +------------+-------------+-------+------------+-------+
    

Copy

### Load Parquet data into separate columns¶

Similar to the previous example, but loads semi-structured data from a file in
the Parquet format. This example is provided for users who are familiar with
Apache Parquet:

>
>     -- Create a file format object that sets the file format type. Accept
> the default options.
>     create or replace file format my_parquet_format
>       type = 'parquet';
>  
>     -- Create an internal stage and specify the new file format
>     create or replace temporary stage mystage
>       file_format = my_parquet_format;
>  
>     -- Create a target table for the data.
>     create or replace table parquet_col (
>       custKey number default NULL,
>       orderDate date default NULL,
>       orderStatus varchar(100) default NULL,
>       price varchar(255)
>     );
>  
>     -- Stage a data file in the internal stage
>     put file:///tmp/mydata.parquet @mystage;
>  
>     -- Copy data from elements in the staged Parquet file into separate
> columns
>     -- in the target table.
>     -- Note that all Parquet data is stored in a single column ($1)
>     -- SELECT list items correspond to element names in the Parquet file
>     -- Cast element values to the target column data type
>     copy into parquet_col
>       from (select
>       $1:o_custkey::number,
>       $1:o_orderdate::date,
>       $1:o_orderstatus::varchar,
>       $1:o_totalprice::varchar
>       from @mystage/mydata.parquet);
>  
>     -- Query the target table
>     SELECT * from parquet_col;
>  
>     +---------+------------+-------------+-----------+
>     | CUSTKEY | ORDERDATE  | ORDERSTATUS | PRICE     |
>     |---------+------------+-------------+-----------|
>     |   27676 | 1996-09-04 | O           | 83243.94  |
>     |  140252 | 1994-01-09 | F           | 198402.97 |
>     ...
>     +---------+------------+-------------+-----------+
>  
>
> Copy

### Flatten semi-structured data¶

[FLATTEN](../sql-reference/functions/flatten) is a table function that
produces a lateral view of a VARIANT, OBJECT, or ARRAY column. Using the
sample data from Load semi-structured Data into Separate Columns, create a
table with a separate row for each element in the objects.

    
    
    -- Create an internal stage with the file delimiter set as none and the record delimiter set as the new line character
    create or replace stage mystage
      file_format = (type = 'json');
    
    -- Stage a JSON data file in the internal stage with the default values
    put file:///tmp/sales.json @mystage;
    
    -- Create a table composed of the output from the FLATTEN function
    create or replace table flattened_source
    (seq string, key string, path string, index string, value variant, element variant)
    as
      select
        seq::string
      , key::string
      , path::string
      , index::string
      , value::variant
      , this::variant
      from @mystage/sales.json.gz
        , table(flatten(input => parse_json($1)));
    
      select * from flattened_source;
    
    +-----+-----------+-----------+-------+-------------------------+-----------------------------+
    | SEQ | KEY       | PATH      | INDEX | VALUE                   | ELEMENT                     |
    |-----+-----------+-----------+-------+-------------------------+-----------------------------|
    | 1   | location  | location  | NULL  | {                       | {                           |
    |     |           |           |       |   "city": "Lexington",  |   "location": {             |
    |     |           |           |       |   "zip": "40503"        |     "city": "Lexington",    |
    |     |           |           |       | }                       |     "zip": "40503"          |
    |     |           |           |       |                         |   },                        |
    |     |           |           |       |                         |   "price": "75836",         |
    |     |           |           |       |                         |   "sale_date": "2017-3-5",  |
    |     |           |           |       |                         |   "sq__ft": "1000",         |
    |     |           |           |       |                         |   "type": "Residential"     |
    |     |           |           |       |                         | }                           |
    ...
    | 3   | type      | type      | NULL  | "Condo"                 | {                           |
    |     |           |           |       |                         |   "location": {             |
    |     |           |           |       |                         |     "city": "Winchester",   |
    |     |           |           |       |                         |     "zip": "01890"          |
    |     |           |           |       |                         |   },                        |
    |     |           |           |       |                         |   "price": "89921",         |
    |     |           |           |       |                         |   "sale_date": "2017-3-21", |
    |     |           |           |       |                         |   "sq__ft": "1122",         |
    |     |           |           |       |                         |   "type": "Condo"           |
    |     |           |           |       |                         | }                           |
    +-----+-----------+-----------+-------+-------------------------+-----------------------------+
    

Copy

### Split semi-structured elements and load as VARIANT values into separate
columns¶

Following the instructions in Load semi-structured Data into Separate Columns,
you can load individual elements from semi-structured data into different
columns in your target table. Additionally, using the [SPLIT](../sql-
reference/functions/split) function, you can split element values that contain
a separator and load them as an array.

For example, split IP addresses on the dot separator in repeating elements.
Load the IP addresses as arrays in separate columns:

>
>     -- Create an internal stage with the file delimiter set as none and the
> record delimiter set as the new line character
>     create or replace stage mystage
>       file_format = (type = 'json');
>  
>     -- Stage a semi-structured data file in the internal stage
>     put file:///tmp/ipaddress.json @mystage auto_compress=true;
>  
>     -- Query the staged data
>     select t.$1 from @mystage/ipaddress.json.gz t;
>  
>     +----------------------------------------------------------------------+
>     | $1                                                                   |
>     |----------------------------------------------------------------------|
>     | {"ip_address": {"router1": "192.168.1.1","router2": "192.168.0.1"}}, |
>     | {"ip_address": {"router1": "192.168.2.1","router2": "192.168.3.1"}}  |
>     +----------------------------------------------------------------------+
>  
>     -- Create a target table for the semi-structured data
>     create or replace table splitjson (
>       col1 array,
>       col2 array
>       );
>  
>     -- Split the elements into individual arrays using the SPLIT function
> and load them into separate columns
>     -- Note that all JSON data is stored in a single column ($1)
>     copy into splitjson(col1, col2)
>     from (
>       select split($1:ip_address.router1, '.'),split($1:ip_address.router2,
> '.')
>       from @mystage/ipaddress.json.gz t
>     );
>  
>     -- Query the target table
>     select * from splitjson;
>  
>     +----------+----------+
>     | COL1     | COL2     |
>     |----------+----------|
>     | [        | [        |
>     |   "192", |   "192", |
>     |   "168", |   "168", |
>     |   "1",   |   "0",   |
>     |   "1"    |   "1"    |
>     | ]        | ]        |
>     | [        | [        |
>     |   "192", |   "192", |
>     |   "168", |   "168", |
>     |   "2",   |   "3",   |
>     |   "1"    |   "1"    |
>     | ]        | ]        |
>     +----------+----------+
>  
>
> Copy

