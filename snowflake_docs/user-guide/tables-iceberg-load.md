# Load data into Apache Iceberg™ tables¶

Snowflake supports the following options for loading data into a Snowflake-
managed Iceberg table:

  * [INSERT](../sql-reference/sql/insert)

  * [COPY INTO <table>](../sql-reference/sql/copy-into-table)

  * [Snowpipe](data-load-snowpipe-intro)

  * [Using Snowpipe Streaming with Apache Iceberg™ tables](data-load-snowpipe-streaming-iceberg)

  * [Using the Snowflake Connector for Kafka with Apache Iceberg™ tables](kafka-connector-iceberg)

## File formats¶

You can load data into an Iceberg table from files in any of the formats
supported for loading into standard Snowflake tables.

For CSV, JSON, Avro, and ORC, Snowflake converts the data from non-Parquet
file formats into Iceberg Parquet files and stores the data in the base
location of the Iceberg table. Only the default `LOAD_MODE = FULL_INGEST`
option is supported for these file format loading scenarios that require type
conversion.

For Apache Parquet files, Snowflake loads the data directly into table columns
and lets you choose between the following `LOAD_MODE` options:

  * `FULL_INGEST`: Scans the files and rewrites the Parquet data under the base location of the Iceberg table.

  * `ADD_FILES_COPY`: Binary copies the Iceberg-compatible Apache Parquet files that aren’t registered with an Iceberg catalog into the base location of the Iceberg table, then registers the files to the Iceberg table.

For more information, see [COPY INTO <table>](../sql-reference/sql/copy-into-
table).

## Example: Load Iceberg-compatible Parquet files¶

This example covers how to create an Iceberg table and then load data into it
from Iceberg-compatible Parquet data files on an external stage.

For demonstration purposes, this example uses the following resources:

  * An external volume named `iceberg_ingest_vol`. To create an external volume, see [Configure an external volume](tables-iceberg-configure-external-volume).

  * An external stage named `my_parquet_stage` with Iceberg-compatible Parquet files on it. To create an external stage, see [CREATE STAGE](../sql-reference/sql/create-stage).

  1. Create a file format object that describes the staged Parquet files, using the required configuration for copying Iceberg-compatible Parquet data (`TYPE = PARQUET USE_VECTORIZED_SCANNER = TRUE`):
    
        CREATE OR REPLACE FILE FORMAT my_parquet_format
      TYPE = PARQUET
      USE_VECTORIZED_SCANNER = TRUE;
    

Copy

  2. Create a Snowflake-managed Iceberg table, defining columns with data types that are compatible with the source Parquet file data types:
    
        CREATE OR REPLACE ICEBERG TABLE customer_iceberg_ingest (
      c_custkey INTEGER,
      c_name STRING,
      c_address STRING,
      c_nationkey INTEGER,
      c_phone STRING,
      c_acctbal INTEGER,
      c_mktsegment STRING,
      c_comment STRING
    )
      CATALOG='SNOWFLAKE'
      EXTERNAL_VOLUME='iceberg_ingest_vol'
      BASE_LOCATION='customer_iceberg_ingest/';
    

Copy

Note

The example statement specifies Iceberg data types that map to Snowflake data
types. For more information, see [Data types for Apache Iceberg™
tables](tables-iceberg-data-types).

  3. Use a COPY INTO statement to load the data from the staged Parquet files (located directly under the stage URL path) into the Iceberg table:
    
        COPY INTO customer_iceberg_ingest
      FROM @my_parquet_stage
      FILE_FORMAT = 'my_parquet_format'
      LOAD_MODE = ADD_FILES_COPY
      PURGE = TRUE
      MATCH_BY_COLUMN_NAME = CASE_SENSITIVE;
    

Copy

Note

The example specifies `LOAD_MODE = ADD_FILES_COPY`, which tells Snowflake to
copy the files into your external volume location, and then register the files
to the table.

This option avoids file charges, because Snowflake doesn’t scan the source
Parquet files and rewrite the data into new Parquet files.

Output:

    
        +---------------------------------------------------------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------+
    | file                                                          | status | rows_parsed | rows_loaded | error_limit | errors_seen | first_error | first_error_line | first_error_character | first_error_column_name |
    |---------------------------------------------------------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------|
    | my_parquet_stage/snow_af9mR2HShTY_AABspxOVwhc_0_1_008.parquet | LOADED |       15000 |       15000 |           0 |           0 | NULL        |             NULL |                  NULL | NULL                    |
    | my_parquet_stage/snow_af9mR2HShTY_AABspxOVwhc_0_1_006.parquet | LOADED |       15000 |       15000 |           0 |           0 | NULL        |             NULL |                  NULL | NULL                    |
    | my_parquet_stage/snow_af9mR2HShTY_AABspxOVwhc_0_1_005.parquet | LOADED |       15000 |       15000 |           0 |           0 | NULL        |             NULL |                  NULL | NULL                    |
    | my_parquet_stage/snow_af9mR2HShTY_AABspxOVwhc_0_1_002.parquet | LOADED |           5 |           5 |           0 |           0 | NULL        |             NULL |                  NULL | NULL                    |
    | my_parquet_stage/snow_af9mR2HShTY_AABspxOVwhc_0_1_010.parquet | LOADED |       15000 |       15000 |           0 |           0 | NULL        |             NULL |                  NULL | NULL                    |
    +---------------------------------------------------------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------+
    

  4. Query the table:
    
        SELECT
        c_custkey,
        c_name,
        c_mktsegment
      FROM customer_iceberg_ingest
      LIMIT 10;
    

Copy

Output:

    
        +-----------+--------------------+--------------+
    | C_CUSTKEY | C_NAME             | C_MKTSEGMENT |
    |-----------+--------------------+--------------|
    |     75001 | Customer#000075001 | FURNITURE    |
    |     75002 | Customer#000075002 | FURNITURE    |
    |     75003 | Customer#000075003 | MACHINERY    |
    |     75004 | Customer#000075004 | AUTOMOBILE   |
    |     75005 | Customer#000075005 | FURNITURE    |
    |         1 | Customer#000000001 | BUILDING     |
    |         2 | Customer#000000002 | AUTOMOBILE   |
    |         3 | Customer#000000003 | AUTOMOBILE   |
    |         4 | Customer#000000004 | MACHINERY    |
    |         5 | Customer#000000005 | HOUSEHOLD    |
    +-----------+--------------------+--------------+
    

