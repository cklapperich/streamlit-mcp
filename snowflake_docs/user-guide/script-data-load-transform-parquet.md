# Tutorial: Loading and unloading Parquet data¶

## Introduction¶

This tutorial describes how you can upload Parquet data by transforming
elements of a staged Parquet file directly into table columns using the [COPY
INTO <table>](../../sql-reference/sql/copy-into-table) command. The tutorial
also describes how you can use the [COPY INTO <location>](../../sql-
reference/sql/copy-into-location) command to unload table data into a Parquet
file.

## Prerequisites¶

For this tutorial you need to:

  * Download a Snowflake provided Parquet data file.

  * Create a database, a table, and a virtual warehouse.

Database, table, and virtual warehouse are basic Snowflake objects required
for most Snowflake activities.

### Downloading the sample data file¶

To download the sample Parquet data file, click
[`cities.parquet`](../../_downloads/0c1e6c4f4140561029eeb20afdd02664/cities.parquet).
Alternatively, right-click the link and save the link/file to your local file
system.

The tutorial assumes you unpacked files in to the following directories:

>   * Linux/macOS: `/tmp/load`
>
>   * Windows: `C:\tempload`
>
>

The Parquet data file includes sample continent data. The following is a
representative example:

    
    
    {
      "continent": "Europe",
      "country": {
        "city": [
          "Paris",
          "Nice",
          "Marseilles",
          "Cannes"
        ],
        "name": "France"
      }
    }
    

Copy

### Creating the database, table, and virtual warehouse¶

The following commands create objects specifically for use with this tutorial.
When you have completed the tutorial, you can drop these objects.

    
    
     create or replace database mydatabase;
    
     use schema mydatabase.public;
    
      create or replace temporary table cities (
        continent varchar default null,
        country varchar default null,
        city variant default null
      );
    
    create or replace warehouse mywarehouse with
      warehouse_size='X-SMALL'
      auto_suspend = 120
      auto_resume = true
      initially_suspended=true;
    
    use warehouse mywarehouse;
    

Copy

Note these commands create a temporary table. Temporary tables persist only
for the duration of the user session and is not visible to other users.

## Create file format object¶

Execute the [CREATE FILE FORMAT](../../sql-reference/sql/create-file-format)
command to create the `sf_tut_parquet_format` file format.

    
    
    CREATE OR REPLACE FILE FORMAT sf_tut_parquet_format
      TYPE = parquet;
    

Copy

`TYPE = 'parquet'` indicates the source file format type. CSV is the default
file format type.

## Create stage object¶

Execute the [CREATE STAGE](../../sql-reference/sql/create-stage) command to
create the internal `sf_tut_stage` stage.

    
    
    CREATE OR REPLACE TEMPORARY STAGE sf_tut_stage
    FILE_FORMAT = sf_tut_parquet_format;
    

Copy

Similar to temporary tables, temporary stages are automatically dropped at the
end of the session.

## Stage the data file¶

Execute the [PUT](../../sql-reference/sql/put) command to upload the parquet
file from your local file system to the named stage.

  * Linux or macOS

> >     PUT file:///tmp/load/cities.parquet @sf_tut_stage;
>  
>
> Copy

  * Windows

> >     PUT file://C:\temp\load\cities.parquet @sf_tut_stage;
>  
>
> Copy

## Copy data into the target table¶

Copy the `cities.parquet` staged data file into the `CITIES` table.

    
    
    copy into cities
     from (select $1:continent::varchar,
                  $1:country:name::varchar,
                  $1:country:city::variant
          from @sf_tut_stage/cities.parquet);
    

Copy

Note the following:

  * `$1` in the SELECT query refers to the single column where the Parquet data is stored.

  * The query casts each of the Parquet element values it retrieves to specific column types.

Execute the following query to verify data is copied.

    
    
    SELECT * from cities;
    

Copy

