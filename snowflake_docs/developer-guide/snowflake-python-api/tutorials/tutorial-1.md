# Tutorial 1: Create a database, schema, table, and warehouse¶

Feature — Generally Available

Not available in government regions.

## Introduction¶

In this tutorial, you learn the fundamentals for managing Snowflake resource
objects using the Snowflake Python APIs. To get started with the API, you
create and manage a Snowflake database, schema, table, and virtual warehouse.

### Prerequisites¶

Note

If you have already completed the steps in [Common setup for Snowflake Python
APIs tutorials](common-setup), you can skip these prerequisites and proceed to
the first step of this tutorial.

Before you start this tutorial, you must complete the [common setup](common-
setup) instructions, which includes the following steps:

>   * Set up your development environment.
>
>   * Install the Snowflake Python APIs package.
>
>   * Configure your Snowflake connection.
>
>   * Import all the modules required for the Python API tutorials.
>
>   * Create an API `Root` object.
>
>

After completing these prerequisites, you are ready to start using the API.

## Create a database, schema, and table¶

You can use your `root` object to create a database, schema, and table in your
Snowflake account.

  1. To create a database, in the next cell of your notebook, run the following code:
    
        database = root.databases.create(
      Database(
        name="PYTHON_API_DB"),
        mode=CreateMode.or_replace
      )
    

Copy

This code, which is functionally equivalent to the SQL command `CREATE OR
REPLACE DATABASE PYTHON_API_DB`, creates a database in your account named
`PYTHON_API_DB`. This code follows a common pattern for managing objects in
Snowflake:

     * `root.databases.create()` creates a database in Snowflake. It accepts two arguments: a `Database` object and a mode.

     * You pass a `Database` object by using `Database(name="PYTHON_API_DB")`, and set the name of the database by using the `name` argument. Recall that you imported `Database` on line 3 of the notebook.

     * You specify the creation mode by passing the `mode` argument. In this case, you set it to `CreateMode.or_replace`, but the following values are also valid:

       * `CreateMode.if_not_exists`: Functionally equivalent to CREATE IF NOT EXISTS in SQL.

       * `CreateMode.error_if_exists`: Raises an exception if the object already exists in Snowflake. This is the default value if a mode is not specified.

     * You manage the database programmatically by storing a reference to the database in an object you created named `database`.

  2. In [Snowsight](../../../user-guide/ui-snowsight), navigate to the databases section of your Snowflake account. If your code was successful, the `PYTHON_API_DB` database is listed.

Tip

If you use VS Code, install the [Snowflake
extension](https://marketplace.visualstudio.com/items?itemName=snowflake.snowflake-
vsc) to explore all Snowflake objects within your editor.

  3. To create a schema in the `PYTHON_API_DB` database, in your next cell, run the following code:
    
        schema = database.schemas.create(
      Schema(
        name="PYTHON_API_SCHEMA"),
        mode=CreateMode.or_replace,
      )
    

Copy

Note that you call `.schemas.create()` on the `database` object you created
previously.

  4. To create a table in the schema you just created, in your next cell, run the following code:
    
        table = schema.tables.create(
      Table(
        name="PYTHON_API_TABLE",
        columns=[
          TableColumn(
            name="TEMPERATURE",
            datatype="int",
            nullable=False,
          ),
          TableColumn(
            name="LOCATION",
            datatype="string",
          ),
        ],
      ),
    mode=CreateMode.or_replace
    )
    

Copy

This code creates a table in the `PYTHON_API_SCHEMA` schema with two columns
and their data types specified: `TEMPERATURE` as `int`, and `LOCATION` as
`string`.

These last two code examples should look familiar because they follow the
pattern in the first step where you created the `PYTHON_API_DB` database.

  5. To confirm that the objects were created, return to your Snowflake account in Snowsight.

## Retrieve object data¶

You can retrieve metadata about an object in Snowflake.

  1. To retrieve details about the `PYTHON_API_TABLE` table you created previously, in your next notebook cell, run the following code:
    
        table_details = table.fetch()
    

Copy

`fetch()` returns a `TableModel` object.

  2. You can then call `.to_dict()` on the resulting object to view its detailed information.

To print the table details, in your next cell, run the following code:

    
        table_details.to_dict()
    

Copy

