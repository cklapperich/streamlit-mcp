# Snowflake REST APIs¶

Feature — Generally Available

Not available in government regions.

Snowflake REST APIs for resource management provide a set of endpoints that
lets users programmatically interact with and control various resources within
the Snowflake Data Cloud.

The Snowflake REST APIs suite of APIs enables developers to build end-to-end
automation and integration with Snowflake resources. These REST APIs are
compliant with the [OpenAPI
specification](https://spec.openapis.org/oas/v3.1.0). Snowflake REST APIs
enable developers and partners to use the language of their choice to build
integrations with Snowflake using the openAPI specifications.

The Snowflake REST APIs supports the following resources through the
corresponding APIs. The APIs support CREATE OR ALTER operations for applicable
resources.

  * Working with accounts

    * [Accounts](account/account-introduction)

    * [Managed accounts](managed-account/managed-account-introduction)

  * Working with users, roles, and privileges

    * [Users](users/users-introduction)

    * [Roles](roles/roles-introduction)

    * [Database roles](database-role/database-role-introduction)

    * [Grants](grants/grants-introduction)

  * Managing virtual warehouses

    * [Warehouses](warehouses/warehouses-introduction)

  * Working with databases and schemas

    * [Databases](databases/db-introduction)

    * [Schemas](schemas/schemas-introduction)

  * Managing tables and views

    * [Tables](tables/tables-introduction)

    * [Dynamic tables](dynamic-tables/dynamic-tables-introduction)

    * [Event tables](event-table/event-table-introduction)

    * [Views](view/view-introduction)

  * Loading and unloading data

    * [Stages](stages/stages-introduction)

    * [External volumes](external-volume/external-volume-introduction)

    * [Pipes](pipe/pipe-introduction)

  * Managing notebooks

    * [Notebooks](notebook/notebook-introduction)

  * Working with Snowpark Container Services

    * [Compute Pools](compute-pools/cp-introduction)

    * [Image Repositories](image-repositories/images-introduction)

    * [Services](services/services-introduction)

  * Using functions and procedures

    * [Functions](functions/functions-introduction)

    * [User-defined functions](user-defined-function/user-defined-function-introduction)

    * [Procedures](procedure/procedure-introduction)

  * Managing security

    * [Network policies](network-policy/network-policy-introduction)

  * Managing alerts

    * [Alerts](alert/alert-introduction)

  * Leveraging AI/ML

    * [Cortex Inference](cortex-inference/cortex-inference-introduction)

    * [Cortex Search Service](cortex-search/cortex-search-introduction)

  * Managing streams and tasks

    * [Streams](stream/stream-introduction)

    * [Tasks](tasks/tasks-introduction)

  * Managing integrations

    * [Use catalog integrations](catalog-integration/catalog-integration-introduction)

    * [Use notification integrations](notification-integration/notification-integration-introduction)

For reference information about the APIs and their endpoints, see [Snowflake
REST APIs reference](reference).

You can access the Snowflake REST APIs OpenAPI specifications in the
[snowflake-rest-api-specs](https://github.com/snowflakedb/snowflake-rest-api-
specs) Git repository.

Note

The [Snowflake REST APIs reference
documentation](https://docs.snowflake.com/en/developer-guide/snowflake-rest-
api/snowflake-rest-api) reflects the latest version of the Snowflake REST
APIs. Note that not all resources in the API currently provide 100% coverage
of their equivalent [SQL commands](/sql-reference-commands), but the Snowflake
REST APIs are under active development and are continuously expanding.

## Requirements¶

The Snowflake REST APIs has the following requirements:

  * You must have a way to submit REST requests, such as the [Postman app](https://www.postman.com/downloads/), [curl](https://curl.se/), or an HTTP client in the programming language of your choice, installed on your machine.

## Suggested tools¶

  * [Postman app](https://www.postman.com/downloads/)

  * [curl](https://curl.se/)

  * [Snowflake CLI](../snowflake-cli/index)

  * [SnowSQL](../../user-guide/snowsql)

