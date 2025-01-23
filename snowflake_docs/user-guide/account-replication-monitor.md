# Monitoring replication and failover¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Standard & Business Critical
Feature](intro-editions)

  * Database and share replication are available to all accounts.

  * Replication of other account objects & failover/failback require Business Critical Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic provides information on how to monitor account replication
progress, history, and costs.

## Use Snowsight to monitor replication¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Preview Feature](../release-
notes/preview-features) — Open

Available to accounts in all regions and cloud platforms. Currently this
feature is not supported for accounts using private connectivity.

To monitor the replication progress and status for [replication and failover
groups](account-replication-intro.html#label-replication-and-failover-groups)
in an organization, use the Replication page in Snowsight.

You can view the status and details of refresh operations, including:

  * Current status of the most recent refresh operation.

  * Replica lag time (time since the last refresh operation).

  * Distribution of replica lag times across groups.

  * Date and time of the next scheduled refresh operation.

Note

  * Snowsight lists the replication and failover groups for which your role has the MONITOR, OWNERSHIP, or REPLICATE privilege on.

  * Refresh operation details are only available to users with the ACCOUNTADMIN role or the OWNERSHIP privilege on the group.

  * You must be signed in to the target account to view refresh operation details. If you are not, you will be prompted to sign in.

Both the source account and the target account must use the same connection
type (public internet). Otherwise, signing in to the target account fails.

To view the replication status of each replication or failover group, complete
the following steps:

  1. Sign in to Snowsight and navigate to Admin » Accounts.

  2. Select Replication and then select Groups.

The Groups page displays refresh operation details for all the groups for
which your role has a privilege to view. You can use the tiles to filter the
view.

  * For example, if the Status tile indicates there are failed refresh operations, you can select the tile to investigate the group(s) with failures.

  * The lag time in the Longest Replication lag tile refers to the duration of time since the last refresh operation. This is the length of time that the secondary replication or failover group _lags_ behind the primary group. The longest lag time is the length of time since the oldest secondary replication group was last refreshed.

For example, if you have three failover groups, `fg_1`, `fg_2`, `fg_3`, with
independent replication schedules of 10 minutes, 2 hours, and 12 hours
respectively, the longest lag time could be as long as 12 hours. If `fg_3`,
however, was recently refreshed in the target account, its lag time resets to
0 and a different failover group could have a longer lag time.

  * You can select an individual bar in the Group Lag Distribution tile to filter the results to an individual group.

You can also filter groups by using the search field or the dropdown menus:

  * You can search by replication or failover group name using the [![Search icon](../_images/search-icon.svg)](../_images/search-icon.svg) (search) box.

  * Choose Type to filter the results by replication or failover group.

  * Choose Replicating to filter by primary (select To) or secondary groups (select From).

  * Choose the [![Account icon](../_images/account-icon.svg)](../_images/account-icon.svg) (accounts) menu to filter the results by account name.

  * Choose Status to filter results by refresh operation status:

    * Refresh Cancelled

    * Refresh Failed

    * Refresh In Progress

    * Refresh Successful

You can see the following details about your replication and failover groups:

Column | Description  
---|---  
Name | Name of the replication or failover group.  
Is Replicating | Indicates if the group is being replicated _to_ a target account or _from_ a source account. If this column contains _destinations available_ , there are no secondary replication or failover groups. The number of destinations available indicates the number of target accounts the primary group can be replicated to.  
Status | Displays the status of the latest refresh operation. You must be signed in to the target account in order to access replication details. If you are not signed in, select Sign in to view refresh operation status for the secondary group. Both the source account and the target account must use the same connection type (public internet). Otherwise, signing in to the target account fails.  
Replication Lag | The length of time since the last refresh operation. This is the length of time that the secondary replication group “lags” behind the primary replication group.  
Next Refresh | The date and time of the next scheduled refresh operation.  
  
You can select a replication or failover group to view detailed information
about each refresh operation. For more information, see the section on
replication history in Snowsight.

## Monitor the progress of refresh operations¶

This section provides information on how to monitor replication progress for a
specific replication or failover group using either Snowsight or SQL.

### Use Snowsight to monitor the progress of refresh operations¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Preview Feature](../release-
notes/preview-features) — Open

Available to accounts in all regions and cloud platforms. Currently this
feature is not supported for accounts using private connectivity.

You can view the status of a refresh operation in progress and the details of
historical refresh operations using Snowsight.

  1. Sign in to Snowsight and navigate to Admin » Accounts.

  2. Select Replication, select Groups.

  3. Select the name of a replication or failover group.

