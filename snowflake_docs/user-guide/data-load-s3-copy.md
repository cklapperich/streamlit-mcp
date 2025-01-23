# Copying data from an S3 stage¶

Load data from your staged files into the target table.

## Loading your data¶

Execute [COPY INTO <table>](../sql-reference/sql/copy-into-table) to load your
data into the target table.

Note

Loading data requires a [warehouse](warehouses). If you are using a warehouse
that is not configured to auto resume, execute [ALTER WAREHOUSE](../sql-
reference/sql/alter-warehouse) to resume the warehouse. Note that starting the
warehouse could take up to five minutes.

>
>     ALTER WAREHOUSE mywarehouse RESUME;
>  
>
> Copy

The following example loads data from files in the named `my_ext_stage` stage
created in [Creating an S3 stage](data-load-s3-create-stage). Using pattern
matching, the statement only loads files whose names start with the string
`sales`:

>
>     COPY INTO mytable
>       FROM @my_ext_stage
>       PATTERN='.*sales.*.csv';
>  
>
> Copy

Note that file format options are not specified because a named file format
was included in the stage definition.

The following example loads all files prefixed with `data/files` in your S3
bucket using the named `my_csv_format` file format created in [Preparing to
load data](data-load-prepare):

>
>     COPY INTO mytable
>       FROM s3://mybucket/data/files
> credentials=(AWS_KEY_ID='$AWS_ACCESS_KEY_ID'
> AWS_SECRET_KEY='$AWS_SECRET_ACCESS_KEY')
>       FILE_FORMAT = (FORMAT_NAME = my_csv_format);
>  
>
> Copy

The following ad hoc example loads data from all files in the S3 bucket. The
COPY command specifies file format options instead of referencing a named file
format. This example loads CSV files with a pipe (`|`) field delimiter. The
COPY command skips the first line in the data files:

    
    
    COPY INTO mytable
      FROM s3://mybucket credentials=(AWS_KEY_ID='$AWS_ACCESS_KEY_ID' AWS_SECRET_KEY='$AWS_SECRET_ACCESS_KEY')
      FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = '|' SKIP_HEADER = 1);
    

Copy

## Validating your data¶

Before loading your data, you can validate that the data in the uploaded files
will load correctly.

To validate data in an uploaded file, execute [COPY INTO <table>](../sql-
reference/sql/copy-into-table) in validation mode using the VALIDATION_MODE
parameter. The VALIDATION_MODE parameter returns errors that it encounters in
the file. You can then modify the data in the file to ensure it loads without
error.

In addition, [COPY INTO <table>](../sql-reference/sql/copy-into-table)
provides the ON_ERROR copy option to specify an action to perform if errors
are encountered in a file during loading.

## Monitoring data loads¶

Snowflake retains historical data for COPY INTO commands executed within the
previous 14 days. The metadata can be used to monitor and manage the loading
process, including deleting files after upload completes:

  * Monitor the status of each [COPY INTO <table>](../sql-reference/sql/copy-into-table) command on the History [![History tab](../_images/ui-navigation-history-icon.svg)](../_images/ui-navigation-history-icon.svg) page of the Classic Console.

  * Use the [LOAD_HISTORY](../sql-reference/info-schema/load_history) Information Schema view to retrieve the history of data loaded into tables using the COPY INTO command.

## Copying files from one stage to another¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Preview Feature](../release-
notes/preview-features) — Open

Available to all accounts.

Use the [COPY FILES](../sql-reference/sql/copy-files) command to organize data
into a single location by copying files from one named stage to another.

The following example copies all of the files from a source stage
(`src_stage`) to a target stage (`trg_stage`):

    
    
    COPY FILES
      INTO @trg_stage
      FROM @src_stage;
    

Copy

You can also specify a list of file names to copy, or copy files by using
pattern matching. For information, see the [COPY FILES examples](../sql-
reference/sql/copy-files.html#label-copy-files-examples).

