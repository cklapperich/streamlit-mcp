# Session context in Snowflake Notebooks¶

Feature — Generally Available

Generally available in Amazon Web Services (AWS), Microsoft Azure, and Google
Cloud Platform (GCP) commercial regions.

The session context of a notebook is defined by the role, warehouse, database,
and schema that you defined when you created the notebook. When you run the
notebook, it runs as that role, using the warehouse defined in the notebook,
and in the context of the database and schema that contain the notebook.

This topic describes how to access or change the session context of your
notebook.

## Accessing the session context for a notebook¶

You can access the session context using both Python and SQL.

If you’re using the Snowpark Python library or Snowflake Python APIs, use the
[get_active_session()](https://docs.snowflake.com/developer-
guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.context.get_active_session)
method to get the active session context.

    
    
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
    

Copy

For SQL, you can use the [Context functions](../../sql-reference/functions-
context) SQL functions.

    
    
    SELECT CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA();
    

Copy

## Changing the session context for a notebook¶

You can change the session context of the notebook to use a different role,
database and schema, and/or warehouse:

  * Specify a different role to use with the [USE ROLE](../../sql-reference/sql/use-role) SQL command.

    * You can check the role in use by the notebook by calling the [CURRENT_ROLE](../../sql-reference/functions/current_role) function.

    * If you change your role to one that does not have privileges to use the notebook warehouse, database, or schema, queries that require a warehouse or access to the notebook database or schema fail to run. However, you can still run queries that do not use the notebook warehouse, database, and schema.

    * Roles specified with the [USE ROLE](../../sql-reference/sql/use-role) SQL command do not persist across notebook sessions.

    * If you specify a database or schema that the currently active role does not have privileges to access, queries using that database and schema fail to run.

  * If you run the SQL command [USE SECONDARY ROLES](../../sql-reference/sql/use-secondary-roles) to set secondary roles to ALL, the secondary roles associated with your user are used to generate the results of the notebook cells.

  * Specify a different warehouse using the SQL command [USE WAREHOUSE](../../sql-reference/sql/use-warehouse).

    * You can check the warehouse in use for the notebook by calling the [CURRENT_WAREHOUSE](../../sql-reference/functions/current_warehouse) function.

  * Specify a different database or schema using [USE DATABASE](../../sql-reference/sql/use-database) or [USE SCHEMA](../../sql-reference/sql/use-schema) SQL commands.

    * You can check the database in use for the notebook by calling the [CURRENT_DATABASE](../../sql-reference/functions/current_database) function.

    * If you reference objects in the notebook database or the database specified in an earlier notebook cell, you can simplify your SQL statements to include only the schema and object that you want to reference, instead of the fully qualified path to the object.

