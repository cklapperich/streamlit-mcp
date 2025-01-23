# Introduction to external tables¶

An external table is a Snowflake feature that allows you to query data stored
in an [external stage](data-load-overview.html#label-data-load-overview-
external-stages) as if the data were inside a table in Snowflake. The external
stage is not part of Snowflake, so Snowflake does not store or manage the
stage.

External tables let you store (within Snowflake) certain file-level metadata,
including filenames, version identifiers, and related properties. External
tables can access data stored in any format that the [COPY INTO
<table>](../sql-reference/sql/copy-into-table) command supports except XML.

External tables are read-only. You cannot perform data manipulation language
(DML) operations on them. However, you can use external tables for query and
join operations. You can also create views against external tables.

Querying data in an external table might be slower than querying data that you
store natively in a table within Snowflake. To improve query performance, you
can use a [materialized view](views-materialized) based on an external table.

Note

If Snowflake encounters an error while scanning a file in cloud storage during
a query operation, the file is skipped and scanning continues on the next
file. A query can partially scan a file and return the rows scanned before the
error was encountered.

## Planning the schema of an external table¶

This section describes the options available for designing external tables.

### Schema on read¶

All external tables include the following columns:

VALUE:

    

A VARIANT type column that represents a single row in the external file.

METADATA$FILENAME:

    

A pseudocolumn that identifies the name of each staged data file included in
the external table, including its path in the stage.

METADATA$FILE_ROW_NUMBER:

    

A pseudocolumn that shows the row number for each record in a staged data
file.

To create external tables, you are only required to have some knowledge of the
file format and record format of the source data files. Knowing the schema of
the data files is not required.

Note that [SELECT](../sql-reference/sql/select) `*` always returns the VALUE
column, in which all regular or semi-structured data is cast to variant rows.

### Virtual columns¶

If you are familiar with the schema of the source data files, you can create
additional virtual columns as expressions using the VALUE column and/or the
METADATA$FILENAME or METADATA$FILE_ROW_NUMBER pseudocolumns. When the external
data is scanned, the data types of any specified fields or semi-structured
data elements in the data file must match the data types of these additional
columns in the external table. This allows strong type checking and schema
validation over the external data.

### General file sizing recommendations¶

To optimize the number of parallel scanning operations when querying external
tables, we recommend the following file or row group sizes per format:

Format | Recommended Size Range | Notes  
---|---|---  
Parquet files | 256 - 512 MB |   
Parquet row groups | 16 - 256 MB | Note that when Parquet files include multiple row groups, Snowflake can operate on each row group in a different server. For improved query performance, we recommend sizing Parquet files in the recommended range; or, if large file sizes are necessary, including multiple row groups in each file.  
All other supported file formats | 16 - 256 MB |   
  
For optimal performance when querying large data files, create and query
materialized views over external tables.

### Partitioned external tables¶

We strongly recommend partitioning your external tables, which requires that
your underlying data is organized using logical paths that include date, time,
country, or similar dimensions in the path. Partitioning divides your external
table data into multiple parts using partition columns.

An external table definition can include multiple partition columns, which
impose a multi-dimensional structure on the external data. Partitions are
stored in the external table metadata.

Benefits of partitioning include improved query performance. Because the
external data is partitioned into separate slices/parts, query response time
is faster when processing a small part of the data instead of scanning the
entire data set.

Based on your individual use cases, you can either:

  * Add new partitions automatically by refreshing an external table that defines an expression for each partition column.

  * Add new partitions manually.

Partition columns are defined when an external table is created, using the
CREATE EXTERNAL TABLE … PARTITION BY syntax. After an external table is
created, the method by which partitions are added cannot be changed.

The following sections explain the different options for adding partitions in
greater detail. For examples, see [CREATE EXTERNAL TABLE](../sql-
reference/sql/create-external-table).

#### Partitions added automatically¶

An external table creator defines partition columns in a new external table as
expressions that parse the path and/or filename information stored in the
METADATA$FILENAME pseudocolumn. A partition consists of all data files that
match the path and/or filename in the expression for the partition column.

The CREATE EXTERNAL TABLE syntax for adding partitions automatically based on
expressions is as follows:

    
    
    CREATE EXTERNAL TABLE
      <table_name>
         ( <part_col_name> <col_type> AS <part_expr> )
         [ , ... ]
      [ PARTITION BY ( <part_col_name> [, <part_col_name> ... ] ) ]
      ..
    

Copy

