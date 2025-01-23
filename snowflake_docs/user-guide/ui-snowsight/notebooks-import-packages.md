# Import Python packages to use in notebooks¶

Feature — Generally Available

Generally available in Amazon Web Services (AWS), Microsoft Azure, and Google
Cloud Platform (GCP) commercial regions.

Snowflake Notebooks manages the Python packages used in your notebook
environment. You can import [third-party packages listed in the Snowflake
Anaconda channel](https://repo.anaconda.com/pkgs/snowflake/). For information
on importing packages in container runtime, see [Notebooks on Container
Runtime for ML](notebooks-on-spcs).

## Considerations for importing packages¶

  * Packages that you add to a notebook are available only to that notebook. If you want to use the same package in a different notebook, you must add the same packages again to that notebook.

  * Notebook will restart when you add a new package. Snowflake recommends that you add your package at the top of your notebook at the start of your analysis.

## Pre-installed packages¶

By default, Snowflake Notebooks use Python 3.9. Notebook environments come
pre-packaged with common libraries for data science and machine learning, such
as altair, pandas, numpy, [snowflake-snowpark-python](../../developer-
guide/snowpark/python/index), and
[Streamlit](https://docs.streamlit.io/library/api-reference).

## Import packages from Anaconda¶

After your organization administrator [accepts the terms](notebooks-
setup.html#label-notebooks-anaconda-terms), you can import libraries to use in
Snowflake Notebooks.

  1. Sign in to [Snowsight](../ui-snowsight).

  2. Select Projects » Notebooks.

  3. Select a specific notebook for which you want to install Python packages.

  4. Select Packages menu at the top of your notebook.

  5. Search for packages [listed in the Snowflake Anaconda channel](https://repo.anaconda.com/pkgs/snowflake/).

  6. Select a package to install it for use in your notebook, and optionally change the default package version in the list of Installed Packages.

Packages installed by you appear under Installed Packages.

[![Package selector.](../../_images/snowsight-ui-package-
selector.png)](../../_images/snowsight-ui-package-selector.png)

After the package is added, it may take some time to be installed. After it is
installed, you will see a confirmation message and you can then import and use
the libraries in a Python cell.

## Import packages from a Snowflake stage¶

You can import packages from a stage if the package you need is not part of
the pre-installed packages and is not available in the Anaconda channel.

The following limitations apply:

  * Package importer only works for Python modules and folders.

  * Wheel and tar.gz files are not supported.

  * Does not support any code which may be architecture dependent.

Follow these steps to add additional packages:

  1. Sign in to [Snowsight](../ui-snowsight).

  2. Select Projects » Notebooks.

  3. Select a specific notebook for which you want to install Python packages.

  4. Select the Packages menu at the top of your notebook.

  5. Select the Stage Packages tab.

  6. Enter the path to the file on your stage.

> [![Package selector.](../../_images/snowsight-ui-package-selector-
> stage.png)](../../_images/snowsight-ui-package-selector-stage.png)

After the package is added, you can now import and use the libraries in a
Python cell. See this in action in the [import packages from
stage](https://github.com/Snowflake-Labs/snowflake-demo-
notebooks/blob/main/Import%20Package%20from%20Stage/Import%20Package%20from%20Stage.ipynb)
tutorial notebook.

Now that all your packages are installed, [start coding in your
notebook](notebooks-develop-run).

