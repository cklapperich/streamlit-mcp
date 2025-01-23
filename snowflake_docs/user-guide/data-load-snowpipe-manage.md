# Managing Snowpipe¶

This topic describes the administrative tasks associated with managing
Snowpipe.

## Deleting staged files after Snowpipe loads the data¶

Pipe objects do not support the PURGE copy option. Snowpipe cannot delete
staged files automatically when the data is successfully loaded into tables.

To remove staged files that you no longer need, we recommend periodically
executing the [REMOVE](../sql-reference/sql/remove) command to delete the
files.

Alternatively, configure any lifecycle management features provided by your
cloud storage service provider.

## Loading historic data¶

Note

The information in this section pertains to automated data loads using event
notifications. Calls to the Snowpipe REST API can load historic data without
the need for additional steps.

An [ALTER PIPE … REFRESH](../sql-reference/sql/alter-pipe) statement copies a
set of data files staged within the previous 7 days to the Snowpipe ingest
queue for loading into the target table. If you want to load data from files
staged earlier, we recommend the following steps:

  1. Load the historic data into the target table by executing a [COPY INTO <table>](../sql-reference/sql/copy-into-table) statement.

  2. Configure automatic data loads using Snowpipe with event notifications. Files that are newly staged will trigger event notifications for ingestion into the target table. Because the historic data files do not trigger event notifications, they are not loaded twice.

For instructions, see:

Amazon S3:

    

[Automating Snowpipe for Amazon S3](data-load-snowpipe-auto-s3)

Google Cloud Storage:

    

[Automating Snowpipe for Google Cloud Storage](data-load-snowpipe-auto-gcs)

Microsoft Azure:

    

[Automating Snowpipe for Microsoft Azure Blob Storage](data-load-snowpipe-
auto-azure)

  3. Execute an ALTER PIPE … REFRESH statement to queue any files staged in-between Steps 1 and 2. The statement checks the load history for both the target table and the pipe to ensure the same files are not loaded twice.

## Recreating pipes¶

Recreating a pipe (using a [CREATE OR REPLACE PIPE](../sql-
reference/sql/create-pipe) statement) is necessary to modify most pipe
properties.

This section describes considerations and best practices to follow when
recreating pipes.

### Recreating pipes for automated data loads¶

When recreating a pipe that automates data loads using event notifications, we
recommend that you complete the following steps:

  1. Pause the pipe (using [ALTER PIPE … SET PIPE_EXECUTION_PAUSED = true](../sql-reference/sql/alter-pipe)).

  2. Query the [SYSTEM$PIPE_STATUS](../sql-reference/functions/system_pipe_status) function and verify that the pipe execution state is `PAUSED`.

  3. Recreate the pipe (using CREATE OR REPLACE PIPE).

  4. Pause the pipe again.

  5. Review the configuration steps for your cloud messaging service to ensure the settings are still accurate:

     * [Automating Snowpipe for Amazon S3](data-load-snowpipe-auto-s3)

     * [Automating Snowpipe for Google Cloud Storage](data-load-snowpipe-auto-gcs)

     * [Automating Snowpipe for Microsoft Azure Blob Storage](data-load-snowpipe-auto-azure)

  6. Resume the pipe (using ALTER PIPE … SET PIPE_EXECUTION_PAUSED = false).

  7. Query the SYSTEM$PIPE_STATUS function again and verify that the pipe execution state is `RUNNING`.

### Load history¶

The load history for Snowpipe operations is stored in the metadata of the pipe
object. When a pipe is recreated, the load history is dropped. In general,
this condition only affects users if they subsequently execute an [ALTER PIPE
… REFRESH](../sql-reference/sql/alter-pipe) statement on the pipe. Doing so
could load duplicate data from staged files in the storage location for the
pipe if the data was already loaded successfully and the files were not
deleted subsequently.

## Changing the cloud parameters of the referenced stage¶

The cloud parameters of an external stage include the following:

  * `URL`

  * `STORAGE_INTEGRATION`

  * `ENCRYPTION`

After Snowpipe has been configured successfully, if you need to modify any of
the cloud parameters of the referenced stage, you must recreate the pipe.

Warning

Modifying the `URL` parameter of a stage can cause any reliant pipes that
leverage cloud messaging to trigger data loads (i.e. where `AUTO_INGEST =
TRUE`) to stop working.

## Transferring pipe ownership¶

