# Using the Query Acceleration Service¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Enterprise Edition
Feature](intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about
upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-
guide/contacting-support).

The query acceleration service (QAS) can accelerate parts of the query
workload in a warehouse. When it is enabled for a warehouse, it can improve
overall warehouse performance by reducing the impact of outlier queries, which
are queries that use more resources than the typical query. The query
acceleration service does this by offloading portions of the query processing
work to shared compute resources that are provided by the service.

Examples of the types of workloads that might benefit from the query
acceleration service include:

  * Ad hoc analytics.

  * Workloads with unpredictable data volume per query.

  * Queries with large scans and selective filters.

The query acceleration service can handle these types of workloads more
efficiently by performing more work in parallel and reducing the wall-clock
time spent in scanning and filtering.

Note

The query acceleration service depends on server availability. Therefore,
performance improvements might fluctuate over time.

## Identifying queries and warehouses that might benefit from query
acceleration¶

To identify the queries or warehouses that might benefit from the query
acceleration service, you can query the [QUERY_ACCELERATION_ELIGIBLE
view](../sql-reference/account-usage/query_acceleration_eligible). You can
also use the [SYSTEM$ESTIMATE_QUERY_ACCELERATION](../sql-
reference/functions/system_estimate_query_acceleration) function to assess
whether a specific query is eligible for acceleration.

### Eligible queries¶

In general, queries are eligible because they have a portion of the query plan
that can be run in parallel using QAS compute resources. These queries fall
into one of two patterns:

  * Large scans with an aggregation or selective filter.

  * Large scans that insert many new rows.

Snowflake doesn’t have a specific cutoff for what constitutes a “large enough”
scan to be eligible. The threshold for eligibility depends on a variety of
factors, including the query plan and warehouse size. Snowflake only marks a
query as eligible if there is high confidence that the query would be
accelerated if QAS was enabled.

### Common reasons that queries are ineligible¶

Some queries are ineligible for query acceleration. The following are common
reasons why a query cannot be accelerated:

  * There are not enough partitions in the scan. If there are not enough partitions to scan, the benefits of query acceleration are offset by the latency in acquiring resources for the query acceleration service.

  * Even if a query has a filter, the filters may not be selective enough. Alternatively, if the query has an aggregation with GROUP BY, the cardinality of the GROUP BY expression might be too high for eligibility.

  * The query includes a LIMIT clause but does not have an ORDER BY clause.

  * The query includes functions that return nondeterministic results (for example, [SEQ](../sql-reference/functions/seq1) or [RANDOM](../sql-reference/functions/random)).

### Identifying queries with the SYSTEM$ESTIMATE_QUERY_ACCELERATION function¶

The [SYSTEM$ESTIMATE_QUERY_ACCELERATION](../sql-
reference/functions/system_estimate_query_acceleration) function can help
determine if a previously executed query might benefit from the query
acceleration service. If the query is eligible for query acceleration, the
function returns the estimated query execution time for different query
acceleration [scale factors](../sql-reference/sql/create-warehouse.html#label-
query-acceleration-max-scale-factor).

#### Example¶

Execute the following statement to help determine if query acceleration might
benefit a specific query:

    
    
    SELECT PARSE_JSON(SYSTEM$ESTIMATE_QUERY_ACCELERATION('8cd54bf0-1651-5b1c-ac9c-6a9582ebd20f'));
    

Copy

In this example, the query is eligible for the query acceleration service and
includes estimated query times using the service:

    
    
    {
      "estimatedQueryTimes": {
        "1": 171,
        "10": 115,
        "2": 152,
        "4": 133,
        "8": 120
      },
      "originalQueryTime": 300.291,
      "queryUUID": "8cd54bf0-1651-5b1c-ac9c-6a9582ebd20f",
      "status": "eligible",
      "upperLimitScaleFactor": 10
    }
    

Copy

The following example shows the results for a query that is not eligible for
query acceleration service:

    
    
    SELECT PARSE_JSON(SYSTEM$ESTIMATE_QUERY_ACCELERATION('cf23522b-3b91-cf14-9fe0-988a292a4bfa'));
    

Copy

The statement above produces the following output:

    
    
    {
      "estimatedQueryTimes": {},
      "originalQueryTime": 20.291,
      "queryUUID": "cf23522b-3b91-cf14-9fe0-988a292a4bfa",
      "status": "ineligible",
      "upperLimitScaleFactor": 0
    }
    

