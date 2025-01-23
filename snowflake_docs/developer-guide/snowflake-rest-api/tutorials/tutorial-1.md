# Tutorial 1: Create and manage databases, schemas, and tables¶

Feature — Generally Available

Not available in government regions.

## Introduction¶

In this tutorial, you learn how to submit REST queries to create and manage
databases, tables, and schemas.

### Prerequisites¶

Note

If you have already completed the steps in [Common setup for Snowflake REST
APIs tutorials](common-setup), you can skip these prerequisites and proceed to
the first step of this tutorial.

Before you start this tutorial, you must complete the [common setup](common-
setup) instructions, which includes the following steps:

>   * Import the Snowflake REST APIs Postman collections.
>
>   * Authenticate your connection by setting the bearer token in Postman.
>
>

After completing these prerequisites, you are ready to start using the API.

## Create a database and list available databases¶

You can use Postman to create a database and list available databases.

  * To create a database, send a `POST` request with the following request body to the `/api/v2/databases` endpoint, as shown.
    
        {
      "name": "demo_db",
      "kind": "PERMANENT",
      "comment": "snowflake rest api demo-db",
      "data_retention_time_in_days": "1",
      "max_data_extension_time_in_days": "1"
    }
    

Copy

![../../../_images/create-database.png](../../../_images/create-database.png)

  * To list available databases, send a `GET` request to the `/api/v2/databases` endpoint, as shown in the following examples:

    * To find databases whose name contains the string, `demo`, specify `%25demo%25` in the like query parameter.

![../../../_images/list-databases.png](../../../_images/list-databases.png)

    * To return the first database whose name starts with the string, `DEMO_DB`, specify `DEMO_DB` and `1` in the startsWith and showLimit query parameters, respectively.

![../../../_images/list-databases2.png](../../../_images/list-databases2.png)

For more information, see the [Snowflake Database API reference](/developer-
guide/snowflake-rest-api/reference/database.html).

## Create a schema and list available schemas¶

You can use Postman to create a schema and list available schemas.

  * To create a schema, send a `POST` request to the `/api/v2/databases/{database}/schemas` endpoint, as follows:

>     1. Add the database name (`demo_db`) to the database path variable in
> the request header.
>
> ![../../../_images/create-schema1.png](../../../_images/create-schema1.png)
>     2. Add the schema name (`demo_sc`) to the request body.
>  
>         >         {
>           "name": "demo_sc",
>         }
>  
>
> Copy
>
> ![../../../_images/create-schema2.png](../../../_images/create-schema2.png)

  * To list available schemas, send a `GET` request to the `/api/v2/databases/{database}/schemas` endpoint. In this example, you return the first schema whose name starts with the string, `DEMO_SC`, by specifying `DEMO_SC` and `1` in the startsWith and showLimit query parameters, respectively.

> ![../../../_images/list-schemas1.png](../../../_images/list-schemas1.png)

For more information, see the [Snowflake Schema API reference](/developer-
guide/snowflake-rest-api/reference/schema.html).

## Create a table and fetch the table details¶

You can use Postman to create a table and list available tables.

  * To create a table, send a `POST` request to the `/api/v2/databases/{database}/schemas/{schema}/tables` endpoint, as follows:

>     1. Add the database name (`demo_db`) and the schema name (`demo_sc`) in
> the database and database path variables, respectively, in the request
> header.
>
> ![../../../_images/create-schema-table1.png](../../../_images/create-schema-
> table1.png)
>     2. Add the table name (`demo_tbl`) and the table columns to the request
> body. In this case, you added one column named `C1`.
>  
>         >         {
>           "name": "demo_tbl",
>           "columns": [
>             {
>             "name": "c1",
>             "datatype": "integer",
>             "nullable": true,
>             "comment": "An integral value column"
>             }
>           ],
>           "comment": "Demo table for Snowflake REST API"
>         }
>  
>
> Copy
>
> ![../../../_images/create-schema-table2.png](../../../_images/create-schema-
> table2.png)

  * To fetch the table you just created, send a `GET` request to the `/api/v2/databases/{database}/schemas/{schema}/tables/{name}` endpoint. In this case, you specify `demo_db`, `demo_sc`, and `demo_tbl` in the database, schema and name path variables, respectively.

> ![../../../_images/get-schema-table1.png](../../../_images/get-schema-
> table1.png)

For more information, see the [Snowflake Table API reference](/developer-
guide/snowflake-rest-api/reference/table.html).

## Alter a table and fetch the table details¶

You can use Postman to alter a table.

  * To alter the table you created in the last tutorial, send a `PUT` request to the `/api/v2/databases/{database}/schemas/{schema}/tables/{name}` endpoint, as follows:

    1. Specify the names of the database, schema, and table you created in the corresponding path variables.

> ![../../../_images/create-alter-schema-table1.png](../../../_images/create-
> alter-schema-table1.png)

    2. In the request body, enter the new table definition. In this case, you add a new column to the table.

> >         {
>           "name": "demo_tbl",
>           "columns": [
>             {
>             "name": "c1",
>             "datatype": "integer",
>             "nullable": true,
>             "comment": "An integral value column"
>             },
>             {
>             "name": "c2",
>             "datatype": "string",
>             "comment": "An string value column"
>             }
>           ],
>           "comment": "Demo table for Snowflake REST API"
>         }
>  
>
> Copy
>
> ![../../../_images/create-alter-schema-table2.png](../../../_images/create-
> alter-schema-table2.png)

  * Verify the change by fetching the table details by sending a `GET` request to the `/api/v2/databases/{database}/schemas/{schema}/tables/{name}` endpoint. In this case, you specify `demo_db`, `demo_sc`, and `demo_tbl` in the database, schema and name path variables, respectively.

![../../../_images/get-schema-table2.png](../../../_images/get-schema-
table2.png)

Notice the table now contains a new `C2` column.

For more information, see the [Snowflake Table API reference](/developer-
guide/snowflake-rest-api/reference/table.html).

## List available tables¶

You can use the `/api/v2/databases/{database}/schemas/{schema}/tables`
endpoint to return lists of all tables available to you.

  * To list all available tables, send a `GET` request to the `/api/v2/databases/{database}/schemas/{schema}/tables` endpoint with no query parameters, as follows. In this case, you specify `demo_db` and `demo_sc`, and `demo_tbl` in the database, schema and name path variables, respectively.

![../../../_images/list-schema-table1.png](../../../_images/list-schema-
table1.png)

  * To list full details of the columns and constraints in every table, add the recursive query parameter and set the value to `true`, as shown. Be aware that enabling this query parameter can overwhelm your connection if you have multiple complex tables.

![../../../_images/list-schema-tables1.png](../../../_images/list-schema-
tables1.png)

For more information, see the [Snowflake Table API reference](/developer-
guide/snowflake-rest-api/reference/table.html).

## What’s next?¶

Congratulations! In this tutorial, you learned the fundamentals for managing
Snowflake database, schema, and table resources using the Snowflake REST APIs.

### Summary¶

Along the way, you completed the following steps:

  * Create and list databases.

  * Create and list schemas.

  * Create a table and fetch the table details.

  * Alter a table and fetch the table details.

  * List available tables.

### Next tutorial¶

You can now proceed to [Tutorial 2: Create and manage tasks](tutorial-2),
which shows you how to create and manage Snowflake tasks.

