# Tutorial: Get started with logging and tracing¶

## Introduction¶

This tutorial introduces the basics of emitting, collecting, and querying log
and trace data from function and procedure handler code.

The tutorial uses the Snowsight web interface, but you can use any Snowflake
client that supports executing SQL. For more information about Snowsight, see
[Getting started with worksheets](../../../user-guide/ui-snowsight-worksheets-
gs) and [Work with worksheets in Snowsight](../../../user-guide/ui-snowsight-
worksheets).

### What you will learn¶

In this tutorial, you will learn how to:

  * Create an event table to store log and trace data.

Snowflake collects log and trace data in the table’s predefined structure.

  * Emit log messages and trace data from a user-defined function (UDF).

You can use an API designed for your handler language to emit log messages and
trace data from handler code.

  * View the collected log and trace data by querying the event table.

You can query the table with a SELECT statement to analyze the collected data.

### Prerequisites¶

  * You must execute all of the SQL commands in the same SQL command session because the session context is required.

To do this in Snowsight, for example, paste all of your code into the same
worksheet as you go along. As you progress from section to section, each
section builds on the previous.

  * You must be able to use the ACCOUNTADMIN role.

In this tutorial, you will perform all the steps using the ACCOUNTADMIN role.
In general practice, however, you would use roles with privileges specifically
defined for the action you’re performing. For example, you might have separate
roles for developers who create UDFs, for analysts who query collected log and
trace data, and so on.

For more about roles, see [Switch your active role](../../../user-guide/ui-
snowsight-gs.html#label-switching-your-active-role) and [Access control
considerations](../../../user-guide/security-access-control-considerations).

## Set up the database, warehouse, and access¶

In this section, you’ll create a warehouse and database you’ll need for the
tutorial. You’ll also begin using the ACCOUNTADMIN role, which is required to
execute some of the statements in this tutorial.

You’re creating a database in which you’ll later create the event table and
the user-defined function. You can delete all of the objects you create in the
tutorial, including the database and warehouse, when you no longer need them.

