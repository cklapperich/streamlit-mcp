# Working with resource monitors¶

A _resource monitor_ can help control costs and avoid unexpected credit usage
caused by running warehouses. A [virtual warehouse](warehouses-overview)
consumes Snowflake credits while it runs. You can use a resource monitor to
monitor credit usage by virtual warehouses and the cloud services needed to
support those warehouses. You can also set up a resource monitor to suspend a
user-managed virtual warehouse when it reaches a credit limit.

The number of credits consumed depends on the size of the warehouse and how
long it runs. For more information on warehouse credit usage, see [Virtual
warehouse credit usage](cost-understanding-compute.html#label-virtual-
warehouse-credit-usage).

Credit usage limits can be set for a specified interval or date range. When a
limit is reached and/or reaches a specified threshold, the resource monitor
can trigger various actions, such as sending alert notifications and/or
suspending user-managed warehouses.

Only users with the ACCOUNTADMIN role can create a resource monitor, but an
account administrator can grant privileges to other roles to allow other users
to view and modify resource monitors.

## Resource monitor properties¶

A resource monitor is a first-class object in Snowflake, consisting of the
following properties:

### Credit quota¶

Credit quota specifies the number of Snowflake credits allocated to the
monitor for the specified frequency interval. Any number can be specified.

In addition, Snowflake tracks the _used credits/quota_ within the specified
frequency interval by all warehouses assigned to the monitor. At the specified
interval, this number resets to `0`.

Credit quota accounts for credits consumed by both user-managed virtual
warehouses and virtual warehouses used by cloud services.

For example, your resource monitor limit is set at 1000 credits. If your
warehouse consumes 700 credits, and cloud services consume 300 credits within
a specified interval or date range, an alert will be triggered.

Note

Resource monitor limits do not take into account the daily 10% adjustment for
cloud services. Snowflake uses all credit consumption by the cloud services
layer to calculate whether a limit has been reached, even if that consumption
is never billed. For more information about how cloud services credits and
adjustments are calculated, see [Understanding billing for cloud services
usage](cost-understanding-compute.html#label-understanding-billing-for-cloud-
services-usage).

For instructions on how to view your cloud services credit usage, see
[Exploring compute cost](cost-exploring-compute).

### Monitor type¶

This property specifies whether the resource monitor is used to monitor your
account or a specific set of individual warehouses:

  * An _account monitor_ monitors the credit usage of all the warehouses in the account. An account can only have one account monitor.

  * A _warehouse monitor_ monitors the credit usage of the warehouses assigned to the resource monitor. An account can have multiple warehouse monitors.

A warehouse monitor can have one or more warehouses assigned to it, but each
warehouse can only be assigned to one resource monitor.

If this property is not set, the resource monitor doesn’t monitor any credit
usage. It simply remains dormant.

For more information, see Assignment of resource monitors.

### Schedule¶

The default schedule for a resource monitor specifies that it starts
monitoring credit usage immediately and the used credits reset to `0` at the
beginning of each calendar month (i.e. the start of the standard Snowflake
billing cycle).

However, you can optionally customize the schedule for a resource monitor
using the following properties:

Frequency:

    

The interval at which the used credits reset relative to the specified start
date.

Supported values:

  * Daily

  * Weekly

  * Monthly

  * Yearly

  * Never (used credits never reset; assigned warehouses continue using credits until the credit quota is reached)

Start:

    

Date and time (i.e. timestamp) when the resource monitor starts monitoring the
assigned warehouses.

Supported values:

  * Immediately (i.e. current timestamp)

  * Later (i.e. any future timestamp)

In addition, Snowflake uses this date to determine when to reset the used
credits, based on the specified frequency. Note, however, that regardless of
the time specified in the start date and time, resource monitors reset at
12:00 AM UTC. For example, if the start is 15-July-2019 (Monday) at 8:00 AM:

  * Frequency = Monthly: Used credits reset at 12:00 AM UTC on the 15th of each following month.

  * Frequency = Weekly: Used credits reset at 12:00 AM UTC on each following Monday.

Note that, if you specify the last day of a month as the start date, Snowflake
resets the used credits on the last day of all following months, regardless of
the number of days in the month. For example, if you set the start date to
January 31, Snowflake subsequently resets the used credits for the resource
monitor on February 28 (or February 29 in a leap year), March 31, April 30,
and so on.

End:

    

Date and time (i.e. timestamp) when Snowflake suspends the warehouses
associated with the resource monitor, regardless of whether the used credits
reached any of the thresholds defined for the resource monitor’s actions (see
the next section in this topic).

