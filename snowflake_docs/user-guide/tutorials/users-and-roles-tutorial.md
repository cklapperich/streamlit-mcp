# Create users and grant roles¶

## Introduction¶

This tutorial shows you how to create a user and grant a role to it by using
SQL commands. You use a template worksheet in Snowsight to follow and complete
these tasks.

Note

Snowflake bills a minimal amount for the on-disk storage used for the sample
data in this tutorial. The tutorial provides steps to drop the database and
minimize storage cost.

Snowflake requires a [virtual warehouse](../warehouses) to load the data and
execute queries. A running virtual warehouse consumes Snowflake credits. In
this tutorial, you will be using a [30-day trial
account](https://signup.snowflake.com/), which provides free credits, so you
won’t incur any costs.

### What you will learn¶

In this tutorial you will learn how to:

  * Use a role that has the privileges to create and use the Snowflake objects required by this tutorial.

  * Create a user.

  * Grant a role to the user and grant access to a warehouse.

  * Explore the users and roles in your account.

  * Drop the user you created.

## Prerequisites¶

This tutorial assumes the following:

  * You have a [supported browser](../ui-snowsight-gs.html#label-snowsight-getting-started-supported-browsers).

  * You have a trial account. If you do not have a trial account yet, you can sign up for a [free trial](https://signup.snowflake.com/). You can choose any [Snowflake Cloud Region](../intro-regions).

  * Your user is the account administrator and is granted the ACCOUNTADMIN system role. For more information, see [Using the ACCOUNTADMIN Role](../security-access-control-considerations.html#label-security-accountadmin-role).

Note

This tutorial is only available to users with a trial account. The sample
worksheet is not available for other types of accounts.

## Step 1. Sign in using Snowsight¶

To access Snowsight over the public Internet, do the following:

  1. In a supported web browser, navigate to <https://app.snowflake.com>.

  2. Provide your [account identifier](../admin-account-identifier) or account URL. If you’ve previously signed in to Snowsight, you might see an account name that you can select.

  3. Sign in using your Snowflake account credentials.

## Step 2. Open the [Template] worksheet¶

You can use worksheets to write and run SQL commands on your database. Your
trial account has access to a pre-loaded template worksheet for this tutorial.
The worksheet contains the SQL commands that you will run to set the role
context, create a user, and grant role privileges. Because it is a template
worksheet, you will be invited to enter your own values for certain SQL
parameters.

For more information about worksheets, see [Getting started with
worksheets](../ui-snowsight-worksheets-gs).

To open the worksheet:

  1. Select Projects » Worksheets to open the list of worksheets.

  2. Open [Template] Adding a user and granting roles.

Your browser looks similar to the following image.

> ![SQL users worksheet, which contains the SQL commands for this tutorial,
> along with descriptive comments.](../../_images/create-user-tutorial.png)

## Step 3. Set the role to use¶

The role you use determines the privileges you have. In this tutorial, use the
USERADMIN system role so that you can create and manage users and roles in
your account. For more information, see [Overview of Access
Control](../security-access-control-overview).

To set the role to use, do the following:

  1. In the open worksheet, place your cursor in the [USE ROLE](../../sql-reference/sql/use-role) line.
    
        USE ROLE USERADMIN;
    

Copy

  2. In the upper-right corner of the worksheet, select Run.

Note

In this tutorial, run SQL statements one at a time. Do not select Run All.

## Step 4. Create a user¶

A Snowflake user has login credentials. When a user is granted a role, the
user can perform all the operations that the role allows, via the privileges
that were granted to the role. For more information, see [User
management](../admin-user-management).

In this step of the tutorial, you create a user with a name, a password, and
some other properties.

In the open worksheet, place your cursor in the [CREATE USER](../../sql-
reference/sql/create-user) line, insert a username and other parameter values
of your choice (an example is shown below), and select Run.

For MUST_CHANGE_PASSWORD, set the value to `true`, which ensures that a
password reset is requested on first login. For DEFAULT_WAREHOUSE, use
`COMPUTE_WH`.

>
>     CREATE OR REPLACE USER snowman
>     PASSWORD = 'sn0wf@ll'
>     LOGIN_NAME = 'snowstorm'
>     FIRST_NAME = 'Snow'
>     LAST_NAME = 'Storm'
>     EMAIL = 'snow.storm@snowflake.com'
>     MUST_CHANGE_PASSWORD = true
>     DEFAULT_WAREHOUSE = COMPUTE_WH;
>  
>
> Copy

This command returns the following output:

>
>     User SNOWMAN successfully created.
>  

If you were creating a real user in a real Snowflake account, you would now
send the following information in a secure manner to the person who would need
to access this new account:

  * Snowflake Account URL: the Snowflake account link where the user will log in. You can find this link at the top of your browser (for example: <https://app.snowflake.com/myorg/myaccount/>, where `myorg` is the Snowflake organization ID, and `myaccount` is the account ID).

  * LOGIN_NAME, as specified in the CREATE USER command.

  * PASSWORD, as specified in the CREATE USER command.

## Step 5. Grant a system role and warehouse access to the user¶

Now that you have created a user, you can use the SECURITYADMIN role to grant
the SYSADMIN role to the user, as well as grant USAGE on the COMPUTE_WH
warehouse.

Granting a role to another role creates a parent-child relationship between
the roles (also referred to as a role hierarchy). Granting a role to a user
enables the user to perform all operations allowed by the role (through the
access privileges granted to the role).

The SYSADMIN role has privileges to create warehouses, databases, and database
objects in an account and grant those privileges to other roles. Only grant
this role to users who should have these privileges. For information about
other system-defined roles, see [Overview of Access Control](../security-
access-control-overview).

To grant the user access to a role and a warehouse, do the following:

  1. In the open worksheet, place your cursor in the [USE ROLE](../../sql-reference/sql/use-role) line, then select Run.
    
        USE ROLE SECURITYADMIN;
    

Copy

  2. Place your cursor in the [GRANT ROLE](../../sql-reference/sql/grant-role) line, enter the name of the user you created, then select Run.
    
        GRANT ROLE SYSADMIN TO USER snowman;
    

Copy

  3. Place your cursor in the GRANT USAGE line, then select Run.
    
        GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE SYSADMIN;
    

Copy

## Step 6. Explore the users and roles in your account¶

Now you can explore all the users and roles in your account by using the
ACCOUNTADMIN role.

To explore users and roles, do the following:

  1. In the open worksheet, place your cursor in the [USE ROLE](../../sql-reference/sql/use-role) line, then select Run.
    
        USE ROLE ACCOUNTADMIN;
    

Copy

  2. Place your cursor in the [SHOW USERS](../../sql-reference/sql/show-users) line, then select Run.
    
        SHOW USERS;
    

Copy

Your output looks similar to the following image.

![Show all the users in the account. Table output with the following columns:
name, created_on, login_name, display_name, first_name.](../../_images/create-
user-tutorial-show-users.png)

  3. Place your cursor in the [SHOW ROLES](../../sql-reference/sql/show-roles) line, then select Run.
    
        SHOW ROLES;
    

Copy

Your output looks similar to the following image.

![Show all the roles in the account. Table output with the following columns:
created_on, name, is_default, is_current, is_inherited.](../../_images/create-
user-tutorial-show-roles.png)

## Step 7. Drop the user and review key points¶

Congratulations! You have successfully completed this tutorial for trial
accounts. Take a few minutes to review the key points that were covered. Learn
more by reviewing other topics in the Snowflake Documentation.

### Drop the user¶

Assuming that it is no longer needed, you can now drop the user you created.

In the open worksheet, place your cursor in the [DROP USER](../../sql-
reference/sql/drop-user) line, enter the name of the user you created, then
select Run.

    
    
    DROP USER snowman;
    

Copy

### Review key points¶

In summary, you used a pre-loaded worksheet in Snowsight to complete the
following steps:

  1. Set the role to use.

  2. Create a new user.

  3. Grant the user role privileges and access to a warehouse.

  4. Explore the users and roles in the account.

  5. Drop the user you created.

Here are some key points to remember about users and roles:

  * You need the required permissions to create and manage objects in your account. In this tutorial, you used the USERADMIN, SECURITYADMIN, SYSADMIN, and ACCOUNTADMIN system roles for different purposes.

  * The ACCOUNTADMIN role is not normally used to create objects. Instead, we recommend creating a hierarchy of roles aligned with business functions in your organization. For more information, see [Using the ACCOUNTADMIN Role](../security-access-control-considerations.html#label-security-accountadmin-role).

  * A warehouse provides the compute resources that you need to execute DML operations, load data, and run queries. This tutorial uses the `compute_wh` warehouse that is included with your trial account.

### What’s next?¶

Continue learning about Snowflake using the following resources:

  * Complete the other tutorials provided by Snowflake:

    * [Snowflake Tutorials](../../learn-tutorials)

  * Familiarize yourself with key Snowflake concepts and features, as well as the SQL commands used to create users and grant role privileges:

    * [Introduction to Snowflake](../../user-guide-intro)

    * [User, role, & privilege commands](../../sql-reference/commands-user-role)

  * Try the Tasty Bytes Quickstarts provided by Snowflake:

    * [Tasty Bytes Quickstarts](https://quickstarts.snowflake.com/?cat=tasty-bytes)

