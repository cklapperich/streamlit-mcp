# Storage Costs for Time Travel and Fail-safe¶

Storage fees are incurred for maintaining historical data during both the Time
Travel and Fail-safe periods.

## Storage Usage and Fees¶

The fees are calculated for each 24-hour period (i.e. 1 day) from the time the
data changed. The number of days historical data is maintained is based on the
table type and the Time Travel retention period for the table.

Also, Snowflake minimizes the amount of storage required for historical data
by maintaining only the information required to restore the individual table
rows that were updated or deleted. As a result, storage usage is calculated as
a percentage of the table that changed. Full copies of tables are only
maintained when tables are dropped or truncated.

## Temporary and Transient Tables¶

To help manage the storage costs associated with Time Travel and Fail-safe,
Snowflake provides two table types, temporary and transient, which do not
incur the same fees as standard (i.e. permanent) tables:

  * Transient tables can have a Time Travel retention period of either 0 or 1 day.

  * Temporary tables can also have a Time Travel retention period of 0 or 1 day; however, this retention period ends as soon as the table is dropped or the session in which the table was created ends.

  * Transient and temporary tables have no Fail-safe period.

As a result, the maximum additional fees incurred for Time Travel and Fail-
safe by these types of tables is limited to 1 day. The following table
illustrates the different scenarios, based on table type:

Table Type | Time Travel Retention Period (Days) | Fail-safe Period (Days) | Min , Max Historical Data Maintained (Days)  
---|---|---|---  
Permanent | 0 or 1 (for Snowflake Standard Edition) | 7 | **7 , 8**  
0 to 90 (for Snowflake Enterprise Edition) | 7 | **7 , 97**  
Transient | 0 or 1 | 0 | **0 , 1**  
Temporary | 0 or 1 | 0 | **0 , 1**  
  
## Considerations for Using Temporary and Transient Tables to Manage Storage
Costs¶

When choosing whether to store data in permanent, temporary, or transient
tables, consider the following:

  * Temporary tables are dropped when the session in which they were created ends. Data stored in temporary tables is not recoverable after the table is dropped.

  * Historical data in transient tables cannot be recovered by Snowflake after the Time Travel retention period ends. Use transient tables only for data you can replicate or reproduce independently from Snowflake.

  * Long-lived tables, such as fact tables, should always be defined as permanent to ensure they are fully protected by Fail-safe.

  * Short-lived tables (i.e. <1 day), such as ETL work tables, can be defined as transient to eliminate Fail-safe costs.

  * If downtime and the time required to reload lost data are factors, permanent tables, even with their added Fail-safe costs, may offer a better overall solution than transient tables.

Note

The default type for tables is permanent. To define a table as temporary or
transient, you must explicitly specify the type during table creation:

> `CREATE [ OR REPLACE ] [ TEMPORARY | TRANSIENT ] TABLE <name> ...`

For more information, see [CREATE TABLE](../sql-reference/sql/create-table).

## Migrating Data from Permanent Tables to Transient Tables¶

Migrating data from permanent tables to transient tables involves performing
the following tasks:

  1. Use [CREATE TABLE … AS SELECT](../sql-reference/sql/create-table) to create and populate the transient tables with the data from the original, permanent tables.

  2. Apply all access control privileges granted on the original tables to the new tables. For more information about access control, see [Overview of Access Control](security-access-control-overview).

  3. Use [DROP TABLE](../sql-reference/sql/drop-table) to delete the original tables.

  4. Optionally, use [ALTER TABLE](../sql-reference/sql/alter-table) to rename the new tables to match the original tables.