Snowflake computes and adds partitions based on the defined partition column
expressions when an external table metadata is refreshed. By default, the
metadata is refreshed automatically when the object is created. In addition,
the object owner can configure the metadata to refresh automatically when new
or updated data files are available in the external stage. The owner can
alternatively refresh the metadata manually by executing the ALTER EXTERNAL
TABLE … REFRESH command.

#### Partitions added manually¶

An external table creator determines the partition type of a new external
table as _user-defined_ and specifies only the data types of partition
columns. Use this option when you prefer to add and remove partitions
selectively rather than automatically adding partitions for all new files in
an external storage location that match an expression.

This option is generally chosen to synchronize external tables with other
metastores (e.g. AWS Glue or Apache Hive).

The CREATE EXTERNAL TABLE syntax for manually added partitions is as follows:

    
    
    CREATE EXTERNAL TABLE
      <table_name>
         ( <part_col_name> <col_type> AS <part_expr> )
         [ , ... ]
      [ PARTITION BY ( <part_col_name> [, <part_col_name> ... ] ) ]
      PARTITION_TYPE = USER_SPECIFIED
      ..
    

Copy

Include the required `PARTITION_TYPE = USER_SPECIFIED` parameter.

The partition column definitions are expressions that parse the column
metadata in the internal (hidden) METADATA$EXTERNAL_TABLE_PARTITION column.

The object owner adds partitions to the external table metadata manually by
executing the ALTER EXTERNAL TABLE … ADD PARTITION command:

    
    
    ALTER EXTERNAL TABLE <name> ADD PARTITION ( <part_col_name> = '<string>' [ , <part_col_name> = '<string>' ] ) LOCATION '<path>'
    

Copy

Automatically refreshing an external table with user-defined partitions is not
supported. Attempting to manually refresh this type of external table produces
a user error.

### Delta Lake support¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Preview Feature](../release-
notes/preview-features) — Open

Available to all accounts.

Note

