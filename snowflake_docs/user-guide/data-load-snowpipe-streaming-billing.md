# Snowpipe Streaming costs¶

With Snowpipe Streaming’s serverless compute model, users can stream any data
volume without managing a virtual warehouse. Instead, Snowflake provides and
manages the compute resources, automatically growing or shrinking capacity
based on the current Snowpipe Streaming load.

Accounts are charged based on the per-second time that serverless compute and
active client streaming ingestion uses. Note the following:

  * File migration occurs asynchronously from streaming ingestion.

  * File migration might be pre-empted by clustering or other DML operations.

  * File migration might not always occur, and therefore compute costs might be reduced.

  * For Snowflake-managed Apache Iceberg™ tables, file migration operates similarly to Iceberg table maintenance to create new compacted Parquet files, if necessary.

For more information, see the “Serverless Feature Credit Table” in the
[Snowflake Service Consumption Table](https://www.snowflake.com/legal-
files/CreditConsumptionTable.pdf).

## Estimating Snowpipe Streaming charges¶

Given the number of factors that can differentiate Snowpipe Streaming loads,
it is very difficult for Snowflake to provide sample costs. Size of records,
number of records, data types, etc. can affect the compute resource
consumption for file migration. Client charges are dictated only by how many
clients are actively writing data to Snowflake on a per-second basis.

We suggest that you experiment by performing a typical streaming ingestion
load to estimate future charges. To see a sample streaming ingestion
experiment with estimated costs, see [this blog
post](https://www.snowflake.com/blog/data-ingestion-best-practices-part-
three/).

Note

Snowpipe Streaming ingestion to Snowflake-managed Iceberg tables is available
free of charge for a limited period of time.

## Viewing the data load history for your account¶

Account administrators (users with the ACCOUNTADMIN role) or users with a role
granted the MONITOR USAGE global privilege can use SQL commands to view the
credits billed to your Snowflake account within a specified date range. You
can use the following views to query the history of data migrated into
Snowflake tables, the amount of time spent loading data into Snowflake tables
using Snowpipe Streaming, and the credits consumed.

To view the total Snowpipe Streaming costs, including both compute and client
costs, query the metering history when the `SERVICE_TYPE` is set to
`SNOWPIPE_STREAMING`.

>   * [METERING_HISTORY view](../sql-reference/account-usage/metering_history)
> (in [Account Usage](../sql-reference/account-usage)).
>
>

For more information about querying the total Snowpipe Streaming costs, see [a
SQL example](cost-exploring-compute.html#label-cost-explore-query-snowpipe-
streaming).

To see the detailed breakdowns of client ingestion and migration compute, you
can query the following views:

>   * [SNOWPIPE_STREAMING_CLIENT_HISTORY view](../sql-reference/account-
> usage/snowpipe_streaming_client_history) (in [Account Usage](../sql-
> reference/account-usage)).
>
>   * [SNOWPIPE_STREAMING_FILE_MIGRATION_HISTORY view](../sql-
> reference/account-usage/snowpipe_streaming_file_migration_history) (in
> [Account Usage](../sql-reference/account-usage)).
>
>

