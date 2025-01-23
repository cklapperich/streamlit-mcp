# Load and query sample data using SQL¶

## Introduction¶

This tutorial uses a fictitious food truck brand named Tasty Bytes to show you
how to load and query data in Snowflake using SQL. You use a pre-loaded
worksheet in Snowsight to complete these tasks.

The following illustration provides an overview of Tasty Bytes.

![Contains an overview of Tasty Bytes, a global food truck network with 15
brands of localized food truck options several countries and cities. The image
describes the company's mission, vision, locations, current state, and future
goals.](../../_images/tasty-bytes-overview.png)

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

  * Use a role to get access to functionality from granted privileges.

  * Use a warehouse to access resources.

  * Create a database and schema.

  * Create a table.

  * Load data into the table.

  * Query the data in the table.

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

## Step 2. Open the SQL worksheet for loading and querying data¶

You can use worksheets to write and run SQL commands on your Snowflake
database. Your trial account has access to a pre-loaded worksheet for this
tutorial. The worksheet has the SQL commands that you will run to create a
database, load data into it, and query the data. For more information about
worksheets, see [Getting started with worksheets](../ui-snowsight-worksheets-
gs).

To open the pre-loaded tutorial worksheet:

  1. Select Projects » Worksheets to open the list of worksheets.

  2. Open [Tutorial] Using SQL to load and query sample data.

Your worksheet looks similar to the following image.

> ![The SQL load and query worksheet, which contains the SQL commands for this
> tutorial, along with descriptive comments.](../../_images/tasty-bytes-
> select-worksheet.png)

## Step 3. Set the role and warehouse to use¶

