# Snowpipe Streaming¶

Calling the Snowpipe Streaming API (“API”) prompts the low-latency loading of
streaming data rows using the Snowflake Ingest SDK and your own managed
application code. The streaming ingest API writes rows of data to Snowflake
tables, unlike bulk data loads or Snowpipe, which write data from staged
files. This architecture results in lower load latencies with corresponding
lower costs for loading similar volumes of data, which makes it a powerful
tool for handling real-time data streams.

This topic describes the concepts for custom client applications that call the
API. For related Snowflake Connector for Kafka (“Kafka connector”)
instructions, see [Using Snowflake Connector for Kafka with Snowpipe
Streaming](data-load-snowpipe-streaming-kafka).

## Snowpipe Streaming API versus Snowpipe¶

The API is intended to complement Snowpipe, not replace it. Use the Snowpipe
Streaming API in streaming scenarios where data is streamed via rows (for
example, Apache Kafka topics) instead of written to files. The API fits into
an ingest workflow that includes an existing custom Java application that
produces or receives records. The API removes the need to create files to load
data into Snowflake tables and enables the automatic, continuous loading of
data streams into Snowflake as the data becomes available.

> ![Snowpipe Streaming](../_images/data-load-snowpipe-streaming.png)

The following table describes the differences between Snowpipe Streaming and
Snowpipe:

Category | Snowpipe Streaming | Snowpipe  
---|---|---  
Form of data to load | Rows | Files. If your existing data pipeline generates files in blob storage, we recommend using Snowpipe instead of the API.  
Third-party software requirements | Custom Java application code wrapper for the Snowflake Ingest SDK | None  
Data ordering | Ordered insertions within each channel | Not supported. Snowpipe can load data from files in an order different from the file creation timestamps in cloud storage.  
Load history | Load history recorded in [SNOWPIPE_STREAMING_FILE_MIGRATION_HISTORY view](../sql-reference/account-usage/snowpipe_streaming_file_migration_history) (Account Usage) | Load history recorded in [LOAD_HISTORY view](../sql-reference/account-usage/load_history) (Account Usage) and [COPY_HISTORY function](../sql-reference/functions/copy_history) (Information Schema)  
Pipe object | Does not require a pipe object: the API writes records directly to target tables. | Requires a pipe object that queues and loads staged file data into target tables.  
  
## Software requirements¶

### Java SDK¶

The Snowpipe Streaming service is currently implemented as a set of APIs for
the Snowflake Ingest SDK. The SDK is available for download from the [Maven
Central
Repository](https://mvnrepository.com/artifact/net.snowflake/snowflake-ingest-
sdk). Snowflake recommends using the Snowflake Ingest SDK version 2.2.0 or
later.

