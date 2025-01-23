# Schema detection and evolution for Kafka connector with Snowpipe Streaming¶

The Kafka connector with Snowpipe Streaming supports schema detection and
evolution. The structure of tables in Snowflake can be defined and evolved
automatically to support the structure of new Snowpipe streaming data loaded
by the Kafka connector.

Without schema detection and evolution, the Snowflake table loaded by the
Kafka connector only consists of two VARIANT columns, RECORD_CONTENT and
RECORD_METADATA. With schema detection and evolution enabled, Snowflake can
detect the schema of the streaming data and load data into tables that
automatically match any user-defined schema. Snowflake also allows adding new
columns or dropping the NOT NULL constraint from columns missing in new data
files.

Note

This feature only works with Kafka connector with Snowpipe Streaming. It
doesn’t support Kafka connector with file-based Snowpipe.

## Prerequisites¶

Before enabling this feature, make sure to set up the following prerequisites.

>   * Download Kafka connector version 2.0.0 or later. For more information,
> see [Installing and configuring the Kafka connector](kafka-connector-
> install).
>
>   * Use the [ALTER TABLE](../sql-reference/sql/alter-table) command to set
> the `ENABLE_SCHEMA_EVOLUTION` parameter to TRUE on the table. You must also
> use a role that has the OWNERSHIP privilege on the table. For more
> information, see [Table schema evolution](data-load-schema-evolution).
>
>

## Configuring required Kafka properties¶

Configure the following required properties in your Kafka connector properties
file:

`snowflake.ingestion.method`

    

Specify to use `SNOWPIPE_STREAMING` to load your Kafka topic data. Note that
this feature doesn’t support `SNOWPIPE`.

`snowflake.enable.schematization`

    

Specify to `TRUE` to enable schema detection and evolution for Kafka Connector
with Snowpipe Streaming. The default value is `FALSE`.

When this property is set to `TRUE`,

  * For any new tables that are created by Kafka connector, the table parameter `ENABLE_SCHEMA_EVOLUTION` is automatically set to `TRUE`.

  * For any existing tables, you still need to manually set the table parameter `ENABLE_SCHEMA_EVOLUTION` to `TRUE`.

`schema.registry.url`

    

Specify to the URL of the schema registry service. The default value is empty.

Depending on the file format, `schema.registry.url` is required or optional.
Schema detection with Kafka connector is supported in either of the scenarios
below:

>   * Schema registry is required for Avro and Protobuf. The column is created
> with the data types defined in the provided schema registry.
>
>   * Schema registry is optional for JSON. If there is no schema registry,
> the data type will be inferred based on the data provided.
>
>

Configure additional properties in your Kafka connector properties file as
usual. For more information, see [Configuring the Kafka connector](kafka-
connector-install.html#label-kafka-connector-configuration-file).

## Converters¶

Structured data converters, such as Json, Avro and Protobuf, are supported.
Note that we have only tested the following structured data converters:

  * `io.confluent.connect.avro.AvroConverter`

  * `io.confluent.connect.protobuf.ProtobufConverter`

  * `org.apache.kafka.connect.json.JsonConverter`

  * `io.confluent.connect.json.JsonSchemaConverter`

Any unstructured data converters are not supported with schematization. For
example,

  * `org.apache.kafka.connect.converters.ByteArrayConverter`

  * `org.apache.kafka.connect.storage.StringConverter`

Snowflake converters are not supported with Snowpipe Streaming. Some
customized data converters are untested and may also not be supported.

## Usage notes¶

  * Schema detection with Kafka connector is supported with or without a provided schema registry. If using schema registry (Avro and Protobuf), the column will be created with the data types defined in the provided schema registry. If there is no schema registry (JSON), the data type will be inferred based on the data provided.

  * Schema evolution with Kafka connector supports the following table column modifications:

>     * Adding new columns
>
>     * Dropping NOT NULL constraint if the source data column is missing.

  * If Kafka connector creates the target table, schema evolution is enabled by default. However, if schema evolution is disabled for an existing table then Kafka connector will try to send the rows with mismatched schemas to the configured dead-letter queues (DLQ).

  * JSON ARRAY is not supported for further schematization.

  * For the Kafka connector with Snowpipe Streaming, schema evolution is not tracked by the `SchemaEvolutionRecord` output in the following views and commands: [INFORMATION_SCHEMA COLUMNS View](../sql-reference/info-schema/columns), [ACCOUNT_USAGE COLUMNS View](../sql-reference/account-usage/columns), [DESCRIBE TABLE command](../sql-reference/sql/desc-table), and [SHOW COLUMNS command](../sql-reference/sql/show-columns). The `SchemaEvolutionRecord` output always shows NULL.

## Examples¶

The following examples demonstrate the tables that are created before and
after the schema detection and evolution are enabled for Kafka connector with
Snowpipe Streaming.

>
>     -- Before schema detection and evolution is enabled, the table only
> consists of two VARIANT columns, RECORD_CONTENT and RECORD_METADATA, as the
> following example demonstrates.
>
> +------+---------------------------------------------------------+---------------------------------------------------+
>     | Row  | RECORD_METADATA                                         | RECORD_CONTENT                                    |
>
> |------+---------------------------------------------------------+---------------------------------------------------|
>     | 1    |{"CreateTime":1669074170090, "headers": {"current.iter...| "account": "ABC123", "symbol": "ZTEST", "side":...|
>     | 2    |{"CreateTime":1669074170400, "headers": {"current.iter...| "account": "XYZ789", "symbol": "ZABZX", "side":...|
>     | 3    |{"CreateTime":1669074170659, "headers": {"current.iter...| "account": "XYZ789", "symbol": "ZTEST", "side":...|
>     | 4    |{"CreateTime":1669074170904, "headers": {"current.iter...| "account": "ABC123", "symbol": "ZABZX", "side":...|
>     | 5    |{"CreateTime":1669074171063, "headers": {"current.iter...| "account": "ABC123", "symbol": "ZTEST", "side":...|
>
> +------+---------------------------------------------------------+---------------------------------------------------|
>  
>     -- After schema detection and evolution is enabled, the table contains
> the columns that match the user-defined schema. The table can also
> automatically evolve to support the structure of new Snowpipe streaming data
> loaded by the Kafka connector.
>
> +------+---------------------------------------------------------+---------+--------+-------+----------+
>     | Row  | RECORD_METADATA                                         | ACCOUNT | SYMBOL | SIDE  | QUANTITY |
>
> |------+---------------------------------------------------------+---------+--------+-------+----------|
>     | 1    |{"CreateTime":1669074170090, "headers": {"current.iter...| ABC123  | ZTEST  | BUY   | 3572     |
>     | 2    |{"CreateTime":1669074170400, "headers": {"current.iter...| XYZ789  | ZABZX  | SELL  | 3024     |
>     | 3    |{"CreateTime":1669074170659, "headers": {"current.iter...| XYZ789  | ZTEST  | SELL  | 799      |
>     | 4    |{"CreateTime":1669074170904, "headers": {"current.iter...| ABC123  | ZABZX  | BUY   | 2033     |
>     | 5    |{"CreateTime":1669074171063, "headers": {"current.iter...| ABC123  | ZTEST  | BUY   | 1558     |
>
> +------+---------------------------------------------------------+---------+--------+-------+----------|
>  
>
> Copy

