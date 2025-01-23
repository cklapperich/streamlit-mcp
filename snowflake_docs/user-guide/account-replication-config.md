# Replicating databases and account objects across multiple accounts¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Standard & Business Critical
Feature](intro-editions)

  * Database and share replication are available to all accounts.

  * Replication of other account objects & failover/failback require Business Critical Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic describes the steps necessary to replicate account objects and data
across Snowflake accounts in the same organization, and keep the objects and
data synchronized. Account replication can occur across Snowflake accounts in
different [regions](intro-regions) and across [cloud platforms](intro-cloud-
platforms).

Note

When you upgrade an account to Business Critical Edition (or higher), it might
take up to 12 hours for failover capabilities to become available.

## Region support for replication and failover/failback¶

Customers can replicate across all regions within a Region Group. To replicate
between regions in different [Region groups](admin-account-
identifier.html#label-region-groups) (for example, from a Snowflake commercial
region to a Snowflake government region), please contact [Snowflake
Support](https://docs.snowflake.com/user-guide/contacting-support) to enable
access.

## Transitioning from database replication to group-based replication¶

Databases that have been enabled for replication using [ALTER
DATABASE](../sql-reference/sql/alter-database) must have replication disabled
before they can be added to a replication or failover group.

Note

Execute the SQL statements in this section using the ACCOUNTADMIN role.

### Step 1. Disable replication for a replication enabled database¶

Execute the [SYSTEM$DISABLE_DATABASE_REPLICATION](../sql-
reference/functions/system_disable_database_replication) function to disable
replication for a primary database, along with any secondary databases linked
to it, in order to add it to a replication or failover group.

Execute the following SQL statement from the source account with the primary
database:

    
    
    SELECT SYSTEM$DISABLE_DATABASE_REPLICATION('mydb');
    

Copy

### Step 2. Add the database to a primary failover group and create a
secondary failover group¶

Once you have successfully disabled replication for a database, you can add
the primary database to a failover group in the source account.

Then create a secondary failover group in the target account. When the
secondary failover group is refreshed in the target account, the previously
secondary database will automatically be added as a member of the secondary
failover group and refreshed with the changes from the primary database.

For more details on creating primary and secondary failover groups, see
Workflow.

Note

When you add a previously replicated database to a replication or failover
group, Snowflake does not re-replicate the data that has already been
replicated for that database. Only changes since the last refresh are
replicated when the group is refreshed.

## Workflow¶

The following SQL statements demonstrate the workflow for enabling account and
database object replication and refreshing objects. Each step is discussed in
detail below.

Note

The following examples require replication be enabled for the source and
target accounts. For details, see Prerequisite: Enable replication for
accounts in the organization.

### Examples¶

Execute the following SQL statements in your preferred Snowflake client to
enable account and database object replication and failover, and refresh
objects.

#### Executed on source account¶

  1. Create a role and grant it the CREATE FAILOVER GROUP privilege. This step is _optional_ :
    
        USE ROLE ACCOUNTADMIN;
    
    CREATE ROLE myrole;
    
    GRANT CREATE FAILOVER GROUP ON ACCOUNT
      TO ROLE myrole;
    

Copy

  2. Create a failover group in the source account and enable replication to specific target accounts.

Note

     * If you have databases to add to a replication or failover group that have been previously enabled for database replication and failover using [ALTER DATABASE](../sql-reference/sql/alter-database), follow the Transitioning from database replication to group-based replication instructions (in this topic) before adding them to a group.

     * To add a database to a failover group, the active role must have the MONITOR privilege on the database. For details on database privileges, see [Database privileges](security-access-control-privileges.html#label-database-privileges) (in a separate topic).
    
        USE ROLE myrole;
    
    CREATE FAILOVER GROUP myfg
      OBJECT_TYPES = USERS, ROLES, WAREHOUSES, RESOURCE MONITORS, DATABASES
      ALLOWED_DATABASES = db1, db2
      ALLOWED_ACCOUNTS = myorg.myaccount2, myorg.myaccount3
      REPLICATION_SCHEDULE = '10 MINUTE';
    

Copy

#### Executed on target account¶

  3. Create a role in the target account and grant it the CREATE FAILOVER GROUP privilege. This step is _optional_ :
    
        USE ROLE ACCOUNTADMIN;
    
    CREATE ROLE myrole;
    
    GRANT CREATE FAILOVER GROUP ON ACCOUNT
      TO ROLE myrole;
    

Copy

  4. Create a failover group in the target account as a replica of the failover group in the source account.

Note

If account objects (e.g. users or roles) exist in the target account that do
not exist in the source account, refer to Initial replication of users and
roles before creating a secondary group.

    
        USE ROLE myrole;
    
    CREATE FAILOVER GROUP myfg
      AS REPLICA OF myorg.myaccount1.myfg;
    

Copy

  5. Manually refresh the secondary failover group. This is an _optional_ step. If the primary failover group is created with a replication schedule, the initial refresh of the secondary failover group is automatically executed when the secondary failover group is created.

    1. Create a role with the REPLICATE privilege on the failover group. This step is _optional_.

Execute in the target account using a role with the OWNERSHIP privilege on the
failover group:

        
                GRANT REPLICATE ON FAILOVER GROUP myfg TO ROLE my_replication_role;
        

Copy

    2. Execute the refresh statement using a role with the REPLICATE privilege:
        
                USE ROLE my_replication_role;
        
        ALTER FAILOVER GROUP myfg REFRESH;
        

Copy

  6. Create a role with the FAILOVER privilege on the failover group. This step is _optional_.

Execute in the target account using a role with the OWNERSHIP privilege on the
failover group:

    
        GRANT FAILOVER ON FAILOVER GROUP myfg TO ROLE my_failover_role;;
    

Copy

## Replicating account objects and databases¶

The instructions in this section explain how to prepare your accounts for
replication, enable the replication of specific objects from the source
account to the target account, and synchronize the objects in the target
account.

Important

Target accounts do not have Tri-Secret Secure or private connectivity to the
Snowflake service, such as [AWS PrivateLink](admin-security-privatelink),
enabled by default. If you require Tri-Secret Secure or private connectivity
to the Snowflake service for compliance, security or other purposes, it is
your responsibility to configure and enable those features in the target
account.

### Prerequisite: Enable replication for accounts in the organization¶

The organization administrator (ORGADMIN role) must enable replication for the
source and target accounts.

To enable replication for accounts, a user with the ORGADMIN role uses the
[SYSTEM$GLOBAL_ACCOUNT_SET_PARAMETER](../sql-
reference/functions/system_global_account_set_parameter) function to set the
`ENABLE_ACCOUNT_DATABASE_REPLICATION` parameter to `true`. Note that multiple
accounts in an organization can be enabled for replication from the same
ORGADMIN account.

Log into an ORGADMIN account to enable replication for each source and target
account in your organization.

    
    
    USE ROLE ORGADMIN;
    
    -- View the list of the accounts in your organization
    -- Note the organization name and account name for each account for which you are enabling replication
    SHOW ACCOUNTS;
    
    -- Enable replication by executing this statement for each source and target account in your organization
    SELECT SYSTEM$GLOBAL_ACCOUNT_SET_PARAMETER('<organization_name>.<account_name>', 'ENABLE_ACCOUNT_DATABASE_REPLICATION', 'true');
    

Copy

Though the SYSTEM$GLOBAL_ACCOUNT_SET_PARAMETER function supports the legacy
[account locator](admin-account-identifier.html#label-account-locator)
identifier, it causes unexpected results when an organization has multiple
accounts that share the same locator (in different regions).

### Step 1: Create a role with the CREATE FAILOVER GROUP privilege in the
source account — _Optional_¶

Create a role and grant it the CREATE FAILOVER GROUP privilege. This step is
optional. If you have already created this role, skip to Step 2: Create a
primary failover group in a source account.

    
    
    USE ROLE ACCOUNTADMIN;
    
    CREATE ROLE myrole;
    
    GRANT CREATE FAILOVER GROUP ON ACCOUNT
        TO ROLE myrole;
    

Copy

### Step 2: Create a primary failover group in a source account¶

Create a primary failover group and enable the replication and failover of
specific objects from the current (source) account to one or more target
accounts in the same organization.

#### View all accounts enabled for replication¶

To retrieve the list of accounts in your organization that are enabled for
replication, use [SHOW REPLICATION ACCOUNTS](../sql-reference/sql/show-
replication-accounts).

Execute the following SQL statement using the ACCOUNTADMIN role:

    
    
    SHOW REPLICATION ACCOUNTS;
    

Copy

Returns:

    
    
    +------------------+-------------------------------+--------------+-----------------+-----------------+-------------------+--------------+
    | snowflake_region | created_on                    | account_name | account_locator | comment         | organization_name | is_org_admin |
    +------------------+-------------------------------+--------------+-----------------+-----------------+-------------------+--------------+
    | AWS_US_WEST_2    | 2020-07-15 21:59:25.455 -0800 | myaccount1   | myacctlocator1  |                 | myorg             | true         |
    +------------------+-------------------------------+--------------+-----------------+-----------------+-------------------+--------------+
    | AWS_US_EAST_1    | 2020-07-23 14:12:23.573 -0800 | myaccount2   | myacctlocator2  |                 | myorg             | false        |
    +------------------+-------------------------------+--------------+-----------------+-----------------+-------------------+--------------+
    | AWS_US_EAST_2    | 2020-07-25 19:25:04.412 -0800 | myaccount3   | myacctlocator3  |                 | myorg             | false        |
    +------------------+-------------------------------+--------------+-----------------+-----------------+-------------------+--------------+
    

See the complete list of [Region IDs](admin-account-identifier.html#label-
snowflake-region-ids).

#### View failover and replication group membership¶

Account, database, and share objects have [constraints on group
membership](account-replication-considerations.html#label-group-membership-
constraints). Before creating new groups or adding objects to existing groups,
you can review the list of existing failover groups and the objects in each
group.

Note

Only an account administrator (user with the ACCOUNTADMIN role) or the group
owner (role with the OWNERSHIP privilege on the group) can execute the SQL
statements in this section.

View all failover groups linked to the current account, and the object types
in each group:

>
>     SHOW FAILOVER GROUPS;
>  
>
> Copy

View all the databases in failover group `myfg`:

>
>     SHOW DATABASES IN FAILOVER GROUP myfg;
>  
>
> Copy

View all the shares in failover group `myfg`:

>
>     SHOW SHARES IN FAILOVER GROUP myfg;
>  
>
> Copy

#### Enable replication from a source account to target account¶

You can create a replication or failover group using Snowsight or SQL.

Note

If you have databases to add to a replication or failover group that have been
previously enabled for database replication using [ALTER DATABASE](../sql-
reference/sql/alter-database), follow the Transitioning from database
replication to group-based replication instructions (in this topic) before
adding them to a group.

##### Create a replication or failover group using Snowsight¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Preview Feature](../release-
notes/preview-features) — Open

Available to accounts in all regions and cloud platforms. Currently this
feature is not supported for accounts using private connectivity.

Note

  * Only account administrators can create a replication or failover group using Snowsight (refer to Limitations of using Snowsight for replication configuration).

  * You must be signed in to the target account as a user with the ACCOUNTADMIN role. If you are not, you will be prompted to sign in.

Both the source account and the target account must use the same connection
type (public internet). Otherwise, signing in to the target account fails.

Complete the following steps to create a new replication or failover group:

  1. Sign in to Snowsight and navigate to Admin » Accounts.

  2. Select Replication, select Groups.

  3. Select \+ Add Group.

  4. Select Target Account, then select Next.

  5. In the Group Name box, enter a name for the group that meets the following requirements:

     * Must start with an alphabetic character and cannot contain spaces or special characters unless the identifier string is enclosed in double quotes (e.g. “My object”). Identifiers enclosed in double quotes are also case-sensitive.

For more information, see [Identifier requirements](../sql-
reference/identifiers-syntax).

     * Must be unique across failover and replication groups in an account.

  6. Choose Select Objects to add share and account objects to your group.

Note

Account objects can only be added to one replication or failover group. If a
replication or failover group with any account objects already exists in your
account, you cannot select those objects.

  7. Choose Select Databases to add database objects to your group.

  8. Select the Replication Frequency.

  9. If the account is Business Critical Edition or higher, a failover group is created by default. You can choose to create a replication group instead. To create a replication group, select Advanced Options, then unselect Enable Failover.

  10. Select Start Replication to create the replication group.

If creating the replication group is unsuccessful, refer to Troubleshoot
issues with creating and editing replication groups using Snowsight for common
errors and how to resolve them.

##### Create a failover group using SQL¶

Create a failover group of specified account and database objects in the
source account and enable replication and failover to a list of target
accounts. See [CREATE FAILOVER GROUP](../sql-reference/sql/create-failover-
group) for syntax.

For example, enable replication of users, roles, warehouses, resources
monitors, and databases `db1` and `db2` from the source account to the
`myaccount2` account in the same organization. Set the replication schedule to
automatically refresh `myaccount2` every 10 minutes.

Execute the following statement on the source account:

    
    
    USE ROLE myrole;
    
    CREATE FAILOVER GROUP myfg
        OBJECT_TYPES = USERS, ROLES, WAREHOUSES, RESOURCE MONITORS, DATABASES, INTEGRATIONS, NETWORK POLICIES
        ALLOWED_DATABASES = db1, db2
        ALLOWED_INTEGRATION_TYPES = API INTEGRATIONS
        ALLOWED_ACCOUNTS = myorg.myaccount2
        REPLICATION_SCHEDULE = '10 MINUTE';
    

Copy

### Step 3: Create a role with the CREATE FAILOVER GROUP privilege in the
target account — _Optional_¶

Create a role in the target account and grant it the CREATE FAILOVER GROUP
privilege. This step is optional. If you have already created this role, skip
to Step 4: Create a secondary failover group in the target account.

    
    
    USE ROLE ACCOUNTADMIN;
    
    CREATE ROLE myrole;
    
    GRANT CREATE FAILOVER GROUP ON ACCOUNT
        TO ROLE myrole;
    

Copy

### Step 4: Create a secondary failover group in the target account¶

Note

If account objects (e.g. users or roles) exist in the target account that do
not exist in the source account, refer to Initial replication of users and
roles before creating a secondary group.

Create a secondary failover group in the target account as a replica of the
primary failover group in the source account.

Execute a [CREATE FAILOVER GROUP … AS REPLICA OF](../sql-reference/sql/create-
failover-group) statement in each target account for which you enabled
replication in Step 2: Create a primary failover group in a source account (in
this topic).

Executed from each target account:

    
    
    USE ROLE myrole;
    
    CREATE FAILOVER GROUP myfg
      AS REPLICA OF myorg.myaccount1.myfg;
    

Copy

### Step 5. Refresh a secondary failover group in the target account manually
— _Optional_¶

To manually refresh the objects in a target account, execute the [ALTER
FAILOVER GROUP … REFRESH](../sql-reference/sql/alter-failover-
group.html#label-alter-failover-group) command.

As a best practice, we recommend scheduling your secondary refreshes by
setting the REPLICATION_SCHEDULE parameter using [CREATE FAILOVER
GROUP](../sql-reference/sql/create-failover-group) or [ALTER FAILOVER
GROUP](../sql-reference/sql/alter-failover-group).

Note

If the user who calls the function in the target account was dropped in the
source account, the refresh operation fails.

#### Grant the REPLICATE privilege on failover group to role — _Optional_¶

To execute the command to refresh a secondary replication or failover group in
the target account, you must use a role with the REPLICATE privilege on the
failover group. The REPLICATE privilege is currently not replicated and must
be granted on a failover (or replication) group in both the source and target
accounts.

> Execute this statement from the source account using a role with the
> OWNERSHIP privilege on the group:
>  
>  
>     GRANT REPLICATE ON FAILOVER GROUP myfg TO ROLE my_replication_role;
>  
>
> Copy
>
> Execute this statement from the target account using a role with the
> OWNERSHIP privilege on the group:
>  
>  
>     GRANT REPLICATE ON FAILOVER GROUP myfg TO ROLE my_replication_role;
>  
>
> Copy

#### Manually refresh a secondary failover group¶

For example, to refresh the objects in the failover group `myfg`, execute the
following statement from the target account:

>
>     USE ROLE my_replication_role;
>  
>     ALTER FAILOVER GROUP myfg REFRESH;
>  
>
> Copy

### Step 6. Grant the FAILOVER privilege on failover group to role —
_Optional_¶

To execute the command to fail over a secondary failover group in a target
account, you must use a role with the [FAILOVER privilege](account-
replication-considerations.html#label-replication-privileges) on the failover
group. The FAILOVER privilege is currently not replicated and must be granted
in each source and target account.

For more information, see [Replication of roles and grants](account-
replication-intro.html#label-replicated-privileges).

For example, to grant the FAILOVER privilege to role `my_failover_role` on
failover group `my_fg`, execute the following statement in the _target
account_ using a role with the OWNERSHIP privilege on the group:

    
    
    GRANT FAILOVER ON FAILOVER GROUP myfg TO ROLE my_failover_role;
    

Copy

For instructions on creating a custom role with a specified set of privileges,
see [Creating custom roles](security-access-control-configure.html#label-
security-custom-role).

For general information about roles and privilege grants for performing SQL
actions on [securable objects](security-access-control-overview.html#label-
access-control-securable-objects), see [Overview of Access Control](security-
access-control-overview).

## Apply global IDs to objects created by scripts in target accounts¶

If you created account objects, for example, users and roles, in your target
account by any means other than via replication (e.g. using scripts), these
users and roles have no global identifier by default. The refresh operation
uses global identifiers to synchronize these objects to the same objects in
the source account.

In most cases, when a target account is refreshed from the source account, the
refresh operation drops any account objects of the types in the `OBJECT_TYPES`
list in the target account that have no global identifier. The initial
replication of users and roles to a target account, however, might cause the
first refresh operation to fail. For details on this behavior, refer to
Initial replication of users and roles.

### Use SYSTEM$LINK_ACCOUNT_OBJECTS_BY_NAME() to apply global IDs¶

You can prevent the loss of some object types by linking matching objects with
the same name in the source and target accounts. The
SYSTEM$LINK_ACCOUNT_OBJECTS_BY_NAME function adds a global identifier to
account objects in the target account.

Note

Global identifiers are only added to account objects that are included in a
replication or failover group for the following object types:

  * `RESOURCE_MONITOR`

  * `ROLE`

  * `USER`

  * `WAREHOUSE`

Apply global identifiers to account objects in the target account of the types
included in the `object_types` list for failover group `myfg`:

Execute the following SQL statement using the ACCOUNTADMIN role:

    
    
    SELECT SYSTEM$LINK_ACCOUNT_OBJECTS_BY_NAME('myfg');
    

Copy

### Initial replication of users and roles¶

The behavior of the initial refresh operation for USERS and ROLES object types
can vary depending on whether or not there are matching objects with the same
name in the target account.

Note

  * The behavior described in this section applies only the first time these object types are replicated to the target account.

  * The scenarios below describe the replication of USERS. The same also applies to the replication of ROLES.

  * If there are existing users in the target account with the same name as users in the source account, the initial refresh operation fails and describes the two options you have to continue:

>     * Force the refresh operation and allow any existing users in the target
> account to be dropped. The users in the source account will be replicated to
> the target account.
>
> To force a refresh for a group, use the FORCE parameter for the refresh
> command. For example, to force the refresh of a failover group, execute the
> following command:
>  
>         >         ALTER FAILOVER GROUP <fg_name> REFRESH FORCE;
>  
>
> Copy
>
>     * Link the account objects by name. The
> [SYSTEM$LINK_ACCOUNT_OBJECTS_BY_NAME](../sql-
> reference/functions/system_link_account_objects_by_name) function links
> users with the same name in both the target account and the source account.
> Users in the target account that are linked are not deleted.
>
> To link account objects by name, execute the following command:
>  
>         >         SELECT SYSTEM$LINK_ACCOUNT_OBJECTS_BY_NAME('<rg_name>');
>  
>
> Copy
>
> Note
>
> Any user in the target account that _does not_ have a matching user in the
> source account with the same name is dropped.

  * If there are no users in the target account with names matching users in the source account, the initial refresh operation in the target account drops all users. This can result in the following data and metadata loss:

>     * If USERS are included in the OBJECT_TYPES list for a replication or
> failover group:
>

>>       * Worksheets are lost.

>>

>>       * Query history is lost.

>
>     * If USERS are included in the OBJECT_TYPES list, but ROLES is not:
>

>>       * Privilege grants to users are lost.

>
>     * If ROLES are included in the OBJECT_TYPES list:
>

>>       * Privilege grants to share objects are lost.

To avoid dropping users or roles in the target account:

  1. In the source account, manually recreate any users or roles that exist _only_ in the target account before the initial replication.

  2. In the target account, link matching objects with the same name in both accounts using the [SYSTEM$LINK_ACCOUNT_OBJECTS_BY_NAME](../sql-reference/functions/system_link_account_objects_by_name) function.

## Configure cloud storage access for secondary storage integrations¶

If you enable storage integration replication, you must take additional steps
after the storage integration is replicated to target accounts. The replicated
integration has its own identity and access management (IAM) entity that is
different from the identity and IAM entity of the primary integration.
Therefore, you must update your cloud provider permissions to grant the
replicated integration access to your cloud storage.

You only need to configure this trust relationship on target accounts one
time.

The process is similar to granting access in the source account. See the
following pages for more information:

  * [Configuring a Snowflake storage integration to access Amazon S3](data-load-s3-config-storage-integration)

  * [Configuring an integration for Google Cloud Storage](data-load-gcs-config)

  * [Configuring a Snowflake storage integration for Azure](data-load-azure-config.html#label-configuring-azure-storage-integration)

## Configure automated refresh for directory tables on secondary stages¶

If you replicate an external stage with a directory table, and you have
configured automated refresh for the source directory table, you must take
steps to configure [automated refresh](data-load-dirtables-auto) for the
secondary directory table.

The process is similar to setting up automated refresh in your source account.
See the following for more information:

  * Amazon S3: The configuration process depends on how you set up event notifications.

    * If you use Amazon S3 Event Notifications with Amazon Simple Queue Service (SQS), follow the instructions in [Step 2: Configure event notifications](data-load-dirtables-auto-s3.html#label-data-load-dirtables-auto-s3-configure-event-notifications). You can also migrate from SQS to SNS. For more information, see [Migrate to Amazon Simple Notification Service (SNS)](account-replication-stages-pipes-load-history.html#label-account-replication-stages-pipes-load-history-migrate-to-sns).

    * If you use Amazon Simple Notification Service (SNS), see [Subscribing the Snowflake SQS Queue to your SNS topic](data-load-dirtables-auto-s3.html#label-sns-topic-dirtables).

  * Google Cloud Storage: Create a new subscription to your Pub/Sub topic and a new notification integration in your target account. Then, grant Snowflake access to the Pub/Sub subscription. For instructions, see [Configuring Automation Using GCS Pub/Sub](data-load-dirtables-auto-gcs.html#label-data-load-dirtables-auto-refresh-gcs).

  * Azure Blob Storage: Create a new Event Grid subscription and storage queue. Then, create a new notification integration in the target account and grant Snowflake access to your storage queue. For instructions, see [Configuring Automation With Azure Event Grid](data-load-dirtables-auto-azure.html#label-data-load-dirtables-auto-azure).

Important

  * After you complete these configuration steps in your target account, you should perform a full refresh of your directory table to ensure that it has not missed any notifications.

  * For Google Cloud Storage and Azure Blob Storage, the name of the notification integration in each target account must match the name of the notification integration in the source account.

## Configure notifications for secondary auto-ingest pipes¶

You must take additional steps to configure cloud notifications for secondary
auto-ingest pipes before failover. This section covers why this additional
configuration is required, and how to complete it for each supported cloud
provider.

### Amazon S3¶

The configuration process depends on how you set up event notifications. For
example, suppose you have an auto-ingest pipe that relies on an Amazon Simple
Notification Service (SNS) topic to publish messages about the Snowflake stage
location.

When you replicate the pipe to a target account, Snowflake automatically
creates a new Amazon Simple Queue Service (SQS) queue. You must subscribe this
SQS queue for your target account to the SNS topic to get notifications about
the stage location.

  * If you use Amazon S3 Event Notifications with Amazon Simple Queue Service (SQS), follow the instructions in [Step 4: Configure event notifications](data-load-snowpipe-auto-s3.html#label-data-load-snowpipe-auto-s3-configure-sqs).

Important

To ensure that the pipe has not missed any notifications, you should refresh
the pipe after switching to the new SQS queue.

You can also migrate from SQS to SNS. For more information, see [Migrate to
Amazon Simple Notification Service (SNS)](account-replication-stages-pipes-
load-history.html#label-account-replication-stages-pipes-load-history-migrate-
to-sns).

  * If you use Amazon Simple Notification Service (SNS), see [Subscribing the Snowflake SQS Queue to your SNS topic](data-load-snowpipe-auto-s3.html#label-create-sns-topic-subscription).

  * If you use Amazon EventBridge, see [Option 3: Setting up Amazon EventBridge to automate Snowpipe](data-load-snowpipe-auto-s3.html#label-data-load-snowpipe-auto-s3-eventbridge).

### Microsoft Azure Blob Storage¶

A pipe that automatically loads data from files located on a stage in
Microsoft Azure blob storage requires an Event Grid subscription, storage
queue, and a notification integration bound to the storage queue. A secondary
pipe in a target account needs a separate Event Grid, storage queue, and
notification integration bound to the storage queue. The Event Grid in both
source and target accounts must be configured as endpoints for the same Azure
Storage source.

See the diagram below for configuration details:

[![Pipe replication for Azure](../_images/data-pipeline-replication-
azure.png)](../_images/data-pipeline-replication-azure.png)

Create a new Event Grid subscription and storage queue. Then, create a new
notification integration in the target account and grant Snowflake access to
your storage queue. For instructions, see [Configuring Automation With Azure
Event Grid](data-load-snowpipe-auto-azure.html#label-azure-configuring-
automation).

Important

The name of the notification integration in each target account must match the
name of the notification integration in the source account.

### External stage for Google Cloud Storage¶

A pipe that automatically loads data from files located in Google Cloud
Storage requires a Google Pub/Sub subscription and a notification integration
that references that subscription. Each replicated pipe in a target account
also requires a Google Pub/Sub subscription and a notification integration
that references that subscription. The Pub/Sub subscription in each source and
target account must be subscribed to the same Pub/Sub Topic that receives
notifications from the Google Cloud Storage source.

See the diagram below for configuration details:

[![Pipe replication for GCP](../_images/data-pipeline-replication-
gcp.png)](../_images/data-pipeline-replication-gcp.png)

Create a new subscription to your Pub/Sub topic and a new notification
integration in your target account.

    

Then, grant Snowflake access to the Pub/Sub subscription. For instructions,
see [Configuring Automation Using GCS Pub/Sub](data-load-snowpipe-auto-
gcs.html#label-gcp-pubsub-snowpipe).

Important

The name of the notification integration in each target account must match the
name of the notification integration in the source account.

## Updating the remote service for API integrations¶

If you have enabled API integration replication, additional steps are required
after the API integration is replicated to the target account. The replicated
integration has its own identity and access management (IAM) entity that are
different from the identity and IAM entity of the primary integration.
Therefore, you must update the permissions on the remote service to grant
access to replicated functions. The process is similar to granting access to
the functions on the primary account. See the below links for more details:

  * Amazon Web Services [Set up the trust relationship(s) between Snowflake and the new IAM role](../sql-reference/external-functions-creating-aws-common-api-integration-proxy-link.html#label-external-functions-creating-aws-set-up-trust-relationship).

  * Google Cloud Platform: [Create a GCP Security Policy for the Proxy Service](../sql-reference/external-functions-creating-gcp-ui-security-policy).

  * Microsoft Azure:

    * Step 1. [Link the API integration for Azure](../sql-reference/external-functions-creating-azure-common-api-integration-proxy-link)

    * Step 2. [Create a validate-JWT policy](../sql-reference/external-functions-creating-azure-ui-security-policy.html#label-azure-create-validate-jwt-policy)

## Comparing data sets in primary and secondary databases¶

If database objects are replicated in a replication or failover group, the
[HASH_AGG](../sql-reference/functions/hash_agg) function can be used to
compare the rows in a random set of tables in a primary and secondary database
to verify data consistency. The HASH_AGG function returns an aggregate signed
64-bit hash value over the (unordered) set of input rows. Query this function
on all or a random subset of tables in a secondary database and on the primary
database (as of the timestamp for the primary database snapshot) and compare
the output.

### Example¶

In the examples below, the database `mydb` is included in the failover group
`myfg`. The database `mydb` contains the table `mytable`.

#### Executed on target account¶

  1. Query the [REPLICATION_GROUP_REFRESH_PROGRESS](../sql-reference/functions/replication_group_refresh_progress) table function (in the [Snowflake Information Schema](../sql-reference/info-schema)). Note the `primarySnapshotTimestamp` in the `DETAILS` column for the `PRIMARY_UPLOADING_METADATA` phase. This is the timestamp for the latest snapshot of the primary database.
    
        SELECT PARSE_JSON(details)['primarySnapshotTimestamp']
      FROM TABLE(information_schema.replication_group_refresh_progress('myfg'))
      WHERE PHASE_NAME = 'PRIMARY_UPLOADING_METADATA';
    

Copy

  2. Query the HASH_AGG function for a specified table in the secondary database. The following query returns a hash value for all rows in the `mytable` table:
    
        SELECT HASH_AGG( * ) FROM mytable;
    

Copy

#### Executed on source account¶

  3. Query the HASH_AGG function for the same table in the primary database. Using Time Travel, specify the timestamp when the latest snapshot was taken for the secondary database:
    
        SELECT HASH_AGG( * ) FROM mytable AT(TIMESTAMP => '<primarySnapshotTimestamp>'::TIMESTAMP);
    

Copy

  4. Compare the results from the two queries. The output should be identical.

## Modifying a replication or failover group¶

You can edit the name, included objects, and replication schedule of a
replication or failover group using Snowsight or SQL.

### Modify a replication or failover group using Snowsight¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Preview Feature](../release-
notes/preview-features) — Open

Available to accounts in all regions and cloud platforms. Currently this
feature is not supported for accounts using private connectivity.

Note

Only account administrators can edit a replication or failover group using
Snowsight (refer to Limitations of using Snowsight for replication
configuration).

To edit the name of the group, you must be signed in to the target account. If
you are not signed in, the Status column displays a sign in message instead of
the refresh status.

Both the source account and the target account must use the same connection
type (public internet). Otherwise, signing in to the target account fails.

  1. Sign in to Snowsight and navigate to Admin » Accounts.

  2. Select Replication, select Groups.

  3. Locate the replication or failover group you want to edit. Select the More menu (…) in the last column of the row.

  4. Select Edit.

  5. To change the group name, enter a new name in the Group Name box that meets the following requirements:

     * Must start with an alphabetic character and cannot contain spaces or special characters unless the identifier string is enclosed in double quotes (e.g. “My object”). Identifiers enclosed in double quotes are also case-sensitive.

For more information, see [Identifier requirements](../sql-
reference/identifiers-syntax).

     * Names for failover groups and replication groups in an account must be unique.

  6. Choose Select Objects to add or remove share and account objects.

Note

Account objects can only be added to one replication or failover group. If a
replication or failover group with any account objects already exists in your
account, you cannot select those objects.

  7. Choose Select Databases to add or remove database objects.

  8. Select the Replication Frequency to change the replication schedule for a group.

  9. Select Save Changes to update the group.

If saving the changes to the group is unsuccessful, refer to Troubleshoot
issues with creating and editing replication groups using Snowsight for common
errors and how to resolve them.

### Modify a replication or failover group using SQL¶

You can modify a replication or failover group properties using the [ALTER
REPLICATION GROUP](../sql-reference/sql/alter-replication-group) or [ALTER
FAILOVER GROUP](../sql-reference/sql/alter-failover-group) command.

## Dropping a secondary replication or failover group¶

You can drop a secondary replication or failover using the [DROP REPLICATION
GROUP](../sql-reference/sql/drop-replication-group) or the [DROP FAILOVER
GROUP](../sql-reference/sql/drop-failover-group) command. Only the replication
or failover group owner (i.e. the role with the OWNERSHIP privilege on the
group) can drop the group.

To drop a secondary replication or failover group using Snowsight, you must
drop the group in the source account. See Drop a replication or failover group
using Snowsight.

## Dropping a primary replication or failover group¶

You can drop a primary replication or failover group using Snowsight or SQL.
If you are deleting a primary group using SQL, you must first drop all
secondary groups. See Dropping a secondary replication or failover group.

### Drop a primary replication or failover group using SQL¶

A primary replication or failover group can only be dropped after all the
replicas of the group (i.e. secondary replication or failover groups) have
been dropped. Alternatively, you can promote a secondary failover group to
serve as the primary failover group, then drop the former primary failover
group.

Note that only the group owner can drop the group.

### Drop a replication or failover group using Snowsight¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Preview Feature](../release-
notes/preview-features) — Open

Available to accounts in all regions and cloud platforms. Currently this
feature is not supported for accounts using private connectivity.

Note

Only account administrators can delete a replication or failover group using
Snowsight (refer to Limitations of using Snowsight for replication
configuration).

You can delete a primary replication or failover group and any linked
secondary groups.

  1. Sign in to Snowsight and navigate to Admin » Accounts.

  2. Select Replication, select Groups.

  3. Locate the replication or failover group you want to delete. Select the More menu (…) in the last column of the row.

  4. Select Drop, then select Drop Group.

## Troubleshoot issues with creating and editing replication groups using
Snowsight¶

The following scenarios can help you troubleshoot common issues that can occur
when creating or editing replication or failover group using Snowsight.

  * You cannot add a database to a group

  * You cannot add a share to a group

### You cannot add a database to a group¶

Error | 
    
    
    Database '<database_name>' is already configured to replicate to
    account '<account_name>' by replication group '<group_name>'.
      
  
---|---  
Cause | A database can only be in one replication or failover group. One of the databases you selected for the group is already included in another replication or failover group.  
Solution | Choose Select Databases and unselect any database(s) that are already included in another group.  
Error | 
    
    
    Cannot directly add previously replicated object '<database_name>' to a
    replication group. Please use the provided system functions to convert
    this object first.
      
  
---|---  
Cause | The database you want to add to a replication or failover group was previously configured for database replication.  
Solution | Disable database replication for the database. See Transitioning from database replication to group-based replication.  
  
### You cannot add a share to a group¶

Error | 
    
    
    Share '<share_name>' is already configured to replicate to
    account '<account_name>' by replication group '<group_name>'.
      
  
---|---  
Cause | A share can only be in one replication or failover group. One of the shares you selected for the group is already included in another replication or failover group.  
Solution | Choose Select Objects and unselect any share(s) that are already included in another group.  
  
## Limitations of using Snowsight for replication configuration¶

  * Only a user with the ACCOUNTADMIN role can create a replication or failover group using Snowsight. A user with a role with the CREATE REPLICATION GROUP or CREATE FAILOVER GROUP privilege can create a group using the respective SQL commands.

  * Only a user with the ACCOUNTADMIN role can edit or drop a replication or failover group using Snowsight. A user with a role with the OWNERSHIP privilege on a replication or failover group can edit and drop groups using the respective SQL commands.

