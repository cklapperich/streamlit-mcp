# Sharing unstructured data with a secure view¶

This topic briefly covers how to share unstructured data files by using a
secure view and [Secure Data Sharing](data-sharing-intro). With Secure Data
Sharing, data providers can share selected objects in a database from one
Snowflake account with data consumers in another Snowflake account.

For more information and additional examples, see [Create and configure
shares](data-sharing-provider).

## Step 1: Create a secure view¶

First, use the [CREATE SECURE VIEW](../sql-reference/sql/create-view) command
to create a secure view from unstructured data on a stage. A view allows the
result of a query to be accessed like a table, and a secure view is
specifically designated for data privacy. For more information, see [Overview
of Views](views-introduction).

You can allow data consumers to retrieve either scoped or pre-signed URLs from
the secure view. Scoped URLs provide better security, while pre-signed URLs
can be accessed without authorization or authentication. To choose the correct
URL for your use case, see [Types of URLs available to access
files](unstructured-intro.html#label-unstructured-data-urls).

Note

Snowflake does not create scoped or pre-signed URLs until a user in a consumer
account queries a secure view. This create-on-demand behavior helps you manage
the lifetime of pre-signed URLs. To minimize the risk of leaking pre-signed
URLs, you can also set a short time interval for the EXPIRATION_TIME parameter
of the [GET_PRESIGNED_URL](../sql-reference/functions/get_presigned_url)
function.

The following examples create secure views that allow data consumers to query
the scoped or pre-signed URLs for a specific set of staged files. Both views
query the RELATIVE_PATH column in a directory table to retrieve the scoped or
pre-signed URL.

### Scoped URL¶

This example calls the [BUILD_SCOPED_FILE_URL](../sql-
reference/functions/build_scoped_file_url) function to create a secure view
with the scoped URLs for a set of staged files. The example passes the
RELATIVE_PATH column in a directory table on a stage named `mystage` to the
BUILD_SCOPED_FILE_URL function:

    
    
    CREATE OR REPLACE SECURE VIEW images_scoped_v AS
    SELECT BUILD_SCOPED_FILE_URL(@mystage, relative_path) AS scoped_file_url
    FROM DIRECTORY(@mystage);
    

Copy

You can also create a secure view from a subset of files on a stage so that
you do not have to share the entire stage. The following example creates a
secure view of images on a stage where the `client_name` field is equal to
`abc`:

    
    
    CREATE OR REPLACE SECURE VIEW images_for_client_abc AS
    SELECT build_scoped_file_url(@myStage, relative_path) AS scoped_file_url
    FROM directory(@mystage) d join clients c on d.relative_path = c.relative_path
    WHERE c.client_name = 'abc';
    

Copy

### Pre-signed URL¶

This example calls the [GET_PRESIGNED_URL](../sql-
reference/functions/get_presigned_url) function to retrieve the pre-signed
URLs for a set of staged files. The example specifies 60 seconds for the
EXPIRATION_TIME parameter so that the pre-signed URLs will only be accessible
for one minute.

    
    
    CREATE OR REPLACE SECURE VIEW images_presigned_v AS
    SELECT GET_PRESIGNED_URL(@mystage, relative_path, 60) AS presigned_url
    FROM DIRECTORY(@mystage);
    

Copy

## Step 2: Create a share¶

Next, create an empty share, and then grant access privileges for your secure
view to the share. Doing so adds the secure view object to the share.

The following example creates a share with the [CREATE SHARE](../sql-
reference/sql/create-share) command and then uses the [GRANT <privilege> … TO
SHARE](../sql-reference/sql/grant-privilege-share) command to grant the SELECT
privilege for a secure view to the share.

    
    
    CREATE SHARE my_share;
    GRANT SELECT ON my_secure_view TO SHARE my_share;
    

Copy

## Step 3: Add accounts to the share¶

Finally, you must provide access for consumer accounts to your share by adding
the accounts to your share.

The following example uses the [ALTER SHARE](../sql-reference/sql/alter-share)
command to add an account named `consumer_account_1` to the share named
`my_share`.

    
    
    ALTER SHARE my_share ADD ACCOUNTS=consumer_account_1;
    

Copy

After you complete this step, the `consumer_account_1` account can see the
share and access the files in the secure view.

