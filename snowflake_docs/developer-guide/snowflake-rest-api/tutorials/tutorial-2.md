# Tutorial 2: Create and manage tasks¶

Feature — Generally Available

Not available in government regions.

## Introduction¶

In this tutorial, you learn how to submit REST queries to create and manage
tasks.

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

## Create a warehouse¶

You can use the Warehouse API to create a Snowflake warehouse.

To create an extra small (`xsmall`) warehouse named `demo_wh`, send the
following POST request to the `/api/v2/warehouses` endpoint, as shown:

  * In the Params tab, set the `createMode` parameter to `errorIfExists`, which ensures that you don’t unintentionally overwrite an existing warehouse.

![../../../_images/create-warehouse-params.png](../../../_images/create-
warehouse-params.png)

  * In the Body tab, add the following code to the request body as shown.
    
        {
      "name": "demo_wh",
      "warehouse_size": "xsmall"
    }
    

Copy

![../../../_images/create-warehouse1.png](../../../_images/create-
warehouse1.png)

For more information, see the [Snowflake Warehouse API reference](/developer-
guide/snowflake-rest-api/reference/warehouse.html).

## Create a task¶

You can use the Task API to create a Snowflake task.

To create a task, send a POST request to the
`/api/v2/databases/{database}/schemas/{schema}/tasks` endpoint, as shown:

  * In the Params tab, set the `createMode` parameter to `orReplace`, and set the `database` and `schema` path variables to use the environment variables (`{{default_db}}` and `{{default_schema}}`) you set in the [Common setup for Snowflake REST APIs tutorials](common-setup) tutorials.

![../../../_images/create-task-params.png](../../../_images/create-task-
params.png)

  * In the Body tab, add the request body as shown.
    
        {
      "name": "{{test_task_name}}",
      "definition": "SELECT 1",
      "warehouse": "{{default_wh}}",
      "schedule": {"minutes": 2, "schedule_type": "MINUTES_TYPE"},
      "config": {"consecteture": false, "sed_9": 61393640, "doloref3": -85761000},
      "commnent": "comment",
      "session_parameters": {
        "TIMEZONE": "America/Los Angeles",
        "AUTOMCOMMIT": true
      },
      "error_integration": null,
      "user_task_managed_initial_warehouse_size": null,
      "predecessors": null,
      "task_auto_retry_attempts": 3,
      "user_task_timeout_ms": 10000,
      "suspend_task_after_num_failures": 3,
      "condition": true,
      "allow_overlapping_execution": false
    }
    

Copy

![../../../_images/create-task1.png](../../../_images/create-task1.png)

For more information, see the [Snowflake Task API reference](/developer-
guide/snowflake-rest-api/reference/task.html).

## Fetch a task¶

You can use the Task API to fetch a Snowflake task.

To fetch details about a task, send a GET request to the
`/api/v2/databases/{database}/schemas/{schema}/tasks` endpoint, as shown:

  * In the Params tab, set the `database`, `schema`, and `name` path variables to use the environment variables (`{{default_db}}`, `{{default_schema}}`, and `{{test_task_name}}`) you set in the [Common setup for Snowflake REST APIs tutorials](common-setup) tutorials.

![../../../_images/fetch-task1.png](../../../_images/fetch-task1.png)

For more information, see the [Snowflake Task API reference](/developer-
guide/snowflake-rest-api/reference/task.html).

## List tasks¶

You can use the Task API to list Snowflake tasks.

To list all available tasks, send a GET request to the
`/api/v2/databases/{database}/schemas/{schema}/tasks` endpoint, as shown:

  * In the Params tab, set the `rootOnly` parameter to `false`, and set the `database` and `schema` path variables to use the environment variables (`{{default_db}}` and `{{default_schema}}`) you set in the [Common setup for Snowflake REST APIs tutorials](common-setup) tutorials.

![../../../_images/list-tasks1.png](../../../_images/list-tasks1.png)

For more information, see the [Snowflake Task API reference](/developer-
guide/snowflake-rest-api/reference/task.html).

## Delete a task¶

You can use the Task API to delete a Snowflake task.

To delete a task, send a DELETE request to the
`/api/v2/databases/{database}/schemas/{schema}/tasks/{name}` endpoint, as
shown:

  * In the Params tab, set the `database`, `schema`, and `name` path variables to use the environment variables (`{{default_db}}`, `{{default_schema}}`, and `{{test_task_name}}`) you set in the [Common setup for Snowflake REST APIs tutorials](common-setup) tutorials.

