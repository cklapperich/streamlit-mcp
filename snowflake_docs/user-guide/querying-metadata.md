# Querying Metadata for Staged Files¶

Snowflake automatically generates metadata for files in internal (i.e.
Snowflake) stages or external (Amazon S3, Google Cloud Storage, or Microsoft
Azure) stages. This metadata is “stored” in virtual columns that can be:

  * Queried using a standard [SELECT](../sql-reference/sql/select) statement.

  * Loaded into a table, along with the regular data columns, using [COPY INTO <table>](../sql-reference/sql/copy-into-table). For general information about querying staged data files, see [Querying Data in Staged Files](querying-stage).

## Metadata Columns¶

Currently, the following metadata columns can be queried or copied into
tables:

METADATA$FILENAME

    

Name of the staged data file the current row belongs to. Includes the full
path to the data file.

METADATA$FILE_ROW_NUMBER

    

Row number for each record in the staged data file.

METADATA$FILE_CONTENT_KEY

    

Checksum of the staged data file the current row belongs to.

METADATA$FILE_LAST_MODIFIED

    

Last modified timestamp of the staged data file the current row belongs to.
Returned as TIMESTAMP_NTZ.

METADATA$START_SCAN_TIME

    

Start timestamp of operation for each record in the staged data file. Returned
as TIMESTAMP_LTZ.

## Query Limitations¶

  * Metadata cannot be inserted into existing table rows.

  * Metadata columns can only be queried by name; as such, they are not included in the output of any of the following statements:

>     * [SELECT *](../sql-reference/sql/select)
>
>     * [SHOW <objects>](../sql-reference/sql/show)
>
>     * [DESCRIBE <object>](../sql-reference/sql/desc)
>
>     * [Queries on INFORMATION_SCHEMA views](../sql-reference/info-schema)

## Query Examples¶

### Example 1: Querying the Metadata Columns for a CSV File¶

The following example illustrates staging multiple CSV data files (with the
same file format) and then querying the metadata columns, as well as the
regular data columns, in the files.

This example assumes the files have the following names and are located in the
root directory in a macOS or Linux environment:

  * `/tmp/data1.csv` contains two records:
    
        a|b
    c|d
    

Copy

  * `/tmp/data2.csv` contains two records:
    
        e|f
    g|h
    

Copy

To stage and query the files:

>
>     -- Create a file format
>     CREATE OR REPLACE FILE FORMAT myformat
>       TYPE = 'csv' FIELD_DELIMITER = '|';
>  
>     -- Create an internal stage
>     CREATE OR REPLACE STAGE mystage1;
>  
>     -- Stage a data file
>     PUT file:///tmp/data*.csv @mystage1;
>  
>     -- Query the filename and row number metadata columns and the regular
> data columns in the staged file
>     -- Note that the table alias is provided to make the statement easier to
> read and is not required
>     SELECT METADATA$FILENAME, METADATA$FILE_ROW_NUMBER,
> METADATA$FILE_CONTENT_KEY, METADATA$FILE_LAST_MODIFIED,
> METADATA$START_SCAN_TIME, t.$1, t.$2 FROM @mystage1 (file_format =>
> myformat) t;
>  
>
> +-------------------+--------------------------+---------------------------+-----------------------------+-------------------------------+----+----+
>     | METADATA$FILENAME | METADATA$FILE_ROW_NUMBER | METADATA$FILE_CONTENT_KEY | METADATA$FILE_LAST_MODIFIED |      METADATA$START_SCAN_TIME | $1 | $2 |
>
> |-------------------+--------------------------+---------------------------+-----------------------------+-------------------------------+----+----|
>     | data2.csv.gz      |                        1 | aaa11bb2cccccaaaaac1234d9 |     2022-05-01 10:15:57.000 |  2023-02-02 01:31:00.713 +0000| e  | f  |
>     | data2.csv.gz      |                        2 | aa387aabb2ccedaaaaac123b8 |     2022-05-01 10:05:35.000 |  2023-02-02 01:31:00.755 +0000| g  | h  |
>     | data1.csv.gz      |                        1 | 39ab11bb2cdeacdcdac1234d9 |     2022-08-03 10:15:26.000 |  2023-02-02 01:31:00.778 +0000| a  | b  |
>     | data1.csv.gz      |                        2 | 2289aab2abcdeaacaaac348d0 |     2022-09-10 11:15:55.000 |  2023-02-02 01:31:00.778 +0000| c  | d  |
>
> +-------------------+--------------------------+---------------------------+-----------------------------+-------------------------------+----+----+
>  
>     SELECT METADATA$FILENAME, METADATA$FILE_ROW_NUMBER,
> METADATA$FILE_CONTENT_KEY, METADATA$FILE_LAST_MODIFIED,
> METADATA$START_SCAN_TIME, t.$1, t.$2 FROM @mystage1 t;
>  
>
> +-------------------+--------------------------+---------------------------+-----------------------------+-------------------------------+-----+------+
>     | METADATA$FILENAME | METADATA$FILE_ROW_NUMBER | METADATA$FILE_CONTENT_KEY | METADATA$FILE_LAST_MODIFIED |      METADATA$START_SCAN_TIME | $1  | $2   |
>
> |-------------------+--------------------------+---------------------------+-----------------------------+-------------------------------+-----+------|
>     | data2.csv.gz      |                        1 | aaa11bb2cccccaaaaac1234d9 |     2022-05-01 10:15:57.000 |  2023-02-02 01:31:00.713 +0000| e|f | NULL |
>     | data2.csv.gz      |                        2 | aa387aabb2ccedaaaaac123b8 |     2022-05-01 10:05:35.000 |  2023-02-02 01:31:00.755 +0000| g|h | NULL |
>     | data1.csv.gz      |                        1 | 39ab11bb2cdeacdcdac1234d9 |     2022-08-03 10:15:26.000 |  2023-02-02 01:31:00.778 +0000| a|b | NULL |
>     | data1.csv.gz      |                        2 | 2289aab2abcdeaacaaac348d0 |     2022-09-10 11:15:55.000 |  2023-02-02 01:31:00.778 +0000| c|d | NULL |
>
> +-------------------+--------------------------+---------------------------+-----------------------------+-------------------------------+-----+------+
>  
>
> Copy

