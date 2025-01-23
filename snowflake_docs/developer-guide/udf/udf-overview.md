# User-defined functions overview¶  
  
You can write user-defined functions (UDFs) to extend the system to perform
operations that are not available through the built-in system-defined
functions provided by Snowflake. Once you create a UDF, you can reuse it
multiple times.

A UDF is just one way to extend Snowflake. For others, see the following:

  * [Stored procedures overview](../stored-procedure/stored-procedures-overview)

  * [Writing external functions](../../sql-reference/external-functions)

  * [Snowpark API](../snowpark/index)

Note

A UDF is like a stored procedure, but the two differ in important ways. For
more information, see [Choosing whether to write a stored procedure or a user-
defined function](../stored-procedures-vs-udfs).

## What is a user-defined function (UDF)?¶

A user-defined function (UDF) is a function you define, which can be called in
a similar way to [built-in functions](../../sql-reference/intro-summary-
operators-functions). You can write UDFs in SQL or other supported languages,
and you can call a function written in one language from code written in
another. You can use UDFs to extend built-in functions or to encapsulate
calculations that are standard for your organization.

You write a UDF’s logic – its handler – in one of the supported languages.
Once you have a handler, you can [create a UDF](udf-creating-sql) with a
CREATE FUNCTION command, then [call the UDF](udf-calling-sql) with a SELECT
statement.

### Scalar and tabular functions¶

You can write a UDF that returns a single value (a scalar UDF) or that returns
a tabular value (a user-defined table function, or UDTF).

  * A _scalar_ function (UDF) returns one output row for each input row. The returned row consists of a single column/value.

  * A _tabular_ function (UDTF) returns a tabular value for each input row. In the handler for a UDTF, you write methods that conform to an interface required by Snowflake. These methods will:

    * Process each row in a partition (required).

    * Initialize the handler once for each partition (optional).

    * Finalize processing for each partition (optional).

The names of the methods vary by handler language. For a list of supported
languages, see Supported languages.

