# Understanding storage cost¶

Storage cost represents the cost of:

  * Files [staged](data-load-considerations-stage) for bulk data loading/unloading (stored compressed or uncompressed).

  * Database tables, including historical data for [Time Travel](data-time-travel).

  * [Fail-safe](data-failsafe) for database tables.

  * [Clones](object-clone) of database tables that reference data deleted in the table that owns the clones.

The monthly costs for storing data in Snowflake is based on a flat rate per
terabyte (TB). The amount charged depends on your type of account (Capacity or
On Demand) and region (US or EU).

For storage pricing, see the [Snowflake Pricing
Guide](https://www.snowflake.com/pricing/pricing-guide/).

## Staged file costs¶

Files staged for bulk data loading/unloading incur storage costs based on the
size of the files. For more information on loading data, see [Load data into
Snowflake](../guides-overview-loading-data).

## Database costs¶

Database costs include data stored in database tables. Database costs also
include historical data maintained for Time Travel. Snowflake automatically
compresses all data stored in tables and uses the compressed file size to
calculate the total storage used for an account.

See also [Data storage considerations](tables-storage-considerations).

## Time Travel and Fail-safe costs¶

Time Travel and Fail-safe fees are calculated for each 24-hour period (i.e. 1
day) from the time the data changed. The number of days historical data is
maintained is based on the table type and the Time Travel retention period for
the table.

Snowflake minimizes the amount of storage required for historical data by
maintaining only the information required to restore the individual table rows
that were updated or deleted. As a result, storage usage is calculated as a
percentage of the table that changed. Full copies of tables are only
maintained when tables are dropped or truncated.

See also [Storage Costs for Time Travel and Fail-safe](data-cdp-storage-
costs).

## Temporary and transient tables costs¶

To help manage the storage costs associated with Time Travel and Fail-safe,
Snowflake provides two table types, temporary and transient. Temporary and
transient tables do not incur the same fees as permanent tables:

  * Transient and temporary tables contribute to the storage charges that Snowflake bills your account until explicitly dropped. Data stored in these table types contributes to the overall storage charges Snowflake bills your account while they exist.

  * Temporary tables are typically used for non-permanent session specific transitory data such as ETL or other session specific data. Temporary tables only exist for the lifetime or their associated session. On session end, temporary table data is purged and unrecoverable. Temporary tables are not accessible outside the specific session which created them.

  * Transient tables exist until explicitly dropped and are available to all users with appropriate privileges.

  * Transient and temporary tables can have a Time Travel retention period of either 0 or 1 day.

  * Transient and temporary tables have no Fail-safe period.

  * Transient and temporary tables can, at most, incur a one day’s worth of storage cost.

The following table illustrates the different scenarios, based on table type:

Table Type | Time Travel Retention Period (Days) | Fail-safe Period (Days) | Min , Max Historical Data Maintained (Days)  
---|---|---|---  
Permanent | 0 or 1 (for Snowflake Standard Edition) | 7 | **7 , 8**  
0 to 90 (for Snowflake Enterprise Edition) | 7 | **7 , 97**  
Transient | 0 or 1 | 0 | **0 , 1**  
Temporary | 0 or 1 | 0 | **0 , 1**  
  
### Using temporary and transient tables to manage storage costs¶

When choosing whether to store data in permanent, temporary, or transient
tables, consider the following:

  * Temporary tables are dropped when the session in which they were created ends. Data stored in temporary tables is not recoverable after the table is dropped.

  * Historical data in transient tables cannot be recovered by Snowflake after the Time Travel retention period ends. Use transient tables only for data you can replicate or reproduce independently from Snowflake.

  * Long-lived tables, such as fact tables, should always be defined as permanent to ensure they are fully protected by Fail-safe.

  * Short-lived tables (i.e. <1 day), such as ETL work tables, can be defined as transient to eliminate Fail-safe costs.

  * If downtime and the time required to reload lost data are factors, permanent tables, even with their added Fail-safe costs, may offer a better overall solution than transient tables.

Note

The default type for tables is permanent. To define a table as temporary or
transient, you must explicitly specify the type during table creation.

## Hybrid table costs¶

If you choose to use hybrid tables for your operational and analytical
workloads, consider that cost for data storage in that table type is based on
your consumption rates of the following:

  * Hybrid Table Storage (incurred primarily by the hybrid tables themselves and the indexes they contain)

  * Hybrid Table Requests

Generally, hybrid tables are more costly than standard Snowflake tables.

For more information, see [Evaluate cost for hybrid tables](tables-hybrid-
cost).

## Cloning tables, schemas, and databases costs¶

Snowflake’s zero-copy cloning feature provides a convenient way to quickly
take a “snapshot” of any table (excluding hybrid tables), schema, or database
and create a derived copy of that object which initially shares the underlying
storage. This can be extremely useful for creating instant backups that do not
incur any additional costs (until changes are made to the cloned object).

However, cloning makes calculating total storage usage more complex because
each clone has its own separate life-cycle. This means that changes can be
made to the original object or the clone independently of each other and these
changes are protected through CDP.

For example, when a clone is created of a table, the clone utilizes no storage
because it shares all the existing micro-partitions of the original table at
the time it was cloned; however, rows can then be added, deleted, or updated
in the clone independently from the original table. Each change to the clone
results in new micro-partitions that are owned exclusively by the clone and
are protected through CDP.

In addition, clones can be cloned, with no limitations on the number or
iterations of clones that can be created (e.g. you can create a clone of a
clone of a clone, and so on), which results in an n-level hierarchy of cloned
objects, each with their own portion of shared and independent storage.

## Cross-Cloud Auto-Fulfillment costs¶

Cross-Cloud Auto-Fulfillment lets you provide a data product to consumers in
other cloud regions without manual data replication. When your data product is
auto-fulfilled to another region, you incur storage and other costs. For
details, see [Managing Cross-Cloud Auto-Fulfillment Costs](https://other-
docs.snowflake.com/collaboration/provider-understand-cost-auto-fulfillment).

**Next Topic**

>   * [Exploring storage cost](cost-exploring-data-storage)
>
>

