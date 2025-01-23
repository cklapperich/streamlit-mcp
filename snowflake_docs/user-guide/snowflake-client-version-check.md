# Viewing Snowflake Client Versions¶

To view the version of the Snowflake client used to execute SQL statements in
Snowflake, you can use the Client Driver column on the Query History page in
Snowsight or the Client Info column on the History page in Classic Console.

Use this information to determine if the client versions actively used by
users in your account meet the [minimum requirements](../release-
notes/requirements). You can also use this information, if applicable, to
identify the client version when submitting cases to [Snowflake
Support](https://docs.snowflake.com/user-guide/contacting-support).

To view the versions of Snowflake clients used recently in your account:

  1. Sign in to [Snowsight](ui-snowsight) or the Classic Console.

  2. Switch to the ACCOUNTADMIN role.

Snowsight:

    

Open the user menu and select your active role, and then select »
ACCOUNTADMIN.

Classic Console:

    

Select the dropdown menu in the upper right (next to your login name) » Switch
Role » ACCOUNTADMIN.

  3. Open the Query History page:

Snowsight:

    

Select Monitoring » Query History.

Classic Console:

    

Select the History [![History tab](../_images/ui-navigation-history-
icon.svg)](../_images/ui-navigation-history-icon.svg) tab.

  4. Locate the column containing the version of the client or driver that submitted the query:

Snowsight:

    

Use the Client Driver column.

Classic Console:

    

Use the Client Info column.

If the column is not visible, select Columns and choose the column to display.

  5. Note the client version in the row for each SQL statement.

For clients and drivers, the column includes an icon that indicates if the
client version is supported, unsupported, or nearing the end of support. You
can hover over the icon to display a tooltip that indicates the current status
of the client version.

> [![Icons visible in the Classic Console that indicate whether or not the
> client version is supported](../_images/ui-monitor-queries-unsupported-
> clients.png)](../_images/ui-monitor-queries-unsupported-clients.png)

Snowflake updates the information on which versions are supported every three
months. See [Client versions & support policy](../release-notes/requirements).

