# Introduction to unstructured data¶

Unstructured data is information that does not fit into a predefined data
model or schema. Typically text-heavy, such as form responses and social media
conversations, unstructured data also encompasses images, video, and audio.
Industry-specific file types such as VCF (genomics), KDF (semiconductors), or
HDF5 (aeronautics) are included in this category.

Snowflake supports the following actions:

  * Securely access data files located in cloud storage.

  * Share file access URLs with collaborators and partners.

  * Load file access URLs and other file metadata into Snowflake tables.

  * Process unstructured data.

  * [Load unstructured data with Document AI](data-load-unstructured-data) (Preview)

This topic introduces key concepts and provides instructions for accessing,
sharing, and processing unstructured data files.

## Cloud Storage service support¶

Both external (external cloud storage) and internal (i.e. Snowflake) stages
support unstructured data.

External stages:

    

Store files in external cloud storage: Amazon S3, Google Cloud Storage, or one
of the supported Microsoft Azure cloud storage services:

  * Blob storage

  * Data Lake Storage Gen2

  * General-purpose v1

  * General-purpose v2

## Types of URLs available to access files¶

The following types of URLs are available to access files in cloud storage:

Scoped URL:

    

Encoded URL that permits temporary access to a staged file without granting
privileges to the stage.

The URL expires when the [persisted query result period](querying-persisted-
results) ends (i.e. the results cache expires), which is currently 24 hours.

File URL:

    

URL that identifies the database, schema, stage, and file path to a set of
files. A role that has sufficient privileges on the stage can access the
files.

Pre-signed URL:

    

Simple HTTPS URL used to access a file via a web browser. A file is
temporarily accessible to users via this URL using a pre-signed access token.
The expiration time for the access token is configurable.

The following table describes key characteristics of these URL types:

| Scoped URL | File URL | Pre-signed URL  
---|---|---|---  
Use cases | Recommended for file administrators to give scoped access to data files to specific roles in the same account. Provide access to the files with a view that retrieves scoped URLs. Only roles that have privileges on the view can access the files. Snowflake records information in the query history about who uses a scoped URL to access a file, and when. Ideal for use in custom applications, for providing unstructured data to other accounts through a share, or for downloading and analysis of unstructured data in Snowsight. | Permanent URL to a file on a stage. To download or access a file, users send the file URL in a GET request to the REST API endpoint along with the authorization token. Ideal for custom applications that require access to unstructured data files. | Used to download or access files without authenticating into Snowflake or passing an authorization token. Pre-signed URLs are open; any user or application can directly access or download the files. Ideal for business intelligence applications or reporting tools that need to display the unstructured file contents.  
How to generate | Query the [BUILD_SCOPED_FILE_URL](../sql-reference/functions/build_scoped_file_url) function. | Either Query the directory table for the stage that references the staged files or call the [BUILD_STAGE_FILE_URL](../sql-reference/functions/build_stage_file_url) function. | Query the [GET_PRESIGNED_URL](../sql-reference/functions/get_presigned_url) function.  
Usage | The following options are available:

  * In Snowsight, click on a scoped URL in the query results table. Snowsight retrieves the file only for the user who generated the scoped URL.
  * Send a scoped URL in a GET request to the file support REST API endpoint. For information, see [REST API for unstructured data support](data-load-unstructured-rest-api).

| The following options are available:

  * In Snowsight, click on a file URL in the query results table. Snowsight retrieves the file only if the active role has sufficient privileges.
  * Send a file URL in a GET request to the file support REST API endpoint. For information, see [REST API for unstructured data support](data-load-unstructured-rest-api).

| The following options are available:

  * In Snowsight, click on a pre-signed URL in the query results table.
  * Navigate to the pre-signed URL directly in a web browser.

  
[Snowflake Secure Data Sharing](../guides-overview-sharing) | Unstructured data files can be accessed by data consumers via column values of this type in secure views shared by data providers. | Unstructured data files cannot be accessed by data consumers via column values of this type in secure views shared by data providers. | Unstructured data files can be accessed by data consumers via column values of this type in secure views shared by data providers.  
Authorization | Only the user who generates a scoped URL can use the URL to access the referenced file. | Role specified in the GET REST API call must have sufficient privileges on the stage: USAGE (external stage) or READ (internal stage). | Any person who has the pre-signed URL can access the referenced file for the life of the token.  
Expiration | Expiration period for the query results cache (currently 24 hours). | Permanent. | Length of time specified in the `expiration_time` argument.  
  
## Server-side encryption for unstructured data access¶

To enable unstructured data access on an internal stage, you can consider
using server-side encryption when you create the stage. Otherwise, staged
files will be client-side encrypted by default. The encryption keys are owned
by Snowflake, and client-side encrypted files are unreadable by users and
external tools using pre-signed, file, or scoped URLs.

To configure server-side encryption for an internal stage, specify the
`SNOWFLAKE_SSE` encryption type in the [CREATE STAGE](../sql-
reference/sql/create-stage) command. See [Internal stage parameters
(internalStageParams)](../sql-reference/sql/create-stage.html#label-create-
stage-internalstageparams) for more information.

