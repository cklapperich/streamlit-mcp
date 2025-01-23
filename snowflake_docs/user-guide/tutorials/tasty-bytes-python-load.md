# Load and query sample data using Snowpark Python¶

## Introduction¶

This tutorial uses a fictitious food truck brand named Tasty Bytes to show you
how to load and query data in Snowflake using [Snowpark
Python](../../developer-guide/snowpark/python/index). You use a pre-loaded
Python worksheet in Snowsight to complete these tasks.

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

In this tutorial you will learn how to complete the following tasks using the
[Snowpark Python API](https://docs.snowflake.com/en/developer-
guide/snowpark/reference/python/latest/index):

  * Create a database and schema.

  * Create a stage that holds data in an Amazon S3 bucket.

  * Create a DataFrame to specify the stage that is the source of the data.

  * Create a table that contains data from files on a stage.

  * Set up a DataFrame to query the new table and filter the data.

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

## Step 2. Open the Python worksheet¶

You can use Python worksheets to write and run Python code. Your trial account
has access to a pre-loaded Python worksheet for this tutorial. The worksheet
has the Python code that you will run to create a database, load data into it,
and query the data. For more information about Python worksheets, see [Writing
Snowpark Code in Python Worksheets](../../developer-
guide/snowpark/python/python-worksheets).

To open the pre-loaded tutorial Python worksheet:

  1. Select Projects » Worksheets to open the list of worksheets.

  2. Open [Tutorial] Using Python to load and query sample data.

Your worksheet looks similar to the following image.

> ![The Python load and query worksheet, which contains the code for this
> tutorial, along with descriptive comments.](../../_images/tasty-bytes-
> select-worksheet-python.png)

