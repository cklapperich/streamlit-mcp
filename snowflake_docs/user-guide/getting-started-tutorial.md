# Snowflake in 20 minutes¶

## Introduction¶

This tutorial uses the Snowflake command line client, [SnowSQL](../snowsql),
to introduce key concepts and tasks, including:

  * Creating Snowflake objects—You create a database and a table for storing data.

  * Loading data—We provide small sample CSV data files for you to load into the table.

  * Querying—You explore sample queries.

Note

Snowflake bills a minimal amount for the on-disk storage used for the sample
data in this tutorial. The tutorial provides steps to drop the database and
minimize storage cost.

Snowflake requires a [virtual warehouse](../warehouses) to load the data and
execute queries. A running virtual warehouse consumes Snowflake credits. In
this tutorial, you will be using a [30-day trial
account](https://signup.snowflake.com/), which provides free credits, so you
won’t incur any costs.

### What you’ll learn¶

In this tutorial you’ll learn how to:

  * Create Snowflake objects—You create a database and a table for storing data.

  * Install SnowSQL—You install and use SnowSQL, the Snowflake command line query tool.

Users of Visual Studio Code might consider using the [Snowflake Extension for
Visual Studio Code](../vscode-ext) instead of SnowSQL.

  * Load CSV data files—You use various mechanisms to load data into tables from CSV files.

  * Write and execute sample queries—You write and execute a variety of queries against newly loaded data.

## Prerequisites¶

This tutorial requires a database, table, and virtual warehouse to load and
query data. Creating these Snowflake objects requires a Snowflake user with a
role with the necessary access control privileges. In addition,
[SnowSQL](../snowsql) is required to execute the SQL statements in the
tutorial. Lastly, the tutorial requires CSV files that contain sample data to
load.

You can complete this tutorial using an existing Snowflake warehouse,
database, and table, and your own local data files, but we recommend using the
Snowflake objects and the set of provided data.

To set up Snowflake for this tutorial, complete the following before
continuing:

  1. Create a user

To create the database, table, and virtual warehouse, you must be logged in as
a Snowflake user with a role that grants you the privileges to create these
objects.

     * If you’re using a 30-day trial account, you can log in as the user that was created for the account. This user has the role with the privileges needed to create the objects.

     * If you don’t have a Snowflake user, you can’t perform this tutorial. If you don’t have a role that lets you create a user, ask someone who does to perform this step for you. Users with the ACCOUNTADMIN or SECURITYADMIN role can create users.

  2. Install SnowSQL

To install SnowSQL, see [Installing SnowSQL](../snowsql-install-config).

  3. Download sample data files

For this tutorial you download sample employee data files in CSV format that
Snowflake provides.

To download and unzip the sample data files:

    1. Download the set of sample data files. Right-click the name of the archive file, [`getting-started.zip`](../../_downloads/34f4a66f56d00340f8f7a92acaccd977/getting-started.zip), and save the link/file to your local file system.

    2. Unzip the sample files. The tutorial assumes you unpacked files into one of the following directories:

>      * Linux/macOS: `/tmp`
>
>      * Windows: `C:\\temp`

Each file has five data records. The data uses a comma (,) character as field
delimiter. The following is an example record:

    
        Althea,Featherstone,afeatherstona@sf_tuts.com,"8172 Browning Street, Apt B",Calatrava,7/12/2017
    

Copy

There are no blank spaces before or after the commas separating the fields in
each record. This is the default that Snowflake expects when loading CSV data.

## Log in to SnowSQL¶

After you have [SnowSQL](../snowsql), start SnowSQL to connect to Snowflake:

  1. Open a command line window.

  2. Start SnowSQL:
    
        $ snowsql -a <account_identifier> -u <user_name>
    

Copy

Where:

>      * `<account_identifier>` is the unique identifier for your Snowflake
> account.
>  
>
> The preferred format of the [account identifier](../admin-account-
> identifier) is as follows:
>
> `_organization_name_ -_account_name_`
>  
>
> Names of your Snowflake organization and account. For more information, see
> [Format 1 (preferred): Account name in your organization](../admin-account-
> identifier.html#label-account-name).
>
>      * `<user_name>` is the login name for your Snowflake user.

Note

If your account has an identity provider (IdP) that has been defined for your
account, you can use a web browser to authenticate instead of a password, as
the following example demonstrates:

    
        $ snowsql -a <account_identifier> -u <user_name> --authenticator externalbrowser
    

Copy

For more information, see [Using a web browser for federated
authentication/SSO](../snowsql-start.html#label-snowsql-web-browser-sso).

  3. When SnowSQL prompts you, enter the password for your Snowflake user.

If you log in successfully, SnowSQL displays a command prompt that includes
your current warehouse, database, and schema.

Note

If you get locked out of the account and can’t obtain the account identifier,
you can find it in the Welcome email that Snowflake sent to you when you
signed up for the trial account, or you can work with your ORGADMIN to [get
the account details](../../sql-reference/sql/show-accounts). You can also find
the values for `locator`, `cloud`, and `region` in the Welcome email.

If your Snowflake user doesn’t have a default warehouse, database, and schema,
or if you didn’t configure SnowSQL to specify a default warehouse, database,
and schema, the prompt displays `no warehouse`, `no database`, and `no
schema`. For example:

    
    
    user-name#(no warehouse)@(no database).(no schema)>
    

Copy

This prompt indicates that there is no warehouse, database, and schema
selected for the current session. You create these objects in the next step.
As you follow the next steps in this tutorial to create these objects, the
prompt automatically updates to include the names of these objects.

For more information, see [Connecting through SnowSQL](../snowsql-start).

## Create Snowflake objects¶

During this step you create the following Snowflake objects:

  * A database (`sf_tuts`) and a table (`emp_basic`). You load sample data into this table.

  * A [virtual warehouse](../warehouses-overview) (`sf_tuts_wh`). This warehouse provides the compute resources needed to load data into the table and query the table. For this tutorial, you create an X-Small warehouse.

At the completion of this tutorial, you will remove these objects.

### Create a database¶

Create the `sf_tuts` database using the [CREATE DATABASE](../../sql-
reference/sql/create-database) command:

    
    
    CREATE OR REPLACE DATABASE sf_tuts;
    

Copy

In this tutorial, you use the default schema (`public`) available for each
database, rather than creating a new schema.

Note that the database and schema you just created are now in use for your
current session, as reflected in the SnowSQL command prompt. You can also use
the context functions to get this information.

    
    
    SELECT CURRENT_DATABASE(), CURRENT_SCHEMA();
    

Copy

The following is an example result:

    
    
    +--------------------+------------------+
    | CURRENT_DATABASE() | CURRENT_SCHEMA() |
    |--------------------+------------------|
    | SF_TUTS            | PUBLIC           |
    +--------------------+------------------+
    

### Create a table¶

Create a table named `emp_basic` in `sf_tuts.public` using the [CREATE
TABLE](../../sql-reference/sql/create-table) command:

    
    
    CREATE OR REPLACE TABLE emp_basic (
       first_name STRING ,
       last_name STRING ,
       email STRING ,
       streetaddress STRING ,
       city STRING ,
       start_date DATE
       );
    

Copy

Note that the number of columns in the table, their positions, and their data
types correspond to the fields in the sample CSV data files that you stage in
the next step in this tutorial.

### Create a virtual warehouse¶

Create an X-Small warehouse named `sf_tuts_wh` using the [CREATE
WAREHOUSE](../../sql-reference/sql/create-warehouse) command:

    
    
    CREATE OR REPLACE WAREHOUSE sf_tuts_wh WITH
       WAREHOUSE_SIZE='X-SMALL'
       AUTO_SUSPEND = 180
       AUTO_RESUME = TRUE
       INITIALLY_SUSPENDED=TRUE;
    

Copy

The `sf_tuts_wh` warehouse is initially suspended, but the DML statement also
sets `AUTO_RESUME = true`. The AUTO_RESUME setting causes a warehouse to
automatically start when SQL statements that require compute resources are
executed.

After you create the warehouse, it’s now in use for your current session. This
information is displayed in your SnowSQL command prompt. You can also retrieve
the name of the warehouse by using the following context function:

    
    
    SELECT CURRENT_WAREHOUSE();
    

Copy

The following is an example result:

    
    
    +---------------------+
    | CURRENT_WAREHOUSE() |
    |---------------------|
    | SF_TUTS_WH          |
    +---------------------+
    

## Stage data files¶

A Snowflake stage is a location in cloud storage that you use to load and
unload data from a table. Snowflake supports the following types of stages:

  * **Internal stages** —Used to store data files internally within Snowflake. Each user and table in Snowflake gets an internal stage by default for staging data files.

  * **External stages** —Used to store data files externally in Amazon S3, Google Cloud Storage, or Microsoft Azure. If your data is already stored in these cloud storage services, you can use an external stage to load data in Snowflake tables.

In this tutorial, we upload the sample data files (downloaded in
Prerequisites) to the internal stage for the `emp_basic` table that you
created earlier. You use the [PUT](../../sql-reference/sql/put) command to
upload the sample data files to that stage.

### Staging sample data files¶

Execute the [PUT](../../sql-reference/sql/put) command in
[SnowSQL](../snowsql) to upload local data files to the table stage provided
for the `emp_basic` table you created.

    
    
    PUT file://<file-path>[/\]employees0*.csv @sf_tuts.public.%emp_basic;
    

Copy

For example:

  * Linux or macOS
    
        PUT file:///tmp/employees0*.csv @sf_tuts.public.%emp_basic;
    

Copy

  * Windows
    
        PUT file://C:\temp\employees0*.csv @sf_tuts.public.%emp_basic;
    

Copy

Let’s take a closer look at the command:

  * `file://<file-path>[/]employees0*.csv` specifies the full directory path and names of the files on your local machine to stage. Note that file system wildcards are allowed, and if multiple files fit the pattern they are all displayed.

  * `@<namespace>.%<table_name>` indicates to use the stage for the specified table, in this case the `emp_basic` table.

The command returns the following result, showing the staged files:

    
    
    +-----------------+--------------------+-------------+-------------+--------------------+--------------------+----------+---------+
    | source          | target             | source_size | target_size | source_compression | target_compression | status   | message |
    |-----------------+--------------------+-------------+-------------+--------------------+--------------------+----------+---------|
    | employees01.csv | employees01.csv.gz |         360 |         287 | NONE               | GZIP               | UPLOADED |         |
    | employees02.csv | employees02.csv.gz |         355 |         274 | NONE               | GZIP               | UPLOADED |         |
    | employees03.csv | employees03.csv.gz |         397 |         295 | NONE               | GZIP               | UPLOADED |         |
    | employees04.csv | employees04.csv.gz |         366 |         288 | NONE               | GZIP               | UPLOADED |         |
    | employees05.csv | employees05.csv.gz |         394 |         299 | NONE               | GZIP               | UPLOADED |         |
    +-----------------+--------------------+-------------+-------------+--------------------+--------------------+----------+---------+
    

The PUT command compresses files by default using `gzip`, as indicated in the
TARGET_COMPRESSION column.

### Listing the staged files (Optional)¶

You can list the staged files using the [LIST](../../sql-reference/sql/list)
command.

    
    
    LIST @sf_tuts.public.%emp_basic;
    

Copy

The following is an example result:

    
    
    +--------------------+------+----------------------------------+------------------------------+
    | name               | size | md5                              | last_modified                |
    |--------------------+------+----------------------------------+------------------------------|
    | employees01.csv.gz |  288 | a851f2cc56138b0cd16cb603a97e74b1 | Tue, 9 Jan 2018 15:31:44 GMT |
    | employees02.csv.gz |  288 | 125f5645ea500b0fde0cdd5f54029db9 | Tue, 9 Jan 2018 15:31:44 GMT |
    | employees03.csv.gz |  304 | eafee33d3e62f079a054260503ddb921 | Tue, 9 Jan 2018 15:31:45 GMT |
    | employees04.csv.gz |  304 | 9984ab077684fbcec93ae37479fa2f4d | Tue, 9 Jan 2018 15:31:44 GMT |
    | employees05.csv.gz |  304 | 8ad4dc63a095332e158786cb6e8532d0 | Tue, 9 Jan 2018 15:31:44 GMT |
    +--------------------+------+----------------------------------+------------------------------+
    

## Copy data into target tables¶

To load your staged data into the target table, execute [COPY INTO
<table>](../../sql-reference/sql/copy-into-table).

The [COPY INTO <table>](../../sql-reference/sql/copy-into-table) command uses
the virtual warehouse you created in Create Snowflake objects to copy files.

    
    
    COPY INTO emp_basic
      FROM @%emp_basic
      FILE_FORMAT = (type = csv field_optionally_enclosed_by='"')
      PATTERN = '.*employees0[1-5].csv.gz'
      ON_ERROR = 'skip_file';
    

Copy

Where:

  * The FROM clause specifies the location containing the data files (the internal stage for the table).

  * The FILE_FORMAT clause specifies the file type as CSV, and specifies the double-quote character (`"`) as the character used to enclose strings. Snowflake supports diverse file types and options. These are described in [CREATE FILE FORMAT](../../sql-reference/sql/create-file-format).

  * The PATTERN clause specifies that the command should load data from the filenames matching this regular expression (`.*employees0[1-5].csv.gz`).

  * The ON_ERROR clause specifies what to do when the COPY command encounters errors in the files. By default, the command stops loading data when the first error is encountered. This example skips any file containing an error and moves on to loading the next file. (None of the files in this tutorial contain errors; this is included for illustration purposes.)

The COPY command also provides an option for validating files before they are
loaded. For more information about additional error checking and validation
instructions, see the [COPY INTO <table>](../../sql-reference/sql/copy-into-
table) topic and the other [data loading tutorials](../../guides-overview-
loading-data).

The COPY command returns a result showing the list of files copied and related
information:

    
    
    +--------------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------+
    | file               | status | rows_parsed | rows_loaded | error_limit | errors_seen | first_error | first_error_line | first_error_character | first_error_column_name |
    |--------------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------|
    | employees02.csv.gz | LOADED |           5 |           5 |           1 |           0 | NULL        |             NULL |                  NULL | NULL                    |
    | employees04.csv.gz | LOADED |           5 |           5 |           1 |           0 | NULL        |             NULL |                  NULL | NULL                    |
    | employees05.csv.gz | LOADED |           5 |           5 |           1 |           0 | NULL        |             NULL |                  NULL | NULL                    |
    | employees03.csv.gz | LOADED |           5 |           5 |           1 |           0 | NULL        |             NULL |                  NULL | NULL                    |
    | employees01.csv.gz | LOADED |           5 |           5 |           1 |           0 | NULL        |             NULL |                  NULL | NULL                    |
    +--------------------+--------+-------------+-------------+-------------+-------------+-------------+------------------+-----------------------+-------------------------+
    

## Query loaded data¶

You can query the data loaded in the `emp_basic` table using standard
[SQL](../../sql-reference/constructs) and any supported [functions](../../sql-
reference-functions) and [operators](../../sql-reference/operators).

You can also manipulate the data, such as updating the loaded data or
inserting more data, using standard [DML commands](../../sql-reference/sql-
dml).

### Retrieve all data¶

Return all rows and columns from the table:

    
    
    SELECT * FROM emp_basic;
    

Copy

The following is a partial result:

    
    
    +------------+--------------+---------------------------+-----------------------------+--------------------+------------+
    | FIRST_NAME | LAST_NAME    | EMAIL                     | STREETADDRESS               | CITY               | START_DATE |
    |------------+--------------+---------------------------+-----------------------------+--------------------+------------|
    | Arlene     | Davidovits   | adavidovitsk@sf_tuts.com  | 7571 New Castle Circle      | Meniko             | 2017-05-03 |
    | Violette   | Shermore     | vshermorel@sf_tuts.com    | 899 Merchant Center         | Troitsk            | 2017-01-19 |
    | Ron        | Mattys       | rmattysm@sf_tuts.com      | 423 Lien Pass               | Bayaguana          | 2017-11-15 |
     ...
     ...
     ...
    | Carson     | Bedder       | cbedderh@sf_tuts.co.au    | 71 Clyde Gallagher Place    | Leninskoye         | 2017-03-29 |
    | Dana       | Avory        | davoryi@sf_tuts.com       | 2 Holy Cross Pass           | Wenlin             | 2017-05-11 |
    | Ronny      | Talmadge     | rtalmadgej@sf_tuts.co.uk  | 588 Chinook Street          | Yawata             | 2017-06-02 |
    +------------+--------------+---------------------------+-----------------------------+--------------------+------------+
    

Copy

### Insert additional data rows¶

In addition to loading data from staged files into a table, you can insert
rows directly into a table using the [INSERT](../../sql-reference/sql/insert)
DML command.

For example, to insert two additional rows into the table:

    
    
    INSERT INTO emp_basic VALUES
       ('Clementine','Adamou','cadamou@sf_tuts.com','10510 Sachs Road','Klenak','2017-9-22') ,
       ('Marlowe','De Anesy','madamouc@sf_tuts.co.uk','36768 Northfield Plaza','Fangshan','2017-1-26');
    

Copy

### Query rows based on email address¶

Return a list of email addresses with United Kingdom top-level domains using
the [[ NOT ] LIKE](../../sql-reference/functions/like) function:

    
    
    SELECT email FROM emp_basic WHERE email LIKE '%.uk';
    

Copy

The following is an example result:

    
    
    +--------------------------+
    | EMAIL                    |
    |--------------------------|
    | gbassfordo@sf_tuts.co.uk |
    | rtalmadgej@sf_tuts.co.uk |
    | madamouc@sf_tuts.co.uk   |
    +--------------------------+
    

### Query rows based on start date¶

For example, to calculate when certain employee benefits might start, add 90
days to employee start dates using the [DATEADD](../../sql-
reference/functions/dateadd) function. Filter the list by employees whose
start date occurred earlier than January 1, 2017:

    
    
    SELECT first_name, last_name, DATEADD('day',90,start_date) FROM emp_basic WHERE start_date <= '2017-01-01';
    

Copy

The following is an example result:

    
    
    +------------+-----------+------------------------------+
    | FIRST_NAME | LAST_NAME | DATEADD('DAY',90,START_DATE) |
    |------------+-----------+------------------------------|
    | Granger    | Bassford  | 2017-03-30                   |
    | Catherin   | Devereu   | 2017-03-17                   |
    | Cesar      | Hovie     | 2017-03-21                   |
    | Wallis     | Sizey     | 2017-03-30                   |
    +------------+-----------+------------------------------+
    

## Summary, clean up, and additional resources¶

Congratulations! You’ve successfully completed this introductory tutorial.

Take a few minutes to review a short summary and the key points covered in the
tutorial. You might also want to consider cleaning up by dropping any objects
you created in the tutorial. Learn more by reviewing other topics in the
Snowflake Documentation.

### Summary and key points¶

In summary, data loading is performed in two steps:

  1. Stage the data files to load. The files can be staged internally (in Snowflake) or in an external location. In this tutorial, you stage files internally.

  2. Copy data from the staged files into an existing target table. A running warehouse is required for this step.

Remember the following key points about loading CSV files:

  * A CSV file consists of 1 or more records, with 1 or more fields in each record, and sometimes a header record.

  * Records and fields in each file are separated by delimiters. The default delimiters are:

> Records:
>  
>
> newline characters
>
> Fields:
>  
>
> commas

In other words, Snowflake expects each record in a CSV file to be separated by
new lines and the fields (i.e. individual values) in each record to be
separated by commas. If different characters are used as record and field
delimiters, you must explicitly specify this as part of the file format when
loading.

  * There is a direct correlation between the fields in the files and the columns in the table you will be loading, in terms of:

>     * Number of fields (in the file) and columns (in the target table).
>
>     * Positions of the fields and columns within their respective
> file/table.
>
>     * Data types, such as string, number, or date, for fields and columns.

The records will not be loaded if the numbers, positions, and data types don’t
align with the data.

Note

Snowflake supports loading files in which the fields don’t exactly align with
the columns in the target table; however, this is a more advanced data loading
topic (covered in [Transforming data during a load](../data-load-transform)).

### Tutorial cleanup (Optional)¶

If the objects you created in this tutorial are no longer needed, you can
remove them from the system with [DROP <object>](../../sql-reference/sql/drop)
statements.

    
    
    DROP DATABASE IF EXISTS sf_tuts;
    
    DROP WAREHOUSE IF EXISTS sf_tuts_wh;
    

Copy

### Exit the connection¶

To exit a connection, use the `!exit` command for SnowSQL (or its alias,
`!disconnect`).

Exit drops the current connection and quits SnowSQL if it is the last
connection.

### What’s next?¶

Continue learning about Snowflake using the following resources:

  * Complete the other tutorials provided by Snowflake:

    * [Snowflake Tutorials](../../learn-tutorials)

  * Familiarize yourself with key Snowflake concepts and features, as well as the SQL commands to perform queries and insert/update data:

    * [Introduction to Snowflake](../../user-guide-intro)

    * [Query syntax](../../sql-reference/constructs)

    * [Data Manipulation Language (DML) commands](../../sql-reference/sql-dml)

