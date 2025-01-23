# Writing stored procedures in Snowflake Scripting¶

This topic provides an introduction to writing a stored procedure in SQL by
using Snowflake Scripting. For more information about Snowflake Scripting, see
the [Snowflake Scripting Developer Guide](../snowflake-scripting/index).

## Introduction¶

To write a stored procedure that uses Snowflake Scripting:

  * Use the [CREATE PROCEDURE](../../sql-reference/sql/create-procedure) or [WITH … CALL …](../../sql-reference/sql/call-with) command with LANGUAGE SQL.

  * In the body of the stored procedure (the AS clause), you use a [Snowflake Scripting block](../snowflake-scripting/blocks).

Note

If you are creating a Snowflake Scripting procedure in [SnowSQL](../../user-
guide/snowsql) or the [Classic Console](../../user-guide/ui-using), you must
use [string literal delimiters](../../sql-reference/data-types-
text.html#label-quoted-string-constants) (`'` or `$$`) around the body of the
stored procedure.

For details, see [Using Snowflake Scripting in SnowSQL, the Classic Console,
and Python Connector](../snowflake-scripting/running-examples).

You can capture log and trace data as your handler code executes. For more
information, refer to [Logging, tracing, and metrics](../logging-
tracing/logging-tracing-overview).

Note the following:

  * The same rules around [caller’s rights vs. owner’s rights](stored-procedures-rights) apply to these stored procedures.

  * The same considerations and guidelines in [Working with stored procedures](stored-procedures-usage) apply to Snowflake Scripting stored procedures.

The following is an example of a simple stored procedure that returns the
value of the argument that is passed in:

    
    
    CREATE OR REPLACE PROCEDURE output_message(message VARCHAR)
    RETURNS VARCHAR NOT NULL
    LANGUAGE SQL
    AS
    BEGIN
      RETURN message;
    END;
    

Copy

Note: If you are using [SnowSQL](../../user-guide/snowsql), the [Classic
Console](../../user-guide/ui-using), or the `execute_stream` or
`execute_string` method in [Python Connector](../python-connector/python-
connector) code, use this example instead (see [Using Snowflake Scripting in
SnowSQL, the Classic Console, and Python Connector](../snowflake-
scripting/running-examples)):

    
    
    CREATE OR REPLACE PROCEDURE output_message(message VARCHAR)
    RETURNS VARCHAR NOT NULL
    LANGUAGE SQL
    AS
    $$
    BEGIN
      RETURN message;
    END;
    $$
    ;
    

Copy

The following is an example of calling the stored procedure:

    
    
    CALL output_message('Hello World');
    

Copy

The following is an example of creating and calling an anonymous stored
procedure by using the [WITH … CALL …](../../sql-reference/sql/call-with)
command:

    
    
    WITH anonymous_output_message AS PROCEDURE (message VARCHAR)
      RETURNS VARCHAR NOT NULL
      LANGUAGE SQL
      AS
      $$
      BEGIN
        RETURN message;
      END;
      $$
    CALL anonymous_output_message('Hello World');
    

Copy

Note that in an anonymous stored procedure, you must use [string literal
delimiters](../../sql-reference/data-types-text.html#label-quoted-string-
constants) (`'` or `$$`) around the body of the procedure.

## Using arguments passed to a stored procedure¶

If you pass in any arguments to your stored procedure, you can refer to those
arguments by name in any Snowflake Scripting expression. See the next sections
for more details:

  * Simple example of using arguments passed to a stored procedure

  * Using an argument in a SQL statement (binding)

  * Using an argument as an object identifier

  * Using an argument when building a string for a SQL statement

### Simple example of using arguments passed to a stored procedure¶

The following stored procedure uses the values of the arguments in
[IF](../../sql-reference/snowflake-scripting/if) and [RETURN](../../sql-
reference/snowflake-scripting/return) statements.

    
    
    CREATE OR REPLACE PROCEDURE return_greater(number_1 INTEGER, number_2 INTEGER)
    RETURNS INTEGER NOT NULL
    LANGUAGE SQL
    AS
    BEGIN
      IF (number_1 > number_2) THEN
        RETURN number_1;
      ELSE
        RETURN number_2;
      END IF;
    END;
    

Copy

Note: If you are using [SnowSQL](../../user-guide/snowsql), the [Classic
Console](../../user-guide/ui-using), or the `execute_stream` or
`execute_string` method in [Python Connector](../python-connector/python-
connector) code, use this example instead (see [Using Snowflake Scripting in
SnowSQL, the Classic Console, and Python Connector](../snowflake-
scripting/running-examples)):

    
    
    CREATE OR REPLACE PROCEDURE return_greater(number_1 INTEGER, number_2 INTEGER)
    RETURNS INTEGER NOT NULL
    LANGUAGE SQL
    AS
    $$
    BEGIN
      IF (number_1 > number_2) THEN
        RETURN number_1;
      ELSE
        RETURN number_2;
      END IF;
    END;
    $$
    ;
    

Copy

The following is an example of calling the stored procedure:

    
    
    CALL return_greater(2, 3);
    

Copy

### Using an argument in a SQL statement (binding)¶

As is the case with Snowflake Scripting variables, if you need to use an
argument in a SQL statement, put a colon (`:`) in front of the argument name.
(See [Using a variable in a SQL statement (binding)](../snowflake-
scripting/variables.html#label-snowscript-variables-binding).)

The following sections contain examples that use bind variables in stored
procedures:

  * Example that uses a bind variable in a WHERE clause

  * Example of using a bind variable to set the value of a property

  * Example that uses bind variables to set parameters in a command

#### Example that uses a bind variable in a WHERE clause¶

The following stored procedure uses the `id` argument in the WHERE clause of a
SELECT statement. In the WHERE clause, the argument is specified as `:id`.

    
    
    CREATE OR REPLACE PROCEDURE find_invoice_by_id(id VARCHAR)
    RETURNS TABLE (id INTEGER, price NUMBER(12,2))
    LANGUAGE SQL
    AS
    DECLARE
      res RESULTSET DEFAULT (SELECT * FROM invoices WHERE id = :id);
    BEGIN
      RETURN TABLE(res);
    END;
    

Copy

Note: If you are using [SnowSQL](../../user-guide/snowsql), the [Classic
Console](../../user-guide/ui-using), or the `execute_stream` or
`execute_string` method in [Python Connector](../python-connector/python-
connector) code, use this example instead (see [Using Snowflake Scripting in
SnowSQL, the Classic Console, and Python Connector](../snowflake-
scripting/running-examples)):

    
    
    CREATE OR REPLACE PROCEDURE find_invoice_by_id(id VARCHAR)
    RETURNS TABLE (id INTEGER, price NUMBER(12,2))
    LANGUAGE SQL
    AS
    $$
    DECLARE
      res RESULTSET DEFAULT (SELECT * FROM invoices WHERE id = :id);
    BEGIN
      RETURN TABLE(res);
    END;
    $$
    ;
    

Copy

The following is an example of calling the stored procedure:

    
    
    CALL find_invoice_by_id('2');
    

Copy

In addition, the [TO_QUERY](../../sql-reference/functions/to_query) function
provides a simple syntax for accepting a SQL string directly in the FROM
clause of a SELECT statement. For a comparison of the TO_QUERY function with
dynamic SQL, see [Constructing SQL at runtime](../../user-guide/querying-
construct-at-runtime).

#### Example of using a bind variable to set the value of a property¶

The following stored procedure uses the `comment` argument to add a comment
for a table in a CREATE TABLE statement. In the statement, the argument is
specified as `:comment`.

    
    
    CREATE OR REPLACE PROCEDURE test_bind_comment(comment VARCHAR)
    RETURNS STRING
    LANGUAGE SQL
    AS
    BEGIN
      CREATE OR REPLACE TABLE test_table_with_comment(a VARCHAR, n NUMBER) COMMENT = :comment;
    END;
    

Copy

Note: If you are using [SnowSQL](../../user-guide/snowsql), the [Classic
Console](../../user-guide/ui-using), or the `execute_stream` or
`execute_string` method in [Python Connector](../python-connector/python-
connector) code, use this example instead (see [Using Snowflake Scripting in
SnowSQL, the Classic Console, and Python Connector](../snowflake-
scripting/running-examples)):

    
    
    CREATE OR REPLACE PROCEDURE test_bind_comment(comment VARCHAR)
    RETURNS STRING
    LANGUAGE SQL
    AS
    $$
    BEGIN
      CREATE OR REPLACE TABLE test_table_with_comment(a VARCHAR, n NUMBER) COMMENT = :comment;
    END;
    $$
    ;
    

Copy

The following is an example of calling the stored procedure:

    
    
    CALL test_bind_comment('My Test Table');
    

Copy

View the comment for the table by querying the [TABLES view](../../sql-
reference/info-schema/tables) in the INFORMATION_SCHEMA:

    
    
    SELECT comment FROM information_schema.tables WHERE table_name='TEST_TABLE_WITH_COMMENT';
    

Copy

    
    
    +---------------+
    | COMMENT       |
    |---------------|
    | My Test Table |
    +---------------+
    

You can also view the comment by running a [SHOW TABLES](../../sql-
reference/sql/show-tables) command.

#### Example that uses bind variables to set parameters in a command¶

Assume you have a stage named `st` with CSV files:

    
    
    CREATE OR REPLACE STAGE st;
    PUT file://good_data.csv @st;
    PUT file://errors_data.csv @st;
    

Copy

You want to load the data in the CSV files into a table named
`test_bind_stage_and_load`:

    
    
    CREATE OR REPLACE TABLE test_bind_stage_and_load (a VARCHAR, b VARCHAR, c VARCHAR);
    

Copy

The following stored procedure uses the FROM, ON_ERROR, and VALIDATION_MODE
parameters in a [COPY INTO <table>](../../sql-reference/sql/copy-into-table)
statement. In the statement, the parameter values are specified as
`:my_stage_name`, `:on_error`, and `:valid_mode`, respectively.

    
    
    CREATE OR REPLACE PROCEDURE test_copy_files_validate(
      my_stage_name VARCHAR,
      on_error VARCHAR,
      valid_mode VARCHAR)
    RETURNS STRING
    LANGUAGE SQL
    AS
    BEGIN
      COPY INTO test_bind_stage_and_load
        FROM :my_stage_name
        ON_ERROR=:on_error
        FILE_FORMAT=(type='csv')
        VALIDATION_MODE=:valid_mode;
    END;
    

Copy

Note: If you are using [SnowSQL](../../user-guide/snowsql), the [Classic
Console](../../user-guide/ui-using), or the `execute_stream` or
`execute_string` method in [Python Connector](../python-connector/python-
connector) code, use this example instead (see [Using Snowflake Scripting in
SnowSQL, the Classic Console, and Python Connector](../snowflake-
scripting/running-examples)):

    
    
    CREATE OR REPLACE PROCEDURE test_copy_files_validate(
      my_stage_name VARCHAR,
      on_error VARCHAR,
      valid_mode VARCHAR)
    RETURNS STRING
    LANGUAGE SQL
    AS
    $$
    BEGIN
      COPY INTO test_bind_stage_and_load
        FROM :my_stage_name
        ON_ERROR=:on_error
        FILE_FORMAT=(type='csv')
        VALIDATION_MODE=:valid_mode;
    END;
    $$
    ;
    

Copy

The following is an example of calling the stored procedure:

    
    
    CALL test_copy_files_validate('@st', 'skip_file', 'return_all_errors');
    

Copy

### Using an argument as an object identifier¶

If you need to use an argument to refer to an object (e.g. a table name in the
FROM clause of a SELECT statement), use the [IDENTIFIER](../../sql-
reference/identifier-literal) keyword to indicate that the argument represents
an object identifier. For example:

    
    
    CREATE OR REPLACE PROCEDURE get_row_count(table_name VARCHAR)
    RETURNS INTEGER NOT NULL
    LANGUAGE SQL
    AS
    DECLARE
      row_count INTEGER DEFAULT 0;
      res RESULTSET DEFAULT (SELECT COUNT(*) AS COUNT FROM IDENTIFIER(:table_name));
      c1 CURSOR FOR res;
    BEGIN
      FOR row_variable IN c1 DO
        row_count := row_variable.count;
      END FOR;
      RETURN row_count;
    END;
    

Copy

Note: If you are using [SnowSQL](../../user-guide/snowsql), the [Classic
Console](../../user-guide/ui-using), or the `execute_stream` or
`execute_string` method in [Python Connector](../python-connector/python-
connector) code, use this example instead (see [Using Snowflake Scripting in
SnowSQL, the Classic Console, and Python Connector](../snowflake-
scripting/running-examples)):

    
    
    CREATE OR REPLACE PROCEDURE get_row_count(table_name VARCHAR)
    RETURNS INTEGER NOT NULL
    LANGUAGE SQL
    AS
    $$
    DECLARE
      row_count INTEGER DEFAULT 0;
      res RESULTSET DEFAULT (SELECT COUNT(*) AS COUNT FROM IDENTIFIER(:table_name));
      c1 CURSOR FOR res;
    BEGIN
      FOR row_variable IN c1 DO
        row_count := row_variable.count;
      END FOR;
      RETURN row_count;
    END;
    $$
    ;
    

Copy

The following is an example of calling the stored procedure:

    
    
    CALL get_row_count('invoices');
    

Copy

This example executes a CREATE TABLE … AS SELECT (CTAS) statement in a stored
procedure based on the table names provided in arguments.

    
    
    CREATE OR REPLACE PROCEDURE ctas_sp(existing_table VARCHAR, new_table VARCHAR)
      RETURNS TEXT
      LANGUAGE SQL
    AS
    BEGIN
      CREATE OR REPLACE TABLE IDENTIFIER(:new_table) AS
        SELECT * FROM IDENTIFIER(:existing_table);
      RETURN 'Table created';
    END;
    

Copy

Note: If you are using [SnowSQL](../../user-guide/snowsql), the [Classic
Console](../../user-guide/ui-using), or the `execute_stream` or
`execute_string` method in [Python Connector](../python-connector/python-
connector) code, use this example instead (see [Using Snowflake Scripting in
SnowSQL, the Classic Console, and Python Connector](../snowflake-
scripting/running-examples)):

    
    
    CREATE OR REPLACE PROCEDURE ctas_sp(existing_table VARCHAR, new_table VARCHAR)
      RETURNS TEXT
      LANGUAGE SQL
    AS
    $$
    BEGIN
      CREATE OR REPLACE TABLE IDENTIFIER(:new_table) AS
        SELECT * FROM IDENTIFIER(:existing_table);
      RETURN 'Table created';
    END;
    $$
    ;
    

Copy

Before calling the procedure, create a simple table and insert data:

    
    
    CREATE OR REPLACE TABLE test_table_for_ctas_sp (
      id NUMBER(2),
      v  VARCHAR(2))
    AS SELECT
      column1,
      column2,
    FROM
      VALUES
        (1, 'a'),
        (2, 'b'),
        (3, 'c');
    

Copy

Call the stored procedure to create a new table that is based on this table:

    
    
    CALL ctas_sp('test_table_for_ctas_sp', 'test_table_for_ctas_sp_backup');
    

Copy

### Using an argument when building a string for a SQL statement¶

Note that if you are building a SQL statement as a string to be passed to
[EXECUTE IMMEDIATE](../../sql-reference/sql/execute-immediate) (see [Assigning
a query to a declared RESULTSET](../snowflake-scripting/resultsets.html#label-
snowscript-resultsets-assign)), do not prefix the argument with a colon. For
example:

    
    
    CREATE OR REPLACE PROCEDURE find_invoice_by_id_via_execute_immediate(id VARCHAR)
    RETURNS TABLE (id INTEGER, price NUMBER(12,2))
    LANGUAGE SQL
    AS
    DECLARE
      select_statement VARCHAR;
      res RESULTSET;
    BEGIN
      select_statement := 'SELECT * FROM invoices WHERE id = ' || id;
      res := (EXECUTE IMMEDIATE :select_statement);
      RETURN TABLE(res);
    END;
    

Copy

## Returning tabular data¶

If you need to return tabular data (e.g. data from a RESULTSET) from your
stored procedure, specify RETURNS TABLE(…) in your [CREATE
PROCEDURE](../../sql-reference/sql/create-procedure) statement.

If you know the [Snowflake data types](../../sql-reference-data-types) of the
columns in the returned table, specify the column names and types in the
RETURNS TABLE().

    
    
    CREATE OR REPLACE PROCEDURE get_top_sales()
    RETURNS TABLE (sales_date DATE, quantity NUMBER)
    ...
    

Copy

Otherwise (e.g. if you are determining the column types during run time), you
can omit the column names and types:

    
    
    CREATE OR REPLACE PROCEDURE get_top_sales()
    RETURNS TABLE ()
    ...
    

Copy

Note

Currently, in the `RETURNS TABLE(...)` clause, you can’t specify GEOGRAPHY as
a column type. This applies whether you are creating a stored or anonymous
procedure.

    
    
    CREATE OR REPLACE PROCEDURE test_return_geography_table_1()
      RETURNS TABLE(g GEOGRAPHY)
      ...
    

Copy

    
    
    WITH test_return_geography_table_1() AS PROCEDURE
      RETURNS TABLE(g GEOGRAPHY)
      ...
    CALL test_return_geography_table_1();
    

Copy

If you attempt to specify GEOGRAPHY as a column type, calling the stored
procedure results in the error:

    
    
    Stored procedure execution error: data type of returned table does not match expected returned table type
    

Copy

To work around this issue, you can omit the column arguments and types in
`RETURNS TABLE()`.

    
    
    CREATE OR REPLACE PROCEDURE test_return_geography_table_1()
      RETURNS TABLE()
      ...
    

Copy

    
    
    WITH test_return_geography_table_1() AS PROCEDURE
      RETURNS TABLE()
      ...
    CALL test_return_geography_table_1();
    

Copy

If you need to return the data in a RESULTSET, use TABLE() in your
[RETURN](../../sql-reference/snowflake-scripting/return) statement.

For example:

    
    
    CREATE OR REPLACE PROCEDURE get_top_sales()
    RETURNS TABLE (sales_date DATE, quantity NUMBER)
    LANGUAGE SQL
    AS
    DECLARE
      res RESULTSET DEFAULT (SELECT sales_date, quantity FROM sales ORDER BY quantity DESC LIMIT 10);
    BEGIN
      RETURN TABLE(res);
    END;
    

Copy

Note: If you are using [SnowSQL](../../user-guide/snowsql), the [Classic
Console](../../user-guide/ui-using), or the `execute_stream` or
`execute_string` method in [Python Connector](../python-connector/python-
connector) code, use this example instead (see [Using Snowflake Scripting in
SnowSQL, the Classic Console, and Python Connector](../snowflake-
scripting/running-examples)):

    
    
    CREATE OR REPLACE PROCEDURE get_top_sales()
    RETURNS TABLE (sales_date DATE, quantity NUMBER)
    LANGUAGE SQL
    AS
    $$
    DECLARE
      res RESULTSET DEFAULT (SELECT sales_date, quantity FROM sales ORDER BY quantity DESC LIMIT 10);
    BEGIN
      RETURN TABLE(res);
    END;
    $$
    ;
    

Copy

The following is an example of calling the stored procedure:

    
    
    CALL get_top_sales();
    

Copy

## Calling a stored procedure from another stored procedure¶

In a stored procedure, if you need to call another stored procedure, use one
of the following approaches:

  * Calling a stored procedure without using the returned value

  * Using the value returned from a stored procedure call

### Calling a stored procedure without using the returned value¶

Use a [CALL](../../sql-reference/sql/call) statement to call the stored
procedure (as you normally would).

If you need to pass in any variables or arguments as input arguments in the
CALL statement, remember to use a colon (`:`) in front of the variable name.
(See [Using a variable in a SQL statement (binding)](../snowflake-
scripting/variables.html#label-snowscript-variables-binding).)

The following is an example of a stored procedure that calls another stored
procedure but does not depend on the return value.

First, create a table for use in the example:

    
    
    -- Create a table for use in the example.
    CREATE OR REPLACE TABLE int_table (value INTEGER);
    

Copy

Then, create the stored procedure that you will call from another stored
procedure:

    
    
    -- Create a stored procedure to be called from another stored procedure.
    CREATE OR REPLACE PROCEDURE insert_value(value INTEGER)
    RETURNS VARCHAR NOT NULL
    LANGUAGE SQL
    AS
    BEGIN
      INSERT INTO int_table VALUES (:value);
      RETURN 'Rows inserted: ' || SQLROWCOUNT;
    END;
    

Copy

Note: If you are using [SnowSQL](../../user-guide/snowsql), the [Classic
Console](../../user-guide/ui-using), or the `execute_stream` or
`execute_string` method in [Python Connector](../python-connector/python-
connector) code, use this example instead (see [Using Snowflake Scripting in
SnowSQL, the Classic Console, and Python Connector](../snowflake-
scripting/running-examples)):

    
    
    -- Create a stored procedure to be called from another stored procedure.
    CREATE OR REPLACE PROCEDURE insert_value(value INTEGER)
    RETURNS VARCHAR NOT NULL
    LANGUAGE SQL
    AS
    $$
    BEGIN
      INSERT INTO int_table VALUES (:value);
      RETURN 'Rows inserted: ' || SQLROWCOUNT;
    END;
    $$
    ;
    

Copy

Next, create a second stored procedure that calls the first stored procedure:

    
    
    CREATE OR REPLACE PROCEDURE insert_two_values(value1 INTEGER, value2 INTEGER)
    RETURNS VARCHAR NOT NULL
    LANGUAGE SQL
    AS
    BEGIN
      CALL insert_value(:value1);
      CALL insert_value(:value2);
      RETURN 'Finished calling stored procedures';
    END;
    

Copy

Note: If you are using [SnowSQL](../../user-guide/snowsql), the [Classic
Console](../../user-guide/ui-using), or the `execute_stream` or
`execute_string` method in [Python Connector](../python-connector/python-
connector) code, use this example instead (see [Using Snowflake Scripting in
SnowSQL, the Classic Console, and Python Connector](../snowflake-
scripting/running-examples)):

    
    
    CREATE OR REPLACE PROCEDURE insert_two_values(value1 INTEGER, value2 INTEGER)
    RETURNS VARCHAR NOT NULL
    LANGUAGE SQL
    AS
    $$
    BEGIN
      CALL insert_value(:value1);
      CALL insert_value(:value2);
      RETURN 'Finished calling stored procedures';
    END;
    $$
    ;
    

Copy

Finally, call the second stored procedure:

    
    
    CALL insert_two_values(4, 5);
    

Copy

### Using the value returned from a stored procedure call¶

If are calling a stored procedure that returns a scalar value and you need to
access that value, use the `INTO :_snowflake_scripting_variable_` clause in
the [CALL](../../sql-reference/sql/call) statement to capture the value in a
[Snowflake Scripting variable](../snowflake-scripting/variables).

The following example calls the `get_row_count` stored procedure that was
defined in Using an argument as an object identifier.

    
    
    CREATE OR REPLACE PROCEDURE count_greater_than(table_name VARCHAR, maximum_count INTEGER)
      RETURNS BOOLEAN NOT NULL
      LANGUAGE SQL
      AS
      DECLARE
        count1 NUMBER;
      BEGIN
        CALL get_row_count(:table_name) INTO :count1;
        IF (:count1 > maximum_count) THEN
          RETURN TRUE;
        ELSE
          RETURN FALSE;
        END IF;
      END;
    

Copy

Note: If you are using [SnowSQL](../../user-guide/snowsql), the [Classic
Console](../../user-guide/ui-using), or the `execute_stream` or
`execute_string` method in [Python Connector](../python-connector/python-
connector) code, use this example instead (see [Using Snowflake Scripting in
SnowSQL, the Classic Console, and Python Connector](../snowflake-
scripting/running-examples)):

    
    
    CREATE OR REPLACE PROCEDURE count_greater_than(table_name VARCHAR, maximum_count INTEGER)
      RETURNS BOOLEAN NOT NULL
      LANGUAGE SQL
      AS
      $$
      DECLARE
        count1 NUMBER;
      BEGIN
        CALL get_row_count(:table_name) INTO :count1;
        IF (:count1 > maximum_count) THEN
          RETURN TRUE;
        ELSE
          RETURN FALSE;
        END IF;
      END;
      $$
      ;
    

Copy

The following is an example of calling the stored procedure:

    
    
    CALL count_greater_than('invoices', 3);
    

Copy

If the stored procedure returns a table, you can capture the return value by
setting a [RESULTSET](../snowflake-scripting/resultsets) to a string
containing the CALL statement. (See [Assigning a query to a declared
RESULTSET](../snowflake-scripting/resultsets.html#label-snowscript-resultsets-
assign).)

To retrieve the return value from the call, you can use a [CURSOR for the
RESULTSET](../snowflake-scripting/resultsets.html#label-snowscript-resultsets-
use-cursor). For example:

    
    
    DECLARE
      res1 RESULTSET;
    BEGIN
    res1 := (CALL my_procedure());
    LET c1 CURSOR FOR res1;
    FOR row_variable IN c1 DO
      IF (row_variable.col1 > 0) THEN
        ...;
      ELSE
        ...;
      END IF;
    END FOR;
    ...
    

Copy

## Using and setting SQL variables in a stored procedure¶

By default, Snowflake Scripting stored procedures run with owner’s rights.
When a stored procedure runs with owner’s rights, it can’t access [SQL (or
session) variables](../../sql-reference/session-variables).

However, a caller’s rights stored procedure can read the caller’s session
variables and use them in the logic of the stored procedure. For example, a
caller’s rights stored procedure can use the value in a SQL variable in a
query. To create a stored procedure that runs with caller’s rights, specify
the `EXECUTE AS CALLER` parameter in the [CREATE PROCEDURE](../../sql-
reference/sql/create-procedure) statement.

These examples illustrate this key difference between caller’s rights and
owner’s rights stored procedures. They attempt to use SQL variables in two
ways:

  * Set a SQL variable before calling the stored procedure, then use the SQL variable inside the stored procedure.

  * Set a SQL variable inside the stored procedure, then use the SQL variable after returning from the stored procedure.

Both using the SQL variable and setting the SQL variable work correctly in a
caller’s rights stored procedure. Both fail when using an owner’s rights
stored procedure, even if the caller is the owner.

For more information about owner’s rights and caller’s rights, see
[Understanding caller’s rights and owner’s rights stored procedures](stored-
procedures-rights).

### Using a SQL variable in a stored procedure¶

This example uses a SQL variable in a stored procedure.

First, set a SQL variable in a session:

    
    
    SET example_use_variable = 2;
    

Copy

Create a simple stored procedure that runs with caller’s rights and uses this
SQL variable:

    
    
    CREATE OR REPLACE PROCEDURE use_sql_variable_proc()
    RETURNS NUMBER
    LANGUAGE SQL
    EXECUTE AS CALLER
    AS
    DECLARE
      sess_var_x_2 NUMBER;
    BEGIN
      sess_var_x_2 := 2 * $example_use_variable;
      RETURN sess_var_x_2;
    END;
    

Copy

Note: If you are using [SnowSQL](../../user-guide/snowsql), the [Classic
Console](../../user-guide/ui-using), or the `execute_stream` or
`execute_string` method in [Python Connector](../python-connector/python-
connector) code, use this example instead (see [Using Snowflake Scripting in
SnowSQL, the Classic Console, and Python Connector](../snowflake-
scripting/running-examples)):

    
    
    CREATE OR REPLACE PROCEDURE use_sql_variable_proc()
    RETURNS NUMBER
    LANGUAGE SQL
    EXECUTE AS CALLER
    AS
    $$
    DECLARE
      sess_var_x_2 NUMBER;
    BEGIN
      sess_var_x_2 := 2 * $example_use_variable;
      RETURN sess_var_x_2;
    END;
    $$
    ;
    

Copy

Call the stored procedure:

    
    
    CALL use_sql_variable_proc();
    

Copy

    
    
    +-----------------------+
    | USE_SQL_VARIABLE_PROC |
    |-----------------------|
    |                     4 |
    +-----------------------+
    

Set the SQL variable to a different value:

    
    
    SET example_use_variable = 9;
    

Copy

Call the procedure again to see that the returned value has changed:

    
    
    CALL use_sql_variable_proc();
    

Copy

    
    
    +-----------------------+
    | USE_SQL_VARIABLE_PROC |
    |-----------------------|
    |                    18 |
    +-----------------------+
    

### Setting a SQL variable in a stored procedure¶

You can set a SQL variable in a stored procedure that’s running with caller’s
rights. For more information, including guidelines for using SQL variables in
stored procedures, see [Caller’s rights stored procedures](stored-procedures-
rights.html#label-stored-procedure-session-state-caller).

Note

Although you can set a SQL variable inside a stored procedure and leave it set
after the end of the procedure, Snowflake does not recommend doing this.

This example sets a SQL variable in a stored procedure.

First, set a SQL variable in a session:

    
    
    SET example_set_variable = 55;
    

Copy

Confirm the value of the SQL variable:

    
    
    SHOW VARIABLES LIKE 'example_set_variable';
    

Copy

    
    
    +----------------+-------------------------------+-------------------------------+----------------------+-------+-------+---------+
    |     session_id | created_on                    | updated_on                    | name                 | value | type  | comment |
    |----------------+-------------------------------+-------------------------------+----------------------+-------+-------+---------|
    | 10363782631910 | 2024-11-27 08:18:32.007 -0800 | 2024-11-27 08:20:17.255 -0800 | EXAMPLE_SET_VARIABLE | 55    | fixed |         |
    +----------------+-------------------------------+-------------------------------+----------------------+-------+-------+---------+
    

For example, the following stored procedure sets the SQL variable
`example_set_variable` to a new value and returns the new value:

    
    
    CREATE OR REPLACE PROCEDURE set_sql_variable_proc()
    RETURNS NUMBER
    LANGUAGE SQL
    EXECUTE AS CALLER
    AS
    BEGIN
      SET example_set_variable = $example_set_variable - 3;
      RETURN $example_set_variable;
    END;
    

Copy

Note: If you are using [SnowSQL](../../user-guide/snowsql), the [Classic
Console](../../user-guide/ui-using), or the `execute_stream` or
`execute_string` method in [Python Connector](../python-connector/python-
connector) code, use this example instead (see [Using Snowflake Scripting in
SnowSQL, the Classic Console, and Python Connector](../snowflake-
scripting/running-examples)):

    
    
    CREATE OR REPLACE PROCEDURE set_sql_variable_proc()
    RETURNS NUMBER
    LANGUAGE SQL
    EXECUTE AS CALLER
    AS
    $$
    BEGIN
      SET example_set_variable = $example_set_variable - 3;
      RETURN $example_set_variable;
    END;
    $$
    ;
    

Copy

Call the stored procedure:

    
    
    CALL set_sql_variable_proc();
    

Copy

    
    
    +-----------------------+
    | SET_SQL_VARIABLE_PROC |
    |-----------------------|
    |                    52 |
    +-----------------------+
    

Confirm the new value of the SQL variable:

    
    
    SHOW VARIABLES LIKE 'example_set_variable';
    

Copy

    
    
    +----------------+-------------------------------+-------------------------------+----------------------+-------+-------+---------+
    |     session_id | created_on                    | updated_on                    | name                 | value | type  | comment |
    |----------------+-------------------------------+-------------------------------+----------------------+-------+-------+---------|
    | 10363782631910 | 2024-11-27 08:18:32.007 -0800 | 2024-11-27 08:24:04.027 -0800 | EXAMPLE_SET_VARIABLE | 52    | fixed |         |
    +----------------+-------------------------------+-------------------------------+----------------------+-------+-------+---------+
    