For more information about the detailed view, see the section on replication
history in Snowsight.

### Use SQL to monitor the progress of refresh operations¶

To monitor the progress of a replication or failover group refresh, query the
[REPLICATION_GROUP_REFRESH_PROGRESS,
REPLICATION_GROUP_REFRESH_PROGRESS_BY_JOB](../sql-
reference/functions/replication_group_refresh_progress) table function (in the
[Snowflake Information Schema](../sql-reference/info-schema)).

#### Example¶

View the progress of the most recent refresh operation for the failover group
`myfg`:

    
    
    SELECT phase_name, start_time, end_time, progress, details
      FROM TABLE(INFORMATION_SCHEMA.REPLICATION_GROUP_REFRESH_PROGRESS('myfg'));
    

Copy

## View replication history¶

You can view replication history using Snowsight or using SQL.

Note

You can view the replication history for the replication and failover groups
for which your role has the MONITOR, OWNERSHIP, or REPLICATE privilege on.

### Use Snowsight to view replication history¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Preview Feature](../release-
notes/preview-features) — Open

Available to accounts in all regions and cloud platforms. Currently this
feature is not supported for accounts using private connectivity.

You can view the replication history and details for each refresh operation
for a specific replication or failover group in the details page for the
group.

  1. Sign in to Snowsight and navigate to Admin » Accounts.

  2. Select Replication, select Groups.

  3. Select the name of a replication or failover group.

You can then review the following information about the group:

  * Group type (replication group or failover group).

  * Replication schedule (for example, every 10 minutes).

  * Duration of each refresh operation.

  * Replica lag time (length of time since last refresh operation).

  * Date and time of the next scheduled refresh operation.

You can filter the data on the page by status and time period:

  * Choose Status to filter results by refresh operation status:

    * Refresh Cancelled

    * Refresh Failed

    * Refresh In Progress

    * Refresh Successful

  * Choose Duration to show refresh operation details for:

    * Last hour

    * Last 24 hours

    * Last 7 days

    * All

Selecting All displays the last 14 days of refresh operations.

The details for each refresh operation include the following columns:

