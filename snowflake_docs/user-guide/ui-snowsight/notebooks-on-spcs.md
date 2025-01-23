# Notebooks on Container Runtime for ML¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) [Preview
Feature](../../release-notes/preview-features) — Open

Available to all accounts in [AWS commercial regions](../intro-
regions.html#label-na-general-regions).

## Overview¶

You can run Snowflake Notebooks on Container Runtime for ML. Container Runtime
for ML is powered by Snowpark Container Services, giving you a flexible
container infrastructure that supports building and operationalizing a wide
variety of workflows entirely within Snowflake. Container Runtime for ML
provides software and hardware options to support advanced data science and
machine learning workloads. Compared to [virtual warehouses](../warehouses),
Container Runtime for ML provides a more flexible compute environment where
you can install packages from multiple sources and select compute resources,
including GPU machine types, while still running SQL queries on warehouses for
optimal performance.

This document describes some considerations for using notebooks on [Container
Runtime for ML](../../developer-guide/snowflake-ml/container-runtime-
ml.html#label-container-runtime-for-ml). You can also try the [Getting Started
with Snowflake Notebook Container
Runtime](https://quickstarts.snowflake.com/guide/notebook-container-
runtime/index.html) quickstart to learn more about using the Container Runtime
for ML in your development.

## Prerequisites¶

Before you start using Snowflake Notebooks on Container Runtime for ML, the
ACCOUNTADMIN role must complete the notebook setup steps for creating the
necessary resources and granting privileges to those resources. For detailed
steps, see [Administrator setup](notebooks-setup.html#label-notebooks-setup-
admin).

## Create a notebook on Container Runtime for ML¶

When you create a notebook on Container Runtime for ML, you choose a
warehouse, runtime, and compute pool to provide the resources to run your
notebook. The runtime you choose gives you access to different Python packages
based on your use case. Different warehouse sizes or compute pools have
different cost and performance implications. All of these settings can be
changed later if needed.

Note

A user with the ACCOUNTADMIN, ORGADMIN, or SECURITYADMIN roles cannot directly
create or own a notebook on Container Runtime for ML. Notebooks created or
directly owned by these roles will fail to run. However, if a notebook is
owned by a role that the ACCOUNTADMIN, ORGADMIN, or SECURITYADMIN roles
inherit privileges from, such as the PUBLIC role, then you can use those roles
to run that notebook.

To create a Snowflake Notebook to run on Container Runtime for ML, follow
these steps:

  1. Sign in to Snowsight.

  2. Select Notebooks.

  3. Select \+ Notebook.

  4. Enter a name for your notebook.

  5. Select a database and schema in which to store your notebook. These cannot be changed after you create the notebook.

Note

The database and schema are only required for storing your notebooks. You can
query any database and schema your role has access to from within your
notebook.

  6. Select the Run on container as your Python environment.

  7. Select the Runtime type: CPU or GPU.

  8. Select a Compute pool.

  9. Change the selected warehouse to use to run SQL and Snowpark queries.

  10. To create and open your notebook, select Create.

Runtime:

> This preview provides two types of runtimes: CPU and GPU. Each runtime image
> contains a base set of Python packages and versions verified and integrated
> by Snowflake. All runtime images support data analysis, modeling, and
> training with Snowpark Python, Snowflake ML, and Streamlit.
>
> To install additional packages from a public repo, you can use pip. An
> external access integration (EAI) is required for Snowflake Notebooks to
> install packages from external endpoints. To configure EAIs, see [Set up
> external access for Snowflake Notebooks](notebooks-external-access).
> However, if a package is already part of the base image, then you can’t
> change the version on the package by installing a different version with pip
> install. For a list of the pre-installed packages, see [Container Runtime
> for ML](../../developer-guide/snowflake-ml/container-runtime-ml).

Compute pool:

> A compute pool provides the compute resources for your notebook kernel and
> Python code. Use smaller, CPU-based compute pools to get started, and select
> higher-memory, GPU-based compute pools to optimize for intensive GPU usage
> scenarios like computer vision or LLMs/VLMs.
>
> Note that each compute node is limited to running one notebook per user at a
> time. You should set the MAX_NODES parameter to a value greater than one
> when creating compute pools for notebooks. For an example, see [Compute
> resources](notebooks-setup.html#label-notebooks-create-notebooks-compute).
> For more details on Snowpark Container Services compute pools, see [Snowpark
> Container Services: Working with compute pools](../../developer-
> guide/snowpark-container-services/working-with-compute-pool).
>
> When a notebook is not being used, consider shutting it down to free up node
> resources. You can shut down a notebook by selecting End session in the
> connection dropdown button.

## Run a notebook on Container Runtime for ML¶

After you create your notebook, you can start running code immediately by
adding and running cells. For information about adding cells, see [Develop and
run code in Snowflake Notebooks](notebooks-develop-run).

### Importing more packages¶

In addition to pre-installed packages to get your notebook up and running, you
can install packages from public sources that you have external access set up
for. You can also use packages stored in a stage or a private repository. You
need use the ACCOUNTADMIN role or a role that can create external access
integrations (EAIs) to set up and grant you access for visiting specific
external endpoints. Use the [ALTER NOTEBOOK](../../sql-reference/sql/alter-
notebook) command to enable external access on your notebook. Once granted,
you will see the EAIs in Notebook settings. Toggle the EAIs before you start
installing from external channels. For instructions, see [Create external
access integrations (EAI)](notebooks-external-access.html#label-notebooks-
provision-eai).

The following example installs an external package using pip install in a code
cell:

    
    
    !pip install transformers scipy ftfy accelerate
    

Copy

### Updating notebook settings¶

You can update settings, such as which compute pools or warehouse to use, any
time in Notebook settings, which can be accessed through the [![more actions
for worksheet](../../_images/snowsight-worksheet-vertical-
ellipsis.png)](../../_images/snowsight-worksheet-vertical-ellipsis.png)
**Notebook actions** menu at the top right.

One of the settings you can update in Notebook settings is the idle timeout
setting. The default for idle timeout is 1 hour, and you can set it for up to
72 hours. To set this in SQL, use the [CREATE NOTEBOOK](../../sql-
reference/sql/create-notebook) or [ALTER NOTEBOOK](../../sql-
reference/sql/alter-notebook) command to set the
IDLE_AUTO_SHUTDOWN_TIME_SECONDS property of the notebook.

## Running ML workloads¶

Notebooks on Container Runtime for ML are well suited for running ML workloads
such as model training and parameter tuning. Runtimes come pre-installed with
popular ML packages. Wit external integration access set up, you can install
any other packages you need using `!pip install`.

Note

The Python process caches loaded modules. Change versions of installed
packages before importing the packages in code. Otherwise, you might have to
disconnect and reconnect to the notebook session to load the new versions.

The following examples show how to use some of the available libraries for
your ML workload.

### Use new container-optimized libraries¶

Container Runtime for ML incorporates new APIs tailored specifically for ML
development in the container environment. By distributing the processing
across multiple cores, these APIs offer optimized data loading, model
training, and hyperparameter optimization. Learn more about these APIs in the
[Container Runtime](../../developer-guide/snowflake-ml/container-runtime-ml)
section of the Snowflake ML developer guide.

### Use OSS ML libraries¶

The following example uses an OSS ML library, `xgboost`, with an active
Snowpark session to fetch data directly into memory for training:

    
    
    from snowflake.snowpark.context import get_active_session
    import pandas as pd
    import xgboost as xgb
    from sklearn.model_selection import train_test_split
    
    session = get_active_session()
    df = session.table("my_dataset")
    # Pull data into local memory
    df_pd = df.to_pandas()
    X = df_pd[['feature1', 'feature2']]
    y = df_pd['label']
    # Split data into test and train in memory
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=34)
    # Train in memory
    model = xgb.XGBClassifier()
    model.fit(X_train, y_train)
    # Predict
    y_pred = model.predict(X_test)
    

Copy

### Use Snowflake ML modeling APIs¶

When Snowflake’s ML modeling APIs are used on Container Runtime for ML, all
execution (including training and prediction) happens on the container runtime
directly instead of on the query warehouse. Snowflake ML on Container Runtime
can pull data faster and is recommended for large-scale training. With the GPU
runtime, Snowflake ML will by default use all GPUs to accelerate training.

The following code block example uses XGBoost for modeling:

    
    
    from snowflake.snowpark.context import get_active_session
    from snowflake.ml.modeling.xgboost import XGBClassifier
    from snowflake.ml.modeling.metrics import accuracy_score
    
    session = get_active_session()
    df = session.table("my_dataset")
    feature_cols=['FEATURE1', 'FEATURE2']
    label_col = 'LABEL'
    predicted_col = [PREDICTED_LABEL]
    df = df[features_cols + [label_col]]
    # Split is pushed down to associated warehouse
    train_df, test_df = df.random_split(weights=[0.85, 0.15], seed=34)
    
    model = XGBClassifier(
        input_cols=feature_cols,
        label_cols=label_col,
        output_cols=predicted_col,
        # This will enable leveraging all GPUs on the node
        tree_method="gpu_hist",
    )
    # Train
    model.fit(train_df)
    # Predict
    result = model.predict(test_df)
    
    accuracy = accuracy_score(
    df=result,
    y_true_col_names=label_cols,
    y_pred_col_names=predicted_col)
    

Copy

The following is an example using Light Gradient Boosting Machine (LightGBM):

    
    
    from snowflake.snowpark.context import get_active_session
    from snowflake.ml.modeling.lightgbm import LGBMClassifier
    from snowflake.ml.modeling.metrics import accuracy_score
    
    session = get_active_session()
    df = session.table("my_dataset")
    feature_cols=['FEATURE1', 'FEATURE2']
    label_col = 'LABEL'
    predicted_col = [PREDICTED_LABEL]
    
    df = df[features_cols + [label_col]]
    # Split is pushed down to associated warehouse
    train_df, test_df = df.random_split(weights=[0.85, 0.15], seed=34)
    
    model = LGBMClassifier(
        input_cols=feature_cols,
        label_cols=label_col,
        ouput_cols=predicted_col,
        # This will enable leveraging all GPUs on the node
        device_type="gpu",
    )
    
    # Train
    model.fit(train_df)
    # Predict
    result = model.predict(test_df)
    
    accuracy = accuracy_score(
    df=result,
    y_true_col_names=label_cols,
    y_pred_col_names=predicted_col)
    

Copy

### Use new container-optimized libraries¶

Container Runtime for ML pre-installs new APIs tailored specifically for ML
training in the container environment.

#### Data connector APIs¶

Data connector APIs provide a single interface for connecting Snowflake data
sources (including tables, DataFrames, and Datasets) to popular ML frameworks
(such as PyTorch and TensorFlow). These APIs are found in the
`snowflake.ml.data` namespace.

`snowflake.ml.data.data_connector.DataConnector`

    

Connects Snowpark DataFrames or Snowflake ML Datasets to TensorFlow or PyTorch
DataSets or Pandas DataFrames. Instantiate a connector using one of the
following class methods:

  * `DataConnector.from_dataframe:` Accepts a Snowpark DataFrame.

  * `DataConnector.from_dataset`: Accepts a Snowflake ML Dataset, specified by name and version.

  * `DataConnector.from_sources`: Accepts list of sources, each of which can be a DataFrame or a Dataset.

Once you have instantiated the connector (calling the instance, for example,
`data_connector`), call the following methods to produce the desired kind of
output.

  * `data_connector.to_tf_dataset`: Returns a TensorFlow Dataset suitable for use with TensorFlow.

  * `data_connector.to_torch_dataset`: Returns a PyTorch Dataset suitable for use with PyTorch.

For more information on these APIs, see the [Snowflake ML API
reference](/developer-guide/snowpark-ml/reference/latest/data).

#### Distributed modeling APIs¶

Distributed modeling APIs provide parallel versions of LightGBM, PyTorch, and
XGBoost that take full advantage of the available resources in the container
environment. These are found in the `snowflake.ml.modeling.distributors`
namespace. The APIs of the distributed classes are similar to those of the
standard versions.

For more information on these APIs, see the [API reference](/developer-
guide/snowpark-ml/reference/latest/distributors).

XGBoost

    

The primary XGBoost class is
`snowflake.ml.modeling.distributors.xgboost.XGBEstimator`. Related classes
include:

  * `snowflake.ml.modeling.distributors.xgboost.XGBScalingConfig`

For an example of working with this API, see the [XGBoost on
GPU](https://github.com/Snowflake-Labs/sfguide-getting-started-with-container-
runtime-apis/blob/main/XGBoost_on_GPU_Quickstart.ipynb) example notebook in
the Snowflake Container Runtime for ML GitHub repository.

LightGBM

    

The primary LightGBM class is
`snowflake.ml.modeling.distributors.lightgbm.LightGBMEstimator`. Related
classes include:

  * `snowflake.ml.modeling.distributors.lightgbm.LightGBMScalingConfig`

For an example of working with this API, see the [LightGBM on
GPU](https://github.com/Snowflake-Labs/sfguide-getting-started-with-container-
runtime-apis/blob/main/LightGBM_on_GPU_Quickstart.ipynb) example notebook in
the Snowflake Container Runtime for ML GitHub repository.

PyTorch

    

The primary PyTorch class is
`snowflake.ml.modeling.distributors.pytorch.PyTorchDistributor`. Related
classes include:

  * `snowflake.ml.modeling.distributors.pytorch.WorkerResourceConfig`

  * `snowflake.ml.modeling.distributors.pytorch.PyTorchScalingConfig`

  * `snowflake.ml.modeling.distributors.pytorch.Context`

  * `snowflake.ml.modeling.distributors.pytorch.get_context`

For an example of working with this API, see the [PyTorch on
GPU](https://github.com/Snowflake-Labs/sfguide-getting-started-with-container-
runtime-apis/blob/main/PyTorch_on_GPU_Quickstart.ipynb) example notebook in
the Snowflake Container Runtime for ML GitHub repository.

### Limitations¶

  * The Snowflake ML Modeling API supports only `predict`, `predict_proba`, `predict_log_proba` inference methods on Container Runtime for ML. Other methods run in the query warehouse.

  * Snowflake ML Modeling API supports only `sklearn` compatible pipelines on the Container Runtime.

  * Snowflake ML Modeling API does not support `preprocessing` or `metrics` classes on Container Runtime for ML. These run in the query warehouse.

  * The `fit`, `predict`, and `score` methods are executed on Container Runtime for ML. Other Snowflake ML methods run in the query warehouse.

  * `sample_weight_cols` is not supported for XGBoost or LightGBM models.

## Cost/billing considerations¶

When running notebooks on Container Runtime for ML, you may incur both
[warehouse compute](../cost-understanding-compute) and [SPCS compute
costs](../../developer-guide/snowpark-container-services/accounts-orgs-usage-
views).

Snowflake Notebooks require a virtual warehouse to run SQL and Snowpark
queries for optimized performance. Therefore, you might also incur virtual
warehouse compute costs if you use SQL in SQL cells and Snowpark push-down
queries executed in Python cells. The following diagram shows where compute
happens for each type of cell.

[![Diagram showing the compute distribution of notebook
cells.](../../_images/notebook-compute-diagram.png)](../../_images/notebook-
compute-diagram.png)

For example, the following Python example uses the
[xgboost](https://xgboost.readthedocs.io/en/stable/) library. The data is
pulled into the container and compute occurs on Snowpark Container Services:

    
    
    from snowflake.snowpark.context import get_active_session
    import pandas as pd
    import xgboost as xgb
    from sklearn.model_selection import train_test_split
    
    session = get_active_session()
    df = session.table("my_dataset")
    # Pull data into local memory
    df_pd = df.to_pandas()
    X = df_pd[['feature1', 'feature2']]
    y = df_pd['label']
    # Split data into test and train in memory
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=34)
    

Copy

To learn more about warehouse costs, see [Overview of
warehouses](../warehouses-overview).