Copy

### Identifying queries and warehouses with the QUERY_ACCELERATION_ELIGIBLE
view¶

Query the [QUERY_ACCELERATION_ELIGIBLE view](../sql-reference/account-
usage/query_acceleration_eligible) to identify the queries and warehouses that
might benefit the most from the query acceleration service. For each query,
the view includes the amount of query execution time that is eligible for the
query acceleration service.

#### Examples¶

Note

These examples assume the ACCOUNTADMIN role (or a [role granted IMPORTED
PRIVILEGES](../sql-reference/account-usage.html#label-enabling-usage-for-
other-roles) on the shared SNOWFLAKE database) is in use. If it is not in use,
execute the following command before running the queries in the examples:

    
    
    USE ROLE ACCOUNTADMIN;
    

Copy

Identify the queries in the past week that might benefit the most from the
service by the longest amount of query execution time that is eligible for
acceleration:

    
    
    SELECT query_id, eligible_query_acceleration_time
      FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_ELIGIBLE
      WHERE start_time > DATEADD('day', -7, CURRENT_TIMESTAMP())
      ORDER BY eligible_query_acceleration_time DESC;
    

Copy

Identify the queries in the past week that might benefit the most from the
service in a specific warehouse `mywh`:

    
    
    SELECT query_id, eligible_query_acceleration_time
      FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_ELIGIBLE
      WHERE warehouse_name = 'MYWH'
      AND start_time > DATEADD('day', -7, CURRENT_TIMESTAMP())
      ORDER BY eligible_query_acceleration_time DESC;
    

Copy

Identify the warehouses with the most queries, in the past week, eligible for
the query acceleration service:

    
    
    SELECT warehouse_name, COUNT(query_id) AS num_eligible_queries
      FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_ELIGIBLE
      WHERE start_time > DATEADD('day', -7, CURRENT_TIMESTAMP())
      GROUP BY warehouse_name
      ORDER BY num_eligible_queries DESC;
    

Copy

Identify the warehouses with the most eligible time for the query acceleration
service in the past week:

    
    
    SELECT warehouse_name, SUM(eligible_query_acceleration_time) AS total_eligible_time
      FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_ELIGIBLE
      WHERE start_time > DATEADD('day', -7, CURRENT_TIMESTAMP())
      GROUP BY warehouse_name
      ORDER BY total_eligible_time DESC;
    

Copy

