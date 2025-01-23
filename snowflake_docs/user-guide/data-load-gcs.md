# Bulk loading from Google Cloud Storage¶

If you already have a Google Cloud Storage account and use Cloud Storage
buckets for storing and managing your data files, you can make use of your
existing buckets and folder paths for bulk loading into Snowflake.

Note

Snowflake supports Regional Storage and Multi-Regional Storage accounts only.

This set of topics describes how to use the [COPY INTO <table>](../sql-
reference/sql/copy-into-table) command to load data from a Cloud Storage
bucket into tables.

As illustrated in the diagram below, loading data from a Cloud Storage bucket
is performed in two steps:

Step 1:

    

Snowflake assumes the data files have already been staged in a Cloud Storage
bucket. If they haven’t been staged yet, use the upload interfaces/utilities
provided by Google to stage the files.

Step 2:

    

Use the [COPY INTO <table>](../sql-reference/sql/copy-into-table) command to
load the contents of the staged file(s) into a Snowflake database table. You
can load directly from the bucket, but Snowflake recommends creating an
external stage that references the bucket and using the external stage
instead.

Regardless of the method you use, this step requires a running, current
virtual warehouse for the session if you execute the command manually or
within a script. The warehouse provides the compute resources to perform the
actual insertion of rows into the table.

![Data loading overview](../_images/data-load-gcs.png)

Note

As long as your Snowflake account is hosted on Google Cloud, your network
traffic does not traverse the public internet.

Tip

The instructions in this set of topics assume you have read [Preparing to load
data](data-load-prepare) and have created a named file format, if desired.

Before you begin, you may also want to read [Data loading
considerations](data-load-considerations) for best practices, tips, and other
guidance.

**Next Topics:**

  * **Configuration tasks (complete as needed):**

    * [Configuring an integration for Google Cloud Storage](data-load-gcs-config)
    * [Google Cloud Storage data file encryption](data-load-gcs-encrypt)

  * **Data loading tasks (complete for each set of files you load):**

    * [Copying data from a Google Cloud Storage stage](data-load-gcs-copy)

  * **Troubleshooting:**

    * [Troubleshooting loads from Google Cloud Storage](data-load-gcs-ts)

