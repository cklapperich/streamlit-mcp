# Limitations with Notebooks¶

Feature — Generally Available

Generally available in Amazon Web Services (AWS), Microsoft Azure, and Google
Cloud Platform (GCP) commercial regions.

This topic describes unsupported features and limitations of Snowflake
Notebooks.

  * Only one executable `ipynb` file is permitted within each notebook. Multiple executables are not permitted.

  * You cannot use the [GRANT OWNERSHIP](../../sql-reference/sql/grant-ownership) or [USAGE](../../sql-reference/account-usage) commands to grant ownership or usage on a notebook to a different role.

  * Streamlit components and widgets, such as slider values, do not retain their state if you refresh the browser window, open the notebook in a new tab, or close and reopen the current tab.

  * [UNDROP <object>](../../sql-reference/sql/undrop) is not supported for Snowflake Notebooks. After you drop a notebook, it cannot be restored.

  * When you create a notebook from a repository, only the selected notebook is executable. Any other notebooks in the repository can be selected and edited, but they are not executable.

  * Notebooks cannot be created or executed by [SNOWFLAKE database roles](../../sql-reference/snowflake-db-roles).

  * Notebooks do not support [replication](../account-replication-config).

  * Renaming a notebook will invalidate the notebook URL.

  * Snowflake Notebooks are hosted in a third-party domain to provide increased security. In Safari, you must enable third-party cookies to allow reconnection to a running notebook after losing a connection. To enable this setting, in Safari select Settings » Privacy, and then clear the Prevent cross-site tracking checkbox.