The notebook should display a dictionary that contains metadata about the
`PYTHON_API_TABLE` table, similar to this:

    
        {
        "name": "PYTHON_API_TABLE",
        "kind": "TABLE",
        "enable_schema_evolution": False,
        "change_tracking": False,
        "data_retention_time_in_days": 1,
        "max_data_extension_time_in_days": 14,
        "default_ddl_collation": "",
        "columns": [
            {"name": "TEMPERATURE", "datatype": "NUMBER(38,0)", "nullable": False},
            {"name": "LOCATION", "datatype": "VARCHAR(16777216)", "nullable": True},
        ],
        "created_on": datetime.datetime(
            2024, 5, 9, 8, 59, 15, 832000, tzinfo=datetime.timezone.utc
        ),
        "database_name": "PYTHON_API_DB",
        "schema_name": "PYTHON_API_SCHEMA",
        "rows": 0,
        "bytes": 0,
        "owner": "ACCOUNTADMIN",
        "automatic_clustering": False,
        "search_optimization": False,
        "owner_role_type": "ROLE",
    }
    

Copy

As shown, this dictionary contains information about the `PYTHON_API_TABLE`
table that you created previously, with detailed information about `columns`,
`owner`, `database`, `schema`, and more.

Object metadata is useful when you are building business logic in your
application. For example, you might build logic that runs depending on certain
information about an object. You can use `fetch()` to retrieve object metadata
in such scenarios.

## Programmatically alter a table¶

You can programmatically add a column to a table. The `PYTHON_API_TABLE` table
currently has two columns: `TEMPERATURE` and `LOCATION`. In this scenario, you
want to add a new column named `ELEVATION` of type `int` and set it as the
table’s primary key.

  1. In your next cell, run the following code:
    
        table_details.columns.append(
        TableColumn(
          name="elevation",
          datatype="int",
          nullable=False,
          constraints=[PrimaryKey()],
        )
    )
    

Copy

Note

This code does not create the column. Instead, this column definition is
appended to the array that represents the table’s columns in the `TableModel`.
To view this array, review the value of `columns` as described in the
instructions for viewing the table metadata.

  2. To modify the table and add the column, in your next cell, run the following code:
    
        table.create_or_alter(table_details)
    

Copy

In this line, you call `create_or_alter()` on the object representing
`PYTHON_API_TABLE`, and pass the updated value of `table_details`. This line
adds the `ELEVATION` column to `PYTHON_API_TABLE`.

  3. To confirm that the column was added, in your next cell, run the following code:
    
        table.fetch().to_dict()
    

Copy

The output should look similar to this:

    
        {
        "name": "PYTHON_API_TABLE",
        "kind": "TABLE",
        "enable_schema_evolution": False,
        "change_tracking": False,
        "data_retention_time_in_days": 1,
        "max_data_extension_time_in_days": 14,
        "default_ddl_collation": "",
        "columns": [
            {"name": "TEMPERATURE", "datatype": "NUMBER(38,0)", "nullable": False},
            {"name": "LOCATION", "datatype": "VARCHAR(16777216)", "nullable": True},
            {"name": "ELEVATION", "datatype": "NUMBER(38,0)", "nullable": False},
        ],
        "created_on": datetime.datetime(
            2024, 5, 9, 8, 59, 15, 832000, tzinfo=datetime.timezone.utc
        ),
        "database_name": "PYTHON_API_DB",
        "schema_name": "PYTHON_API_SCHEMA",
        "rows": 0,
        "bytes": 0,
        "owner": "ACCOUNTADMIN",
        "automatic_clustering": False,
        "search_optimization": False,
        "owner_role_type": "ROLE",
        "constraints": [
            {"name": "ELEVATION", "column_names": ["ELEVATION"], "constraint_type": "PRIMARY KEY"}
        ]
    }
    

Copy

Review the value of `columns` and the value of `constraints`, both of which
now include the `ELEVATION` column.

  4. To confirm the existence of the new column, return to your Snowflake account in Snowsight and inspect the table.

## Create and manage a warehouse¶

You can also manage virtual warehouses with the Snowflake Python APIs. For
example, you might need to create another warehouse temporarily to run certain
queries. In this scenario, you can use the API to create, suspend, or drop a
warehouse.

  1. To retrieve the collection of warehouses associated with your session, in your next cell, run the following code:
    
        warehouses = root.warehouses
    

Copy

You manage warehouses in your session using the resulting `warehouses` object.

  2. To define and create a new warehouse, in your next cell, run the following code:
    
        python_api_wh = Warehouse(
        name="PYTHON_API_WH",
        warehouse_size="SMALL",
        auto_suspend=500,
    )
    
    warehouse = warehouses.create(python_api_wh,mode=CreateMode.or_replace)
    

Copy

