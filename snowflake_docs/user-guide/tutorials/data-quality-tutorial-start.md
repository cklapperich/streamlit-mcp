# Tutorial: Getting started with data metric functions¶

## Introduction¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) [Enterprise Edition
Feature](../intro-editions)

Data Quality and data metric functions (DMFs) require Enterprise Edition. To
inquire about upgrading, please contact [Snowflake
Support](https://docs.snowflake.com/user-guide/contacting-support).

You can complete this tutorial using a worksheet in Snowsight or using a CLI
client such as [SnowSQL](../snowsql). Simply paste the code examples and run
them.

By the end of this tutorial, you will learn how to:

  * Create a custom data metric function (DMF) to measure data quality.

  * Manage the DMF to optimize serverless credit usage.

  * Monitor the serverless credit usage associated with calling the scheduled DMF.

## Access control setup¶

To complete this tutorial, use a single custom role that has all of the
required access, which includes the following:

  * Creating a database, which subsequently allows creating a schema, creating a DMF in the schema, and creating a table in the schema

  * Creating a warehouse to perform query operations

  * Querying the view that contains the results of calling the scheduled DMF

  * Querying the view that contains serverless compute usage information

Create the `dq_tutorial_role` role to use throughout the tutorial:

>
>     USE ROLE ACCOUNTADMIN;
>     CREATE ROLE IF NOT EXISTS dq_tutorial_role;
>  
>
> Copy

Grant privileges, and grant the application role and database roles to the
`dq_tutorial_role`:

>
>     GRANT CREATE DATABASE ON ACCOUNT TO ROLE dq_tutorial_role;
>     GRANT EXECUTE DATA METRIC FUNCTION ON ACCOUNT TO ROLE dq_tutorial_role;
>     GRANT APPLICATION ROLE SNOWFLAKE.DATA_QUALITY_MONITORING_VIEWER TO ROLE
> dq_tutorial_role;
>     GRANT DATABASE ROLE SNOWFLAKE.USAGE_VIEWER TO ROLE dq_tutorial_role;
>     GRANT DATABASE ROLE SNOWFLAKE.DATA_METRIC_USER TO ROLE dq_tutorial_role;
>  
>
> Copy

Create a warehouse to query the table that contains the data and grant the
USAGE privilege on the role to the `dq_tutorial_role` role:

>
>     CREATE WAREHOUSE IF NOT EXISTS dq_tutorial_wh;
>     GRANT USAGE ON WAREHOUSE dq_tutorial_wh TO ROLE dq_tutorial_role;
>  
>
> Copy

Confirm the grants to the `dq_tutorial_role` role:

>
>     SHOW GRANTS TO ROLE dq_tutorial_role;
>  
>
> Copy

Establish a role hierarchy and grant the role to a user who can complete this
tutorial (replace the `jsmith` value):

>
>     GRANT ROLE dq_tutorial_role TO ROLE SYSADMIN;
>     GRANT ROLE dq_tutorial_role TO USER jsmith;
>  
>
> Copy

## Data setup¶

To facilitate managing the data and the DMF for this tutorial, create a
dedicated database to contain these objects:

### Create a table¶

    
    
    USE ROLE dq_tutorial_role;
    CREATE DATABASE IF NOT EXISTS dq_tutorial_db;
    CREATE SCHEMA IF NOT EXISTS sch;
    
    CREATE TABLE customers (
      account_number NUMBER(38,0),
      first_name VARCHAR(16777216),
      last_name VARCHAR(16777216),
      email VARCHAR(16777216),
      phone VARCHAR(16777216),
      created_at TIMESTAMP_NTZ(9),
      street VARCHAR(16777216),
      city VARCHAR(16777216),
      state VARCHAR(16777216),
      country VARCHAR(16777216),
      zip_code NUMBER(38,0)
    );
    

Copy

### Insert values into a table¶

Add data to the table:

>
>     USE WAREHOUSE dq_tutorial_wh;
>  
>     INSERT INTO customers (account_number, city, country, email, first_name,
> last_name, phone, state, street, zip_code)
>       VALUES (1589420, 'san francisco', 'usa', 'john.doe@', 'john', 'doe',
> 1234567890, null, null, null);
>  
>     INSERT INTO customers (account_number, city, country, email, first_name,
> last_name, phone, state, street, zip_code)
>       VALUES (8028387, 'san francisco', 'usa', 'bart.simpson@example.com',
> 'bart', 'simpson', 1012023030, null, 'market st', 94102);
>  
>     INSERT INTO customers (account_number, city, country, email, first_name,
> last_name, phone, state, street, zip_code)
>       VALUES
>         (1589420, 'san francisco', 'usa', 'john.doe@example.com', 'john',
> 'doe', 1234567890, 'ca', 'concar dr', 94402),
>         (2834123, 'san mateo', 'usa', 'jane.doe@example.com', 'jane', 'doe',
> 3641252911, 'ca', 'concar dr', 94402),
>         (4829381, 'san mateo', 'usa', 'jim.doe@example.com', 'jim', 'doe',
> 3641252912, 'ca', 'concar dr', 94402),
>         (9821802, 'san francisco', 'usa', 'susan.smith@example.com',
> 'susan', 'smith', 1234567891, 'ca', 'geary st', 94121),
>         (8028387, 'san francisco', 'usa', 'bart.simpson@example.com',
> 'bart', 'simpson', 1012023030, 'ca', 'market st', 94102);
>  
>
> Copy

## Create and work with DMFs¶

In the following sections, we will create a user-defined DMF to measure the
count of invalid email addresses and subsequently do the following:

  * Schedule the DMF to run every 5 minutes.

  * Check the DMF table references (find the tables the DMF is set on).

  * Query a built-in view that contains the result of calling the scheduled DMF.

  * Unset the DMF from the table to avoid unnecessary serverless credit usage.

### Create a DMF¶

Create a data metric function (DMF) to return the number of email addresses in
a column that don’t match the specified regular expression:

>
>     CREATE DATA METRIC FUNCTION IF NOT EXISTS
>       invalid_email_count (ARG_T table(ARG_C1 STRING))
>       RETURNS NUMBER AS
>       'SELECT COUNT_IF(FALSE = (
>         ARG_C1 REGEXP
> ''^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$''))
>         FROM ARG_T';
>  
>
> Copy