This pre-loaded Python worksheet automatically uses the ACCOUNTADMIN system
role so that you can view and manage objects in your account. For more
information, see [Using the ACCOUNTADMIN Role](../security-access-control-
considerations.html#label-security-accountadmin-role).

The worksheet also uses the COMPUTE_WH virtual warehouse. A warehouse provides
the required resources to create and manage objects and run SQL commands.
These resources include CPU, memory, and temporary storage. For more
information, see [Virtual warehouses](../warehouses).

## Step 3. Learn how to use Python worksheets¶

Python worksheets let you use [Snowpark Python](../../developer-
guide/snowpark/python/index) in Snowsight to run SQL statements. This step in
this tutorial describes the code in each step in the Python worksheet. When
you use a Python worksheet, you cannot run individual blocks of code
separately. You must run the whole worksheet. Before you select Run in the
worksheet, review the following steps so that you better understand the Python
code.

  1. In the open Python worksheet, this step includes the following code:
    
        import snowflake.snowpark as snowpark
    from snowflake.snowpark.functions import col
    from snowflake.snowpark.types import StructField, StructType, IntegerType, StringType, VariantType
    

Copy

This tutorial imports the `snowpark` package and selected classes and
functions so that they are available to your code.

  2. This step in the worksheet includes the following code:
    
        def main(session: snowpark.Session):
    

Copy

This line defines the default `main` handler function. The handler function
contains the code you will run in this tutorial. This line passes in a
`Session` object that you can use to execute SQL statements in Snowflake.

    
        # Use SQL to create our Tasty Bytes Database
    session.sql('CREATE OR REPLACE DATABASE tasty_bytes_sample_data;').collect()
    

Copy

This line creates a database named `tasty_bytes_sample_data`. This database
stores data in tables that you can manage and query. For more information, see
[Databases, Tables and Views - Overview](../../guides-overview-db).

The code uses the [sql](https://docs.snowflake.com/en/developer-
guide/snowpark/reference/python/latest/api/snowflake.snowpark.Session.sql)
method to create a [DataFrame](../../developer-guide/snowpark/python/working-
with-dataframes) that represents the results of the SQL statement. In
Snowpark, you can query and process data with a DataFrame. The code also uses
the [collect](https://docs.snowflake.com/en/developer-
guide/snowpark/reference/python/latest/api/snowflake.snowpark.DataFrame.collect)
method to run the SQL statement represented by the DataFrame. The other lines
of code in this step in the worksheet also use these methods.

    
        # Use SQL to create our Raw POS (Point-of-Sale) Schema
    session.sql('CREATE OR REPLACE SCHEMA tasty_bytes_sample_data.raw_pos;').collect()
    

Copy

This line creates a schema named `raw_pos` in the `tasty_bytes_sample_data`
database. A schema is a logical grouping of database objects, such as tables
and views. For example, a schema might contain the database objects required
for a specific application.

    
        # Use SQL to create our Blob Stage
    session.sql('CREATE OR REPLACE STAGE tasty_bytes_sample_data.public.blob_stage url = "s3://sfquickstarts/tastybytes/" file_format = (type = csv);').collect()
    

Copy

This line creates a stage named `blob_stage`. A stage is a location that holds
data files to load into a Snowflake database. This tutorial creates a stage
that loads data from an Amazon S3 bucket. The tutorial uses an existing bucket
with a CSV file that contains the data. It loads the data from this CSV file
into the table that is created later in this tutorial. For more information,
see [Bulk loading from Amazon S3](../data-load-s3).

  3. This step in the worksheet includes the following code:
    
        # Define our Menu Schema
    menu_schema = StructType([StructField("menu_id",IntegerType()),\
                         StructField("menu_type_id",IntegerType()),\
                         StructField("menu_type",StringType()),\
                         StructField("truck_brand_name",StringType()),\
                         StructField("menu_item_id",IntegerType()),\
                         StructField("menu_item_name",StringType()),\
                         StructField("item_category",StringType()),\
                         StructField("item_subcategory",StringType()),\
                         StructField("cost_of_goods_usd",IntegerType()),\
                         StructField("sale_price_usd",IntegerType()),\
                         StructField("menu_item_health_metrics_obj",VariantType())])
    

Copy

This code creates a `StructType` object named `menu_schema`. This object
consists of a `list` of `StructField` objects that describe the fields in the
CSV file in the stage. For more information, see [Working With Files in a
Stage](../../developer-guide/snowpark/python/working-with-
dataframes.html#label-snowpark-python-dataframe-stages).

  4. This step in the worksheet includes the following code:
    
        # Create a Dataframe from our Menu file from our Blob Stage
    df_blob_stage_read = session.read.schema(menu_schema).csv('@tasty_bytes_sample_data.public.blob_stage/raw_pos/menu/')
    

Copy

This line creates the `df_blob_stage_read` DataFrame. This DataFrame is
configured to read data from the CSV file located in the specified stage,
using the specified `menu_schema` schema. The schema contains information
about the types and names of the columns of data.

    
        # Save our Dataframe as a Menu table in our Tasty Bytes Database and Raw POS Schema
    df_blob_stage_read.write.mode("overwrite").save_as_table("tasty_bytes_sample_data.raw_pos.menu")
    

Copy

This code uses the [save_as_table](https://docs.snowflake.com/en/developer-
guide/snowpark/reference/python/latest/api/snowflake.snowpark.DataFrameWriter.save_as_table)
method to create the `menu` table and load the data from the stage into it.

  5. This step in the worksheet includes the following code:
    
        # Create a new Dataframe reading from our Menu table and filtering for the Freezing Point brand
    df_menu_freezing_point = session.table("tasty_bytes_sample_data.raw_pos.menu").filter(col("truck_brand_name") == 'Freezing Point')
    

Copy

This line creates the `df_menu_freezing_point` DataFrame and configures it to
query the `menu` table. The [filter](https://docs.snowflake.com/en/developer-
guide/snowpark/reference/python/latest/api/snowflake.snowpark.DataFrame.filter)
method prepares the SQL for execution with a conditional expression. The
conditional expression filters the rows in the `menu` table to return the rows
where the `truck_brand_name` column equals `Freezing Point` (similar to a
WHERE clause).

    
        # return our Dataframe
    return df_menu_freezing_point
    

Copy

This line returns the `df_menu_freezing_point` DataFrame so that the query is
ready for execution. DataFrames are lazily evaluated, which means that this
line does not send the query to the server for execution.

When you are ready, select Run to run the code and view the output. When you
select Run, the Python worksheet executes the Python code, which generates and
executes the SQL statements. The query for the returned DataFrame is executed,
and the results are displayed in the worksheet.

Your output looks similar to the following image.

![Table output with the following columns: MENU_ID, MENU_TYPE_ID, MENU_TYPE,
TRUCK_BRAND_NAME, MENU_ITEM_ID. The first row has the following values: 10001,
1, Ice Cream, Freezing Point, 10.](../../_images/tasty-bytes-python-
output.png)

## Step 4. Clean up, summary, and additional resources¶

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

In summary, you used a pre-loaded Python worksheet in Snowsight to complete
the following steps in Python code:

  1. Import Snowpark modules for a Python application.

  2. Create a Python function.

  3. Create a database and schema.

  4. Create a stage that holds data in an Amazon S3 bucket.

  5. Create a DataFrame to specify the source of the data in a stage.

  6. Create a table that contains data from files on the stage,

  7. Set up a DataFrame to query the new table and filter the data.

Here are some key points to remember about loading and querying data:

  * You used Snowpark to execute SQL statements in Python code.

  * You created a stage to load data from a CSV file.

  * You created a database to store the data and a schema to group the database objects logically.

  * You used a DataFrame to specify the data source and filter data for a query.

### What’s next?¶

Continue learning about Snowflake using the following resources:

  * Complete the other tutorials provided by Snowflake:

    * [Snowflake Tutorials](../../learn-tutorials)

  * Familiarize yourself with key Snowflake concepts and features, as well as the Snowpark Python classes and methods used to perform queries and insert/update data:

    * [Introduction to Snowflake](../../user-guide-intro)

    * [Snowpark Python](../../developer-guide/snowpark/python/index)

  * Try the Tasty Bytes Quickstarts provided by Snowflake:

    * [Tasty Bytes Quickstarts](https://quickstarts.snowflake.com/?cat=tasty-bytes)