![../../../_images/delete-task.png](../../../_images/delete-task.png)

For more information, see the [Snowflake Task API reference](/developer-
guide/snowflake-rest-api/reference/task.html).

## Execute a task¶

You can use the Task API to execute a Snowflake task.

To execute a task that will not retry if it fails, send a POST request to the
`/api/v2/databases/{database}/schemas/{schema}/tasks/{name}:execute` endpoint,
as shown:

  * In the Params tab, set the `retryLast` parameter to `false`, and set the `database` and `schema` path variables to use the environment variables (`{{default_db}}` and `{{default_schema}}`) you set in the [Common setup for Snowflake REST APIs tutorials](common-setup) tutorials.

![../../../_images/execute-task.png](../../../_images/execute-task.png)

For more information, see the [Snowflake Task API reference](/developer-
guide/snowflake-rest-api/reference/task.html).

## Complete graphs¶

Note

This tutorial assumes your have a default warehouse defined.

You can use the Task API to return details for graph runs that have completed.

To return details for completed graph runs for a task, send a GET request to
the `/api/v2/databases/{database}/schemas/{schema}/tasks/{name}:execute`
endpoint, as shown:

  * In the Params tab, do the following:

    * Set the `resultLimit` and `errorOnly` query parameters to `5` and `false`, respectively.

    * Set the `database`, `schema`, and `name` path variables to use the environment variables (`{{default_db}}`, `{{default_schema}}`, and `{{test_task_name}}`) you set in the [Common setup for Snowflake REST APIs tutorials](common-setup) tutorials.

![../../../_images/complete-graphs.png](../../../_images/complete-graphs.png)

For more information, see the [Snowflake Task API reference](/developer-
guide/snowflake-rest-api/reference/task.html).

## Create a child task¶

You can use the Task API to create a child task for an existing Snowflake
task.

To create a child task, send a POST request to the
`/api/v2/databases/{database}/schemas/{schema}/tasks` endpoint, as shown:

  * In the Params tab, set the `createMode` parameter to `orReplace`, and set the `database` and `schema` path variables to use the environment variables (`{{default_db}}` and `{{default_schema}}`) you set in the [Common setup for Snowflake REST APIs tutorials](common-setup) tutorials.

![../../../_images/create-task-params.png](../../../_images/create-task-
params.png)

  * In the Body tab, add the request body as shown. The `name` parameter specifies the name of the child task and `predecessors` identifies the name of the parent task.
    
        {
      "name": "test_child_task",
      "definition": "SELECT 1",
      "warehouse": "{{default_wh}}",
      "predecessors": "{{test_task_name}}"
    }
    

Copy

![../../../_images/create-child-task.png](../../../_images/create-child-
task.png)

For more information, see the [Snowflake Task API reference](/developer-
guide/snowflake-rest-api/reference/task.html).

## Fetch a parent task’s dependent tasks¶

Note

This tutorial assumes your have a default warehouse defined.

You can use the Task API to fetch a Snowflake task’s child (dependent) task.

To fetch details about a child (dependent) task, send a GET request to the
`/api/v2/databases/{database}/schemas/{schema}/tasks/{name}/dependents`
endpoint, as shown:

  * In the Params tab, set the `recursive` query parameter to `true`, and set the `database`, `schema`, and `name` path variables to use the environment variables (`{{default_db}}`, `{{default_schema}}`, and `{{test_task_name}}`) you set in the [Common setup for Snowflake REST APIs tutorials](common-setup) tutorials.

![../../../_images/get-task-dependents.png](../../../_images/get-task-
dependents.png)

Note that the result includes both the parent task and its child task.

For more information, see the [Snowflake Task API reference](/developer-
guide/snowflake-rest-api/reference/task.html).

## What’s next?¶

Congratulations! In this tutorial, you learned the fundamentals for managing
Snowflake warehouse and task resources using the Snowflake REST APIs.

### Summary¶

Along the way, you completed the following steps:

  * Create a warehouse.

  * Create a task.

  * Fetch a task.

  * Delete a task.

  * Execute task.

  * Complete graphs.

  * Create a child task.

  * Fetch a parent task’s dependent tasks.

