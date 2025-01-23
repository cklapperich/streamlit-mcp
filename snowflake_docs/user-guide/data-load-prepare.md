# Preparing to load data¶

This topic provides an overview of supported data file formats and data
compression. Depending on your data’s structure, you might need to
[prepare](data-load-considerations-prepare) the data before loading it.

## Supported data types¶

See [SQL data types reference](../sql-reference-data-types) for descriptions
of the data types supported by Snowflake.

## Data file compression¶

We recommend that you compress your data files when you are loading large data
sets. See [CREATE FILE FORMAT](../sql-reference/sql/create-file-format) for
the compression algorithms supported for each data type.

When loading compressed data, Snowflake will automatically determine the file
and codec compression method for your data files. The COMPRESSION file format
option describes how your data files are already compressed in the stage. Set
the COMPRESSION option in one of the following ways:

>   * As a file format option specified directly in the [COPY INTO
> <table>](../sql-reference/sql/copy-into-table) statement.
>
>   * As a file format option specified for a named file format or stage
> object. The named file format/stage object can then be referenced in the
> COPY INTO _< table>_ statement.
>
>

## Supported file formats¶

The following file formats are supported:

> Structured/Semi-structured | Type | Notes  
> ---|---|---  
> Structured | Delimited (CSV, TSV, etc.) | Any valid singlebyte delimiter is supported; default is comma (i.e. CSV).  
> Semi-structured | JSON |   
> | Avro | Includes automatic detection and processing of compressed Avro files.  
> | ORC | Includes automatic detection and processing of compressed ORC files.  
> | Parquet | Includes automatic detection and processing of compressed Parquet files. . . Currently, Snowflake supports the schema of Parquet files produced using the Parquet writer v1. Files produced using v2 of the writer are not supported.  
> | XML | Supported as a [preview](../release-notes/preview-features) feature.  
  
File format options specify the type of data contained in a file, as well as
other related characteristics about the format of the data. The file format
options you can specify are different depending on the type of data you plan
to load. Snowflake provides a full set of file format option defaults.

### Semi-structured file formats¶

Snowflake natively supports semi-structured data, which means semi-structured
data can be loaded into relational tables without requiring the definition of
a schema in advance. Snowflake supports loading semi-structured data directly
into columns of type VARIANT (see [Semi-structured data types](../sql-
reference/data-types-semistructured) for more details).

Currently supported semi-structured data formats include JSON, Avro, ORC,
Parquet, or XML:

  * For JSON, Avro, ORC, and Parquet data, each top-level, complete object is loaded as a separate row in the table. Each object can contain new line characters and spaces as long as the object is valid.

  * For XML data, each top-level element is loaded as a separate row in the table. An element is identified by a start and close tag of the same name.

Typically, tables used to store semi-structured data consist of a single
VARIANT column. Once the data is loaded, you can query the data similar to
structured data. You can also perform other tasks, such as extracting values
and objects from arrays. For more information, see the [FLATTEN](../sql-
reference/functions/flatten) table function.

Note

Semi-structured data can be loaded into tables with multiple columns, but the
semi-structured data must be stored as a field in a structured file (e.g. CSV
file). Then, the data can be loaded into a specified column in the table.

### Named file formats¶

Snowflake supports creating named file formats, which are database objects
that encapsulate all of the required format information. Named file formats
can then be used as input in all the same places where you can specify
individual file format options, thereby helping to streamline the data loading
process for similarly-formatted data.

Named file formats are optional, but are recommended when you plan to load
similarly formatted data on a regular basis.

#### Creating a named file format¶

You can create a file format using either the web interface or SQL:

> Snowsight:
>  
>
>   1. Select Data » Databases.
>
>   2. Locate a database and select the schema to which you want to add the
> file format.
>
>   3. Select Create » File Format.
>
>   4. Complete the SQL statement and select Create File Format.
>
>

> Classic Console:
>  
>
>   1. Select Databases [![Databases tab](../_images/ui-navigation-database-
> icon.svg)](../_images/ui-navigation-database-icon.svg) » _< db_name>_ » File
> Formats.
>
>   2. Select Create… and complete the prompts in the dialog.
>
>

> SQL:
>  
>
> [CREATE FILE FORMAT](../sql-reference/sql/create-file-format)

For descriptions of all file format options and the default values, see
[CREATE FILE FORMAT](../sql-reference/sql/create-file-format).

## Supported copy options¶

Copy options determine the behavior of a data load with regard to error
handling, maximum data size, and so on.

For descriptions of all copy options and the default values, see [COPY INTO
<table>](../sql-reference/sql/copy-into-table).

### Overriding default file format and copy options¶

You can specify the desired load behavior (i.e. override the default settings)
in any of the following locations:

In the table definition:

    

Not recommended.

In the named stage definition:

    

Not recommended.

Directly in the COPY INTO TABLE statement when loading data:

    

Explicitly set the options separately. For more information, see [COPY INTO
<table>](../sql-reference/sql/copy-into-table).

Note

Do not specify copy options using the CREATE STAGE, ALTER STAGE, CREATE TABLE,
or ALTER TABLE commands. We recommend that you use the [COPY INTO
<table>](../sql-reference/sql/copy-into-table) command to specify copy
options.

If file format options or copy options are specified in multiple locations,
the load operation applies the options in the following order of precedence:

  1. COPY INTO TABLE statement.

  2. Stage definition.

  3. Table definition.

Note

File format options set in multiple locations are not cumulative. Any options
set in one place override all options (whether the same or different options)
set lower in the order of precedence.

Copy options set in multiple locations are cumulative. Individual options set
in one place override the same option set lower in the order of precedence.

