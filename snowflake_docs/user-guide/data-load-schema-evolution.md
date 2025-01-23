# Table schema evolution¶

Semi-structured data tends to evolve over time. Systems that generate data add
new columns to accommodate additional information, which requires downstream
tables to evolve accordingly.

The structure of tables in Snowflake can evolve automatically to support the
structure of new data received from the data sources. Snowflake supports the
following:

>   * Automatically adding new columns.
>
>   * Automatically dropping the NOT NULL constraint from columns that are
> missing in new data files.
>
>

To enable table schema evolution, do the following:

>   * If you are creating a new table, set the `ENABLE_SCHEMA_EVOLUTION`
> parameter to TRUE when you use the [CREATE TABLE](../sql-
> reference/sql/create-table) command.
>
>   * For an existing table, modify the table using the [ALTER TABLE](../sql-
> reference/sql/alter-table) command and set the `ENABLE_SCHEMA_EVOLUTION`
> parameter to TRUE.
>
>

Loading data from files evolves the table columns when all of the following
are true:

>   * The Snowflake table has the `ENABLE_SCHEMA_EVOLUTION` parameter set to
> TRUE.
>
>   * The [COPY INTO <table>](../sql-reference/sql/copy-into-table) statement
> uses the `MATCH_BY_COLUMN_NAME` option.
>
>   * The role used to load the data has the EVOLVE SCHEMA or OWNERSHIP
> privilege on the table.
>
>

Additionally, for schema evolution with CSV, when used with
`MATCH_BY_COLUMN_NAME` and `PARSE_HEADER`, `ERROR_ON_COLUMN_COUNT_MISMATCH`
must be set to false.

Schema evolution is a standalone feature but can be used in conjunction with
the [schema detection support for retrieving the column definitions](data-
load-overview.html#label-detect-column-definitions-in-semi-structured-data-
files) from a set of files in cloud storage. In combination, these features
enable continuous data pipelines to create new tables from a set of data files
in cloud storage and then modify columns of the tables as the schema of new
source data files evolves with column additions or deletions.

## Usage notes¶

