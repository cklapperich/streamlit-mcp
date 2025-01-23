# Monitoring warehouse load¶

The web interface provides a _query load_ chart that depicts concurrent
queries processed by a warehouse over a two-week period. Warehouse query load
measures the average number of queries that were running or queued within a
specific interval.

You can customize the time period and time interval during which to evaluate
warehouse performance by querying the Account Usage [QUERY_HISTORY
view](../sql-reference/account-usage/query_history).

## Viewing the load monitoring chart¶

Note

To view the load monitoring chart, you must be using a role that has the
MONITOR privilege on the warehouse.

To view the chart:

> Snowsight:
>  
>
> Select Admin » Warehouses » _< warehouse_name>_
>
> The Warehouse Activity tile appears with a bar chart and lets you select a
> window of time to view in the chart. By default, the chart displays the past
> two weeks in 1-day intervals.
>
> You can select a range from 1 hour (minimum) to 2 weeks (maximum). The chart
> displays the total query load in intervals of 1 minute to 1 day, depending
> on the range you selected.
>
> Classic Console:
>  
>
> Select Warehouses [![Warehouses tab](../_images/ui-navigation-warehouse-
> icon.svg)](../_images/ui-navigation-warehouse-icon.svg) » _<
> warehouse_name>_
>
> The Warehouse Load Over Time page appears with a bar chart and a slider for
> selecting the window of time to view in the chart. By default, the chart
> displays the past 8 hours in 5-minute intervals.
>
> Use the slider to select the range of time to view in the chart. You can
> select a range from 8 hours (minimum) to 14 days (maximum). The chart
> displays the total query load in intervals of 5 minutes to 1 hour, depending
> on the range you selected. As you change the size of the range, the
> intervals change dynamically to maintain the appropriate scale.
>
> You can also drag the slider to any position within the 14-day range to
> display the load for that period of time.

### Understanding the bar chart¶

Hover over a bar to view the average number of queries processed by the
warehouse during the time period represented. The bar displays the individual
load for each query status that occurred within the interval:

Query Status | Description  
---|---  
Running | Queries that were actively running during the interval. Note that they may have started running before and continued running after the interval.  
Queued (Provisioning) | Queries that were waiting while the warehouse provisioned compute resources. Typically only occurs in the first few minutes after a warehouse resumes.  
Blocked | Queries that were blocked during the interval due to a transaction lock.  
Queued | Queries that were waiting to run due to warehouse overload (i.e. waiting for other queries to finish running and free compute resources).  
  
## How query load is calculated¶

Query load is calculated by dividing the execution time (in seconds) of all
queries in an interval by the total time (in seconds) for the interval.

For example, the following table illustrates how query load is calculated
based on 5 queries that contributed to the warehouse load during a 5-minute
interval. The load from running queries was .92 and queued queries (due to
warehouse overload) was .08.

Query | Status | Execution Time / Interval (in Seconds) | Query Load  
---|---|---|---  
Query 1 | Running | 30 / 300 | 0.10  
Query 2 | Running | 201 / 300 | 0.67  
Query 3 | Running | 15 / 300 | 0.05  
Query 4 | Running | 30 / 300 | 0.10  
|  | **Running Load** | **0.92**  
Query 5 | Queued | 24 / 300 | 0.08  
|  | **Queued Load** | **0.08**  
|  | **TOTAL WAREHOUSE LOAD** | **1.00**  
  
To determine the actual number of running queries (and the duration of each
query) during a specific interval, consult the History [![History
tab](../_images/ui-navigation-history-icon.svg)](../_images/ui-navigation-
history-icon.svg) page. On the page, filter the query history by warehouse,
then scroll down to the interval you specified in the load monitoring chart.

## Using the load monitoring chart to make decisions¶

The load monitoring chart can help you make decisions for managing your
warehouses by showing current and historic usage patterns.

### Slow query performance¶

When you notice that a query is running slowly, check whether an overloaded
warehouse is causing the query to compete for resources or get queued:

  * If the running query load is high or there’s queuing, consider starting a separate warehouse and moving queued queries to that warehouse. Alternatively, if you are using [multi-cluster warehouses](warehouses-multicluster), you could change your multi-cluster settings to add additional clusters to handle higher concurrency going forward.

  * If the running query load is low and query performance is slow, you could resize the warehouse to provide more compute resources. You would need to restart the query once all the new resources were fully provisioned to take advantage of the added resources.

### Peak query performance¶

Analyze the daily workload on the warehouse over the previous two weeks. If
you see recurring usage spikes, consider moving some of the peak workload to
its own warehouse and potentially running the remaining workload on a smaller
warehouse. Alternatively, you could change your multi-cluster settings to add
additional clusters to handle higher concurrency going forward.

If you notice that your current workload is considerably higher than normal,
open the History [![History tab](../_images/ui-navigation-history-
icon.svg)](../_images/ui-navigation-history-icon.svg) page to investigate
which queries are contributing to the higher load.

### Excessive credit usage¶

Analyze the daily workload on the warehouse over the previous two weeks. If
the chart shows recurring time periods when the warehouse was running and
consuming credits, but the total query load was less than **1** for
substantial periods of time, the warehouse use is inefficient. You might
consider any of the following actions:

  * Decrease the warehouse size. Note that decreasing the warehouse size generally increases the query execution time.

  * For a multi-cluster warehouse, decrease the **MIN_CLUSTER_COUNT** parameter value.

## Using Account Usage QUERY_HISTORY view to evaluate warehouse performance¶

You can query the QUERY_HISTORY view to calculate virtual warehouse
performance metrics such as throughput and latency for specific statement
types. For more information, see [Examples: Warehouse performance](../sql-
reference/account-usage.html#label-account-usage-warehouse-performance-query).

