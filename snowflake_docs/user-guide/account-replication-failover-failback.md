# Failing over account objects¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Business Critical
Feature](intro-editions)

This features requires Business Critical Edition (or higher). To inquire about
upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-
guide/contacting-support).

This topic describes the steps necessary to fail over replicated account
objects across multiple accounts in different [regions](intro-regions) for
disaster recovery.

## Prerequisite requirements¶

  1. Enable replication for a primary failover group in a set of accounts.

  2. Create at least one secondary failover group (i.e. replica) of the primary failover group in one or more accounts and regularly refresh (i.e. synchronize) the replica with the latest updates to the objects in the failover group.

For instructions, see [Replicating databases and account objects across
multiple accounts](account-replication-config).

## Promoting a target account to serve as the source account¶

To promote a target account to serve as the source account, you must sign in
to the target account you want to promote to serve as the new source account
and execute the [ALTER FAILOVER GROUP … PRIMARY](../sql-reference/sql/alter-
failover-group.html#label-alter-failover-group) command.

### Promote a secondary failover group to primary failover group¶

Note

The example in this section must be executed by a role with the FAILOVER
privilege.

The following example promotes `myaccount2` in the current `myorg`
organization to serve as the source account.

  1. Sign in to target account `myaccount2`.

  2. List failover groups in the account:
    
        SHOW FAILOVER GROUPS;
    

Copy

  3. Execute the following statement for each secondary failover group you want to promote to serve as the primary failover group:
    
        ALTER FAILOVER GROUP myfg PRIMARY;
    

Copy

Note

During a partial outage in your source region, the replication service might
continue to be available and might continue to refresh the secondary failover
groups in target regions.

To ensure data integrity, Snowflake prevents failover if a refresh operation
is in progress. This means you cannot promote a secondary failover group to
serve as the primary if it is being refreshed by a replication operation. The
ALTER FAILOVER GROUP … PRIMARY command returns an error in this scenario.

### Resolving failover statement failure due to an in-progress refresh
operation¶

If there is a refresh operation in progress for the secondary failover group
you are trying to promote, the failover statement results in the following
error:

    
    
    Replication group "<GROUP_NAME>" cannot currently be set as primary because it is being
    refreshed. Either wait for the refresh to finish or cancel the refresh and try again.
    

To successfully fail over, you must complete the following steps.

  1. Select and complete one of the following options:

Important

Suspending a refresh operation in the SECONDARY_DOWNLOADING_METADATA or
SECONDARY_DOWNLOADING_DATA phase might result in an inconsistent state on the
target account. For more information, see View the current phase of an in-
progress refresh operation.

    1. Suspend future refresh operations for the failover group. If there is an in-progress refresh operation, you must wait for it to complete before you can failover:
        
                ALTER FAILOVER GROUP myfg SUSPEND;
        

Copy

    2. Suspend future refresh operations _and_ cancel a scheduled refresh operation that is currently in progress (if there is one).

If the in-progress refresh operation was manually triggered, see Cancel an in-
progress refresh operation that wasn’t automatically scheduled.

        
                ALTER FAILOVER GROUP myfg SUSPEND IMMEDIATE;
        

Copy

Note

You might experience a slight delay between the time that the statement
returns and the time that the cancellation of the refresh operation is
finished.

  2. Verify no refresh operations are in progress for the failover group `myfg`. The following query should return no results:
    
        SELECT phase_name, start_time, job_uuid
      FROM TABLE(INFORMATION_SCHEMA.REPLICATION_GROUP_REFRESH_HISTORY('myfg'))
      WHERE phase_name <> 'COMPLETED' and phase_name <> 'CANCELED';
    

Copy

To see canceled refresh operations for failover group `myfg`, you can execute
the following statement:

    
        SELECT phase_name, start_time, job_uuid
      FROM TABLE(INFORMATION_SCHEMA.REPLICATION_GROUP_REFRESH_HISTORY('myfg'))
      WHERE phase_name = 'CANCELED';
    

Copy

  3. Now you can promote the secondary failover group `myfg` to primary failover group:
    
        ALTER FAILOVER GROUP myfg PRIMARY;
    

Copy

### Resume scheduled replication in target accounts¶

On failover, scheduled refreshes on all secondary failover groups are
suspended. [ALTER FAILOVER GROUP … RESUME](../sql-reference/sql/alter-
failover-group) must be executed in each **target account** with a secondary
failover group to resume automatic refreshes.

    
    
    ALTER FAILOVER GROUP myfg RESUME;
    

Copy

## View the current phase of an in-progress refresh operation¶

A refresh operation can be safely canceled during most phases of the refresh
operation. However, canceling a refresh operation in the
SECONDARY_DOWNLOADING_METADATA or SECONDARY_DOWNLOADING_DATA phase might
result in an inconsistent state on the target account. If the refresh
operation has started one of these phases, it proceeds to completion
regardless of the availability of the source account. Allowing the phase to
complete before you fail over ensures replicas are in a consistent state.
After the replicas are in a consistent state, you can resume or replay your
ingest and transformation pipelines to update the replicas to the current
state.

To view the current phase of an in-progress refresh operation for a failover
group, use the Information Schema [REPLICATION_GROUP_REFRESH_PROGRESS,
REPLICATION_GROUP_REFRESH_PROGRESS_BY_JOB](../sql-
reference/functions/replication_group_refresh_progress) table function.

For example, to view the current phase of an in-progress refresh operation for
failover group `myfg`, execute the following statement:

    
    
    SELECT phase_name, start_time, end_time
      FROM TABLE(
        INFORMATION_SCHEMA.REPLICATION_GROUP_REFRESH_PROGRESS('myfg')
      );
    

Copy

For a list of refresh operations phases, see the [usage notes](../sql-
reference/functions/replication_group_refresh_progress.html#label-replication-
group-refresh-progress-usage-notes) for the function.

## Cancel an in-progress refresh operation that wasn’t automatically
scheduled¶

To cancel an in-progress refresh operation that was not triggered
automatically by a replication schedule, you must use the
[SYSTEM$CANCEL_QUERY](../sql-reference/functions/system_cancel_query)
function:

  1. Find the query ID or JOB_UUID for running refresh operations using one of the following options:

    1. Find the query IDs for all running refresh operations:
        
                SELECT query_id, query_text
          FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY())
          WHERE query_type = 'REFRESH REPLICATION GROUP'
          AND execution_status = 'RUNNING'
          ORDER BY start_time;
        

