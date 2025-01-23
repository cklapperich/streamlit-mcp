# Tutorial 2: Create and manage tasks and task graphs (DAGs)¶

Feature — Generally Available

Not available in government regions.

## Introduction¶

In this tutorial, you create and use Snowflake tasks to manage some basic
stored procedures. You also create a task graph — also called a directed
acyclic graph (DAG) — to orchestrate tasks with a higher-level task graph API.

### Prerequisites¶

Note

If you have already completed both [Common setup for Snowflake Python APIs
tutorials](common-setup) and [Tutorial 1: Create a database, schema, table,
and warehouse](tutorial-1), you can skip these prerequisites and proceed to
the first step of this tutorial.

Before you start this tutorial, you must complete the following steps:

  1. Follow the [common setup](common-setup) instructions, which includes the following steps:

     * Set up your development environment.

     * Install the Snowflake Python APIs package.

     * Configure your Snowflake connection.

     * Import all the modules required for the Python API tutorials.

     * Create an API `Root` object.

  2. Run the following code to create a database named `PYTHON_API_DB` and a schema named `PYTHON_API_SCHEMA` in that database.
    
        database = root.databases.create(
      Database(
        name="PYTHON_API_DB"),
        mode=CreateMode.or_replace
      )
    
    schema = database.schemas.create(
      Schema(
        name="PYTHON_API_SCHEMA"),
        mode=CreateMode.or_replace,
      )
    

Copy

These are the same database and schema objects you create in [Tutorial
1](tutorial-1).

After completing these prerequisites, you are ready to start using the API for
task management.

## Set up Snowflake objects¶

Set up the stored procedures that your tasks will invoke and the stage that
will hold the stored procedures. You can use your Snowflake Python APIs `root`
object to create a stage in the `PYTHON_API_DB` database and
`PYTHON_API_SCHEMA` schema you previously created.

  1. To create a stage named `TASKS_STAGE`, in the next cell of your notebook, run the following code:
    
        stages = root.databases[database.name].schemas[schema.name].stages
    stages.create(Stage(name="TASKS_STAGE"))
    

Copy

This stage will hold the stored procedures and any dependencies those
procedures need.

  2. To create two basic Python functions that the tasks will run as stored procedures, in your next cell, run the following code:
    
        def trunc(session: Session, from_table: str, to_table: str, count: int) -> str:
      (
        session
        .table(from_table)
        .limit(count)
        .write.save_as_table(to_table)
      )
      return "Truncated table successfully created!"
    
    def filter_by_shipmode(session: Session, mode: str) -> str:
      (
        session
        .table("snowflake_sample_data.tpch_sf100.lineitem")
        .filter(col("L_SHIPMODE") == mode)
        .limit(10)
        .write.save_as_table("filter_table")
      )
      return "Filter table successfully created!"
    

Copy

These functions do the following:

     * `trunc()`: Creates a truncated version of an input table.

     * `filter_by_shipmode()`: Filters the `SNOWFLAKE_SAMPLE_DATA.TPCH_SF100.LINEITEM` table by ship mode, limits the results to 10 rows, and writes the results in a new table.

Note

This function queries the [TPC-H sample data](../../../user-guide/sample-data-
tpch) in the SNOWFLAKE_SAMPLE_DATA database. Snowflake creates the sample
database in new accounts by default. If the database has not been created in
your account, see [Using the Sample Database](../../../user-guide/sample-data-
using).

The functions are intentionally basic and are intended for demonstration
purposes.

## Create and manage tasks¶

Define, create, and manage two tasks that will run your previously created
Python functions as stored procedures.

  1. To define the two tasks, `task1` and `task2`, in the next cell of your notebook, run the following code:
    
        tasks_stage = f"{database.name}.{schema.name}.TASKS_STAGE"
    
    task1 = Task(
        name="task_python_api_trunc",
        definition=StoredProcedureCall(
          func=trunc,
          stage_location=f"@{tasks_stage}",
          packages=["snowflake-snowpark-python"],
        ),
        warehouse="COMPUTE_WH",
        schedule=timedelta(minutes=1)
    )
    
    task2 = Task(
        name="task_python_api_filter",
        definition=StoredProcedureCall(
          func=filter_by_shipmode,
          stage_location=f"@{tasks_stage}",
          packages=["snowflake-snowpark-python"],
        ),
        warehouse="COMPUTE_WH"
    )
    

Copy