### Set the schedule on the table¶

The DMF schedule defines when all DMFs on the table run. Currently, 5 minutes
is the shortest possible time interval:

>
>     ALTER TABLE customers SET DATA_METRIC_SCHEDULE = '5 MINUTE';
>  
>
> Copy

Note

For the purpose of the tutorial, the schedule is set for 5 minutes. However,
after you optimize your DMF use cases, experiment with the other schedule
settings, such as cron expressions or trigger events associated with DML
operations that affect the table.

### Set the DMFs on the table and check the references¶

Associate the DMF to the table:

>
>     ALTER TABLE customers ADD DATA METRIC FUNCTION
>       invalid_email_count ON (email);
>  
>
> Copy

Because the schedule is set for 5 minutes, we need to wait 5 minutes in order
for Snowflake to call the DMF and process the results. For now, we can check
to see that the DMF is associated with the table by calling the
[DATA_METRIC_FUNCTION_REFERENCES](../../sql-
reference/functions/data_metric_function_references) Information Schema table
function:

>
>     SELECT * FROM TABLE(INFORMATION_SCHEMA.DATA_METRIC_FUNCTION_REFERENCES(
>       REF_ENTITY_NAME => 'dq_tutorial_db.sch.customers',
>       REF_ENTITY_DOMAIN => 'TABLE'));
>  
>
> Copy

### View the DMF results¶

The results of calling the scheduled DMF are stored in the
DATA_QUALITY_MONITORING_RESULTS view. To determine the number of invalid email
addresses, query the [DATA_QUALITY_MONITORING_RESULTS](../../sql-
reference/local/data_quality_monitoring_results) view to see the results of
calling the scheduled DMF:

>
>     SELECT scheduled_time, measurement_time, table_name, metric_name, value
>     FROM SNOWFLAKE.LOCAL.DATA_QUALITY_MONITORING_RESULTS
>     WHERE TRUE
>     AND METRIC_NAME = 'INVALID_EMAIL_COUNT'
>     AND METRIC_DATABASE = 'DQ_TUTORIAL_DB'
>     LIMIT 100;
>  
>
> Copy

The results show that the `value` column contains `1`. This number corresponds
to one improperly formatted email address, which corresponds to the first
INSERT statement in the Insert values into a table section.

### Unset the DMFs from the table¶

You have established that the DMF is working as expected based on the
definition of the DMF, the schedule, and the expected results.

To avoid unnecessary serverless credit usage, unset the DMF from the table:

>
>     ALTER TABLE customers DROP DATA METRIC FUNCTION
>       invalid_email_count ON (email);
>  
>
> Copy

## View your serverless credit consumption¶

Calling scheduled data metric functions (DMFs) requires [serverless compute
resources](../cost-understanding-compute). You can query the Account Usage
view [DATA_QUALITY_MONITORING_USAGE_HISTORY](../../sql-reference/account-
usage/data_quality_monitoring_usage_history) to view the [DMF serverless
compute cost](../data-quality-intro.html#label-data-quality-cost).

Because the view has a latency of 1-2 hours, wait for that time to pass before
querying the view. You can come back to this step later.

Query the view and filter the results to include the time interval of your
scheduled DMF:

>
>     USE ROLE dq_tutorial_role;
>     SELECT *
>     FROM SNOWFLAKE.ACCOUNT_USAGE.DATA_QUALITY_MONITORING_USAGE_HISTORY
>     WHERE TRUE
>     AND START_TIME >= CURRENT_TIMESTAMP - INTERVAL '3 days'
>     LIMIT 100;
>  
>
> Copy

## Clean up, summary, and additional resources¶

Congratulations! You’ve successfully completed this tutorial.

Take a few minutes to review the summary and the key points covered in this
tutorial.

Consider cleaning up by dropping the objects you created in this tutorial.
Learn more by reviewing other topics in the Snowflake documentation.

### Summary and key points¶

In summary, you learned how to do the following:

  * Create a custom DMF to measure data quality and manage the DMF to optimize serverless credit usage.

  * Monitor the serverless credit usage associated with calling the scheduled DMF.

### Drop the tutorial objects¶

If you plan to repeat the tutorial, you can keep the objects that you created.

Otherwise, drop the tutorial objects as follows:

    
    
    USE ROLE ACCOUNTADMIN;
    DROP DATABASE dq_tutorial_db;
    DROP WAREHOUSE dq_tutorial_wh;
    DROP ROLE dq_tutorial_role;
    

Copy

### What’s next?¶

Continue learning about Snowflake using the following resources:

  * Learn more about DMFs by starting with [Introduction to Data Quality and data metric functions](../data-quality-intro).

  * Complete the other tutorials provided by Snowflake in the [Snowflake Tutorials](../../learn-tutorials) topic.

