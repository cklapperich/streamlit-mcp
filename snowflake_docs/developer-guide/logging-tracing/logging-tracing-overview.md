# Logging, tracing, and metrics¶

You can record the activity of your Snowflake function and procedure handler
code (including code you write [using Snowpark APIs](../snowpark/index)) by
capturing log messages and trace events from the code as it executes. Once
you’ve collected the data, you can query it with SQL to analyze the results.

Logging, tracing, and metrics are among the observability features Snowflake
provides to make it easier for you to debug and optimize applications.
Snowflake captures observability data in a structure based on the
[OpenTelemetry](https://opentelemetry.io/) standard.

In particular, you can record and analyze the following:

  * [Log messages](logging) — Independent, detailed messages with information about the state of a specific piece of your code.

  * [Metrics data](metrics) — CPU and memory metrics that Snowflake generates.

  * [Trace events](tracing) — Structured data you can use to get information spanning and grouping multiple parts of your code.

## Get started¶

Use the following high-level steps to begin capturing and using log and trace
data.

  1. Ensure that you have an active event table. You can do one of the following:

     * [Use the default event table](event-table-setting-up.html#label-logging-event-table-default) that is active by default.

     * [Create and set as active an event table](event-table-setting-up.html#label-logging-event-table-create).

Snowflake collects telemetry data from your code in the event table.

  2. Set telemetry levels so that data is collected.

With levels, you can specify which data – and how much data – is collected.
Make sure the levels are set correctly.

  3. Begin emitting log or trace data from handler code.

Once you’ve created an event table and associated it with your account, you
can use an API in your handler’s language to emit log messages. After you’ve
captured log and trace data, you can query the data to analyze the results.

For more information on instrumenting your code, see the following:

     * [Logging messages from functions and procedures](logging)

     * [Trace events for functions and procedures](tracing)

  4. Query the event table to analyze collected log and trace data.

For more information, see the following:

     * [Viewing log messages](logging-accessing-messages)

     * [Viewing metrics data](metrics-viewing-data)

     * [Viewing trace data](tracing-accessing-events)

## Set telemetry levels¶

You can manage the level of telemetry data stored in the event table — such as
log, trace, and metrics data — by setting the level for each type of data. Use
level settings to ensure that you’re capturing the amount and kind of data you
want.

For more information, see [Setting levels for logging, metrics, and
tracing](telemetry-levels).

## Compare log messages and trace events¶

The following table compares the characteristics and benefits of log messages
and trace events.

Characteristic | Log entries | Trace events  
---|---|---  
Intended use | Record detailed but unstructured information about the state of your code. Use this information to understand what happened during a particular invocation of your function or procedure. | Record a brief but structured summary of each invocation of your code. Aggregate this information to understand behavior of your code at a high level.  
Structure as a payload | None. A log entry is just a string. | Structured with attributes you can attach to trace events. Attributes are key-value pairs that can be easily queried with a SQL query.  
Supports grouping | No. Each log entry is an independent event. | Yes. Trace events are organized into spans. A span can have its own attributes.  
Quantity limits | Unlimited. All log entries emitted by your code are ingested into the event table. | The number of trace events per span is capped at 128. There is also a limit on the number of span attributes.  
Complexity of queries against recorded data | Relatively high. Your queries must parse each log entry to extract meaningful information from it. | Relatively low. Your queries can take advantage of the structured nature of trace events.

