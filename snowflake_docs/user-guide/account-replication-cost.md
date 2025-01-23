# Understanding replication cost¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Standard & Business Critical
Feature](intro-editions)

  * Database and share replication are available to all accounts.

  * Replication of other account objects & failover/failback require Business Critical Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Charges based on replication are divided into two categories: data transfer
and compute resources. Both categories are billed on the target account (i.e.
the account that stores the secondary database or secondary
replication/failover group that is refreshed).

Data transfer:

    

The initial replication and subsequent synchronization operations transfer
data between regions. Cloud providers charge for data transferred from one
region to another within their own network.

The data transfer rate is determined by the location of the source account
(i.e. the account that stores the primary replication or failover group). For
data transfer pricing, see the [Snowflake Service Consumption
Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

For more information, see [Understanding data transfer cost](cost-
understanding-data-transfer).

Compute resources:

    

Replication operations use Snowflake-provided compute resources for the
following:

  * To determine the delta of both metadata and data to be copied during the refresh operation.

  * To copy the data between accounts across regions.

The service type for compute costs for replication in the [account
usage](../sql-reference/account-usage) and [organization usage](../sql-
reference/organization-usage) views is REPLICATION.

For more information, see [Understanding compute cost](cost-understanding-
compute).

Note

  * The target account also incurs standard storage costs for the data in each secondary database in the account.

  * The target account also incurs costs for the automatic background processes that service [materialized views](account-replication-considerations.html#label-replication-and-materialized-views) and [search optimization](search-optimization/working-with-tables.html#label-search-optimization-replication-support). The maintenance costs for secondary objects is lower than for primary objects. For details, see the “Serverless Feature Credit Table” in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf) for the costs per compute hour.

  * Replication charges are applied even if the initial replication or a refresh operation doesn’t succeed. Any data that is copied before the initial replication or refresh operation fails can be reused by a subsequent refresh operation (if performed within 14 days) and doesn’t need to be copied again.

**In this Topic:**

## Estimating and controlling costs¶

In general, monthly billing for replication is proportional to:

  * Amount of table data in the primary database, or databases in a replication/failover group, that changes as a result of data loading or DML operations.

  * Frequency of secondary database, or replication/failover group, refreshes from the primary database or replication/failover group.

You can control the cost of replication by carefully choosing which databases
or objects to replicate and their refresh frequency. You can stop incurring
replication costs by ceasing refresh operations.

## Viewing actual costs¶

Users with the ACCOUNTADMIN role can use SQL to view the amount of data
transferred (in bytes) and the credit usage for replication using replication
or failover groups for your Snowflake account within a specified date range.

To view the data transfer amounts and credit usage for replication for your
account:

> SQL:
>  
>
> Query either of the following:
>
>   * [REPLICATION_GROUP_USAGE_HISTORY](../sql-
> reference/functions/replication_group_usage_history) table function (in the
> [Snowflake Information Schema](../sql-reference/info-schema)). This function
> returns replication usage activity within the last 14 days.
>
>   * [REPLICATION_GROUP_USAGE_HISTORY view](../sql-reference/account-
> usage/replication_group_usage_history) (in [Account Usage](../sql-
> reference/account-usage)). This view returns replication usage activity
> within the last 365 days (1 year).
>
>

>
> For examples, see [Monitor replication costs](account-replication-
> monitor.html#label-replication-group-cost).

To view the cost of replication for individual databases replicated with
Database Replication, see [Monitoring database replication cost](db-
replication-config.html#label-monitoring-database-replication-cost).

