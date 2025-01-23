# Common setup for Snowflake REST APIs tutorials¶

Feature — Generally Available

Not available in government regions.

## Introduction¶

This topic provides instructions for the common setup required for all
Snowflake REST APIs tutorials available in this documentation.

### Overview of the Snowflake REST APIs¶

Before starting your setup, take a look at the Snowflake REST APIs.

The Snowflake REST APIs supports the following resources through the
corresponding APIs. The APIs support CREATE OR ALTER operations for applicable
resources.

  * Working with accounts

    * [Accounts](../account/account-introduction)

    * [Managed accounts](../managed-account/managed-account-introduction)

  * Working with users, roles, and privileges

    * [Users](../users/users-introduction)

    * [Roles](../roles/roles-introduction)

    * [Database roles](../database-role/database-role-introduction)

    * [Grants](../grants/grants-introduction)

  * Managing virtual warehouses

    * [Warehouses](../warehouses/warehouses-introduction)

  * Working with databases and schemas

    * [Databases](../databases/db-introduction)

    * [Schemas](../schemas/schemas-introduction)

  * Managing tables and views

    * [Tables](../tables/tables-introduction)

    * [Dynamic tables](../dynamic-tables/dynamic-tables-introduction)

    * [Event tables](../event-table/event-table-introduction)

    * [Views](../view/view-introduction)

  * Loading and unloading data

    * [Stages](../stages/stages-introduction)

    * [External volumes](../external-volume/external-volume-introduction)

    * [Pipes](../pipe/pipe-introduction)

  * Managing notebooks

    * [Notebooks](../notebook/notebook-introduction)

  * Working with Snowpark Container Services

    * [Compute Pools](../compute-pools/cp-introduction)

    * [Image Repositories](../image-repositories/images-introduction)

    * [Services](../services/services-introduction)

  * Using functions and procedures

    * [Functions](../functions/functions-introduction)

    * [User-defined functions](../user-defined-function/user-defined-function-introduction)

    * [Procedures](../procedure/procedure-introduction)

  * Managing security

    * [Network policies](../network-policy/network-policy-introduction)

  * Managing alerts

    * [Alerts](../alert/alert-introduction)

  * Leveraging AI/ML

    * [Cortex Inference](../cortex-inference/cortex-inference-introduction)

    * [Cortex Search Service](../cortex-search/cortex-search-introduction)

  * Managing streams and tasks

    * [Streams](../stream/stream-introduction)

    * [Tasks](../tasks/tasks-introduction)

  * Managing integrations

    * [Catalog Integration](../catalog-integration/catalog-integration-introduction)

    * [Notification](../notification-integration/notification-integration-introduction)

For reference information about the APIs and their endpoints, see [Snowflake
REST APIs reference](../reference).

Tip

If you prefer writing Python applications, you can use the Snowflake Python
APIs to manage Snowflake objects. For more information, see [Snowflake Python
APIs: Managing Snowflake objects with Python](../../snowflake-python-
api/snowflake-python-overview).

## Import the Snowflake REST APIs collections¶

This tutorial walks you through the process of importing the Snowflake REST
APIs collections from Postman.

  1. Download the API collections from the [Git repository](https://github.com/snowflakedb/snowflake-rest-api-specs/tree/main/releases/8.40/collections) into a folder.

![../../../_images/api-collections-git.png](../../../_images/api-collections-
git.png)

  2. Open the Postman application, and create an account, if necessary.

  3. In Postman, open the desired workspace.

![../../../_images/postman-workspace.png](../../../_images/postman-
workspace.png)

  4. Select Import.

![../../../_images/postman-import-workspace.png](../../../_images/postman-
import-workspace.png)

  5. Select folders.

![../../../_images/postman-download-collections.png](../../../_images/postman-
download-collections.png)

  6. In the dialog, select the folder where you extracted the collection, and select Open.

![../../../_images/postman-import-elements.png](../../../_images/postman-
import-elements.png)

  7. Verify that all of the items are selected, and select Import.

You should see the collections listed in the left panel, as shown:

![../../../_images/postman-verify-import.png](../../../_images/postman-verify-
import.png)

## Specify the bearer token in Postman¶

REST requests require a JWT token in the request header to authenticate the
request. If you don’t have a JWT token, see [Generate a JWT
token](../authentication.html#label-sfrest-api-jwt-token).

In Postman, you can copy the JWT token into the `bearerToken` header property,
as shown.

![../../../_images/postman-bearer-token.png](../../../_images/postman-bearer-
token.png)

You can then set the `x-snowflake-authorization-token-type` key to
`KEYPAIR_JWT` in each request header, as shown:

![../../../_images/postman-set-header.png](../../../_images/postman-set-
header.png)

Note

As mentioned in the tutorial [prerequisites](../tutorials-overview), you must
define an AUTHENTICATION POLICY. If you receive an error message similar to `{
"code": "390202", "message": "Authentication attempt rejected by the current
authentication policy." }`, you can run the following SQL command to define a
policy:

    
    
    SHOW AUTHENTICATION POLICIES; alter AUTHENTICATION POLICY <your authentication policy> set AUTHENTICATION_METHODS = ('KEYPAIR', 'PASSWORD', 'OAUTH');
    

Copy

## Set environment variables in the Postman environment¶

You can set environment variables in your Postman environment. You can then
use these variables in Postman, in the form `{{variable_name}}`.

All endpoint URLs begin with a `baseURL`, which identifies your Snowflake
account. The baseURL has the form: `<account_locator>.snowflakecomputing.com`,
where `<account_locator>` is your Snowflake account name.

To set the `baseURL` variable, as well as any other variables, in Postman,
enable each parameter and set its value, as shown:

![../../../_images/postman-env-vars.png](../../../_images/postman-env-
vars.png)

For each value you set, you must select Save to save the new value.

## What’s next?¶

Congratulations! In this tutorial, you learned the fundamentals for managing
Snowflake database, schema, and table resources using the Snowflake REST APIs.

### Summary¶

Along the way, you completed the following steps:

  * Import Snowflake REST APIs collections.

  * Specify a bearer token in Postman.

  * Set environment variables in the Postman environment.

### Next tutorial¶

You can now proceed to [Tutorial 1: Create and manage databases, schemas, and
tables](tutorial-1), which shows you how to create and manage Snowflake
databases, schemas, and tables.