>   * This feature supports Apache Avro, Apache Parquet, CSV, JSON, and ORC
> files.
>
>   * This feature is limited to [COPY INTO <table>](../sql-
> reference/sql/copy-into-table) statements and Snowpipe data loads. INSERT
> operations cannot evolve the target table schema automatically.
>
>   * [Snowpipe Streaming](data-load-snowpipe-streaming-overview) data loads
> using the Snowflake Ingest SDK directly are not supported with schema
> evolution. [The Kafka connector with Snowpipe Streaming](data-load-snowpipe-
> streaming-kafka-schema-detection) supports schema detection and evolution.
>
>   * By default, this feature is limited to adding a maximum of 10 columns or
> evolving no more than 1 schema per COPY operation. To request more than 10
> added columns or 1 schema per COPY operation, contact [Snowflake
> Support](https://docs.snowflake.com/user-guide/contacting-support).
>
>   * There is no limit on dropping NOT NULL column constraints.
>
>   * Schema evolution is tracked by the `SchemaEvolutionRecord` output in the
> following views and commands: [INFORMATION_SCHEMA COLUMNS View](../sql-
> reference/info-schema/columns), [ACCOUNT_USAGE COLUMNS View](../sql-
> reference/account-usage/columns), [DESCRIBE TABLE command](../sql-
> reference/sql/desc-table), and [SHOW COLUMNS command](../sql-
> reference/sql/show-columns).
>
> However, for the Kafka connector with Snowpipe Streaming, schema evolution
> is not tracked by the `SchemaEvolutionRecord` output. The
> `SchemaEvolutionRecord` output always shows NULL.
>
>   * When a column is manually renamed or modified after a schema evolution,
> the schema evolution record will be cleared.
>
>   * Schema evolution is not supported by [tasks](tasks-intro).
>
>

## Examples¶

The following example creates a table with column definitions derived from a
set of Parquet data. With automatic table schema evolution enabled for the
table, further data loads from Parquet files with additional name/value pairs
automatically add columns to the table:

Note that the `mystage` stage and `my_parquet_format` file format referenced
in the statement must already exist. A set of files must already be staged in
the cloud storage location referenced in the stage definition.

This example builds on an example in the [INFER_SCHEMA](../sql-
reference/functions/infer_schema) topic:

>
>     -- Create table t1 in schema d1.s1, with the column definitions derived
> from the staged file1.parquet file.
>     USE SCHEMA d1.s1;
>  
>     CREATE OR REPLACE TABLE t1
>       USING TEMPLATE (
>         SELECT ARRAY_AGG(object_construct(*))
>           FROM TABLE(
>             INFER_SCHEMA(
>               LOCATION=>'@mystage/file1.parquet',
>               FILE_FORMAT=>'my_parquet_format'
>             )
>           ));
>  
>     -- Row data in file1.parquet.
>     +------+------+------+
>     | COL1 | COL2 | COL3 |
>     |------+------+------|
>     | a    | b    | c    |
>     +------+------+------+
>  
>     -- Describe the table.
>     -- Note that column c2 is required in the Parquet file metadata.
> Therefore, the NOT NULL constraint is set for the column.
>     DESCRIBE TABLE t1;
>
> +------+-------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+
>     | name | type              | kind   | null? | default | primary key | unique key | check | expression | comment | policy name |
>
> |------+-------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------|
>     | COL1 | VARCHAR(16777216) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
>     | COL2 | VARCHAR(16777216) | COLUMN | N     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
>     | COL3 | VARCHAR(16777216) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
>
> +------+-------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+
>  
>     -- Use the SECURITYADMIN role or another role that has the global MANAGE
> GRANTS privilege.
>     -- Grant the EVOLVE SCHEMA privilege to any other roles that could
> insert data and evolve table schema in addition to the table owner.
>  
>     GRANT EVOLVE SCHEMA ON TABLE d1.s1.t1 TO ROLE r1;
>  
>     -- Enable schema evolution on the table.
>     -- Note that the ENABLE_SCHEMA_EVOLUTION property can also be set at
> table creation with CREATE OR REPLACE TABLE
>     ALTER TABLE t1 SET ENABLE_SCHEMA_EVOLUTION = TRUE;
>  
>     -- Load a new set of data into the table.
>     -- The new data drops the NOT NULL constraint on the col2 column.
>     -- The new data adds the new column col4.
>     COPY INTO t1
>       FROM @mystage/file2.parquet
>       FILE_FORMAT = (type=parquet)
>       MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;
>  
>     -- Row data in file2.parquet.
>     +------+------+------+
>     | col1 | COL3 | COL4 |
>     |------+------+------|
>     | d    | e    | f    |
>     +------+------+------+
>  
>     -- Describe the table.
>     DESCRIBE TABLE t1;
>
> +------+-------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
>     | name | type              | kind   | null? | default | primary key | unique key | check | expression | comment | policy name | schema evolution record                                                                                                                                                                  |
>
> |------+-------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
>     | COL1 | VARCHAR(16777216) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL                                                                                                                                                                                     |
>     | COL2 | VARCHAR(16777216) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | {"evolutionType":"DROP_NOT_NULL","evolutionMode":"COPY","fileName":"file2.parquet","triggeringTime":"2024-03-15 23:52:59.514000000Z","queryId":"01b303b8-0808-c9ed-0000-0971491b5932"}   |
>     | COL3 | VARCHAR(16777216) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL                                                                                                                                                                                     |
>     | COL4 | VARCHAR(16777216) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | {"evolutionType":"ADD_COLUMN","evolutionMode":"COPY","fileName":"file2.parquet","triggeringTime":"2024-03-15 23:52:59.514000000Z","queryId":"01b303b8-0808-c9ed-0000-0971491b5932"}      |
>
> +------+-------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
>     -- Note that since MATCH_BY_COLUMN_NAME is set as CASE_INSENSITIVE, all
> column names are retrieved as uppercase letters.
>  
>
> Copy