The query returns the following result:

    
    
    +---------------+---------+-----------------+
    | CONTINENT     | COUNTRY | CITY            |
    |---------------+---------+-----------------|
    | Europe        | France  | [               |
    |               |         |   "Paris",      |
    |               |         |   "Nice",       |
    |               |         |   "Marseilles", |
    |               |         |   "Cannes"      |
    |               |         | ]               |
    |---------------+---------+-----------------|
    | Europe        | Greece  | [               |
    |               |         |   "Athens",     |
    |               |         |   "Piraeus",    |
    |               |         |   "Hania",      |
    |               |         |   "Heraklion",  |
    |               |         |   "Rethymnon",  |
    |               |         |   "Fira"        |
    |               |         | ]               |
    |---------------+---------+-----------------|
    | North America | Canada  | [               |
    |               |         |   "Toronto",    |
    |               |         |   "Vancouver",  |
    |               |         |   "St. John's", |
    |               |         |   "Saint John", |
    |               |         |   "Montreal",   |
    |               |         |   "Halifax",    |
    |               |         |   "Winnipeg",   |
    |               |         |   "Calgary",    |
    |               |         |   "Saskatoon",  |
    |               |         |   "Ottawa",     |
    |               |         |   "Yellowknife" |
    |               |         | ]               |
    +---------------+---------+-----------------+
    

Copy

## Unload the table¶

Unload the `CITIES` table into another Parquet file.

Note

By default, Snowflake optimizes table columns in unloaded Parquet data files
by setting the smallest precision that accepts all of the values. If you
prefer consistent output file schema determined by the “logical” column data
types (i.e. the types in the unload SQL query or source table), set the
[ENABLE_UNLOAD_PHYSICAL_TYPE_OPTIMIZATION](../../sql-
reference/parameters.html#label-enable-unload-physical-type-optimization)
session parameter to FALSE.

    
    
    copy into @sf_tut_stage/out/parquet_
    from (select continent,
                 country,
                 c.value::string as city
         from cities,
              lateral flatten(input => city) c)
      file_format = (type = 'parquet')
      header = true;
    

Copy

Note the following:

  * The `file_format = (type = 'parquet')` specifies parquet as the format of the data file on the stage. When the Parquet file type is specified, the `COPY INTO <location>` command unloads data to a single column by default.

  * The `header=true` option directs the command to retain the column names in the output file.

  * In the nested SELECT query:

    * The [FLATTEN](../../sql-reference/functions/flatten) function first flattens the `city` column array elements into separate columns.

    * The LATERAL modifier joins the output of the FLATTEN function with information outside of the object - in this example, the `continent` and `country`.

Execute the following query to verify data is copied into staged Parquet file.

    
    
    select t.$1 from @sf_tut_stage/out/ t;
    

Copy

The query returns the following results (only partial result is shown):

    
    
    +---------------------------------+
    | $1                              |
    |---------------------------------|
    | {                               |
    |   "CITY": "Paris",              |
    |   "CONTINENT": "Europe",        |
    |   "COUNTRY": "France"           |
    | }                               |
    |---------------------------------|
    | {                               |
    |   "CITY": "Nice",               |
    |   "CONTINENT": "Europe",        |
    |   "COUNTRY": "France"           |
    | }                               |
    |---------------------------------|
    | {                               |
    |   "CITY": "Marseilles",         |
    |   "CONTINENT": "Europe",        |
    |   "COUNTRY": "France"           |
    | }                               |
    +---------------------------------+
    

Copy

## Remove the successfully copied data files¶

After you verify that you successfully copied data from your stage into the
tables, you can remove data files from the internal stage using the
[REMOVE](../../sql-reference/sql/remove) command to save on [data
storage](../cost-understanding-compute).

    
    
    REMOVE @sf_tut_stage/cities.parquet;
    

Copy

## Clean up¶

Execute the following [DROP <object>](../../sql-reference/sql/drop) commands
to return your system to its state before you began the tutorial:

    
    
    DROP DATABASE IF EXISTS mydatabase;
    DROP WAREHOUSE IF EXISTS mywarehouse;
    

Copy

Dropping the database automatically removes all child database objects such as
tables.

