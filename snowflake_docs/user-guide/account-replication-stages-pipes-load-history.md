# Stage, pipe, and load history replication¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Standard & Business Critical
Feature](intro-editions)

  * Database and share replication are available to all accounts.

  * Replication of other account objects & failover/failback require Business Critical Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic provides information about replication support for data pipeline
objects and related metadata, including stages, storage integrations, pipes,
and load history. You can replicate these objects to configure failover for
ingest and ETL pipelines across [regions](intro-regions) and across [cloud
platforms](intro-cloud-platforms).

Before you get started, we recommend that you have familiarity with Snowflake
support for replication and failover/failback. For more information, see
[Introduction to replication and failover across multiple accounts](account-
replication-intro).

## Requirements¶

Important

If a database in a target account that you plan to use already contains stages
and pipes, we recommend that you contact support before enabling replication.
When a replication or failover group in your source account includes that
database, any pre-existing stages and pipes are dropped from the database.

To replicate any external stages that use a storage integration, you must
configure your replication or failover group to replicate `STORAGE
INTEGRATIONS`. Otherwise, external stages are replicated without the
associated storage integration.

You can use an [ALTER REPLICATION GROUP](../sql-reference/sql/alter-
replication-group) or [ALTER FAILOVER GROUP](../sql-reference/sql/alter-
failover-group) statement to modify these properties for an existing group.

If you add `INTEGRATIONS` to the `OBJECT_TYPES` list in your ALTER statement,
include any other existing objects in the list to avoid dropping those objects
in the target account. The same applies if you add `STORAGE INTEGRATIONS` to
the `ALLOWED_INTEGRATION_TYPES` list.

For example:

    
    
    ALTER FAILOVER GROUP my_failover_group SET
      OBJECT_TYPES = ROLES, INTEGRATIONS
      ALLOWED_INTEGRATION_TYPES = API INTEGRATIONS, STORAGE INTEGRATIONS;
    

Copy

Note

Your cloud storage provider might limit replication of data pipeline objects
between commercial and government cloud regions. To avoid government cloud
data replication limitations, configure your failover resources in any region
accessible to your government cloud region. For more information about
government cloud limitations, review your cloud storage provider’s
documentation.

## Replication and stages¶

This section describes the current level of replication functionality that
Snowflake supports for different types of stages.

### Replication of internal stages¶

The following table describes how replication works for each type of internal
stage.

Type | Description of Replication Support  
---|---  
Table stage | Empty table stages are created for tables in a replicated database. Files on table stages are not replicated.  
User stage | User and user stage replication requires Business Critical Edition (or higher). Empty user stages are created for replicated users. Files on user stages are not replicated.  
Named stage | Named internal stages are replicated when you replicate a database. The stage must have a directory table enabled on it in order to replicate the files on the stage.  
  
### Replication of external stages¶

Note

Snowflake does not replicate files on an external stage. The cloud storage URL
points to the same location for external stages in primary and secondary
databases.

The following table describes how replication works for each type of external
stage.