The role you use determines the privileges you have. In this tutorial, use the
ACCOUNTADMIN system role so that you can view and manage objects in your
account. For more information, see [Using the ACCOUNTADMIN Role](../security-
access-control-considerations.html#label-security-accountadmin-role).

A warehouse provides the required resources to create and manage objects and
run SQL commands. These resources include CPU, memory, and temporary storage.
Your trial account has a virtual warehouse (`compute_wh`) that you can use for
this tutorial. For more information, see [Virtual warehouses](../warehouses).

To set the role and warehouse to use, do the following:

  1. In the open worksheet, place your cursor in the USE ROLE line.
    
        USE ROLE accountadmin;
    

Copy

  2. In the upper-right corner of the worksheet, select Run.

Note

In this tutorial, run SQL statements one at a time. Do not select Run All.

  3. Place your cursor in the USE WAREHOUSE line, then select Run.
    
        USE WAREHOUSE compute_wh;
    

Copy

## Step 4. Create a database, schema, and table¶

A database stores data in tables that you can manage and query. A schema is a
logical grouping of database objects, such as tables and views. For example, a
schema might contain the database objects required for a specific application.
For more information, see [Databases, Tables and Views -
Overview](../../guides-overview-db).

In this tutorial, you create a database named `tasty_bytes_sample_data`, a
schema named `raw_pos`, and a table named `menu`.

To create the database, schema, and table, do the following:

  1. In the open worksheet, place your cursor in the CREATE OR REPLACE DATABASE line, then select Run.
    
        CREATE OR REPLACE DATABASE tasty_bytes_sample_data;
    

Copy

  2. Place your cursor in the CREATE OR REPLACE SCHEMA line, then select Run.
    
        CREATE OR REPLACE SCHEMA tasty_bytes_sample_data.raw_pos;
    

Copy

  3. Place your cursor in the CREATE OR REPLACE TABLE lines, then select Run.
    
        CREATE OR REPLACE TABLE tasty_bytes_sample_data.raw_pos.menu
    (
        menu_id NUMBER(19,0),
        menu_type_id NUMBER(38,0),
        menu_type VARCHAR(16777216),
        truck_brand_name VARCHAR(16777216),
        menu_item_id NUMBER(38,0),
        menu_item_name VARCHAR(16777216),
        item_category VARCHAR(16777216),
        item_subcategory VARCHAR(16777216),
        cost_of_goods_usd NUMBER(38,4),
        sale_price_usd NUMBER(38,4),
        menu_item_health_metrics_obj VARIANT
    );
    

Copy

  4. To confirm that the table was created successfully, place your cursor in the SELECT line, then select Run.
    
        SELECT * FROM tasty_bytes_sample_data.raw_pos.menu;
    

Copy

Your output shows the columns of the table you created. At this point in the
tutorial, the table does not have any rows.

## Step 5. Create a stage and load the data¶

A stage is a location that holds data files to load into a Snowflake database.
This tutorial creates a stage that loads data from an Amazon S3 bucket. This
tutorial uses an existing bucket with a CSV file that contains the data. You
load the data from this CSV file into the table you created previously. For
information, see [Bulk loading from Amazon S3](../data-load-s3).

To create a stage, do the following:

  1. In the open worksheet, place your cursor in the CREATE OR REPLACE STAGE lines, then select Run.
    
        CREATE OR REPLACE STAGE tasty_bytes_sample_data.public.blob_stage
    url = 's3://sfquickstarts/tastybytes/'
    file_format = (type = csv);
    

Copy

  2. To confirm that the stage was created successfully, place your cursor in the LIST line, then select Run.
    
        LIST @tasty_bytes_sample_data.public.blob_stage/raw_pos/menu/;
    

Copy

Your output looks similar to the following image.

![Table output with the following columns: name, size, md5, last_modified. One
row shows the details for the stage.](../../_images/tasty-bytes-list-
results.png)

  3. To load the data into the table, place your cursor in the COPY INTO lines, then select Run.
    
        COPY INTO tasty_bytes_sample_data.raw_pos.menu
    FROM @tasty_bytes_sample_data.public.blob_stage/raw_pos/menu/;
    

Copy

## Step 6. Query the data¶

Now that the data is loaded, you can run queries on the `menu` table.

To run a query in the open worksheet, select the line or lines of the SELECT
command, and then select Run.

For example, to return the number of rows in the table, run the following
query:

    
    
    SELECT COUNT(*) AS row_count FROM tasty_bytes_sample_data.raw_pos.menu;
    

Copy

Your output looks similar to the following image.

![Table output with the following column: ROW_COUNT. One row with the
following value: 100.](../../_images/tasty-bytes-select-number-of-rows.png)

Run this query to return the top ten rows in the table:

    
    
    SELECT TOP 10 * FROM tasty_bytes_sample_data.raw_pos.menu;
    

Copy

Your output looks similar to the following image.

![Table output with the following columns: MENU_ID, MENU_TYPE_ID, MENU_TYPE,
TRUCK_BRAND_NAME, MENU_ITEM_ID, MENU_ITEM_NAME. The first row has the
following values: 10001, 1, Ice Cream, Freezing Point, 10,
Lemonade.](../../_images/tasty-bytes-select-top-ten.png)

For more information about running a query that returns the specified number
of rows, see [TOP <n>](../../sql-reference/constructs/top_n).

You can run other queries in the worksheet to explore the data in the `menu`
table.

## Step 7. Clean up, summary, and additional resources¶

Congratulations! You have successfully completed this tutorial for trial
accounts.

Take a few minutes to review a short summary and the key points covered in
this tutorial. Consider cleaning up by dropping any objects you created in
this tutorial. Learn more by reviewing other topics in the Snowflake
Documentation.

### Clean up tutorial objects (optional)¶

If the objects you created in this tutorial are no longer needed, you can
remove them from the system with [DROP <object>](../../sql-reference/sql/drop)
commands. To remove the database you created, run the following command:

    
    
    DROP DATABASE IF EXISTS tasty_bytes_sample_data;
    

Copy

### Summary and key points¶

In summary, you used a pre-loaded worksheet in Snowsight to complete the
following steps:

  1. Set the role and warehouse context.

  2. Create a database, schema, and table.

  3. Create a stage and load the data from the stage into the database.

  4. Query the data.

Here are some key points to remember about loading and querying data:

  * You need the required permissions to create and manage objects in your account. In this tutorial, you use the ACCOUNTADMIN system role for these privileges.

This role is not normally used to create objects. Instead, we recommend
creating a hierarchy of roles aligned with business functions in your
organization. For more information, see [Using the ACCOUNTADMIN
Role](../security-access-control-considerations.html#label-security-
accountadmin-role).

  * You need a warehouse for the resources required to create and manage objects and run SQL commands. This tutorial uses the `compute_wh` warehouse included with your trial account.

  * You created a database to store the data and a schema to group the database objects logically.

  * You created a stage to load data from a CSV file.

  * After the data was loaded into your database, you queried it using SELECT statements.

### What’s next?¶

Continue learning about Snowflake using the following resources:

  * Complete the other tutorials provided by Snowflake:

    * [Snowflake Tutorials](../../learn-tutorials)

  * Familiarize yourself with key Snowflake concepts and features, as well as the SQL commands used to perform queries and insert/update data:

    * [Introduction to Snowflake](../../user-guide-intro)

    * [Query syntax](../../sql-reference/constructs)

    * [Data Manipulation Language (DML) commands](../../sql-reference/sql-dml)

  * Try the Tasty Bytes Quickstarts provided by Snowflake:

    * [Tasty Bytes Quickstarts](https://quickstarts.snowflake.com/?cat=tasty-bytes)

