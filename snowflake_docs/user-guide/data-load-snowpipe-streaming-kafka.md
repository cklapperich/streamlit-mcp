# Using Snowflake Connector for Kafka with Snowpipe Streaming¶

You can replace Snowpipe with [Snowpipe Streaming](data-load-snowpipe-
streaming-overview) in your data loading chain from Kafka. When the specified
flush buffer threshold (time, memory, or number of messages) is reached, the
connector calls the Snowpipe Streaming API (“API”) to write rows of data to
Snowflake tables, unlike Snowpipe, which writes data from temporary staged
files. This architecture results in lower load latencies with corresponding
lower costs for loading similar volumes of data.

Version 2.0.0 (or later) of the Kafka connector is required for use with
Snowpipe Streaming. The Kafka connector with Snowpipe Streaming includes the
Snowflake Ingest SDK and supports streaming rows from Apache Kafka topics
directly into target tables.

> ![Snowpipe Streaming with Kafka connector](../_images/data-load-snowpipe-
> streaming-kafka.png)

## Minimum required version¶

The minimum required Kafka connector version that supports Snowpipe Streaming
is 2.0.0.

## Kafka configuration properties¶

Save your connection settings in the Kafka connector properties file. For more
information, see [Configuring the Kafka connector](kafka-connector-
install.html#label-kafka-connector-configuration-file).

### Required properties¶

Add or edit your connection settings in the Kafka connector properties file.
For more information, see [Configuring the Kafka connector](kafka-connector-
install.html#label-kafka-connector-configuration-file).

`snowflake.ingestion.method`

    

 _Required only if using the Kafka connector as the streaming ingest client._
Specifies whether to use Snowpipe Streaming or standard Snowpipe to load your
Kafka topic data. The supported values are as follows:

  * `SNOWPIPE_STREAMING`

  * `SNOWPIPE` (default)

No additional settings are required to choose the backend service to queue and
load topic data. Configure additional properties in your Kafka connector
properties file as usual.

`snowflake.role.name`

    

Access control role to use when inserting the rows into the table.

### Client optimization properties¶

`enable.streaming.client.optimization`

    

Specifies whether to enable one-client optimization. This property is
supported by Kafka connector release version 2.1.2 and later. It is enabled by
default.

With one-client optimization, only one client is created for multiple topic
partitions per Kafka connector. This feature can reduce client runtime and
lower migration cost by creating larger files.

Values:

    

  * `true`

  * `false`

Default:

    

`true`

Note that in a high throughput scenario (for example, 50 MB/s per connector),
enabling this property can result in a higher latency or cost. We recommend
that you disable this property for high-throughput scenarios.

### Buffer and polling properties¶

`buffer.flush.time`

    

Number of seconds between buffer flushes; each flush results in insert
operations for the buffered records. The Kafka connector calls the Snowpipe
Streaming API once after each flush.

The minimum value supported for the `buffer.flush.time` property is `1` (in
seconds). For higher average data flow rates, we suggest that you decrease the
default value for improved latency. If cost is a greater concern than latency,
you could increase the buffer flush time. Be careful to flush the Kafka memory
buffer before it becomes full to avoid out-of-memory exceptions.

Values:

    

  * Minimum: `1`

  * Maximum: No upper limit

Default:

    

`10`

Note that Snowpipe Streaming automatically flushes data every one second,
which is different from the buffer flush time for the Kafka connector. After
the Kafka buffer flush time is reached, data will be sent with one second
latency to Snowflake through Snowpipe Streaming. For more information, see
[Snowpipe Streaming latency](data-load-snowpipe-streaming-overview.html#label-
snowpipe-streaming-latency).

`buffer.count.records`

    

Number of records buffered in memory per Kafka partition before ingesting to
Snowflake.

Values:

    

  * Minimum: `1`

  * Maximum: No upper limit

Default:

    

`10000`

`buffer.size.bytes`

    

Cumulative size in bytes of records buffered in memory per the Kafka partition
before they are ingested in Snowflake as data files.

The records are compressed when they are written to data files. As a result,
the size of the records in the buffer may be larger than the size of the data
files created from the records.

Values:

    

  * Minimum: `1`

  * Maximum: No upper limit

Default:

    

`20000000` (20 MB)

`snowflake.streaming.max.client.lag`

    

Specifies how often [Snowflake Ingest
Java](https://github.com/snowflakedb/snowflake-ingest-java) flushes the data
to Snowflake, in seconds.

A low value keeps the latency low, but it might result in a worse query
performance especially when `snowflake.streaming.enable.single.buffer` is
enabled. For more information, see the [recommended latency configurations for
Snowpipe Streaming](data-load-snowpipe-streaming-recommendation.html#label-
snowpipe-streaming-recommendations-latency).

Values:

    

  * Minimum: `1` second

  * Maximum: `600` seconds

Default:

    

`120` seconds for version 3.0.0 or later, `1` second otherwise

`snowflake.streaming.enable.single.buffer`

    

Specifies whether to enable single buffer for Snowpipe Streaming and to skip
buffering data in the connector’s internal buffer.

This property is supported by the Kafka connector version 2.3.1 and later.

Streaming connector uses internal buffer alongside with the one provided by
[Snowflake Ingest Java](https://github.com/snowflakedb/snowflake-ingest-java).
Setting this property to `true` makes Kafka connector skip the internal buffer
in order to achieve lower latency.

Note that setting this property to `true` makes `buffer.flush.time` and
`buffer.count.records` irrelevant.

Values:

    

  * `true`

  * `false`

Default:

    

`true` for version 3.0.0 and later, `false` otherwise

In addition to the Kafka connector properties, note the Kafka consumer
`max.poll.records` property, which controls the maximum number of records
returned by Kafka to Kafka Connect in a single poll. The default value of
`500` can be increased, but be mindful of memory constraints. For more
information about this property, see the documentation for your Kafka package:

  * [Apache Kafka](https://kafka.apache.org/documentation/#consumerconfigs_max.poll.records)

  * [Confluent](https://docs.confluent.io/platform/current/installation/configuration/consumer-configs.html#consumerconfigs_max.poll.records)

### Error handling and DLQ properties¶

`errors.tolerance`

    

Specifies how to handle errors encountered by the Kafka connector:

This property supports the following values:

Values:

    

  * `NONE`: Stop loading data when the first error is encountered.

  * `ALL`: Ignore all errors and continue to load data.

Default:

    

`NONE`

`errors.log.enable`

    

Specifies whether to write error messages to the Kafka Connect log file.

This property supports the following values:

Values:

    

  * `TRUE`: Write error messages.

  * `FALSE`: Do not write error messages.

Default:

    

`FALSE`

`errors.deadletterqueue.topic.name`

    

Specifies the name of the DLQ (dead-letter queue) topic in Kafka for
delivering messages to Kafka that could not be ingested into Snowflake tables.
For more information, see Dead-letter Queues (in this topic).

Values:

    

Custom text string

Default:

    

None

## Exactly-once semantics¶

Exactly-once semantics ensure the delivery of Kafka messages without
duplication or data loss. This delivery guarantee is set by default for the
Kafka connector with Snowpipe Streaming.

The Kafka Connector adopts a one-to-one mapping between partition and channel
and uses two distinct offsets:

>   * Consumer offset: This tracks the most recent offset consumed by the
> consumer and is managed by Kafka.
>
>   * Offset token: This tracks the most recent committed offset in Snowflake
> and is managed by Snowflake.
>
>

Note that the Kafka connector does not always handle missing offsets.
Snowflake expects that all records to have sequentially increasing offsets.
The missing offsets will break the Kafka connector in specific use cases. It
is recommended that you use tombstone records instead of NULL records.

The Kafka connector achieves exactly-once delivery by implementing the
following best practices:

Opening/reopening a channel:

>   * When opening or reopening a channel for a given partition, the Kafka
> Connector uses the latest committed offset token retrieved from Snowflake
> through the `getLatestCommittedOffsetToken` API as the source of truth and
> resets the consumer offset in Kafka accordingly.
>
>   * If the consumer offset is no longer within the data retention period, an
> exception is thrown, and you can determine the appropriate action to take.
>
>   * The only scenario in which the Kafka Connector does not reset the
> consumer offset in Kafka and uses it as the source of truth is when the
> offset token from Snowflake is NULL. In this case, the connector accepts the
> offset sent by Kafka, and the offset token is subsequently updated.
>
>

Processing records:

>   * To ensure an additional layer of safety against non-continuous offsets
> that could arise from potential bugs in Kafka, Snowflake maintains an in-
> memory variable that tracks the latest processed offset. Snowflake only
> accepts rows if the current row’s offset equals the latest processed offset
> plus one, thereby adding an extra layer of protection to ensure that the
> ingestion process is continuous and accurate.
>
>

Dealing with exceptions, failures, crashes recovery:

>   * As part of the recovery process, Snowflake consistently adheres to the
> channel open/reopen logic outlined earlier by reopening the channel and
> resetting the consumer offset with the latest committed offset token. By
> doing this, Snowflake signals Kafka to send the data from the offset value
> that is one greater than the latest committed offset token, which enables
> the resumption of ingestion from the point of failure with no data loss.
>
>

Implementing a retry mechanism:

>   * To account for potential transient issues, Snowflake incorporates a
> retry mechanism in the API calls. Snowflake retries these API calls multiple
> times to increase the chances of success and mitigate the risk of
> intermittent failures affecting the ingestion process.
>
>

Advancing the consumer offset:

>   * At regular intervals, Snowflake advances the consumer offset using the
> latest committed offset token to ensure that the ingestion process is
> continuously aligned with the latest state of data in Snowflake.
>
>

## Converters¶

Snowpipe Streaming supports many community-based converters such as the
following:

  * `io.confluent.connect.avro.AvroConverter`

  * `org.apache.kafka.connect.json.JsonConverter`

  * `io.confluent.connect.protobuf.ProtobufConverter`

  * `io.confluent.connect.json.JsonSchemaConverter`

  * `org.apache.kafka.connect.converters.ByteArrayConverter`

  * `org.apache.kafka.connect.storage.StringConverter`

Other community-based converters may be supported but have not been validated.
Snowflake converters are not supported with Snowpipe Streaming.

## Dead-letter queues¶

The Kafka connector with Snowpipe Streaming supports dead-letter queues (DLQ)
for broken records or records that cannot be processed successfully due to a
failure.

For more information about monitoring, see the Apache Kafka
[documentation](https://kafka.apache.org/documentation/#connect_monitoring).

## Schema detection and schema evolution¶

The Kafka connector with Snowpipe Streaming supports schema detection and
evolution. The structure of tables in Snowflake can be defined and evolved
automatically to support the structure of new Snowpipe Streaming data loaded
by the Kafka connector. To enable schema detection and evolution for the Kafka
connector with Snowpipe Streaming, configure the following Kafka properties:

  * `snowflake.ingestion.method`

  * `snowflake.enable.schematization`

  * `schema.registry.url`

For more information, see [Schema detection and evolution for Kafka connector
with Snowpipe Streaming](data-load-snowpipe-streaming-kafka-schema-detection).

## Estimating ingestion latency¶

To estimate ingestion latency, use the `SnowflakeConnectorPushTime` field in
RECORD_METADATA. This timestamp represents a point in time when a record was
pushed into an Ingest SDK buffer.

For more information about the RECORD_METADATA format, see [Schema of tables
for Kafka topics](kafka-connector-overview.html#label-schema-of-table-for-
snowflake-kafka-connector).

Note

This field **does not** represent when a record became visible in a Snowflake
table, because it doesn’t take into account your configured [Snowpipe
Streaming latency](data-load-snowpipe-streaming-overview.html#label-snowpipe-
streaming-latency).

## Billing and usage¶

For Snowpipe Streaming billing information, see [Snowpipe Streaming
costs](data-load-snowpipe-streaming-billing).

## Limitations¶

For Snowpipe Streaming limitations, see [limitations](data-load-snowpipe-
streaming-overview.html#label-snowpipe-streaming-limitations).