To query a Delta table, consider using an [Apache Iceberg™ table](tables-
iceberg) instead. Iceberg tables use an [external volume](tables-
iceberg.html#label-tables-iceberg-external-volume-def) to connect to Delta
table files in your cloud storage. Iceberg tables created from Delta tables
files are currently in preview.

For more information, see [Iceberg tables](tables-iceberg) and [CREATE ICEBERG
TABLE (Delta files in object storage)](../sql-reference/sql/create-iceberg-
table-delta). You can also Migrate a Delta external table to Apache Iceberg™.

[Delta Lake](https://delta.io/) is a table format on your data lake that
supports ACID (atomicity, consistency, isolation, durability) transactions
among other features. All data in Delta Lake is stored in Apache Parquet
format. Create external tables that reference your cloud storage locations
enhanced with Delta Lake.

To create an external table that references a Delta Lake, set the
`TABLE_FORMAT = DELTA` parameter in the CREATE EXTERNAL TABLE statement.

When this parameter is set, the external table scans for Delta Lake
transaction log files in the `[ WITH ] LOCATION` location. Delta log files
have names like `_delta_log/00000000000000000000.json`,
`_delta_log/00000000000000000010.checkpoint.parquet`, etc. When the metadata
for an external table is refreshed, Snowflake parses the Delta Lake
transaction logs and determines which Parquet files are current. In the
background, the refresh performs add and remove file operations to keep the
external table metadata in sync.

For more information, including examples, see [CREATE EXTERNAL TABLE](../sql-
reference/sql/create-external-table).

Note

  * External tables that reference Delta Lake files don’t support deletion vectors.

  * Automated refreshes aren’t supported for this feature because the ordering of event notifications triggered by DDL operations in cloud storage is not guaranteed. To register any added or removed files, periodically execute an [ALTER EXTERNAL TABLE … REFRESH](../sql-reference/sql/alter-external-table) statement.

#### Migrate a Delta external table to Apache Iceberg™¶

To migrate one or more external tables that reference a Delta Lake to [Apache
Iceberg™ tables](tables-iceberg), complete the following steps:

  1. Use the [SHOW EXTERNAL TABLES](../sql-reference/sql/show-external-tables) command to retrieve the `location` (external stage and folder path) for the external table(s).

For example, the following command returns information for external tables and
filters on names like `my_delta_ext_table`:

    
        SHOW EXTERNAL TABLES LIKE 'my_delta_ext_table';
    

Copy

  2. [Create an external volume](tables-iceberg-configure-external-volume). Specify the location that you retrieved in the previous step as the `STORAGE_BASE_URL`.

To create a single external volume for multiple Delta tables under the same
storage location, set the external volume’s active location
(`STORAGE_BASE_URL`) as the common root directory.

For example, consider the following locations for three Delta tables that
branch from the same storage location:

     * `s3://my-bucket/delta-ext-table-1/`

     * `s3://my-bucket/delta-ext-table-2/`

     * `s3://my-bucket/delta-ext-table-3/`

Specify the bucket as the `STORAGE_BASE_URL` when you create the external
volume. Later, you can specify the relative path to the table files (for
example, `delta-ext-table-1/`) as the `BASE_LOCATION` when you create an
Iceberg table.

    
        CREATE OR REPLACE EXTERNAL VOLUME delta_migration_ext_vol
    STORAGE_LOCATIONS = (
      (
        NAME = storage_location_1
        STORAGE_PROVIDER = 'S3'
        STORAGE_BASE_URL = 's3://my-bucket/'
        STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::123456789123:role/my-storage-role' )
    );
    

Copy

  3. [Create a catalog integration for Delta tables](tables-iceberg-configure-catalog-integration-object-storage.html#label-tables-iceberg-create-cat-int-delta).

  4. Create an Iceberg table using the [CREATE ICEBERG TABLE (Delta files in object storage)](../sql-reference/sql/create-iceberg-table-delta) command. The `BASE_LOCATION` of the external volume must point to the existing external table location.

The following example creates an Iceberg table based on external table files
located in `s3://my-bucket/delta-ext-table-1/`, and references the external
volume created previously.

To determine the full storage location for the table, Snowflake appends the
`BASE_LOCATION` to the `STORAGE_BASE_URL` of the external volume.

    
        CREATE ICEBERG TABLE my_delta_table_1
      BASE_LOCATION = 'delta-ext-table-1'
      EXTERNAL_VOLUME = 'delta_migration_ext_vol'
      CATALOG = 'delta_catalog_integration';
    

Copy

  5. Drop the external table:
    
        DROP EXTERNAL TABLE my_delta_ext_table_1;
    

Copy

### Adding or dropping columns¶

Alter an existing external table to add or remove columns using the following
ALTER TABLE syntax:

  * Add columns: ALTER TABLE … ADD COLUMN.

  * Remove columns: ALTER TABLE … DROP COLUMN.

Note

The default VALUE column and METADATA$FILENAME and METADATA$FILE_ROW_NUMBER
pseudocolumns cannot be dropped.

See the example in [ALTER TABLE](../sql-reference/sql/alter-table).

### Protecting external tables¶

You can protect an external table using a masking policy and a row access
policy. For details, see:

  * [Masking policies and external tables](security-column-intro.html#label-security-column-intro-ext-table).

  * [Row access policies and external tables](security-row-intro.html#label-security-row-intro-ext-table).

## Materialized views over external tables¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Enterprise Edition
Feature](intro-editions)

Materialized views require Enterprise Edition. To inquire about upgrading,
please contact [Snowflake Support](https://docs.snowflake.com/user-
guide/contacting-support).

In many cases, [materialized views](views-materialized) over external tables
can provide performance that is faster than equivalent queries over the
underlying external table. This performance difference can be significant when
a query is run frequently or is sufficiently complex.

Refresh the file-level metadata in any queried external tables in order for
your materialized views to reflect the current set of files in the referenced
cloud storage location.

You can refresh the metadata for an external table automatically using the
event notification service for your cloud storage service or manually using
[ALTER EXTERNAL TABLE … REFRESH](../sql-reference/sql/alter-external-table)
statements.

## Automatically refreshing external table metadata¶

The metadata for an external table can be refreshed automatically using the
event notification service for your cloud storage service.

The refresh operation synchronizes the metadata with the latest set of
associated files in the external stage and path, i.e.:

>   * New files in the path are added to the table metadata.
>
>   * Changes to files in the path are updated in the table metadata.
>
>   * Files no longer in the path are removed from the table metadata.
>
>

For more information, see [Refreshing external tables automatically](tables-
external-auto).

## Billing for external tables¶

An overhead to manage event notifications for the automatic refreshing of
external table metadata is included in your charges. This overhead increases
in relation to the number of files added in cloud storage for the external
stages and paths specified for your external tables. This overhead charge
appears as Snowpipe charges in your billing statement because Snowpipe is used
for event notifications for the automatic external table refreshes. You can
estimate this charge by querying the [PIPE_USAGE_HISTORY](../sql-
reference/functions/pipe_usage_history) function or examining the Account
Usage [PIPE_USAGE_HISTORY view](../sql-reference/account-
usage/pipe_usage_history).

In addition, a small maintenance overhead is charged for manually refreshing
the external table metadata (using ALTER EXTERNAL TABLE … REFRESH). This
overhead is charged in accordance with the standard [cloud services billing
model](cost-understanding-compute.html#label-cloud-services-credit-usage),
like all similar activity in Snowflake. Manual refreshes of standard external
tables are cloud services operations only; however, manual refreshes of
external tables enhanced with Delta Lake rely on user-managed compute
resources (i.e. a virtual warehouse).

Users with the ACCOUNTADMIN role, or a role with the global MONITOR USAGE
privilege, can query the [AUTO_REFRESH_REGISTRATION_HISTORY](../sql-
reference/functions/auto_refresh_registration_history) table function to
retrieve the history of data files registered in the metadata of specified
objects and the credits billed for these operations.

## Workflow¶

Note

External tables don’t support storage versioning (S3 versioning, Object
Versioning in Google Cloud Storage, or versioning for Azure Storage).

### Amazon S3¶

This section provides a high-level overview of the setup and load workflow for
external tables that reference Amazon S3 stages. For complete instructions,
see [Refreshing external tables automatically for Amazon S3](tables-
external-s3).

  1. Create a named stage object (using [CREATE STAGE](../sql-reference/sql/create-stage)) that references the external location (i.e. S3 bucket) where your data files are staged.

  2. Create an external table (using [CREATE EXTERNAL TABLE](../sql-reference/sql/create-external-table)) that references the named stage.

  3. Manually refresh the external table metadata using [ALTER EXTERNAL TABLE](../sql-reference/sql/alter-external-table) … REFRESH to synchronize the metadata with the current list of files in the stage path. This step also verifies the settings in your external table definition.

  4. Configure an event notification for the S3 bucket. Snowflake relies on event notifications to continually refresh the external table metadata to maintain consistency with the staged files.

  5. Manually refresh the external table metadata one more time using ALTER EXTERNAL TABLE … REFRESH to synchronize the metadata with any changes that occurred since Step 3. Thereafter, the S3 event notifications trigger the metadata refresh automatically.

  6. Configure Snowflake access control privileges for any additional roles to grant them query access to the external table.

### Google Cloud Storage¶

This section provides a high-level overview of the setup and load workflow for
external tables that reference Google Cloud Storage (GCS) stages.

  1. Configure a Google Pub/Sub subscription for GCS events.

  2. Create a notification integration in Snowflake. A notification integration is a Snowflake object that provides an interface between Snowflake and third-party cloud message queuing services such as Pub/Sub.

  3. Create a named stage object (using [CREATE STAGE](../sql-reference/sql/create-stage)) that references the external location (i.e. GCS bucket) where your data files are staged.

  4. Create an external table (using [CREATE EXTERNAL TABLE](../sql-reference/sql/create-external-table)) that references the named stage and integration.

  5. Manually refresh the external table metadata once using [ALTER EXTERNAL TABLE](../sql-reference/sql/alter-external-table) … REFRESH to synchronize the metadata with any changes that occurred since Step 4. Thereafter, the Pub/Sub notifications trigger the metadata refresh automatically.

  6. Configure Snowflake access control privileges for any additional roles to grant them query access to the external table.

### Microsoft Azure¶

This section provides a high-level overview of the setup and load workflow for
external tables that reference Azure stages. For complete instructions, see
[Refreshing external tables automatically for Azure Blob Storage](tables-
external-azure).

  1. Configure an Event Grid subscription for Azure Storage events.

  2. Create a notification integration in Snowflake. A notification integration is a Snowflake object that provides an interface between Snowflake and third-party cloud message queuing services such as Microsoft Event Grid.

  3. Create a named stage object (using [CREATE STAGE](../sql-reference/sql/create-stage)) that references the external location (i.e. Azure container) where your data files are staged.

  4. Create an external table (using [CREATE EXTERNAL TABLE](../sql-reference/sql/create-external-table)) that references the named stage and integration.

  5. Manually refresh the external table metadata once using [ALTER EXTERNAL TABLE](../sql-reference/sql/alter-external-table) … REFRESH to synchronize the metadata with any changes that occurred since Step 4. Thereafter, the Event Grid notifications trigger the metadata refresh automatically.

  6. Configure Snowflake access control privileges for any additional roles to grant them query access to the external table.

## Querying external tables¶

[Query](../guides-overview-queries) external tables just as you would standard
tables.

Snowflake omits query results for records that contain invalid UTF-8 data.
After encountering invalid data, Snowflake continues to scan the file without
returning an error message.

To avoid missing records in your query results caused by invalid UTF-8 data,
specify `REPLACE_INVALID_CHARACTERS = TRUE` for your [file format](../sql-
reference/sql/create-external-table.html#label-create-ext-table-
formattypeoptions). Doing so replaces any invalid UTF-8 characters with the
Unicode replacement character (`�`) when you query the table.

For Parquet files, you can also set `BINARY_AS_TEXT = FALSE` for your file
format so that Snowflake interprets the columns with no defined logical data
type as binary data instead of as UTF-8 text.

### Filtering records in Parquet files¶

To take advantage of row group statistics to prune data in Parquet files, a
WHERE clause can include either partition columns or regular columns, or both.
The following limitations apply:

  * The clause cannot include any VARIANT columns.

  * The clause can only include one or more of the following [comparison operators](../sql-reference/operators-comparison):

    * =

    * >

    * <

  * The clause can only include one or more [logical/Boolean operators](../sql-reference/operators-logical), as well as the [STARTSWITH](../sql-reference/functions/startswith) SQL function.

In addition, queries in the form `"value:<path>::<data type>"` (or the
[GET](../sql-reference/functions/get)/ [GET_PATH , :](../sql-
reference/functions/get_path) function equivalent) take advantage of the
vectorized scanner. Queries in the form `"value"` or simply `"value:<path>"`
are processed using the non-vectorized scanner. Convert all time zone data to
a standard time zone using the [CONVERT_TIMEZONE](../sql-
reference/functions/convert_timezone) function for queries that use the
vectorized scanner.

When files are sorted by a key included in a query filter, and if there are
multiple row groups in the files, better pruning results are possible.

The following table shows similar query structures that illustrate the
behaviors in this section, where `et` is an external table and `c1`, `c2`, and
`c3` are virtual columns:

Optimized | Not optimized  
---|---  
`SELECT c1, c2, c3 FROM et;` | `SELECT value:c1, c2, c3 FROM et;`  
`SELECT c1, c2, c3 FROM et WHERE c1 = 'foo';` `SELECT c1, c2, c3 FROM et WHERE value:c1::string = 'foo';` | `SELECT c1, c2, c3 FROM et WHERE value:c1 = 'foo';`  
  
### Persisted query results¶

Similar to tables, the query results for external tables [persist](querying-
persisted-results) for 24 hours. Within this 24-hour period, the following
operations invalidate and purge the query result cache for external tables:

  * Any DDL operation that modifies the external table definition. This includes explicitly modifying the external table definition (using ALTER EXTERNAL TABLE) or recreating the external table (using [CREATE OR REPLACE EXTERNAL TABLE](../sql-reference/sql/create-external-table)).

  * Changes in the set of files in cloud storage that are registered in the external table metadata. Either automatic refresh operations using the event notification service for the storage location or manual refresh operations (using ALTER EXTERNAL TABLE … REFRESH) invalidate the result cache.

Note that changes in the referenced files in cloud storage do not invalidate
the query results cache in the following circumstances, leading to outdated
query results:

  * The automated refresh operation is disabled (i.e. AUTO_REFRESH = FALSE) or is not configured correctly.

  * The external table metadata is not refreshed manually.

## Removing older staged files from external table metadata¶

A stored procedure can remove older staged files from the metadata in an
external table using an [ALTER EXTERNAL TABLE](../sql-reference/sql/alter-
external-table) … REMOVE FILES statement. The stored procedure would remove
files from the metadata based on their last modified date in the stage.

For example:

  1. Create the stored procedure using a [CREATE PROCEDURE](../sql-reference/sql/create-procedure) statement:
    
        CREATE or replace PROCEDURE remove_old_files(external_table_name varchar, num_days float)
      RETURNS varchar
      LANGUAGE javascript
      EXECUTE AS CALLER
      AS
      $$
      // 1. Get the relative path of the external table
      // 2. Find all files registered before the specified time period
      // 3. Remove the files
    
    
      var resultSet1 = snowflake.execute({ sqlText:
        `call exttable_bucket_relative_path('` + EXTERNAL_TABLE_NAME + `');`
      });
      resultSet1.next();
      var relPath = resultSet1.getColumnValue(1);
    
    
      var resultSet2 = snowflake.execute({ sqlText:
        `select file_name
         from table(information_schema.EXTERNAL_TABLE_FILES (
             TABLE_NAME => '` + EXTERNAL_TABLE_NAME +`'))
         where last_modified < dateadd(day, -` + NUM_DAYS + `, current_timestamp());`
      });
    
      var fileNames = [];
      while (resultSet2.next())
      {
        fileNames.push(resultSet2.getColumnValue(1).substring(relPath.length));
      }
    
      if (fileNames.length == 0)
      {
        return 'nothing to do';
      }
    
    
      var alterCommand = `ALTER EXTERNAL TABLE ` + EXTERNAL_TABLE_NAME + ` REMOVE FILES ('` + fileNames.join(`', '`) + `');`;
    
      var resultSet3 = snowflake.execute({ sqlText: alterCommand });
    
      var results = [];
      while (resultSet3.next())
      {
        results.push(resultSet3.getColumnValue(1) + ' -> ' + resultSet3.getColumnValue(2));
      }
    
      return results.length + ' files: \n' + results.join('\n');
    
      $$;
    
      CREATE or replace PROCEDURE exttable_bucket_relative_path(external_table_name varchar)
      RETURNS varchar
      LANGUAGE javascript
      EXECUTE AS CALLER
      AS
      $$
      var resultSet = snowflake.execute({ sqlText:
        `show external tables like '` + EXTERNAL_TABLE_NAME + `';`
      });
    
      resultSet.next();
      var location = resultSet.getColumnValue(10);
    
      var relPath = location.split('/').slice(3).join('/');
      return relPath.endsWith("/") ? relPath : relPath + "/";
    
      $$;
    

Copy

  2. Call the stored procedure:
    
        -- Remove all files from the exttable external table metadata:
    call remove_old_files('exttable', 0);
    
    -- Remove files staged longer than 90 days ago from the exttable external table metadata:
    call remove_old_files('exttable', 90);
    

Copy

Alternatively, create a task using [CREATE TASK](../sql-reference/sql/create-
task) that calls the stored procedure periodically to remove older files from
the external table metadata.

## Apache Hive metastore integration¶

Snowflake supports integrating [Apache Hive](https://hive.apache.org/)
metastores with Snowflake using external tables. The Hive connector detects
metastore events and transmits them to Snowflake to keep the external tables
synchronized with the Hive metastore. This allows users to manage their data
in Hive while querying it from Snowflake.

For instructions, see [Integrating Apache Hive metastores with
Snowflake](tables-external-hive).

## External table DDL¶

To support creating and managing external tables, Snowflake provides the
following set of special DDL commands:

  * [CREATE EXTERNAL TABLE](../sql-reference/sql/create-external-table)

  * [ALTER EXTERNAL TABLE](../sql-reference/sql/alter-external-table)

  * [DROP EXTERNAL TABLE](../sql-reference/sql/drop-external-table)

  * [DESCRIBE EXTERNAL TABLE](../sql-reference/sql/desc-external-table)

  * [SHOW EXTERNAL TABLES](../sql-reference/sql/show-external-tables)

## Required access privileges¶

Creating and managing external tables requires a role with a minimum of the
following role permissions:

Object | Privilege  
---|---  
Database | USAGE  
Schema | USAGE, CREATE STAGE (if creating a new stage), CREATE EXTERNAL TABLE  
Stage (if using an existing stage) | USAGE  
  
## Information Schema¶

The Snowflake [Snowflake Information Schema](../sql-reference/info-schema)
includes views and table functions you can query to retrieve information about
your external tables and their staged data files.

### View¶

[EXTERNAL_TABLES view](../sql-reference/info-schema/external_tables)

    

Displays information for external tables in the specified (or current)
database.

### Table functions¶

[AUTO_REFRESH_REGISTRATION_HISTORY](../sql-
reference/functions/auto_refresh_registration_history)

    

Retrieve the history of data files registered in the metadata of specified
objects and the credits billed for these operations.

[EXTERNAL_TABLE_FILES](../sql-reference/functions/external_table_files)

    

Retrieve information about the staged data files included in the metadata for
a specified external table.

[EXTERNAL_TABLE_FILE_REGISTRATION_HISTORY](../sql-
reference/functions/external_table_registration_history)

    

Retrieve information about the metadata history for an external table,
including any errors found when refreshing the metadata.

