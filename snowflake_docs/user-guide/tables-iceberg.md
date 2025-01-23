# Apache Iceberg™ tables¶

Apache Iceberg™ tables for Snowflake combine the performance and query
semantics of typical Snowflake tables with external cloud storage that you
manage. They are ideal for existing data lakes that you cannot, or choose not
to, store in Snowflake.

Iceberg tables use the [Apache Iceberg™](https://iceberg.apache.org/) open
table format specification, which provides an abstraction layer on data files
stored in open formats and supports features such as:

  * ACID (atomicity, consistency, isolation, durability) transactions

  * Schema evolution

  * Hidden partitioning

  * Table snapshots

Snowflake supports Iceberg tables that use the [Apache
Parquet™](https://parquet.apache.org/) file format.

## Getting started¶

To get started with Iceberg tables, see [Tutorial: Create your first Apache
Iceberg™ table](tutorials/create-your-first-iceberg-table).

## How it works¶

This section provides information specific to working with Iceberg tables _in
Snowflake_. To learn more about the Iceberg table format specification, see
the official [Apache Iceberg
documentation](https://iceberg.apache.org/docs/latest/) and the [Iceberg Table
Spec](https://iceberg.apache.org/spec/).

  * Data storage

  * Catalog

  * Metadata and snapshots

  * Cross-cloud/cross-region support

  * Billing

### Data storage¶

Iceberg tables store their data and metadata files in an external cloud
storage location (Amazon S3, Google Cloud Storage, or Azure Storage). The
external storage is not part of Snowflake. You are responsible for all
management of the external cloud storage location, including the configuration
of data protection and recovery. Snowflake does not provide [Fail-safe](data-
failsafe) storage for Iceberg tables.

Snowflake connects to your storage location using an external volume, and
Iceberg tables incur no Snowflake storage costs. For more information, see
Billing.

To learn more about storage for Iceberg tables, see [Storage for Apache
Iceberg™ tables](tables-iceberg-storage).

#### External volume¶

An external volume is a named, account-level Snowflake object that you use to
connect Snowflake to your external cloud storage for Iceberg tables. An
external volume stores an identity and access management (IAM) entity for your
storage location. Snowflake uses the IAM entity to securely connect to your
storage for accessing table data, Iceberg metadata, and manifest files that
store the table schema, partitions, and other metadata.

A single external volume can support one or more Iceberg tables.

To set up an external volume for Iceberg tables, see [Configure an external
volume](tables-iceberg-configure-external-volume).

### Catalog¶

An Iceberg catalog enables a compute engine to manage and load Iceberg tables.
The catalog forms the first architectural layer in the [Iceberg table
specification](https://iceberg.apache.org/spec/#overview) and must support:

  * Storing the current metadata pointer for one or more Iceberg tables. A metadata pointer maps a table name to the location of that table’s current metadata file.

  * Performing atomic operations so that you can update the current metadata pointer for a table.

To learn more about Iceberg catalogs, see the [Apache Iceberg
documentation](https://iceberg.apache.org/concepts/catalog/).

Snowflake supports different catalog options. For example, you can use
Snowflake as the Iceberg catalog, or use a catalog integration to connect
Snowflake to an external Iceberg catalog.

#### Catalog integration¶

A catalog integration is a named, account-level Snowflake object that stores
information about how your table metadata is organized for the following
scenarios:

  * When you don’t use Snowflake as the Iceberg catalog. For example, you need a catalog integration if your table is managed by AWS Glue.

  * When you want to integrate with [Snowflake Open Catalog](https://other-docs.snowflake.com/en/opencatalog/overview) to:

    * Query an Iceberg table in Snowflake Open Catalog using Snowflake.

    * Sync a Snowflake-managed Iceberg table with Snowflake Open Catalog so that third-party compute engines can query the table.

A single catalog integration can support one or more Iceberg tables that use
the same external catalog.

To set up a catalog integration, see [Configure a catalog integration](tables-
iceberg-configure-catalog-integration).

### Metadata and snapshots¶

Iceberg uses a snapshot-based querying model, where data files are mapped
using manifest and metadata files. A snapshot represents the state of a table
at a point in time and is used to access the complete set of data files in the
table.

To learn about table metadata and Time Travel support, see [Metadata and
retention for Apache Iceberg™ tables](tables-iceberg-metadata).

### Cross-cloud/cross-region support¶

Cross-cloud/cross-region support depends on the type of Iceberg table.

Table type | Cross-cloud/cross-region support | Notes  
---|---|---  
Tables that use an external catalog with a catalog integration | ✔ | If the [active storage location](tables-iceberg-storage.html#label-tables-iceberg-ext-vol-active-storage-location) for your external volume is not with the same cloud provider or in the same region as your Snowflake account, the following limitations apply:

  * You can’t use the [SYSTEM$GET_ICEBERG_TABLE_INFORMATION](../sql-reference/functions/system_get_iceberg_table_information) function to retrieve information about the latest refreshed snapshot.
  * You can’t convert the table to use Snowflake as the catalog.

If your Snowflake account and external volume are in different regions, your
external cloud storage account incurs egress costs when you query the table.  
Tables that use Snowflake as the catalog | ❌ | Your external volume must use an [active storage location](tables-iceberg-storage.html#label-tables-iceberg-ext-vol-active-storage-location) with the same cloud provider (in the same region) that hosts your Snowflake account. If the active location is not in the same region, the CREATE ICEBERG TABLE statement returns a user error.  
  
### Billing¶

Snowflake bills your account for virtual warehouse (compute) usage and cloud
services when you work with Iceberg tables. Snowflake also bills your account
if you use [automated refresh](tables-iceberg-auto-refresh.html#label-tables-
iceberg-auto-refresh-billing).

Snowflake does not bill your account for the following:

  * Iceberg table storage costs. Your cloud storage provider bills you directly for data storage usage.

  * Active bytes used by Iceberg tables. However, the [INFORMATION_SCHEMA.TABLE_STORAGE_METRICS](../sql-reference/info-schema/table_storage_metrics) and [ACCOUNT_USAGE.TABLE_STORAGE_METRICS](../sql-reference/account-usage/table_storage_metrics) views display ACTIVE_BYTES for Iceberg tables to help you track how much storage a table occupies. To view an example, see [Retrieve storage metrics](tables-iceberg-manage.html#label-tables-iceberg-get-storage-metrics).

Note

If your Snowflake account and external volume are in different regions, your
external cloud storage account incurs egress costs when you query the table.

## Catalog options¶

Snowflake supports the following Iceberg catalog options:

  * Use Snowflake as the Iceberg catalog

  * Use an external Iceberg catalog

The following table summarizes the differences between these catalog options.

| Use Snowflake as the catalog | Use an external catalog  
---|---|---  
Read access | ✔ | ✔  
Write access | ✔ | ❌ For Snowflake platform support, you can convert the table to use Snowflake as the catalog.  
Data and metadata storage | External volume (cloud storage) | External volume (cloud storage)  
Snowflake platform support | ✔ | ❌  
Integrates with Snowflake Open Catalog | ✔ You can sync a Snowflake-managed table with Open Catalog to query a table using other compute engines. | ✔ You can use Snowflake to query Iceberg tables managed by Open Catalog.  
Works with the [Snowflake Catalog SDK](tables-iceberg-catalog) | ✔ | ✔  
  
### Use Snowflake as the catalog¶

An Iceberg table that uses Snowflake as the Iceberg catalog (Snowflake-managed
Iceberg table) provides full Snowflake platform support with read and write
access. The table data and metadata are stored in external cloud storage,
which Snowflake accesses using an external volume. Snowflake handles all life-
cycle maintenance, such as compaction, for the table.

[![How Iceberg tables that use Snowflake as the Iceberg catalog
work](../_images/tables-iceberg-snowflake-as-catalog.svg)](../_images/tables-
iceberg-snowflake-as-catalog.svg)

### Use an external catalog¶

An Iceberg table that uses an external catalog provides limited Snowflake
platform support with read-only access. With this table type, Snowflake uses a
catalog integration to retrieve information about your Iceberg metadata and
schema.

You can use this option to create an Iceberg table for the following sources:

  * AWS Glue Data Catalog

  * Iceberg metadata files in object storage

  * Delta table files in object storage

  * Open Catalog

  * Remote Iceberg REST catalog

Snowflake does not assume any life-cycle management on the table.

The table data and metadata are stored in external cloud storage, which
Snowflake accesses using an external volume.

The following diagram shows how an Iceberg table uses a catalog integration
with an external Iceberg catalog.

[![How Iceberg tables that use a catalog integration work](../_images/tables-
iceberg-external-catalog.svg)](../_images/tables-iceberg-external-catalog.svg)

## Considerations and limitations¶

The following considerations and limitations apply to Iceberg tables, and are
subject to change:

**Clouds and regions**

>   * Iceberg tables are available for all Snowflake accounts, on all cloud
> platforms and in all regions except in the China region.
>
>   * Cross-cloud/cross-region tables are supported when you use an external
> catalog. For more information, see Cross-cloud/cross-region support.
>
>

**Iceberg**

>   * Versions 1 and 2 of the Apache Iceberg specification are supported,
> excluding the following [features](https://iceberg.apache.org/spec/):
>
>     * Row-level deletes (either position deletes or equality deletes).
> However, tables that use Snowflake as the catalog support Snowflake
> [DELETE](../sql-reference/sql/delete) statements.
>
>     * Using the `history.expire.min-snapshots-to-keep` [table
> property](https://iceberg.apache.org/docs/1.2.1/configuration/#table-
> behavior-properties) to specify the default minimum number of snapshots to
> keep. For more information, see Metadata and snapshots.
>
>   * Iceberg partitioning with the `bucket` transform function impacts
> performance for queries that use conditional clauses to filter results.
>
>   * For Iceberg tables that aren’t managed by Snowflake, be aware of the
> following:
>
>     * Time travel to any snapshot generated after table creation is
> supported as long as you periodically refresh the table before the snapshot
> expires.
>
>     * Converting a table that has an un-materialized identity partition
> column isn’t supported. An un-materialized identity partition column is
> created when a table defines an identity transform using a source column
> that doesn’t exist in a Parquet file.
>
>

**File formats**

>   * Iceberg tables support Apache Parquet files.
>
>   * Parquet files that use the unsigned integer logical type aren’t
> supported.
>
>

**External volumes**

>   * You can’t access the cloud storage locations in external volumes using a
> storage integration.
>
>   * You must configure a separate trust relationship for each external
> volume that you create.
>
>   * You can use [outbound private connectivity](private-connectivity-
> outbound) to access Snowflake-managed Iceberg tables and Iceberg tables that
> use a catalog integration for object storage, but cannot use it to access
> Iceberg tables that use other catalog integrations.
>
>

**Metadata files**

>   * The metadata files don’t identify the most recent snapshot of an Iceberg
> table.
>
>   * You can’t modify the location of the data files or snapshot using the
> ALTER ICEBERG TABLE command. To modify either of these settings, you must
> recreate the table (using the CREATE OR REPLACE ICEBERG TABLE syntax).
>
>   * For tables that use an external catalog:
>

>>     * Ensure that manifest files don’t contain duplicates. If duplicate
files are present in the _same_ snapshot, Snowflake returns an error that
includes the path of the duplicate file.

>>

>>     * You can’t create a table if the Parquet metadata contains invalid
UTF-8 characters. Ensure that your Parquet metadata is UTF-8 compliant.

>
>   * Snowflake detects corruptions and inconsistencies in Parquet metadata
> produced outside of Snowflake, and surfaces issues through error messages.
>
> It’s possible to create, refresh, or query externally managed (or converted)
> tables, even if the table metadata is inconsistent. When writing Iceberg
> data, ensure that the table’s metadata statistics (for example, `RowCount`
> or `NullCount`) match the data content.
>
>   * For tables that use Snowflake as the catalog, Snowflake processes DDL
> statements individually and produces metadata in a way that might differ
> from other catalogs. For more information, see [DDL statements](tables-
> iceberg-transactions.html#label-tables-iceberg-transactions-ddl).
>
>

**Clustering**

> [Clustering](tables-clustering-keys) support depends on the type of Iceberg
> table.
>
> Table type | Notes  
> ---|---  
> Tables that use Snowflake as the Iceberg catalog | Set a clustering key by using either the CREATE ICEBERG TABLE or the ALTER ICEBERG TABLE command. To set or manage a clustering key, see [CREATE ICEBERG TABLE (Snowflake as the Iceberg catalog)](../sql-reference/sql/create-iceberg-table-snowflake) and [ALTER ICEBERG TABLE](../sql-reference/sql/alter-iceberg-table).  
> Tables that use an external catalog | Clustering is not supported.  
> Converted tables | Snowflake only clusters files if they were created after converting the table, or if the files have since been modified using a DML statement.  
  
**Delta**

>   * Snowflake streams aren’t supported for Iceberg tables created from Delta
> table files with partition columns. However, insert-only streams for tables
> created from Delta files _without_ partition columns are supported.
>
>   * Dynamic tables aren’t supported on Iceberg tables created from Delta
> table files.
>
>   * Snowflake doesn’t support creating Iceberg tables from Delta table
> definitions in the AWS Glue Data Catalog.
>
>   * Parquet files (data files for Delta tables) that use any of the
> following features or data types aren’t supported:
>

>>     * Field IDs.

>>

>>     * The INTERVAL data type.

>>

>>     * The DECIMAL data type with precision higher than 38.

>>

>>     * LIST or MAP types with one-level or two-level representation.

>>

>>     * Unsigned integer types (INT(signed = false)).

>>

>>     * The FLOAT16 data type.

>
> For more information about Delta data types and Iceberg tables, see [Delta
> data types](tables-iceberg-data-types.html#label-tables-iceberg-delta-
> source-data-types).
>
>   * Refresh operations during CREATE and ALTER … REFRESH can process a
> maximum of 1,000 Delta commit files per operation.
>
> Note
>
> Snowflake uses Delta checkpoint files when creating an Iceberg table. The
> 1,000 commit file limit only applies to commits after the latest checkpoint.
>
>   * Generating Iceberg metadata using the
> SYSTEM$GET_ICEBERG_TABLE_INFORMATION function isn’t supported.
>
>   * The following Delta Lake features aren’t currently supported: Row
> tracking, deletion vector files, change data files, change metadata,
> DataChange, CDC, protocol evolution.
>
>

**Automated refresh**

>   * When automated refresh is enabled, you can’t manually refresh the table
> metadata. To perform a manual refresh, [turn off automated refresh](tables-
> iceberg-auto-refresh.html#label-tables-iceberg-auto-refresh-update) first.
>
>   * For catalog integrations created before Snowflake version 8.22, you must
> manually set the `REFRESH_INTERVAL_SECONDS` parameter before you enable
> automated refresh on tables that depend on that catalog integration. For
> instructions, see [ALTER CATALOG INTEGRATION … SET AUTO_REFRESH](../sql-
> reference/sql/alter-catalog-integration).
>
>   * Ensure that the new table snapshot is a direct child of the current
> table snapshot. Otherwise, automated refresh enters the `STOPPED` state. To
> recover automated refresh when this occurs, see [Error recovery](tables-
> iceberg-auto-refresh.html#label-tables-iceberg-auto-refresh-error-recovery).
>
>     * If your table is empty, [perform a manual refresh](tables-iceberg-
> manage.html#label-tables-iceberg-refresh-metadata) _before_ you enable
> automated refresh to avoid undefined behavior.
>
>   * Automated refresh isn’t supported when you use a [catalog integration
> for object storage](tables-iceberg-configure-catalog-integration-object-
> storage).
>
>   * Iceberg version 1 manifests without a sequence number column aren’t
> currently supported.
>
>

**Access by third-party clients to Iceberg data, metadata**

>   * Third-party clients can’t append to, delete from, or upsert data to
> Iceberg tables that use Snowflake as the catalog.
>
>

**S3-compatible storage**

> Iceberg tables that use S3-compatible storage are cross-region tables and
> don’t support the following actions:
>
>   * Using Snowflake as the Iceberg catalog or converting a table to use
> Snowflake as the Iceberg catalog.
>
>   * Retrieving information about the latest refreshed snapshot with the
> [SYSTEM$GET_ICEBERG_TABLE_INFORMATION](../sql-
> reference/functions/system_get_iceberg_table_information) function.
>
>

**Unsupported features**

> The following Snowflake features aren’t currently supported for all Iceberg
> tables:
>
>   * The following drivers:
>
>     * [.NET Driver](../developer-guide/dotnet/dotnet-driver)
>
>     * [PHP PDO Driver for Snowflake](../developer-guide/php-pdo/php-pdo-
> driver)
>
>   * [Fail-safe](data-failsafe)
>
>   * [Hybrid tables](tables-hybrid)
>
>   * Listings that enable [Cross-Cloud Auto-Fulfillment](https://other-
> docs.snowflake.com/collaboration/provider-listings-auto-fulfillment).
>
>   * [Query Acceleration Service](query-acceleration-service)
>
>   * [Replication](account-replication-intro) of Iceberg tables, external
> volumes, or catalog integrations
>
>   * [Search optimization service](search-optimization-service)
>
>   * Snowflake encryption
>
>   * [Snowflake Native App Framework](../developer-guide/native-apps/native-
> apps-about)
>
>   * [Snowflake schema evolution](data-load-schema-evolution)
>
>   * [Tagging](object-tagging) using the
> [ASSOCIATE_SEMANTIC_CATEGORY_TAGS](../sql-reference/stored-
> procedures/associate_semantic_category_tags) stored procedure
>
>   * [Temporary and transient tables](tables-temp-transient)
>
>

>
> The following features aren’t supported for Iceberg tables _that use an
> external catalog_ :
>
>   * [Cloning](tables-storage-considerations.html#label-cloning-tables)
>
>   * [Clustering](tables-clustering-micropartitions)
>
>   * Standard and append-only [streams](streams-intro). Insert-only streams
> are supported.
>
>

