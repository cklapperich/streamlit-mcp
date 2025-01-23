# Organization accounts¶  
  
[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Preview Feature](../release-
notes/preview-features) — Open

Available to all non-government accounts that are Enterprise Edition (or
higher).

To inquire about upgrading, please contact [Snowflake
Support](https://docs.snowflake.com/user-guide/contacting-support).

An _organization account_ is a special type of account that organization
administrators use to perform tasks that affect the entire organization. For
example, administrators use the organization account to do the following:

  * View organization-level data collected from all accounts in the organization, including the query history from each account.

  * Enable Snowflake Marketplace terms for the entire organization.

  * Manage the lifecycle of accounts in an organization, including creating and deleting accounts.

  * Enable replication for an account.

Before this preview, administrators needed to perform these organization-level
tasks using an account that had the [ORGADMIN role enabled](organizations-
gs.html#label-enabling-orgadmin-role-for-account). These _ORGADMIN-enabled
accounts_ are different from the organization account. Unlike the classic
approach where an organization might have multiple ORGADMIN-enabled accounts,
there is only one organization account.

During the preview of organization accounts, organization administrators can
still use an [ORGADMIN-enabled](organizations-gs.html#label-enabling-orgadmin-
role-for-account) account to manage the lifecycle of accounts (for example,
creating and deleting accounts). After organization accounts become generally
available, there will be a transition period, after which administrators will
use the organization account for all organization-level tasks.

Note

Though, in most cases, there are not any limitations on what actions can be
performed in an organization account, it is intended to be used primarily for
organization-level tasks, and not for analytics or other workloads.

## About administrator roles and assignable privileges¶

Organization administrators use the GLOBALORGADMIN role in the organization
account to perform all organization-level tasks, including administration of
the organization account itself. The GLOBALORGADMIN role has all of the
privileges of the ORGADMIN role along with the privileges that are associated
with the ACCOUNTADMIN role in a regular account.

The GLOBALORGADMIN role can assign privileges to other roles to let other
users perform organization-level tasks. In the organization account, the
GLOBALORGADMIN role can assign the following privileges:

  * APPLY TAG

  * MANAGE ACCOUNTS

  * MANAGE LISTING AUTO FULFILLMENT

  * MANAGE ORGANIZATION CONTACTS

  * MANAGE ORGANIZATION TERMS

  * PURCHASE DATA EXCHANGE LISTING

These privileges are set on the account level. For example, to assign the
MANAGE ACCOUNTS privilege to the role `custom_role`, execute the following:

    
    
    USE ROLE GLOBALORGADMIN;
    
    GRANT MANAGE ACCOUNTS ON ACCOUNT TO custom_role;
    

Copy

For more information about these privileges, see [Access control
privileges](security-access-control-privileges).

## Create the organization account¶

Note

Creating the organization account results in the ORGANIZATION_USAGE schema
being populated with data, which incurs additional costs for your
organization.

To create the organization account:

  1. Choose an existing account from which you will create the organization account. This existing account must have the [ORGADMIN role enabled](organizations-gs.html#label-enabling-orgadmin-role-for-account).

  2. Sign in to the account you are using to create the organization account.

  3. Switch to the ORGADMIN role. For example:
    
        USE ROLE ORGADMIN;
    

Copy

  4. Execute the [CREATE ORGANIZATION ACCOUNT](../sql-reference/sql/create-organization-account) command. For example:
    
        CREATE ORGANIZATION ACCOUNT myorgaccount
        ADMIN_NAME = admin
        ADMIN_PASSWORD = 'TestPassword1'
        EMAIL = 'myemail@myorg.org'
        MUST_CHANGE_PASSWORD = true
        EDITION = enterprise;
    

Copy

Note

Snowflake does not support custom account locators for organization accounts.
For alternatives, contact your Snowflake representative.

## Delete the organization account¶

If you need to delete the organization account, contact [Snowflake
Support](https://docs.snowflake.com/user-guide/contacting-support).

## Move the organization account to a different region¶

You can move an organization account between regions as long as those regions
are in either the PUBLIC region group or a VPS region group.

Snowflake uses replication groups to move objects from the organization
account in the source region to the organization account in the new region. As
a result, only objects that can be replicated are moved with the organization
account. For a list of objects that can be moved with the organization
account, see [Replicated objects](account-replication-intro.html#label-
replicated-objects).

Moving the organization account to a different region is a two-step process:

  1. Call the [SYSTEM$INITIATE_MOVE_ORGANIZATION_ACCOUNT](../sql-reference/functions/system_initiate_move_organization_account) function from the organization account to start the process of moving it. Snowflake begins replicating objects to the new region.

The function accepts a temporary account name, the new region, and a list of
objects to move as its arguments. For example:

    
        CALL SYSTEM$INITIATE_MOVE_ORGANIZATION_ACCOUNT(
      'MY_TEMP_NAME',
      'aws_us_west_2',
      'ALL');
    

Copy

  2. When you have verified that the data in the organization account has been successfully replicated in the new region, call the [SYSTEM$COMMIT_MOVE_ORGANIZATION_ACCOUNT](../sql-reference/functions/system_commit_move_organization_account) function to finalize the move, specifying a grace period after which the original organization account is deleted.

For example, the following call finalizes the move, and specifies that the
original organization account in the source region will be deleted after 14
days.

    
        CALL SYSTEM$COMMIT_MOVE_ORGANIZATION_ACCOUNT(14);
    

Copy

At any point, you can view the status of an attempt to move an organization
account by calling the [SYSTEM$SHOW_MOVE_ORGANIZATION_ACCOUNT_STATUS](../sql-
reference/functions/system_show_move_organization_account_status) function.

Note

When an organization account is moved, the views in the ORGANIZATION_USAGE
schema must be repopulated with data, a process that can take up to one week.

## Views in the ORGANIZATION_USAGE schema¶

Like regular accounts, the organization account has an ORGANIZATION_USAGE
schema in the shared SNOWFLAKE database that contains usage data.

Most views in the ORGANIZATION_USAGE schema correspond to a view in the
ACCOUNT_USAGE schema. For example, the ALERT_HISTORY view in both schemas
contains data about alerts. The view in the ORGANIZATION_USAGE schema
consolidates data from the corresponding account-level view of each account,
allowing you to query usage data for all accounts from one view.

The ORGANIZATION_USAGE schema in an organization account contains more views
than the ORGANIZATION_USAGE schema in a regular account, which allows you to
gain additional insights into aggregated account usage across accounts. For
example, the organization account allows you to use a single view to track
access history across the organization, something you cannot do in a regular
account. These additional views are considered premium views, and incur
additional costs.

Note

It can take two weeks from the time an organization account was created until
the ORGANIZATION_USAGE schema is fully populated with historical data from
accounts.

### Grant access to the Organization Usage views¶

By default, only users who have been granted the GLOBALORGADMIN role can
access the views in the ORGANIZATION_USAGE schema of an organization account.
To grant access to other users, the organization administrator can grant the
appropriate application role to an account role or user. In an organization
account, privileges to views are granted using application roles, not database
roles.

Users who have been granted the ORG_USAGE_ADMIN application role can access
all views in the ORGANIZATION_USAGE schema of the organization account. The
following example lets user `joe` access all views in the schema:

    
    
    USE ROLE GLOBALORGADMIN;
    
    GRANT APPLICATION ROLE ORG_USAGE_ADMIN TO ROLE custom_role;
    
    GRANT ROLE custom_role TO USER joe;
    

Copy

The organization administrator can also grant access on a more granular level.
For example, the ORGANIZATION_OBJECT_VIEWER application role grants access to
the DATABASES view, but does not grant access to the TASK_HISTORY view. For a
list of the application role required to access a specific view, see
ORGANIZATION_USAGE Views.

### Costs associated with the ORGANIZATION_USAGE schema¶

The premium views in the ORGANIZATION_USAGE schema of the organization account
(that is, views that don’t exist in regular accounts) incur the following
costs:

  * Compute costs associated with the serverless tasks that populate the views.

  * Storage costs associated with storing the data in the views.

Note

If you want to avoid these costs by removing data from the ORGANIZATION_USAGE
schema, contact [Snowflake Support](https://docs.snowflake.com/user-
guide/contacting-support).

You can use the following queries to return the historical costs associated
with the ORGANIZATION_USAGE schema in the organization account.

Compute costs

    

If you have access to the USAGE_IN_CURRENCY_DAILY view in the
ORGANIZATION_USAGE schema, you can execute the following query to determine
the cost of populating the views. You must execute the query in the
organization account.

    
    
    SELECT * FROM snowflake.organization_usage.usage_in_currency_daily
      WHERE usage_type = 'organization usage';
    

Copy

Storage costs

    

If you have access to the TABLE_STORAGE_METRICS view in the ACCOUNT_USAGE
schema, you can execute the following query to determine the approximate
amount of storage in TBs. You must execute the query in the organization
account.

    
    
    SELECT
      SUM(active_bytes + time_travel_bytes + failsafe_bytes + retained_for_clone_bytes) / pow(1000, 4)
        AS org_usage_approx_storage_tb
      FROM snowflake.account_usage.table_storage_metrics
      WHERE 1=1
        AND table_schema = 'ORGANIZATION_USAGE_LOCAL';
    

Copy

### Effect on views in the ACCOUNT_USAGE schema¶

Snowflake uses the hidden schema `snowflake.organization_usage_local` to store
internal objects used in conjunction with the ORGANIZATION_USAGE schema (for
example, tables, procedures, and tasks). These objects might be visible in the
ACCOUNT_USAGE views in the organization account. Because these objects are
internal, they might change without notice in the future.

### Differences between account-level and organization-level views¶

The only differences between a new view in the ORGANIZATION_USAGE schema and
the corresponding view in the ACCOUNT_USAGE schema are the following:

  * The addition of a few columns.

  * The latency of the view.

  * Whether older data is removed from the view.

#### New columns¶

The majority of the columns in ORGANIZATION_USAGE views are identical to the
columns in the corresponding ACCOUNT_USAGE views. The following columns have
been added to the organization-level views:

Column | Data type | Description | Views  
---|---|---|---  
ORGANIZATION_NAME | VARCHAR | Name of the organization. | All  
ACCOUNT_NAME | VARCHAR | User-defined identifier for an account. | All  
ACCOUNT_LOCATOR | VARCHAR | System-defined identifier for an account. | All  
PROVIDER_BASE_ACCESSED_OBJECTS | ARRAY | Specifies base data objects in the provider’s account that were accessed by a consumer query. | ACCESS_HISTORY  
PROVIDER_POLICIES_REFERENCED | ARRAY | If a consumer query accessed base objects that are protected by a policy (for example, a masking policy) in the provider’s account, the column lists the policy. | ACCESS_HISTORY  
  
For more information about the PROVIDER_BASE_ACCESSED_OBJECTS and
PROVIDER_POLICIES_REFERENCED columns, see [Organizational listing
governance](collaboration/listings/organizational/org-listing-governance).

#### Latency¶

It might take up to 24 hours for a view in the ORGANIZATION_USAGE schema to be
updated. This might differ from the latency of the corresponding view in the
ACCOUNT_USAGE schema.

#### Older data¶

Unlike account-level views, the organization-level views continue to add new
data without replacing older data. For example, the
ACCOUNT_USAGE.ALERT_HISTORY view never contains data older than 365 days
whereas the ORGANIZATION_USAGE.ALERT_HISTORY continues to add data without
removing older data, so it can contain data that is older than 365 days.

### ORGANIZATION_USAGE Views¶

The ORGANIZATION_USAGE schema in the organization account contains the
following views.

Granting the required application role to a user provides them access to the
view. For more information about granting these application roles, see Grant
access to the Organization Usage views.

View | Description | Required application role  
---|---|---  
[ACCESS_HISTORY view](../sql-reference/account-usage/access_history) [1] | Displays the access history for queries in the organization. | ORGANIZATION_GOVERNANCE_VIEWER  
[ACCOUNTS view](../sql-reference/organization-usage/accounts) | Displays the accounts in an organization. | ORGANIZATION_ACCOUNTS_VIEWER  
[ALERT_HISTORY view](../sql-reference/account-usage/alert_history) | Displays the history of alert usage. | ORGANIZATION_USAGE_VIEWER  
[AUTOMATIC_CLUSTERING_HISTORY view](../sql-reference/account-usage/automatic_clustering_history) | Displays the history of automatic clustering. | ORGANIZATION_USAGE_VIEWER  
[CLASSES view](../sql-reference/account-usage/classes) | Displays a row for each class in an organization. | ORGANIZATION_USAGE_VIEWER  
[CLASS_INSTANCES view](../sql-reference/account-usage/class_instances) | Displays a row for each instance of a class defined in an organization. | ORGANIZATION_USAGE_VIEWER  
[COLUMNS view](../sql-reference/account-usage/columns) | Displays a row for each column in the tables defined in an organization. | ORGANIZATION_OBJECT_VIEWER  
[COMPLETE_TASK_GRAPHS view](../sql-reference/account-usage/complete_task_graphs) | Displays the status of completed graph runs, such as runs that executed successfully, failed, or were cancelled. | ORGANIZATION_OBJECT_VIEWER  
[CONTRACT_ITEMS view](../sql-reference/organization-usage/contract_items) | Displays contract information for an organization. | ORGANIZATION_BILLING_VIEWER  
[COPY_HISTORY view](../sql-reference/account-usage/copy_history) | Displays load activity for both COPY INTO <table> statements and continuous data loading using Snowpipe. | ORGANIZATION_USAGE_VIEWER  
[DATABASE_STORAGE_USAGE_HISTORY view](../sql-reference/account-usage/database_storage_usage_history) | Displays the average daily storage usage, in bytes, for databases in the . | ORGANIZATION_USAGE_VIEWER  
[DATABASES view](../sql-reference/account-usage/databases) | Displays a row for each database defined in an organization. | ORGANIZATION_OBJECT_VIEWER  
[DATA_TRANSFER_DAILY_HISTORY view](../sql-reference/organization-usage/data_transfer_daily_history) | Displays the daily total of data transferred from Snowflake tables into a different cloud storage provider’s network and/or geographical region. | ORGANIZATION_USAGE_VIEWER  
[DATA_TRANSFER_HISTORY view](../sql-reference/account-usage/data_transfer_history) | Displays the history of data transferred from Snowflake tables into a different cloud storage provider’s network and/or geographical region. | ORGANIZATION_USAGE_VIEWER  
[FILE_FORMATS view](../sql-reference/account-usage/file_formats) | Displays a row for each file format defined in an organization. | ORGANIZATION_OBJECT_VIEWER  
[FUNCTIONS view](../sql-reference/account-usage/functions) | Displays a row for each user-defined function (UDF) defined in an organization. | ORGANIZATION_OBJECT_VIEWER  
[GRANTS_TO_ROLES view](../sql-reference/account-usage/grants_to_roles) | Displays access control privileges that have been granted to a role. | ORGANIZATION_SECURITY_VIEWER  
[GRANTS_TO_USERS view](../sql-reference/account-usage/grants_to_users) | Displays the roles that have been granted to a user. | ORGANIZATION_SECURITY_VIEWER  
[LISTING_AUTO_FULFILLMENT_USAGE_HISTORY view](../sql-reference/organization-usage/listing_auto_fulfillment_usage_history) | Displays estimates that help determine the costs associated with Cross-Cloud Auto-Fulfillment. | ORGANIZATION_BILLING_VIEWER  
[LOAD_HISTORY view](../sql-reference/account-usage/load_history) | Displays the history of data loaded into tables using the COPY INTO <table> command. | ORGANIZATION_USAGE_VIEWER  
[LOCK_WAIT_HISTORY view](../sql-reference/account-usage/lock_wait_history) | Displays the history of transactions that wait on locks. | ORGANIZATION_USAGE_VIEWER  
[LOGIN_HISTORY view](../sql-reference/account-usage/login_history) | Displays login attempts by Snowflake users. | ORGANIZATION_SECURITY_VIEWER  
[MARKETPLACE_DISBURSEMENT_REPORT view](https://other-docs.snowflake.com/en/collaboration/views/marketplace-disbursement-report-org) | Displays the history of your earnings from paid listings in the Snowflake Marketplace. | ORGANIZATION_BILLING_VIEWER  
[MARKETPLACE_PAID_USAGE_DAILY view](https://other-docs.snowflake.com/en/collaboration/views/marketplace-paid-usage-daily-org) | Displays daily history of your usage of paid listings from the Snowflake Marketplace. | ORGANIZATION_USAGE_VIEWER  
MARKETPLACE_PURCHASE_EVENTS view |  | ORGANIZATION_BILLING_VIEWER  
[MASKING_POLICIES view](../sql-reference/account-usage/masking_policies) | Displays the masking policies in an organization. | ORGANIZATION_GOVERNANCE_VIEWER  
[MATERIALIZED_VIEW_REFRESH_HISTORY view](../sql-reference/account-usage/materialized_view_refresh_history) | Displays the refresh history of materialized views. | ORGANIZATION_USAGE_VIEWER  
[METERING_DAILY_HISTORY view](../sql-reference/organization-usage/metering_daily_history) | Displays the credit usage for an organization on a given day. | ORGANIZATION_USAGE_VIEWER  
[MONETIZED_USAGE_DAILY](https://other-docs.snowflake.com/en/collaboration/views/monetized-usage-daily-org) | Displays the history of daily consumer usage for each listing in the Snowflake Marketplace, including charges accumulated for the usage. | ORGANIZATION_USAGE_VIEWER  
[OBJECT_DEPENDENCIES view](../sql-reference/account-usage/object_dependencies) | Displays one row for each object dependency. | ORGANIZATION_OBJECT_VIEWER  
[PASSWORD_POLICIES view](../sql-reference/account-usage/password_policies) | Displays the user-defined password policies in an organization. | ORGANIZATION_SECURITY_VIEWER  
[PIPE_USAGE_HISTORY view](../sql-reference/account-usage/pipe_usage_history) | Displays the history of data loaded into Snowflake tables using Snowpipe. | ORGANIZATION_USAGE_VIEWER  
[PIPES view](../sql-reference/account-usage/pipes) | Displays a row for each pipe defined in an organization. | ORGANIZATION_OBJECT_VIEWER  
[POLICY_REFERENCES view](../sql-reference/account-usage/policy_references) | Displays policy objects and their references in an organization. | ORGANIZATION_GOVERNANCE_VIEWER  
[PROCEDURES view](../sql-reference/account-usage/procedures) | Displays a row for each stored procedure defined in an organization. | ORGANIZATION_OBJECT_VIEWER  
[QUERY_ACCELERATION_ELIGIBLE view](../sql-reference/account-usage/query_acceleration_eligible) | Displays queries that are eligible for the query acceleration service. | ORGANIZATION_GOVERNANCE_VIEWER  
[QUERY_ACCELERATION_HISTORY view](../sql-reference/account-usage/query_acceleration_history) | Displays the history of queries accelerated by the query acceleration service. | 

  * ORGANIZATION_GOVERNANCE_VIEWER
  * ORGANIZATION_USAGE_VIEWER

  
[QUERY_HISTORY view](../sql-reference/account-usage/query_history) | Displays the various dimensions (time range, session, user, warehouse, etc.) of the Snowflake query history. | ORGANIZATION_GOVERNANCE_VIEWER  
[RATE_SHEET_DAILY view](../sql-reference/organization-usage/rate_sheet_daily) | Displays the effective rates used for calculating usage in the organization currency based on credits used for all Snowflake accounts in your organization. | ORGANIZATION_BILLING_VIEWER  
[REFERENTIAL_CONSTRAINTS view](../sql-reference/account-usage/referential_constraints) | Displays a row for each referential integrity constraint defined in an organization. | ORGANIZATION_OBJECT_VIEWER  
[REMAINING_BALANCE_DAILY view](../sql-reference/organization-usage/remaining_balance_daily) | Displays the daily remaining balance and on demand consumption daily for an organization. | ORGANIZATION_BILLING_VIEWER  
[REPLICATION_GROUP_REFRESH_HISTORY view](../sql-reference/account-usage/replication_group_refresh_history) | Displays the refresh history for a specified replication or failover group. | ORGANIZATION_USAGE_VIEWER  
[REPLICATION_GROUP_USAGE_HISTORY view](../sql-reference/account-usage/replication_group_usage_history) | Displays the replication history for a specified replication or failover group. | ORGANIZATION_USAGE_VIEWER  
[REPLICATION_USAGE_HISTORY view](../sql-reference/account-usage/replication_usage_history) | Displays the replication history for a specified database. | ORGANIZATION_USAGE_VIEWER  
[RESOURCE_MONITORS view](../sql-reference/account-usage/resource_monitors) | Displays the resource monitors that have been created in the reader accounts managed by an account. | ORGANIZATION_OBJECT_VIEWER  
[ROLES view](../sql-reference/account-usage/roles) | Displays a list of all access control roles defined in an organization. | ORGANIZATION_SECURITY_VIEWER  
[ROW_ACCESS_POLICIES view](../sql-reference/account-usage/row_access_policies) | Displays a row for each row access policy defined in an organization. | ORGANIZATION_GOVERNANCE_VIEWER  
[SCHEMATA view](../sql-reference/account-usage/schemata) | Displays a row for each schema in the account except the ACCOUNT_USAGE, READER_ACCOUNT_USAGE, and INFORMATION_SCHEMA schemas. | ORGANIZATION_OBJECT_VIEWER  
[SEARCH_OPTIMIZATION_HISTORY view](../sql-reference/account-usage/search_optimization_history) | Displays the history of using the search optimization service. | ORGANIZATION_USAGE_VIEWER  
[SEQUENCES view](../sql-reference/account-usage/sequences) | Displays a row for each sequence defined in an organization. | ORGANIZATION_OBJECT_VIEWER  
[SESSION_POLICIES view](../sql-reference/account-usage/session_policies) | Displays the session policies in an organization. | ORGANIZATION_SECURITY_VIEWER  
[SESSIONS view](../sql-reference/account-usage/sessions) | Displays information about sessions, including information on the authentication method to Snowflake and the Snowflake login event. | ORGANIZATION_SECURITY_VIEWER  
[SNOWPIPE_STREAMING_CLIENT_HISTORY view](../sql-reference/account-usage/snowpipe_streaming_client_history) | Displays the amount of time spent loading data into Snowflake tables using Snowpipe Streaming. | ORGANIZATION_USAGE_VIEWER  
[STAGE_STORAGE_USAGE_HISTORY view](../sql-reference/account-usage/stage_storage_usage_history) | Displays the average daily data storage usage, in bytes, for all the Snowflake internal stages in the organization. | ORGANIZATION_USAGE_VIEWER  
[STAGES view](../sql-reference/account-usage/stages) | Displays a row for each stage defined in an organization. | ORGANIZATION_OBJECT_VIEWER  
[STORAGE_DAILY_HISTORY view](../sql-reference/organization-usage/storage_daily_history) | Displays the average daily storage usage, in bytes, for all accounts in the organization. | ORGANIZATION_USAGE_VIEWER  
[TABLE_CONSTRAINTS view](../sql-reference/account-usage/table_constraints) | Displays a row for each referential integrity constraint defined for the tables in an organization. | ORGANIZATION_OBJECT_VIEWER  
[TABLE_STORAGE_METRICS view](../sql-reference/account-usage/table_storage_metrics) | Displays table-level storage utilization information, which is used to calculate the storage billing for each table in an organization, including tables that have been dropped, but are still incurring storage costs. | ORGANIZATION_USAGE_VIEWER  
[TABLES view](../sql-reference/account-usage/tables) | Displays a row for each table and view in an organization. | ORGANIZATION_OBJECT_VIEWER  
[TAG_REFERENCES view](../sql-reference/account-usage/tag_references) | Displays the associations between objects and tags. | ORGANIZATION_GOVERNANCE_VIEWER  
[TAGS view](../sql-reference/account-usage/tags) | Displays the tags in an organization. | ORGANIZATION_OBJECT_VIEWER  
[TASK_HISTORY view](../sql-reference/account-usage/task_history) | Displays the history of task usage. | ORGANIZATION_USAGE_VIEWER  
[TASK_VERSIONS view](../sql-reference/account-usage/task_versions) | Displays the history of task versions. The returned rows indicate the tasks that comprised a task graph and their properties at a given time. | ORGANIZATION_OBJECT_VIEWER  
[USAGE_IN_CURRENCY_DAILY view](../sql-reference/organization-usage/usage_in_currency_daily) | Displays the daily credit usage and usage in currency for an organization. | ORGANIZATION_BILLING_VIEWER  
[USERS view](../sql-reference/account-usage/users) | Displays a list of all users in an organization. | ORGANIZATION_SECURITY_VIEWER  
[VIEWS view](../sql-reference/account-usage/views) | Displays a row for each view in an organization, not including the views in the ACCOUNT_USAGE, READER_ACCOUNT_USAGE, and INFORMATION_SCHEMA schemas. | ORGANIZATION_OBJECT_VIEWER  
[WAREHOUSE_EVENTS_HISTORY view](../sql-reference/account-usage/warehouse_events_history) | Displays the events that have been triggered for the single-cluster and multi-cluster warehouses in an organization. | ORGANIZATION_USAGE_VIEWER  
[WAREHOUSE_LOAD_HISTORY view](../sql-reference/account-usage/warehouse_load_history) | Displays the workload on your warehouse. | ORGANIZATION_USAGE_VIEWER  
[WAREHOUSE_METERING_HISTORY view](../sql-reference/organization-usage/warehouse_metering_history) | Displays the hourly credit usage for one or more warehouses across all the accounts in your organization. | ORGANIZATION_USAGE_VIEWER  
  
[1] For differences between the ACCESS_HISTORY view in the organization
account and the ACCESS_HISTORY view in the ACCOUNT_USAGE schema, see
[Organizational listing governance](collaboration/listings/organizational/org-
listing-governance).

