# Snowflake Model Registry¶

Note

The model registry API described in this topic is generally available as of
package version 1.5.0.

The Snowflake Model Registry lets you securely manage models and their
metadata in Snowflake, regardless of origin. The model registry stores machine
learning models as first-class schema-level objects in Snowflake so they can
easily be found and used by others in your organization. You can create
registries and store models in them using Python classes in the Snowpark ML
library. Models can have multiple versions, and you can designate a version as
the default.

After you have stored a model, you can invoke its methods (equivalent to
functions or stored procedures) to perform model operations, such as
inference, in a Snowflake [virtual warehouse](../../../user-guide/warehouses).

Tip

For an example of an end-to-end workflow in Snowpark ML, including the
Snowflake Model Registry, see [Introduction to Machine Learning with Snowpark
ML](https://quickstarts.snowflake.com/guide/intro_to_machine_learning_with_snowpark_ml_for_python/#0).

If you have models in Microsoft Azure Machine Learning or in Amazon SageMaker,
see [Deploying Models from Azure ML and SageMaker to Snowpark
ML](https://quickstarts.snowflake.com/guide/deploying_models_from_azureml_and_sagemaker_to_snowparkml/index.html?index=..%2F..index#0).

The most important classes in the Snowflake Model Registry Python API are:

  * [snowflake.ml.registry.Registry](https://docs.snowflake.com/en/developer-guide/snowpark-ml/reference/latest/api/registry/snowflake.ml.registry.Registry): Manages models within a schema.

  * [snowflake.ml.model.Model](https://docs.snowflake.com/en/developer-guide/snowpark-ml/reference/latest/api/model/snowflake.ml.model.Model): Represents a model.

  * [snowflake.ml.model.ModelVersion](https://docs.snowflake.com/en/developer-guide/snowpark-ml/reference/latest/api/model/snowflake.ml.model.ModelVersion): Represents a version of a model.

The Snowflake Model Registry supports the following types of models:

  * [Snowpark ML Modeling](../modeling)

  * scikit-learn

  * XGBoost

  * LightGBM

  * CatBoost

  * PyTorch

  * TensorFlow

  * MLFlow PyFunc

  * Sentence Transformer

  * Hugging Face pipeline

  * Other types of models via the `snowflake.ml.model.CustomModel` class (see [Storing Custom Models in the Snowflake Model Registry](custom-models))

This topic describes how to perform registry operations in Python using
Snowpark ML. You can also perform many registry operations in SQL; see [Model
commands](../../../sql-reference/commands-model).

## Required privileges¶

To create a model, you must either own the schema where the model is created
or have the CREATE MODEL privilege on it. To use a model, you must either own
the model or have the USAGE privilege on it. The USAGE privilege allows
grantees to use the model for inference without being able to see any of its
internals.

If a user’s role has USAGE on a model, it appears in [Snowsight’s model
registry page](snowsight-ui). For details, see [Access control
privileges](../../../user-guide/security-access-control-privileges).

Note

Models currently do not support replication.

## Current limitations and issues¶

The Snowflake Model Registry currently has the following limitations:

  * The registry cannot be used in [Snowflake Native Apps](../../native-apps/native-apps-about).

  * Models cannot be shared or cloned and are skipped during replication.

Versions 1.5.0 and 1.5.1 of the `snowflake-ml-python` package have the
following known issues. Until these are addressed, use the provided
workaround.

  * In Snowflake release 8.23 and earlier, the library does not work in [owner’s rights stored procedures](../../stored-procedure/stored-procedures-rights.html#label-stored-procedure-session-state-owners). Use caller’s rights stored procedures instead.

  * In stored procedures, logging a model requires embedding a copy of the local Snowpark ML library in the model. Specify the `embed_local_ml_library` option in the `log_model` call as shown:
    
        registry.log_model(..., options={"embed_local_ml_library": True, ...})
    

Copy

The following limits apply to models and model versions:

Models | 

  * Maximum of 1000 versions

  
---|---  
Model versions | 

  * Maximum of 10 methods
  * Maximum of 10 imports
  * Maximum of 500 arguments per method
  * Maximum metadata (including metrics) of 100 KB
  * Maximum total model size of 5 GB
  * Maximum config file size of 250 KB, including `conda.yml` and other manifest files that `log_model` generates internally. (If a model has many functions and all of them have many arguments, for example, this limit might be exceeded.)

  
  
## Opening the Snowflake Model Registry¶

Models are first-class Snowflake objects and can be organized within a
database and schema along with other Snowflake objects. The Snowflake Model
Registry provides a Python class for managing models within a schema. Thus,
any Snowflake schema can be used as a registry. It is not necessary to
initialize or otherwise prepare a schema for this purpose. Snowflake
recommends creating one or more dedicated schemas for this purpose, such as
ML.REGISTRY. You can create the schema using [CREATE SCHEMA](../../../sql-
reference/sql/create-schema).

Before you can create or modify models in the registry, you must open the
registry. Opening the registry returns a reference to it, which you can then
use to add new models and obtain references to existing models.

    
    
    from snowflake.ml.registry import Registry
    
    reg = Registry(session=sp_session, database_name="ML", schema_name="REGISTRY")
    

Copy

## Registering models and versions¶

Adding a model to the registry is called _logging_ the model. Log a model by
calling the registry’s `log_model` method. This method serializes the model —
a Python object — and creates a Snowflake model object from it. This method
also adds metadata, such as a description, to the model as specified in the
`log_model` call.

Each model can have unlimited versions. To log additional versions of the
model, call `log_model` again with the same `model_name` but a different
`version_name`.

You cannot add tags to a model when it is added to the registry, because tags
are attributes of the model, and `log_model` adds a specific model version,
only creating a model when adding its first version. You can update the
model’s tags after logging the first version of the model.

In the following example, `clf`, short for “classifier,” is the Python model
object, which was already created elsewhere in your code. You can add a
comment at registration time, as shown here. The combination of name and
version must be unique in the schema. You may specify `conda_dependencies`
lists; the specified packages will be deployed with the model.

    
    
    mv = reg.log_model(clf,
                       model_name="my_model",
                       version_name="v1",
                       conda_dependencies=["scikit-learn"],
                       comment="My awesome ML model",
                       metrics={"score": 96},
                       sample_input_data=train_features,
                       task=type_hints.Task.TABULAR_BINARY_CLASSIFICATION)
    

Copy

The arguments of `log_model` are described here.

**Required arguments**

Argument | Description  
---|---  
`model` | The Python model object of a supported model type. Must be serializable (“pickleable”).  
`model_name` | The model’s name, used with `version_name` to identify the model in the registry. The name cannot be changed after the model is logged. Must be a [valid Snowflake identifier](../../../sql-reference/identifiers-syntax).  
  
Note

The combination of model name and version must be unique in the schema.

**Optional arguments**

Argument | Description  
---|---  
`version_name` | String specifying the model’s version, used with `model_name` to identify the model in the registry. Must be a [valid Snowflake identifier](../../../sql-reference/identifiers-syntax). If missing, a human-readable version name is generated automatically.  
`code_paths` | List of paths to directories of code to import when loading or deploying the model.  
`comment` | Comment, for example a description of the model.  
`conda_dependencies` | List of Conda packages required by your model. This argument specifies package names and optional versions in [Conda format](https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/pkg-search.html), that is, `"[channel::]package [operator version]"`. If you do not specify a channel, the Snowflake channel is assumed.  
`ext_modules` | List of external modules to pickle with the model. Supported with scikit-learn, Snowpark ML, PyTorch, TorchScript, and custom models.  
`metrics` | Dictionary that contains metrics linked to the model version.  
`options` | Dictionary that contains options for model creation. The following options are available for all model types:

  * `embed_local_ml_library`: whether to embed a copy of the local Snowpark ML library into the model. Default: `False`.
  * `relax_version`: whether to relax the version constraints of the dependencies. This replaces version specifiers like `==x.y.z` with specifiers like `<=x.y, <(x+1)`. Default: `True`.
  * `method_options`: A dictionary of per-method options, where the key is the name of a method and the value is a dictionary that contains one or more of the options described here. The available options are:
    * `case_sensitive`: Indicates whether the method and its signature are case-sensitive. Case-sensitive methods must be double-quoted when used in SQL. This option also allows non-alphabetic characters in method names. Default: `False`.
    * `max_batch_size`: Maximum batch size that the method will accept when called in the warehouse. Default: `None` (the batch size is automatically determined).

Individual model types may support additional options. See Notes on specific
model types.  
`pip_requirements` | List of package specs for PyPI packages required by your model.  
`python_version` | The version of Python in which the model will run. Defaults to `None`, which designates the latest version available in the warehouse.  
`sample_input_data` | A DataFrame that contains sample input data. The feature names required by the model and their types are extracted from this DataFrame. Either this argument or `signatures` must be provided for all models except Snowpark ML and MLFlow models and Hugging Face pipelines.  
`signatures` | Model method signatures as a mapping from target method name to signatures of input and output. Either this argument or `sample_input_data` must be provided for all models except Snowpark ML and MLFlow models and Hugging Face pipelines.  
`task` | The task defining the problem the model is meant to solve. If unspecified, best effort is made to infer the model task from the model class or it is set to `type_hints.Task.UNKNOWN`. Check `snowflake.ml.model.type_hints` for all task options.  
  
`log_model` returns a `snowflake.ml.model.ModelVersion` object, which
represents the version of the model that was added to the registry.

After registration, the model itself cannot be modified (although you can
change its metadata). To delete a model and all its versions, use the
registry’s delete_model method.

## Working with model artifacts¶

After a model has been logged, its artifacts (the files backing the model,
including its serialized Python objects and various metadata files such as its
manifest) are available on an internal stage. Artifacts cannot be modified,
but you can view or download the artifacts of models you own.

Note

Having the USAGE privilege on a model does not allow you to access its
artifacts; ownership is required.

You can access model artifacts from a stage using, for example, the [GET
command](../../../sql-reference/sql/get) or its equivalent in Snowpark Python,
[FileOperation.get](https://docs.snowflake.com/en/developer-
guide/snowpark/reference/python/latest/api/snowflake.snowpark.FileOperation.get).

However, you cannot address model artifacts using the usual stage path syntax.
Instead, use a `snow://` URL, a more general way to specify the location of
objects in Snowflake. For example, a version inside a model can be specified
by a URL of the form `snow://model/<model_name>/versions/<version_name>/`.

Knowing the of name of the model and the version you want, you can use the
[LIST command](../../../sql-reference/sql/list) to view the artifacts of the
model as follows:

    
    
    LIST 'snow://model/my_model/versions/V3/';
    

Copy

The output resembles:

    
    
    name                                      size                  md5                      last_modified
    versions/V3/MANIFEST.yml           30639    2f6186fb8f7d06e737a4dfcdab8b1350        Thu, 18 Jan 2024 09:24:37 GMT
    versions/V3/functions/apply.py      2249    e9df6db11894026ee137589a9b92c95d        Thu, 18 Jan 2024 09:24:37 GMT
    versions/V3/functions/predict.py    2251    132699b4be39cc0863c6575b18127f26        Thu, 18 Jan 2024 09:24:37 GMT
    versions/V3/model.zip             721663    e92814d653cecf576f97befd6836a3c6        Thu, 18 Jan 2024 09:24:37 GMT
    versions/V3/model/env/conda.yml          332        1574be90b7673a8439711471d58ec746        Thu, 18 Jan 2024 09:24:37 GMT
    versions/V3/model/model.yaml       25718    33e3d9007f749bb2e98f19af2a57a80b        Thu, 18 Jan 2024 09:24:37 GMT
    

To retrieve one of these artifacts, use the SQL GET command:

    
    
    GET 'snow://model/model_my_model/versions/V3/MANIFEST.yml'
    

Copy

Or the equivalent with Snowpark Python:

    
    
    session.file.get('snow://model/my_model/versions/V3/MANIFEST.yml', 'model_artifacts')
    

Copy

Note

The names and organization of a model’s artifacts can vary depending on the
type of the model and might change. The preceding example artifact list is
intended to be illustrative, not authoritative.

## Deleting models¶

Use the registry’s `delete_model` method to delete a model and all its
versions:

    
    
    reg.delete_model("mymodel")
    

Copy

Tip

You can also delete models in SQL using [DROP MODEL](../../../sql-
reference/sql/drop-model).

## Getting models from the registry¶

To get information about each model, use the `show_models` method:

    
    
    model_df = reg.show_models()
    

Copy

Tip

In SQL, use [SHOW MODELS](../../../sql-reference/sql/show-models) to get a
list of models.

The result of `show_models` is a pandas DataFrame. The available columns are
listed here:

Column | Description  
---|---  
`created_on` | Date and time when the model was created.  
`name` | Name of the model.  
`database_name` | Database in which the model is stored.  
`schema_name` | Schema in which the model is stored.  
`owner` | Role that owns the model.  
`comment` | Comment for the model.  
`versions` | JSON array listing versions of the model.  
`default_version_name` | Version of the model used when referring to the model without a version.  
  
To get a list of the models in the registry instead, each as a `Model`
instance, use the `models` method:

    
    
    model_list = reg.models()
    

Copy

To get a reference to a specific model from the registry by name, use the
registry’s `get_model` method:

    
    
    m = reg.get_model("MyModel")
    

Copy

Note

`Model` instances are not copies of the original logged Python model object;
they are references to the underlying model object in the registry.

After you have a reference to a model, either one from the list returned by
the `models` method or one retrieved using `get_model`, you can work with its
metadata and its versions.

## Viewing and updating a model’s metadata¶

You can view and update a model’s metadata attributes in the registry,
including its name, comment, tags, and metrics.

### Retrieving and updating comments¶

Use the model’s `comment` attribute to retrieve and update the model’s
comment:

    
    
    print(m.comment)
    m.comment = "A better description than the one I provided originally"
    

Copy

Note

The `description` attribute is a synonym for `comment`. The previous code can
also be written this way:

    
    
    print(m.description)
    m.description = "A better description than the one I provided originally"
    

Copy

Tip

You can also set a model’s comment in SQL by using [ALTER MODEL](../../../sql-
reference/sql/alter-model).

### Retrieving and updating tags¶

Tags are metadata used to record a model’s purpose, algorithm, training data
set, lifecycle stage, or other information you choose. You can set tags when
the model is registered or at any time afterward. You can also update the
values of existing tags or remove tags entirely.

Note

You must define the names of all tags (and potentially their possible values)
first by using CREATE TAG. See [Object Tagging](../../../user-guide/object-
tagging).

To get all of a model’s tags as a Python dictionary, use `show_tags`:

    
    
    print(m.show_tags())
    

Copy

To add a new tag or change the value of an existing tag, use `set_tag`:

    
    
    m.set_tag("live_version", "v1")
    

Copy

To retrieve the value of a tag, use `get_tag`:

    
    
    m.get_tag("live_version")
    

Copy

To remove a tag, use `unset_tag`:

    
    
    m.unset_tag("live_version")
    

Copy

Tip

You can also set a model’s comment in SQL by using [ALTER MODEL](../../../sql-
reference/sql/alter-model).

### Renaming a model¶

Use the `rename` method to rename or move a model. Specify a fully qualified
name as the new name to move the model to a different database or schema.

    
    
    m.rename("MY_MODEL_TOO")
    

Copy

Tip

You can also rename a model in SQL using [ALTER MODEL](../../../sql-
reference/sql/alter-model).

## Working with model versions¶

A model can have unlimited versions, each identified by a string. You can use
any version naming convention that you like. Logging a model actually logs a
_specific version_ of the model. To log additional versions of a model, call
`log_model` again with the same `model_name` but a different `version_name`.

Tip

In SQL, use [SHOW VERSIONS IN MODEL](../../../sql-reference/sql/show-versions-
in-model) to see the versions of a model.

A version of a model is represented by an instance of the
`snowflake.ml.model.ModelVersion` class.

To get a list of all the versions of a model, call the model object’s
`versions` method. The result is a list of `ModelVersion` instances:

    
    
    version_list = m.versions()
    

Copy

To get information about each model as a DataFrame instead, call the model’s
`show_versions` method:

    
    
    version_df = m.show_versions()
    

Copy

The resulting DataFrame contains the following columns:

Column | Description  
---|---  
`created_on` | Date and time when the model version was created.  
`name` | Name of the version.  
`database_name` | Database in which the version is stored.  
`schema_name` | Schema in which the version is stored.  
`model_name` | Name of the model that this version belongs to.  
`is_default_version` | Boolean value indicating whether this version is the model’s default version.  
`functions` | JSON array of the names of the functions available in this version.  
`metadata` | JSON object containing metadata as key-value pairs (`{}` if no metadata is specified).  
`user_data` | JSON object from the `user_data` section of the model definition manifest (`{}` if no user data is specified).  
  
### Deleting model versions¶

You can delete a model version by using the model’s `delete_version` method:

    
    
    m.delete_version("rc1")
    

Copy

Tip

You can also delete a model version in SQL by using [ALTER MODEL … DROP
VERSION](../../../sql-reference/sql/alter-model-drop-version).

### Default version¶

A version of a model can be designated as the default model. Retrieve or set
the model’s `default` attribute to obtain the current default version (as a
`ModelVersion` object) or to change it (using a string):

    
    
    default_version = m.default
    m.default = "v2"
    

Copy

Tip

In SQL, use [ALTER MODEL](../../../sql-reference/sql/alter-model) to set the
default version.

### Model version aliases¶

You can assign an alias to a model version by using the SQL [ALTER
MODEL](../../../sql-reference/sql/alter-model) command. You can use an alias
wherever a version name is required, such as when getting a reference to a
model version, in Python or in SQL. A given alias can be assigned to only one
model version at a time.

In addition to aliases you create, the following system aliases are available
in all models:

  * `DEFAULT` refers to the default version of the model.

  * `FIRST` refers to the oldest version of the model by creation time.

  * `LAST` refers to the newest version of the model by creation time.

Alias names you create must not be the same as any existing version name or
alias in the model, including system aliases.

### Getting a reference to a model version¶

To get a reference to a specific version of a model as a `ModelVersion`
instance, use the model’s `version` method. Use the model’s `default`
attribute to get the default version of the model:

    
    
    m = reg.get_model("MyModel")
    
    mv = m.version("v1")
    mv = m.default
    

Copy

After you have a reference to a specific version of a model (such as the
variable `mv` in this example), you can retrieve or update its comments or
metrics and call the model’s methods (or functions) as shown in the following
sections.

### Retrieving and updating comments¶

As with models, model versions can have comments, which can be accessed and
set via the model version’s `comment` or `description` attribute:

    
    
    print(mv.comment)
    print(mv.description)
    
    mv.comment = "A model version comment"
    mv.description = "Same as setting the comment"
    

Copy

Tip

You can also change a model version’s comment in SQL by using [ALTER MODEL …
MODIFY VERSION](../../../sql-reference/sql/alter-model-modify-version).

### Retrieving and updating metrics¶

Metrics are key-value pairs used to track prediction accuracy and other model
version characteristics. You can set metrics when creating a model version or
set them using the `set_metric` method. A metric value can be any Python
object that can be serialized to JSON, including numbers, strings, lists, and
dictionaries. Unlike tags, metric names and possible values do not need to be
defined in advance.

A test accuracy metric might be generated using sklearn’s `accuracy_score`:

    
    
    from sklearn import metrics
    
    test_accuracy = metrics.accuracy_score(test_labels, prediction)
    

Copy

The confusion matrix can be generated similarly using sklearn:

    
    
    test_confusion_matrix = metrics.confusion_matrix(test_labels, prediction)
    

Copy

Then you can set these values as metrics:

    
    
    # scalar metric
    mv.set_metric("test_accuracy", test_accuracy)
    
    # hierarchical (dictionary) metric
    mv.set_metric("evaluation_info", {"dataset_used": "my_dataset", "accuracy": test_accuracy, "f1_score": f1_score})
    
    # multivalent (matrix) metric
    mv.set_metric("confusion_matrix", test_confusion_matrix)
    

Copy

To retrieve a model version’s metrics as a Python dictionary, use
`show_metrics`:

    
    
    metrics = mv.show_metrics()
    

Copy

To delete a metric, call `delete_metric`:

    
    
    mv.delete_metric("test_accuracy")
    

Copy

Tip

You can also modify a model version’s metrics (which are stored in as
metadata) in SQL by using [ALTER MODEL … MODIFY VERSION](../../../sql-
reference/sql/alter-model-modify-version).

### Retrieving model explanations¶

The model registry can explain a model’s results, telling you which input
features contribute most to predictions, by calculating [Shapley
values](https://towardsdatascience.com/the-shapley-value-for-ml-
models-f1100bff78d1). This preview feature is available by default in all
model views created in Snowflake 8.31 and later through the underlying model’s
`explain` method. You can call `explain` from SQL or via a model view’s `run`
method in Python.

For details on this feature, see [Model Explainability](model-explainability).

### Exporting a model version¶

Use `mv.export` to export a model’s files to a local directory; the directory
is created if it does not exist:

    
    
    mv.export("~/mymodel/")
    

Copy

By default, the exported files include the code, the environment to load the
model, and model weights. To also export the files needed to run the model in
a warehouse, specify `export_mode = ExportMode.FULL`:

    
    
    mv.export("~/mymodel/", export_mode=ExportMode.FULL)
    

Copy

### Loading a model version¶

Use `mv.load` to load the original Python model object that was originally
added to the registry. You can then use the model for inference just as though
you had defined it in your Python code:

    
    
    clf = mv.load()
    

Copy

To ensure proper functionality of a model loaded from the registry, the target
Python environment (that is, the versions of the Python interpreter and of all
libraries) should be identical to the environment from which the model was
logged. Specify `force=True` in the `load` call to force the model to be
loaded even if the environment is different.

Tip

To make sure your environment is the same as the one where the model is
hosted, download a copy of the conda environment from the model registry:

    
    
    conda_env = session.file.get("snow://model/<modelName>/versions/<versionName>/runtimes/python_runtime/env/conda.yml", ".")
    open("~/conda.yml", "w").write(conda_env)
    

Copy

Then create a new conda environment from this file:

    
    
    conda env create --name newenv --file=~/conda.yml
    conda activate newenv
    

Copy

The optional `options` argument is a dictionary of options for loading the
model. Currently, the argument supports only the `use_gpu` option.

Option | Type | Description | Default  
---|---|---|---  
`use_gpu` | `bool` | Enables GPU-specific loading logic. | `False`  
  
The following example illustrates the use of the `options` argument:

    
    
    clf = mv.load(options={"use_gpu": True})
    

Copy

## Calling model methods¶

Model versions can have _methods,_ which are attached functions that can be
executed to perform inference or other model operations. The versions of a
model can have different methods, and the signatures of these methods can also
differ.

To call a method of a model version, use `mv.run`, where `mv` is a
`ModelVersion` object. Specify the name of the function to be called and pass
a Snowpark or pandas DataFrame that contains the inference data, along with
any required parameters. The method is executed in a Snowflake warehouse.

The return value of the method is a Snowpark or pandas DataFrame, matching the
type of DataFrame passed in. Snowpark DataFrames are evaluated lazily, so the
method is run only when the DataFrame’s `collect`, `show`, or `to_pandas`
method is called.

Note

Invoking a method runs it in the warehouse specified in the session you’re
using to connect to the registry. See [Specifying a Warehouse](../snowpark-
ml.html#label-snowpark-ml-specify-warehouse).

The following example illustrates running the `predict` method of a model.
This model’s `predict` method does not require any parameters besides the
inference data (`test_features` here). If it did, they would be passed as
additional arguments after the inference data:

    
    
    remote_prediction = mv.run(test_features, function_name="predict")
    remote_prediction.show()   # assuming test_features is Snowpark DataFrame
    

Copy

To see what methods can be called on a given model, call `mv.show_functions`.
The return value of this method is a list of `ModelFunctionInfo` objects. Each
of these objects includes the following attributes:

  * `name`: The name of the function that can be called from Python or SQL.

  * `target_method`: The name of the Python method in the original logged model.

Tip

You can also call model methods in SQL. See [Model methods](../../../sql-
reference/commands-model.html#label-snowpark-model-registry-model-methods).

## Sharing models¶

[![Snowflake logo in black \(no text\)](../../../_images/logo-snowflake-
black.png)](../../../_images/logo-snowflake-black.png) [Preview
Feature](../../../release-notes/preview-features) — Open

Available to all accounts.

The model registry can store two types of models. You can distinguish them
using the MODEL_TYPE column in the output of [SHOW MODELS](../../../sql-
reference/sql/show-models).

  * CORTEX_FINETUNED: Models generated with [Cortex Fine-tuning](../../../user-guide/snowflake-cortex/cortex-finetuning), which do not contain user code. To share this type of model, use [Data Sharing](../../../user-guide/data-sharing-intro).

  * USER_MODEL: Models that contain user code, such as models developed using [Snowpark ML modeling classes](../modeling). These models cannot currently be shared. The ability to share models that contain user code will be available in a future release.

## Cost considerations¶

Using the Snowflake Model Registry incurs standard Snowflake consumption-based
costs. These include:

  * Cost of storing model artifacts, metadata, and functions. For general information about storage costs, see [Exploring storage cost](../../../user-guide/cost-exploring-data-storage).

  * Cost of copying files between stages to Snowflake. See [COPY FILES](../../../sql-reference/sql/copy-files).

  * Cost of serverless model object operations through the Snowsight UI or the SQL or Python interface, such as showing models and model versions and altering model comments, tags, and metrics.

  * Warehouse compute costs, which vary depending on the type of model and the quantity of data used in inference. For general information about Snowflake compute costs, see [Understanding compute cost](../../../user-guide/cost-understanding-compute). Warehouse compute costs are incurred for:

    * Model and version creation operations

    * Invoking a model’s methods

## Notes on specific model types¶

This section provides additional information on logging specific types of
models into the Snowflake Model Registry.

### Snowpark ML¶

The registry supports models created using [Snowpark ML modeling
APIs](../modeling) (models derived from
`snowpark.ml.modeling.framework.base.BaseEstimator`). The following additional
options can be used in the `options` dictionary when you call `log_model`:

Option | Description  
---|---  
`target_methods` | A list of the names of the methods available on the model object. Snowpark ML models have the following target methods by default, assuming the method exists: `predict`, `transform`, `predict_proba`, `predict_log_proba`, `decision_function`.  
  
You do not need to specify `sample_input_data` or `signatures` when logging a
Snowpark ML model; these are automatically inferred during fitting.

#### Example¶

    
    
    import pandas as pd
    import numpy as np
    from sklearn import datasets
    from snowflake.ml.modeling.xgboost import XGBClassifier
    
    iris = datasets.load_iris()
    df = pd.DataFrame(data=np.c_[iris["data"], iris["target"]], columns=iris["feature_names"] + ["target"])
    df.columns = [s.replace(" (CM)", "").replace(" ", "") for s in df.columns.str.upper()]
    
    input_cols = ["SEPALLENGTH", "SEPALWIDTH", "PETALLENGTH", "PETALWIDTH"]
    label_cols = "TARGET"
    output_cols = "PREDICTED_TARGET"
    
    clf_xgb = XGBClassifier(
            input_cols=input_cols, output_cols=output_cols, label_cols=label_cols, drop_input_cols=True
    )
    clf_xgb.fit(df)
    model_ref = registry.log_model(
        clf_xgb,
        model_name="XGBClassifier",
        version_name="v1",
    )
    model_ref.run(df.drop(columns=label_cols).head(10), function_name='predict_proba')
    

Copy

### scikit-learn¶

The registry supports models created using scikit-learn (models derived from
`sklearn.base.BaseEstimator` or `sklearn.pipeline.Pipeline`). The following
additional options can be used in the `options` dictionary when you call
`log_model`:

Option | Description  
---|---  
`target_methods` | A list of the names of the methods available on the model object. scikit-learn models have the following target methods by default, assuming the method exists: `predict`, `transform`, `predict_proba`, `predict_log_proba`, `decision_function`.  
  
You must specify either the `sample_input_data` or `signatures` parameter when
logging a scikit-learn model so that the registry knows the signatures of the
target methods.

#### Example¶

    
    
    from sklearn import datasets, ensemble
    
    iris_X, iris_y = datasets.load_iris(return_X_y=True, as_frame=True)
    clf = ensemble.RandomForestClassifier(random_state=42)
    clf.fit(iris_X, iris_y)
    model_ref = registry.log_model(
        clf,
        model_name="RandomForestClassifier",
        version_name="v1",
        sample_input_data=iris_X,
        options={
            "method_options": {
                "predict": {"case_sensitive": True},
                "predict_proba": {"case_sensitive": True},
                "predict_log_proba": {"case_sensitive": True},
            }
        },
    )
    model_ref.run(iris_X[-10:], function_name='"predict_proba"')
    

Copy

### XGBoost¶

The registry supports models created using XGBoost (models derived from
`xgboost.XGBModel` or `xgboost.Booster`). The following additional options can
be used in the `options` dictionary when you call `log_model`:

Option | Description  
---|---  
`target_methods` | A list of the names of the methods available on the model object. Models derived from `XGBModel` have the following target methods by default, assuming the method exists: `predict`, `predict_proba`. (Before v1.4.0, `apply` was also included.) Models derived from `Booster` have the `predict` method by default.  
`cuda_version` | The version of the CUDA runtime to be used when deploying to a platform with GPU; defaults to 11.7. If manually set to `None`, the model cannot be deployed to a platform having a GPU.  
  
You must specify either the `sample_input_data` or `signatures` parameter when
logging an XGBoost model so that the registry knows the signatures of the
target methods.

#### Example¶

    
    
    import xgboost
    from sklearn import datasets, model_selection
    
    cal_X, cal_y = datasets.load_breast_cancer(as_frame=True, return_X_y=True)
    cal_X_train, cal_X_test, cal_y_train, cal_y_test = model_selection.train_test_split(cal_X, cal_y)
    params = dict(n_estimators=100, reg_lambda=1, gamma=0, max_depth=3, objective="binary:logistic")
    regressor = xgboost.train(params, xgboost.DMatrix(data=cal_X_train, label=cal_y_train))
    model_ref = registry.log_model(
        regressor,
        model_name="xgBooster",
        version_name="v1",
        sample_input_data=cal_X_test,
        options={
            "target_methods": ["predict"],
            "method_options": {
                "predict": {"case_sensitive": True},
            },
        },
    )
    model_ref.run(cal_X_test[-10:])
    

Copy

### PyTorch¶

The registry supports PyTorch models (classes derived from `torch.nn.Module`
or `torch.jit.ModuleScript`) if the model’s `forward` method accepts one or
more `torch.Tensor` instances as input and returns a `torch.Tensor` or a tuple
of them. The registry converts between pandas DataFrames and tensors when
calling the model and returning the results. Tensors correspond to columns in
the dataframe.

For example, suppose your model accepts two tensors like this:

    
    
    import torch
    
    class TorchModel(torch.nn.Module):
        def __init__(self, n_input: int, n_hidden: int, n_out: int, dtype: torch.dtype = torch.float32) -> None:
            super().__init__()
            self.model = torch.nn.Sequential(
                torch.nn.Linear(n_input, n_hidden, dtype=dtype),
                torch.nn.ReLU(),
                torch.nn.Linear(n_hidden, n_out, dtype=dtype),
                torch.nn.Sigmoid(),
            )
    
        def forward(self, tensor_1: torch.Tensor, tensor_2: torch.Tensor) -> torch.Tensor:
            return self.model(tensor_1) + self.model(tensor_2)
    

Copy

If you want to pass `torch.Tensor([[1,2],[3,4]])` as `tensor_1` and
`torch.Tensor([[5,6], [7,8]])` as `tensor_2`, create a DataFrame like this to
pass to the model:

    
    
    import pandas as pd
    tensors = pd.DataFrame([[[1,2],[5,6]],[[3,4],[7,8]]])
    

Copy

Then the `tensors` DataFrame looks like this:

    
    
            0       1
    0  [1, 2]  [5, 6]
    1  [3, 4]  [7, 8]
    

Copy

Similarly, if your model returns two tensors, such as
`(torch.Tensor([[1,2],[3,4]]), torch.Tensor([[5,6], [7,8]]))`, the result is a
DataFrame like the one above.

When providing sample input data for a PyTorch model, you must provide either
a list of tensors (which will be converted to a pandas DataFrame) or a
DataFrame. A list may contain a single tensor, but a tensor on its own is not
accepted.

#### Logging the model¶

The following additional options can be used in the `options` dictionary when
you call `log_model`:

Option | Description  
---|---  
`target_methods` | A list of the names of the methods available on the model object. PyTorch models default to `forward`.  
`cuda_version` | The version of the CUDA runtime to be used when deploying to a platform with GPU; defaults to 11.7. If manually set to `None`, the model cannot be deployed to a platform having a GPU.  
  
You must specify either the `sample_input_data` or `signatures` parameter when
logging a PyTorch model so that the registry knows the signatures of the
target methods.

#### Example¶

    
    
    import torch
    import numpy as np
    
    class TorchModel(torch.nn.Module):
            def __init__(self, n_input: int, n_hidden: int, n_out: int, dtype: torch.dtype = torch.float32) -> None:
                    super().__init__()
                    self.model = torch.nn.Sequential(
                            torch.nn.Linear(n_input, n_hidden, dtype=dtype),
                            torch.nn.ReLU(),
                            torch.nn.Linear(n_hidden, n_out, dtype=dtype),
                            torch.nn.Sigmoid(),
                    )
    
            def forward(self, tensor: torch.Tensor) -> torch.Tensor:
                    return self.model(tensor)
    
    n_input, n_hidden, n_out, batch_size, learning_rate = 10, 15, 1, 100, 0.01
    dtype = torch.float32
    x = np.random.rand(batch_size, n_input)
    data_x = torch.from_numpy(x).to(dtype=dtype)
    data_y = (torch.rand(size=(batch_size, 1)) < 0.5).to(dtype=dtype)
    
    model = TorchModel(n_input, n_hidden, n_out, dtype=dtype)
    loss_function = torch.nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
    for _epoch in range(100):
            pred_y = model.forward(data_x)
            loss = loss_function(pred_y, data_y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
    
    
    model_ref = registry.log_model(
        model,
        model_name="torchModel",
        version_name="v1",
        sample_input_data=[data_x],
    )
    model_ref.run([data_x])
    

Copy

### TensorFlow¶

Models that extend `tensorflow.Module` or `tensorflow.keras.Model` are
supported when they accept and return tensors and are compilable or compiled.

  * The `__call__` method for a `tensorflow.Module` or the `call` method for a `tensorflow.keras.Model` accepts one or more `tensorflow.Tensor` or `tensorflow.Variable` as input and returns a `tensorflow.Tensor` or `tensorflow.Variable` or a tuple of one of these types.

  * If your model extends `Module`, it must be compilable, meaning the `__call__` method is decorated with `@tensorflow.function`; see [tf.function documentation](https://www.tensorflow.org/guide/function). If it extends `Model`, it must be compiled; see [compile documentation](https://www.tensorflow.org/api_docs/python/tf/keras/Model#compile).

The registry converts between pandas DataFrames and tensors when calling the
model and returning the results. Tensors correspond to columns in the
dataframe.

For example, suppose your model accepts two tensors like this:

    
    
    import tensorflow as tf
    
    class KerasModel(tf.keras.Model):
        def  __init__(self, n_hidden: int, n_out: int) -> None:
            super().__init__()
            self.fc_1 = tf.keras.layers.Dense(n_hidden, activation="relu")
            self.fc_2 = tf.keras.layers.Dense(n_out, activation="sigmoid")
    
        def call(self, tensor_1: tf.Tensor, tensor_2: tf.Tensor) -> tf.Tensor:
            input = tensor_1 + tensor_2
            x = self.fc_1(input)
            x = self.fc_2(x)
            return x
    

Copy

If you want to pass `tf.Tensor([[1,2],[3,4]])` as `tensor_1` and
`tf.Tensor([[5,6], [7,8]])` as `tensor_2`, create a DataFrame like this to
pass to the model:

    
    
    import pandas as pd
    tensors = pd.DataFrame([[[1,2],[5,6]],[[3,4],[7,8]]])
    

Copy

Then the `tensors` DataFrame looks like this:

    
    
            0       1
    0  [1, 2]  [5, 6]
    1  [3, 4]  [7, 8]
    

Copy

Similarly, if your model returns two tensors, such as
`(tf.Tensor([[1,2],[3,4]]), tf.Tensor([[5,6], [7,8]]))`, the result is a
DataFrame like the one above.

When providing sample input data for a TensorFlow model, you must provide
either a list of tensors (which will be converted to a pandas DataFrame) or a
DataFrame. A list may contain a single tensor, but a tensor on its own is not
accepted.

#### Logging the model¶

The following additional options can be used in the `options` dictionary when
you call `log_model`:

Option | Description  
---|---  
`target_methods` | A list of the names of the methods available on the model object. TensorFlow models default to `forward`.  
`cuda_version` | The version of the CUDA runtime to be used when deploying to a platform with GPU; defaults to 11.7. If manually set to `None`, the model cannot be deployed to a platform having a GPU.  
  
You must specify either the `sample_input_data` or `signatures` parameter when
logging a TensorFlow model so that the registry knows the signatures of the
target methods.

#### Example¶

    
    
    import tensorflow as tf
    import numpy as np
    
    class KerasModel(tf.keras.Model):
            def __init__(self, n_hidden: int, n_out: int) -> None:
                    super().__init__()
                    self.fc_1 = tf.keras.layers.Dense(n_hidden, activation="relu")
                    self.fc_2 = tf.keras.layers.Dense(n_out, activation="sigmoid")
    
            def call(self, tensor: tf.Tensor) -> tf.Tensor:
                    input = tensor
                    x = self.fc_1(input)
                    x = self.fc_2(x)
                    return x
    
    n_input, n_hidden, n_out, batch_size, learning_rate = 10, 15, 1, 100, 0.01
    dtype = tf.float32
    x = np.random.rand(batch_size, n_input)
    data_x = tf.convert_to_tensor(x, dtype=dtype)
    raw_data_y = tf.random.uniform((batch_size, 1))
    raw_data_y = tf.where(raw_data_y > 0.5, tf.ones_like(raw_data_y), tf.zeros_like(raw_data_y))
    data_y = tf.cast(raw_data_y, dtype=dtype)
    
    model = KerasModel(n_hidden, n_out)
    model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=learning_rate), loss=tf.keras.losses.MeanSquaredError())
    model.fit(data_x, data_y, batch_size=batch_size, epochs=100)
    
    model_ref = registry.log_model(
        model,
        model_name="tfModel",
        version_name="v1",
        sample_input_data=[data_x],
    )
    model_ref.run([data_x])
    

Copy

### MLFlow¶

MLFlow models that provide a PyFunc flavor are supported. If your MLFlow model
has a signature, the `signature` argument is inferred from the model.
Otherwise, you must provide either `signature` or `sample_input_data`.

The following additional options can be used in the `options` dictionary when
you call `log_model`:

Option | Description  
---|---  
`model_uri` | The URI of the artifacts of the MLFlow model. Must be provided if it is not available in the model’s metadata as `model.metadata.get_model_info().model_uri`.  
`ignore_mlflow_metadata` | If `True`, the model’s metadata is not imported to the model object in the registry. Default: `False`  
`ignore_mlflow_dependencies` | If `True`, the dependencies in the model’s metadata are ignored, which is useful due to package available limitations in Snowflake warehouses. Default: `False`  
  
#### Example¶

    
    
    import mlflow
    from sklearn import datasets, model_selection, ensemble
    
    db = datasets.load_diabetes(as_frame=True)
    X_train, X_test, y_train, y_test = model_selection.train_test_split(db.data, db.target)
    with mlflow.start_run() as run:
        rf = ensemble.RandomForestRegressor(n_estimators=100, max_depth=6, max_features=3)
        rf.fit(X_train, y_train)
    
        # Use the model to make predictions on the test dataset.
        predictions = rf.predict(X_test)
        signature = mlflow.models.signature.infer_signature(X_test, predictions)
        mlflow.sklearn.log_model(
            rf,
            "model",
            signature=signature,
        )
        run_id = run.info.run_id
    
    
    model_ref = registry.log_model(
        mlflow.pyfunc.load_model(f"runs:/{run_id}/model"),
        model_name="mlflowModel",
        version_name="v1",
        conda_dependencies=["mlflow<=2.4.0", "scikit-learn", "scipy"],
        options={"ignore_mlflow_dependencies": True}
    )
    model_ref.run(X_test)
    

Copy

### Hugging Face pipeline¶

Note

For details on the expected input and output of specific types of Hugging Face
pipelines, see [Inferred signatures for Hugging Face pipelines](hugging-face).

The registry supports Hugging Face model classes defined as
[transformers](https://huggingface.co/docs/transformers/index) that derive
from `transformers.Pipeline`. The following code is an example of logging a
compatible model:

    
    
    lm_hf_model = transformers.pipeline(
        task="text-generation",
        model="bigscience/bloom-560m",
        token="...",  # Put your HuggingFace token here.
        return_full_text=False,
        max_new_tokens=100,
    )
    
    lmv = reg.log_model(lm_hf_model, model_name='bloom', version_name='v560m')
    

Copy

Important

A model based on `huggingface_pipeline.HuggingFacePipelineModel` contains only
configuration data; the model weights are downloaded from the Hugging Face Hub
each time the model is used.

Currently, the model registry supports only self-contained models that are
ready to run without [external network access configuration](../../external-
network-access/external-network-access-overview). Therefore, the best practice
is to instead use `transformers.Pipeline` as shown in the example above. This
downloads model weights to your local system, and `log_model` then uploads a
self-contained model object that does not need internet access.

The registry infers the `signatures` argument only if the pipeline contains
one task from the following list:

  * `conversational`

  * `fill-mask`

  * `question-answering`

  * `summarization`

  * `table-question-answering`

  * `text2text-generation`

  * `text-classification` (also called `sentiment-analysis`)

  * `text-generation`

  * `token-classification` (also called `ner`)

  * `translation`

  * `translation_xx_to_yy`

  * `zero-shot-classification`

The `sample_input_data` argument is completely ignored for Hugging Face
models. Specify the `signatures` argument when logging a Hugging Face model
that is not in the above list so that the registry knows the signatures of the
target methods.

To see the inferred signature, use the `show_functions` method. The following
dictionary, for example, is the result of `lmv.show_functions()` where `lmv`
is the model logged above:

    
    
    {'name': '__CALL__',
      'target_method': '__call__',
      'signature': ModelSignature(
                          inputs=[
                              FeatureSpec(dtype=DataType.STRING, name='inputs')
                          ],
                          outputs=[
                              FeatureSpec(dtype=DataType.STRING, name='outputs')
                          ]
                      )}]
    

Copy

With this information, you can call the model as follows:

    
    
    import pandas as pd
    remote_prediction = lmv.run(pd.DataFrame(["Hello, how are you?"], columns=["inputs"]))
    

Copy

#### Usage notes¶

  * Many Hugging Face models are large and do not fit in a standard warehouse. Use a Snowpark-optimized warehouse or choose a smaller version of the model. For example, instead of using the `Llama-2-70b-chat-hf` model, try `Llama-2-7b-chat-hf`.

  * Snowflake warehouses do not have GPUs. Use only CPU-optimized Hugging Face models.

  * Some Hugging Face transformers return an array of dictionaries per input row. The registry converts such output to a string containing a JSON representation of the array. For example, multi-output Question Answering output looks like this:
    
        [{"score": 0.61094731092453, "start": 139, "end": 178, "answer": "learn more about the world of athletics"},
    {"score": 0.17750297486782074, "start": 139, "end": 180, "answer": "learn more about the world of athletics.\""}]
    

Copy

You must specify either the `sample_input_data` or `signatures` parameter when
logging a Hugging Face model so that the registry knows the signatures of the
target methods.

#### Example¶

    
    
    # Prepare model
    import transformers
    import pandas as pd
    
    finbert_model = transformers.pipeline(
        task="text-classification",
        model="ProsusAI/finbert",
        top_k=2,
    )
    
    # Log the model
    mv = registry.log_model(
        finbert_model,
        model_name="finbert",
        version_name="v1",
    )
    
    # Use the model
    mv.run(pd.DataFrame(
            [
                ["I have a problem with my Snowflake that needs to be resolved asap!!", ""],
                ["I would like to have udon for today's dinner.", ""],
            ]
        )
    )
    

Copy

Result:

    
    
    0  [{"label": "negative", "score": 0.8106237053871155}, {"label": "neutral", "score": 0.16587384045124054}]
    1  [{"label": "neutral", "score": 0.9263970851898193}, {"label": "positive", "score": 0.05286872014403343}]
    

Copy