Supported values: Any future timestamp.

Note that this property is not commonly used.

Important

If you choose to customize the schedule for a resource monitor, the frequency
is relative to the specified start date, which is different than the default
schedule.

Also, if you specify a frequency, you must also specify a start date and time,
and vice versa (i.e. you cannot set one without setting the other).

### Actions¶

Also referred to as _triggers_ , each action specifies a threshold, as a
percentage of the credit quota for the resource monitor, and the action to
perform when the threshold is reached within the specified interval. Note that
actions support thresholds greater than `100`.

Resource monitors support the following actions:

Notify & Suspend:

    

Send a notification and suspend all assigned warehouses after all statements
being executed by the warehouse(s) have completed.

Notify & Suspend Immediately:

    

Send a notification and suspend all assigned warehouses immediately, which
cancels any statements being executed by the warehouses at the time.

Notify:

    

Perform no action on warehouses, but send a notification.

Notifications are sent to all account administrators with notifications
enabled. Email notifications for resource monitors that monitor warehouses are
also sent to any non-administrator user that is enabled to receive those
notifications.

Note

Non-administrator users can only receive email notifications for _warehouse_
monitors.

Each resource monitor can have the following actions:

  * One **Suspend** action.

  * One **Suspend Immediate** action.

  * Up to five **Notify** actions.

Note

A resource monitor must have at least one action defined; if no actions have
been defined, nothing happens when the used credits reach the threshold.

## Assignment of resource monitors¶

A single monitor can be set at the account level to control credit usage for
all warehouses in your account.

In addition, a one or more warehouses can be assigned to a resource monitor,
thereby controlling the credit usage for each assigned warehouse. Note,
however, that a warehouse can be assigned to only a single resource monitor
below the account level.

The following diagram illustrates a scenario in which one resource monitor is
set at the account level and individual warehouses are assigned to two other
resource monitors:

![Warehouse and resource monitor relationships](../_images/resource-
monitor.png)

Based on this diagram:

  * The credit quota for the entire account is 5000 for the interval (month, week, etc.), as controlled by Resource Monitor 1; if this quota is reached within the interval, the actions defined for the resource monitor (**Suspend** , **Suspend Immediate** , etc.) are enforced for all five warehouses.

  * Warehouse 3 can consume a maximum of 1000 credits within the interval.

  * Warehouse 4 and 5 can consume a maximum combined total of 2500 credits within the interval.

Note that the actual credits consumed by Warehouses 3, 4, and 5 may be less
than their quotas if the quota for the account is reached first.

