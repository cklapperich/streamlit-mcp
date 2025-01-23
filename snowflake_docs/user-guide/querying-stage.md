# Querying Data in Staged Files¶

Snowflake supports using standard SQL to query data files located in an
internal (i.e. Snowflake) stage or _named_ external (Amazon S3, Google Cloud
Storage, or Microsoft Azure) stage. This can be useful for inspecting/viewing
the contents of the staged files, particularly before loading or after
unloading data.

In addition, by referencing [metadata columns](querying-metadata) in a staged
file, a staged data query can return additional information, such as filename
and row numbers, about the file.

Snowflake utilizes support for staged data queries to enable [transforming
data during loading](data-load-transform).

Note

This functionality is primarily for performing simple queries only,
particularly when loading and/or transforming data, and is not intended to
replace loading data into tables and performing queries on the tables.

## Query Syntax and Parameters¶

Query staged data files using a [SELECT](../sql-reference/sql/select)
statement with the following syntax:

>
>     SELECT [<alias>.]$<file_col_num>[:<element>] [ ,
> [<alias>.]$<file_col_num>[:<element>] , ...  ]
>       FROM { <internal_location> | <external_location> }
>       [ ( FILE_FORMAT => '<namespace>.<named_file_format>', PATTERN =>
> '<regex_pattern>' ) ]
>       [ <alias> ]
>  
>
> Copy

For the syntax for transforming data during a load, see [COPY INTO
<table>](../sql-reference/sql/copy-into-table).

Important

The list of objects returned for an external stage may include one or more
“directory blobs”; essentially, paths that end in a forward slash character
(`/`), e.g.:

    
    
    LIST @my_gcs_stage;
    
    +---------------------------------------+------+----------------------------------+-------------------------------+
    | name                                  | size | md5                              | last_modified                 |
    |---------------------------------------+------+----------------------------------+-------------------------------|
    | my_gcs_stage/load/                    |  12  | 12348f18bcb35e7b6b628ca12345678c | Mon, 11 Sep 2019 16:57:43 GMT |
    | my_gcs_stage/load/data_0_0_0.csv.gz   |  147 | 9765daba007a643bdff4eae10d43218y | Mon, 11 Sep 2019 18:13:07 GMT |
    +---------------------------------------+------+----------------------------------+-------------------------------+
    

Copy

These blobs are listed when directories are created in the Google Cloud
console rather than using any other tool provided by Google.

SELECT statements that reference a stage can fail when the object list
includes directory blobs. To avoid errors, we recommend using file pattern
matching to identify the files for inclusion (i.e. the PATTERN clause) when
the file list for a stage includes directory blobs.

### Required Parameters¶

`[_alias_.]$_file_col_num_[:_element_] [ ,
[_alias_.]$_file_col_num_[:_element_] , ... ]`

    

Specifies an explicit set of fields/columns in data files staged in either an
internal or external location, where:

`_alias_`

    

Specifies the optional “table” alias defined, if any, in the FROM clause.

`_file_col_num_`

    

Specifies the positional number of the field/column (in the file) that
contains the data to be loaded (`1` for the first field, `2` for the second
field, etc.)

`_element_`

    

Specifies the path and element name of a repeating value (applies only to
semi-structured data files).

`_internal_location_` or `_external_location_`

    

Specifies the location where the data files are staged:

  * `_internal_location_` is the URI specifier for the location in Snowflake where files containing data are staged:

`@[_namespace_.]_internal_stage_name_[/_path_]` | Files are in the specified named internal stage.  
---|---  
`@[_namespace_.]%_table_name_[/_path_]` | Files are in the stage for the specified table.  
`@~[/_path_]` | Files are in the stage for the current user.  
  * `_external_location_` is the URI specifier for the named external stage or external location (Amazon S3, Google Cloud Storage, or Microsoft Azure) where files containing data are staged:

`@[_namespace_.]_external_stage_name_[/_path_]` | Files are in the specified named external stage.  
---|---  

Where:

>   * `_namespace_` is the database and/or schema in which the internal or
> external stage resides. It is optional if a database and schema are
> currently in use within the user session; otherwise, it is required.
>
>   * The optional `_path_` parameter restricts the set of files being queried
> to the files under the folder prefix. If `_path_` is specified, but no file
> is explicitly named in the path, all data files in the path are queried.
>
>

Note

  * The URI string for an external storage location (Amazon S3, Google Cloud Storage, or Microsoft Azure) must be enclosed in single quotes; however, you can enclose any URI string in single quotes, which allows special characters, including spaces, in location and file names. For example:

> Internal:
>  
>
> `'@~/path 1/file 1.csv'`
>
> `'@%my table/path 1/file 1.csv'`
>
> `'@my stage/path 1/file 1.csv'`

  * Relative path modifiers such as `/./` and `/../` are interpreted literally, because “paths” are literal prefixes for a name. For example:

> S3:
>  
>
> `COPY INTO mytable FROM @mystage/./../a.csv`

In these COPY statements, the system look for a file literally named
`./../a.csv` in the storage location.

### Optional Parameters¶

`( FILE_FORMAT => '_namespace_._named_file_format_ ' )`

    

Specifies a named file format that describes the format of the staged data
files to query.

