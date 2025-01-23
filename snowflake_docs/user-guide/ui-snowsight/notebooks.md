# About Snowflake Notebooks¶

Feature — Generally Available

Generally available in Amazon Web Services (AWS), Microsoft Azure, and Google
Cloud Platform (GCP) commercial regions.

Snowflake Notebooks is a unified development interface in Snowsight that
offers an interactive, cell-based programming environment for Python, SQL, and
Markdown. In Snowflake Notebooks, you can leverage your Snowflake data to
perform exploratory data analysis, develop machine learning models, and
perform other data science and data engineering workflows, all within the same
interface.

  * Explore and experiment with data already in Snowflake, or upload new data to Snowflake from local files, external cloud storage, or datasets from the Snowflake Marketplace.

  * Write SQL or Python code and quickly compare results with cell-by-cell development and execution.

  * Interactively visualize your data using embedded Streamlit visualizations and other libraries like Altair, Matplotlib, or seaborn.

  * Integrate with Git to collaborate with effective version control. See [Sync Snowflake Notebooks with a Git repository](notebooks-snowgit).

  * Contextualize results and make notes about different results with Markdown cells and charts.

  * Run your notebook on a schedule to automate pipelines. See [Schedule your Snowflake Notebook to run](notebooks-schedule).

  * Make use of the role-based access control and other data governance functionality available in Snowflake to allow other users with the same role to view and collaborate on the notebook.

  * Create a private notebook stored in your personal database, where you can develop code interactively and experiment with production data assets. See [Private notebooks](notebooks-private).

![An example notebook in the Snowsight UI](../../_images/sf-notebooks-
intro.png)

## Notebook runtimes¶

Snowflake Notebooks offers two types of runtimes: warehouse runtime and
container runtime. Notebooks rely on virtual warehouses and/or Snowpark
Container Services compute pools to provide the compute resource. For both
architectures, SQL and Snowpark queries are always pushed down to execute on
the warehouse for optimized performance.

The warehouse runtime gives you the fastest way to start, with a familiar
warehouse environment that is generally available. The container runtime
provides a more flexible environment that can support many different types of
workloads, including SQL analytics and data engineering. You can install
additional Python packages if the container runtime doesn’t include what you
need by default. Container runtime also comes in CPU and GPU versions that
have many popular ML packages pre-installed, making them ideal for ML and deep
learning workloads.

The following table shows supported features for each type of runtime. You can
use this table to help decide which runtime is the right choice for your use
case.

Supported Features | Warehouse Runtime | Container Runtime  
---|---|---  
Compute | Kernel runs on the notebook warehouse. | Kernel runs on [Compute Pool](../../developer-guide/snowpark-container-services/working-with-compute-pool) node.  
Environment | Python 3.9 | Python 3.10  
Base image | Streamlit + Snowpark | Snowflake container runtime. CPU and GPU images are pre-installed with a set of Python libraries.  
Additional Python libraries | Install using Snowflake Anaconda or from a Snowflake stage. | Install using `pip` or from a Snowflake stage.  
Editing support | 

  * Python, SQL and Markdown cells.
  * Reference outputs from SQL cells in Python cells and vice versa.
  * Use visualization libraries like Streamlit.

| Same as warehouse  
Access | Ownership required to access and edit notebooks. | Same as warehouse  
Supported Notebook features (still in Preview) | 

  * Git integration (Preview)
  * Scheduling (Preview)

| Same as warehouse  
  
### Get started with Snowflake Notebooks¶

To start experimenting with Snowflake Notebooks, sign into [Snowsight](../ui-
snowsight), [set up your account to use notebooks](notebooks-setup.html#label-
notebooks-setup), and then select Notebooks from the Projects pane. A list of
notebooks that you have access to in your account is displayed. You can either
create a new notebook from scratch or upload an existing `.ipynb` file.

The following table shows the topics to review if you’re new to Snowflake
Notebooks:

Getting started guides  
---  
[![Set up Snowflake Notebook](../../_images/setup-sf-notebooks-tile.png)](../../_images/setup-sf-notebooks-tile.png) | [Setting up Snowflake Notebooks](notebooks-setup.html#label-notebooks-setup) Instructions for developers and admins before using Notebook.  
[![Create Snowflake Notebook](../../_images/create-sf-notebooks-tile.png)](../../_images/create-sf-notebooks-tile.png) | [Create a Snowflake Notebook](notebooks-create.html#label-notebooks-create) Create a new notebook from scratch or from an existing file.  
[![Develop and run code in Snowflake Notebook](../../_images/develop-sf-notebooks-tile.png)](../../_images/develop-sf-notebooks-tile.png) | [Develop and Run Code in Snowflake Notebook](notebooks-develop-run) Create, edit, execute Python, SQL, Markdown cells.  
  
### Developer guides¶

Guide | Description  
---|---  
[Session context in notebooks](notebooks-sessions.html#label-notebooks-callers-rights) | Accessing and modifying the session context.  
[Saving results in notebooks](notebooks-save-share.html#label-notebooks-sharing) | Saving notebooks and results across sessions.  
[Import Python packages to use in notebooks](notebooks-import-packages.html#label-notebooks-import-libraries) | Importing Python package from Anaconda channel.  
[Visualize and Interact with your data in Notebook](notebooks-visualize-data.html#label-notebooks-visualize-data) | Visualize data with matplotlib, plotly, altair and develop a data app with Streamlit.  
[Cell and variable referencing in Notebook](notebooks-develop-run.html#label-notebooks-reference-cell-results) | Reference SQL cell output and Python variable values.  
[Keyboard shortcuts for Notebooks](notebooks-keyboard-shortcuts.html#label-notebooks-keyboard-shortcuts) | Leverage keyboard shortcut to navigate and streamline editing experience.  
  
### Leveling up your notebook workflows¶

Guide | Description  
---|---  
[Sync Snowflake Notebooks with Git](notebooks-snowgit) | Version control your notebook for collaboration and development.  
[Work with files in notebook](notebooks-work-with-files) | Manage and work with files in your notebook environment.  
[Schedule notebook runs](notebooks-schedule) | Schedule notebooks to run and execute code within Snowflake.  
[Experience Snowflake with notebooks](notebooks-use-with-snowflake) | Leverage other Snowflake capabilities within Snowflake Notebooks.  
[Troubleshoot errors in Snowflake Notebooks](notebooks-troubleshoot) | Troubleshoot errors you may run into while using Snowflake Notebooks.  
  
### Quickstarts¶

  * [Getting Started with Your First Snowflake Notebook](https://quickstarts.snowflake.com/guide/getting_started_with_snowflake_notebooks/) [[Video](https://www.youtube.com/watch?v=tpg35YgA9Gk&list=PLavJpcg8cl1Efw8x_fBKmfA2AMwjUaeBI&index=3)] [[Source](https://github.com/Snowflake-Labs/snowflake-demo-notebooks/blob/main/My%20First%20Notebook%20Project/My%20First%20Notebook%20Project.ipynb)]

Learn how to quickly get started with your first notebook project in less than
10 minutes.

  * [Visual Data Stories with Snowflake Notebooks](https://quickstarts.snowflake.com/guide/visual_data_stories_with_snowflake_notebooks/index.html) [[Video](https://www.youtube.com/watch?v=WJUNTudCsYM&list=PLavJpcg8cl1Efw8x_fBKmfA2AMwjUaeBI&index=4)] [[Source](https://github.com/Snowflake-Labs/snowflake-demo-notebooks/blob/main/Visual%20Data%20Stories%20with%20Snowflake%20Notebooks/Visual%20Data%20Stories%20with%20Snowflake%20Notebooks.ipynb)]

Learn how you can create compelling data narratives using visualizations,
Markdown, images, and interactive data apps all within your notebook,
alongside your code and data.

### Highlighted use cases¶

Check out highlighted use cases for data science, data engineering and ML/AI
in [Github](https://github.com/Snowflake-Labs/notebook-demo).

[![Data engineering on Snowflake Notebook](../../_images/data-eng-notebooks-tile.png)](../../_images/data-eng-notebooks-tile.png) | [Data Engineering](https://github.com/Snowflake-Labs/snowflake-demo-notebooks/blob/main/README.md#data-engineering) Develop, manage, schedule and run scalable data pipelines with SQL and Snowpark.  
---|---  
[![Data science using Snowflake Notebook](../../_images/data-science-notebooks-tile.png)](../../_images/data-science-notebooks-tile.png) | [Data Science](https://github.com/Snowflake-Labs/snowflake-demo-notebooks/blob/main/README.md#data-science) Explore, visualize, and analyze your data with Python and SQL.  
[![Machine learning using Snowflake Notebook](../../_images/ml-notebooks-tile.png)](../../_images/ml-notebooks-tile.png) | [Machine Learning and AI](https://github.com/Snowflake-Labs/snowflake-demo-notebooks/blob/main/README.md#machine-learning) Feature Engineering, model training, and development with Cortex and Snowpark ML.  
  
Note

These quickstarts are only shown as examples. Following along with the example
may require additional rights to third-party data, products, or services that
are not owned or provided by Snowflake. Snowflake does not guarantee the
accuracy of these examples.

### Additional resources¶

  * For notebook demos, tutorials and examples, see collection of Snowflake Notebooks demos in [GitHub](https://github.com/Snowflake-Labs/notebook-demo).

  * To view tutorial videos, see the Snowflake Notebooks [YouTube playlist](https://www.youtube.com/playlist?list=PLavJpcg8cl1Efw8x_fBKmfA2AMwjUaeBI).

  * To learn about SQL commands to create, execute and show notebooks, see Snowflake Notebooks [API reference](../../sql-reference/commands-notebook).

  * Looking for reference architectures, industry specific use-cases and solutions best practices using Notebooks? See [Notebooks examples](https://developers.snowflake.com/solutions/?_sft_technology=notebooks) in the Snowflake Solution Center.