Complete the following steps to transfer ownership of a pipe:

  1. Set the [PIPE_EXECUTION_PAUSED](../sql-reference/parameters.html#label-pipe-execution-paused) parameter to TRUE.

This parameter enables pausing or resuming a pipe. The parameter is supported
at the following levels:

     * Account

     * Schema

     * Pipe

At the pipe level, the object owner (or a parent role in a role hierarchy) can
set the parameter to pause or resume an individual pipe.

An account administrator (user with the ACCOUNTADMIN role) can set this
parameter at the account level to pause or resume all pipes in the account.
Likewise, a user with the MODIFY privilege on the schema can pause or resume
pipes at the schema level. Note that this larger domain control only affects
pipes for which the parameter was not already set at a lower level; e.g., by
the owner at the object level.

  2. Transfer ownership of the pipe using [GRANT OWNERSHIP](../sql-reference/sql/grant-ownership).

  3. Force the pipe to resume (using [SYSTEM$PIPE_FORCE_RESUME](../sql-reference/functions/system_pipe_force_resume)).

This step allows the new owner to evaluate the pipe status and determine how
many data files are waiting to be loaded using [SYSTEM$PIPE_STATUS](../sql-
reference/functions/system_pipe_status). We recommend verifying that only
files approved for loading into the target table are queued.

## Modifying the COPY statement in a pipe definition¶

Complete the following steps to modify the COPY statement in a pipe
definition; for example, when columns are added to the target table.

To execute the commands in this section, the current role for the user must
have the OWNERSHIP privilege on the pipe.

  1. Pause the pipe (using [ALTER PIPE … SET PIPE_EXECUTION_PAUSED=true](../sql-reference/sql/alter-pipe)).

  2. Query the [SYSTEM$PIPE_STATUS](../sql-reference/functions/system_pipe_status) function and verify that the pipe execution state is `PAUSED` and the pending file count is 0.

  3. Recreate the pipe to change the COPY statement in the definition. Choose either of the following options:

     * Drop the pipe (using [DROP PIPE](../sql-reference/sql/drop-pipe)) and create it (using [CREATE PIPE](../sql-reference/sql/create-pipe)).

     * Recreate the pipe (using the [CREATE OR REPLACE PIPE](../sql-reference/sql/create-pipe) syntax). Internally, the pipe is dropped and created.

  4. Pause the pipe again.

  5. Review the configuration steps for your cloud messaging service to ensure the settings are still accurate:

     * [Automating Snowpipe for Amazon S3](data-load-snowpipe-auto-s3)

     * [Automating Snowpipe for Google Cloud Storage](data-load-snowpipe-auto-gcs)

     * [Automating Snowpipe for Microsoft Azure Blob Storage](data-load-snowpipe-auto-azure)

  6. Resume the pipe (using ALTER PIPE … SET PIPE_EXECUTION_PAUSED = false).

  7. Query the SYSTEM$PIPE_STATUS function again and verify that the pipe execution state is `RUNNING`.

Note

The file loading metadata is associated with the pipe object rather than the
table. Recreating the pipe removes the history of files loaded. Ensure that
files already loaded by Snowpipe are not accidentally resubmitted to the pipe
and loaded into the target table again. To view the query history for a table,
query the [COPY_HISTORY](../sql-reference/functions/copy_history) function.

## Resuming a stale pipe¶

Note

This section only pertains to pipe objects that leverage cloud messaging to
trigger data loads (i.e. where `AUTO_INGEST = TRUE` in the pipe definition).

When a pipe is paused, event messages received for the pipe enter a limited
retention period. The period is 14 days by default. If a pipe is paused for
longer than 14 days, it is considered stale.

To resume a stale pipe, a qualified role must call the
[SYSTEM$PIPE_FORCE_RESUME](../sql-
reference/functions/system_pipe_force_resume) function and input the
STALENESS_CHECK_OVERRIDE argument. This argument indicates an understanding
that the role is resuming a stale pipe.

For example, resume the stale `stalepipe1` pipe in the `mydb.myschema`
database and schema:

    
    
    SELECT SYSTEM$PIPE_FORCE_RESUME('mydb.myschema.stalepipe1','staleness_check_override');
    

Copy

While the stale pipe was paused, if ownership of the pipe was transferred to
another role, then resuming the pipe requires the additional
OWNERSHIP_TRANSFER_CHECK_OVERRIDE argument. For example, resume the stale
`stalepipe2` pipe in the `mydb.myschema` database and schema, which
transferred to a new role:

    
    
    SELECT SYSTEM$PIPE_FORCE_RESUME('mydb.myschema.stalepipe1','staleness_check_override, ownership_transfer_check_override');
    

Copy

As an event notification received while a pipe is paused reaches the end of
the limited retention period, Snowflake schedules it to be dropped from the
internal metadata. If the pipe is later resumed, Snowpipe processes these
older notifications on a best effort basis. Snowflake cannot guarantee that
they are processed.

For example, if a pipe is resumed 15 days after it was paused, Snowpipe
generally skips any event notifications that were received on the first day
the pipe was paused (i.e. that are now more than 14 days old). If the pipe is
resumed 16 days after it was paused, Snowpipe generally skips any event
notifications that were received on the first and second days after the pipe
was paused. And so on.

## Managing pipes in Snowsight¶

You can perform basic management tasks for pipes in Snowsight.

  1. Sign in to Snowsight.

  2. In the navigation menu, select Data » Databases.

  3. Locate the database and schema that contain the pipe.

  4. Select the pipe to open the details.

Note

To view details about the pipe, you must use a role with the MONITOR or
OWNERSHIP privilege on the pipe and the USAGE privilege on both the database
and schema that contain the pipe. See [Pipe privileges](security-access-
control-privileges.html#label-access-control-privileges-pipe) for more
details.

When you view pipe details in Snowsight, you can review basic information
about your pipe, such as the owner role and creation date.

You can also perform the following basic management tasks for a pipe in
Snowsight:

  * To add a comment to the pipe, select [![More options](../_images/snowsight-worksheet-explorer-ellipsis.png)](../_images/snowsight-worksheet-explorer-ellipsis.png) » Edit. To edit other properties of a pipe, you must use the [CREATE PIPE](../sql-reference/sql/create-pipe) SQL command to replace the pipe.

  * To drop the pipe, select [![More options](../_images/snowsight-worksheet-explorer-ellipsis.png)](../_images/snowsight-worksheet-explorer-ellipsis.png) » Drop.

  * To transfer ownership of the pipe to another role, select [![More options](../_images/snowsight-worksheet-explorer-ellipsis.png)](../_images/snowsight-worksheet-explorer-ellipsis.png) » Transfer Ownership.

The Details section includes information about the following:

  * Execution status of the pipe, such as whether it is Running, Paused, or something else.

  * The number of files pending in the pipe, if any.

  * The date of last ingestion performed with the pipe, if applicable.

You can also review the pipe definition in the Definition section, or use the
Privileges section to review and manage privileges. For details on managing
privileges, see [Manage object privileges with Snowsight](security-access-
control-configure.html#label-snowsight-manage-object-privileges).

