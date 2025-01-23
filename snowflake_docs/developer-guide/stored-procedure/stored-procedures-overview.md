# Stored procedures overview¶

You can write stored procedures to extend the system with procedural code that
executes SQL. In a stored procedure, you can use programmatic constructs to
perform branching and looping. Once you create a stored procedure, you can
reuse it multiple times.

You write a procedure’s logic – its handler – in one of the supported
languages. Once you have a handler, you can [create a procedure](stored-
procedures-creating-sql) with a CREATE PROCEDURE command, then [call the
procedure](stored-procedures-calling) with a CALL statement.

From a stored procedure, you can return a single value or (where supported
with the handler language) tabular data. For more information about supported
return types, see [CREATE PROCEDURE](../../sql-reference/sql/create-
procedure).

Note

To both create and call an anonymous procedure, use [CALL (with anonymous
procedure)](../../sql-reference/sql/call-with). Creating and calling an
anonymous procedure does not require a role with CREATE PROCEDURE schema
privileges.

Note

A stored procedure is like a UDF, but the two differ in important ways. For
more information, see [Choosing whether to write a stored procedure or a user-
defined function](../stored-procedures-vs-udfs).

## What is a stored procedure?¶

A stored procedure contains logic you write so you can call it from SQL. A
stored procedure’s logic typically performs database operations by executing
SQL statements.

With a stored procedure, you can also:

  * Dynamically create and execute SQL statements.

  * Execute code with the privileges of the role that owns the procedure, rather than with the privileges of the role that runs the procedure.

This allows the stored procedure owner to delegate the power to perform
specified operations to users who otherwise could not do so. However, there
are limitations on these owner’s rights stored procedures.

You might want to use a stored procedure to automate a task that requires
multiple SQL statements and is performed frequently. For example, imagine that
you want to clean up a database by deleting data older than a specified date.
You can write multiple DELETE statements, each of which deletes data from a
specific table. You can put all of those statements in a single stored
procedure and pass a parameter that specifies the cut-off date. Then you can
simply call the procedure to clean up the database. As your database changes,
you can update the procedure to clean up additional tables; if there are
multiple users who use the cleanup command, they can call one procedure,
rather than remember every table name and clean up each table individually.

## Stored procedure example¶

Code in the following example creates a stored procedure called `myproc` with
a Python handler called `run`.

    
    
    CREATE OR REPLACE PROCEDURE myproc(from_table STRING, to_table STRING, count INT)
      RETURNS STRING
      LANGUAGE PYTHON
      RUNTIME_VERSION = '3.9'
      PACKAGES = ('snowflake-snowpark-python')
      HANDLER = 'run'
    as
    $$
    def run(session, from_table, to_table, count):
      session.table(from_table).limit(count).write.save_as_table(to_table)
      return "SUCCESS"
    $$;
    

Copy

Code in the following example calls the stored procedure `myproc`.

    
    
    CALL myproc('table_a', 'table_b', 5);
    

Copy

## Supported languages¶

You write a procedure’s handler – its logic – in any of several programming
languages. Each language allows you to manipulate data within the constraints
of the language and its runtime environment. Regardless of the handler
language, you create the procedure itself in the same way using SQL,
specifying your handler and handler language.

You can write a handler in any of the following languages:

Language | Developer Guide  
---|---  
Java (using the Snowpark API) | [Writing stored procedures in Java](stored-procedures-java)  
JavaScript | [Writing stored procedures in JavaScript](stored-procedures-javascript)  
Python (using the Snowpark API) | [Writing stored procedures in Python](python/procedure-python-overview)  
Scala (using the Snowpark API) | [Writing stored procedures in Scala](stored-procedures-scala)  
Snowflake Scripting (SQL) | [Writing stored procedures in Snowflake Scripting](stored-procedures-snowflake-scripting)  
  
### Language choice¶

You write a procedure’s handler – its logic – in any of several programming
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

When choosing a language, consider also the handler locations supported. Not
all languages support referring to the handler on a stage (the handler code
must instead be in-line). For more information, see [Keeping handler code in-
line or on a stage](../inline-or-staged).

Language | Handler Location  
---|---  
Java | In-line or staged  
JavaScript | In-line  
Python | In-line or staged  
Scala | In-line or staged  
Snowflake Scripting | In-line  
  
## Developer guides¶

### Guidelines and constraints¶

Tips:

    

For tips on writing stored procedures, see [Working with stored
procedures](stored-procedures-usage).

Snowflake constraints:

    

You can ensure stability within the Snowflake environment by developing within
Snowflake constraints. For more information, see [Designing Handlers that Stay
Within Snowflake-Imposed Constraints](../udf-stored-procedure-constraints).

Naming:

    

Be sure to name procedures in a way that avoids collisions with other
procedures. For more information, see [Naming and overloading procedures and
UDFs](../udf-stored-procedure-naming-conventions).

Arguments:

    

Specify the arguments for your stored procedure and indicate which arguments
are optional. For more information, see [Defining arguments for UDFs and
stored procedures](../udf-stored-procedure-arguments).

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

Whether you choose to have a stored procedure run with caller’s rights or
owner’s rights can impact the information it has access to and the tasks it
may be allowed to perform. For more information, see [Understanding caller’s
rights and owner’s rights stored procedures](stored-procedures-rights).

Stored procedures share certain security concerns with user-defined functions
(UDFs). For more information, see the following:

  * You can help a procedure’s handler code execute securely by following the best practices described in [Security Practices for UDFs and Procedures](../udf-stored-procedure-security-practices)

  * Ensure that sensitive information is concealed from users who should not have access to it. For more information, see [Protecting Sensitive Information with Secure UDFs and Stored Procedures](../secure-udf-procedure)

### Handler code deployment¶

When creating a procedure, you can specify its handler – which implements the
procedure’s logic – as code in-line with the CREATE PROCEDURE statement or as
code external to the statement, such as compiled code packaged and copied to a
stage.

For more information, see [Keeping handler code in-line or on a
stage](../inline-or-staged).

## Create and call procedures¶

You use SQL to create and call a procedure.

  * Once you have written handler code, you can create a stored procedure by executing the CREATE PROCEDURE statement, specifying the procedure’s handler. For more information, see [Creating a stored procedure](stored-procedures-creating-sql).

  * To call a procedure, execute a SQL CALL statement that specifies the procedure. For more information, see [Calling a stored procedure](stored-procedures-calling).

  * To create a temporary procedure that executes only once and is discarded, use WITH…CALL . For more information, see [CALL (with anonymous procedure)](../../sql-reference/sql/call-with).

