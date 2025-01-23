# Common setup for Snowflake Python APIs tutorials¶

Feature — Generally Available

Not available in government regions.

## Introduction¶

This topic provides instructions for the common setup required for all
Snowflake Python APIs tutorials available in this documentation.

### Overview of the Snowflake Python APIs¶

Before starting your setup, take a look at the Snowflake Python APIs
structure. The following table lists some common modules in the API:

Module | Description  
---|---  
`snowflake.core` | Defines an iterator to represent certain resource instances fetched from the Snowflake database.  
`snowflake.core.database` | Manages Snowflake databases.  
`snowflake.core.schema` | Manages Snowflake schemas.  
`snowflake.core.table` | Manages Snowflake tables.  
`snowflake.core.task` | Manages Snowflake tasks.  
`snowflake.core.task.dagv1` | A set of APIs at a higher level than the task APIs in `snowflake.core.task` to more conveniently manage task graphs (DAGs).  
`snowflake.core.compute_pool` | Manages compute pools in Snowpark Container Services.  
`snowflake.core.image_repository` | Manages image repositories in Snowpark Container Services.  
`snowflake.core.service` | Manages services in Snowpark Container Services.  
  
For a complete list of the APIs currently available, see the [API reference
documentation](https://docs.snowflake.com/developer-guide/snowflake-python-
api/reference/latest/index).

The `snowflake.core` module represents the entry point to the core Snowflake
Python APIs that manage Snowflake objects. To use the API, you follow a common
pattern:

  1. Establish a session using Snowpark or a Python Connector connection, representing your connection to Snowflake.

  2. Import and instantiate the `Root` class from `snowflake.core`, and pass the Snowpark session object as an argument.

You use the resulting `Root` object to access the rest of the methods and
types in the API.

The following code is an example of what this pattern typically looks like:

    
    
    from snowflake.snowpark import Session
    from snowflake.core import Root
    
    session = Session.builder.configs(connection_params).create()
    root = Root(session)
    

Copy

For more information about various connection options and attributes, see
[Connect to Snowflake with the Snowflake Python APIs](../snowflake-python-
connecting-snowflake).

Note

The Snowflake Python APIs can establish a connection to Snowflake using either
a Snowpark session or a Python Connector connection. The preceding example
uses a Snowpark session.

Continue to the next step to start setting up the API and your development
environment!

## Install the Snowflake Python APIs¶

Important

The Snowflake Python APIs currently supports the following versions of Python:

  * 3.9

  * 3.10

  * 3.11

Before installing the API, you need to activate a Python environment.

In this tutorial, you can use conda or a virtual environment (venv).

  1. To create and activate a conda or virtual environment, open a command line terminal and run the following commands:

condavenv

    
        conda create -n <env_name> python==3.10
    conda activate <env_name>
    

Copy

    
        python3 -m venv '.venv'
    source '.venv/bin/activate'
    

Copy

  2. The Snowflake Python APIs package is available in PyPI.

To install the API package in the new conda or virtual environment, run the
following command:

    
        pip install snowflake -U
    

Copy

## Set up your development environment¶

This tutorial walks through code examples that you can run in a Jupyter
notebook. Each step in the tutorial incrementally showcases the capabilities
of the Snowflake Python APIs.

You start by setting up your development environment so that you can run the
code examples in a notebook.

  1. Create a file named `$HOME/.snowflake/connections.toml` with the following connection parameters, and update it with your real credentials:
    
        [default]
    account = "<YOUR ACCOUNT NAME>"
    user = "<YOUR ACCOUNT USER>"
    password = "<YOUR ACCOUNT USER PASSWORD>"
    # optional
    # warehouse = "<YOUR COMPUTE WH>"
    # optional
    # database = "<YOUR DATABASE>"
    # optional
    # schema = "<YOUR SCHEMA>"
    

Copy

Note

The `account` parameter does not support [account identifiers](../../../user-
guide/admin-account-identifier) with underscores. You must specify an account
identifier with dashes in place of any underscores. For more information, see
[Account name in your organization](../../../user-guide/admin-account-
identifier.html#label-account-name).

This example specifies these parameters as the default connection to Snowflake
in your environment by creating a connection definition named `default`.

  2. Use one of the following methods to open a notebook:

     * Open a new notebook in a code editor that supports Jupyter notebooks (such as Visual Studio Code).

     * To open a notebook in your browser, start a notebook server with the command `jupyter notebook`.

To ensure that your environment can run a notebook, run `conda install
notebook` in your terminal before starting the notebook server.

  3. In the first cell of the notebook, run the following import statements:
    
        from datetime import timedelta
    
    from snowflake.snowpark import Session
    from snowflake.snowpark.functions import col
    from snowflake.core import Root, CreateMode
    from snowflake.core.database import Database
    from snowflake.core.schema import Schema
    from snowflake.core.stage import Stage
    from snowflake.core.table import Table, TableColumn, PrimaryKey
    from snowflake.core.task import StoredProcedureCall, Task
    from snowflake.core.task.dagv1 import DAGOperation, DAG, DAGTask
    from snowflake.core.warehouse import Warehouse
    

Copy

Note

After running this cell, you might be prompted to set your Python kernel. If
you activated a conda environment, select conda as the Python kernel (for
example, something similar to: `~/miniconda3/envs/<your conda
env>/bin/python`).

In this cell, you import Snowpark and the core APIs that manage Snowflake
objects.

  4. In the next cell, run the following code:
    
        connection_params = {
        "connection_name": "default"
    }
    

Copy

In this cell, you set the Snowflake connection parameters for your session by
creating a `connection_params` dictionary specifying the connection definition
named `default` that you previously configured.

  5. To establish a connection to Snowflake, create a Snowpark session and pass `connection_params` as an argument:
    
        session = Session.builder.configs(connection_params).create()
    

Copy

  6. To create a `Root` object, pass your `session` object to the `Root` constructor:
    
        root = Root(session)
    

Copy

And that’s it! By running the code in these four cells, you’re now ready to
use the Snowflake Python APIs.

### What’s next?¶

You can now explore [Tutorial 1: Create a database, schema, table, and
warehouse](tutorial-1).