Identify the upper limit [scale factor](../sql-reference/sql/create-
warehouse.html#label-query-acceleration-max-scale-factor) in the past week for
the query acceleration service for warehouse `mywh`:

    
    
    SELECT MAX(upper_limit_scale_factor)
      FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_ELIGIBLE
      WHERE warehouse_name = 'MYWH'
      AND start_time > DATEADD('day', -7, CURRENT_TIMESTAMP());
    

Copy

Identify the distribution of scale factors in the past week for the query
acceleration service for warehouse `mywh`:

    
    
    SELECT upper_limit_scale_factor, COUNT(upper_limit_scale_factor)
      FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_ELIGIBLE
      WHERE warehouse_name = 'MYWH'
      AND start_time > DATEADD('day', -7, CURRENT_TIMESTAMP())
      GROUP BY 1 ORDER BY 1;
    

Copy

## Supported SQL commands¶

The query acceleration service supports the following SQL commands:

>   * SELECT
>
>   * INSERT
>
>   * CREATE TABLE AS SELECT (CTAS)
>
>   * COPY INTO <table>
>
>

A query, or a portion of a query (i.e. subquery or clause), with a supported
SQL command might be accelerated by the query acceleration service if it is
eligible for acceleration.

## Enabling query acceleration¶

Enable the query acceleration service by specifying ENABLE_QUERY_ACCELERATION
= TRUE when creating a warehouse (using [CREATE WAREHOUSE](../sql-
reference/sql/create-warehouse)) or later (using [ALTER WAREHOUSE](../sql-
reference/sql/alter-warehouse)).

### Examples¶

The following example enables the query acceleration service for a warehouse
named `my_wh`:

>
>     CREATE WAREHOUSE my_wh WITH
>       ENABLE_QUERY_ACCELERATION = true;
>  
>
> Copy

Execute the [SHOW WAREHOUSES](../sql-reference/sql/show-warehouses) command to
display details about the `my_wh` warehouse.

>
>     SHOW WAREHOUSES LIKE 'my_wh';
>  
>
> +---------+---------+----------+---------+---------+--------+------------+------------+--------------+-------------+-----------+--------------+-----------+-------+-------------------------------+-------------------------------+-------------------------------+--------------+---------+---------------------------+-------------------------------------+------------------+---------+----------+--------+-----------+------------+
>     | name    | state   | type     | size    | running | queued | is_default | is_current | auto_suspend | auto_resume | available | provisioning | quiescing | other | created_on                    | resumed_on                    | updated_on                    | owner        | comment | enable_query_acceleration | query_acceleration_max_scale_factor | resource_monitor | actives | pendings | failed | suspended | uuid       |
>
> |---------+---------+----------+---------+---------+--------+------------+------------+--------------+-------------+-----------+--------------+-----------+-------+-------------------------------+-------------------------------+-------------------------------+--------------+---------+---------------------------+-------------------------------------+------------------+---------+----------+--------+-----------+------------|
>     | MY_WH   | SUSPENDED | STANDARD | Medium |       0 |      0 | N          | N          |          600 | true        |           |              |           |       | 2023-01-20 14:31:49.283 -0800 | 2023-01-20 14:31:49.388 -0800 | 2023-01-20 16:34:28.583 -0800 | ACCOUNTADMIN |         | true                      |                                   8 | null             |       0 |        0 |      0 |         4 | 1132659053 |
>
> +---------+---------+----------+---------+---------+--------+------------+------------+--------------+-------------+-----------+--------------+-----------+-------+-------------------------------+-------------------------------+-------------------------------+--------------+---------+---------------------------+-------------------------------------+------------------+---------+----------+--------+-----------+------------+
>  
>
> Copy

The query acceleration service may increase the credit consumption rate of a
warehouse. The maximum scale factor can help limit the consumption rate. See
[CREATE WAREHOUSE](../sql-reference/sql/create-warehouse) or [ALTER
WAREHOUSE](../sql-reference/sql/alter-warehouse) for more details about the
[QUERY_ACCELERATION_MAX_SCALE_FACTOR](../sql-reference/sql/create-
warehouse.html#label-query-acceleration-max-scale-factor) property.

The QUERY_ACCELERATION_ELIGIBLE view and the
SYSTEM$ESTIMATE_QUERY_ACCELERATION function might be useful in determining an
appropriate scale factor for a warehouse. See Identifying queries and
warehouses that might benefit from query acceleration (in this topic) for
details.

## Adjusting the scale factor¶

The scale factor is a cost control mechanism that allows you to set an upper
bound on the amount of compute resources a warehouse can lease for query
acceleration. This value is used as a multiplier based on warehouse size and
cost.

For example, suppose that you set the scale factor to 5 for a medium
warehouse. This means that:

  * The warehouse can lease compute resources up to 5 times the size of a medium warehouse.

  * Because a medium warehouse costs [4 credits per hour](cost-understanding-compute.html#label-virtual-warehouse-credit-usage), leasing these resources can cost up to an additional 20 credits per hour (4 credits per warehouse x 5 times its size).

The cost is the same no matter how many queries are using the query
acceleration service at the same time. The query acceleration service is
billed by the second, only when the service is in use. These credits are
billed separately from warehouse usage.

Not all queries require the full set of resources that are made available by
the scale factor. The amount of resources requested for the service depends on
how much of the query is eligible for acceleration and how much data will be
processed to answer it. Regardless of the scale factor value or the amount of
resources requested, the amount of available compute resources for query
acceleration is bound by the availability of resources in the service and the
number of other concurrent requests. The query acceleration service only uses
as many resources as it needs and that are available at the time the query is
executed.

If the scale factor is not explicitly set, the default value is `8`. Setting
the scale factor to `0` eliminates the upper bound limit and allows queries to
lease as many resources as necessary and as available to service the query.

### Example¶

The following example modifies the warehouse named `my_wh` to enable the query
acceleration service with a maximum scale factor of 0.

>
>     ALTER WAREHOUSE my_wh SET
>       ENABLE_QUERY_ACCELERATION = true
>       QUERY_ACCELERATION_MAX_SCALE_FACTOR = 0;
>  
>
> Copy

## Monitoring query acceleration service usage¶

### Using the web interface to monitor query acceleration usage¶

Once you enable the query acceleration service, you can view the Profile
Overview panel in the [Query Profile tab](ui-snowsight-activity) to see the
effects of the query acceleration results.

The following screenshot displays an example of the statistics displayed for
the query overall. If multiple operations in a query were accelerated, the
results are aggregated in this view so you can see the total amount of work
done by the query acceleration service.

> ![../_images/query-acceleration-profile-overview.png](../_images/query-
> acceleration-profile-overview.png)

The Query Acceleration section of the Profile Overview panel includes the
following statistics:

  * _Partitions scanned by service_ — number of files offloaded for scanning to the query acceleration service.

  * _Scans selected for acceleration_ — number of table scans being accelerated.

In the operator details (see [Statistics](ui-snowsight-activity.html#label-
snowsight-query-profile-statistics)), click on the operator to see detailed
information. The following screenshot displays an example of the statistics
displayed for a TableScan operation:

> ![../_images/query-acceleration-table-scan.png](../_images/query-
> acceleration-table-scan.png)

The Query Acceleration section of the TableScan details panel includes the
following statistics:

  * _Partitions scanned by service_ — number of files offloaded for scanning to the query acceleration service.

### Using the Account Usage QUERY_HISTORY view to monitor query acceleration
usage¶

To see the effects of query acceleration on a query, you can use the following
columns in the [QUERY_HISTORY view](../sql-reference/account-
usage/query_history).

  * QUERY_ACCELERATION_BYTES_SCANNED

  * QUERY_ACCELERATION_PARTITIONS_SCANNED

  * QUERY_ACCELERATION_UPPER_LIMIT_SCALE_FACTOR

You can use these columns to identify the queries that benefited from the
query acceleration service. For each query, you can also determine the total
number of partitions and bytes scanned by the query acceleration service.

For descriptions of each of these columns, see [QUERY_HISTORY view](../sql-
reference/account-usage/query_history).

Note

For a given query, the sum of the QUERY_ACCELERATION_BYTES_SCANNED and
BYTES_SCANNED columns might be greater when the query acceleration service is
used than when the service is not used. The same is true for the sum of the
columns QUERY_ACCELERATION_PARTITIONS_SCANNED and PARTITIONS_SCANNED.

The increase in the number of bytes and partitions is due to the intermediary
results that are generated by the service to facilitate query acceleration.

For example, to find the queries with the most bytes scanned by the query
acceleration service in the past 24 hours:

    
    
    SELECT query_id,
           query_text,
           warehouse_name,
           start_time,
           end_time,
           query_acceleration_bytes_scanned,
           query_acceleration_partitions_scanned,
           query_acceleration_upper_limit_scale_factor
      FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
      WHERE query_acceleration_partitions_scanned > 0 
      AND start_time >= DATEADD(hour, -24, CURRENT_TIMESTAMP())
      ORDER BY query_acceleration_bytes_scanned DESC;
    

Copy

To find the queries with the largest number of partitions scanned by the query
acceleration service in the past 24 hours:

    
    
    SELECT query_id,
           query_text,
           warehouse_name,
           start_time,
           end_time,
           query_acceleration_bytes_scanned,
           query_acceleration_partitions_scanned,
           query_acceleration_upper_limit_scale_factor
      FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
      WHERE query_acceleration_partitions_scanned > 0 
      AND start_time >= DATEADD(hour, -24, CURRENT_TIMESTAMP())
      ORDER BY query_acceleration_partitions_scanned DESC;
    

Copy

## Query acceleration service cost¶

Query Acceleration consumes credits as it uses [serverless compute
resources](cost-understanding-compute.html#label-serverless-credit-usage) to
execute portions of eligible queries.

Query Acceleration is billed like other serverless features in Snowflake in
that you pay by the second for the compute resources used. To learn how many
credits per compute-hour are consumed by the Query Acceleration Service, refer
to the “Serverless Feature Credit Table” in the [Snowflake Service Consumption
Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

### Viewing billing information in the Classic Console¶

If you have Query Acceleration enabled for your account, the billing page in
the Classic Console includes a warehouse called QUERY_ACCELERATION that shows
all credits used by the service across all warehouses in your account.

The screenshot below shows an example of the billing information displayed for
the QUERY_ACCELERATION warehouse:

> ![../_images/query-acceleration-billing-ui.png](../_images/query-
> acceleration-billing-ui.png)

### Viewing billing using the Account Usage QUERY_ACCELERATION_HISTORY view¶

You can view billing data in the Account Usage [QUERY_ACCELERATION_HISTORY
view](../sql-reference/account-usage/query_acceleration_history).

#### Example¶

This query returns the total number of credits used by each warehouse in your
account for the query acceleration service (month-to-date):

    
    
    SELECT warehouse_name,
           SUM(credits_used) AS total_credits_used
      FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_HISTORY
      WHERE start_time >= DATE_TRUNC(month, CURRENT_DATE)
      GROUP BY 1
      ORDER BY 2 DESC;
    

Copy

### Viewing billing using the Organization Usage QUERY_ACCELERATION_HISTORY
view¶

You can view billing data for the query acceleration service for all accounts
in your organization in the Organization Usage [QUERY_ACCELERATION_HISTORY
view](../sql-reference/organization-usage/query_acceleration_history).

#### Example¶

This query returns the total number of credits used by each warehouse in each
account for the query acceleration service (month-to-date):

    
    
    SELECT account_name,
           warehouse_name,
           SUM(credits_used) AS total_credits_used
      FROM SNOWFLAKE.ORGANIZATION_USAGE.QUERY_ACCELERATION_HISTORY
      WHERE usage_date >= DATE_TRUNC(month, CURRENT_DATE)
      GROUP BY 1, 2
      ORDER BY 3 DESC;
    

Copy

### Viewing billing using the QUERY_ACCELERATION_HISTORY function¶

You can also view billing data using the Information Schema
[QUERY_ACCELERATION_HISTORY](../sql-
reference/functions/query_acceleration_history) function.

#### Example¶

The following example uses the QUERY_ACCELERATION_HISTORY function to return
information about the queries accelerated by this service within the past 12
hours:

>
>     SELECT start_time,
>            end_time,
>            credits_used,
>            warehouse_name,
>            num_files_scanned,
>            num_bytes_scanned
>       FROM TABLE(INFORMATION_SCHEMA.QUERY_ACCELERATION_HISTORY(
>         date_range_start=>DATEADD(H, -12, CURRENT_TIMESTAMP)));
>  
>
> Copy

## Evaluating cost and performance¶

This section includes example queries that might help you evaluate query
performance and cost before and after enabling the query acceleration service.

### Viewing warehouse and query acceleration service costs¶

The following query computes the costs of the warehouse and the query
acceleration service for a specific warehouse. You can execute this query
after enabling the query acceleration service for a warehouse to compare costs
before and after enabling query acceleration. The date range for the query
begins 8 weeks prior to the first credit usage for the query acceleration
service to 8 weeks after the last incurred cost for query acceleration service
(or up to the current date).

Note

  * This query is most useful for evaluating the cost of the service if the warehouse properties and workload remain the same before and after enabling the query acceleration service.

  * This query returns results only if there has been credit usage for accelerated queries in the warehouse.

This example query returns the warehouse and query acceleration service costs
for `my_warehouse`:

    
    
    WITH credits AS (
      SELECT 'QC' AS credit_type,
             TO_DATE(end_time) AS credit_date,
             SUM(credits_used) AS num_credits
        FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_HISTORY
        WHERE warehouse_name = 'my_warehouse'
        AND credit_date BETWEEN
               DATEADD(WEEK, -8, (
                 SELECT TO_DATE(MIN(end_time))
                   FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_HISTORY
                   WHERE warehouse_name = 'my_warehouse'
               ))
               AND
               DATEADD(WEEK, +8, (
                 SELECT TO_DATE(MAX(end_time))
                   FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_HISTORY
                   WHERE warehouse_name = 'my_warehouse'
               ))
      GROUP BY credit_date
      UNION ALL
      SELECT 'WC' AS credit_type,
             TO_DATE(end_time) AS credit_date,
             SUM(credits_used) AS num_credits
        FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
        WHERE warehouse_name = 'my_warehouse'
        AND credit_date BETWEEN
               DATEADD(WEEK, -8, (
                 SELECT TO_DATE(MIN(end_time))
                   FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_HISTORY
                   WHERE warehouse_name = 'my_warehouse'
               ))
               AND
               DATEADD(WEEK, +8, (
                 SELECT TO_DATE(MAX(end_time))
                   FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_HISTORY
                   WHERE warehouse_name = 'my_warehouse'
               ))
      GROUP BY credit_date
    )
    SELECT credit_date,
           SUM(IFF(credit_type = 'QC', num_credits, 0)) AS qas_credits,
           SUM(IFF(credit_type = 'WC', num_credits, 0)) AS compute_credits,
           compute_credits + qas_credits AS total_credits,
           AVG(total_credits) OVER (
             PARTITION BY NULL ORDER BY credit_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
             AS avg_total_credits_7days
      FROM credits
      GROUP BY credit_date
      ORDER BY credit_date;
    

Copy

### Viewing query performance¶

This query returns the average execution time for query acceleration eligible
queries for a given warehouse. The date range for the query begins 8 weeks
prior to the first credit usage for the query acceleration service to 8 weeks
after the last incurred cost for query acceleration service (or up to the
current date). The results might help you evaluate how the average query
performance changed after enabling the query acceleration service.

Note

  * This query is most useful for evaluating query performance if the warehouse workload remains the same before and after enabling the query acceleration service.

  * If the warehouse workload remains stable, the value in the `num_execs` column should remain consistent.

  * If the value in the `num_execs` column of the query results dramatically increases or decreases, the results of this query will likely not be useful for query performance evaluation.

This example query returns the query execution time by day and computes the 7
day average for the week prior for queries that are eligible for acceleration
in the warehouse `my_warehouse`:

    
    
    WITH qas_eligible_or_accelerated AS (
      SELECT TO_DATE(qh.end_time) AS exec_date,
            COUNT(*) AS num_execs,
            SUM(qh.execution_time) AS exec_time,
            MAX(IFF(qh.query_acceleration_bytes_scanned > 0, 1, NULL)) AS qas_accel_flag
        FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY AS qh
        WHERE qh.warehouse_name = 'my_warehouse'
        AND TO_DATE(qh.end_time) BETWEEN
               DATEADD(WEEK, -8, (
                 SELECT TO_DATE(MIN(end_time))
                   FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_HISTORY
                  WHERE warehouse_name = 'my_warehouse'
               ))
               AND
               DATEADD(WEEK, +8, (
                 SELECT TO_DATE(MAX(end_time))
                   FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_HISTORY
                  WHERE warehouse_name = 'my_warehouse'
               ))
        AND (qh.query_acceleration_bytes_scanned > 0
              OR
              EXISTS (
                SELECT 1
                  FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ACCELERATION_ELIGIBLE AS qae
                   WHERE qae.query_id = qh.query_id
                   AND qae.warehouse_name = qh.warehouse_name
              )
             )
        GROUP BY exec_date
    )
    SELECT exec_date,
           SUM(exec_time) OVER (
             PARTITION BY NULL ORDER BY exec_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
           ) /
           NULLIFZERO(SUM(num_execs) OVER (
             PARTITION BY NULL ORDER BY exec_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
           ) AS avg_exec_time_7days,
          exec_time / NULLIFZERO(num_execs) AS avg_exec_time,
          qas_accel_flag,
          num_execs,
          exec_time
      FROM qas_eligible_or_accelerated;
    

Copy

The output from the statement includes the following columns:

Column | Description  
---|---  
EXEC_DATE | Query execution date.  
AVG_EXEC_TIME_7DAYS | The average execution time for the prior 7 days inclusive of EXEC_DATE.  
AVG_EXEC_TIME | The average query execution time.  
QAS_ACCEL_FLAG | 1 if any queries were accelerated; NULL if no queries were accelerated.  
NUM_EXECS | Number of queries accelerated.  
EXEC_TIME | Total execution time of all query acceleration eligible queries.  
  
## Compatibility with search optimization¶

Query acceleration and [search optimization](search-optimization-service) can
work together to optimize query performance. First, search optimization can
prune the [micro-partitions](tables-clustering-micropartitions.html#label-
what-are-micropartitions) not needed for a query. Then, for eligible queries,
query acceleration can offload portions of the rest of the work to shared
compute resources provided by the service.

Performance of queries accelerated by both services varies depending on
workload and available resources.

