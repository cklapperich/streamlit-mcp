# Copying data from an internal stage¶

Load data from your staged files into the target table.

## Loading your data¶

Execute [COPY INTO <table>](../sql-reference/sql/copy-into-table) to load your
staged data into the target table.

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

### User stage¶

The following example loads data from all files prefixed with `staged` in your
user stage using the named `my_csv_format` file format created in [Preparing
to load data](data-load-prepare):

    
    
    COPY INTO mytable from @~/staged FILE_FORMAT = (FORMAT_NAME = 'my_csv_format');
    

Copy

### Table stage¶

The following ad hoc example loads data from all files in the stage for the
`mytable` table. The COPY command specifies file format options instead of
referencing a named file format. This example loads CSV files with a pipe
(`|`) field delimiter. The COPY command skips the first line in the data
files:

    
    
    COPY INTO mytable FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = '|' SKIP_HEADER = 1);
    

Copy

Note that when copying data from files in a table stage, the FROM clause can
be omitted because Snowflake automatically checks for files in the table
stage.

### Named stage¶

The following example loads data from all files from the `my_stage` named
stage, which was created in [Choosing an internal stage for local files](data-
load-local-file-system-create-stage):

    
    
    COPY INTO mytable from @my_stage;
    

Copy

Note that a file format does not need to be specified because it is included
in the stage definition.

## Validating your data¶

Before loading your data, you can validate that the data in the uploaded files
will load correctly.

To validate data in an uploaded file, execute [COPY INTO <table>](../sql-
reference/sql/copy-into-table) in validation mode using the VALIDATION_MODE
parameter. The VALIDATION_MODE parameter returns any errors that it encounters
in a file. You can then modify the data in the file to ensure it loads without
error.

In addition, the ON_ERROR copy option for the [COPY INTO <table>](../sql-
reference/sql/copy-into-table) command indicates what action to perform if
errors are encountered in a file during loading.

## Monitoring files staged internally¶

Snowflake maintains detailed metadata for each file uploaded into internal
stage (for users, tables, and stages), including:

  * File name

  * File size (compressed, if compression was specified during upload)

  * LAST_MODIFIED date, i.e. the timestamp when the data file was initially staged or when it was last modified, whichever is later

In addition, Snowflake retains historical data for COPY INTO commands executed
within the previous 14 days. The metadata can be used to monitor and manage
the loading process, including deleting files after upload completes:

  * Use the [LIST](../sql-reference/sql/list) command to view the status of data files that have been staged.

  * Monitor the status of each [COPY INTO <table>](../sql-reference/sql/copy-into-table) command on the History [![History tab](../_images/ui-navigation-history-icon.svg)](../_images/ui-navigation-history-icon.svg) page of the Classic Console.

  * Use the [VALIDATE](../sql-reference/functions/validate) function to validate the data files you’ve loaded and retrieve any errors encountered during the load.

  * Use the [LOAD_HISTORY](../sql-reference/info-schema/load_history) Information Schema view to retrieve the history of data loaded into tables using the COPY INTO command.

## Managing data files¶

Staged files can be deleted from a Snowflake stage (user stage, table stage,
or named stage) using the following methods:

  * Files that were loaded successfully can be deleted from the stage during a load by specifying the PURGE copy option in the [COPY INTO <table>](../sql-reference/sql/copy-into-table) command.

  * After the load completes, use the [REMOVE](../sql-reference/sql/remove) command to remove the files in the stage.

Removing files ensures they aren’t inadvertently loaded again. It also
improves load performance, because it reduces the number of files that COPY
commands must scan to verify whether existing files in a stage were loaded
already.

### Copying files from one stage to another¶

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

