# Snowsight quick tour¶

In Snowsight, you can perform data analysis and engineering tasks, monitor
query and data loading and transformation activity, explore your Snowflake
database objects, and administer your Snowflake database, including managing
the cost and adding users and roles.

Snowsight lets you:

  * Build, test, and deploy Snowpark Python Worksheets.

  * Write queries and code, and take advantage of autocomplete for database objects and SQL functions in worksheets.

  * Organize worksheets into folders.

  * Share worksheets and dashboards with other users.

  * Visualize worksheet results in charts and dashboards.

  * Create and manage database objects such as databases, tables, stages, file formats, and more.

  * Manage costs and set budgets.

  * Review query history and data loading history.

  * See task graphs and run history.

  * Debug and rerun failed task graphs.

  * Monitor dynamic table graphs and refreshes.

  * Manage and create Snowflake users and roles and visualize a hierarchy of roles and their grants.

  * Perform data governance tasks like masking data, adding policies, and reviewing the governance of your data.

For more information about these and other tasks that you can perform, see
[Snowsight: The Snowflake web interface](ui-snowsight).

## Write SQL and Snowpark Python code in worksheets¶

Worksheets provide a simple way for you to write SQL queries (DML and DDL),
see the results, and interact with them. With a worksheet, you can do any of
the following:

  * Run ad hoc queries and other DDL/DML operations.

  * Write Snowpark Python code in a Python worksheet.

  * Review the query history and results of queries that you executed.

  * Examine multiple worksheets, each with its own separate session.

  * Export the results for a selected statement, while results are still available.

![If you select Worksheets in the navigation menu, you see a list of
worksheets, and you can select one to view the worksheet contents and update
the worksheet.](../_images/ui-tour-worksheet.png)

For more details, see:

  * [Getting started with worksheets](ui-snowsight-worksheets-gs)

  * [Work with worksheets in Snowsight](ui-snowsight-worksheets)

  * [Querying data using worksheets](ui-snowsight-query)

  * [Writing Snowpark Code in Python Worksheets](../developer-guide/snowpark/python/python-worksheets)

## Visualize query results with charts and dashboards¶

When you run a query in Snowsight, you can choose to view your results as a
chart. You can also create a collection of charts as a Dashboard, allowing you
to review your data more easily. Dashboards provide flexible collections of
charts arranged as tiles. Dashboard charts start with SQL to generate results
and associated charts. You can share these charts with others, modify the
charts, and display them as dashboard tiles.

![You can select Dashboards in the navigation menu to see a list of
dashboards. Select a dashboard, in this example a Groceries dashboard, to see
the dashboard. This image shows a dashboard with a bar chart tile showing the
quantity of apples, cheese, and other groceries purchased throughout a
year.](../_images/ui-tour-dashboard.png)

To learn more about charts, see [Visualizing worksheet data](ui-snowsight-
visualizations). To learn more about dashboards, see [Visualizing data with
dashboards](ui-snowsight-dashboards)

## Explore and manage your database objects¶

You can explore and manage your database objects in Snowsight as follows:

  * Explore databases and objects, including tables, functions, views, and more using the database object explorer.

  * Create objects like databases, tables, file formats, and more.

  * Search within the object explorer to browse database objects across your account.

  * Preview the contents of database objects like tables, and view the files uploaded to a stage.

  * Load files to an existing table, or create a table from a file so that you can start working with data in Snowflake faster.

![Select Data and then Databases to explore and manage your database objects.
By default, you see a list of databases to which your active role has
access.](../_images/ui-tour-data-databases.png)

To learn more, see:

  * [Explore and manage database objects in Snowsight](ui-snowsight-data)

  * [Load data using the web interface](data-load-web-ui)

  * [Staging files using Snowsight](data-load-local-file-system-stage-ui)

## Share and publish data products¶

Collaborate with users in other Snowflake accounts by sharing data and
application packages with them, or publishing those data products on the
Snowflake Marketplace. When you share or publish data products with a listing,
you can use auto-fulfillment to easily provide your data products in other
Snowflake regions.

As a consumer of data, you can access datasets and application packages shared
with your account or published on the Snowflake Marketplace, helping you
derive real time data insights without needing to set up a data pipeline or
write any code.

![The Data Products section contains a lot of options, one of which is the
Marketplace where you can explore available data products and
providers.](../_images/ui-tour-marketplace.png)

For more details, see:

  * [Create and configure shares](data-sharing-provider)

  * [About the Snowflake Native App Framework](../developer-guide/native-apps/native-apps-about)

  * [Access Provider Studio](https://other-docs.snowflake.com/en/collaboration/provider-studio-accessing.html)

  * [About Snowflake Marketplace](https://other-docs.snowflake.com/en/collaboration/collaboration-marketplace-about.html)

  * [Snowflake Partner Connect](ecosystem-partner-connect)

## Monitor activity in Snowsight¶

You can monitor and view query details, explore the performance of executed
queries, monitor data loading status and errors, review task graphs, and debug
and re-run them as needed. You can also monitor the refresh state of your
Dynamic Tables and review the various tagging and security policies that you
create to maintain data governance.

![The Monitoring section contains Query History, Copy History, Task History,
Dynamic Tables, and Governance.](../_images/ui-tour-monitoring.png)

For more information, see:

  * [Monitor query activity with Query History](ui-snowsight-activity)

  * [Monitor data loading activity by using Copy History](data-load-monitor)

  * [Viewing tasks and task graphs in Snowsight](ui-snowsight-tasks)

  * [About monitoring dynamic tables](dynamic-tables-monitor)

  * [Data Governance in Snowflake](../guides-overview-govern)

## Perform administrative tasks in Snowsight¶

Admin pages let you understand Snowflake data use, manage warehouses, monitor
resources, manage users and roles, administer Snowflake accounts, and more.

![You can manage Warehouses, perform Cost Management, access Users and Roles,
Accounts, and Contacts from the Admin menu.](../_images/ui-tour-admin.png)

For more information, see:

  * [Exploring overall cost](cost-exploring-overall)

  * [Working with warehouses](warehouses-tasks)

  * [Configuring access control](security-access-control-configure)

## Get account information and update your user profile from the user menu¶

To open the user menu, select your username.

[![Select your username to open the user menu and switch your active role,
switch accounts, open and update your profile, open Support and file support
cases, open the documentation, read the privacy notice, open the Classic
Console, or sign out.](../_images/ui-tour-account-menu.png)](../_images/ui-
tour-account-menu.png)

From the user menu, you can:

  * Change your active role.

  * Set your email address for notifications, if you are an account administrator.

  * Manage and update your user profile.

  * Switch languages for the user session, when additional languages have been enabled for your account.

  * File Support cases and access the Snowflake documentation.

  * Determine the organization, edition, cloud platform, and region of the current Snowflake account.

  * Access the account identifier and account URL.

  * Switch Snowflake accounts, if you have access to multiple accounts.

  * Open Classic Console.

  * Sign out, close your current session, and exit.

For more details, see:

  * [Overview of Access Control](security-access-control-overview) for information about roles and how they influence the actions you can take in Snowsight.

  * [Manage Snowflake Support cases](ui-support)

  * [Manage your user profile by using Snowsight](ui-snowsight-profile)

  * [Getting started with Snowsight](ui-snowsight-gs)

## Related videos¶

From Data to Decision with Snowsight

A Quick Look At The Latest Upgrade To Snowsight