To create a database and warehouse for use in the tutorial:

  1. Sign in to Snowsight.

  2. [Switch to the ACCOUNTADMIN role](../../../user-guide/ui-snowsight-gs.html#label-switching-your-active-role).

  3. Open Projects » Worksheets.

  4. Select + » SQL Worksheet.

  5. [Rename the new worksheet](../../../user-guide/ui-snowsight-worksheets.html#label-worksheets-manage) to `Logging-tracing tutorial`.

  6. In the new worksheet, paste and run the following statement to create a database. The new database is just for this tutorial.

> >     CREATE OR REPLACE DATABASE tutorial_log_trace_db;
>  
>
> Copy

  7. Paste and run the following statement to create a warehouse. The new warehouse is just for this tutorial.

> >     CREATE OR REPLACE WAREHOUSE tutorial_log_trace_wh
>       WAREHOUSE_TYPE = STANDARD
>       WAREHOUSE_SIZE = XSMALL;
>  
>
> Copy

In this section, you put in place the pieces you need for the tutorial. In the
next section, you’ll create an event table for storing log and trace data.

## Create an event table¶

In this section, you’ll create an event table. As your handler code emits log
messages and trace data, Snowflake saves the emitted data in event table rows.
You can query the event table to analyze the data.

You must create an event table to collect log and trace data. An event table
always uses the [predefined structure](../event-table-columns) defined by
Snowflake.

Important

To complete this section, you’ll need to be able to use the ACCOUNTADMIN role,
which is required when altering an account so that the new event table is the
account’s active event table.

To create the event table, you must use a role with the CREATE EVENT TABLE
privilege assigned.

To create the event table and make it the active event table for the account:

  1. Paste and run the following statement to create an event table.

> >     CREATE OR REPLACE EVENT TABLE tutorial_event_table;
>  
>
> Copy
>
> This table is where Snowflake stores log and trace data.

  2. Paste and run the following statement to alter the account so that the event table you created is the active one for the account.

> >     USE ROLE ACCOUNTADMIN;
>  
>     ALTER ACCOUNT SET EVENT_TABLE =
> tutorial_log_trace_db.public.tutorial_event_table;
>  
>
> Copy

This statement sets the new event table as the table that Snowflake should use
for storing log messages and trace data from handlers in the current account.
You can have only one active event table for an account.

In this section, you created an event table. In the next section, you’ll start
emitting log messages that Snowflake stores in the table.

## Emit log messages¶

In this section, you’ll create a user-defined function (UDF) with Python
handler code that emits log messages. As your code emits log messages,
Snowflake collects the message data and stores it in the event table you
created.

Snowflake supports APIs to log messages from each supported handler language.
For handlers you write in Python, you can use the `logging` module in Python’s
standard library.

To create a UDF that emits log messages:

  1. Paste and run the following statement to set the log level to `INFO`.

> >     ALTER SESSION SET LOG_LEVEL = INFO;
>  
>
> Copy

This specifies the severity of log messages that Snowflake should capture as
the UDF runs. In this case, the level permits all messages ranging from
informational (`INFO`) to the most severe (`FATAL`).

  2. Paste and run the following statement to create a user-defined function.

> >     CREATE OR REPLACE FUNCTION log_trace_data()
>     RETURNS VARCHAR
>     LANGUAGE PYTHON
>     RUNTIME_VERSION = 3.9
>     HANDLER = 'run'
>     AS $$
>     import logging
>     logger = logging.getLogger("tutorial_logger")
>  
>     def run():
>       logger.info("Logging from Python function.")
>       return "SUCCESS"
>     $$;
>  
>
> Copy

Highlighted lines in the code do the following:

>      * Import the Python `logging` module so that the handler code can use
> it.
>
>      * Create a logger, which exposes the interface your code will use to
> log messages.
>
>      * Log a message at the `INFO` level.

  3. Paste and run the following statement to execute the function you just created.

> >     SELECT log_trace_data();
>  
>
> Copy
>
> This produces the following output. In addition, as the function executed,
> it emitted a log message that Snowflake collected in the event table.
>  
>     >     --------------------
>     | LOG_TRACE_DATA() |
>     --------------------
>     | SUCCESS          |
>     --------------------
>  

In this section, you emitted a log message from a UDF. In the next section,
you’ll query the event table to retrieve data related to the message.

## Query for log messages¶

In this section, you’ll query the event table for log message data emitted by
the UDF you ran in the previous section.

Note

It can take several seconds for log or trace data emitted by handler code to
be recorded in the event table. If you don’t see results immediately, try
again in a few seconds.

Snowflake uses [predefined event table columns](../event-table-columns) to
collect and store log and trace data of the following kinds:

  * **Data you emit from handler code** , such as log messages and trace event data.

You’ll find these in columns such as RECORD_TYPE, RECORD, RECORD_ATTRIBUTES,
and others.

  * **Data about the context** in which the log or trace data was emitted, such as the timestamp, name of the handler method from which the data was emitted, and so on.

You’ll find this data in columns such as RESOURCE_ATTRIBUTES, TIMESTAMP, and
SCOPE.

To query the event table for log message data:

  1. Paste and run the following statement to query the event table.

> >     SELECT
>       TIMESTAMP AS time,
>       RESOURCE_ATTRIBUTES['snow.executable.name'] as executable,
>       RECORD['severity_text'] AS severity,
>       VALUE AS message
>     FROM
>       tutorial_log_trace_db.public.tutorial_event_table
>     WHERE
>       RECORD_TYPE = 'LOG'
>       AND SCOPE['name'] = 'tutorial_logger';
>  
>
> Copy

Some columns contain structured data expressed as key-value pairs. In this
query, you specify attribute keys within a column by using [bracket
notation](../../../user-guide/querying-semistructured.html#label-bracket-
notation-when-querying-semistructured-data) such as `RECORD['severity_text']`.

You also use bracket notation (`SCOPE['name']`) to specify that you want to
select column values only where the log entries are emitted with the Python
logger, `tutorial_logger`, you created in handler code.

  2. View the output.

> >
> -----------------------------------------------------------------------------------------------------------
>     | TIME                | EXECUTABLE                           | SEVERITY | MESSAGE                         |
>
> -----------------------------------------------------------------------------------------------------------
>     | 2023-04-19 22:00:49 | "LOG_TRACE_DATA():VARCHAR(16777216)" | "INFO"   | "Logging from Python function." |
>
> -----------------------------------------------------------------------------------------------------------
>  

The output illustrates how the [event table’s predefined columns](../event-
table-columns) each contain parts of the collected data. For the `EXECUTABLE`
and `SEVERITY` values, you’ve used bracket notation to specify the attributes
whose values you want.

> Output Column | Description  
> ---|---  
> TIME | The time the entry was created (from the TIMESTAMP column).  
> EXECUTABLE | UDF name and parameters (from the RESOURCE_ATTRIBUTES column’s `snow.executable.name` attribute).  
> SEVERITY | Log entry severity (from the RECORD column’s `severity_text` attribute).  
> MESSAGE | Log message (from the VALUE column).  
  

In this section, you used a SELECT statement to query for log data. In the
next section, you’ll update the UDF so that it emits trace data.

## Emit trace data¶

In this section, you’ll update the UDF handler code so that it also emits
trace data. As your code emits trace data, Snowflake collects the data and
stores it in the event table you created.

Trace data has structural qualities, including event data grouped into spans
and data captured as key-value pairs, that let you assemble a more detailed
picture of your code’s activity than log data typically allows.

Snowflake supports APIs to emit trace data from each supported handler
language. For handlers you write in Python, you can use the Snowflake
`telemetry` package.

To update the UDF to emit trace data:

  1. Paste and run the following statement to specify what trace data should be captured.

> >     ALTER SESSION SET TRACE_LEVEL = ON_EVENT;
>  
>
> Copy

This sets the trace level to `ON_EVENT`. This specifies that only trace data
emitted explicitly by your own code should be captured.

  2. Paste and run the following statement to create a UDF that emits trace data.

> >     CREATE OR REPLACE FUNCTION log_trace_data()
>     RETURNS VARCHAR
>     LANGUAGE PYTHON
>     PACKAGES = ('snowflake-telemetry-python')
>     RUNTIME_VERSION = 3.9
>     HANDLER = 'run'
>     AS $$
>     import logging
>     logger = logging.getLogger("tutorial_logger")
>     from snowflake import telemetry
>  
>     def run():
>       telemetry.set_span_attribute("example.proc.run", "begin")
>       telemetry.add_event("event_with_attributes", {"example.key1":
> "value1", "example.key2": "value2"})
>       logger.info("Logging from Python function.")
>       return "SUCCESS"
>     $$;
>  
>
> Copy

By running this code, you’re replacing the function you created earlier with
one that adds code for emitting trace data. The highlighted lines do the
following:

     * Add `snowflake-telemetry-python` – which contains the `telemetry` package – to the UDF’s execution environment.

     * Import the `telemetry` package so you can call its functions.

     * Set an attribute and attribute value to the span that Snowflake creates when the code runs.

A span represents a procedure’s or UDF’s execution unit, within which you can
add multiple events.

     * Add an event (with its own attributes) to record as part of the span.

  3. Paste and run the following statement to execute the function you just created.

> >     SELECT log_trace_data();
>  
>
> Copy
>
> This produces the following output. In addition, as the function executed,
> it emitted trace data that Snowflake collected in the event table.
>  
>     >     --------------------
>     | LOG_TRACE_DATA() |
>     --------------------
>     | SUCCESS          |
>     --------------------
>  

In this section, you emitted trace data from a UDF. In the next section,
you’ll query the event table to retrieve data related to the trace.

## Query for trace messages¶

In this section, you’ll query the event table for trace data emitted by the
UDF you ran in the previous section.

Note

It can take several seconds for log or trace data emitted by handler code to
be recorded in the event table. If you don’t see results immediately, try
again in a few seconds.

The query you write will retrieve contextual information about events emitted
by the function. That context includes the name of the function that emitted
it.

To query the event table for trace data:

  1. Paste and run the following statement to query the event table for trace data.

> >     SELECT
>       TIMESTAMP AS time,
>       RESOURCE_ATTRIBUTES['snow.executable.name'] AS handler_name,
>       RECORD['name'] AS event_name,
>       RECORD_ATTRIBUTES AS attributes
>     FROM
>       tutorial_log_trace_db.public.tutorial_event_table
>     WHERE
>       RECORD_TYPE = 'SPAN_EVENT'
>       AND HANDLER_NAME LIKE 'LOG_TRACE_DATA%';
>  
>
> Copy

Some columns contain structured data expressed as key-value pairs. For these,
you can select attribute values within a column by using [bracket
notation](../../../user-guide/querying-semistructured.html#label-bracket-
notation-when-querying-semistructured-data), as shown in the code.

  2. View the output.

> >
> -----------------------------------------------------------------------------------------------------------------------------------------------------
>     | TIME                    | HANDLER_NAME                         | EVENT_NAME              | ATTRIBUTES                                             |
>
> -----------------------------------------------------------------------------------------------------------------------------------------------------
>     | 2023-05-10 20:49:35.080 | "LOG_TRACE_DATA():VARCHAR(16777216)" | "event_with_attributes" | { "example.key1": "value1", "example.key2": "value2" } |
>
> -----------------------------------------------------------------------------------------------------------------------------------------------------
>  

The output illustrates how the [event table’s predefined columns](../event-
table-columns) each contain parts of the collected data. For the `EXECUTABLE`
and `SEVERITY` values, you’ve used bracket notation to specify the attribute
whose value you want.

> Output Column | Description  
> ---|---  
> TIME | Time the entry was created (from the TIMESTAMP column).  
> HANDLER_NAME | UDF name and parameters (from the RESOURCE_ATTRIBUTES column’s `snow.executable.name` attribute).  
> EVENT_NAME | Name of the event added with the `add_event` function (from the RECORD column’s `name` attribute).  
> ATTRIBUTES | Attributes added to accompany the event (from the RECORD_ATTRIBUTES column).  
  

In this section, you queried the event table for trace data emitted by the UDF
you wrote. In the last section, you’ll get links to information related to the
things you did during the tutorial.

## Learn more¶

You finished! Nicely done.

In this tutorial, you got an end-to-end view of how you can emit and store log
and trace data from handler code, then query the stored data. Along the way,
you:

  * **Created an event table.** For information related to event tables, see the following:

    * For more detail on setting up an event table, see [Event table overview](../event-table-setting-up).

    * For reference information about the columns that make up an event table, see [Event table columns](../event-table-columns).

    * For more on things you can do with event tables, see [Working with event tables](../event-table-operations).

  * **Created a user-defined function (UDF)** that emitted log and trace data. For related information, see the following:

    * For an overview of logging support in Snowflake, see [Logging messages from functions and procedures](../logging). For specific about logging with Python, see [Logging messages from functions and procedures](../logging) and the [logging](https://docs.python.org/library/logging.html) module in Python’s standard library.

    * For details on setting levels, see [Setting levels for logging, metrics, and tracing](../telemetry-levels).

    * For an overview of tracing support, see [Trace events for functions and procedures](../tracing). For specific about tracing with Python, see [Emitting trace events in Python](../tracing-python).

    * For general information on creating UDFs, see [User-defined functions overview](../../udf/udf-overview).

  * **Queried the event table** for log and trace data. For information related to event tables, see the following:

    * For a more complete view of how to query for log data, see [Viewing log messages](../logging-accessing-messages).

    * For a view of how to query for trace data, see [Viewing trace data](../tracing-accessing-events).

    * For more information on spans and events, along with information how Snowflake stores data for them, see [How Snowflake represents trace events](../tracing-how-events-work).

