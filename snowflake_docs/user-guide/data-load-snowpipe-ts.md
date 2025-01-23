# Troubleshooting Snowpipe¶

This topic describes a methodical approach to troubleshooting issues with
loading data using Snowpipe.

The steps to troubleshoot issues with Snowpipe differ depending on the
workflow used to load data files.

## Automatically loading data using Cloud Storage event notifications¶

### Error notifications¶

Configure error notifications for Snowpipe. When Snowpipe encounters errors
during a load, the feature pushes a notification to a configured cloud
messaging service, enabling analysis of your data files. For more information,
see [Snowpipe error notifications](data-load-snowpipe-errors).

### General troubleshooting steps¶

Complete the following steps to identify the cause of most issues preventing
the automatic loading of files.

#### Step 1: Check the pipe status¶

Retrieve the current status of the pipe. The results are displayed in JSON
format. For information, see [SYSTEM$PIPE_STATUS](../sql-
reference/functions/system_pipe_status).

Check the following values:

> `lastReceivedMessageTimestamp`
>  
>
> Specifies the timestamp of the last event message received from the message
> queue. Note that this message might not apply to the specific pipe, e.g., if
> the path associated with the message does not match the path in the pipe
> definition. In addition, only messages triggered by created data objects are
> consumed by auto-ingest pipes.
>
> If the timestamp is earlier than expected, this likely indicates an issue
> with either the service configuration (i.e. Amazon SQS or Amazon SNS, or
> Azure Event Grid) or the service itself. If the field is empty, verify your
> service configuration settings. If field contains a timestamp but it is
> earlier than expected, verify whether any settings were changed in your
> service configuration.
>
> `lastForwardedMessageTimestamp`
>  
>
> Specifies the timestamp of the last “create object” event message with a
> matching path that was forwarded to the pipe.
>
> If event messages are getting received from the message queue but are not
> forwarded to the pipe, then there is likely a mismatch between the blob
> storage path where the new data files are created and the combined path
> specified in the Snowflake stage and pipe definitions. Verify any paths
> specified in the stage and pipe definitions. Note that a path specified in
> the pipe definition is appended to any path in the stage definition.

#### Step 2. View the COPY history for the table¶

If event messages are getting received and forwarded, then query the load
activity history for the target table. For information, see
[COPY_HISTORY](../sql-reference/functions/copy_history).

The `STATUS` column indicates whether a particular set of files was loaded,
partially loaded, or failed to load. The `FIRST_ERROR_MESSAGE` column provides
a reason when an attempt partially loaded or failed.

Note that if a set of files has multiple issues, the `FIRST_ERROR_MESSAGE`
column only indicates the first error encountered. To view all errors in the
files, execute a [COPY INTO <table>](../sql-reference/sql/copy-into-table)
statement with the VALIDATION_MODE copy option set to `RETURN_ALL_ERRORS`. The
VALIDATION_MODE copy option instructs a COPY statement to validate the data to
be loaded and return results based on the validation option specified. No data
is loaded when this copy option is specified. In the statement, reference the
set of files you had attempted to load using Snowpipe. For more information
about the copy option, see [COPY INTO <table>](../sql-reference/sql/copy-into-
table).

If the COPY_HISTORY output does not include a set of expected files, query an
earlier time period. If the files were duplicates of earlier files, the load
history might have recorded the activity when the attempt to load the original
files was made.

#### Step 3: Validate the data files¶

If the load operation encounters errors in the data files, the COPY_HISTORY
table function describes the first error encountered in each file. To validate
the data files, query the [VALIDATE_PIPE_LOAD](../sql-
reference/functions/validate_pipe_load) function.

### Files generated in Microsoft Azure Data Lake Storage Gen2 storage not
loaded¶

Currently, some third-party clients do not call `FlushWithClose` in the ADLS
Gen 2 REST API. This step is necessary to trigger events that notify Snowpipe
to load the files. Try calling the REST API manually to trigger Snowpipe to
load these files.

