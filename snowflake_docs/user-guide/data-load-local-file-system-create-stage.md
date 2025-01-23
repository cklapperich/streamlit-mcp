# Choosing an internal stage for local files¶

A stage specifies where data files are stored (i.e. “staged”) so that the data
in the files can be loaded into a table.

## Types of internal stages¶

Snowflake supports the following types of internal stages:

>   * User
>
>   * Table
>
>   * Named
>
>

By default, each user and table in Snowflake is automatically allocated an
internal stage for staging data files to be loaded. In addition, you can
create named internal stages.

File staging information is required during both steps in the data loading
process:

  1. You must specify an internal stage in the [PUT](../sql-reference/sql/put) command when uploading files to Snowflake.

  2. You must specify the same stage in the [COPY INTO <table>](../sql-reference/sql/copy-into-table) command when loading data into a table from the staged files.

Consider the best type of stage for specific data files. Each option provides
benefits and potential drawbacks.

### User stages¶

Each user has a Snowflake stage allocated to them by default for storing
files. This stage is a convenient option if your files will only be accessed
by a single user, but need to be copied into multiple tables.

User stages have the following characteristics and limitations:

  * User stages are referenced using `@~`; e.g. use `LIST @~` to list the files in a user stage.

  * Unlike named stages, user stages cannot be altered or dropped.

  * User stages do not support setting file format options. Instead, you must specify file format and copy options as part of the [COPY INTO <table>](../sql-reference/sql/copy-into-table) command.

This option is not appropriate if:

  * Multiple users require access to the files.

  * The current user does not have INSERT privileges on the tables the data will be loaded into.

### Table stages¶

Note

Apache Iceberg™ tables in Snowflake don’t support table stages.

By default, each table has a Snowflake stage allocated to it for storing
files. This stage is called a _table_ stage.

You might use a table stage if you only need to copy files into a single
table, but want to make the files accessible to multiple users.

Table stages have the following characteristics and limitations:

  * A table stage has the same name as the table. For example, a table named `mytable` has a stage referenced as `@%mytable`.

  * A table stage is an implicit stage tied to a table object. It’s not a separate database object. As a result, a table stage has no grantable privileges of its own. A table stage is also not appropriate if you need to copy file data into multiple tables.

  * To stage files on a table stage, list the files, query the files, or drop them, you must be the table owner (have the role with the OWNERSHIP privilege on the table).

  * Unlike a named stage, you can’t alter or drop a table stage.

  * Table stages don’t support transforming data while loading it (using a query as the source for the COPY command).

### Named stages¶

Named stages are database objects that provide the greatest degree of
flexibility for data loading:

  * Users with the appropriate privileges on the stage can load data into any table.

  * Because the stage is a database object, the security/access rules that apply to all objects apply. The privileges to use a stage can be granted or revoked from roles. In addition, ownership of the stage can be transferred to another role.

If you plan to stage data files that will be loaded only by you, or will be
loaded only into a single table, then you may prefer to simply use either your
user stage or the stage for the table into which you will be loading data.

Named stages are optional but recommended when you plan regular data loads
that could involve multiple users and/or tables. For instructions on creating
a named stage, see Creating a Named Stage below.

## Creating a named stage¶

You can create a named internal stage using SQL or the web interface.

Note

To create an internal stage, you must use a role that is granted or inherits
the necessary privileges. For details, see [Access control
requirements](../sql-reference/sql/create-stage.html#label-create-stage-
privileges) for [CREATE STAGE](../sql-reference/sql/create-stage).

### Create a named stage using SQL¶

Use the [CREATE STAGE](../sql-reference/sql/create-stage) command to create a
named stage using SQL.

The following example creates an internal stage that uses server-side
encryption:

>
>     CREATE STAGE my_int_stage
>       ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');
>  
>
> Copy

### Create a named stage using Snowsight¶

To use Snowsight to create a named internal stage, do the following:

  1. Sign in to Snowsight.

  2. In the navigation menu, select Create » Stage » Snowflake Managed.

  3. In the Create Stage dialog, enter a Stage Name.

  4. Select the database and schema where you want to create the stage.

  5. Optionally deselect Directory table. Directory tables let you see files on the stage, but require a warehouse and thus incur a cost. You can choose to deselect this option for now and enable a directory table later.

  6. Select the type of Encryption supported for all files on your stage. For details, see [encryption for internal stages](../sql-reference/sql/create-stage.html#label-create-stage-internalstageparams). You can’t change the encryption type after you create the stage.

> Note
>
> To enable data access, use server-side encryption. Otherwise, staged files
> are client-side encrypted by default and unreadable when downloaded. For
> more information, see [Server-side encryption for unstructured data
> access](unstructured-intro.html#label-file-url-server-side-encryption).

  7. Complete the fields to describe your stage. For more information, see [CREATE STAGE](../sql-reference/sql/create-stage).

  8. Select Create.

### Create a named stage using Classic Console¶

Select Databases [![Databases tab](../_images/ui-navigation-database-
icon.svg)](../_images/ui-navigation-database-icon.svg) » _< db_name>_ »
Stages.

**Next:** [Staging data files from a local file system](data-load-local-file-
system-stage)