### Considerations¶

  * If a query calls a UDF to access staged files, the operation fails with a user error if the SQL statement also queries a view that calls any UDF or UDTF, regardless of whether the function in the view accesses staged files or not.

  * UDTFs can process multiple files in parallel; however, UDFs currently process files serially. As a workaround, group rows in a subquery using the [GROUP BY](../../sql-reference/constructs/group-by) clause. See [Process a CSV with a UDTF](../../user-guide/unstructured-data-java.html#label-unstructured-udtf-examples) for an example.

  * Currently, if staged files referenced in a query are modified or deleted while the query is running, the function call fails with an error.

  * If you specify the [CURRENT_DATABASE](../../sql-reference/functions/current_database) or [CURRENT_SCHEMA](../../sql-reference/functions/current_schema) function in the handler code of the UDF, the function returns the database or schema that contains the UDF, not the database or schema in use for the session.

## Get started¶

For a tutorial through which you write a UDTF with a handler written in SQL,
see [Quickstart: Getting Started With User-Defined SQL
Functions](https://quickstarts.snowflake.com/guide/getting_started_with_user_defined_sql_functions/?index=..%2F..index#0)

## UDF example¶

Code in the following example creates a UDF called `addone` with a handler
written in Python. The handler function is `addone_py`. This UDF returns an
`int`.

    
    
    CREATE OR REPLACE FUNCTION addone(i int)
    RETURNS INT
    LANGUAGE PYTHON
    RUNTIME_VERSION = '3.9'
    HANDLER = 'addone_py'
    as
    $$
    def addone_py(i):
      return i+1
    $$;
    

Copy

Code in the following example executes the `addone` UDF.

    
    
    SELECT addone(3);
    

Copy

## Supported languages¶

You write a function’s handler – its logic – in any of several programming
languages. Each language allows you to manipulate data within the constraints
of the language and its runtime environment. Regardless of the handler
language, you create the procedure itself in the same way using SQL,
specifying your handler and handler language.

You can write a handler in any of the following languages:

Language | Developer Guides  
---|---  
Java | 

  * [Java UDFs](java/udf-java-introduction)
  * [Java UDTFs](java/udf-java-tabular-functions)

  
JavaScript | 

  * [JavaScript UDFs](javascript/udf-javascript-introduction)
  * [JavaScript UDTFs](javascript/udf-javascript-tabular-functions)

  
Python | 

  * [Python UDFs](python/udf-python-introduction)
  * [Python UDTFs](python/udf-python-tabular-functions)

  
Scala | 

  * [Scala UDFs](scala/udf-scala-introduction)

  
SQL | 

  * [SQL UDFs](sql/udf-sql-introduction)
  * [SQL UDTFs](sql/udf-sql-tabular-functions)

  
  
### Language choice¶

You write a UDF’s handler – its logic – in any of several programming
languages. Each language allows you to manipulate data within the constraints
of the language and its runtime environment.

You might choose a particular language if:

  * You already have code in that language.

For example, if you already have a Java method that will work as a handler,
and the method’s object is in a .jar file, you could copy the .jar to a stage,
specify the handler as the class and method, then specify the language as
Java.

  * The language has capabilities that others don’t have.

  * The language has libraries that can help you do the processing that you need to do.

When choosing a language, consider also the following:

  * **Handler locations supported.** Not all languages support referring to the handler on a stage (the handler code must instead be in-line). For more information, see [Keeping handler code in-line or on a stage](../inline-or-staged).

  * **Whether the handler results in a UDF that’s sharable.** A sharable UDF can be used with the Snowflake [Secure Data Sharing](../../user-guide/data-sharing-intro) feature.

Language | Handler Location | Sharable  
---|---|---  
Java | In-line or staged | No [1]  
JavaScript | In-line | Yes  
Python | In-line or staged | No [2]  
Scala | In-line or staged | No [3]  
SQL | In-line | Yes  
[1]

For more information about limits on sharing Java UDFs, see [General
limitations](java/udf-java-limitations.html#label-limitations-on-java-udfs).

[2]

For more information about limits on sharing Python UDFs, see [General
limitations](python/udf-python-limitations.html#label-limitations-on-python-
udfs).

[3]

For more information about limits on sharing Scala UDFs, see [Scala UDF
limitations](scala/udf-scala-limitations).

## Developer guides¶

### Guidelines and constraints¶

Snowflake constraints:

    

You can ensure stability within the Snowflake environment by developing within
Snowflake constraints. For more information, see [Designing Handlers that Stay
Within Snowflake-Imposed Constraints](../udf-stored-procedure-constraints).

Naming:

    

Be sure to name functions in a way that avoids collisions with other
functions. For more information, see [Naming and overloading procedures and
UDFs](../udf-stored-procedure-naming-conventions).

Arguments:

    

Specify the arguments and indicate which arguments are optional. For more
information, see [Defining arguments for UDFs and stored procedures](../udf-
stored-procedure-arguments).

Data type mappings:

    

For each handler language, there’s a separate set of mappings between the
language’s data types and the SQL types used for arguments and return values.
For more about the mappings for each language, see [Data Type Mappings Between
SQL and Handler Languages](../udf-stored-procedure-data-type-mapping).

### Handler writing¶

Handler languages:

    

For language-specific content on writing a handler, see Supported languages.

External network access:

    

You can access external network locations with [external network
access](../external-network-access/external-network-access-overview). You can
create secure access to specific network locations external to Snowflake, then
use that access from within the handler code.

Logging and tracing:

    

You can record code activity by [capturing log messages and trace
events](../logging-tracing/logging-tracing-overview), storing the data in a
database you can query later.

### Security¶

You can grant privileges on objects needed for them to perform specific SQL
actions with a UDF or UDTF. For more information, see [Granting privileges for
user-defined functions](udf-access-control)

Functions share certain security concerns with stored procedures. For more
information, see the following:

  * You can help a procedure’s handler code execute securely by following the best practices described in [Security Practices for UDFs and Procedures](../udf-stored-procedure-security-practices)

  * Ensure that sensitive information is concealed from users who should not have access to it. For more information, see [Protecting Sensitive Information with Secure UDFs and Stored Procedures](../secure-udf-procedure)

### Handler code deployment¶

When creating a function, you can specify its handler – which implements the
function’s logic – as code in-line with the CREATE FUNCTION statement or as
code external to the statement, such as compiled code packaged and copied to a
stage.

For more information, see [Keeping handler code in-line or on a
stage](../inline-or-staged).

## Create and call functions¶

You use SQL to create and call a user-defined function.

  * To create a function, execute the CREATE FUNCTION statement, specifying the function’s handler. For more information, see [Creating a UDF](udf-creating-sql).

  * To call a function, execute a SQL SELECT statement that specifies the function as a parameter. For more information, see [Calling a UDF](udf-calling-sql).

