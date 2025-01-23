# Monitor data loading activity by using Copy History¶

You can monitor data loading activity for all tables in your account, or for a
specific table, by using Snowsight or SQL.

  * Monitor data loading for your account by using Copy History.

  * Monitor data loading for a table by using Copy History.

## Monitor data loading for your account by using Copy History¶

Review the data loading activity that has occurred over the last 365 days for
all tables in your account by using the Copy History page in Snowsight or the
[COPY_HISTORY view](../sql-reference/account-usage/copy_history) in the
ACCOUNT_USAGE schema of the SNOWFLAKE database.

The account-level data loading activity has a latency of up to 2 hours and
includes bulk data loading performed using COPY INTO statements, continuous
data loading using pipes, and files loaded through the web interface.

### Prerequisites¶

  * You must use a role with access to the SNOWFLAKE database. See [Enabling other roles to use schemas in the SNOWFLAKE database](../sql-reference/account-usage.html#label-enabling-usage-for-other-roles).

  * Viewing the Copy History page in Snowsight or querying the SNOWFLAKE database requires a warehouse. If you have a default warehouse for your user profile, Snowsight uses that warehouse. You can switch warehouses at any time.

### Review account-level Copy History¶

Note

You must use a role with access to the SNOWFLAKE database. See [Enabling other
roles to use schemas in the SNOWFLAKE database](../sql-reference/account-
usage.html#label-enabling-usage-for-other-roles).

  1. Sign in to Snowsight.

  2. Select Monitoring » Copy History.

The Copies Over Time graph provides a visualization of data loading over a
given period of time. By default, the graph shows a 7-day history with each
bar on the graph representing one day.

Select a bar on the graph to filter the Copies table by that day.

For more details about data loading activity, you can review the Copies table.
The table includes the following information:

  * File Name displays the name of the file loaded.

  * Loaded displays the timestamp in your local timezone for when the data was loaded.

  * Status displays the status of the data load. You can hover over data loads with a status of Failed to review error details.

  * Database displays the database into which data was loaded.

  * Schema displays the schema into which data was loaded.

  * Table displays the table into which data was loaded.

  * Pipe displays the pipe used to load data, if applicable.

  * Size displays the size of the data loaded, rounded to the nearest decimal point in KB, MB, GB, or TB. For example, if you load 45800 bytes, the size is listed as 45.8KB.

  * Rows displays the number of rows loaded, rounded to the nearest decimal point in thousands, millions, and so on. For example, if you load 2000 rows of data, the rows are listed as 2K.

  * Location displays a link to the location from which the data was loaded. For example, a link to an AWS S3 bucket added as an external stage, or an internal named stage. Hover over the link to see the stage name, or select the link to copy the path to the stage.

To more easily identify specific data loading activities, you can search and
filter the Copy History page.

You can filter by the following:

  * Time range, up to 365 days (1 year)

  * Status of the data loading activity, such as All (default), In progress, Loaded, Failed, Partially loaded, and Skipped.

  * The location of the data:

    * Database

    * Schema

    * Pipe

You can also search the column values in the Copies table for specific data
loading activities.

Select [![Open underlying SQL query in worksheet](../_images/open-in-
worksheet.png)](../_images/open-in-worksheet.png) (Open underlying SQL query
in worksheet) to open a worksheet that contains the SQL query used to populate
the table. The SQL query is based on the filters you select.

When you select a specific data load activity in the Copies table, Snowsight
opens the table-level Copy History. See Monitor data loading for a table by
using Copy History. You might see newer results in that table due to reduced
latency, but you can only review 14 days of activity.

## Monitor data loading for a table by using Copy History¶

Review the data loading activity that has occurred over the last 14 days for a
specific table in a database by using the Copy History details for the table
in Snowsight or the [COPY_HISTORY](../sql-reference/functions/copy_history)
table function.

The table-level data loading activity has very low latency and includes bulk
data loading performed using COPY INTO statements, continuous data loading
using pipes, and files loaded through the web interface.

### Prerequisites¶

You must use a role that has one of the following:

  * The MONITOR privilege on your Snowflake account.

  * The USAGE privilege on the database and schema that contain the table, and any privilege on the table.

If you use a role that does not have the MONITOR privilege on the pipe, pipe
details are masked as NULL.

Viewing the Copy History details for a database in Snowsight or running the
table function requires a warehouse. If you have a default warehouse for your
user profile, Snowsight uses that warehouse. You can switch warehouses at any
time.

### Review table-level Copy History¶

To review the copy history for a table, locate and open the table for which
you want to review activity:

  1. Sign in to Snowsight.

  2. Select Data » Databases.

  3. Locate and select the database with the table for which you want to review activity.

  4. Select the schema with the table for which you want to review activity.

  5. Select Tables and select the table.

  6. In the table details, select the Copy History tab.

The Copies Over Time graph provides a visualization of data loading over a
given period of time. By default, the graph shows a 7-day history with each
bar on the graph representing one day.

Select a bar on the graph to filter the Copies table by that day.

You can filter by the following:

  * Time range, up to 14 days.

  * Status of the data loading activity, such as All (default), In progress, Loaded, Failed, Partially loaded, and Skipped.

  * The pipe used to load the data.

You can also search the column values in the Copies table for specific data
loading activities.

Select [![Open underlying SQL query in worksheet](../_images/open-in-
worksheet.png)](../_images/open-in-worksheet.png) (Open underlying SQL query
in worksheet) to open a worksheet that contains the SQL query used to populate
the table. The SQL query is based on the filters you select.

