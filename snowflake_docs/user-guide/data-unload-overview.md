# Overview of data unloading¶

Similar to data loading, Snowflake supports bulk export (i.e. unload) of data
from a database table into flat, delimited text files.

## Bulk unloading process¶

The process for unloading data into files is the same as the loading process,
except in reverse:

Step 1:

    

Use the [COPY INTO <location>](../sql-reference/sql/copy-into-location)
command to copy the data from the Snowflake database table into one or more
files in a Snowflake or external stage.

Step 2:

    

Download the file from the stage:

  * From a Snowflake stage, use the [GET](../sql-reference/sql/get) command to download the data file(s).

  * From S3, use the interfaces/tools provided by Amazon S3 to get the data file(s).

  * From Azure, use the interfaces/tools provided by Microsoft Azure to get the data file(s).

## Bulk unloading using queries¶

Snowflake supports specifying a SELECT statement instead of a table in the
[COPY INTO <location>](../sql-reference/sql/copy-into-location) command. The
results of the query are written to one or more files as specified in the
command and the file(s) are stored in the specified location (internal or
external).

SELECT queries in COPY statements support the full syntax and semantics of
Snowflake SQL queries, including JOIN clauses, which enables downloading data
from multiple tables.

## Bulk unloading into single or multiple files¶

The COPY INTO _< location>_ command provides a copy option (SINGLE) for
unloading data into a single file or multiple files. The default is SINGLE =
FALSE (i.e. unload into multiple files).

Snowflake assigns each file a unique name. The location path specified for the
command can contain a filename prefix that is assigned to all the data files
generated. If a prefix is not specified, Snowflake prefixes the generated
filenames with `data_`.

Snowflake appends a suffix that ensures each file name is unique across
parallel execution threads; e.g. `data_stats_0_1_0`.

When unloading data into multiple files, use the MAX_FILE_SIZE copy option to
specify the maximum size of each file created.

## Partitioned data unloading¶

The COPY INTO _< location>_ command includes a PARTITION BY copy option for
partitioned unloading of data to stages.

The ability to partition data during the unload operation enables a variety of
use cases, such as using Snowflake to transform data for output to a data
lake. In addition, partitioning unloaded data into a directory structure in
cloud storage can increase the efficiency with which third-party tools consume
the data.

The PARTITION BY copy option accepts an expression by which the unload
operation partitions table rows into separate files unloaded to the specified
stage.

## Tasks for unloading data using the COPY command¶

For more information about the tasks associated with unloading data, see:

  * [Unloading into a Snowflake stage](data-unload-snowflake)

  * [Unloading into Amazon S3](data-unload-s3)

  * [Unloading into Google Cloud Storage](data-unload-gcs)

  * [Unloading into Microsoft Azure](data-unload-azure)

