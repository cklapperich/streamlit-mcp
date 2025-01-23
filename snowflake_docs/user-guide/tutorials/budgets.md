# Tutorial: Get started with budgets¶

## Introduction¶

This tutorial introduces you to account-level credit usage monitoring with
Budgets by setting up the account budget and creating a custom budget that
monitors a group of specified objects.

With budgets, you can monitor credit usage for the compute costs of supported
objects, including credit usage for background maintenance tasks and
serverless features. Budgets enables you to set a monthly spending limit for
each budget and sends a notification email when your current spending is
projected to exceed the monthly spending limit.

You can complete this tutorial using a worksheet in Snowsight or using a CLI
client such as [SnowSQL](../snowsql). Some portions of this tutorial can be
completed using Snowsight.

By the end of this tutorial, you will learn how to do the following:

  * Create custom roles to monitor and manage budgets.

  * Grant the required privileges to add objects to a custom budget.

  * Activate and set up an account budget.

  * Create a custom budget and add objects to it.

### Prerequisites¶

To complete this tutorial, the following prerequisites are required:

  * You must be able to use the ACCOUNTADMIN role to create the roles used in this tutorial.

  * You must [verify your email address](../notifications/email-notifications.html#label-email-notification-verify-address). Only verified email addresses can be added to a budget notification list.

## Create a notification integration¶

Budgets use a notification integration to send notification emails when
current credit usage is expected to exceed the monthly spending limit. The
`ALLOWED_RECIPIENTS` list _must_ include the verified email addresses of the
users to receive budgets notifications.

A notification integration is required if you are completing the tutorial
using SQL. Follow the steps below to create one.

When you use Snowsight to set up a budget, the notification integration is
automatically created for you. If you are going to use Snowsight to set up
your budgets, you can skip to the next step.

  1. Execute the following statement to create a notification integration. Use your verified email address in the ALLOWED_RECIPIENTS list:
    
        USE ROLE ACCOUNTADMIN;
    
    CREATE NOTIFICATION INTEGRATION budgets_notification_integration
      TYPE=EMAIL
      ENABLED=TRUE
      ALLOWED_RECIPIENTS=('<YOUR_EMAIL_ADDRESS>');
    

Copy

  2. After you create the notification integration, grant the USAGE privilege to the SNOWFLAKE application. This privilege is required in order for Budgets to use the notification integration to send emails.

Execute the following statement to grant the USAGE privilege on the
notification integration:

    
        GRANT USAGE ON INTEGRATION budgets_notification_integration
      TO APPLICATION snowflake;
    

Copy

## Create a database, schema, and custom roles¶

In this step, the following objects are created for the tutorial to create,
manage, and monitor budgets:

  * A database and schema in which to create custom budgets.

  * A custom role to manage the account budget.

  * A custom role to monitor the account budget.

  * A custom role to create custom budgets.

  1. Create a database and schema in which to create a custom budget using the following steps:

SQLSnowsight

    1. Create the database and schema in which to create the custom budget:
        
                USE ROLE ACCOUNTADMIN;
        
        CREATE DATABASE budgets_db;
        
        CREATE SCHEMA budgets_db.budgets_schema;
        

Copy

    1. Create the database and schema in which to create the custom budget:

      1. Sign in to Snowsight.

      2. Switch to the ACCOUNTADMIN role.

      3. Select Data » Databases » \+ Database.

      4. In the Name field, enter `budgets_db`.

      5. Select Create.

      6. After the database is created, select the `budgets_db`.

      7. Select Schemas » \+ Schema.

      8. In the Name field, enter `budgets_schema`.

      9. Select Create.

  2. Create custom role `account_budget_admin` for the account budget administrator. The account budget administrator can take the following actions on the account budget:

     * Activate and deactivate the account budget.

     * Set the spending limit.

     * Edit notification settings.

     * Monitor credit usage for the account.
    
        USE ROLE ACCOUNTADMIN;
    
    CREATE ROLE account_budget_admin;
    
    GRANT APPLICATION ROLE SNOWFLAKE.BUDGET_ADMIN TO ROLE account_budget_admin;
    
    GRANT IMPORTED PRIVILEGES ON DATABASE SNOWFLAKE TO ROLE account_budget_admin;
    

Copy

  3. Create custom role `account_budget_monitor` to be granted to account budget monitors. An account budget monitor can take the following actions on the account budget:

     * Monitor credit usage for the account.

     * View the email notification settings.

     * View the monthly spending limit for the account.
    
        USE ROLE ACCOUNTADMIN;
    
    CREATE ROLE account_budget_monitor;
     
    GRANT APPLICATION ROLE SNOWFLAKE.BUDGET_VIEWER TO ROLE account_budget_monitor;
    
    GRANT IMPORTED PRIVILEGES ON DATABASE SNOWFLAKE TO ROLE account_budget_monitor;
    

Copy

  4. Create a custom role `budget_owner` with the required role and privileges to create custom budgets in the schema `budgets_db.budgets_schema`:
    
        USE ROLE ACCOUNTADMIN;
       
    CREATE ROLE budget_owner;
      
    GRANT USAGE ON DATABASE budgets_db TO ROLE budget_owner;
    GRANT USAGE ON SCHEMA budgets_db.budgets_schema TO ROLE budget_owner;
    
    GRANT DATABASE ROLE SNOWFLAKE.BUDGET_CREATOR TO ROLE budget_owner;
    
    GRANT CREATE SNOWFLAKE.CORE.BUDGET ON SCHEMA budgets_db.budgets_schema
      TO ROLE budget_owner;
    

Copy

  5. Create two custom roles to manage and monitor custom budgets. These roles will be granted additional privileges later in the tutorial after the custom budget is created. To create the custom roles, follow these steps:

    1. Create a custom `budget_admin` role that can manage and monitor a custom budget:
        
                USE ROLE ACCOUNTADMIN;
        
        CREATE ROLE budget_admin;
        
        GRANT USAGE ON DATABASE budgets_db TO ROLE budget_admin;
        
        GRANT USAGE ON SCHEMA budgets_db.budgets_schema TO ROLE budget_admin;
        
        GRANT DATABASE ROLE SNOWFLAKE.USAGE_VIEWER TO ROLE budget_admin;
        

Copy

>     1. Create a custom `budget_monitor` role that can monitor a custom
> budget:
>

>> >>     USE ROLE ACCOUNTADMIN;

>>  
>>     CREATE ROLE budget_monitor;

>>  
>>     GRANT USAGE ON DATABASE budgets_db TO ROLE budget_monitor;

>>  
>>     GRANT USAGE ON SCHEMA budgets_db.budgets_schema TO ROLE budget_monitor;

>>  
>>     GRANT DATABASE ROLE SNOWFLAKE.USAGE_VIEWER TO ROLE budget_monitor;

>>  
>>

>> Copy

  6. Grant custom budget roles to yourself to use in future steps of the tutorial:

> SQLSnowsight
>
>     1. Grant the `account_budget_admin` role to yourself:
>  
>         >         GRANT ROLE account_budget_admin
>           TO USER <YOUR_USER_NAME>;
>  
>
> Copy
>
>     2. Grant the `account_budget_monitor` role to yourself:
>  
>         >         GRANT ROLE account_budget_monitor
>           TO USER <YOUR_USER_NAME>;
>  
>
> Copy
>
>     3. Grant the `budget_owner` role to yourself:
>  
>         >         GRANT ROLE budget_owner
>           TO USER <YOUR_USER_NAME>;
>  
>
> Copy
>
>     4. Grant the `budget_monitor` role to yourself:
>  
>         >         GRANT ROLE budget_monitor
>           TO USER <YOUR_USER_NAME>;
>  
>
> Copy
>
> Grant custom budget roles to yourself:
>
>     1. Sign in to Snowsight.
>
>     2. Switch to the ACCOUNTADMIN role.
>
>     3. In the navigation menu, select Admin » Users & Roles, and then select
> Roles.
>
>     4. Select Table and locate and select the role `account_budget_admin`.
>
>     5. In the section 0 users have been granted ACCOUNT_BUDGET_ADMIN, select
> Grant to User.
>
>     6. For User to receive grant, select your username to grant the role to.
>
>     7. Select Grant.
>
>     8. After the role is granted, return to the previous page.
>
>     9. Select the role `account_budget_monitor`.
>
>     10. In the section 0 users have been granted ACCOUNT_BUDGET_MONITOR,
> select Grant to User.
>
>     11. Select Grant.
>
>     12. Repeat the previous four steps (h-k) to grant yourself the following
> additional roles:
>
>        * `budget_owner`
>
>        * `budget_monitor`

In this section, you created custom roles to manage and monitor budgets, and
create custom budgets.

## Create the objects for the custom budget¶

In this step, create objects to add to a custom budget and grant privileges to
the custom roles you created in the previous step. You will be creating the
following objects:

  * A warehouse to add to a custom budget.

  * A database to add to a custom budget.

  1. Create a warehouse and grant the USAGE and APPLYBUDGET privileges on the warehouse to the custom roles you created. The APPLYBUDGET privilege is required to add an object to a budget.

> SQLSnowsight
>
>     1. Create warehouse `na_finance_wh`:
>  
>         >         CREATE WAREHOUSE na_finance_wh;
>  
>
> Copy
>
>     2. Grant the USAGE privilege to custom budget roles:
>  
>         >         GRANT USAGE ON WAREHOUSE na_finance_wh TO ROLE
> account_budget_admin;
>         GRANT USAGE ON WAREHOUSE na_finance_wh TO ROLE
> account_budget_monitor;
>         GRANT USAGE ON WAREHOUSE na_finance_wh TO ROLE budget_admin;
>         GRANT USAGE ON WAREHOUSE na_finance_wh TO ROLE budget_owner;
>         GRANT USAGE ON WAREHOUSE na_finance_wh TO ROLE budget_monitor;
>  
>
> Copy
>
>     3. Grant the APPLYBUDGET privilege on the warehouse to role
> `budget_owner`:
>  
>         >         GRANT APPLYBUDGET ON WAREHOUSE na_finance_wh TO ROLE
> budget_owner;
>  
>
> Copy
>
>     1. Create warehouse `na_finance_wh`:
>
>       1. Sign in to Snowsight.
>
>       2. Select Admin » Warehouses » \+ Warehouse
>
>       3. In the Warehouse Name field, enter `na_finance_wh`.
>
>       4. Select Create Warehouse.
>
>     2. Grant the USAGE privilege on the warehouse to custom roles,
> `account_budge_admin` and `budget_admin`:
>
>       1. Select Admin » Warehouses.
>
>       2. Select warehouse you just created `na_finance_wh`.
>
>       3. In the Privileges tile, select \+ Privilege.
>
>       4. For the Role, select the `account_budget_admin` role.
>
>       5. For the Privileges, select USAGE.
>
>       6. Select Grant Privileges.
>
>       7. Repeat the previous 4 steps for the role `budget_admin`.
>
>     3. Grant the USAGE and APPLYBUDGET privileges on the warehouse to role
> `budget_owner`:
>
>       1. Select Admin » Warehouses.
>
>       2. Select warehouse you just created `na_finance_wh`.
>
>       3. In the Privileges tile, select \+ Privilege.
>
>       4. For the Role, select the `budget_owner` role.
>
>       5. For the Privileges, select APPLYBUDGET and USAGE.
>
>       6. Select Grant Privileges.

  2. Create a database and grant the APPLYBUDGET privilege on the warehouse to the custom budget owner role you created. The APPLYBUDGET privilege is required to add an object to a budget.

> SQLSnowsight
>
>     1. Create a database:
>  
>         >         CREATE DATABASE na_finance_db;
>  
>
> Copy
>
>     2. Grant the APPLYBUDGET privilege on the database to role
> `budget_owner`:
>  
>         >         GRANT APPLYBUDGET ON DATABASE  na_finance_db TO ROLE
> budget_owner;
>  
>
> Copy
>
>     1. Create a database:
>
>       1. Sign in to Snowsight.
>
>       2. Select Data » Databases » \+ Database
>
>       3. In the Name field, enter `na_finance_db`.
>
>       4. Select Create.
>
>     2. Grant the APPLYBUDGET privilege on the database to role
> `budget_owner`:
>
>       1. Select Data » Databases.
>
>       2. Select the database you just created `na_finance_db`.
>
>       3. In the Privileges tile, select \+ Privilege.
>
>       4. For the Role, select the `budget_owner` role.
>
>       5. For the Privileges, select APPLYBUDGET.
>
>       6. Select Grant Privileges.

In this section, you created the objects to be added to a custom budget and
granted the APPLYBUDGET privilege required to add those objects to a budget.
You also created the database and schema in which to create the custom budget
and granted the USAGE privilege required to create a budget in the schema. Now
you are ready to activate, create, and set up budgets.

## Activate and set up the account budget¶

The account budget monitors credit usage for the compute costs of all Budgets
supported objects in the account, including background maintenance tasks (for
example, automatic clustering) and serverless features. The account budget
must be activated before it can start monitoring credit usage. After it is
activated, you can set the monthly spending limit for the account and the
email list of notification recipients. Budgets sends a notification email when
current credit usage is expected to exceed the monthly spending limit.

Activate and set up the account budget using the following steps:

SQLSnowsight

  1. Use the `account_budget_admin` role you created in a previous step to activate the account budget:
    
        USE ROLE account_budget_admin;
    
    CALL snowflake.local.account_root_budget!ACTIVATE();
    

Copy

  2. Set the spending limit for the account budget to 500 credits per month:
    
        CALL snowflake.local.account_root_budget!SET_SPENDING_LIMIT(500);
    

Copy

  3. To set up the email notification list, use your verified email address and the notification integration you created earlier in the tutorial:
    
        CALL snowflake.local.account_root_budget!SET_EMAIL_NOTIFICATIONS(
       'budgets_notification_integration',
       '<YOUR_EMAIL_ADDRESS>');
    

Copy

Activate and set up the account budget:

  1. Sign in to Snowsight.

  2. Select the ACCOUNT_BUDGET_ADMIN role you created in a previous step.

  3. Select Admin » Cost Management.

  4. Select Budgets.

  5. If prompted, select `na_finance_wh` for the warehouse.

  6. In the upper-right corner of the dashboard, select Set up Account Budget.

  7. Enter 500 for the spending limit for the account.

To help you set your monthly spending limit, the configuration tool displays
your projected spend for the month and your average monthly spend for the
previous 3 months. For example, see the screenshot below.

  8. Enter your email address to receive notification emails.

![Account budget configuration screenshot](../../_images/set-up-account-
budget.png)

  9. Select Finish Setup.

In this section, you activated the account budget and set the spending limit
and the email address to receive budget notifications.

## Create a custom budget¶

Now that you have activated and set up your account budget, create a custom
budget to monitor the credit usage in your account for a specified group of
objects. For this tutorial, add the `na_finance_wh` warehouse and
`na_finance_db` to the custom budget.

Create custom budgets with the following steps:

  1. Use the `budget_owner` role to create budget `na_finance_budget` in `budgets_db.budgets_schema`:
    
        USE ROLE budget_owner;
    USE SCHEMA budgets_db.budgets_schema;
    USE WAREHOUSE na_finance_wh;
    
    CREATE SNOWFLAKE.CORE.BUDGET na_finance_budget();
    

Copy

  2. Set the monthly spending limit and email notification list for budget `na_finance_budget` using the following steps:

SQLSnowsight

    1. Set the monthly spending limit to 500 credits:
        
                CALL na_finance_budget!SET_SPENDING_LIMIT(500);
        

Copy

    2. To set up the notification list, use your verified email address and the notification integration created in the first step of the tutorial:
        
                CALL na_finance_budget!SET_EMAIL_NOTIFICATIONS('budgets_notification_integration',
                                                       '<YOUR_EMAIL_ADDRESS>');
        

Copy

    3. Add database `na_finance_db` and warehouse `na_finance_wh` to budget `na_finance_budget`:
        
                CALL na_finance_budget!ADD_RESOURCE(
          SYSTEM$REFERENCE('database', 'na_finance_db', 'SESSION', 'applybudget'));
        
        CALL na_finance_budget!ADD_RESOURCE(
          SYSTEM$REFERENCE('warehouse', 'na_finance_wh', 'SESSION', 'applybudget'));
        

Copy

Use the `budget_owner` role to set up budget `na_finance_budget`:

    1. Sign in to Snowsight.

    2. Select the BUDGET_OWNER role you created in a previous step.

    3. Select Admin » Cost Management.

    4. Select Budgets.

    5. Select the budget `na_finance_budget`.

    6. In the upper-right corner of the dashboard, select [![Pencil icon](../../_images/pencil-icon.svg)](../../_images/pencil-icon.svg) (Edit Budget).

    7. Enter 500 for the Spending limit.

    8. Enter your email address to receive notification emails.

    9. Select Resources to monitor.

Note

You can only add an object to one custom budget. If an object is currently
included in one custom budget and you add that object to a second custom
budget, Budgets removes the object from the first custom budget without
issuing a warning.

       * To add a database, expand Databases to select a database. Select `na_finance_db`.

When you select a database, all the Budgets supported objects the database
contains are also selected. Additionally, any future objects created in the
database are automatically added to the budget.

![Custom budget select resources screenshot](../../_images/custom-budget-
select-resources.png)

       * To add a warehouse, expand Warehouses to select a warehouse. Select `na_finance_wh`.

    10. Select Save Changes.

The Save Changes button is activated only when all the fields are completed.

  3. Grant instance roles to the custom roles you created in a previous step.

    1. Grant the required roles and privileges to the `budget_admin` role to let the `budget_admin` role modify and monitor the custom budget `na_finance_budget`:
        
                USE ROLE budget_owner;
        
        GRANT SNOWFLAKE.CORE.BUDGET ROLE budgets_db.budgets_schema.na_finance_budget!ADMIN
          TO ROLE budget_admin;
        

Copy

    2. Grant the VIEWER instance role to the `budget_monitor` role to let the `budget_monitor` role monitor the custom budget `na_finance_budget`:
        
                USE ROLE budget_owner;
        
        GRANT SNOWFLAKE.CORE.BUDGET ROLE budgets_db.budgets_schema.na_finance_budget!VIEWER
          TO ROLE budget_monitor;
        

Copy

In this section, you created a custom budget, added objects for the budget to
monitor, and set up the email address to receive budget notifications.

## Monitoring credit usage¶

You have completed all the steps in the tutorial to activate your account
budget, create a custom budget, and create custom roles to monitor and manage
both account and custom budgets. Credit usage data for your budgets takes some
time to populate.

Budgets uses serverless tasks to collect credit usage data for the budgets in
your account. After you activate the account budget or create a custom budget,
it takes a while for the serverless task to execute. After credit usage data
becomes available, you can monitor credit usage for budgets using Snowsight.

To monitor credit usage after usage data becomes available, use the following
steps:

SQLSnowsight

Use the `account_budget_monitor` role created in a previous step and view the
spending history for the account budget in the past week by executing the
following statements:

    
    
    USE ROLE account_budget_monitor;
    
    CALL snowflake.local.account_root_budget!GET_SPENDING_HISTORY(
      TIME_LOWER_BOUND => DATEADD('days', -7, CURRENT_TIMESTAMP()),
      TIME_UPPER_BOUND => CURRENT_TIMESTAMP()
    );
    

Copy

You can monitor spending history by service type. To view the spending history
for the search optimization serverless feature for the account budget in the
past week, execute the following statement:

    
    
    USE ROLE account_budget_monitor;
    
    CALL snowflake.local.account_root_budget!GET_SERVICE_TYPE_USAGE(
       SERVICE_TYPE => 'SEARCH_OPTIMIZATION',
       TIME_DEPART => 'day',
       USER_TIMEZONE => 'UTC',
       TIME_LOWER_BOUND => DATEADD('day', -7, CURRENT_TIMESTAMP()),
       TIME_UPPER_BOUND => CURRENT_TIMESTAMP()
    );
    

Copy

Use the `budget_monitor` role to view the spending history for the past week
for custom budget `na_finance_budget`:

    
    
    USE ROLE budget_monitor;
    
    CALL budgets_db.budgets_schema.na_finance_budget!GET_SPENDING_HISTORY(
      TIME_LOWER_BOUND => DATEADD('days', -7, CURRENT_TIMESTAMP()),
      TIME_UPPER_BOUND => CURRENT_TIMESTAMP()
    );
    

Copy

Use the `account_budget_monitor` role to view spending history for the account
budget:

  1. Sign in to Snowsight.

  2. Select the ACCOUNT_BUDGET_MONITOR role you created in a previous step.

  3. Select Admin » Cost Management.

  4. Select Budgets.

  5. If prompted, select the `na_finance_wh`.

Use the `budget_monitor` role to view spending history for the
`na_finance_budget` custom budget:

  1. Sign in to Snowsight.

  2. Select the BUDGET_MONITOR role you created in a previous step.

  3. Select Admin » Cost Management.

  4. Select Budgets.

  5. If prompted, select the `na_finance_wh`.

## Clean up, summary, and additional resources¶

Congratulations! You have successfully completed this tutorial.

After credit usage data is populated for your account budget and custom
budget, see [Use Snowsight to monitor budgets](../budgets/config.html#label-
monitoring-budgets-in-ui).

### Summary and key points¶

In summary, you learned how to:

  * Create custom roles to manage and monitor budgets.

Custom roles enable non-account administrators to monitor credit usage for a
budget and modify budget settings. For more information, see [Budgets roles
and privileges](../budgets.html#label-budgets-roles-and-privileges).

  * Grant the required privileges to add objects to a custom budget.

The APPLYBUDGET privilege must be granted on an object to add or remove it
from a custom budget. Objects are added or removed by [reference](../../sql-
reference/references). For more information, see [Adding and removing objects
from a custom budget](../budgets/config.html#label-modifying-objects-in-
custom-budgets).

  * Activate and set up the account budget.

The account budget must be activated and set up to start monitoring credit
usage for your account. The account budget monitors compute costs including
background maintenance tasks and serverless features and sends an email
notification when current spending is expected to exceed the monthly spending
limit.

For more information, see [Activating the account
budget](../budgets/config.html#label-activate-account-budget).

  * Create a custom budget to monitor a specified group of objects in your account.

Custom budgets monitor credit usage for a group of objects in your account.
Custom budgets monitor credit usage for compute costs for the objects in the
group including background maintenance tasks and serverless features.

For more information, see [Creating a custom
budget](../budgets/config.html#label-create-custom-budget).

For more information, see the following topics:

  * For a list of supported objects and the serverless features monitored by custom budgets, see [Supported objects](../budgets.html#label-budgets-supported-objects) and [Supported serverless features](../budgets.html#label-budgets-supported-serverless-features).

  * For more information on monitoring budgets spending, see [Use Snowsight to monitor budgets](../budgets/config.html#label-monitoring-budgets-in-ui).

### Delete objects created in the tutorial¶

You can choose to keep the custom roles and custom budget you created in the
tutorial to monitor credit usage. Otherwise, drop the budget and the related
custom roles:

To delete the custom budget created in the tutorial, execute the following
statements:

    
    
    USE ROLE budget_owner;
    
    DROP SNOWFLAKE.CORE.BUDGET budgets_db.budgets_schema.na_finance_budget;
    

Copy

To delete the objects created in this tutorial, execute the following
statements:

    
    
    USE ROLE ACCOUNTADMIN;
    
    DROP DATABASE na_finance_db;
    DROP WAREHOUSE na_finance_wh;
    DROP DATABASE budgets_db;
    

Copy

To delete the custom roles created for managing and monitoring the custom
budget, execute the following statements:

    
    
    USE ROLE ACCOUNTADMIN;
    
    DROP ROLE budget_monitor;
    DROP ROLE budget_admin;
    DROP ROLE budget_owner;
    

Copy

Snowflake recommends leaving the account budget activated. However, if you
decide to deactivate it, see [Deactivating the account
budget](../budgets/config.html#label-deactivate-account-budget) for more
information and instructions.

To delete the account budget monitor and administrator roles, execute the
following statements:

    
    
    USE ROLE ACCOUNTADMIN;
    
    DROP ROLE account_budget_monitor;
    DROP ROLE account_budget_admin;
    

Copy

To delete the notification integration, execute the following statements:

    
    
    USE ROLE ACCOUNTADMIN;
    
    DROP NOTIFICATION INTEGRATION budgets_notification_integration;
    

Copy

### Additional resources¶

Continue learning about budgets and Snowflake using the following resources:

  * [Monitor credit usage with budgets](../budgets)

  * [Understand budget costs](../budgets/cost)

  * [Troubleshoot budgets](../budgets/troubleshoot)

