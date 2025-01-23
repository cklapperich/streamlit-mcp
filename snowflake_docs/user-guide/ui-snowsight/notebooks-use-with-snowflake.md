# Experience Snowflake with notebooks¶

Feature — Generally Available

Generally available in Amazon Web Services (AWS), Microsoft Azure, and Google
Cloud Platform (GCP) commercial regions.

Snowflake Notebooks is a development environment that you can use with other
Snowflake features. This topic shows how to leverage other Snowflake features
within notebooks.

## Snowpark Python in notebooks¶

The [Snowpark library](../../developer-guide/snowpark/index) provides an
intuitive API for querying and processing data in a data pipeline. Using the
Snowpark library, you can build applications that process data in Snowflake
without moving data to the system where your application code runs. You can
also automate data transformation and processing by writing stored procedures
and scheduling those procedures as tasks in Snowflake.

You can use Snowpark to query and process data at scale in Snowflake by
writing Snowpark code in a Python cell of your notebook.

### Example usage¶

Snowpark Python comes pre-installed in the Snowflake Notebooks environment.
The following example uses the Snowpark library in a notebook to read in a CSV
file and a Snowflake table and display its contents as output.

  1. In your notebook, add a Python cell, either using a [keyboard shortcut](notebooks-keyboard-shortcuts.html#label-notebooks-keyboard-shortcuts) or by selecting \+ Python. Snowflake Notebooks and Snowpark both support Python 3.9.

  2. Set up a Snowpark session. In notebooks, the session context variable is preconfigured. You can use the `get_active_session` method to get the session context variable:

> >     from snowflake.snowpark.context import get_active_session
>     session = get_active_session()
>  
>
> Copy

  3. Use Snowpark to load a CSV file into a Snowpark DataFrame from a stage location. This example uses a stage called `tastybyte_stage`.

> >     df =
> session.read.options({"infer_schema":True}).csv('@TASTYBYTE_STAGE/app_order.csv')
>  
>
> Copy

  4. Load an existing Snowflake table, `app_order`, into the Snowpark DataFrame.

> >     df = session.table("APP_ORDER")
>  
>
> Copy

  5. Display the Snowpark DataFrame.

> >     df
>  
>
> Copy

Note

Outside of the Snowflake Notebooks environment, you must call `df.show()` to
print out the DataFrame. In Snowflake Notebooks, DataFrames are evaluated
eagerly when `df` is printed out. The DataFrame is printed out as an
interactive Streamlit DataFrame display (st.dataframe). DataFrames output is
limited to 10,000 rows or 8 MB, whichever is lower.

### Snowpark limitations¶

  * A Snowflake Notebook creates a Snowpark session, so you can use most of the methods available in a Snowpark session class. However, because a notebook runs inside Snowflake rather than in your local development environment, you cannot use the following methods:

>     * session.add_import
>
>     * session.add_packages
>
>     * session.add_requirements

  * Some Snowpark Python operations don’t work with SPROCs. For a complete list of operations, see [Python stored procedure limitations](../../developer-guide/stored-procedure/python/procedure-python-limitations).

Tip

View more examples of notebooks that use Snowpark:

  * [Data Engineering Pipelines with Snowpark Python](https://github.com/Snowflake-Labs/snowflake-demo-notebooks/blob/main/Data%20Engineering%20Pipelines%20with%20Snowpark%20Python/Data%20Engineering%20Pipelines%20with%20Snowpark%20Python.ipynb)

  * [Adding CSV files notebook](https://github.com/Snowflake-Labs/snowflake-demo-notebooks/blob/main/Load%20CSV%20from%20S3/Load%20CSV%20from%20S3.ipynb)

Note

These quickstarts are only shown as examples. Following along with the example
may require additional rights to third-party data, products, or services that
are not owned or provided by Snowflake. Snowflake does not guarantee the
accuracy of these examples.

## Streamlit in notebooks¶

[Streamlit](../../developer-guide/streamlit/about-streamlit) is an open-source
Python library that makes it easy to create and share custom web apps for
machine learning and data science. You can build interactive data applications
with Streamlit directly in your notebook. You can test and develop your app
directly in a notebook. Streamlit comes preinstalled in notebooks, so you can
start quickly.

### Example usage¶

Streamlit comes pre-installed with the Snowflake Notebooks environment. The
example in this section creates an interactive data app using Streamlit.

  1. Import necessary libraries

> >     import streamlit as st
>     import pandas as pd
>  
>
> Copy

  2. First create some sample data for the app.

> >     species = ["setosa"] * 3 + ["versicolor"] * 3 + ["virginica"] * 3
>     measurements = ["sepal_length", "sepal_width", "petal_length"] * 3
>     values = [5.1, 3.5, 1.4, 6.2, 2.9, 4.3, 7.3, 3.0, 6.3]
>     df = pd.DataFrame({"species": species,"measurement":
> measurements,"value": values})
>     df
>  
>
> Copy

  3. Set up your interactive slider from the Streamlit library.

> >     st.markdown("""# Interactive Filtering with Streamlit! :balloon:
>                 Values will automatically cascade down the notebook
> cells""")
>     value = st.slider("Move the slider to change the filter value 👇",
> df.value.min(), df.value.max(), df.value.mean(), step = 0.3 )
>  
>
> Copy

  4. Finally, display a filtered table based on the slider value.

> >     df[df["value"]>value].sort_values("value")
>  
>
> Copy

You can interact with the app in real time from the notebook. See the filtered
table change based on the value you set on the slider.

Tip

For the complete example, see the interactive data app section of the [Visual
Data Stories with Snowflake Notebooks](https://github.com/Snowflake-
Labs/snowflake-demo-
notebooks/blob/main/Visual%20Data%20Stories%20with%20Snowflake%20Notebooks/Visual%20Data%20Stories%20with%20Snowflake%20Notebooks.ipynb)
notebook.

### Streamlit support in Notebooks¶

When you use the [st.map](https://docs.streamlit.io/develop/api-
reference/charts/st.map) or
[st.pydeck_chart](https://docs.streamlit.io/develop/api-
reference/charts/st.pydeck_chart) Streamlit commands, Mapbox provides the map
tiles when rendering map content. Mapbox is a third-party application and is
subject to Snowflake’s [External Offerings
Terms](https://www.snowflake.com/legal/external-offering-terms/).

The following Streamlit elements are not supported in Notebooks:

  * [st.bokeh_chart](https://docs.streamlit.io/1.39.0/develop/api-reference/charts/st.bokeh_chart)

  * [st.camera_input](https://docs.streamlit.io/1.39.0/develop/api-reference/widgets/st.camera_input)

  * [st.feedback](https://docs.streamlit.io/1.39.0/develop/api-reference/widgets/st.feedback)

  * [st.file_uploader](https://docs.streamlit.io/1.39.0/develop/api-reference/widgets/st.file_uploader)

  * [st.set_page_config](https://docs.streamlit.io/1.39.0/develop/api-reference/configuration/st.set_page_config)

> The `page_title`, `page_icon`, and `menu_items` properties of the
> `st.set_page_config` command are not supported.

  * [st.experimental_audio_input](https://docs.streamlit.io/1.39.0/develop/api-reference/widgets/st.audio_input)

  * [st.experimental_get_query_params](https://docs.streamlit.io/1.39.0/develop/api-reference/caching-and-state/st.experimental_get_query_params)

  * [st.experimental_set_query_params](https://docs.streamlit.io/1.39.0/develop/api-reference/caching-and-state/st.experimental_set_query_params)

  * [st.components.v1.iframe](https://docs.streamlit.io/1.39.0/develop/api-reference/custom-components/st.components.v1.iframe)

  * [st.components.v1.declare_component](https://docs.streamlit.io/1.39.0/develop/api-reference/custom-components/st.components.v1.declare_component)

  * Anchor links

  * Material icons in [Markdown](https://docs.streamlit.io/1.39.0/develop/api-reference/text/st.markdown)

## Snowpark ML in Notebooks¶

[Snowpark ML](../../developer-guide/snowflake-ml/snowpark-ml) is the Python
library that provides the APIs for [Snowflake ML](../../developer-
guide/snowflake-ml/overview) and for custom machine learning model development
in Snowflake. Using Snowpark ML, you can develop custom models using APIs
based on popular ML frameworks, define automatically updated features to train
them, and store them in a model registry for easy discovery and reuse.

Container Runtime for ML provides software and hardware options to support
advanced data science and machine learning workloads. For details on container
runtime, see [Notebooks on Container Runtime for ML](notebooks-on-spcs).

Important

The `snowflake-ml-python` package and its dependencies must be allowed by your
organization’s [package policy](../../developer-guide/udf/python/packages-
policy).

### Example usage¶

To use Snowpark ML, install the `snowflake-ml-python` library for your
notebook:

  1. From the notebook, select Packages.

  2. Locate the snowflake-ml-python library and select the library to install it.

Here is an example of how you can use the Snowpark ML library for
preprocessing your data:

    
    
    import snowflake.ml.modeling.preprocessing as pp
    
    # Initialize a StandardScaler object with input and output column names
    scaler = pp.StandardScaler(
        input_cols=feature_names_input,
        output_cols=feature_names_input
    )
    
    # Fit the scaler to the dataset
    scaler.fit(upsampled_data)
    
    # Transform the dataset using the fitted scaler
    scaled_features = scaler.transform(upsampled_data)
    scaled_features
    

Copy

Here is an example of how you can use the Snowpark ML library for model
training and inference:

    
    
    from snowflake.ml.modeling.ensemble import RandomForestClassifier
    
    # Initialize a RandomForestClassifier object with input, label, and output column names
    model = RandomForestClassifier(
        input_cols=feature_names_input,
        label_cols=label,
        output_cols=output_label,
    )
    
    # Train the RandomForestClassifier model using the training set
    model.fit(training)
    
    # Predict the target variable for the testing set using the trained model
    results = model.predict(testing)
    

Copy

Tip

For more examples of using Snowpark ML, see the following notebooks:

    

  * [Telco Churn Data Analysis and Modeling](https://github.com/Snowflake-Labs/snowflake-demo-notebooks/blob/main/Telco%20Churn%20Data%20Analysis/Telco%20Churn%20Data%20Analysis.ipynbb)

  * [End-to-End Machine Learning with Snowpark ML](https://github.com/Snowflake-Labs/snowflake-demo-notebooks/blob/main/End-to-End%20Machine%20Learning%20with%20Snowpark%20ML/3_sf_nb_snowpark_ml_model_training_inference.ipynb)

## Snowflake ML Registry in Notebooks¶

The [Snowflake Model Registry](../../developer-guide/snowflake-ml/model-
registry/overview) allows you to securely manage models and your metadata in
Snowflake, regardless of origin. The model registry stores machine learning
models as first-class schema-level objects in Snowflake so they can easily be
found and used by others in your organization. You can create registries, and
store models in them, using classes in the Snowpark ML library. Models can
have multiple versions, and you can designate a version as the default.

### Example usage¶

To use the Snowflake ML registry, install the `snowflake-ml-python` library
for your notebook:

  1. From your notebook, select Packages at the top.

  2. Search for the snowflake-ml-python package and select the library to install it.

Here is an example of how you can use the Snowflake ML Registry to log a
model:

    
    
    from snowflake.ml.registry import Registry
    # Create a registry and log the model
    native_registry = Registry(session=session, database_name=db, schema_name=schema)
    
    # Let's first log the very first model we trained
    model_ver = native_registry.log_model(
        model_name=model_name,
        version_name='V0',
        model=regressor,
        sample_input_data=X, # to provide the feature schema
    )
    
    # Add evaluation metric
    model_ver.set_metric(metric_name="mean_abs_pct_err", value=mape)
    
    # Add a description
    model_ver.comment = "This is the first iteration of our Diamonds Price Prediction model. It is used for demo purposes."
    
    # Show Models
    native_registry.get_model(model_name).show_versions()
    

Copy

Tip

View this [end-to-end example](https://www.youtube.com/watch?v=LeSGBW0YoLg) of
how to use Snowflake ML Registry.

## pandas on Snowflake in notebooks¶

[pandas on Snowflake](../../developer-guide/snowpark/python/pandas-on-
snowflake) lets you run your pandas code in a distributed manner directly on
your data in Snowflake. Just by changing the import statement and a few lines
of code, you can get the same familiar pandas-native experience with the
scalability and security benefits of Snowflake.

With pandas on Snowflake, you can work with much larger datasets and avoid the
time and expense of porting your pandas pipelines to other big data frameworks
or provisioning large and expensive machines. It runs workloads natively in
Snowflake through transpilation to SQL, enabling it to take advantage of
parallelization and the data governance and security benefits of Snowflake.

pandas on Snowflake is delivered through the Snowpark pandas API as part of
the Snowpark Python library, which enables scalable data processing of Python
code within the Snowflake platform.

### Example usage¶

Snowpark pandas is available in Snowpark Python version 1.17 and later.
Snowpark Python comes pre-installed with the Snowflake Notebooks environment.

  1. To install Modin, select `modin` from Packages and ensure that the version is 0.28.1 or later.

  2. To set the pandas version, select `pandas` from Packages and ensure that the version is 2.2.1.

In a Python cell, import Snowpark Python and Modin:

>
>     import modin.pandas as pd
>     import snowflake.snowpark.modin.plugin
>  
>
> Copy

  1. Create a Snowpark session:
    
        from snowflake.snowpark.context import get_active_session
    session = get_active_session()
    

Copy

  2. Start using the Snowpark Python API:
    
        # Create a Snowpark Pandas DataFrame with sample data.
    df = pd.DataFrame([[1, 'Big Bear', 8],[2, 'Big Bear', 10],[3, 'Big Bear', None],
                        [1, 'Tahoe', 3],[2, 'Tahoe', None],[3, 'Tahoe', 13],
                        [1, 'Whistler', None],['Friday', 'Whistler', 40],[3, 'Whistler', 25]],
                        columns=["DAY", "LOCATION", "SNOWFALL"])
    # Drop rows with null values.
    df.dropna()
    # Compute the average daily snowfall across locations.
    df.groupby("LOCATION").mean()["SNOWFALL"]
    

Copy

Tip

For more examples of how to use pandas on Snowflake, see [Getting Started with
pandas on
Snowflake](https://quickstarts.snowflake.com/guide/getting_started_with_pandas_on_snowflake/#0).

## Snowflake Python API in Notebooks¶

The [Snowflake Python API](../../developer-guide/snowflake-python-
api/snowflake-python-overview) is a unified library that seamlessly connects
Python with Snowflake workloads. It is intended to provide comprehensive APIs
for interacting with Snowflake resources across data engineering, Snowpark,
Snowpark ML, and application workloads using a first-class Python API.

You can use the Snowflake Python API to manage Snowflake resources by
creating, deleting, or modifying them, and more. You can use Python to perform
tasks you might otherwise perform with [Snowflake SQL commands](../../sql-
reference-commands).

In Notebooks, the session context variable is preconfigured. You can use the
`get_active_session` method to get the session context variable:

>
>     from snowflake.snowpark.context import get_active_session
>     session = get_active_session()
>  
>
> Copy

Create a `Root` object from which to use the Snowflake Python API:

>
>     from snowflake.core import Root
>     api_root = Root(session)
>  
>
> Copy

Here is an example of how you can create a database and schema using the
Python API:

>
>     # Create a database and schema by running the following cell in the
> notebook:
>     database_ref = api_root.databases.create(Database(name="demo_database"),
> mode="orreplace")
>     schema_ref = database_ref.schemas.create(Schema(name="demo_schema"),
> mode="orreplace")
>  
>
> Copy
>
> Tip
>
> For a more detailed example of how to use Snowflake’s Python API, see the
> [Creating Snowflake object using Python API notebook
> example](https://github.com/Snowflake-Labs/snowflake-demo-
> notebooks/blob/main/Creating%20Snowflake%20Object%20using%20Python%20API/Creating%20Snowflake%20Object%20using%20Python%20API.ipynb)
> on Github.

