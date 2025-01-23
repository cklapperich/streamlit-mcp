# Troubleshooting bulk data loads¶

This topic describes a methodical approach to troubleshooting issues with bulk
data loads.

## Data load failures¶

### Step 1: Viewing the COPY history for the table¶

Query the load activity history for a table. For information, see
[COPY_HISTORY](../sql-reference/functions/copy_history). The `STATUS` column
indicates whether a particular set of files was loaded, partially loaded, or
failed to load. The `FIRST_ERROR_MESSAGE` column provides a reason when an
attempt partially loaded or failed.

Note that if a set of files has multiple issues, the `FIRST_ERROR_MESSAGE`
column only indicates the first error encountered. To view all errors in the
files, see Step 2: Validating the Data Load for instructions.

### Step 2: Validating the data load¶

The VALIDATION_MODE copy option instructs a COPY statement to validate the
data to be loaded and return results based on the validation option specified.
No data is loaded when this copy option is specified. For more information
about the copy option, see [COPY INTO <table>](../sql-reference/sql/copy-into-
table).

Execute a COPY statement with the VALIDATION_MODE copy option set to
`RETURN_ALL_ERRORS`. In the statement, reference the set of files you had
attempted to load.

The following example validates a set of files that contain errors. To
facilitate analysis of the errors, a [COPY INTO <location>](../sql-
reference/sql/copy-into-location) statement then unloads the problematic
records into a text file so they could be analyzed and fixed in the original
data files. The statement queries the [RESULT_SCAN](../sql-
reference/functions/result_scan) table function to retrieve the records. Note
that the statements in this section must be run in succession in order to
retrieve the applicable records using the [LAST_QUERY_ID](../sql-
reference/functions/last_query_id) function.

    
    
    COPY INTO mytable
      FROM @mystage/myfile.csv.gz
      VALIDATION_MODE=RETURN_ALL_ERRORS;
    
    SET qid=last_query_id();
    
    COPY INTO @mystage/errors/load_errors.txt FROM (SELECT rejected_record FROM TABLE(result_scan($qid)));
    

Copy

## Other issues¶

### Error: Integration `{0}` associated with the stage `{1}` cannot be found¶

    
    
    003139=SQL compilation error:\nIntegration ''{0}'' associated with the stage ''{1}'' cannot be found.
    

Copy

This error can occur when the association between the external stage and the
storage integration linked to the stage has been broken. This happens when the
storage integration object has been recreated (using [CREATE OR REPLACE
STORAGE INTEGRATION](../sql-reference/sql/create-storage-integration)). A
stage links to a storage integration using a hidden ID rather than the name of
the storage integration. Behind the scenes, the CREATE OR REPLACE syntax drops
the object and recreates it with a different hidden ID.

If you must recreate a storage integration after it has been linked to one or
more stages, you must reestablish the association between each stage and the
storage integration by executing [ALTER STAGE](../sql-reference/sql/alter-
stage) `_stage_name_` SET STORAGE_INTEGRATION = `_storage_integration_name_`,
where:

  * `_stage_name_` is the name of the stage.

  * `_storage_integration_name_` is the name of the storage integration.

### Load times inserted using CURRENT_TIMESTAMP earlier than LOAD_TIME values
in COPY_HISTORY view¶

Table designers may add a timestamp column that inserts the current timestamp
as the default value as records are loaded into a table. The intent is to
capture the time when each record was loaded into the table; however, the
timestamps are earlier than the LOAD_TIME column values returned by the
[COPY_HISTORY function](../sql-reference/functions/copy_history) (Information
Schema) or the [COPY_HISTORY view](../sql-reference/account-
usage/copy_history) (Account Usage). The reason is,
[CURRENT_TIMESTAMP](../sql-reference/functions/current_timestamp) is evaluated
when the load operation is compiled in cloud services rather than when the
record is inserted into the table (i.e. when the transaction for the load
operation is committed).

It is recommended to include and query [METADATA$START_SCAN_TIME](querying-
metadata) instead, which provides a more accurate representation of record
loading.