The following example creates an internal stage named `my_int_stage` with
server-side encryption and a directory table.

    
    
    CREATE STAGE my_int_stage
      ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
      DIRECTORY = ( ENABLE = true );
    

Copy

Important

If you require Tri-Secret Secure for security compliance, use the
`SNOWFLAKE_FULL` encryption type for internal stages. `SNOWFLAKE_SSE` does not
support Tri-Secret Secure.

Note

  * You cannot change the encryption type for an internal stage after you create the stage.

  * Currently, creating internal stages with server-side encryption is limited to the following Snowflake client versions: JDBC Driver v3.12.11 (or higher)

## Directory tables¶

Directory tables store a catalog of staged files in cloud storage. Roles with
sufficient privileges can query a directory table to retrieve file URLs to
access the staged files.

For details, see [Directory tables](data-load-dirtables).

## SQL functions¶

The following [File functions](../sql-reference/functions-file) are provided
to access data files:

SQL Function | Description  
---|---  
[GET_STAGE_LOCATION](../sql-reference/functions/get_stage_location) | Returns the URL for an external or internal named stage using the stage name as the input.  
[GET_RELATIVE_PATH](../sql-reference/functions/get_relative_path) | Extracts the path of a staged file relative to its location in the stage using the stage name and absolute file path in cloud storage as inputs.  
[GET_ABSOLUTE_PATH](../sql-reference/functions/get_absolute_path) | Returns the absolute path of a staged file using the stage name and path of the file relative to its location in the stage as inputs.  
[GET_PRESIGNED_URL](../sql-reference/functions/get_presigned_url) | Generates the pre-signed URL to a staged file using the stage name and relative file path as inputs. Access files in an external stage using the function.  
[BUILD_SCOPED_FILE_URL](../sql-reference/functions/build_scoped_file_url) | Generates a scoped Snowflake file URL to a staged file using the stage name and relative file path as inputs.  
[BUILD_STAGE_FILE_URL](../sql-reference/functions/build_stage_file_url) | Generates a Snowflake file URL to a staged file using the stage name and relative file path as inputs.  
  
## Downloading staged files in Snowsight¶

### Downloading a generated scoped, pre-signed, or file URL¶

Users can select a generated scoped, pre-signed, or file URL in the results
table of a [Snowsight](ui-snowsight) worksheet and download the referenced
file.

  1. Sign in to [Snowsight](ui-snowsight).

  2. Select Projects » Worksheets » My Worksheets, or open a local worksheet by navigating to Recent or Folders » _< worksheet_name>_.

  3. Return a scoped, pre-signed, or file URL in a query using any one of the supported methods.

  4. Select the URL in the results table. Snowsight downloads the file referenced by the URL.

[![Download pre-signed URL in Snowsight results
table](../_images/unstructured-snowsight-
download.png)](../_images/unstructured-snowsight-download.png)

### Downloading from an internal stage¶

Users can download a file from the internal stage directly from Snowsight.

  1. Sign in to [Snowsight](ui-snowsight).

  2. Navigate to your file on the internal stage. For more information about finding files, see [Viewing staged files](data-load-local-file-system-stage-ui.html#label-snowsight-stage-details).

  3. Select the [![More options](../_images/snowsight-worksheet-explorer-ellipsis.png)](../_images/snowsight-worksheet-explorer-ellipsis.png) button, and select Download.

[![Download file directly from the internal stage in
Snowsight](../_images/unstructured-snowsight-download-internal-
stage.png)](../_images/unstructured-snowsight-download-internal-stage.png)

## Processing unstructured data¶

Snowflake supports the following features to help you process unstructured
data.

External Functions

    

External functions are user-defined functions that you store and execute
outside of Snowflake. With external functions, you can use libraries such as
Amazon Textract, Document AI, or Azure Computer Vision that cannot be accessed
from internal user-defined functions (UDFs).

For more information, see [Writing external functions](../sql-
reference/external-functions).

User-defined Functions and Stored Procedures

    

Snowflake supports multiple ways to read a file within Java or Python code so
that you can process unstructured data or use your own machine learning models
in user-defined functions (UDFs), user-defined table functions (UDTFs), or
stored procedures.

You can [extend the SQL that you use in Snowflake](../developer-
guide/extensibility), or build an application using the [Snowpark
API](../developer-guide/snowpark/index).

See the following topics for more information and examples.

>   * [Processing unstructured data with UDF and procedure
> handlers](unstructured-data-java)
>
>   * [Reading a File with a Python UDF Handler](../developer-
> guide/udf/python/udf-python-examples.html#label-udf-python-read-files)
>
>   * [Reading files with a Python Stored Procedure Handler](../developer-
> guide/stored-procedure/python/procedure-python-read-files)
>
>   * [Reading Files with the Snowpark API for Java](../developer-
> guide/snowpark/java/creating-udfs.html#label-snowpark-java-udf-read-files)
>
>   * [Reading Files with the Snowpark API for Python](../developer-
> guide/snowpark/python/creating-udfs.html#label-snowpark-python-udf-read-
> files)
>
>