In this code, you specify the following task parameters:

     * For each task, a definition represented by a [StoredProcedureCall](https://docs.snowflake.com/en/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.task.StoredProcedureCall#snowflake.core.task.StoredProcedureCall) object that includes the following attributes:

       * The callable function to run

       * The stage location where the contents of your Python function and its dependencies are uploaded

       * The stored procedure’s package dependencies

     * A warehouse to run the stored procedure (required when creating a task with a `StoredProcedureCall` object). This tutorial uses the `COMPUTE_WH` warehouse that is included with your trial account.

     * A run schedule for the root task, `task1`. The schedule specifies the interval at which to run the task periodically.

For more information about stored procedures, see [Writing stored procedures
in Python](../../stored-procedure/python/procedure-python-overview).

  2. To create the two tasks, retrieve a `TaskCollection` object (`tasks`) from your database schema and call `.create()` on your task collection:
    
        # create the task in the Snowflake database
    tasks = schema.tasks
    trunc_task = tasks.create(task1, mode=CreateMode.or_replace)
    
    task2.predecessors = [trunc_task.name]
    filter_task = tasks.create(task2, mode=CreateMode.or_replace)
    

Copy

In this code example, you also link the tasks by setting `task1` as a
predecessor to `task2`, which creates a minimal task graph.

  3. To confirm that the two tasks now exist, in your next cell, run the following code:
    
        taskiter = tasks.iter()
    for t in taskiter:
        print(t.name)
    

Copy

  4. When you create tasks, they are suspended by default.

To start a task, call `.resume()` on the task resource object:

    
        trunc_task.resume()
    

Copy

  5. To confirm that the `trunc_task` task was started, in your next cell, run the following code:
    
        taskiter = tasks.iter()
    for t in taskiter:
        print("Name: ", t.name, "| State: ", t.state)
    

Copy

The output should be similar to this:

    
        Name:  TASK_PYTHON_API_FILTER | State:  suspended
    Name:  TASK_PYTHON_API_TRUNC | State:  started
    

You can repeat this step whenever you want to confirm the status of the tasks.

  6. To clean up your task resources, you first suspend the task before dropping it.

In your next cell, run the following code:

    
        trunc_task.suspend()
    

Copy

  7. To confirm that the task is suspended, repeat step 5.

  8. Optional: To drop both tasks, in your next cell, run the following code:
    
        trunc_task.drop()
    filter_task.drop()
    

Copy

## Create and manage a task graph¶

When you’re coordinating the execution of a large number of tasks,
individually managing each task can be a challenge. The Snowflake Python APIs
provides functionality to orchestrate tasks with a higher-level task graph
API.

A task graph, which is also called a directed acyclic graph (DAG), is a series
of tasks composed of a root task and child tasks, organized by their
dependencies. For more information, see [Manage task dependencies with task
graphs](../../../user-guide/tasks-graphs.html#label-task-dag).

  1. To create and deploy a task graph, run the following code:
    
        dag_name = "python_api_dag"
    dag = DAG(name=dag_name, schedule=timedelta(days=1))
    with dag:
        dag_task1 = DAGTask(
            name="task_python_api_trunc",
            definition=StoredProcedureCall(
                func=trunc,
                stage_location=f"@{tasks_stage}",
                packages=["snowflake-snowpark-python"]),
            warehouse="COMPUTE_WH",
        )
        dag_task2 = DAGTask(
            name="task_python_api_filter",
            definition=StoredProcedureCall(
                func=filter_by_shipmode,
                stage_location=f"@{tasks_stage}",
                packages=["snowflake-snowpark-python"]),
            warehouse="COMPUTE_WH",
        )
        dag_task1 >> dag_task2
    dag_op = DAGOperation(schema)
    dag_op.deploy(dag, mode=CreateMode.or_replace)
    

Copy

In this code, you do the following:

     * Create a task graph object by calling the `DAG` constructor and specifying a name and schedule.

     * Define task graph–specific tasks using the `DAGTask` constructor. Note that the constructor accepts the same arguments that you specified for the `StoredProcedureCall` class in a previous step.

     * Specify `dag_task1` as the root task and predecessor to `dag_task2` with more convenient syntax.

     * Deploy the task graph to the `PYTHON_API_SCHEMA` schema of the `PYTHON_API_DB` database.

  2. To confirm the creation of the task graph, in your next cell, run the following code:
    
        taskiter = tasks.iter()
    for t in taskiter:
        print("Name: ", t.name, "| State: ", t.state)
    

Copy

You can repeat this step whenever you want to confirm the status of the tasks.

  3. To start the task graph by starting the root task, in your next cell, run the following code:
    
        dag_op.run(dag)
    

Copy

  4. To confirm that the `PYTHON_API_DAG$TASK_PYTHON_API_TRUNC` task started, repeat step 2.

Note

The function call invoked by the task graph will not succeed because you are
not calling it with any of its required arguments. The purpose of this step is
only to demonstrate how to programmatically start the task graph.

  5. To drop the task graph, in your next cell, run the following code:
    
        dag_op.drop(dag)
    

Copy

  6. Clean up the database object that you created in these tutorials:
    
        database.drop()
    

Copy

## What’s next?¶

Congratulations! In this tutorial, you learned how to create and manage tasks
and task graphs using the Snowflake Python APIs.

### Summary¶

Along the way, you completed the following steps:

  * Create a stage that can hold stored procedures and their dependencies.

  * Create and manage tasks.

  * Create and manage a task graph.

  * Clean up your Snowflake resource objects by dropping them.

### Next tutorial¶

You can now proceed to [Tutorial 3: Create and manage Snowpark Container
Services](tutorial-3), which shows how to create and manage components in
Snowpark Container Services.

### Additional resources¶

For more examples of using the API to manage other types of objects in
Snowflake, see the following developer guides:

Guide | Description  
---|---  
[Managing Snowflake databases, schemas, tables, and views with Python](../snowflake-python-managing-databases) | Use the API to create and manage databases, schemas, and tables.  
[Managing Snowflake users, roles, and grants with Python](../snowflake-python-managing-user-roles) | Use the API to create and manage users, roles, and grants.  
[Managing data loading and unloading resources with Python](../snowflake-python-managing-data-loading) | Use the API to create and manage data loading and unloading resources, including external volumes, pipes, and stages.  
[Managing Snowpark Container Services (including service functions) with Python](../snowflake-python-managing-containers) | Use the API to manage components of Snowpark Container Services, including compute pools, image repositories, services, and service functions.

