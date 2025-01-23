# Snowpark Developer Guide for Python¶

The [Snowpark library](../index) provides an intuitive API for querying and
processing data in a data pipeline. Using the Snowpark library, you can build
applications that process data in Snowflake without moving data to the system
where your application code runs. You can also automate data transformation
and processing by writing stored procedures and scheduling those procedures as
tasks in Snowflake.

## Get Started¶

You can write Snowpark Python code in a local development environment or in a
Python worksheet in Snowsight.

If you need to write a client application, set up a local development
environment by doing the following:

  1. Set up your preferred development environment to build Snowpark apps. See [Setting Up Your Development Environment for Snowpark Python](setup).

  2. Establish a session to interact with the Snowflake database. See [Creating a Session for Snowpark Python](creating-session).

If you want to write a stored procedure to automate tasks in Snowflake, use
Python worksheets in Snowsight. See [Writing Snowpark Code in Python
Worksheets](python-worksheets).

## Write Snowpark Python Code¶

You can query, process, and transform data in a variety of ways using Snowpark
Python.

  * Query and process data with a `DataFrame` object. See [Working with DataFrames in Snowpark Python](working-with-dataframes).

  * Run your pandas code directly on your data in Snowflake. See [pandas on Snowflake](pandas-on-snowflake).

  * Convert custom lambdas and functions to user-defined functions (UDFs) that you can call to process data. See [Creating User-Defined Functions (UDFs) for DataFrames in Python](creating-udfs).

  * Write a user-defined tabular function (UDTF) that processes data and returns data in a set of rows with one or more columns. See [Creating User-Defined Table Functions (UDTFs) for DataFrames in Python](creating-udtfs).

  * Write a stored procedure that you can call to process data, or automate with a task to build a data pipeline. See [Creating Stored Procedures for DataFrames in Python](creating-sprocs).

### Perform Machine Learning Tasks¶

You can use Snowpark Python to perform machine learning tasks like training
models:

  * Train machine learning models by writing stored procedures. See [Training Machine Learning Models with Snowpark Python](python-snowpark-training-ml).

  * Train, score, and tune machine learning models using Snowpark Python stored procedures and deploy the trained models with user-defined functions. See [Machine Learning with Snowpark Python - Credit Card Approval Prediction](https://quickstarts.snowflake.com/guide/getting_started_snowpark_machine_learning/index.html) (Snowflake Quickstarts).

### Troubleshoot Snowpark Python Code¶

Troubleshoot your code with logging statements and by viewing the underlying
SQL. See [Troubleshooting with Snowpark Python](troubleshooting).

### Record and Analyze Data About Code Execution¶

You can record log messages and trace events in an event table for later
analysis. For more information, see [Logging, tracing, and
metrics](../../logging-tracing/logging-tracing-overview).

## API Reference¶

The Snowpark for Python API reference contains extensive details about the
available classes and methods. See [Snowpark Library for Python API
Reference](/developer-guide/snowpark/reference/python/latest/index).

The pandas on Snowflake API reference contains extensive details about the
available classes and methods. See [Snowpark pandas
API](https://docs.snowflake.com/en/developer-
guide/snowpark/reference/python/latest/modin/index) .

For the list of changes to the API between versions, see [Snowpark Library for
Python release notes](../../../release-notes/clients-drivers/snowpark-python).