Type | Description of Replication Support  
---|---  
Named stage with no credentials (public storage location) | Named external stages are replicated when you replicate a database. The files on an external stage are not replicated.  
Named stage with credentials (private storage location) | Replicated stages include the cloud provider credentials, such as secret keys or access tokens.  
Named stage with storage integration (private storage location) | Storage integration replication requires Business Critical Edition (or higher). The replication or failover group must include `STORAGE INTEGRATIONS` in the `ALLOWED_INTEGRATION_TYPES` list. For more information, see [CREATE FAILOVER GROUP](../sql-reference/sql/create-failover-group). You must also take action to configure the trust relationships for your cloud storage in the target accounts. For more information, see [Configure cloud storage access for secondary storage integrations](account-replication-config.html#label-configure-cloud-storage-access-secondary-storage-integrations).  
  
Note

To associate a secondary stage or pipe with a different cloud storage location
than the one associated with the primary object, contact the support team. For
example, you might choose a location in another region.

### Considerations¶

The following constraints apply to stage objects:

  * Snowflake currently supports stage replication as part of group-based replication (replication and failover groups). Stage replication is not supported for database replication.

  * You can replicate an external stage. However, the files on an external stage are not replicated.

  * You can replicate an internal stage. To replicate the files on an internal stage, you must enable a directory table on the stage. Snowflake replicates only the files that are mapped by the directory table.

  * When you replicate an internal stage with a directory table, you cannot disable the directory table on the primary or secondary stage. The directory table contains critical information about replicated files and files loaded using a COPY statement.

  * A refresh operation will fail if the directory table on an internal stage contains a file that is larger than 5GB. To work around this limitation, move any files larger than 5GB to a different stage.

You cannot disable the directory table on a primary or secondary stage, or any
stage that has previously been replicated. Follow these steps _before_ you add
the database that contains the stage to a replication or failover group.

    1. [Disable the directory table](../sql-reference/sql/alter-stage.html#label-alter-stage-directory-table-syntax) on the primary stage.

    2. Move the files that are larger than 5GB to another stage that does not have a directory table enabled.

    3. After you move the files to another stage, re-enable the directory table on the primary stage.

  * Files on user stages and table stages are not replicated.

  * For named external stages that use a storage integration, you must configure the trust relationship for secondary storage integrations in your target accounts prior to failover. For more information, see [Configure cloud storage access for secondary storage integrations](account-replication-config.html#label-configure-cloud-storage-access-secondary-storage-integrations).

  * If you replicate an external stage with a directory table, and you have configured [automated refresh](data-load-dirtables-auto) for the source directory table, you must configure automated refresh for the secondary directory table before failover. For more information, see [Configure automated refresh for directory tables on secondary stages](account-replication-config.html#label-configure-automated-refresh-secondary-directory-tables).

  * A copy command might take longer than expected if the directory table on a replicated stage is not consistent with the replicated files on the stage. To make a directory table consistent, refresh it with an [ALTER STAGE … REFRESH](../sql-reference/sql/alter-stage) statement. To check the consistency status of a directory table, use the [SYSTEM$GET_DIRECTORY_TABLE_STATUS](../sql-reference/functions/system_get_directory_table_status) function.

## Replication and pipes¶

This section describes the current level of replication functionality
supported for different types of pipes.

Snowflake supports replication for the following:

  * Pipe objects, including auto-ingest and REST endpoint pipes that load data from external stages.

  * Pipe-level parameters.

  * Privilege grants on pipe objects.

Note

To associate a secondary stage or pipe with a different cloud storage location
than the one associated with the primary object, contact the support team. For
example, you might choose a location in another region.

### Pipes in secondary databases¶

Pipes in a secondary database are in a `READ_ONLY` execution state and receive
notifications but do not load data until you promote the secondary database to
serve as the primary. After you promote a secondary database, the pipes will
transition to a `FAILING_OVER` execution state. Once failover is complete, the
pipes should be in the `RUNNING` execution state and begin to load any data
that is available since the last refresh time (that is, the last time that the
former primary database was updated).

### Replication of auto-ingest pipes¶

In the event of a failover, a replicated auto-ingest pipe becomes the new
primary pipe and can do the following:

  * Load any data that has not yet been loaded. This includes any data that is new since the newly promoted primary database was last refreshed.

  * Continue to receive notifications when the stage has new files to load, and loads data from those files.

Note

To receive notifications, you must configure a secondary auto-ingest pipe in a
target account prior to failover. For more information, see [Configure
notifications for secondary auto-ingest pipes](account-replication-
config.html#label-configure-notifications-secondary-pipes).

### Replication of REST endpoint pipes¶

For pipes that use the [Snowpipe REST API](data-load-snowpipe-rest-load) to
load data, Snowflake replicates the pipes and their load history metadata to
each target account that you specify. There are no additional configuration
steps you need to take on the target accounts. For a detailed list of load
history metadata, see [Load metadata](data-load-considerations-
load.html#label-copy-load-metadata).

To continue data loading in the event of a failover, call the REST API from
the newly-promoted source account.

### Considerations¶

The following constraints apply to pipe objects:

  * Snowflake currently supports pipe replication as part of group-based replication (replication and failover groups). Pipe replication is not supported for database replication.

  * Snowflake replicates the copy history of a pipe only when the pipe belongs to the same replication group as its target table.

  * Replication of notification integrations is not supported.

  * Snowflake only replicates load history after the latest table truncate.

  * To receive notifications, you must configure a secondary auto-ingest pipe in a target account prior to failover. For more information, see [Configure notifications for secondary auto-ingest pipes](account-replication-config.html#label-configure-notifications-secondary-pipes).

  * Use the [SYSTEM$PIPE_STATUS](../sql-reference/functions/system_pipe_status) function to resolve any pipes not in their expected execution state after failover.

## Example 1: Replicate a named internal stage¶

This example demonstrates how replication works for internal stages. In
particular, the example shows how the directory table is the single source of
truth for stage metadata before and after replication.

The first part of the example completes the following tasks in a source
account.

  1. Create an internal stage named `my_int_stage` with a directory table enabled to replicate the files on the stage. Then copy data from a table named `my_table` into files on the stage.

Note

The example refreshes the directory table after loading `file1` and `file2`
onto the stage to synchronize the table metadata with the latest set of files
in the stage definition for the directory tables. However, no refresh
operation occurs after loading `file3`.

    
        CREATE OR REPLACE STAGE my_stage
      DIRECTORY = (ENABLE = TRUE);
    
    COPY INTO @my_stage/folder1/file1 from my_table;
    COPY INTO @my_stage/folder2/file2 from my_table;
    ALTER STAGE my_stage REFRESH;
    
    COPY INTO @my_stage/folder3/file3 from my_table;
    

Copy

  2. Create a failover group:
    
        CREATE FAILOVER GROUP my_stage_failover_group
      OBJECT_TYPES = DATABASES
      ALLOWED_DATABASES = my_database_1
      ALLOWED_ACCOUNTS = myorg.my_account_2;
    

Copy

The second part of the example completes the replication and failover process
in a target account:

  1. Create a failover group as a replica of the failover group in the source account, refresh the objects in the new failover group, and promote the target account to serve as the source account.
    
        CREATE FAILOVER GROUP my_stage_failover_group
      AS REPLICA OF myorg.my_account_1.my_stage_failover_group;
    
    ALTER FAILOVER GROUP my_stage_failover_group REFRESH;
    
    ALTER FAILOVER GROUP my_stage_failover_group PRIMARY;
    

Copy

  2. Next, refresh the directory table on the replicated stage and copy all of the files tracked by the directory table on `my_stage` into a table named `my_table` .

Note

The COPY INTO statement loads `file1` and `file2` into the table, but not
`file3`. This is because the directory table was not refreshed after adding
`file3` in the source account.

    
        ALTER STAGE my_stage REFRESH;
    
    COPY INTO my_table FROM @my_stage;
    

Copy

## Example 2: Replicate an external stage and storage integration¶

This example provides a sample workflow for replicating an external stage and
storage integration to a target account.

The example assumes that you have already completed the following: [Configured
secure access to your Amazon S3 bucket](data-load-snowpipe-auto-s3.html#label-
data-load-snowpipe-secure-access-s3).

The first part of the example completes the following tasks in a source
account.

  1. Create a storage integration for an Amazon S3 bucket in database `my_database_2`.
    
        CREATE STORAGE INTEGRATION my_storage_int
      TYPE = external_stage
      STORAGE_PROVIDER = 's3'
      STORAGE_ALLOWED_LOCATIONS = ('s3://mybucket/path')
      STORAGE_BLOCKED_LOCATIONS = ('s3://mybucket/blockedpath')
      ENABLED = true;
    

Copy

  2. Create an external stage in database `my_database_2` using storage integration `my_storage_int`.
    
        CREATE STAGE my_ext_stage
      URL = 's3://mybucket/path'
      STORAGE_INTEGRATION = my_storage_int
    

Copy

  3. Create a failover group and include database `my_database_2` and storage integration objects.
    
        CREATE FAILOVER GROUP my_external_stage_fg
      OBJECT_TYPES = databases, integrations
      ALLOWED_INTEGRATION_TYPES = storage integrations
      ALLOWED_DATABASES = my_database_2
      ALLOWED_ACCOUNTS = myorg.my_account_2;
    

Copy

The second part of the example completes the replication and failover process
in a target account:

  1. Create a failover group as a replica of the failover group in the source account and refresh.
    
        CREATE FAILOVER GROUP my_external_stage_fg
      AS REPLICA OF myorg.my_account_1.my_external_stage_fg;
    
    ALTER FAILOVER GROUP my_external_stage_fg REFRESH;
    

Copy

  2. After you replicate the storage integration to the target account, you must take additional steps to update your cloud provider permissions to grant the replication integration access to your cloud storage. For more information, see [Configure cloud storage access for secondary storage integrations](account-replication-config.html#label-configure-cloud-storage-access-secondary-storage-integrations).

## Example 3: Replicate an auto-ingest pipe¶

This example provides a sample workflow for replicating a pipe that uses an
[Amazon Simple Notification Service (SNS) topic with Amazon Simple Queue
Service (SQS) to automate Snowpipe](data-load-snowpipe-auto-s3.html#label-
configuring-amazon-sns-for-snowpipe).

The example assumes that you have already completed the following tasks:

  * [Created and configured a storage integration for Amazon S3](data-load-snowpipe-auto-s3.html#label-data-load-snowpipe-secure-access-s3). For example purposes, we use a storage integration named `my_s3_storage_int`.

  * [Created an Amazon SNS topic and subscription, and subscribed the Snowflake SQS queue to your SNS topic](data-load-snowpipe-auto-s3.html#label-create-sns-topic-subscription).

  * Created an external stage that references your storage integration. For example purposes, we use a stage named `my_s3_stage`. For instructions, see [CREATE STAGE](../sql-reference/sql/create-stage).

Start with the following tasks in a source account.

  1. Use the [CREATE PIPE](../sql-reference/sql/create-pipe) command to create a pipe with auto-ingest enabled that loads data from the external stage into a table named `mytable`.
    
        CREATE PIPE snowpipe_db.public.mypipe AUTO_INGEST=TRUE
     AWS_SNS_TOPIC='<topic_arn>'
     AS
       COPY INTO snowpipe_db.public.mytable
       FROM @snowpipe_db.public.my_s3_stage
       FILE_FORMAT = (TYPE = 'JSON');
    

Copy

  2. Refresh the pipe with an [ALTER PIPE](../sql-reference/sql/alter-pipe) statement to load data from the stage from the last 7 days.
    
        ALTER PIPE mypipe REFRESH;
    

Copy

  3. Finally, use [CREATE FAILOVER GROUP](../sql-reference/sql/create-failover-group) to create a failover group that allows replication of storage integrations.
    
        CREATE FAILOVER GROUP my_pipe_failover_group
      OBJECT_TYPES = DATABASES, INTEGRATIONS
      ALLOWED_INTEGRATION_TYPES = STORAGE INTEGRATIONS
      ALLOWED_DATABASES = snowpipe_db
      ALLOWED_ACCOUNTS = myorg.my_account_2;
    

Copy

The second part of the example completes the replication and failover process
in a target account:

  1. Create a failover group as a replica of the failover group in the source account.
    
        CREATE FAILOVER GROUP my_pipe_failover_group
      AS REPLICA OF myorg.my_account_1.my_pipe_failover_group;
    

Copy

  2. Execute a [DESCRIBE INTEGRATION](../sql-reference/sql/desc-integration) statement to retrieve the ARN for the AWS IAM User for your Snowflake account on the secondary deployment.

Use the ARN to grant the IAM user permissions to access your S3 bucket. [See
Step 5: Grant the IAM User Permissions to Access Bucket Objects](data-
load-s3-config-storage-integration.html#label-data-load-s3-storage-
integration-steps).

    
        DESC INTEGRATION my_s3_storage_int;
    

Copy

  3. Call the [SYSTEM$GET_AWS_SNS_IAM_POLICY](../sql-reference/functions/system_get_aws_sns_iam_policy) system function to generate an IAM policy that grants the new SQS queue permission to subscribe to your SNS topic. Snowflake created the new SQS queue in your target account when you replicated the failover group from your source account.
    
        SELECT SYSTEM$GET_AWS_SNS_IAM_POLICY('<topic_arn>');
    

Copy

`_topic_arn_` is the Amazon Resource Name (ARN) of the SNS topic that you
created for the original pipe in your source account.

Then, [Subscribe the new Amazon SQS queue to your SNS topic](data-load-
snowpipe-auto-s3.html#label-create-sns-topic-subscription).

  4. Refresh the objects in your new failover group.
    
        ALTER FAILOVER GROUP my_pipe_failover_group REFRESH;
    

Copy

  5. Finally, promote the target account to serve as the source account with the [ALTER FAILOVER GROUP](../sql-reference/sql/alter-failover-group) command.
    
        ALTER FAILOVER GROUP my_pipe_failover_group PRIMARY;
    

Copy

The `mypipe` pipe will begin to load any data that was made available since
the last time the failover group was refreshed in the source account.

To verify that the replicated pipe is working, query the table from the pipe’s
COPY statement.

    
        SELECT * FROM mytable;
    

Copy

## Migrate to Amazon Simple Notification Service (SNS)¶

This section covers how to migrate from sending Amazon S3 event notifications
directly to an Amazon Simple Queue Service (SQS) queue to using an Amazon
Simple Notification Service (SNS) topic for the following scenarios:

  * [Refreshing directory tables automatically for Amazon S3](data-load-dirtables-auto-s3)

  * [Automating Snowpipe for Amazon S3](data-load-snowpipe-auto-s3)

When you replicate a directory table or pipe, Snowflake creates a new SQS
queue in your target account to handle automation. You can configure a single
SNS topic to deliver event notifications from your S3 bucket to all SQS queues
across multiple accounts. By broadcasting your S3 event notification(s) to
every SQS queue, you reduce the risk of losing notifications and data after
failover.

Note

If you already use SNS, migration is not necessary. Instead, follow the usual
steps to configure automation with SNS for secondary directory tables or auto-
ingest pipes before failover.

  * [Configure automated refresh for directory tables on secondary stages](account-replication-config.html#label-configure-automated-refresh-secondary-directory-tables)

  * [Configure notifications for secondary auto-ingest pipes](account-replication-config.html#label-configure-notifications-secondary-pipes)

### Prerequisites¶

To migrate, you must meet the following conditions:

  * You have already set up one or more event notifications for your S3 bucket. For instructions, see the topic for your use case:

    * [Refreshing Directory Tables Automatically for Amazon S3: Creating a New S3 Event Notification](data-load-dirtables-auto-s3.html#label-data-load-dirtables-auto-s3-option-1)

    * [Creating a New S3 Event Notification to Automate Snowpipe](data-load-snowpipe-auto-s3.html#label-data-load-snowpipe-auto-s3-option-1)

  * You have already created a replication or failover group in a target account that includes a stage with a directory table or a pipe.

### Migrate to an SNS Topic¶

  1. Create an SNS topic in your AWS account. For instructions, see [Creating an Amazon SNS topic](https://docs.aws.amazon.com/sns/latest/dg/sns-create-topic.html) in the AWS SNS documentation.

  2. Subscribe your target destinations (for example, other SQS queues or AWS Lambda workloads) for your S3 event notification(s) to your SNS topic. SNS publishes event notifications for your bucket to all subscribers to the topic. For instructions, see the [AWS SNS documentation](https://docs.aws.amazon.com/sns/latest/dg/sns-create-subscribe-endpoint-to-topic.html).

  3. Update the access policy for your topic with the following permissions:

     * Allow the Snowflake IAM user to subscribe the SQS queue that is in your _target_ account to your topic.

     * Allow Amazon S3 to publish event notifications from your bucket to the SNS topic.

For instructions, see [Step 1: Subscribe the Snowflake SQS Queue to the SNS
Topic](data-load-snowpipe-auto-s3.html#label-create-sns-topic-subscription).

  4. In your target Snowflake account, call the [SYSTEM$CONVERT_PIPES_SQS_TO_SNS](../sql-reference/functions/system_convert_pipes_sqs_to_sns) function. The function subscribes the SQS queue in your _target_ account to your SNS topic without interrupting metadata synchronization or ingestion work.

Specify your S3 bucket name and SNS topic ARN.

    
        SELECT SYSTEM$CONVERT_PIPES_SQS_TO_SNS('s3_mybucket', 'arn:aws:sns:us-west-2:001234567890:MySNSTopic')
    

Copy

  5. Update your S3 event notifications to use your SNS topic as a destination. For instructions, see the [Amazon S3 User Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/enable-event-notifications.html).

After you complete these steps, the SQS queue automatically unbinds from your
S3 event notification(s). All of the directory tables and pipes that use the
specified S3 bucket will start using SNS as the source of notifications.

