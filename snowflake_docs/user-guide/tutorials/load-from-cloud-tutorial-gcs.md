# Load data from cloud storage: GCS¶

## Introduction¶

This tutorial shows you how to load data from cloud storage into Snowflake
using SQL. You use a template worksheet in Snowsight to complete these tasks.
You can choose which cloud provider you want to use: AWS S3, Microsoft Azure,
or Google Cloud Storage (GCS). The worksheet contains customized SQL commands
for compatibility with each type of storage.

Attention

The example provided in this tutorial is specific to GCS and shows SQL
commands that work for loading data from a GCS bucket.

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

  * Use a warehouse to access resources.

  * Create a database and schema.

  * Create a table.

  * Create a storage integration for your cloud platform.

  * Create a stage for your storage integration.

  * Load data into the table from the stage.

  * Query the data in the table.

## Prerequisites¶

This tutorial assumes the following:

  * You have a [supported browser](../ui-snowsight-gs.html#label-snowsight-getting-started-supported-browsers).

  * You have a trial account. If you do not have a trial account yet, you can sign up for a [free trial](https://signup.snowflake.com/). You can choose any [Snowflake Cloud Region](../intro-regions).

  * You have an account that you can use to bulk load data from one of the following cloud providers:

    * AWS S3. See [Bulk loading from Amazon S3](../data-load-s3).

    * Microsoft Azure. See [Bulk loading from Microsoft Azure](../data-load-azure).

    * Google Cloud Storage. See [Bulk loading from Google Cloud Storage](../data-load-gcs).

Note

This tutorial is only available to users with a trial account. The sample
worksheet is not available for other types of accounts.

## Step 1. Sign in using Snowsight¶

To access Snowsight over the public Internet, do the following:

  1. In a supported web browser, navigate to <https://app.snowflake.com>.

  2. Provide your [account identifier](../admin-account-identifier) or account URL. If you’ve previously signed in to Snowsight, you might see an account name that you can select.

  3. Sign in using your Snowflake account credentials.

## Step 2. Open the Load data from cloud storage worksheet¶

You can use worksheets to write and run SQL commands on your database. Your
trial account has access to a template worksheet for this tutorial. The
worksheet has the SQL commands that you will run to create database objects,
load data, and query the data. Because it is a template worksheet, you will be
invited to enter your own values for certain SQL parameters. For more
information about worksheets, see [Getting started with worksheets](../ui-
snowsight-worksheets-gs).

The worksheet for this tutorial is not pre-loaded into the trial account. To
open the worksheet for this tutorial:

  1. If you are signing in to your Snowsight trial account for the first time, select Start under Load data into Snowflake on the Where do you want to start? screen.

If you have left the Where do you want to start? screen, go to the Worksheets
tab and select Continue in the banner.

  2. Click anywhere in the middle panel named Load data from cloud storage.

The [Template] Load data from cloud storage worksheet opens, and your browser
looks similar to the following image.

> ![SQL load from cloud template worksheet, which contains the SQL commands
> for this tutorial, along with descriptive comments.](../../_images/load-
> data-from-cloud-worksheet.png)

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

A database is a repository for your data. The data is stored in tables that
you can manage and query. A schema is a logical grouping of database objects,
such as tables and views. For example, a schema might contain the database
objects required for a specific application. For more information, see
[Databases, Tables and Views - Overview](../../guides-overview-db).

To create a database, a schema, and a table, do the following:

  1. In the open worksheet, place your cursor in the CREATE OR REPLACE DATABASE line, enter a name for your database and an optional comment, then select Run. For example:
    
        CREATE OR REPLACE DATABASE cloud_data_db
      COMMENT = 'Database for loading cloud data';
    

Copy

  2. Place your cursor in the CREATE OR REPLACE SCHEMA line, enter a name for your schema and an optional comment, then select Run. For example:
    
        CREATE OR REPLACE SCHEMA cloud_data_db.gcs_data
      COMMENT = 'Schema for tables loaded from GCS';
    

Copy

  3. Place your cursor in the CREATE OR REPLACE TABLE lines, complete the table definition, add an optional comment, and select Run. For example, the following table contains six columns:
    
        CREATE OR REPLACE TABLE cloud_data_db.gcs_data.calendar
      (
      full_date DATE,
      day_name VARCHAR(10),
      month_name VARCHAR(10),
      day_number VARCHAR(2),
      full_year VARCHAR(4),
      holiday BOOLEAN
      )
      COMMENT = 'Table to be loaded from GCS calendar data file';
    

Copy

  4. To confirm that the table was created successfully, place your cursor in the SELECT line, then select Run.
    
        SELECT * FROM cloud_data_db.gcs_data.calendar;
    

Copy

The output shows the columns of the table you created. Currently, the table
does not have any rows.

## Step 5. Create a storage integration¶

Before you can load data from cloud storage, you must configure a storage
integration that is specific to your cloud provider. The following example is
specific to GCS.

Storage integrations are named, first-class Snowflake objects that avoid the
need for passing explicit cloud provider credentials such as secret keys or
access tokens; instead, integration objects reference a GCS service account.

To create a storage integration for GCS, do the following:

  1. In the open worksheet, place your cursor in the CREATE OR REPLACE STORAGE INTEGRATION lines, define the required parameters, and select Run. For example:
    
        CREATE OR REPLACE STORAGE INTEGRATION gcs_data_integration
      TYPE = EXTERNAL_STAGE
      STORAGE_PROVIDER = 'GCS'
      ENABLED = TRUE
      STORAGE_ALLOWED_LOCATIONS = ('gcs://tutorial24bucket/gcsdata/');
    

Copy

  2. Place your cursor in the DESCRIBE INTEGRATION line, specify the name of the storage integration you created, and select Run. This command returns information about the storage integration you created, including the Service Account ID (`STORAGE_GCP_SERVICE_ACCOUNT`) that was created automatically for your Snowflake account. You will use this value to configure permissions for Snowflake in the GCS Console.
    
        DESCRIBE INTEGRATION gcs_data_integration;
    

Copy

The output for this command looks similar to the following:

![Output of DESCRIBE INTEGRATION command, with the following columns:
property, property_type, property_value,
property_default.](../../_images/desc_storage_integration_gcs_output.png)

  3. Place your cursor in the SHOW INTEGRATIONS line and select Run.
    
        SHOW INTEGRATIONS;
    

Copy

The output for this command looks similar to the following:

![Output of SHOW INTEGRATIONS command, with the following columns: name, type,
category, enabled, comment,
created_on.](../../_images/show_storage_integration_gcs_output.png)

  4. Use the GCS Console to configure permissions to access storage buckets from your Cloud Storage Service Account. Follow Step 3 under [Configuring an integration for Google Cloud Storage](../data-load-gcs-config).

## Step 6. Create a stage¶

A stage is a location that holds data files to load into a Snowflake database.
This tutorial creates a stage that can load data from a specific type of cloud
storage, such as a GCS bucket.

To create a stage, do the following:

  1. In the open worksheet, place your cursor in the CREATE OR REPLACE STAGE lines, specify a name, the storage integration you created, the bucket URL, and the correct file format, then select Run. For example:
    
        CREATE OR REPLACE STAGE cloud_data_db.gcs_data.gcsdata_stage
      STORAGE_INTEGRATION = gcs_data_integration
      URL = 'gcs://tutorial24bucket/gcsdata/'
      FILE_FORMAT = (TYPE = CSV);
    

Copy

  2. Return information about the stage you created:
    
        SHOW STAGES;
    

Copy

The output for this command looks similar to the following:

![Output of SHOW STAGES command](../../_images/show_stage_output_gcs.png)

## Step 7. Load data from the stage¶

Load the table from the stage you created by using the [COPY INTO
<table>](../../sql-reference/sql/copy-into-table) command. For more
information about loading from GCS buckets, see [Copying data from a Google
Cloud Storage stage](../data-load-gcs-copy).

To load the data into the table, place your cursor in the COPY INTO lines,
specify the table name, the stage you created, and name of the file (or files)
you want to load, then select Run. For example:

>
>     COPY INTO cloud_data_db.gcs_data.calendar
>       FROM @cloud_data_db.gcs_data.gcsdata_stage
>         FILES = ('calendar.txt');
>  
>
> Copy

Your output looks similar to the following image.

![Copy five rows into the
table.](../../_images/load_from_cloud_copy_results_gcs.png)

## Step 8. Query the table¶

Now that the data is loaded, you can run queries on the `calendar` table.

To run a query in the open worksheet, select the line or lines of the SELECT
command, and then select Run. For example, run the following query:

    
    
    SELECT * FROM cloud_data_db.gcs_data.calendar;
    

Copy

Your output looks similar to the following image.

![Select all the rows in the
table.](../../_images/load_from_cloud_query_results.png)

## Step 9. Cleanup, summary, and additional resources¶

Congratulations! You have successfully completed this tutorial for trial
accounts.

Take a few minutes to review a short summary and the key points covered in the
tutorial. You might also want to consider cleaning up by dropping any objects
you created in the tutorial. Learn more by reviewing other topics in the
Snowflake Documentation.

### Summary and Key Points¶

In summary, you used a pre-loaded template worksheet in Snowsight to complete
the following steps:

  1. Set the role and warehouse to use.

  2. Create a database, schema, and table.

  3. Create a storage integration and configure permissions on cloud storage.

  4. Create a stage and load the data from the stage into the table.

  5. Query the data.

Here are some key points to remember about loading and querying data:

  * You need the required permissions to create and manage objects in your account. In this tutorial, you use the ACCOUNTADMIN system role for these privileges.

This role is not normally used to create objects. Instead, we recommend
creating a hierarchy of roles aligned with business functions in your
organization. For more information, see [Using the ACCOUNTADMIN
Role](../security-access-control-considerations.html#label-security-
accountadmin-role).

  * You need a warehouse for the resources required to create and manage objects and run SQL commands. This tutorial uses the `compute_wh` warehouse included with your trial account.

  * You created a database to store the data and a schema to group the database objects logically.

  * You created a storage integration and a stage to load data from a CSV file stored in a GCS bucket.

  * After the data was loaded into your database, you queried it using a SELECT statement.

### What’s next?¶

Continue learning about Snowflake using the following resources:

  * Complete the other tutorials provided by Snowflake:

    * [Snowflake Tutorials](../../learn-tutorials)

  * Familiarize yourself with key Snowflake concepts and features, as well as the SQL commands used to load tables from cloud storage:

    * [Introduction to Snowflake](../../user-guide-intro)

    * [Load data into Snowflake](../../guides-overview-loading-data)

    * [Data loading and unloading commands](../../sql-reference/commands-data-loading)

  * Try the Tasty Bytes Quickstarts provided by Snowflake:

    * [Tasty Bytes Quickstarts](https://quickstarts.snowflake.com/?cat=tasty-bytes)