Note that this parameter is optional if either of the following conditions are
true:

  * The files are formatted in the default file format (CSV) with the default delimiters: `,` (as the field delimiter) and the new line character (as the record delimiter).

  * The files are in an internal or external stage and the stage definition describes the file format.

If referencing a file format in the current namespace for your user session,
you can omit the single quotes around the format identifier.

Otherwise, this parameter is required. For more details, see File Formats (in
this topic).

`_namespace_` optionally specifies the database and/or schema for the table,
in the form of `_database_name_._schema_name_` or `_schema_name_`. It is
optional if a database and schema are currently in use within the user
session; otherwise, it is required.

If the identifier contains spaces, special characters, or mixed-case
characters, the entire string must be enclosed in double quotes. Identifiers
enclosed in double quotes are also case-sensitive.

`PATTERN => '_regex_pattern_ '`

    

A regular expression pattern string, enclosed in single quotes, specifying the
file names and/or paths on the external stage to match.

Tip

For the best performance, try to avoid applying patterns that filter on a
large number of files.

`_alias_`

    

Specifies a “table” alias for the internal/external location where the files
are staged.

## File Formats¶

To parse a staged data file, it is necessary to describe its file format. The
default file format is character-delimited UTF-8 text (i.e. CSV), with the
comma character (`,`) as the field delimiter and new line character as the
record delimiter. If the source data is in another format (JSON, Avro, etc.),
you must specify the corresponding file format type (and options).

To explicitly specify file format options, set them in one of the following
ways:

Querying staged data files:

    

As file format options specified for a named file format or stage object. The
named file format/stage object can then be referenced in the SELECT statement.

Loading columns from staged data files:

    

  * As file format options specified directly in the [COPY INTO <table>](../sql-reference/sql/copy-into-table).

  * As file format options specified for a named file format or stage object. The named file format/stage object can then be referenced in the [COPY INTO <table>](../sql-reference/sql/copy-into-table) statement.

## Query Examples¶

### Example 1: Querying Columns in a CSV File¶

The following example illustrates staging multiple CSV data files (with the
same file format) and then querying the data columns in the files.

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
>     -- Create a file format.
>     CREATE OR REPLACE FILE FORMAT myformat TYPE = 'csv' FIELD_DELIMITER =
> '|';
>  
>     -- Create an internal stage.
>     CREATE OR REPLACE STAGE mystage1;
>  
>     -- Stage the data files.
>     PUT file:///tmp/data*.csv @mystage1;
>  
>     -- Query the filename and row number metadata columns and the regular
> data columns in the staged file.
>     -- Optionally apply pattern matching to the set of files in the stage
> and optional path.
>     -- Note that the table alias is provided to make the statement easier to
> read and is not required.
>     SELECT t.$1, t.$2 FROM @mystage1 (file_format => 'myformat',
> pattern=>'.*data.*[.]csv.gz') t;
>  
>     +----+----+
>     | $1 | $2 |
>     |----+----|
>     | a  | b  |
>     | c  | d  |
>     | e  | f  |
>     | g  | h  |
>     +----+----+
>  
>     SELECT t.$1, t.$2 FROM @mystage1 t;
>  
>     +-----+------+
>     | $1  | $2   |
>     |-----+------|
>     | a|b | NULL |
>     | c|d | NULL |
>     | e|f | NULL |
>     | g|h | NULL |
>     +-----+------+
>  
>
> Copy

Note

The file format is required in this example to correctly parse the fields in
the staged files. In the second query, the file format is omitted, causing the
`|` field delimiter to be ignored and resulting in the values returned for
`$1` and `$2`.

However, if the file format is included in the stage definition, you can omit
it from the SELECT statement. See Example 3: Querying Elements in a JSON File.

### Example 2: Calling Functions when Querying a Staged Data File¶

Get the ASCII code for the first character of each column in the data files
staged in Example 1: Querying Columns in a CSV File:

>
>     SELECT ascii(t.$1), ascii(t.$2) FROM @mystage1 (file_format => myformat)
> t;
>  
>     +-------------+-------------+
>     | ASCII(T.$1) | ASCII(T.$2) |
>     |-------------+-------------|
>     |          97 |          98 |
>     |          99 |         100 |
>     |         101 |         102 |
>     |         103 |         104 |
>     +-------------+-------------+
>  
>
> Copy

Note

If the file format is included in the stage definition, you can omit it from
the SELECT statement. See Example 3: Querying Elements in a JSON File.

### Example 3: Querying Elements in a JSON File¶

This example illustrates staging a JSON data file containing the following
objects and then querying individual elements within the objects in the file:

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
>     CREATE OR REPLACE FILE FORMAT my_json_format TYPE = 'json';
>  
>     -- Create an internal stage
>     CREATE OR REPLACE STAGE mystage2 FILE_FORMAT = my_json_format;
>  
>     -- Stage the data file
>     PUT file:///tmp/data1.json @mystage2;
>  
>     -- Query the repeating a.b element in the staged file
>     SELECT parse_json($1):a.b FROM @mystage2/data1.json.gz;
>  
>     +--------------------+
>     | PARSE_JSON($1):A.B |
>     |--------------------|
>     | "x1"               |
>     | "x2"               |
>     +--------------------+
>  
>
> Copy

