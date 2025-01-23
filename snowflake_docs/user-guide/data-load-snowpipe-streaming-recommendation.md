# Snowpipe Streaming best practices¶

## Cost optimization¶

As a best practice, we recommend calling the API with fewer Snowpipe Streaming
clients that write more data per second. Use a Java or Scala application to
aggregate data from multiple sources, such as IoT devices or sensors, and then
use the Snowflake Ingest SDK to call the API to load data at higher flow
rates. The API efficiently aggregates data across multiple target tables in an
account.

A single Snowpipe Streaming client can open multiple channels to send data,
but the client cost is only charged per active client. The number of channels
does not affect the client cost. Therefore, we recommend using multiple
channels per client for performance and cost optimization.

Using the same tables for both batch and streaming ingestion can also result
in reduced Snowpipe Streaming compute costs due to pre-empted file migration
operations. If [Automatic Clustering](tables-auto-reclustering) is also
enabled on the same table that Snowpipe Streaming is inserting into, compute
costs for file migration might be reduced. The clustering operation will
optimize and migrate data in the same transaction.

## Performance recommendations¶

For optimal performance in high-throughput deployments, we recommend the
following actions:

  * If you are loading multiple rows, using `insertRows` will be more efficient and cost effective than calling `insertRow` multiple times because less time is spent on locks.

    * Keep the size of each row batch passed to `insertRows` below 16 MB compressed.

    * The optimal size of row batches is between 10-16 MB.

  * Pass values for the TIME, DATE, and all TIMESTAMP columns as one of the [supported types](data-load-snowpipe-streaming-overview.html#label-snowpipe-streaming-supported-java-data-types) from the `java.time` package.

  * When creating a channel using `OpenChannelRequest.builder`, set the `OnErrorOption` to `OnErrorOption.CONTINUE`, and manually check the return value from `insertRows` for potential ingestion errors. This approach currently leads to a better performance than relying on exceptions thrown when `OnErrorOption.ABORT` is used.

  * When setting the default log level to DEBUG, make sure that the following loggers keep logging on INFO: their DEBUG output is very verbose, which can lead to a significant performance degradation.

>     * `net.snowflake.ingest.internal.apache.parquet`
>
>     * `org.apache.parquet`

  * Channels should be long lived when a client is actively inserting data and should be reused because offset token information is retained. Do not close channels after inserting data because data inside the channels is automatically flushed based on the time configured in `MAX_CLIENT_LAG`.

## Latency recommendations¶

With Snowflake Ingest SDK versions 2.0.4 and later, you can use
`MAX_CLIENT_LAG` to configure the data flush latency. By default, Snowpipe
Streaming flushes data every 1 second for standard Snowflake tables (non-
Apache Iceberg™). The `MAX_CLIENT_LAG` configuration lets you override that
and set it to your desired flush latency from 1 second to 10 minutes.

For the low-throughput scenarios where not much data is being generated, you
might only be sending 1 row or 1 KB of data every second. This can result in
longer query compilation time where lots of small partitions must be resolved
to return your query results, especially when the query is triggered before
the migration process compacts the partitions. Setting the `MAX_CLIENT_LAG`
higher allows Snowpipe Streaming to buffer the inserted rows for the
configured amount of time and create better sized partitions. This helps with
query performance and migration significantly.

Therefore, set `MAX_CLIENT_LAG` as high as your target latency allows. For
example, if you have a task that runs every 1 minute to merge or transform
your streamed data, it would be optimal to set `MAX_CLIENT_LAG` to 50 or 55
seconds.

For streaming to Snowflake-managed Iceberg tables (supported by Snowflake
Ingest SDK versions 3.0.0 and later), the default `MAX_CLIENT_LAG` is 30
seconds to ensure optimized Parquet files. You can set the property to a lower
value, but we recommend _not_ doing this unless there is a significantly high
throughput.