Copy

Use the QUERY_TEXT column to identify the QUERY_ID for failover group refresh
operations from the list.

    2. Find the JOB_UUID for an in-progress refresh operation for a specific failover group `myfg`:
        
                SELECT phase_name, start_time, job_uuid
          FROM TABLE(INFORMATION_SCHEMA.REPLICATION_GROUP_REFRESH_HISTORY('myfg'))
          WHERE phase_name <> 'COMPLETED' and phase_name <> 'CANCELED';
        

Copy

  2. Cancel the refresh operation using the SYSTEM$CANCEL_QUERY function and the QUERY_ID or JOB_UUID:
    
        SELECT SYSTEM$CANCEL_QUERY('<QUERY_ID | JOB_UUID>');
    

Copy

Returns the following output:

    
        query [<QUERY_ID>] terminated.
    

  3. After you cancel the in-progress refresh operation, continue to the next steps.

## Reopen active channels for Snowpipe Streaming in newly promoted source
account¶

Tables in a primary database that are populated by [Snowpipe Streaming are
replicated](account-replication-considerations.html#label-replication-
snowpipe-streaming) to secondary databases. After failover, reopen active
Snowpipe Streaming channels for tables and re-insert any missing data rows for
the channels:

  1. Reopen active channels for the table by calling the [openChannel](https://javadoc.io/doc/net.snowflake/snowflake-ingest-sdk/latest/net/snowflake/ingest/streaming/SnowflakeStreamingIngestClient.html) API.

  2. Fetch offset tokens:

    1. Call the [getLatestCommittedOffsetToken](https://javadoc.io/doc/net.snowflake/snowflake-ingest-sdk/latest/net/snowflake/ingest/streaming/SnowflakeStreamingIngestChannel.html#getLatestCommittedOffsetToken\(\)) API or

    2. Execute the [SHOW CHANNELS](../sql-reference/sql/show-channels) command to retrieve a list of the active channels of the table.

  3. Re-insert data rows for the channel from the fetched offset tokens.

### Snowpipe Streaming and the Kafka connector¶

If you are using the Kafka connector and Snowpipe Streaming, follow these
steps after failover:

  1. Update the Kafka connector configuration to point to the newly promoted source account.

  2. Execute the SHOW CHANNELS command to retrieve the list of active channels and the offset tokens. Each channel belongs to a single partition in the Kafka topic.

  3. Manually reset offsets in the Kafka Topic for each of those partitions (channels).

  4. Restart the Kafka Connector.

For more information, refer to:

  * [Using Snowflake Connector for Kafka with Snowpipe Streaming](data-load-snowpipe-streaming-kafka).

  * [Replication and Snowpipe Streaming](account-replication-considerations.html#label-replication-snowpipe-streaming).

