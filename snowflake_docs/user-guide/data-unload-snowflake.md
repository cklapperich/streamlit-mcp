# Unloading into a Snowflake stage¶

This set of topics describes how to use the COPY command to unload data from a
table into an internal (i.e. Snowflake) stage. You can then download the
unloaded data files to your local file system.

As illustrated in the diagram below, unloading data to a local file system is
performed in two, separate steps:

Step 1:

    

Use the [COPY INTO <location>](../sql-reference/sql/copy-into-location)
command to copy the data from the Snowflake database table into one or more
files in a Snowflake stage. In the SQL statement, you specify the stage (named
stage or table/user stage) where the files are written.

Regardless of the stage you use, this step requires a running, current virtual
warehouse for the session if you execute the command manually or within a
script. The warehouse provides the compute resources to write rows from the
table.

Step 2:

    

Use the [GET](../sql-reference/sql/get) command to download the data files to
your local file system.

![Unloading data to a Snowflake stage](../_images/data-unload-snowflake.png)

Tip

The instructions in this set of topics assume you have read [Preparing to
unload data](data-unload-prepare) and have created a named file format, if
desired.

Before you begin, you may also want to read [Data unloading
considerations](data-unload-considerations) for best practices, tips, and
other guidance.

## Unloading the data¶

This section provides instructions for unloading table data to a named
internal stage, table stage, or user stage.

### Unloading data to a named internal stage¶

Internal stages are named database objects that provide the greatest degree of
flexibility for data unloading. Because they are database objects, privileges
for named stages can be granted to any role.

You can create an internal stage using either the web interface or SQL:

> Classic Console:
>  
>
> Click on Databases [![Databases tab](../_images/ui-navigation-database-
> icon.svg)](../_images/ui-navigation-database-icon.svg) » _< db_name>_ »
> Stages
>
> SQL:
>  
>
> [CREATE STAGE](../sql-reference/sql/create-stage)

#### Creating a named stage¶

The following example creates an internal stage that references the named file
format object called `my_csv_unload_format` that was created in [Preparing to
unload data](data-unload-prepare):

>
>     CREATE OR REPLACE STAGE my_unload_stage
>       FILE_FORMAT = my_csv_unload_format;
>  
>
> Copy

#### Unloading data to the named stage¶

  1. Use the [COPY INTO <location>](../sql-reference/sql/copy-into-location) command to unload all the rows from a table into one or more files into the `my_csv_unload_format` stage. The statement prefixes the unloaded file(s) with `unload/` to organize the files in the stage:

For example:

> >     COPY INTO @mystage/unload/ from mytable;
>  
>
> Copy

Note that the `@` character by itself identifies a named stage.

Note

Because the file format options were defined for the stage, it is not
necessary to specify the same file format options in the COPY command.

  2. Use the [LIST](../sql-reference/sql/list) command to view a list of files that have been unloaded to the stage:
    
        LIST @mystage;
    
    +----------------------------------+------+----------------------------------+-------------------------------+
    | name                             | size | md5                              | last_modified                 |
    |----------------------------------+------+----------------------------------+-------------------------------|
    | mystage/unload/data_0_0_0.csv.gz |  112 | 6f77daba007a643bdff4eae10de5bed3 | Mon, 11 Sep 2017 18:13:07 GMT |
    +----------------------------------+------+----------------------------------+-------------------------------+
    

Copy

  3. Use the [GET](../sql-reference/sql/get) command to download the generated file(s) from the table stage to your local machine. The following example downloads the files to the `data/unload` directory:

For example:

Linux or macOS:

> >     GET @mystage/unload/data_0_0_0.csv.gz file:///data/unload;
>  
>
> Copy

Windows:

> >     GET @mystage/unload/data_0_0_0.csv.gz file://C:\data\unload;
>  
>
> Copy

### Unloading data to a table stage¶

  1. Use the [COPY INTO <location>](../sql-reference/sql/copy-into-location) command to unload all the rows from a table into one or more files in the stage for the table. The following example unloads data files to the stage using the named `my_csv_unload_format` file format created in [Preparing to unload data](data-unload-prepare). The statement prefixes the unloaded file(s) with `unload/` to organize the files in the stage:

For example:

> >     COPY INTO @%mytable/unload/ from mytable FILE_FORMAT = (FORMAT_NAME =
> 'my_csv_unload_format' COMPRESSION = NONE);
>  
>
> Copy

Note that the `@%` character combination identifies a table stage.

  2. Use the [LIST](../sql-reference/sql/list) command to view a list of files that have been unloaded to the stage:
    
        LIST @%mytable;
    
    +-----------------------+------+----------------------------------+-------------------------------+
    | name                  | size | md5                              | last_modified                 |
    |-----------------------+------+----------------------------------+-------------------------------|
    | unload/data_0_0_0.csv |   96 | 29918f18bcb35e7b6b628ca41024236c | Mon, 11 Sep 2017 17:45:20 GMT |
    +-----------------------+------+----------------------------------+-------------------------------+
    

Copy

  3. Use the [GET](../sql-reference/sql/get) command to download the generated file(s) from the table stage to your local machine. The following example downloads the files to the `data/unload` directory:

For example:

Linux or macOS:

> >     GET @%mytable/unload/data_0_0_0.csv file:///data/unload;
>  
>
> Copy

Windows:

> >     GET @%mytable/unload/data_0_0_0.csv file://C:\data\unload;
>  
>
> Copy

### Unloading data to your user stage¶

  1. Use the [COPY INTO <location>](../sql-reference/sql/copy-into-location) command to unload all the rows from a table into one or more files in your stage. The following example unloads data files to your user stage using the named `my_csv_unload_format` file format created in [Preparing to unload data](data-unload-prepare). The statement prefixes the unloaded file(s) with `unload/` to organize the files in the stage:

For example:

> >     COPY INTO @~/unload/ from mytable FILE_FORMAT = (FORMAT_NAME =
> 'my_csv_unload_format' COMPRESSION = NONE);
>  
>
> Copy

Note that the `@~` character combination identifies a user stage.

  2. Use the [LIST](../sql-reference/sql/list) command to view a list of files that have been unloaded to the stage:
    
        LIST @~;
    
    +-----------------------+------+----------------------------------+-------------------------------+
    | name                  | size | md5                              | last_modified                 |
    |-----------------------+------+----------------------------------+-------------------------------|
    | unload/data_0_0_0.csv |   96 | 94a306c55733b95a0887511ff355936b | Mon, 11 Sep 2017 17:25:07 GMT |
    +-----------------------+------+----------------------------------+-------------------------------+
    

Copy

  3. Use the [GET](../sql-reference/sql/get) command to download the generated file(s) from your stage to your local machine. The following example downloads the files to the `data/unload` directory:

For example:

Linux or macOS:

> >     GET @~/unload/data_0_0_0.csv file:///data/unload;
>  
>
> Copy

Windows:

> >     GET @~/unload/data_0_0_0.csv file://C:\data\unload;
>  
>
> Copy

## Managing unloaded data files¶

Staged files can be deleted from a Snowflake stage using the [REMOVE](../sql-
reference/sql/remove) command to remove the files in the stage after you are
finished with them.

Removing files improves performance when loading data, because it reduces the
number of files that the [COPY INTO <table>](../sql-reference/sql/copy-into-
table) command must scan to verify whether existing files in a stage were
loaded already.