Important

  * An account-level resource monitor does not override resource monitor assignment for individual warehouses. If either the account resource monitor or the warehouse resource monitor reaches its defined threshold and a suspend action has been defined, the warehouse is suspended.

  * An account-level resource monitor does not control credit usage by the Snowflake-provided compute resources for serverless features (for example, Snowpipe, automatic reclustering, and materialized views).

  * A warehouse-level resource monitor can monitor, but cannot suspend, credit usage by cloud services. After a virtual warehouse is suspended, subsequent queries run against that warehouse can still result in additional cloud services costs. For more information about credit usage for cloud services, see [Cloud service credit usage](cost-understanding-compute.html#label-cloud-services-credit-usage).

## Warehouse suspension and resumption¶

The used credits for a resource monitor reflect the sum of credits consumed by
all assigned warehouses within the specified interval, along with the cloud
services used to support those warehouses during the same interval. If a
monitor has a **Suspend** or **Suspend Immediately** action defined and its
used credits reach the threshold for the action, any warehouses assigned to
the monitor are suspended and cannot be resumed until one of the following
conditions is met:

  * The next interval, if any, starts, as dictated by the start date for the monitor.

  * The credit quota for the monitor is increased.

  * The credit threshold for the suspend action is increased.

  * The warehouses are no longer assigned to the monitor.

  * The monitor is dropped.

Tip

Resource monitors are not intended for strictly controlling consumption on an
hourly basis; they are intended for tracking and controlling credit
consumption per interval (day, week, month, etc.). Also, they are not intended
for setting precise limits on credit usage (i.e. down to the level of
individual credits). For example, when credit quota thresholds are reached for
a resource monitor, the assigned warehouses may take some time to suspend,
even when the action is **Suspend Immediate** , thereby consuming additional
credits.

If you wish to strictly enforce your quotas, we recommend the following:

  * Utilize buffers in the quota thresholds for actions (e.g. set a threshold to 90% instead of 100%).

This will help ensure that your credit usage doesn’t exceed the quota.

  * To more strictly control credit usage for individual warehouses, assign only a single warehouse to each resource monitor.

When multiple warehouses are assigned to the same resource monitor, they share
the same quota thresholds, which may result in credit usage for one warehouse
impacting the other assigned warehouses.

## Resource monitor notifications¶

When a resource monitor reaches the threshold for an action, it generates a
notification similar to the following notification:

    
    
    Resource Monitor MY_ACCOUNT_MONITOR has reached 50% of its MONTHLY
    quota of 500 credits which has triggered a <action> action.
    

The `<action>` is one of the following actions:

  * NOTIFY

  * SUSPEND

  * SUSPEND_IMMEDIATE

Notification behavior depends on the type of resource monitor and whether or
not notifications are enabled for an individual user. Notifications are sent
as follows:

  * For _warehouse_ monitors, a notification is sent to the following users:

    * All account administrators who have enabled resource monitor notifications.

    * Non-administrator users in the notification list for the resource monitor.

  * For _account_ monitors, a notification is sent to the following users:

    * The account administrator with the OWNERSHIP privilege on the resource monitor if they have enabled notifications.

    * All account administrators who have enabled notifications using Classic Console.

Note

A non-administrator user can’t be added to the notification list for an
_account_ monitor.

Important

Resource monitor notifications can be sent by email or in the Classic Console,
but are disabled by default. You must set up notifications before they are
sent. Users that do not have the ACCOUNTADMIN role can only be sent email
notifications.

To enable notifications, see Enabling receipt of notifications.

## DDL for resource monitors¶

Snowflake provides the following DDL commands for creating and using/managing
resource monitors:

  * [CREATE RESOURCE MONITOR](../sql-reference/sql/create-resource-monitor)

  * [ALTER RESOURCE MONITOR](../sql-reference/sql/alter-resource-monitor)

  * [SHOW RESOURCE MONITORS](../sql-reference/sql/show-resource-monitors)

  * [DROP RESOURCE MONITOR](../sql-reference/sql/drop-resource-monitor)

In addition, the following DDL commands can be used to assign a resource
monitor to a warehouse and determine whether a warehouse is assigned to a
monitor:

  * [CREATE WAREHOUSE](../sql-reference/sql/create-warehouse) or [ALTER WAREHOUSE](../sql-reference/sql/alter-warehouse)

  * [SHOW WAREHOUSES](../sql-reference/sql/show-warehouses)

## Access control privileges for resource monitors¶

By default, resource monitors can only be created by account administrators
and, therefore, can only be viewed and maintained by them.

However, roles that have been granted the following privileges on specific
resource monitors can view and modify the resource monitor as needed using
SQL:

  * MONITOR

  * MODIFY

For more information, see [Access control privileges](security-access-control-
privileges) and [GRANT <privileges>](../sql-reference/sql/grant-privilege).

Note that only account administrators can view and manage resource monitors
via the Classic Console.

## Enabling receipt of notifications¶

Before you can receive any notifications from resource monitors, you must
enable notifications in the web interface and verify your email.

Snowsight:

    

To enable notifications, follow these steps:

  1. Verify your email address if you haven’t already done so. For instructions on how to verify your email address, see [Verify your email address](ui-snowsight-profile.html#label-snowsight-verify-email-address).

  2. Select your username, then select Profile

  3. For Notifications, select Enable notifications from resource monitors.

Note

     * If you haven’t verified your email address, the Notifications option isn’t available until you verify your email.

     * In Notifications, the Enable notifications from resource monitors option is only available to users with the ACCOUNTADMIN role in the following cases:

       * If there is a resource monitor assigned to the account and the account administrator has the OWNERSHIP privilege on the account monitor.

       * If there are warehouse monitors in the account. All account administrators can receive notifications for warehouse monitors.

Classic Console:

    

To enable notifications, follow these steps:

  1. Verify your email address if you haven’t already done so. For instructions on how to verify your email address, see [Verifying Your Email Address in the Classic Console](ui-preferences.html#label-classic-verify-email-address).

  2. Select the drop-down menu next to your name in the upper-right corner, and then select Preferences » Notifications.

  3. Select one of the options.

Note

All account administrators who have enabled receipt of notifications using
Classic Console receive notifications for account and warehouse monitors.

## Creating resource monitors¶

Resource monitors can be created through either the web interface or SQL;
however, only account administrators (i.e. users with the ACCOUNTADMIN role)
can create resource monitors.

Important

You must assign at least one warehouse to a resource monitor or set the
monitor at the account level for it to begin monitoring/tracking credit usage:

  * In the web interface, you are required to do this at creation time.

  * In SQL, you must create the resource monitor first, then assign one or more warehouses to it by executing [ALTER WAREHOUSE](../sql-reference/sql/alter-warehouse) as a separate, additional step.

Also, to receive notifications when resource monitor actions are triggered,
you must enable notifications.

### Creating a resource monitor with a default schedule¶

You can create a resource monitor that uses the default schedule (that is,
starts monitoring immediately and resets on the first day of each calendar
month) using the web interface or SQL.

Note

Only users with the ACCOUNTADMIN role can create resource monitors.

Snowsight:

    

  1. Sign in to Snowsight and navigate to Admin » Cost Management.

  2. Select Resource Monitors, then select \+ Resource Monitor.

  3. For Name, enter a name for the resource monitor.

  4. For Credit Quota, enter the number of credits for each specified interval.

  5. Select the Monitor Type. Choose Account to create an account monitor or choose Warehouse to select the warehouses to monitor.

  6. For Actions, choose which notifications to enable by entering a threshold next to the option. You must select at least one option.

Select Add to create additional notifications. You can specify up to five
notify actions.

Classic Console:

    

  1. Select Account [![Account tab](../_images/ui-navigation-account-icon.svg)](../_images/ui-navigation-account-icon.svg) » Resource Monitors » Create Resource Monitor.

  2. For Name, enter a name.

  3. For Credit Quota, enter the number of credits for each specified interval.

  4. Select the Monitor Level. Choose Account to create an account monitor or choose Warehouse to select the warehouses to monitor.

  5. Select the Actions and Notifications to enable by entering a threshold next to the option. You must select at least one option.

Select +Add more notification thresholds to create additional notifications.
You can specify up to five notify actions.

SQL:

    

In SQL, this task is performed in two steps:

  1. Execute a [CREATE RESOURCE MONITOR](../sql-reference/sql/create-resource-monitor) command, but do not specify any scheduling properties.

  2. Execute an [ALTER WAREHOUSE](../sql-reference/sql/alter-warehouse) statement to assign warehouses to the resource monitor or an [ALTER ACCOUNT](../sql-reference/sql/alter-account) statement to set the resource monitor for the account.

For example:

  * To create a monitor that starts monitoring immediately, resets at the beginning of each month, and suspends the assigned warehouse when the used credits reach 100% of the credit quota:

> >     USE ROLE ACCOUNTADMIN;
>  
>     CREATE OR REPLACE RESOURCE MONITOR limit1 WITH CREDIT_QUOTA=1000
>       TRIGGERS ON 100 PERCENT DO SUSPEND;
>  
>     ALTER WAREHOUSE wh1 SET RESOURCE_MONITOR = limit1;
>  
>
> Copy

The SUSPEND action waits for currently executing queries to finish before
suspending the warehouse. A query might start before the threshold is reached
and complete after the SUSPEND action is triggered. In this case, the
warehouse continues to consume credits even after the quota is reached.

  * To create a similar monitor that suspends at 90% and suspends immediately at 100% after the quota has been reached:

> >     USE ROLE ACCOUNTADMIN;
>  
>     CREATE OR REPLACE RESOURCE MONITOR limit1 WITH CREDIT_QUOTA=1000
>       TRIGGERS ON 90 PERCENT DO SUSPEND
>                ON 100 PERCENT DO SUSPEND_IMMEDIATE;
>  
>     ALTER WAREHOUSE wh1 SET RESOURCE_MONITOR = limit1;
>  
>
> Copy

In this example, a notification is sent and the assigned warehouses are
suspended when 90% of the credit quota is reached. Currently executing queries
complete, but the resource monitor prevents the warehouses from executing any
new queries. If the assigned warehouses reach 100% of the credit quota, a
notification is sent and the warehouses are suspended immediately, canceling
all currently executing queries. This prevents all warehouses in the account
from consuming credits.

  * To create a monitor that is similar to the first example, but lets the assigned warehouse exceed the quota by 10% and also includes two notification actions to alert account administrators as the used credits reach the halfway and three-quarters points for the quota:

> >     USE ROLE ACCOUNTADMIN;
>  
>     CREATE OR REPLACE RESOURCE MONITOR limit1 WITH CREDIT_QUOTA=1000
>        TRIGGERS ON 50 PERCENT DO NOTIFY
>                 ON 75 PERCENT DO NOTIFY
>                 ON 100 PERCENT DO SUSPEND
>                 ON 110 PERCENT DO SUSPEND_IMMEDIATE;
>  
>     ALTER WAREHOUSE wh1 SET RESOURCE_MONITOR = limit1;
>  
>
> Copy

In this example:

    * When 50% and 75% usage is reached, an alert notification is sent to all account administrators who have enabled notifications, but no other actions are performed.

    * When 100% usage is reached, the assigned warehouse is suspended.

    * If the warehouse is still running when 110% usage is reached, it is suspended immediately.

### Creating a resource monitor with a custom schedule¶

You can create a resource monitor that uses a schedule other than the default
using the web interface or SQL.

Note

Only users with the ACCOUNTADMIN role can create resource monitors.

Complete the following steps to create a resource monitor with a custom
schedule:

Snowsight:

    

  1. Sign in to Snowsight and navigate to Admin » Cost Management.

  2. Select Resource Monitors, then select \+ Resource Monitor.

  3. For Name, enter a name for the resource monitor.

  4. For Credit Quota, enter the number of credits for each specified interval.

  5. Select the Monitor Type. Choose Account to create an account monitor or choose Warehouse to select the warehouses to monitor.

  6. Select Schedule » Customize to set a custom schedule for the specified interval. You can skip this step to use the default schedule.

You can set a custom start and end date using Custom Start Date and Custom End
Date, or specify a date range by using the Range tab.

Note

If you choose to end monitoring at a specified date and time, all assigned
warehouses are suspended on that date and time even if the credit quota has
not been reached. A notification is sent when this occurs that states the
resource monitor has reached a percentage of its quota and has triggered a
suspend immediate action. The percentage of the quota reflects the number of
used credits in the current interval up to the end date and might not be a
threshold you specified.

You can also customize the specified interval for monitoring. Select Resets
and you can select from the following periodic intervals at which to reset the
credit quota:

     * Monthly

     * Daily

     * Weekly

     * Yearly

     * Never

  7. For Actions, choose which notifications to enable by entering a threshold next to the option. You must select at least one option.

Select Add to create additional notifications. You can specify up to five
notify actions.

Classic Console:

    

  1. Select Account [![Account tab](../_images/ui-navigation-account-icon.svg)](../_images/ui-navigation-account-icon.svg) » Resource Monitors » Create Resource Monitor.

  2. For Name, enter a name for the resource monitor.

  3. For Credit Quota, enter the number of credits for each specified interval.

  4. Select the Monitor Level. Choose Account to create an account monitor or choose Warehouse to select the warehouses to monitor.

  5. For Schedule, click the Customize link and specify one or more of the following properties, as desired:

     * Start the monitor immediately or at a later date and time.

     * Reset used credits based on the specified frequency.

     * End monitoring at a specified date and time or never.

Note

If you choose to end monitoring at a specified date and time, all assigned
warehouses are suspended at that date and time even if the credit quota has
not been reached. A notification is sent when this occurs that states the
resource monitor has reached a percentage of its quota and has triggered a
suspend immediate action. The percentage of the quota reflects the number of
used credits in the current interval up to the end date and might not be a
threshold you specified.

  6. For Actions and Notifications, enable a given action or notification by entering a threshold next to the option. You must select at least one option.

Select +Add more notification thresholds to create additional notifications.
You can specify up to five notify actions.

SQL:

    

Execute a [CREATE RESOURCE MONITOR](../sql-reference/sql/create-resource-
monitor) command, with one or more of the following scheduling properties:

  * FREQUENCY

  * START_TIMESTAMP

  * END_TIMESTAMP

For example:

  * To create an account-level resource monitor that starts immediately (based on the current timestamp), resets monthly on the same day, has no end date or time, and suspends the assigned warehouse when the used credits reach 100% of the quota:

> >     USE ROLE ACCOUNTADMIN;
>  
>     CREATE OR REPLACE RESOURCE MONITOR limit1 WITH CREDIT_QUOTA=1000
>         FREQUENCY = MONTHLY
>         START_TIMESTAMP = IMMEDIATELY
>         TRIGGERS ON 100 PERCENT DO SUSPEND;
>  
>     ALTER WAREHOUSE wh1 SET RESOURCE_MONITOR = limit1;
>  
>
> Copy

  * To create a resource monitor that starts at a specific date and time in the future, resets weekly on the same day, has no end date or time, and performs two different suspend actions at different thresholds on two assigned warehouses:

> >     USE ROLE ACCOUNTADMIN;
>  
>     CREATE OR REPLACE RESOURCE MONITOR limit1 WITH CREDIT_QUOTA=2000
>         FREQUENCY = WEEKLY
>         START_TIMESTAMP = '2019-03-04 00:00 PST'
>         TRIGGERS ON 80 PERCENT DO SUSPEND
>                  ON 100 PERCENT DO SUSPEND_IMMEDIATE;
>  
>     ALTER WAREHOUSE wh1 SET RESOURCE_MONITOR = limit1;
>  
>     ALTER WAREHOUSE wh2 SET RESOURCE_MONITOR = limit1;
>  
>
> Copy

Note

You cannot change the customized schedule for a resource monitor back to the
default. You must drop the monitor and create a new monitor.

## Modifying a resource monitor¶

You can modify the following properties for an existing resource monitor:

  * Increase or decrease the credit quota for the monitor.

  * Customize the schedule (frequency, start timestamp, and end timestamp) for the monitor.

  * Add or remove actions, or modify the threshold percentages for existing actions.

  * If the monitor is monitoring your account, convert it to monitor individual warehouses.

  * If the monitor is monitoring individual warehouses:

    * Add or remove warehouses from the list.

    * Convert it to monitor your account.

Note

Changing any of these properties does not affect the used credits to-date for
the monitor. All changes only affect used credits after the changes are saved.

Resource monitors can be modified through the web interface or SQL.

Note

The following privileges are required to modify the properties of a resource
monitor:

  * To modify the credit quota, schedule, or actions for a resource monitor, a user must use a role with the MODIFY privilege on the resource monitor.

  * To modify the monitor type for a resource monitor from warehouse to account or vice versa, a user must use the ACCOUNTADMIN role.

  * To modify the list of warehouses for a warehouse-level resource monitor, a user must use the ACCOUNTADMIN role.

Snowsight:

    

  1. Sign in to Snowsight and navigate to Admin » Cost Management.

  2. Select Resource Monitors, then select a resource monitor.

  3. Select the More menu (…) in top right corner. Select Edit.

Classic Console:

    

  1. Select Account [![Account tab](../_images/ui-navigation-account-icon.svg)](../_images/ui-navigation-account-icon.svg) » Resource Monitors.

  2. Select a resource monitor.

  3. Select Edit.

SQL:

    

  * To change the quota, customize the schedule, or add/remove/modify actions, execute an [ALTER RESOURCE MONITOR](../sql-reference/sql/alter-resource-monitor) statement.

For example, to increase the credit quota for resource monitor `limit1` to
`3000`, execute the following statement:

> >     ALTER RESOURCE MONITOR limit1 SET CREDIT_QUOTA=3000;
>  
>
> Copy

For more examples, see [Examples](../sql-reference/sql/alter-resource-
monitor.html#label-alter-resource-monitor-examples).

  * To change the monitor type, execute an [ALTER WAREHOUSE](../sql-reference/sql/alter-warehouse) or [ALTER ACCOUNT](../sql-reference/sql/alter-account) statement.

For example, to change resource monitor `my_rm` which currently monitors
warehouses to monitor the account `my_account`, execute the following steps:

    1. Find all the warehouses the resource monitor `my_rm` is monitoring. Check the `resource_monitor` column for `my_rm`:
        
                SHOW WAREHOUSES;
        

Copy

Returns the following results:

        
                +--------+-----------+----------+---------+---------+--------+------------+------------+--------------+-------------+-----------+--------------+-----------+-------+-------------------------------+-------------------------------+-------------------------------+--------------+---------+------------------+---------+----------+--------+-----------+------------+--------+-----------------+
        | name   | state     | type     | size    | running | queued | is_default | is_current | auto_suspend | auto_resume | available | provisioning | quiescing | other | created_on                    | resumed_on                    | updated_on                    | owner        | comment | resource_monitor | actives | pendings | failed | suspended | uuid       | budget | owner_role_type |
        |--------+-----------+----------+---------+---------+--------+------------+------------+--------------+-------------+-----------+--------------+-----------+-------+-------------------------------+-------------------------------+-------------------------------+--------------+---------+------------------+---------+----------+--------+-----------+------------+--------+-----------------|
        | MY_WH1 | STARTED   | STANDARD | X-Small |       0 |      0 | N          | N          |          600 | true        |           |              |           |       | 2024-01-17 14:37:36.223 -0800 | 2024-01-17 14:37:36.325 -0800 | 2024-01-17 14:47:49.854 -0800 | MY_ROLE      |         | null             |       0 |        0 |      0 |         1 | 1222706972 | NULL   | ROLE            |
        | MY_WH2 | SUSPENDED | STANDARD | X-Small |       0 |      0 | N          | Y          |          600 | true        |           |              |           |       | 2023-12-20 13:50:50.972 -0800 | 2024-01-17 14:28:39.170 -0800 | 2024-01-17 14:37:57.560 -0800 | ACCOUNTADMIN |         | MY_RM            |       0 |        0 |      0 |         1 | 1222706948 | NULL   | ROLE            |
        | MY_WH3 | SUSPENDED | STANDARD | Small   |       0 |      0 | N          | N          |          600 | true        |           |              |           |       | 2024-01-17 14:26:26.911 -0800 | 2024-01-17 14:33:39.260 -0800 | 2024-01-17 14:38:31.192 -0800 | ACCOUNTADMIN |         | MY_RM            |       0 |        0 |      0 |         2 | 1222706960 | NULL   | ROLE            |
        +--------+-----------+----------+---------+---------+--------+------------+------------+--------------+-------------+-----------+--------------+-----------+-------+-------------------------------+-------------------------------+-------------------------------+--------------+---------+------------------+---------+----------+--------+-----------+------------+--------+-----------------+
        

Resource monitor `my_rm` is monitoring two warehouses `my_wh2` and `my_wh3`.

    2. Remove the resource monitor for both warehouses by executing the following statements:
        
                ALTER WAREHOUSE my_wh2 UNSET RESOURCE_MONITOR;
        
        ALTER WAREHOUSE my_wh3 UNSET RESOURCE_MONITOR;
        

Copy

    3. Change the resource monitor to monitor the account by executing the following statement:
        
                ALTER ACCOUNT my_account SET RESOURCE_MONITOR = my_rm;
        

Copy

Note

If a resource monitor has a customized schedule, you cannot change the
schedule back to the default. You must drop the monitor and create a new
monitor.

## Send resource monitor notifications to non-administrator users¶

Non-administrator users can only receive email notifications for warehouse
monitors. Each non-administrator user must have a verified email address. You
can add up to five non-administrator users to a warehouse monitor using the
CREATE RESOURCE MONITOR or ALTER RESOURCE MONITOR command.

For example, to add users `user1` and `user2` to the warehouse monitor
`my_warehouse_rm`, execute the following statement:

    
    
    ALTER RESOURCE MONITOR my_warehouse_rm
      SET NOTIFY_USERS = (USER1, USER2);
    

Copy

Note

If any user in the notification list does not have a verified email, the
statement fails.

For more information, see the [NOTIFY_USERS parameter](../sql-
reference/sql/alter-resource-monitor.html#label-alter-resource-monitor-notify-
users) and [Usage notes](../sql-reference/sql/alter-resource-
monitor.html#label-alter-resource-monitor-usage-notes) in the [ALTER RESOURCE
MONITOR](../sql-reference/sql/alter-resource-monitor) topic.

To add non-administrator users to the notification list for a resource monitor
when you create a resource monitor using SQL, see [CREATE RESOURCE
MONITOR](../sql-reference/sql/create-resource-monitor).

## Setting a resource monitor for your account¶

A resource monitor can be set for your account through the web interface or
SQL.

Note

Only users with the ACCOUNTADMIN role can set a resource monitor to monitor
the account.

Snowsight:

    

You can set the monitor type to account when you create a resource monitor.
For more information, see Creating resource monitors.

Classic Console:

    

You can set the monitor type to Account when you create or modify a resource
monitor:

  * For more information about creating a resource monitor, see Creating resource monitors.

  * For more information about modifying a resource monitor, see Modifying a resource monitor.

SQL:

    

In SQL, this task is performed in two steps:

  1. Use the [CREATE RESOURCE MONITOR](../sql-reference/sql/create-resource-monitor) command to create the resource monitor (if it doesn’t already exist).

If the resource monitor does exist, to change a warehouse level resource
monitor to monitor an account, see the example in the Modifying a Resource
Monitor section.

  2. Use the [ALTER ACCOUNT](../sql-reference/sql/alter-account) command to set the resource monitor you created as the monitor for your account.

For example, to set the account resource monitor to `my_account_rm`, execute
the following statements:

> >     USE ROLE ACCOUNTADMIN;
>  
>     CREATE RESOURCE MONITOR my_account_rm WITH CREDIT_QUOTA=10000
>       TRIGGERS ON 100 PERCENT DO SUSPEND;
>  
>     ALTER ACCOUNT SET RESOURCE_MONITOR = my_account_rm;
>  
>
> Copy

To change the monitor type of an existing resource monitor from a warehouse
monitor to an account monitor, see the example in the Modifying a Resource
Monitor section.

To view whether a resource monitor is set for your account, use the web
interface or the [SHOW RESOURCE MONITORS](../sql-reference/sql/show-resource-
monitors) command. The `LEVEL` column for a resource monitor displays whether
it is set for your account or individual warehouses.

Important

  * An account-level resource monitor only controls the virtual warehouses explicitly created in your account; it does not control credit usage by the Snowflake-provided warehouses for serverless features (for example, [Snowpipe](data-load-snowpipe-intro), [Automatic Clustering](tables-auto-reclustering), and [materialized views](views-materialized)).

  * A warehouse-level resource monitor can monitor, but cannot suspend, credit usage by cloud services. The monitor can only suspend the user-managed virtual warehouses created in your account. After a user-managed virtual warehouse is suspended, subsequent queries run against that warehouse can still result in additional cloud services costs. For more information about credit usage for cloud services, see [Cloud service credit usage](cost-understanding-compute.html#label-cloud-services-credit-usage).

## Assigning warehouses to a resource monitor¶

Warehouses can be assigned to an existing resource monitor through the web
interface or SQL.

Note

Only users with the ACCOUNTADMIN role can assign warehouses to resource
monitors.

Snowsight:

    

  1. Sign in to Snowsight and navigate to Admin » Cost Management.

  2. Select Resource Monitors, then select a resource monitor.

  3. Select the More menu (…) in top right corner. Select Edit.

  4. If Monitor Type is Account, select Warehouse.

  5. Select Warehouse to choose the warehouses to monitor.

Classic Console:

    

  1. Select Account [![Account tab](../_images/ui-navigation-account-icon.svg)](../_images/ui-navigation-account-icon.svg) » Resource Monitors.

  2. Select a resource monitor.

  3. Select Edit.

  4. If the monitor does not already have any warehouses assigned, select Monitor Level, then select Warehouse.

  5. Select Warehouse and choose the warehouses to monitor.

SQL:

    

Use the [ALTER WAREHOUSE](../sql-reference/sql/alter-warehouse) command to
assign a warehouse to a resource monitor.

For example, to monitor warehouse `my_wh` with the resource monitor `my_rm`,
execute the following statement:

>
>     ALTER WAREHOUSE my_wh SET RESOURCE_MONITOR = my_rm;
>  
>
> Copy

## Viewing resource monitors¶

Resource monitors can be viewed through the web interface or SQL.

Snowsight:

    

  1. Sign in to Snowsight and navigate to Admin » Cost Management.

  2. Select Resource Monitors to see a list of resource monitors for which your role has been granted the MODIFY or MONITOR privilege. Account administrator users can see all resource monitors.

  3. Select a resource monitor to view detailed information about resource monitor settings, current credit usage, and a list of roles with privileges on the resource monitor.

Classic Console:

    

Note

Only users with the ACCOUNTADMIN role can view resource monitors using Classic
Console.

  1. Select Account [![Account tab](../_images/ui-navigation-account-icon.svg)](../_images/ui-navigation-account-icon.svg) » Resource Monitors.

SQL:

    

Using the ACCOUNTADMIN role or a role that has been granted the MONITOR or
MODIFY privilege on the resource monitor, execute a [SHOW RESOURCE
MONITORS](../sql-reference/sql/show-resource-monitors) statement.

In addition, using any role, you can execute a [SHOW WAREHOUSES](../sql-
reference/sql/show-warehouses) statement to view the warehouses owned by the
role (or for which the role has been granted USAGE privilege). The output
includes the resource monitor, if any, to which the warehouse is assigned.

Note

For [provider accounts](data-sharing-gs) that have created reader accounts,
Snowflake provides an additional view, [RESOURCE_MONITORS](../sql-
reference/account-usage/resource_monitors). This view can be used for querying
resource monitor usage in the provider’s reader accounts. For more
information, see [Account Usage](../sql-reference/account-usage).

## Replicating resource monitors¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Business Critical
Feature](intro-editions)

Resource monitor replication requires Business Critical (or higher). To
inquire about upgrading, please contact [Snowflake
Support](https://docs.snowflake.com/user-guide/contacting-support).

Resource monitors can be replicated from a source account to target accounts
using a [replication or failover group](account-replication-intro.html#label-
replication-and-failover-groups). For more information, see [Resource monitor
replication](account-replication-intro.html#label-resource-monitor-
replication).