Note

The file format is required in this example to correctly parse the fields in
the staged files. In the second query, the file format is omitted, causing the
`|` field delimiter to be ignored and resulting in the values returned for
`$1` and `$2`.

However, if the file format is included in the stage definition, you can omit
it from the SELECT statement. See the next example for details.

### Example 2: Querying the Metadata Columns for a JSON File¶

This example illustrates staging a JSON data file containing the following
objects and then querying the metadata columns, as well as the objects, in the
file:

>
>     {"a": {"b": "x1","c": "y1"}},
>     {"a": {"b": "x2","c": "y2"}}
>  
>
> Copy

This example assumes the file is named `/tmp/data1.json` and is located in the
root directory in a macOS or Linux environment.

To stage and query the file:

>
>     -- Create a file format
>     CREATE OR REPLACE FILE FORMAT my_json_format
>       TYPE = 'json';
>  
>     -- Create an internal stage
>     CREATE OR REPLACE STAGE mystage2
>       FILE_FORMAT = my_json_format;
>  
>     -- Stage a data file
>     PUT file:///tmp/data1.json @mystage2;
>  
>     -- Query the filename and row number metadata columns and the regular
> data columns in the staged file
>     SELECT METADATA$FILENAME, METADATA$FILE_ROW_NUMBER, parse_json($1) FROM
> @mystage2/data1.json.gz;
>  
>     +-------------------+--------------------------+----------------+
>     | METADATA$FILENAME | METADATA$FILE_ROW_NUMBER | PARSE_JSON($1) |
>     |-------------------+--------------------------+----------------|
>     | data1.json.gz     |                        1 | {              |
>     |                   |                          |   "a": {       |
>     |                   |                          |     "b": "x1", |
>     |                   |                          |     "c": "y1"  |
>     |                   |                          |   }            |
>     |                   |                          | }              |
>     | data1.json.gz     |                        2 | {              |
>     |                   |                          |   "a": {       |
>     |                   |                          |     "b": "x2", |
>     |                   |                          |     "c": "y2"  |
>     |                   |                          |   }            |
>     |                   |                          | }              |
>     +-------------------+--------------------------+----------------+
>  
>
> Copy

### Example 3: Loading Metadata Columns into a Table¶

The [COPY INTO <table>](../sql-reference/sql/copy-into-table) command supports
copying metadata from staged data files into a target table. Use the data
transformation syntax (i.e. a SELECT list) in your COPY statement. For more
information about transforming data using a COPY statement, see [Transforming
data during a load](data-load-transform).

The following example loads the metadata columns and regular data columns from
Example 1: Querying the Metadata Columns for a CSV File into a table:

>
>     CREATE OR REPLACE TABLE table1 (
>       filename varchar,
>       file_row_number int,
>       file_content_key varchar,
>       file_last_modified timestamp_ntz,
>       start_scan_time timestamp_ltz,
>       col1 varchar,
>       col2 varchar
>     );
>  
>     COPY INTO table1(filename, file_row_number, file_content_key,
> file_last_modified, start_scan_time, col1, col2)
>       FROM (SELECT METADATA$FILENAME, METADATA$FILE_ROW_NUMBER,
> METADATA$FILE_CONTENT_KEY, METADATA$FILE_LAST_MODIFIED,
> METADATA$START_SCAN_TIME, t.$1, t.$2 FROM @mystage1/data1.csv.gz
> (file_format => myformat) t);
>  
>     SELECT * FROM table1;
>  
>
> +--------------+-----------------+---------------------------+-------------------------+-------------------------------+------+------+
>     | FILENAME     | FILE_ROW_NUMBER | FILE_CONTENT_KEY          | FILE_LAST_MODIFIED      |  START_SCAN_TIME              | COL1 | COL2 |
>
> |--------------+-----------------+---------------------------+-------------------------+-------------------------------+------+------+
>     | data1.csv.gz | 1               | 39ab11bb2cdeacdcdac1234d9 | 2022-08-03 10:15:26.000 | 2023-02-02 01:31:00.778 +0000 | a    | b    |
>     | data1.csv.gz | 2               | 2289aab2abcdeaacaaac348d0 | 2022-09-10 11:15:55.000 | 2023-02-02 01:31:00.778 +0000 | c    | d    |
>
> +--------------+-----------------+---------------------------+-------------------------+-------------------------------+------+------+
>  
>
> Copy

