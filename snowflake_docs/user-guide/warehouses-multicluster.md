# Multi-cluster warehouses¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Enterprise Edition
Feature](intro-editions)

To inquire about upgrading to Enterprise Edition (or higher), please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Multi-cluster warehouses enable you to scale compute resources to manage your
user and query concurrency needs as they change, such as during peak and off
hours.

## What is a multi-cluster warehouse?¶

By default, a virtual warehouse consists of a single cluster of compute
resources available to the warehouse for executing queries. As queries are
submitted to a warehouse, the warehouse allocates resources to each query and
begins executing the queries. If sufficient resources are not available to
execute all the queries submitted to the warehouse, Snowflake queues the
additional queries until the necessary resources become available.

With multi-cluster warehouses, Snowflake supports allocating, either
statically or dynamically, additional clusters to make a larger pool of
compute resources available. A multi-cluster warehouse is defined by
specifying the following properties:

  * Maximum number of clusters, greater than 1 (up to 10).

  * Minimum number of clusters, equal to or less than the maximum (up to 10).

Additionally, multi-cluster warehouses support all the same properties and
actions as single-cluster warehouses, including:

  * Specifying a warehouse size.

  * Resizing a warehouse at any time.

  * Auto-suspending a running warehouse due to inactivity; note that this does not apply to individual clusters, but rather the entire multi-cluster warehouse.

  * Auto-resuming a suspended warehouse when new queries are submitted.

### Maximized vs. auto-scale¶

You can choose to run a multi-cluster warehouse in either of the following
modes:

Maximized:

    

This mode is enabled by specifying the same value for both maximum and minimum
number of clusters (note that the specified value must be larger than 1). In
this mode, when the warehouse is started, Snowflake starts all the clusters so
that maximum resources are available while the warehouse is running.

This mode is effective for statically controlling the available compute
resources, particularly if you have large numbers of concurrent user sessions
and/or queries and the numbers do not fluctuate significantly.

Auto-scale:

    

This mode is enabled by specifying different values for maximum and minimum
number of clusters. In this mode, Snowflake starts and stops clusters as
needed to dynamically manage the load on the warehouse:

  * As the number of concurrent user sessions and/or queries for the warehouse increases, and queries start to queue due to insufficient resources, Snowflake automatically starts additional clusters, up to the maximum number defined for the warehouse.

  * Similarly, as the load on the warehouse decreases, Snowflake automatically shuts down clusters to reduce the number of running clusters and, correspondingly, the number of credits used by the warehouse.

To help control the usage of credits in Auto-scale mode, Snowflake provides a
property, SCALING_POLICY, that determines the scaling policy to use when
automatically starting or shutting down additional clusters. For more
information, see Setting the scaling policy for a multi-cluster warehouse (in
this topic).

Tip

To create a multi-cluster warehouse, see Creating a multi-cluster warehouse
(in this topic).

Note the following:

  * For multi-cluster warehouses, the maximum number of clusters in the Maximum Clusters field (Web Interface) or for the MAX_CLUSTER_COUNT property (SQL) must be _greater_ than 1.

  * For single-cluster warehouses, the maximum and minimum number of clusters must _both be equal_ to 1.

  * For auto-scale mode, the maximum number of clusters must be _greater_ than the minimum number of clusters.

  * For maximized mode, the maximum number of clusters must be _equal_ to the minimum number of clusters.

When determining the maximum and minimum number of clusters to use for a
multi-cluster warehouse, start with Auto-scale mode and start small (e.g.
maximum = 2 or 3, minimum = 1). As you track how your warehouse load
fluctuates over time, you can increase the maximum and minimum number of
clusters until you determine the numbers that best support the upper and lower
boundaries of your user/query concurrency.

### Multi-cluster size and credit usage¶

The amount of compute resources in each cluster is determined by the warehouse
size:

  * The total number of clusters for the multi-cluster warehouse is calculated by multiplying the warehouse size by the maximum number of clusters. This also indicates the maximum number of credits consumed by the warehouse per full hour of usage (i.e. if all clusters run during the hour).

For example, the maximum number of credits consumed per hour for a Medium-size
multi-cluster warehouse with 3 clusters is 12 credits.

  * If a multi-cluster warehouse is resized, the new size applies to all the clusters for the warehouse, including clusters that are currently running and any clusters that are started after the multi-cluster warehouse is resized.

The actual number of credits consumed per hour depends on the number of
clusters running during each hour that the warehouse is running. For more
details, see Examples of multi-cluster credit usage (in this topic).

### Benefits of multi-cluster warehouses¶

With a standard, single-cluster warehouse, if your user/query load increases
to the point where you need more compute resources:

  1. You must either increase the size of the warehouse or start additional warehouses and explicitly redirect the additional users/queries to these warehouses.

  2. Then, when the resources are no longer needed, to conserve credits, you must manually downsize the larger warehouse or suspend the additional warehouses.

