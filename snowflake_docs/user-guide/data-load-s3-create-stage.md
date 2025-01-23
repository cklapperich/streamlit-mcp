# Creating an S3 stage¶

An external (i.e. S3) stage specifies where data files are stored so that the
data in the files can be loaded into a table.

Data can be loaded directly from files in a specified S3 bucket, with or
without a folder path (or prefix, in S3 terminology). If the path ends with
`/`, all of the objects in the corresponding S3 folder are loaded.

Note

In the [previous step](data-load-s3-config), if you followed the instructions
to configure an AWS IAM role with the required policies and permissions to
access your external S3 bucket, you have already created an S3 stage. You can
skip this step and continue to [Copying data from an S3 stage](data-
load-s3-copy).

## External stages¶

In addition to loading directly from files in S3 buckets, Snowflake supports
creating named external stages, which encapsulate all of the required
information for staging files, including:

  * The S3 bucket where the files are staged.

  * The named storage integration object or S3 credentials for the bucket (if it is protected).

  * An encryption key (if the files in the bucket have been encrypted).

Named external stages are optional, but recommended when you plan to load data
regularly from the same location.

## Creating an external stage¶

You can create a named external stage using SQL or the web interface.

Note

To create an internal stage, you must use a role that is granted or inherits
the necessary privileges. For details, see [Access control
requirements](../sql-reference/sql/create-stage.html#label-create-stage-
privileges) for [CREATE STAGE](../sql-reference/sql/create-stage).

### Create an external stage using SQL¶

Use the [CREATE STAGE](../sql-reference/sql/create-stage) command to create an
external stage using SQL.

The following example uses SQL to create an external stage named `my_s3_stage`
that references a private/protected S3 bucket named `mybucket` with a folder
path named `encrypted_files/`. The CREATE statement includes the `s3_int`
storage integration that was created in [Option 1: Configuring a Snowflake
storage integration to access Amazon S3](data-load-s3-config-storage-
integration) to access the S3 bucket. The stage references a named file format
object named `my_csv_format`, which describes the data in the files stored in
the bucket path:

>
>     CREATE STAGE my_s3_stage
>       STORAGE_INTEGRATION = s3_int
>       URL = 's3://mybucket/encrypted_files/'
>       FILE_FORMAT = my_csv_format;
>  
>
> Copy

Note

By specifying a named file format object (or individual file format options)
for the stage, it is not necessary to later specify the same file format
options in the COPY command used to load data from the stage.

### Create an external stage using Snowsight¶

To use Snowsight to create a named external stage, do the following:

  1. Sign in to Snowsight.

  2. In the navigation menu, select Create » Stage » External Stage.

  3. Select your external cloud storage provider: Amazon S3, Microsoft Azure, or Google Cloud Platform.

  4. In the Create Stage dialog, enter a Stage Name.

  5. Select the database and schema where you want to create the stage.

  6. Enter the URL of your external cloud storage location.

  7. If your external storage isn’t public, enable Authentication and enter your details. For more information, see [CREATE STAGE](../sql-reference/sql/create-stage).

  8. Optionally deselect Directory table. Directory tables let you see files on the stage, but require a warehouse and thus incur a cost. You can choose to deselect this option for now and enable a directory table later.

> If you enable Directory table, optionally select Enable auto-refresh and
> select your event notification or notification integration to automatically
> refresh the directory table when files are added or removed. To learn more,
> see [Automated directory table metadata refreshes](data-load-dirtables-
> auto).

  9. If your files are encrypted, enable Encryption and enter your details.

  10. Optionally expand the SQL Preview to view a generated SQL statement. To specify additional options for your stage such as AUTO_REFRESH, you can open this SQL preview in a worksheet.

  11. Select Create.

### Create an external stage using Classic Console¶

Select Databases [![Databases tab](../_images/ui-navigation-database-
icon.svg)](../_images/ui-navigation-database-icon.svg) » _< db_name>_ »
Stages.

**Next:** [Copying data from an S3 stage](data-load-s3-copy)

