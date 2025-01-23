# Introduction to Streams and Tasks¶  
  
Snowflake supports continuous data pipelines with Streams and Tasks:

Streams:

    

A _stream_ object records the delta of change data capture (CDC) information
for a table (such as a staging table), including inserts and other data
manipulation language (DML) changes. A stream allows querying and consuming a
set of changes to a table, at the row level, between two transactional points
of time.

In a continuous data pipeline, table streams record when staging tables and
any downstream tables are populated with data from business applications using
continuous data loading and are ready for further processing using SQL
statements.

For more information, see [Introduction to Streams](streams-intro).

Tasks:

    

A _task_ object runs a SQL statement, which can include calls to stored
procedures. Tasks can run on a schedule or based on a trigger that you define,
such as the arrival of data. You can use task graphs to chain tasks together,
definining directed acyclic graphs (DAGs) to support more complex periodic
processing. For more information, see [Introduction to tasks](tasks-intro) and
[Manage task dependencies with task graphs](tasks-graphs).

Combining tasks with table streams is a convenient and powerful way to
continuously process new or changed data. A task can transform new or changed
rows that a stream surfaces using [SYSTEM$STREAM_HAS_DATA](../sql-
reference/functions/system_stream_has_data). Each time a task runs, it can
either consume the change data or skip the current run if no change data
exists.

For other continuous data pipeline features, see:

  * Continuous data loading with [Snowpipe](data-load-snowpipe-intro), [Snowpipe Streaming](data-load-snowpipe-streaming-overview), or [Snowflake Connector for Kafka](kafka-connector).

  * Continuous data transformation with [Dynamic tables](dynamic-tables-intro).

