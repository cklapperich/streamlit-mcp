# Snowflake Datasets¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) [Preview
Feature](../../release-notes/preview-features) — Open

Snowflake Datasets are available in the Snowpark ML Python package
(`snowflake-ml-python`) v1.5.0 and later.

Datasets are new Snowflake schema-level objects specially designed for machine
learning workflows. Snowflake Datasets hold collections of data organized into
versions, where each version holds a materialized snapshot of your data with
guaranteed immutability, efficient data access, and interoperability with
popular deep learning frameworks.

Note

Although Datasets are SQL objects, they are intended for use exclusively with
Snowpark ML. They do not appear in the Snowsight database object explorer, and
you do not use SQL commands to work with them.

You should use Snowflake Datasets in these situations:

  * You need to manage and version large datasets for reproducible machine learning model training and testing.

  * You want to leverage Snowflake’s scalable and secure data storage and processing capabilities.

  * You need fine-grained file-level access and/or data shuffling for distributed training or data streaming.

  * You need to integrate with external machine learning frameworks and tools.

Note

Materialized datasets incur storage costs. To minimize these costs, delete
unused datasets.

## Installation¶

The Dataset Python SDK is included in Snowpark ML (Python package `snowflake-
ml-python`) starting in version 1.5.0. For installation instructions, see
[Using Snowflake ML Locally](snowpark-ml.html#label-snowpark-ml-get-started).

## Required privileges¶

Creating Datasets requires the CREATE DATASET schema-level privilege.
Modifying Datasets, for example adding or deleting dataset versions, requires
OWNERSHIP on the Dataset. Reading from a Dataset requires only the USAGE
privilege on the Dataset (or OWNERSHIP). For more information about granting
privileges in Snowflake, see [GRANT <privileges>](../../sql-
reference/sql/grant-privilege).

Tip

Setting up privileges for the Snowflake Feature Store using either the
`setup_feature_store` method or the [privilege setup SQL script](feature-
store/rbac) also sets up Dataset privileges. If you have already set up
feature store privileges by one of these methods, no further action is needed.

## Creating and using Datasets¶

Datasets are created by passing a Snowpark DataFrame to the
`snowflake.ml.dataset.create_from_dataframe` function.

    
    
    from snowflake import snowpark
    from snowflake.ml import dataset
    
    # Create Snowpark Session
    # See https://docs.snowflake.com/en/developer-guide/snowpark/python/creating-session
    session = snowpark.Session.builder.configs(connection_parameters).create()
    
    # Create a Snowpark DataFrame to serve as a data source
    # In this example, we generate a random table with 100 rows and 1 column
    df = session.sql(
        "select uniform(0, 10, random(1)) as x, uniform(0, 10, random(2)) as y from table(generator(rowcount => 100))"
    )
    
    # Materialize DataFrame contents into a Dataset
    ds1 = dataset.create_from_dataframe(
        session,
        "my_dataset",
        "version1",
        input_dataframe=df)
    

Copy

Datasets are versioned. Each version is an immutable, point-in-time snapshot
of the data managed by the Dataset. The Python API includes a
`Dataset.selected_version` property that indicates whether a given dataset is
selected for use. This property is automatically set by the
`dataset.create_from_dataframe` and `dataset.load_dataset` factory methods, so
creating a dataset automatically selects the created version. The
`Dataset.select_version` and `Dataset.create_version` methods can also be used
to explicitly switch between versions. Reading from a Dataset reads from the
active selected version.

    
    
    # Inspect currently selected version
    print(ds1.selected_version) # DatasetVersion(dataset='my_dataset', version='version1')
    print(ds1.selected_version.created_on) # Prints creation timestamp
    
    # List all versions in the Dataset
    print(ds1.list_versions()) # ["version1"]
    
    # Create a new version
    ds2 = ds1.create_version("version2", df)
    print(ds1.selected_version.name)  # "version1"
    print(ds2.selected_version.name)  # "version2"
    print(ds1.list_versions())        # ["version1", "version2"]
    
    # selected_version is immutable, meaning switching versions with
    # ds1.select_version() returns a new Dataset object without
    # affecting ds1.selected_version
    ds3 = ds1.select_version("version2")
    print(ds1.selected_version.name)  # "version1"
    print(ds3.selected_version.name)  # "version2"
    

Copy

## Reading data from Datasets¶

Dataset version data is stored as evenly sized files in the Apache Parquet
format. The `Dataset` class provides an API similar to that of
[FileSet](filesystem-fileset) for reading data from Snowflake Datasets,
including built-in connectors for TensorFlow and PyTorch. The API is
extensible to support custom framework connectors.

Reading from a Dataset requires an active selected version.

### Connect to TensorFlow¶

Datasets can be converted to TensorFlow’s `tf.data.Dataset` and streamed in
batches for efficient training and evaluation.

    
    
    import tensorflow as tf
    
    # Convert Snowflake Dataset to TensorFlow Dataset
    tf_dataset = ds1.read.to_tf_dataset(batch_size=32)
    
    # Train a TensorFlow model
    for batch in tf_dataset:
        # Extract and build tensors as needed
        input_tensor = tf.stack(list(batch.values()), axis=-1)
    
        # Forward pass (details not included for brevity)
        outputs = model(input_tensor)
    

Copy

### Connect to PyTorch¶

Datasets also support conversion to PyTorch DataPipes and can be streamed in
batches for efficient training and evaluation.

    
    
    import torch
    
    # Convert Snowflake Dataset to PyTorch DataPipe
    pt_datapipe = ds1.read.to_torch_datapipe(batch_size=32)
    
    # Train a PyTorch model
    for batch in pt_datapipe:
        # Extract and build tensors as needed
        input_tensor = torch.stack([torch.from_numpy(v) for v in batch.values()], dim=-1)
    
        # Forward pass (details not included for brevity)
        outputs = model(input_tensor)
    

Copy

### Connect to Snowpark ML¶

Datasets can also be converted back to Snowpark DataFrames for integration
with Snowpark ML Modeling. The converted Snowpark DataFrame is not the same as
the DataFrame that was provided during Dataset creation, but instead points to
the materialized data in the Dataset version.

    
    
    from snowflake.ml.modeling.ensemble import random_forest_regressor
    
    # Get a Snowpark DataFrame
    ds_df = ds1.read.to_snowpark_dataframe()
    
    # Note ds_df != df
    ds_df.explain()
    df.explain()
    
    # Train a model in Snowpark ML
    xgboost_model = random_forest_regressor.RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        input_cols=["X"],
        label_cols=["Y"],
    )
    xgboost_model.fit(ds_df)
    

Copy

### Direct file access¶

The Dataset API also exposes an [fsspec](https://filesystem-
spec.readthedocs.io/en/latest/) interface, which can be used to build custom
integrations with external libraries like PyArrow, Dask, or any other package
that supports `fsspec` and allows distributed and/or stream-based model
training.

    
    
    print(ds1.read.files()) # ['snow://dataset/my_dataset/versions/version1/data_0_0_0.snappy.parquet']
    
    import pyarrow.parquet as pq
    pd_ds = pq.ParquetDataset(ds1.read.files(), filesystem=ds1.read.filesystem())
    
    import dask.dataframe as dd
    dd_df = dd.read_parquet(ds1.read.files(), filesystem=ds1.read.filesystem())
    

Copy

## Current limitations and known issues¶

  * Dataset names are SQL identifiers and subject to [Snowflake identifier requirements](../../sql-reference/identifiers-syntax).

  * Dataset versions are strings and have a maximum length of 128 characters. Some characters are not permitted and will produce an error message.

  * Certain query operations on Datasets with wide schemas (more than about 4,000 columns) are not fully optimized. This should improve in upcoming releases.

