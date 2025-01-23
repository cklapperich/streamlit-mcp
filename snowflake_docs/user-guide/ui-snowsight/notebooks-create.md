# Create Snowflake Notebooks¶

Feature — Generally Available

Generally available in Amazon Web Services (AWS), Microsoft Azure, and Google
Cloud Platform (GCP) commercial regions.

This topic describes how to create Snowflake Notebooks on a warehouse runtime.
You can also create Snowflake Notebooks on container runtime for ML. For
details, see [Create a notebook on Container Runtime for ML](notebooks-on-
spcs.html#label-create-notebook-on-spcs).

You can access notebooks through [Snowsight](../ui-snowsight), where you can:

  * Create a new notebook.

  * Open an existing notebook.

Tip

You can also create a notebook using SQL. See [CREATE NOTEBOOK](../../sql-
reference/sql/create-notebook).

## Prerequisites¶

  * You have [set up and enabled notebooks](notebooks-setup.html#label-notebooks-setup).

  * You are using a role with the [required privileges](notebooks-setup.html#label-notebooks-create-resources-grant-privileges). If you are creating a private notebook, you meet [the prerequisites](notebooks-setup.html#label-notebooks-prerequisites-private-notebooks).

## Create a new notebook¶

You can create a new notebook by selecting \+ Notebook, or you can import a
file with the `*.ipynb` extension. This could be a notebook file created from
an application outside of Snowflake.

To create a new notebook, follow these steps:

  1. Sign in to [Snowsight](../ui-snowsight).

  2. Select Projects » Notebooks in the left-side navigation menu.

  3. Select \+ Notebook.

  4. You have several options when creating a new notebook:

     * To create a role-owned notebook, select your current primary role from the Creating as drop-down list.

     * To create a [private user-owned notebook](notebooks-private), select your username from the Creating as drop-down list.

     * To create a notebook from an existing file, such as a notebook file that was created from an application outside of Snowflake, select the down arrow next to \+ Notebook and then select Import .ipynb file. Open the file to import.

Note

If your notebook imports Python packages, you must add the packages to the
notebook before you can run the imported notebook. See [Import Python packages
to use in notebooks](notebooks-import-packages). If the package you use in
your imported notebook is not available, your code might not run. For
information about adding cells, see [Develop and run code in Snowflake
Notebooks](notebooks-develop-run).

  5. Enter a name for your notebook.

Note

If you’re using an AWS region, you can specify the runtime environment for
your notebook: either the [Container Runtime for ML](notebooks-on-
spcs.html#label-create-notebook-on-spcs) or the warehouse runtime.

  6. Select a Notebook location. This is the database and schema in which to store your notebook. These cannot be changed after you create the notebook. If you create a private notebook after personal databases are enabled for your account, your personal database will be pre-populated by default under Notebook location. However, if you are creating a private notebook and there is only one schema in your personal database, the Notebook location options are not available.

Note

The Notebook location dropdown might not show databases that were created
after the Create Notebook dialog was opened. If you cannot find your recently
created database, schema, or warehouse, try reloading your browser window.

Querying data in the notebook is not restricted to this location. In the
notebook, you can query data in any location you have access to. To specify
the location, run [USE WAREHOUSE](../../sql-reference/sql/use-warehouse) and
[USE SCHEMA](../../sql-reference/sql/use-schema).

  7. Select Run on warehouse or Run on container as your Python environment.

  8. (Optional) Select a Query warehouse to run any SQL and Snowpark queries issued by the notebook.

  9. Select Create to create and open your notebook.

For information about adding cells, see [Develop and run code in Snowflake
Notebooks](notebooks-develop-run).

## Create a notebook from a Git repository¶

You can sync your notebook development with a Git repository. Then you can
create Snowflake Notebooks from notebooks in that Git repository.

To create a notebook from a file in Git, see [Create a notebook from a file in
a Git repository](notebooks-snowgit.html#label-snowsight-notebooks-git-
create).

## Duplicate an existing notebook¶

You can duplicate existing Snowflake Notebooks. Duplicating notebooks may be
useful if you want to, for example, test out some code changes without
altering the original notebook version.

When you duplicate a notebook, the copied notebook is created with the same
role and warehouse as the original notebook, and is contained in the same
database and schema as the original notebook. Because of this, you cannot
duplicate a notebook to move it to a different database and schema, or to
change ownership.

To duplicate a notebook, complete the following steps:

  1. Sign in to [Snowsight](../ui-snowsight).

  2. Select Projects » Notebooks.

  3. Open the notebook that you want to duplicate.

  4. Select the vertical ellipsis [![more actions for worksheet](../../_images/snowsight-worksheet-vertical-ellipsis.png)](../../_images/snowsight-worksheet-vertical-ellipsis.png) menu, then select Duplicate.

  5. (Optional) Enter a name for the duplicate notebook, then select Duplicate.

  6. In the confirmation dialog, select Close to return to the original notebook, or Open notebook to open the duplicate notebook.

## Open an existing notebook¶

To open an existing notebook, follow these steps:

  1. Sign in to Snowsight.

  2. Select Notebooks.

Note

Recently used notebooks also appear in Snowsight. Under Recently viewed,
select Notebooks.

  3. Review the list of notebooks.

You can see all notebooks owned by your active role or owned by a role
inherited by your active role.

  4. Select a notebook to open it for editing.

For details about editing notebooks, see [Develop and run code in Snowflake
Notebooks](notebooks-develop-run).

When you open a notebook, you can see cached results from the last time you
ran any cells in the notebook. The notebook is in the Not connected state by
default, but if you select that state or run any cell, your notebook connects
to your virtual warehouse.