The SDK supports Java version 8 or later and requires [Java Cryptography
Extension (JCE) Unlimited Strength Jurisdiction Policy Files](../developer-
guide/jdbc/java-install.html#label-jdbc-jce-policy-file-install).

Important

The SDK makes REST API calls to Snowflake. You might need to adjust your
network firewall rules to allow connectivity.

### Custom client application¶

The API requires a custom Java application interface capable of pumping rows of data and handling encountered errors. You are responsible for ensuring that the application runs continuously and can recover from failure. For a given batch of rows, the API supports the equivalent of `ON_ERROR = CONTINUE | SKIP_BATCH | ABORT`.

  * `CONTINUE`: Continue to load the acceptable rows of data and return all errors.

  * `SKIP_BATCH`: Skip loading and return all errors if any error is encountered in the entire batch of rows.

  * `ABORT` (default setting): Abort the entire batch of rows and throw an exception when the first error is encountered.

The application should capture errors using the response from the `insertRow`
(single row) or `insertRows` (set of rows) methods.

## Channels¶

The API ingests rows through one or more _channels_. A channel represents a
logical, named streaming connection to Snowflake for loading data into a
table. A single channel maps to exactly one table in Snowflake; however,
multiple channels can point to the same table. The Client SDK can open
multiple channels to multiple tables; however the SDK cannot open channels
across accounts. The ordering of rows and their corresponding offset tokens
are preserved within a channel but not across channels that point to the same
table.

Channels are meant to be long lived when a client is actively inserting data
and should be reused as offset token information is retained. Data inside the
channel is automatically flushed every 1 second by default and do not need to
be closed. For more information, see Latency.

> ![Snowpipe streaming client channel table mapping](../_images/data-load-
> snowpipe-streaming-client-channel.png)

You can choose to permanently drop channels by using the `DropChannelRequest`
API when the channel and the associated offset metadata are no longer needed.
There are two ways to drop a channel:

  * Dropping a channel at closing. Data inside the channel is automatically flushed before the channel is dropped.

  * Dropping a channel blindly. This is not recommended because dropping a channel blindly discards any pending data and might invalidate any already opened channels.

You can run the SHOW CHANNELS command to list the channels for which you have
access privileges. For more information, see [SHOW CHANNELS](../sql-
reference/sql/show-channels).

Note

Inactive channels, along with their offset tokens, are deleted automatically
after 30 days.

## Offset tokens¶

An _offset token_ is a string that a client can include in `insertRow` (single
row) or `insertRows` (set of rows) method requests to track ingestion progress
on a per-channel basis. The token is initialized to NULL on channel creation
and is updated when the rows with a provided offset token are committed to
Snowflake through an asynchronous process. Clients can periodically make
`getLatestCommittedOffsetToken` method requests to get the latest committed
offset token for a particular channel and use that to reason about ingestion
progress. Note that this token is _not_ used by Snowflake to perform de-
duplication; however, clients can use this token to perform de-duplication
using your custom code.

When a client re-opens a channel, the latest persisted offset token is
returned. The client can reset its position in the data source by using the
token to avoid sending the same data twice. Note that when a channel re-open
event occurs, any data buffered in Snowflake is discarded to avoid committing
it.

You can use the latest committed offset token to perform the following common
use cases:

>   * Tracking the ingestion progress
>
>   * Checking whether a specific offset has been committed by comparing it
> with the latest committed offset token
>
>   * Advancing the source offset and purging the data that has already been
> committed
>
>   * Enabling de-duplication and ensuring exactly-once delivery of data
>
>

For example, the Kafka connector could read an offset token from a topic such
as `<partition>:<offset>`, or simply `<offset>`, if the partition is encoded
in the channel name. Consider the following scenario:

  1. The Kafka connector comes online and opens a channel corresponding to `Partition 1` in Kafka topic `T` with the channel name `T:P1`.

  2. The connector begins reading records from the Kafka partition.

  3. The connector calls the API, making an `insertRows` method request, with the offset associated with the record as the offset token.

For example, the offset token could be `10`, referring to the tenth record in
the Kafka partition.

  4. The connector periodically makes `getLatestCommittedOffsetToken` method requests to determine the ingest progress.

If the Kafka connector crashes, the following procedure could be completed to
resume reading records from the correct offset for the Kafka partition:

  1. The Kafka connector comes back online and re-opens the channel, using the same name as earlier.

  2. The connector calls the API, making a `getLatestCommittedOffsetToken` method request to get the latest committed offset for the partition.

For example, assume the latest persisted offset token is `20`.

  3. The connector uses the Kafka read APIs to reset a cursor corresponding to the offset plus 1 (`21` in this example).

  4. The connector resumes reading records. No duplicate data is retrieved after the read cursor is repositioned successfully.

In another example, an application reads logs from a directory and uses the
Snowpipe Streaming Client SDK to export those logs to Snowflake. You could
build a log export application that does the following:

  1. List files in the log directory.

Assume that the logging framework generates log files that can be ordered
lexicographically and that new log files are positioned at the end of this
ordering.

  2. Reads a log file line by line and calls the API, making `insertRows` method requests with an offset token corresponding to the log file name and the line count or byte position.

For example, an offset token could be `messages_1.log:20`, where
`messages_1.log` is the name of the log file, and `20` is the line number.

If the application crashes or needs to be restarted, it would then call the
API, making a `getLatestCommittedOffsetToken` method request to retrieve an
offset token that corresponds to the last exported log file and line.
Continuing with the example, this could be `messages_1.log:20`. The
application would then open `messages_1.log` and seek line `21` to prevent the
same log line from being ingested twice.

Note

The offset token information can be lost. The offset token is linked to a
channel object, and a channel is automatically cleared if no new ingestion is
performed using the channel for a period of 30 days. To prevent the loss of
the offset token, consider maintaining a separate offset and resetting the
channel’s offset token if required.

## Exactly-once delivery best practices¶

Achieving exactly-once delivery can be challenging, and adherence to the
following principles in your custom code is critical:

>   * To ensure appropriate recovery from exceptions, failures, or crashes,
> you must always reopen the channel and restart ingestion using the latest
> committed offset token.
>
>   * Although your application may maintain its own offset, it’s crucial to
> use the latest committed offset token provided by Snowflake as the source of
> truth and reset your own offset accordingly.
>
>   * The only instance in which your own offset should be treated as the
> source of truth is when the offset token from Snowflake is set or reset to
> NULL. A NULL offset token usually means one of the following:
>

>>     * This is a new channel, so no offset token has been set.

>>

>>     * The target table was dropped and recreated, so the channel is
considered new.

>>

>>     * There was no ingestion activity through the channel for 30 days, so
the channel was automatically cleaned up, and the offset token information was
lost.

>
>   * If necessary, you can periodically purge the source data that has
> already been committed based on the latest committed offset token, and
> advance your own offset.
>
>   * If the table schema is modified when Snowpipe Streaming channels are
> active, the channel must be reopened. The Snowflake Kafka connector handles
> this scenario automatically, but if you use Snowflake Ingest SDK directly,
> you must reopen the channel yourself.
>
>

For more information about how the Kafka connector with Snowpipe Streaming
achieves exactly-once delivery, see [Exactly-once semantics](data-load-
snowpipe-streaming-kafka.html#label-snowpipe-streaming-kafka-exactly-once).

## Loading data into Apache Iceberg™ tables¶

With Snowflake Ingest SDK versions 3.0.0 and later, Snowpipe Streaming can
ingest data into Snowflake-managed [Apache Iceberg](tables-iceberg) tables.
The Snowpipe Streaming Ingest Java SDK supports loading into both standard
Snowflake tables (non-Iceberg) and Iceberg tables.

For more information, see [Using Snowpipe Streaming with Apache Iceberg™
tables](data-load-snowpipe-streaming-iceberg).

## Latency¶

Snowpipe Streaming automatically flushes data within channels every one
second. You do not need to close the channel for data to be flushed.

With Snowflake Ingest SDK versions 2.0.4 and later, you can configure the
latency by using the option `MAX_CLIENT_LAG`.

  * For standard Snowflake tables (non-Iceberg), the default `MAX_CLIENT_LAG` is 1 second.

  * For Iceberg tables (supported by Snowflake Ingest SDK versions 3.0.0 and later), the default `MAX_CLIENT_LAG` is 30 seconds.

The maximum latency can be set up to 10 minutes. For more information, see
[MAX_CLIENT_LAG](https://javadoc.io/doc/net.snowflake/snowflake-ingest-
sdk/latest/net/snowflake/ingest/utils/ParameterProvider.html#MAX_CLIENT_LAG)
and [recommended latency configurations for Snowpipe Streaming](data-load-
snowpipe-streaming-recommendation.html#label-snowpipe-streaming-
recommendations-latency).

Note that the Kafka connector for Snowpipe Streaming has its own buffer. After
the Kafka buffer flush time is reached, data will be sent with one second
latency to Snowflake through Snowpipe Streaming. For more information, see
[buffer.flush.time](data-load-snowpipe-streaming-kafka.html#label-snowpipe-
streaming-kafka-buffer).

## Migration to optimized files¶

The API writes the rows from channels into blobs in cloud storage, which are
then committed to the target table. Initially, the streamed data written to a
target table is stored in a temporary intermediate file format. At this stage,
the table is considered a “mixed table” because partitioned data is stored in
a mixture of native and intermediary files. An automated background process
migrates data from the active intermediate files to native files optimized for
query and DML operations as needed.

## Replication¶

Snowpipe streaming supports the [replication and failover](account-
replication-intro) of Snowflake tables populated by Snowpipe Streaming and its
associated channel offsets from a source account to a target account in
different [regions](intro-regions) and across [cloud platforms](intro-cloud-
platforms).

For more information, see [Replication and Snowpipe Streaming](account-
replication-considerations.html#label-replication-snowpipe-streaming).

## Insert-only operations¶

The API is currently limited to inserting rows. To modify, delete, or combine
data, write the “raw” records to one or more staging tables. Merge, join, or
transform the data by using [continuous data pipelines](data-pipelines-intro)
to insert modified data into destination reporting tables.

## Classes and interfaces¶

For documentation on the classes and interfaces, see [Snowflake Ingest SDK
API](https://javadoc.io/doc/net.snowflake/snowflake-ingest-
sdk/latest/overview-summary.html).

## Supported Java data types¶

The following table summarizes which Java data types are supported for
ingestion into Snowflake columns:

Snowflake column type | Allowed Java data type  
---|---  
  
  * CHAR
  * VARCHAR

|

  * String
  * primitive data types (int, boolean, char, …)
  * BigInteger, BigDecimal

  
  
  * BINARY

|

  * byte[]
  * String (hex-encoded)

  
  
  * NUMBER

|

  * numeric types (BigInteger, BigDecimal, byte, int, double, …)
  * String

  
  
  * FLOAT

|

  * numeric types (BigInteger, BigDecimal, byte, int, double, …)
  * String

  
  
  * BOOLEAN

|

  * boolean
  * numeric types (BigInteger, BigDecimal, byte, int, double, …)
  * String

See [boolean conversion details](../sql-reference/data-types-
logical.html#label-boolean-conversion).  
  
  * TIME

|

  * java.time.LocalTime
  * java.time.OffsetTime
  * String
    * [Integer-stored time](../sql-reference/date-time-input-output.html#label-date-time-input-output-auto-detection-integer-stored)
    * `HH24:MI:SS.FFTZH:TZM` (e.g. `20:57:01.123456789+07:00`)
    * `HH24:MI:SS.FF` (e.g. `20:57:01.123456789`)
    * `HH24:MI:SS` (e.g. `20:57:01`)
    * `HH24:MI` (e.g. `20:57`)

  
  
  * DATE

|

  * java.time.LocalDate
  * java.time.LocalDateTime
  * java.time.OffsetDateTime
  * java.time.ZonedDateTime
  * java.time.Instant
  * String
    * [Integer-stored date](../sql-reference/date-time-input-output.html#label-date-time-input-output-auto-detection-integer-stored)
    * `YYYY-MM-DD` (e.g. `2013-04-28`)
    * `YYYY-MM-DDTHH24:MI:SS.FFTZH:TZM` (e.g. `2013-04-28T20:57:01.123456789+07:00`)
    * `YYYY-MM-DDTHH24:MI:SS.FF` (e.g. `2013-04-28T20:57:01.123456`)
    * `YYYY-MM-DDTHH24:MI:SS` (e.g. `2013-04-28T20:57:01`)
    * `YYYY-MM-DDTHH24:MI` (e.g. `2013-04-28T20:57`)
    * `YYYY-MM-DDTHH24:MI:SSTZH:TZM` (e.g. `2013-04-28T20:57:01-07:00`)
    * `YYYY-MM-DDTHH24:MITZH:TZM` (e.g. `2013-04-28T20:57-07:00`)

  
  
  * TIMESTAMP_NTZ
  * TIMESTAMP_LTZ
  * TIMESTAMP_TZ

|

  * java.time.LocalDate
  * java.time.LocalDateTime
  * java.time.OffsetDateTime
  * java.time.ZonedDateTime
  * java.time.Instant
  * String
    * [Integer-stored timestamp](../sql-reference/date-time-input-output.html#label-date-time-input-output-auto-detection-integer-stored)
    * `YYYY-MM-DD` (e.g. `2013-04-28`)
    * `YYYY-MM-DDTHH24:MI:SS.FFTZH:TZM` (e.g. `2013-04-28T20:57:01.123456789+07:00`)
    * `YYYY-MM-DDTHH24:MI:SS.FF` (e.g. `2013-04-28T20:57:01.123456`)
    * `YYYY-MM-DDTHH24:MI:SS` (e.g. `2013-04-28T20:57:01`)
    * `YYYY-MM-DDTHH24:MI` (e.g. `2013-04-28T20:57`)
    * `YYYY-MM-DDTHH24:MI:SSTZH:TZM` (e.g. `2013-04-28T20:57:01-07:00`)
    * `YYYY-MM-DDTHH24:MITZH:TZM` (e.g. `2013-04-28T20:57-07:00`)

  
  
  * VARIANT
  * ARRAY

|

  * String (must be a valid JSON)
  * primitive data types and their arrays
  * BigInteger, BigDecimal
  * java.time.LocalTime
  * java.time.OffsetTime
  * java.time.LocalDate
  * java.time.LocalDateTime
  * java.time.OffsetDateTime
  * java.time.ZonedDateTime
  * java.util.Map<String, T> where T is a valid VARIANT type
  * T[] where T is a valid VARIANT type
  * List<T> where T is a valid VARIANT type

  
  
  * OBJECT

|

  * String (must be a valid JSON object)
  * Map<String, T> where T is a valid variant type

  
  
  * GEOGRAPHY

|

  * Not supported

  
  
  * GEOMETRY

|

  * Not supported

  
  
## Required access privileges¶

Calling the Snowpipe Streaming API requires a role with the following
privileges:

Object | Privilege  
---|---  
Table | OWNERSHIP or a minimum of INSERT and EVOLVE SCHEMA (only required when using schema evolution for Kafka connector with Snowpipe Streaming)  
Database | USAGE  
Schema | USAGE  
  
## Limitations¶

Snowpipe Streaming only supports using 256-bit AES keys for data encryption.

If [Automatic Clustering](tables-auto-reclustering) is also enabled on the
same table that Snowpipe Streaming is inserting into, compute costs for file
migration might be reduced. For more information, see [Snowpipe Streaming best
practices](data-load-snowpipe-streaming-recommendation).

The following objects or types are _not_ supported:

  * The GEOGRAPHY and GEOMETRY data types

  * Columns with collations

  * TRANSIENT or TEMPORARY tables

  * Tables with any of the following column settings:

    * `AUTOINCREMENT` or `IDENTITY`

    * Default column value that is not NULL

  * The total number of channels per table cannot exceed 10k. We recommend reusing channels when needed. Contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) if you need to open more than 10k channels per table.

