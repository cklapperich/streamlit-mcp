# Snowpipe costs¶

With Snowpipe’s serverless compute model, users can initiate any size load
without managing a virtual warehouse. Instead, Snowflake provides and manages
the compute resources, automatically growing or shrinking capacity based on
the current Snowpipe load. Accounts are charged based on their actual compute
resource usage; in contrast with customer-managed virtual warehouses, which
consume credits when active, and may sit idle or be overutilized.

## Resource consumption and management overhead¶

Snowflake tracks the resource consumption of loads for all pipes in an
account, with per-second/per-core granularity, as Snowpipe actively queues and
processes data files. _Per-core_ refers to the physical CPU cores in a compute
server. The utilization recorded is then translated into familiar Snowflake
credits, which are listed on the bill for your account.

Note

Using a multi-threaded client application enables submitting data files in
parallel, which initiates additional servers and loads the data in less time.
However, the actual overall compute time required would be identical to using
a single-threaded client application, just spread out over more internal
Snowpipe servers.

Decisions with regard to data file size and staging frequency impact the cost
and performance of Snowpipe. For recommended best practices, see [Continuous
data loads (i.e. Snowpipe) and file sizing](data-load-considerations-
prepare.html#label-snowpipe-file-size).

In addition to resource consumption, an overhead is included in the
utilization costs charged for Snowpipe. This overhead is charged regardless if
the event notifications or REST API calls resulted in data loaded. This
overhead charge appears as Snowpipe charges in your billing statement.

To learn how many credits per compute-hour are consumed by Snowpipe, refer to
the “Serverless Feature Credit Table” in the [Snowflake Service Consumption
Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

## Estimating Snowpipe charges¶

Given the number of factors that can differentiate Snowpipe loads, it is very
difficult for Snowflake to provide sample costs. File formats and sizes, and
the complexity of COPY statements (including SELECT statement used for
transformations), all impact the resource consumption and file overhead
charged for a Snowpipe load.

We suggest that you experiment by performing a typical set of loads to
estimate future charges.

## Viewing data load history and cost¶

Account administrators (users with the ACCOUNTADMIN role) or users with a role
granted the MONITOR USAGE global privilege can use [Snowsight](ui-snowsight),
the Classic Console, or SQL to view the credits billed to your Snowflake
account within a specified date range.

Occasionally, the data compaction and maintenance process can consume
Snowflake credits. For example, the returned results might show that you
consumed credits with 0 BYTES_INSERTED and 0 FILES_INSERTED. This means that
your data is not being loaded, but the data compaction and maintenance process
has consumed some credits.

To view the credits billed for Snowpipe data loading for your account:

> Snowsight:
>  
>
> Select Admin » Cost Management.
>
> Classic Console:
>  
>
> Select Account [![Account tab](../_images/ui-navigation-account-
> icon.svg)](../_images/ui-navigation-account-icon.svg) » Billing & Usage.
>
> Snowpipe utilization is shown as a special Snowflake-provided warehouse
> named [![Snowflake logo in blue \(no text\)](../_images/logo-snowflake-sans-
> text.png)](../_images/logo-snowflake-sans-text.png) SNOWPIPE.
>
> SQL:
>  
>
> Query either of the following:
>
>   * [PIPE_USAGE_HISTORY](../sql-reference/functions/pipe_usage_history)
> table function (in the [Snowflake Information Schema](../sql-reference/info-
> schema)).
>
>   * [PIPE_USAGE_HISTORY view](../sql-reference/account-
> usage/pipe_usage_history) (in [Account Usage](../sql-reference/account-
> usage)).
>
> The following queries can be executed against the PIPE_USAGE_HISTORY view:
>
> **Query: Snowpipe cost history (by day, by object)**
>
> This query provides a full list of pipes and the volume of credits consumed
> via the service over the last 30 days, broken out by day. Any irregularities
> in the credit consumption or consistently high consumption are flags for
> additional investigation.
>  
>     >     SELECT TO_DATE(start_time) AS date,
>       pipe_name,
>       SUM(credits_used) AS credits_used
>     FROM snowflake.account_usage.pipe_usage_history
>     WHERE start_time >= DATEADD(month,-1,CURRENT_TIMESTAMP())
>     GROUP BY 1,2
>     ORDER BY 3 DESC;
>  
>
> Copy
>
> **Query: Snowpipe History & m-day average**
>
> This query shows the average daily credits consumed by Snowpipe grouped by
> week over the last year. It can help identify anomalies in daily averages
> over the year so you can investigate spikes or unexpected changes in
> consumption.
>  
>     >     WITH credits_by_day AS (
>       SELECT TO_DATE(start_time) AS date,
>         SUM(credits_used) AS credits_used
>       FROM snowflake.account_usage.pipe_usage_history
>       WHERE start_time >= DATEADD(year,-1,CURRENT_TIMESTAMP())
>       GROUP BY 1
>       ORDER BY 2 DESC
>     )
>  
>     SELECT DATE_TRUNC('week',date),
>       AVG(credits_used) AS avg_daily_credits
>     FROM credits_by_day
>     GROUP BY 1
>     ORDER BY 1;
>  
>
> Copy
>
>

Note

[Resource monitors](resource-monitors) provide control over virtual warehouse
credit usage; however, you cannot use them to control credit usage for the
Snowflake-provided warehouses, including the [![Snowflake logo in blue \(no
text\)](../_images/logo-snowflake-sans-text.png)](../_images/logo-snowflake-
sans-text.png) SNOWPIPE warehouse.

