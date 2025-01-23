# Snowflake ML: End-to-End Machine Learning¶

Snowflake ML is an integrated set of capabilities for end-to-end machine
learning in a single platform on top of your governed data.

For out-of-the-box ML workflows in SQL, the ready-to-use [ML
Functions](../../guides-overview-ml-functions) can help shorten development
time and democratize ML across your organization. These functions let you
train models for business use cases such as forecasting and anomaly detection
without writing any code.

For custom ML workflows in Python, data scientists and ML engineers can easily
and securely develop and productionize scalable features and models without
any data movement, silos, or governance tradeoffs. The `snowflake-ml-python`
library provides APIs for developing and deploying your Snowflake ML
pipelines.

To build and operationalize models, data scientists and ML engineers can
leverage a suite of Snowflake ML features. For model development, [Snowflake
ML Modeling APIs](modeling) offer scalable data loading, feature engineering,
and model training with distributed processing using CPUs or GPUs. For ML
Operations (ML Ops), Snowflake ML includes the [Feature Store](feature-
store/overview) and [Model Registry](model-registry/overview) for centralized
management of features and models in production.

You can use Python APIs from the [Snowpark ML](snowpark-ml) library in
[Snowflake Notebooks](../../user-guide/ui-snowsight/notebooks), [Snowsight
worksheets](../../user-guide/ui-snowsight-worksheets-gs). or your local Python
IDE of choice.

![Key components of Snowflake ML: ML Modeling, Feature Store, and Model
Registry](../../_images/snowflake-ml-components.png)

Snowflake ML components help to streamline the ML lifecycle, as shown here.

![The ML development and deployment process supported by Snowflake
ML](../../_images/snowflake-ml-process.png)

## Snowflake Model Registry¶

The [Snowflake Model Registry](model-registry/overview) allows secure
deployment and management of models in Snowflake, supporting models trained
both inside and outside of Snowflake.

## Snowflake Feature Store¶

The [Snowflake Feature Store](feature-store/overview) is an integrated
solution for defining, managing, storing and discovering ML features derived
from your data. The Snowflake Feature Store supports automated, incremental
refresh from batch and streaming data sources, so that feature pipelines need
be defined only once to be continuously updated with new data.

## Snowflake Datasets¶

[Snowflake Datasets](dataset) provide an immutable, versioned snapshot of your
data suitable for ingestion by your machine learning models.

## Snowflake Notebooks¶

[Snowflake Notebooks](../../user-guide/ui-snowsight/notebooks) provide a
familiar experience, similar to Jupyter notebooks, for working with Python
inside Snowflake. They’re ideal for building custom ML workflows and models
using tools you already know how to use. Notebooks that run on Snowpark
Container Services (SPCS) execute on the Container Runtime for ML, a purpose-
built environment for machine learning workflows.

## Container Runtime for ML¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) [Preview
Feature](../../release-notes/preview-features) — Open

Available to all accounts.

Snowflake offers a pre-configured, customizable environment built for a
variety of ML development workloads. With a comprehensive set of pre-installed
ML packages and frameworks that can be easily extended, data scientists and ML
engineers can leverage the best of open source directly over their Snowflake
data.

WIth easy access to GPUs in the form of Snowpark Container Service (SPCS)
compute pools, the flexibility to use any open-source package, and distributed
data loading and modeling APIs, Container Runtime for ML is well-suited for
large-scale ML development. Because these notebooks run on Snowpark Container
Services, they provide a flexible and scalable compute infrastructure
optimized for price-performance.

For more information, see [Notebooks on Container Runtime for ML](../../user-
guide/ui-snowsight/notebooks-on-spcs) and [Container Runtime for
ML](container-runtime-ml).

## Snowflake ML Library¶

The `snowflake-ml-python` Python package provides Python APIs for the various
Snowflake ML workflow components, including the Snowflake Feature Store, the
Snowflake Model Registry, and Dataset versioned data objects. It also includes
APIs, based on popular Python ML libraries such as scikit-learn, for building
and training your own models at scale completely inside the Snowflake cloud.
You can use Snowflake ML features in your local Python development
environment, in Snowsight worksheets, or in Snowflake Notebooks.

Tip

See [Introduction to Machine
Learning](https://quickstarts.snowflake.com/guide/intro_to_machine_learning_with_snowpark_ml_for_python/#0)
for an example of an end-to-end Snowflake ML workflow.

### ML Modeling¶

The `snowflake-ml-python` Python package also includes the [ML Modeling
APIs](modeling), which support data preprocessing, feature engineering, and
model training in Snowflake using popular machine learning frameworks, such as
scikit-learn, xgboost, lightgbm, and pytorch. All processing is performed
without the need for any infrastructure configuration or data movement.

When run from a notebook on [Container Runtime for ML](container-runtime-ml),
these modeling APIs can run distributed over all available CPU cores or GPUs,
depending on the compute pool you’re using. In other cases, the process is
performed in a Snowflake virtual warehouse, where preprocessing and
hyperarameter optimization can be performed in distributed fashion over
multiple nodes.

Note

Container Runtime for ML is currently in private preview.

## Additional Resources¶

See the following resources for information about the Snowflake ML APIs.

**End-to-End ML Workflows**

  * [Quickstart](https://quickstarts.snowflake.com/guide/intro_to_machine_learning_with_snowpark_ml_for_python)

Contact your Snowflake representative for early access to documentation on
other features currently under development.

