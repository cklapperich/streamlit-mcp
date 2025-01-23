# Snowflake SQL API¶

The Snowflake SQL API is a REST API that you can use to access and update data
in a Snowflake database. You can use this API to develop custom applications
and integrations that:

  * Perform queries

  * Manage your deployment (e.g. provision users and roles, create tables, etc.)

The Snowflake SQL API provides operations that you can use to:

  * Submit SQL statements for execution.

  * Check the status of the execution of a statement.

  * Cancel the execution of a statement.

You can use this API to execute [standard queries](../../sql-
reference/constructs) and most [DDL](../../sql-reference/sql-ddl-summary) and
[DML](../../sql-reference/sql-dml) statements. See [Limitations of the SQL
API](intro.html#label-sql-api-limitations) for the types of statements that
are not supported.

[Introduction to the SQL API](intro)

    

Get an overview of the API.

[About the SQL API endpoints](about-endpoints)

    

Learn about the endpoints that make up the API.

[Authenticating to the server](authenticating)

    

Use OAuth or Key Pair to authenticate with the Snowflake server.

[Submitting a request to execute SQL statements](submitting-requests)

    

Set up and submit requests using an API endpoint.

[Handling responses](handling-responses)

    

Check request status and get results and other data after a request.

[Submitting multiple SQL statements in a single request](submitting-multiple-
statements)

    

Send multiple SQL statements in a single API request.

[Creating and calling stored procedures](using-stored-procedures)

    

Create a stored procedure by specifying it in the body of a request.

[Using explicit transactions](using-transactions)

    

Execute SQL in a transaction by specifying the start, end, and statements in
the transaction.

[Getting details about an error](handling-errors)

    

Retrieve error information.

[Canceling the execution of a SQL statement](cancelling-requests)

    

Cancel SQL statement execution.

[Snowflake SQL API reference](reference)

    

Read details about the operations, objects, HTTP headers, and response codes
for this API.

[Deprecated functionality](sql-api-old)

    

Learn about deprecated functionality.