Column | Description  
---|---  
Query ID | Query ID of the refresh operation.  
Status | Displays the status of the refresh operation. Valid values include `Successful`, `Failed`, `In Progress`.  
Ended | Date and time the refresh operation ended.  
Duration | The length of time the refresh operation took to complete. The duration period is broken down and color coded by [replication phase](../sql-reference/functions/replication_group_refresh_progress.html#label-replication-phases). The width of each colored segment indicates the portion of the time spent in that phase. The image below is for reference only. This graph is available when you select the refresh operation for additional details. [![Color coded replication phase and duration.](../_images/snowsight-replication-phases.png)](../_images/snowsight-replication-phases.png)  
Transferred | The number of bytes replicated.  
Objects | The number of objects replicated.  
  
Select a row to view additional details about a specific refresh operation
including:

  * Duration of each replication phase.

  * Error message (for failed refresh operations).

  * List of database objects replicated by type and number.

  * Number of databases replicated and database names.

### Use SQL to view replication history¶

To view the replication history of a specific replication or failover group
within a specified date range, query one of the following:

  * [REPLICATION_GROUP_REFRESH_HISTORY](../sql-reference/functions/replication_group_refresh_history) table function (in the [Snowflake Information Schema](../sql-reference/info-schema)).

  * [REPLICATION_GROUP_REFRESH_HISTORY view](../sql-reference/account-usage/replication_group_refresh_history) (in [Account Usage](../sql-reference/account-usage)).

#### Examples¶

Query the Information Schema REPLICATION_GROUP_REFRESH_HISTORY table function
to view the account replication history of failover group `myfg` in the last 7
days:

    
    
    SELECT PHASE_NAME, START_TIME, END_TIME, TOTAL_BYTES, OBJECT_COUNT
      FROM TABLE(information_schema.replication_group_refresh_history('myfg'))
      WHERE START_TIME >= current_date - interval '7 days';
    

Copy

Query the Account Usage REPLICATION_GROUP_REFRESH_HISTORY view to view the
account replication history in the current month:

    
    
    SELECT REPLICATION_GROUP_NAME, PHASE_NAME, START_TIME, END_TIME, TOTAL_BYTES, OBJECT_COUNT
      FROM snowflake.account_usage.replication_group_refresh_history
      WHERE START_TIME >= date_trunc('month', current_date());
    

Copy

## Monitor replication costs¶

To monitor credit usage for replication, query one of the following:

  * [REPLICATION_GROUP_USAGE_HISTORY view](../sql-reference/account-usage/replication_group_usage_history) (in [Account Usage](../sql-reference/account-usage)).

  * [REPLICATION_GROUP_USAGE_HISTORY](../sql-reference/functions/replication_group_usage_history) table function (in the [Snowflake Information Schema](../sql-reference/info-schema)).

### Examples¶

Query the REPLICATION_GROUP_USAGE_HISTORY table function to view credits used
for account replication in the last 7 days:

    
    
    SELECT start_time, end_time, replication_group_name, credits_used, bytes_transferred
      FROM table(information_schema.replication_group_usage_history(date_range_start=>dateadd('day', -7, current_date())));
    

Copy

Query the Account Usage REPLICATION_GROUP_USAGE_HISTORY view to view the
credits used by replication or failover group for account replication history
in the current month:

    
    
    SELECT start_time, 
      end_time, 
      replication_group_name, 
      credits_used, 
      bytes_transferred
    FROM snowflake.account_usage.replication_group_usage_history
    WHERE start_time >= DATE_TRUNC('month', CURRENT_DATE());
    

Copy

## Monitor replication costs for databases¶

The cost for replication for an individual database included in a replication
or failover group can be calculated by retrieving the number of copied bytes
for the database and associating it with the credits used.

### Examples¶

#### Query Account Usage views¶

The following examples calculate the costs for database replication in one
replication group for the past 30 days.

  1. Query the REPLICATION_GROUP_REFRESH_HISTORY Account Usage view and calculate the sum of the number of bytes replicated per database.

For example, to calculate the sum of the number of bytes replicated for
databases in the replication group `myrg` in the last 30 days:

    
        select sum(value:totalBytesToReplicate) as sum_database_bytes
    from snowflake.account_usage.replication_group_refresh_history rh,
        lateral flatten(input => rh.total_bytes:databases)
    where rh.replication_group_name = 'MYRG'
    and rh.start_time >= current_date - interval '30 days';
    

Copy

Note the output of the sum of database bytes:

    
        +--------------------+
    | SUM_DATABASE_BYTES |
    |--------------------|
    |              22016 |
    +--------------------+
    

Copy

  2. Query the REPLICATION_GROUP_USAGE_HISTORY Account Usage view and calculate the sum of the number of credits used and the sum of the bytes transferred for replication.

For example, to calculate the sum of the number of credits used and the sum of
the bytes transferred for replication of the replication group `myrg` in the
last 30 days:

    
        select sum(credits_used) as credits_used, SUM(bytes_transferred) as bytes_transferred
    from snowflake.account_usage.replication_group_usage_history
    where replication_group_name = 'MYRG'
    and start_time >= current_date - interval '30 days';
    

Copy

Note the output of the sum of the credits used and the sum of bytes
transferred:

    
        +--------------+-------------------+
    | CREDITS_USED | BYTES_TRANSFERRED |
    |--------------+-------------------|
    |  1.357923604 |             22013 |
    +--------------+-------------------+
    

Copy

  3. Calculate the replication costs for databases using the values of the bytes transferred for databases, sum of the credits used, and the sum of all bytes transferred for replication from the previous two steps:

> `(<database_bytes_transferred> / <bytes_transferred>) * <credits_used>`

For example:

> `(22016 / 22013) * 1.357923604 = 1.35810866)`

#### Query Information Schema table functions¶

For refresh operations within the past 14 days, query the associated
Information Schema table functions.

  * [REPLICATION_GROUP_REFRESH_HISTORY](../sql-reference/functions/replication_group_refresh_history)

  * [REPLICATION_GROUP_USAGE_HISTORY](../sql-reference/functions/replication_group_usage_history)

  1. Query the REPLICATION_GROUP_REFRESH_HISTORY table function to view the sum of the number of bytes copied for database replication for the replication group `myrg`:
    
        select sum(value:totalBytesToReplicate)
      from table(information_schema.replication_group_refresh_history('myrg')) as rh,
      lateral flatten(input => total_bytes:databases)
      where rh.phase_name = 'COMPLETED'
      and rh.start_time >= current_date - interval '14 days';
    

Copy

  2. Query the REPLICATION_GROUP_USAGE_HISTORY table function to view sum of the number of credits used and the sum of the bytes transferred for replication for the replication group `myrg`:
    
        select sum(credits_used), sum(bytes_transferred)
      from table(information_schema.replication_group_usage_history(
          date_range_start=>dateadd('day', -14, current_date()),
          replication_group_name => 'myrg'
      ));
    

Copy