In this code, you define a new warehouse by instantiating `Warehouse` and
specifying the warehouse’s name, size, and auto-suspend policy. The auto-
suspend timeout is in units of seconds. In this case, the warehouse will be
suspended after 8.33 minutes of inactivity.

You then create the warehouse by calling `create()` on your warehouse
collection. You store the reference in the resulting `warehouse` object.

  3. Navigate to your Snowflake account in Snowsight and confirm that the warehouse was created.

  4. To retrieve information about the warehouse, in your next cell, run the following code:
    
        warehouse_details = warehouse.fetch()
    warehouse_details.to_dict()
    

Copy

This code should look familiar because it follows the same pattern you used to
fetch table metadata in a previous step. The output should be similar to this:

    
        {
      'name': 'PYTHON_API_WH',
      'auto_suspend': 500,
      'auto_resume': 'true',
      'resource_monitor': 'null',
      'comment': '',
      'max_concurrency_level': 8,
      'statement_queued_timeout_in_seconds': 0,
      'statement_timeout_in_seconds': 172800,
      'tags': {},
      'warehouse_type': 'STANDARD',
      'warehouse_size': 'Small'
    }
    

Copy

  5. Optional: If you have multiple warehouses in your session, use the API to iterate through them or to search for a specific warehouse.

In your next cell, run the following code:

    
        warehouse_list = warehouses.iter(like="PYTHON_API_WH")
    result = next(warehouse_list)
    result.to_dict()
    

Copy

In this code, you call `iter()` on the warehouse collection and pass the
`like` argument, which returns any warehouses whose names match the specified
string. In this case, you pass the name of the warehouse you defined
previously, but this argument is generally a case-insensitive string that
functions as a filter, with support for SQL wildcard characters like `%` and
`_`.

After you run the cell, output similar to the following code shows that you
successfully returned a matching warehouse:

    
        {
      'name': 'PYTHON_API_WH',
      'auto_suspend': 500,
      'auto_resume': 'true',
      'resource_monitor': 'null',
      'comment': '',
      'max_concurrency_level': 8,
      'statement_queued_timeout_in_seconds': 0,
      'statement_timeout_in_seconds': 172800,
      'tags': {},
      'warehouse_type': 'STANDARD',
      'warehouse_size': 'Small'
    }
    

Copy

  6. To programmatically modify the warehouse by changing its size to `LARGE`, in your next cell, run the following code:
    
        warehouse = root.warehouses.create(Warehouse(
        name="PYTHON_API_WH",
        warehouse_size="LARGE",
        auto_suspend=500,
    ), mode=CreateMode.or_replace)
    

Copy

  7. To confirm that the warehouse size was updated to `LARGE`, do one of the following:

     * In your next cell, run the following code:
        
                warehouse.fetch().size
        

Copy

     * Navigate to your Snowflake account in Snowsight and confirm the change in warehouse size.

  8. Optional: If you don’t want to continue using the warehouse, drop it. In your next cell, run the following code:
    
        warehouse.drop()
    

Copy

  9. To confirm the warehouse deletion, return to your Snowflake account in Snowsight.

## What’s next?¶

Congratulations! In this tutorial, you learned the fundamentals for managing
Snowflake resource objects using the Snowflake Python APIs.

### Summary¶

Along the way, you completed the following steps:

  * Install the Snowflake Python APIs.

  * Set up a connection to Snowflake.

  * Create a database, schema, and table.

  * Retrieve object information.

  * Programmatically alter an object.

  * Create, suspend, and drop a warehouse.

### Next tutorial¶

You can now proceed to [Tutorial 2: Create and manage tasks and task graphs
(DAGs)](tutorial-2), which shows how to create and manage tasks and task
graphs.

### Additional resources¶

For more examples of using the API to manage other types of objects in
Snowflake, see the following developer guides:

Guide | Description  
---|---  
[Managing Snowflake users, roles, and grants with Python](../snowflake-python-managing-user-roles) | Use the API to create and manage users, roles, and grants.  
[Managing data loading and unloading resources with Python](../snowflake-python-managing-data-loading) | Use the API to create and manage data loading and unloading resources, including external volumes, pipes, and stages.  
[Managing Snowflake tasks and task graphs with Python](../snowflake-python-managing-tasks) | Use the API to create, execute, and manage tasks and task graphs.  
[Managing Snowpark Container Services (including service functions) with Python](../snowflake-python-managing-containers) | Use the API to manage components of Snowpark Container Services, including compute pools, image repositories, services, and service functions.