For more information about the `Flush` method with the `close` argument, see
<https://docs.microsoft.com/en-
us/dotnet/api/azure.storage.files.datalake.datalakefileclient.flush>. For
additional REST API reference information about the load for the `close`
parameter, see <https://docs.microsoft.com/en-
us/rest/api/storageservices/datalakestoragegen2/path/update>.

### Snowpipe stops loading files after Amazon SNS topic subscription is
deleted¶

The first time a user creates a pipe object that references a specific Amazon
Simple Notification Service (SNS) topic, Snowflake subscribes a Snowflake-
owned Amazon Simple Queue Service (SQS) queue to the topic. If an AWS
administrator deletes the SQS subscription to the SNS topic, any pipe that
references the topic no longer receives event messages from Amazon S3.

To resolve the issue:

  1. Wait 72 hours from the time when the SNS topic subscription was deleted.

After 72 hours, Amazon SNS clears the deleted subscription. For more
information, see the [Amazon SNS
documentation](https://aws.amazon.com/premiumsupport/knowledge-center/sns-
cross-account-subscription/).

  2. Recreate any pipes that reference the topic (using CREATE OR REPLACE PIPE). Reference the same SNS topic in the pipe definition. For instructions, see [Step 3: Create a pipe with auto-ingest enabled](data-load-snowpipe-auto-s3.html#label-create-pipe-auto-ingest-s3).

All pipes that worked prior to the deletion of the SNS topic subscription
should now begin to receive event messages from S3 again.

To circumvent the 72-hour delay, you can create a SNS topic with a different
name. Recreate any pipes that reference the topic using the CREATE OR REPLACE
PIPE command, and specify the new topic name.

### Loads from Google Cloud Storage delayed or files missed¶

When automatic data loading from Google Cloud Storage (GCS) using Pub/Sub
messages is configured, the event message for only a single staged file could
be read. Alternatively, the data loads from GCS could be delayed from between
several minutes and one day or longer. In general, either issue is caused when
a GCS administrator has not granted the Snowflake service account the
`Monitoring Viewer` role.

For instructions, see “Step 2: Grant Snowflake Access to the Pub/Sub
Subscription” in [Configuring secure access to Cloud Storage](data-load-
snowpipe-auto-gcs.html#label-snowpipe-grant-snowflake-access-to-pubsub-
subscription).

## Calling Snowpipe REST endpoints to load data¶

### Error notifications¶

The support for Snowpipe error notifications is available for Snowflake
accounts hosted on Amazon Web Services (AWS). Errors encountered during a data
load trigger notifications that enable analysis of your data files. For more
information, see [Snowpipe error notifications](data-load-snowpipe-errors).

### General troubleshooting steps¶

Complete the following steps to identify the cause of most issues preventing
the loading of files.

#### Step 1: Checking authentication issues¶

The Snowpipe REST endpoints use key pair authentication with JSON Web Token
(JWT).

The Python/Java ingest SDKs generate the JWT for you. When calling the REST
API directly, you need to generate them. If no JWT token is provided in the
request, error `400` is returned by the REST endpoint. If an invalid token is
provided, an error similar to the following is returned:

    
    
    snowflake.ingest.error.IngestResponseError: Http Error: 401, Vender Code: 390144, Message: JWT token is invalid.
    

Copy

#### Step 2. Viewing the COPY history for the table¶

Query the load activity history for a table, including any attempted data
loads using Snowpipe. For information, see [COPY_HISTORY](../sql-
reference/functions/copy_history). The `STATUS` column indicates whether a
particular set of files was loaded, partially loaded, or failed to load. The
`FIRST_ERROR_MESSAGE` column provides a reason when an attempt partially
loaded or failed.

Note that if a set of files has multiple issues, the `FIRST_ERROR_MESSAGE`
column only indicates the first error encountered. To view all errors in the
files, execute a [COPY INTO <table>](../sql-reference/sql/copy-into-table)
statement with the VALIDATION_MODE copy option set to `RETURN_ALL_ERRORS`. The
VALIDATION_MODE copy option instructs a COPY statement to validate the data to
be loaded and return results based on the validation option specified. No data
is loaded when this copy option is specified. In the statement, reference the
set of files you had attempted to load using Snowpipe. For more information
about the copy option, see [COPY INTO <table>](../sql-reference/sql/copy-into-
table).

#### Step 3: Checking the pipe status¶

If the COPY_HISTORY table function returns 0 results for the data load you are
investigating, retrieve the current state of the pipe. The results are
displayed in JSON format. For information, see [SYSTEM$PIPE_STATUS](../sql-
reference/functions/system_pipe_status).

The `executionState` key identifies the execution state of the pipe. For
example, `PAUSED` indicates the pipe is currently paused. The pipe owner could
resume running the pipe using [ALTER PIPE](../sql-reference/sql/alter-pipe).

If the `executionState` value indicates an issue with starting the pipe, check
the `error` key for more information.

#### Step 4: Validate the data files¶

If the load operation encounters errors in the data files, the COPY_HISTORY
table function describes the first error encountered in each file. To validate
the data files, query the [VALIDATE_PIPE_LOAD](../sql-
reference/functions/validate_pipe_load) function.

## Other issues¶

### Set of files not loaded¶

#### Missing COPY_HISTORY record for the load¶

Check whether the COPY INTO _< table>_ statement in the pipe includes the
PATTERN clause. If so, verify whether the regular expression specified as the
PATTERN value is filtering out all of the staged files to load.

To modify the PATTERN value, it is necessary to recreate the pipe using the
`CREATE OR REPLACE PIPE` syntax.

For more information, see [CREATE PIPE](../sql-reference/sql/create-pipe).

#### COPY_HISTORY record indicates unloaded subset of files¶

If the COPY_HISTORY function output indicates a subset of files was not
loaded, you may try to “refresh” the pipe.

This situation can arise in any of the following situations:

  * The external stage was previously used to bulk load data using the COPY INTO _table_ command.

  * **REST API:**

    * External event-driven functionality is used to call the REST APIs, and a backlog of data files already existed in the external stage before the events were configured.

  * **Auto-ingest:**

    * A backlog of data files already existed in the external stage before event notifications were configured.

    * An event notification failure prevented a set of files from getting queued.

To load the data files in your external stage using the configured pipe,
execute a [ALTER PIPE … REFRESH](../sql-reference/sql/alter-pipe) statement.

### Duplicate data in target tables¶

Compare the COPY INTO _< table>_ statements in the definitions of all pipes in
the account by executing [SHOW PIPES](../sql-reference/sql/show-pipes) or by
querying either the [PIPES](../sql-reference/account-usage/pipes) view in
Account Usage or the [PIPES](../sql-reference/info-schema/pipes) view in the
Information Schema. If multiple pipes reference the same cloud storage
location in the COPY INTO _< table>_ statements, verify that the directory
paths do not overlap. Otherwise, multiple pipes could load the same set of
data files into the target tables. For example, this situation can occur when
multiple pipe definitions reference the same storage location with different
levels of granularity, such as `<storage_location>/path1/` and
`<storage_location>/path1/path2/`. In this example, if files are staged in
`<storage_location>/path1/path2/`, both pipes would load a copy of the files.

### Unable to reload modified data, modified data loaded unintentionally¶

Snowflake uses file loading metadata to prevent reloading the same files (and
duplicating data) in a table. Snowpipe prevents loading files with the same
name even if they were later modified (i.e. have a different eTag).

The file loading metadata is associated with the pipe object rather than the
table. As a result:

  * Staged files with the same name as files that were already loaded are ignored, even if they have been modified, e.g. if new rows were added or errors in the file were corrected.

  * Truncating the table using the [TRUNCATE TABLE](../sql-reference/sql/truncate-table) command does not delete the Snowpipe file loading metadata.

However, note that pipes only maintain the load history metadata for 14 days.
Therefore:

Files modified and staged again within 14 days:

    

Snowpipe ignores modified files that are staged again. To reload modified data
files, it is currently necessary to recreate the pipe object using the `CREATE
OR REPLACE PIPE` syntax.

The following example recreates the `mypipe` pipe based on the example in Step
1 of [Preparing to load data using the Snowpipe REST API](data-load-snowpipe-
rest-gs):

    
    
    create or replace pipe mypipe as copy into mytable from @mystage;
    

Copy

Files modified and staged again after 14 days:

    

Snowpipe loads the data again, potentially resulting in duplicate records in
the target table.

In addition, duplicate records can be loaded into the target table if [COPY
INTO <table>](../sql-reference/sql/copy-into-table) statements are executed
that reference the same bucket/container, path, and target table as in your
active Snowpipe loads. The load histories for the COPY command and Snowpipe
are stored separately in Snowflake. After you have loaded any historic staged
data, if you need to load data manually using the pipe configuration, execute
an ALTER PIPE … REFRESH statement. See Set of Files Not Loaded in this topic
for more information.

### Load times inserted using CURRENT_TIMESTAMP earlier than LOAD_TIME values
in COPY_HISTORY view¶

Table designers may add a timestamp column that inserts the current timestamp
as the default value as records are loaded into a table. The intent is to
capture the time when each record was loaded into the table; however, the
timestamps are earlier than the LOAD_TIME column values returned by the
[COPY_HISTORY function](../sql-reference/functions/copy_history) (Information
Schema) or the [COPY_HISTORY view](../sql-reference/account-
usage/copy_history) (Account Usage). The reason is,
[CURRENT_TIMESTAMP](../sql-reference/functions/current_timestamp) is evaluated
when the load operation is compiled in cloud services rather than when the
record is inserted into the table (i.e. when the transaction for the load
operation is committed).

Note

We currently do not recommend using the following functions in the
`_copy_statement_` for Snowpipe:

  * CURRENT_DATE

  * CURRENT_TIME

  * CURRENT_TIMESTAMP

  * GETDATE

  * LOCALTIME

  * LOCALTIMESTAMP

  * SYSDATE

  * SYSTIMESTAMP

It is a known issue that the time values inserted using these functions can be
a few hours earlier than the LOAD_TIME values returned by the [COPY_HISTORY
function](../sql-reference/functions/copy_history) or the [COPY_HISTORY
view](../sql-reference/account-usage/copy_history).

Use the copy option `INCLUDE_METADATA` with
[METADATA$START_SCAN_TIME](querying-metadata) instead, which provides a more
accurate representation of record loading. For more information, see [CREATE
PIPE examples](../sql-reference/sql/create-pipe.html#label-create-pipe-
examples).

### Error: Integration `{0}` associated with the stage `{1}` cannot be found¶

    
    
    003139=SQL compilation error:\nIntegration ''{0}'' associated with the stage ''{1}'' cannot be found.
    

Copy

This error can occur when the association between the external stage and the
storage integration linked to the stage has been broken. This happens when the
storage integration object has been recreated (using [CREATE OR REPLACE
STORAGE INTEGRATION](../sql-reference/sql/create-storage-integration)). A
stage links to a storage integration using a hidden ID rather than the name of
the storage integration. Behind the scenes, the CREATE OR REPLACE syntax drops
the object and recreates it with a different hidden ID.

If you must recreate a storage integration after it has been linked to one or
more stages, you must reestablish the association between each stage and the
storage integration by executing [ALTER STAGE](../sql-reference/sql/alter-
stage) `_stage_name_` SET STORAGE_INTEGRATION = `_storage_integration_name_`,
where:

  * `_stage_name_` is the name of the stage.

  * `_storage_integration_name_` is the name of the storage integration.

### Errors for Snowpipe referencing government regions¶

You may get an error when Snowpipe referencing a bucket in a government region
while the account is in a commercial region. Note that the government regions
of the cloud providers do not allow event notifications to be sent to or from
other commercial regions. For more information, see [AWS GovCloud
(US)](https://docs.aws.amazon.com/govcloud-
us/latest/UserGuide/govcloud-s3.html) and [Azure
Government](https://learn.microsoft.com/en-us/azure/azure-government/).

