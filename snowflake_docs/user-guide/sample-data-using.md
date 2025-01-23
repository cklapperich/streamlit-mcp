# Using the Sample Database¶

The sample database, SNOWFLAKE_SAMPLE_DATA, is identical to the databases that
you create in your account, except that it is read-only. As such, the
following operations are not allowed:

  * No DDL can be performed on the data set schemas (i.e. tables and other database objects cannot be added, dropped, or altered).

  * No DML can be performed on the tables in the schemas.

  * No cloning or Time Travel can be performed on the database or any schemas/tables in the database.

However, you can use all the same commands and syntax to view the sample
database, schemas, and tables, as well as execute queries on the tables.

Important

The sample database is created by default for newer accounts. If the database
has not been created for your account and you want access to it, execute the
following SQL statements with the ACCOUNTADMIN role active:

    
    
    -- Create a database from the share.
    CREATE DATABASE SNOWFLAKE_SAMPLE_DATA FROM SHARE SFC_SAMPLES.SAMPLE_DATA;
    
    -- Grant the PUBLIC role access to the database.
    -- Optionally change the role name to restrict access to a subset of users.
    GRANT IMPORTED PRIVILEGES ON DATABASE SNOWFLAKE_SAMPLE_DATA TO ROLE PUBLIC;
    

Copy

## Viewing the Sample Database¶

You can view the sample database and its contents either in the web interface
or using SQL:

> Snowsight:
>  
>
> Select Data » Databases » SNOWFLAKE_SAMPLE_DATA.
>
> Classic Console:
>  
>
> Click on Databases [![Databases tab](../_images/ui-navigation-database-
> icon.svg)](../_images/ui-navigation-database-icon.svg) »
> SNOWFLAKE_SAMPLE_DATA:
>
>   * Click on an object tab to view summary information about the objects in
> the database.
>
>   * Click on the name of an object to view details about the object.
>
>

> SQL:
>  
>
> Execute a [SHOW DATABASES](../sql-reference/sql/show-databases) command.
>
> You can also use the relevant [SHOW <objects>](../sql-reference/sql/show)
> commands to view the objects in the sample database.

For example, in SQL:

>
>     show databases like '%sample%';
>  
>
> +-------------------------------+-----------------------+------------+------------+-------------------------+--------------+---------+---------+----------------+
>     | created_on                    | name                  | is_default | is_current | origin                  | owner        | comment | options | retention_time |
>
> |-------------------------------+-----------------------+------------+------------+-------------------------+--------------+---------+---------+----------------|
>     | 2016-07-14 14:30:21.711 -0700 | SNOWFLAKE_SAMPLE_DATA | N          | N          | SFC_SAMPLES.SAMPLE_DATA | ACCOUNTADMIN |         |         | 1              |
>
> +-------------------------------+-----------------------+------------+------------+-------------------------+--------------+---------+---------+----------------+
>  
>
> Copy

Note that this example illustrates the sample database, SNOWFLAKE_SAMPLE_DATA,
has been [shared with your account](data-sharing-intro) by Snowflake.

The `origin` column in the SHOW DATABASES output (or the Origin column in the
Databases [![Databases tab](../_images/ui-navigation-database-
icon.svg)](../_images/ui-navigation-database-icon.svg) page in the interface)
displays the fully-qualified name of the shared database,
SFC_SAMPLES.SAMPLE_DATA, indicating it originated from the SFC_SAMPLES account
(used by Snowflake to share the sample data).

## Querying Tables and Views in the Sample Database¶

To use a table or view in the sample database, you can either:

  * Reference the fully-qualified name of the table in your query (in the form of `snowflake_sample_data._schema_name_._object_name_`).

OR

  * Specify the sample database (and schema) for your session using the [USE DATABASE](../sql-reference/sql/use-database) and/or [USE SCHEMA](../sql-reference/sql/use-schema) commands.

The following two examples illustrate using both approaches to query the
`lineitem` table in the `tpch_sf1` schema:

>
>     select count(*) from snowflake_sample_data.tpch_sf1.lineitem;
>  
>     +----------+
>     | COUNT(*) |
>     |----------|
>     |  6001215 |
>     +----------+
>  
>     use schema snowflake_sample_data.tpch_sf1;
>  
>     select count(*) from lineitem;
>  
>     +----------+
>     | COUNT(*) |
>     |----------|
>     |  6001215 |
>     +----------+
>  
>
> Copy

Note

You must have a running, current warehouse in your session to perform queries.
You set the current warehouse in a session using the [USE WAREHOUSE](../sql-
reference/sql/use-warehouse) command (or within the Worksheet in the web
interface.)

## Using the Tutorial SQL Scripts¶

Snowflake provides a set of tutorials, which are annotated SQL statements that
query the sample data sets to answer a set of practical business questions.

To access the tutorials from Classic Console:

  1. In the Worksheets [![Worksheet tab](../_images/ui-navigation-worksheet-icon.svg)](../_images/ui-navigation-worksheet-icon.svg) page, click on the down-arrow next to the worksheet tabs and select Open Tutorials:

> ![../_images/ui-sql-worksheet-ws-menu.png](../_images/ui-sql-worksheet-ws-
> menu.png)

  2. The Open Worksheet dialog displays the list of available tutorials. In the dialog, select a tutorial and click on the Open button:

> ![../_images/ui-sql-worksheet-ws-dialog.png](../_images/ui-sql-worksheet-ws-
> dialog.png)

  3. A new worksheet is created containing the contents of the tutorial:

> ![../_images/ui-sql-worksheet-ws-tutorial.png](../_images/ui-sql-worksheet-
> ws-tutorial.png)

You can then execute the queries in the tutorial as you would in any
worksheet. You can also alter the tutorial in the worksheet and save it as a
custom worksheet.

