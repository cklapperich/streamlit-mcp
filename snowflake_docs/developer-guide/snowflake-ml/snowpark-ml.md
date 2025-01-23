# Python APIs for Snowflake ML¶

The `snowflake-ml-python` Python package provides Python APIs that connect to
the various Snowflake ML workflow components and also includes APIs for
building and training your own models. You can use these APIs in your favorite
Python IDE on your own workstation, in Snowsight worksheets, or in Snowflake
notebooks.

Tip

See [Introduction to Machine Learning with Snowpark
ML](https://quickstarts.snowflake.com/guide/intro_to_machine_learning_with_snowpark_ml_for_python/#0)
for an example of an end-to-end workflow using this library.

## Using Snowflake ML in Snowflake Notebooks¶

[Snowflake Notebooks](../../user-guide/ui-snowsight/notebooks) provide an
easy-to-use notebook interface for your data work, blending Python, SQL, and
Markdown. To use Snowflake ML features in notebooks, choose the Anaconda
package `snowflake-ml-python` using the Packages menu at the top of the
notebook.

Notebooks support both CPU and GPU runtime options. Many kinds of models
require, or benefit from, having a GPU available.

Important

The `snowflake-ml-python` package and its dependencies must be allowed by your
organization’s [package policy](../udf/python/packages-policy).

## Using Snowflake ML in Snowsight Worksheets¶

[Snowsight Worksheets](../../user-guide/ui-snowsight-worksheets) provide a
powerful and versatile method for running Python code. To use Snowflake ML
features in worksheets, choose the Anaconda package `snowflake-ml-python`
using the Packages menu at the top of the worksheet.

Important

The `snowflake-ml-python` package and its dependencies must be allowed by your
organization’s [package policy](../udf/python/packages-policy).

## Using Snowflake ML Locally¶

You must install the `snowflake-ml-python` package to develop on your own
workstation or elsewhere outside Snowflake. All Snowpark ML features are
available in a single package, `snowflake-ml-python`. You can install the
package from the Snowflake conda channel using the `conda` command or from the
Python Package Index (PyPI) using `pip`. Conda is preferred.

  * Installing from the Snowflake conda Channel

  * Installing from PyPI

### Installing from the Snowflake conda Channel¶

Important

Installing `snowflake-ml-python` from conda on an arm-based Mac (with M1 or M2
chip) requires specifying the system architecture when creating the conda
environment. To do this, include `CONDA_SUBDIR=osx-arm64` in the `conda
create` command: `CONDA_SUBDIR=osx-arm64 conda create --name snowpark-ml`.

  1. Create the conda environment where you will install Snowpark ML. If you prefer to use an existing environment, skip this step.
    
        conda create --name snowpark-ml
    

Copy

  2. Activate the conda environment:
    
        conda activate snowpark-ml
    

Copy

  3. Install `snowflake-ml-python` from the Snowflake conda channel:
    
        conda install --override-channels --channel https://repo.anaconda.com/pkgs/snowflake/ snowflake-ml-python
    

Copy

Tip

Install packages from the Snowflake conda channel whenever possible to ensure
that you receive packages that have been validated with Snowpark ML.

### Installing from PyPI¶

You can install `snowflake-ml-python` from the Python Package Index (PyPI) by
using the standard Python package manager, `pip`.

Warning

Do not use this installation procedure if you are using a conda environment.
Use the conda instructions instead.

  1. Change to your project directory and activate your Python virtual environment:

> >     cd ~/projects/ml
>     source .venv/bin/activate
>  
>
> Copy

  2. Install the `snowflake-ml-python` package:

> >     python -m pip install snowflake-ml-python
>  
>
> Copy

### Installing Optional Modeling Dependencies¶

Some modeling APIs require dependencies that are not installed as dependencies
of `snowflake-ml-python`. The scikit-learn and xgboost packages are installed
by default, but lightgbm is an optional dependency. If you plan to use classes
in the `snowflake.ml.modeling.lightgbm` namespace, install lightgbm yourself.

Use the following commands to activate your conda environment and install
lightgbm from the Snowflake conda channel.

    
    
    conda activate snowpark-ml
    conda install --override-channels --channel https://repo.anaconda.com/pkgs/snowflake/ lightgbm
    

Copy

Use the following commands to activate your virtual environment and install
lightgbm using `pip`.

    
    
    .venv/bin/activate
    python -m pip install 'snowflake-ml-python[lightgbm]'
    

Copy

Snowflake might add additional optional dependencies from time to time. To
install all optional dependencies using pip:

    
    
    .venv/bin/activate
    python -m pip install 'snowflake-ml-python[all]'
    

Copy

### Setting Up Snowpark Python¶

Snowpark Python is a dependency of `snowflake-ml-python` and is installed
automatically with it. If Snowpark Python is not already set up on your
system, you might need to perform additional configuration steps. See [Setting
Up Your Development Environment for Snowpark Python](../snowpark/python/setup)
for Snowpark Python setup instructions.

## Connecting to Snowflake¶

Before using Snowflake ML features in Python, connect to Snowflake using a
Snowpark `Session` object. Use the `SnowflakeLoginOptions` function in the
`snowflake.ml.utils.connection_params` module to get the configuration
settings to create the session. The function can read the connection settings
from a named connection in your [SnowSQL configuration file](../../user-
guide/snowsql-config) or from environment variables that you set. It returns a
dictionary containing these parameters, which can be used to create a
connection.

The following examples read the connection parameters from the named
connection `myaccount` in the SnowSQL configuration file. To create a Snowpark
Python session, create a builder for the `Session` class, and pass the
connection information to the builder’s `configs` method:

    
    
    from snowflake.snowpark import Session
    from snowflake.ml.utils import connection_params
    
    params = connection_params.SnowflakeLoginOptions("myaccount")
    sp_session = Session.builder.configs(params).create()
    

Copy

You can now pass the session to any that needs it.

Tip

To create a Snowpark Python session from a Snowflake Connector for Python
connection, pass the connection object to the session builder. Here,
`connection` is the Snowflake Connector for Python connection.

    
    
    session = Session.builder.configs({"connection": connection}).create()
    

Copy

### Specifying a Warehouse¶

Many Snowflake ML featues, for example model training or inference, run code
in a Snowflake warehouse. These operations run in the warehouse specified by
the session you use to connect. For example, if you create a session from a
named connection in your [SnowSQL configuration file](../../user-
guide/snowsql-config), you can specify a warehouse using the `warehousename`
parameter in the named configuration.

You can add the warehouse setting when creating the `Session` object, as shown
here, if it does not already exist in the configuration.

    
    
    from snowflake.snowpark import Session
    from snowflake.ml.utils import connection_params
    # Get named connection from SnowQSL configuration file
    params = connection_params.SnowflakeLoginOptions("myaccount")
    # Add warehouse name for model method calls if it's not already present
    if "warehouse" not in params:
        params["warehouse"] = "mlwarehouse"
    sp_session = Session.builder.configs(params).create()
    

Copy

If no warehouse is specified in the session, or if you want to use a different
warehouse, call the session’s `use_warehouse` method to specify a warehouse.

    
    
    sp_session.use_warehouse("mlwarehouse")
    

Copy

## API Reference¶

The [Snowpark ML API reference](https://docs.snowflake.com/developer-
guide/snowpark-ml/reference/latest/index) includes documentation on all
publicly-released functionality. You can also obtain detailed API
documentation for any API by using Python’s `help` function in an interactive
Python session. For example:

    
    
    from snowflake.ml.modeling.preprocessing import OneHotEncoder
    
    help(OneHotEncoder)
    

Copy

