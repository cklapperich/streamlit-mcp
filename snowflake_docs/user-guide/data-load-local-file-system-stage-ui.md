# Staging files using Snowsight¶

With Snowsight, you can create and manage named stages without writing SQL.
You can also upload files onto a named internal stage so that you can view
your files, reference the files in a Python worksheet, or [load data from the
files into a table](data-load-web-ui.html#label-data-load-from-stage-to-
table).

You can’t upload files onto user stages or table stages using Snowsight. For
more information about stages, see [Overview of data loading](data-load-
overview).

## Creating a stage¶

You can use Snowsight to create a named internal or external stage.

Note

To create an internal stage, you must use a role that is granted or inherits
the necessary privileges. For details, see [Access control
requirements](../sql-reference/sql/create-stage.html#label-create-stage-
privileges) for [CREATE STAGE](../sql-reference/sql/create-stage).

### Create a named internal stage¶

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

### Create a named external stage¶

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

## Uploading files onto a stage¶

You can use Snowsight to upload files onto a named internal stage.

To upload files onto an external stage, use the tools provided by your
external cloud service (Amazon S3, Microsoft Azure, or Google Cloud Storage).

### Upload files onto a named internal stage¶

Note

The maximum file size is 250 MB.

To upload files onto an internal stage, you must use a role that is granted or
inherits the USAGE privilege on the database and schema and the WRITE
privilege on the stage. For more information, see [Stage privileges](security-
access-control-privileges.html#label-access-control-privileges-stage).

To upload files onto your stage, do the following:

  1. Sign in to Snowsight.

  2. Select Data » Add Data.

  3. On the Add Data page, select Load files into a Stage.

  4. In the Upload Your Files dialog that appears, select the files that you want to upload. You can upload multiple files at the same time.

  5. Select the database schema in which you created the stage, then select the stage.

  6. Optionally, select or create a path where you want to save your files within the stage.

  7. Select Upload.

After you upload files onto the stage, you can take one of the following
actions depending on the file:

  * Use the files in a Python worksheet. For more information, see [Add a Python File from a Stage to a Worksheet](../developer-guide/snowpark/python/python-worksheets.html#label-snowsight-py-worksheets-add-py-file).

  * Copy data from the staged files into a table. For more information, see [Load data into an existing table using Snowsight](data-load-web-ui.html#label-data-load-from-stage-to-table) or [Copying data from an internal stage](data-load-local-file-system-copy).

  * Query the data in the stage. For more information, see [Querying Data in Staged Files](querying-stage).

## Viewing staged files¶

You can view staged files using Snowsight. You can view files on both internal
and external stages.

Note

You must use a role that is granted or inherits the USAGE privilege on the
database and schema and the READ privilege on the stage to perform these
steps.

  1. Sign in to Snowsight.

  2. Select Data » Databases.

  3. Select the database and schema that contain the stage.

  4. Select Stages and select the stage for which you want to view files.

  5. If prompted, select Enable Directory Table to enable a directory table for the stage so that you can see files.

  6. If prompted, select a warehouse to refresh the directory table.

To refresh the directory table on a stage, select the refresh icon.

## Managing staged files¶

You can use Snowsight to take the following actions on staged files:

  * Select [![More options](../_images/snowsight-worksheets-gs-options.png)](../_images/snowsight-worksheets-gs-options.png) » Load into table to [load the file from the stage into a table](data-load-web-ui.html#label-data-load-from-stage-to-table-snowsight).

  * Select [![More options](../_images/snowsight-worksheets-gs-options.png)](../_images/snowsight-worksheets-gs-options.png) » Copy path to copy the path to the file for use elsewhere, such as in a worksheet.

For files on an internal stage, you can also take the following actions:

  * Select [![More options](../_images/snowsight-worksheets-gs-options.png)](../_images/snowsight-worksheets-gs-options.png) » Download to download the file from the stage.

  * Select [![More options](../_images/snowsight-worksheets-gs-options.png)](../_images/snowsight-worksheets-gs-options.png) » Remove to remove the file from the stage.

Note

To download a file from an external stage, see [Downloading staged files in
Snowsight](unstructured-intro.html#label-data-unstructured-download-staged-
file).

## Managing stages¶

To manage a stage in Snowsight, do the following:

Note

You must use a role that is granted or inherits the USAGE privilege on the
database and schema and the OWNERSHIP privilege on the stage to perform these
steps.

  1. Sign in to Snowsight.

  2. Select Data » Databases.

  3. Select the database and schema that contain the stage.

  4. Select Stages and select the stage.

  5. Select Stage Details.

You can manage the stage in the following ways:

  * Select [![More options](../_images/snowsight-worksheets-gs-options.png)](../_images/snowsight-worksheets-gs-options.png) » Edit to edit properties or enable a directory table for the stage object.

  * Select [![More options](../_images/snowsight-worksheets-gs-options.png)](../_images/snowsight-worksheets-gs-options.png) » Clone to clone the stage.

  * Select [![More options](../_images/snowsight-worksheets-gs-options.png)](../_images/snowsight-worksheets-gs-options.png) » Drop to drop, or remove, the stage.

  * Select [![More options](../_images/snowsight-worksheets-gs-options.png)](../_images/snowsight-worksheets-gs-options.png) » Transfer Ownership to transfer OWNERSHIP privileges of the stage to another role.

If you want to manage privileges for the stage, use the Privileges section to
view, grant, and revoke privileges.

## Troubleshooting¶

### Files are not visible on an external stage¶

This issue can occur when an external stage does not have a directory table
enabled, or when information about the external storage location is incorrect.

To fix this issue, try the following:

  * Make sure the stage owner has enabled a [directory table](data-load-dirtables) on the stage.

  * Check that the directory table has been refreshed. To refresh the directory table, select your stage in Snowsight, then select the refresh icon.

  * Verify that the cloud provider URL is correct. If your URL contains a subpath, ensure that there is a trailing slash.

### Upload files button is unavailable (inactive)¶

This issue can occur when you don’t have the required privileges to upload
files onto an internal stage, or if another upload is in progress.

To fix this issue, try the following:

  * Make sure that you have selected an internal stage.

  * Use a role that is granted or inherits the USAGE privilege on the database and schema and the WRITE privilege on the stage.

  * Check whether another upload is in progress. Hovering over the inactive button displays information about any in-progress uploads. Snowsight also displays a notification for in-progress uploads. If another upload is in progress, it must complete before you can upload additional files onto the stage.