In contrast, a multi-cluster warehouse enables larger numbers of users to
connect to the same size warehouse. In addition:

  * In Auto-scale mode, a multi-cluster warehouse eliminates the need for resizing the warehouse or starting and stopping additional warehouses to handle fluctuating workloads. Snowflake automatically starts and stops additional clusters as needed.

  * In Maximized mode, you can control the capacity of the multi-cluster warehouse by increasing or decreasing the number of clusters as needed.

Tip

Multi-cluster warehouses are best utilized for scaling resources to improve
concurrency for users/queries. They are not as beneficial for improving the
performance of slow-running queries or data loading. For these types of
operations, resizing the warehouse provides more benefits.

## Examples of multi-cluster credit usage¶

The following four examples illustrate credit usage for a multi-cluster
warehouse. Refer to [Virtual warehouse credit usage](cost-understanding-
compute.html#label-virtual-warehouse-credit-usage) for the number of credits
billed per full hour by warehouse size.

Note

For the sake of simplicity, all these examples depict credit usage in
increments of 1 hour, 30 minutes, and 15 minutes. In a real-world scenario,
with per-second billing, the actual credit usage would contain fractional
amounts, based on the number of seconds that each cluster runs.

### Example 1: Maximized (2 Hours)¶

In this example, a Medium-size warehouse with 3 clusters runs in Maximized
mode for 2 hours:

| Cluster 1 | Cluster 2 | Cluster 3 | **Total Credits**  
---|---|---|---|---  
1st Hour | 4 | 4 | 4 | **12**  
2nd Hour | 4 | 4 | 4 | **12**  
**Total Credits** | **8** | **8** | **8** | **24**  
  
### Example 2: Auto-scale (2 Hours)¶

In this example, a Medium-size warehouse with 3 clusters runs in Auto-scale
mode for 2 hours:

  * Cluster 1 runs continuously.

  * Cluster 2 runs continuously for the 2nd hour only.

  * Cluster 3 runs for 30 minutes during the 2nd hour.

| Cluster 1 | Cluster 2 | Cluster 3 | **Total Credits**  
---|---|---|---|---  
1st Hour | 4 | 0 | 0 | **4**  
2nd Hour | 4 | 4 | 2 | **10**  
**Total Credits** | **8** | **4** | **2** | **14**  
  
### Example 3: Auto-scale (3 Hours)¶

In this example, a Medium-size warehouse with 3 clusters runs in Auto-scale
mode for 3 hours:

  * Cluster 1 runs continuously.

  * Cluster 2 runs continuously for the entire 2nd hour and 30 minutes in the 3rd hour.

  * Cluster 3 runs for 30 minutes in the 3rd hour.

| Cluster 1 | Cluster 2 | Cluster 3 | **Total Credits**  
---|---|---|---|---  
1st Hour | 4 | 0 | 0 | **4**  
2nd Hour | 4 | 4 | 0 | **8**  
3rd Hour | 4 | 2 | 2 | **8**  
**Total Credits** | **12** | **6** | **2** | **20**  
  
### Example 4: Auto-scale (3 Hours) with resize¶

In this example, the same warehouse from example 3 runs in Auto-scale mode for
3 hours with a resize from Medium to Large:

  * Cluster 1 runs continuously.

  * Cluster 2 runs continuously for the 2nd and 3rd hours.

  * Warehouse is resized from Medium to Large at 1:30 hours.

  * Cluster 3 runs for 15 minutes in the 3rd hour.

| Cluster 1 | Cluster 2 | Cluster 3 | **Total Credits**  
---|---|---|---|---  
1st Hour | 4 | 0 | 0 | **4**  
2nd Hour | 4+2 | 4+2 | 0 | **12**  
3rd Hour | 8 | 8 | 2 | **18**  
**Total Credits** | **18** | **14** | **2** | **34**  
  
## Creating a multi-cluster warehouse¶

You can create a multi-cluster warehouse through the web interface or using
SQL:

> Web Interface:
>  
>
> Click on Warehouses [![Warehouses tab](../_images/ui-navigation-warehouse-
> icon.svg)](../_images/ui-navigation-warehouse-icon.svg) » Create:
>
>   1. In the Maximum Clusters field, select a value greater than 1.
>
>   2. In the Minimum Clusters field, optionally select a value greater than
> 1.
>
>   3. Enter other information for the warehouse, as needed, and click Finish.
>
>

> SQL:
>  
>
> Execute a [CREATE WAREHOUSE](../sql-reference/sql/create-warehouse) command
> with:
>
>   * `MAX_CLUSTER_COUNT` set to a value greater than `1`.
>
>   * `MIN_CLUSTER_COUNT` (optionally) set to a value greater than `1`.
>
>

To view information about the multi-cluster warehouses you create:

> Classic Console:
>  
>
> Click on Warehouses [![Warehouses tab](../_images/ui-navigation-warehouse-
> icon.svg)](../_images/ui-navigation-warehouse-icon.svg)
>
> The Clusters column displays the minimum and maximum clusters for each
> warehouse, as well as the number of clusters that are currently running if
> the warehouse is started.
>
> SQL:
>  
>
> Execute a [SHOW WAREHOUSES](../sql-reference/sql/show-warehouses) command.
>
> The output includes three columns (`min_cluster_count`, `max_cluster_count`,
> `started_clusters_column`) that display the same information provided in the
> Clusters column in the web interface.

All other tasks for multi-cluster warehouses (except for the remaining tasks
described in this topic) are identical to single-cluster [warehouse
tasks](warehouses-tasks).

## Setting the scaling policy for a multi-cluster warehouse¶

To help control the credits consumed by a multi-cluster warehouse running in
Auto-scale mode, Snowflake provides scaling policies, which are used to
determine when to start or shut down a cluster.

The scaling policy for a multi-cluster warehouse only applies if it is running
in Auto-scale mode. In Maximized mode, all clusters run concurrently so there
is no need to start or shut down individual clusters.

Snowflake supports the following scaling policies:

Policy | Description | Warehouse Starts… | Warehouse Shuts Down…  
---|---|---|---  
Standard (default) | Prevents/minimizes queuing by favoring starting additional clusters over conserving credits. | The first cluster starts immediately when either a query is queued or the system detects that there’s one more query than the currently-running clusters can execute. Each successive cluster waits to start 20 seconds after the prior one has started. For example, if your warehouse is configured with 10 max clusters, it can take a full 200+ seconds to start all 10 clusters. | After 2 to 3 consecutive successful checks (performed at 1 minute intervals), which determine whether the load on the least-loaded cluster could be redistributed to the other clusters without spinning up the cluster again.  
Economy | Conserves credits by favoring keeping running clusters fully-loaded rather than starting additional clusters, which may result in queries being queued and taking longer to complete. | Only if the system estimates there’s enough query load to keep the cluster busy for at least 6 minutes. | After 5 to 6 consecutive successful checks (performed at 1 minute intervals), which determine whether the load on the least-loaded cluster could be redistributed to the other clusters without spinning up the cluster again.  
  
Note

A third scaling policy, Legacy, was provided for backward compatibility. In
contrast to the other policies, it used a static approach based on length of
time a warehouse is active/inactive.

Legacy has been obsoleted/removed. All warehouses that were using the Legacy
policy now use the default Standard policy.

The scaling policy for a multi-cluster warehouse can be set when it is created
or at any time afterwards, either through the web interface or using SQL:

> Classic Console:
>  
>
> Click on:
>
>   * Warehouses [![Warehouses tab](../_images/ui-navigation-warehouse-
> icon.svg)](../_images/ui-navigation-warehouse-icon.svg) » Create or
>
>   * Warehouses [![Warehouses tab](../_images/ui-navigation-warehouse-
> icon.svg)](../_images/ui-navigation-warehouse-icon.svg) » _<
> warehouse_name>_ » Configure
>
>

>
> In the Scaling Policy field, select the desired value from the drop-down
> list.
>
> SQL:
>  
>
> Execute a [CREATE WAREHOUSE](../sql-reference/sql/create-warehouse) or
> [ALTER WAREHOUSE](../sql-reference/sql/alter-warehouse) command with
> `SCALING_POLICY` set to the desired value.

For example, in SQL:

>
>     ALTER WAREHOUSE mywh SET SCALING_POLICY = 'ECONOMY';
>  
>
> Copy

## Increasing or decreasing clusters for a multi-cluster warehouse¶

You can increase or decrease the number of clusters for a warehouse at any
time, even while it is running and executing statements. Clusters can be
increased or decreased for a warehouse through the web interface or using SQL:

> Classic Console:
>  
>
> Click on Warehouses [![Warehouses tab](../_images/ui-navigation-warehouse-
> icon.svg)](../_images/ui-navigation-warehouse-icon.svg) » _<
> warehouse_name>_ » Configure
>
> SQL:
>  
>
> Execute an [ALTER WAREHOUSE](../sql-reference/sql/alter-warehouse) command.

The effect of changing the maximum and minimum clusters for a running
warehouse depends on whether it is running in Maximized or Auto-scale mode:

  * Maximized:

↑ max & min:

    

Specified number of clusters start immediately.

↓ max & min:

    

Specified number of clusters shut down when they finish executing statements
and the auto-suspend period elapses.

  * Auto-scale:

↑ max:

    

If `new_max_clusters > running_clusters`, no changes until additional clusters
are needed.

↓ max:

    

If `new_max_clusters < running_clusters`, excess clusters shut down when they
finish executing statements and the scaling policy conditions are met.

↑ min:

    

If `new_min_clusters > running_clusters`, additional clusters immediately
started to meet the minimum.

↓ min:

    

If `new_min_clusters < running_clusters`, excess clusters shut down when they
finish executing statements and the scaling policy conditions are met.

## Monitoring multi-cluster warehouses¶

You can monitor usage of multi-cluster warehouses through the web interface:

> Classic Console:
>  
>
> Click on History [![History tab](../_images/ui-navigation-history-
> icon.svg)](../_images/ui-navigation-history-icon.svg)
>
> This page includes a column, Cluster Number, that specifies the cluster used
> to execute the statements submitted to each warehouse.

