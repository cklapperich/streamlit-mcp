# Extending Snowflake with Functions and Procedures¶

You can extend the SQL you use in Snowflake by writing user-defined functions
(UDFs) and stored procedures that you can call from SQL. When you write a UDF
or procedure, you write its logic in one of the supported handler languages,
then create it using SQL.

With a UDF, you calculate and return a value. With a stored procedure, you
generally perform one or more operations by executing statements in SQL or
another supported language.

You can also write an external function whose logic executes on a system
external to Snowflake, such as a cloud provider.

[Choosing whether to write a stored procedure or a user-defined
function](stored-procedures-vs-udfs)

    

Choose between writing a stored procedure and writing a user-defined function.

[Design Guidelines and Constraints for Functions and Procedures](udf-stored-
procedure-guidelines)

    

Read more about the guidelines that functions and procedures share, including
guidelines related to deployment options, security practices, platform
constraints, and conventions.

[Packaging Handler Code](udf-stored-procedure-building)

    

Use tools to package handler code and ensure that dependencies are available
on Snowflake.

[Stored procedures overview](stored-procedure/stored-procedures-overview)

    

Learn the benefits and supported languages.

[User-defined functions overview](udf/udf-overview)

    

Learn the types of UDFs and supported languages.

[Logging, tracing, and metrics](logging-tracing/logging-tracing-overview)

    

Record handler code activity by capturing log messages and trace events,
storing the data in a database you can query later.

[External network access overview](external-network-access/external-network-
access-overview)

    

Create secure access to specific network locations external to Snowflake, then
use that access from within the handler code.

[Introduction to external functions](../sql-reference/external-functions-
introduction)

    

Access custom code that runs outside of Snowflake, such as API services that
provide geocoding and machine learning models.

