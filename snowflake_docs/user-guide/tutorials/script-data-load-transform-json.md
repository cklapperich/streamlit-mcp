# Tutorial: Loading JSON data into a relational table¶

## Introduction¶

When uploading JSON data into a table, you have these options:

  * Store JSON objects natively in a VARIANT type column (as shown in [Tutorial: Bulk loading from a local file system using COPY](data-load-internal-tutorial)).

  * Store JSON object natively in an intermediate table and then use FLATTEN function to extract JSON elements into separate columns in a table (as shown in [Tutorial: JSON basics for Snowflake](json-basics-tutorial))

  * Transform JSON elements directly into table columns as shown in this tutorial.

The COPY command in this tutorial uses a SELECT statement to query for
individual elements in a staged JSON file.

The example commands provided in this tutorial includes a [PUT](../../sql-
reference/sql/put) statement. We recommend executing these commands in SnowSQL
which supports the PUT command. Clients such as [Snowsight](../ui-snowsight-
gs) and the Classic Console do not support the PUT command.

## Prerequisites¶

For this tutorial you need to:

  * Download a Snowflake provided JSON data file.

  * Create a database, a table, and a virtual warehouse for this tutorial.

Database, table, and virtual warehouse are basic Snowflake objects required
for most Snowflake activities.

### Data file for loading¶

To download the sample JSON data file, click
[`sales.json`](../../_downloads/b50c24de20be843b34f2535dfe67fd5e/sales.json).
If clicking the link does not download the file, right-click the link and save
the link/file to your local file system.

The tutorial assumes you unpacked the JSON data file in to the following
directories:

>   * Linux/macOS: `/tmp/load`
>
>   * Windows: `C:\tempload`
>
>

The data file include sample home sales JSON data. An example JSON object is
shown:

    
    
    {
       "location": {
          "state_city": "MA-Lexington",
          "zip": "40503"
       },
       "sale_date": "2017-3-5",
       "price": "275836"
    }
    

Copy

### Creating the database, table, and virtual warehouse¶

The following commands create objects specifically for use with this tutorial.
When you have completed the tutorial, you can drop the objects.

    
    
     create or replace database mydatabase;
    
     use schema mydatabase.public;
    
    CREATE OR REPLACE TEMPORARY TABLE home_sales (
      city STRING,
      zip STRING,
      state STRING,
      type STRING DEFAULT 'Residential',
      sale_date timestamp_ntz,
      price STRING
      );
    
    create or replace warehouse mywarehouse with
      warehouse_size='X-SMALL'
      auto_suspend = 120
      auto_resume = true
      initially_suspended=true;
    
    use warehouse mywarehouse;
    

Copy

Note these commands creates temporary table. Temporary tables persist only for
the duration of the user session and is not visible to other users.

## Create file format object¶

Execute the [CREATE FILE FORMAT](../../sql-reference/sql/create-file-format)
command to create the `sf_tut_json_format` file format.

    
    
    CREATE OR REPLACE FILE FORMAT sf_tut_json_format
      TYPE = JSON;
    

Copy

`TYPE = 'JSON'` indicates the source file format type. CSV is the default file
format type.

## Create stage object¶

Execute [CREATE STAGE](../../sql-reference/sql/create-stage) to create the
internal `sf_tut_stage` stage.

>
>     CREATE OR REPLACE TEMPORARY STAGE sf_tut_stage
>      FILE_FORMAT = sf_tut_json_format;
>  
>
> Copy

Similar to temporary tables, temporary stages are automatically dropped at the
end of the session.

## Stage the data file¶

Execute the [PUT](../../sql-reference/sql/put) command to upload the JSON file
from your local file system to the named stage.

  * Linux or macOS

> >     PUT file:///tmp/load/sales.json @sf_tut_stage AUTO_COMPRESS=TRUE;
>  
>
> Copy

  * Windows

> >     PUT file://C:\temp\load\sales.json @sf_tut_stage AUTO_COMPRESS=TRUE;
>  
>
> Copy

## Copy data into the target table¶

Load the `sales.json.gz` staged data file into the `home_sales` table.

    
    
    COPY INTO home_sales(city, state, zip, sale_date, price)
       FROM (SELECT SUBSTR($1:location.state_city,4),
                    SUBSTR($1:location.state_city,1,2),
                    $1:location.zip,
                    to_timestamp_ntz($1:sale_date),
                    $1:price
             FROM @sf_tut_stage/sales.json.gz t)
       ON_ERROR = 'continue';
    

Copy

Note the $1 in the SELECT query refers to the single column where the JSON is
stored. The query also uses the following functions:

  * The [SUBSTR , SUBSTRING](../../sql-reference/functions/substr) function to extract city and state values from state_city JSON key.

  * The [TO_TIMESTAMP / TO_TIMESTAMP_*](../../sql-reference/functions/to_timestamp) to cast the sale_date JSON key value to a timestamp.

Execute the following query to verify data is copied.

    
    
    SELECT * from home_sales;
    

Copy

## Remove the successfully copied data files¶

After you verify that you successfully copied data from your stage into the
tables, you can remove data files from the internal stage using the
[REMOVE](../../sql-reference/sql/remove) command to save on [data
storage](../cost-understanding-compute).

>
>     REMOVE @sf_tut_stage/sales.json.gz;
>  
>
> Copy

## Clean up¶

Execute the following [DROP <object>](../../sql-reference/sql/drop) commands
to return your system to its state before you began the tutorial:

>
>     DROP DATABASE IF EXISTS mydatabase;
>     DROP WAREHOUSE IF EXISTS mywarehouse;
>  
>
> Copy

Dropping the database automatically removes all child database objects such as
tables.

