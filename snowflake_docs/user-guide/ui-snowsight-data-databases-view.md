# Working with views in Snowsight¶

You can work with [views](views-introduction) in SQL or in Snowsight. For
details about the available SQL commands for working with views, see [Table,
view, & sequence DDL](../sql-reference/ddl-table).

For any Snowflake view, you can open Data » Databases and search for or browse
to the view. Select the view to explore details about the view, the columns
defined in the view, and preview the data in the view.

You must have the relevant [view privileges](security-access-control-
privileges.html#label-view-privileges) to access and manage the view in
Snowsight.

## Explore view details in Snowsight¶

After opening a view in Snowsight, you can do the following:

  * Identify the type of view and when the view was last created. Hover over the time details to see the exact creation date and time.

  * Review the SQL definition of the view on the View Details tab.

  * Manage privileges for the view in the Privileges section of the View Details tab. To manage privileges, see [Manage object privileges with Snowsight](security-access-control-configure.html#label-snowsight-manage-object-privileges).

  * Review the name, type, ordinal (order of the column in the view), tags, and masking policies applied to the view on the Columns tab. To add tags and masking policies to a view, see [Create and assign tags](object-tagging.html#label-object-tagging-create-assign).

## Manage a view in Snowsight¶

You can perform the following basic management tasks for a view in Snowsight:

  * To edit the view name or add a comment, select [![More options](../_images/snowsight-worksheet-explorer-ellipsis.png)](../_images/snowsight-worksheet-explorer-ellipsis.png) » Edit.

  * To drop the view, select [![More options](../_images/snowsight-worksheet-explorer-ellipsis.png)](../_images/snowsight-worksheet-explorer-ellipsis.png) » Drop.

  * To transfer ownership of the view to another role, select [![More options](../_images/snowsight-worksheet-explorer-ellipsis.png)](../_images/snowsight-worksheet-explorer-ellipsis.png) » Transfer Ownership.

## Preview data in a view¶

You can preview up to the first 100 rows of a view on the Data Preview tab for
the view.

Note

If your view is complex, you might not see a data preview. Snowsight queries
the view for the data preview and waits for up to 300 seconds for results to
be returned. If the query takes longer than 300 seconds to complete, Snowsight
cancels the query and displays no preview data.

Select [![More options](../_images/snowsight-worksheet-explorer-
ellipsis.png)](../_images/snowsight-worksheet-explorer-ellipsis.png) to
manipulate the preview data:

  * Sort the data in ascending or descending order.

  * Increase or decrease the decimal precision.

  * Show thousands separators in numbers.

  * Display the data in the column as percentages.

The options available to you depend on the type of data in the column.

Note

The preview requires a warehouse. By default, Snowsight uses the default
warehouse for your user profile, or you can select a different warehouse.

