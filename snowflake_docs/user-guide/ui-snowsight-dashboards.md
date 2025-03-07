# Visualizing data with dashboards¶

You can use dashboards to visualize and communicate query results using charts
in [Snowsight](ui-snowsight). Dashboards are flexible collections of charts
arranged as tiles. The charts are generated by query results and can be
customized. You can also create dashboard tiles from charts in worksheets. For
more details, see [Visualizing worksheet data](ui-snowsight-visualizations).

## Create a dashboard¶

You can create an empty dashboard or create a dashboard directly from a
worksheet.

### Create an empty dashboard¶

To create an empty dashboard, complete the following steps:

  1. Sign in to Snowsight.

  2. In the navigation menu, select Projects » Dashboards.

  3. Select \+ Dashboard.

  4. Enter a name for the dashboard, and then select Create Dashboard.

### Create a dashboard from an existing worksheet¶

You can also use an existing worksheet to create a dashboard.

When you use a worksheet to create a dashboard, the worksheet is removed from
the list of worksheets and can only be accessed from the dashboard. The
worksheet query is stored in the dashboard and can be modified in that
context.

To create a dashboard using an existing worksheet, complete the following
steps:

  1. [Open a worksheet](ui-snowsight-worksheets-gs.html#label-snowsight-open-worksheet).

  2. Hover over the name of the worksheet and select [![more actions for worksheet](../_images/snowsight-worksheet-vertical-ellipsis.png)](../_images/snowsight-worksheet-vertical-ellipsis.png), and then select Move to.

  3. Select New dashboard.

  4. Enter a name for the dashboard, and then select Create Dashboard.

> The dashboard opens, displaying a tile based on the worksheet you used.

Note

If the worksheet is shared with other users, those users lose access to the
worksheet when you create a dashboard because the worksheet is removed when
the dashboard is created. Permissions on the worksheet are revoked and links
to the worksheet no longer function. For more details about sharing
dashboards, see Share dashboards.

## About using dashboards¶

After you create a dashboard, you can manage, add tiles, filters, and share
the dashboard with other users.

Tiles visualize data on your dashboards as charts and tables. Hover over
charts to view details about each data point.

[![Example tile showing a noisy line chart with historical orders grouped by
day](../_images/snowsight-dashboards-tile.png)](../_images/snowsight-
dashboards-tile.png)

### Open a dashboard¶

To open a dashboard, complete the following steps:

  1. Sign in to Snowsight.

  2. In the navigation menu, select Projects » Dashboards.

  3. Locate the dashboard that you want to open:

     * The Recent tab displays the dashboards you opened most recently.

     * The Shared With Me tab displays dashboards that your colleagues shared with you.

     * The My dashboards tab displays dashboards that you created and own.

You can also search the names and contents of worksheets and dashboards.

## Manage a dashboard¶

While viewing a dashboard, you can take the following actions on the
dashboard:

  * Select the dashboard name to rename, duplicate, or delete the dashboard.

  * Select + to add a tile to the dashboard. See Add a tile to a dashboard.

  * Select [![Show or hide filter](../_images/snowsight-query-history-filter.png)](../_images/snowsight-query-history-filter.png) to show, hide, and manage custom filters that you can use in queries on the dashboard. For more details on filters, see [Filter query results in dashboards and worksheets](ui-snowsight-filters.html#label-using-filters).

  * Use the context selector [![Context selector to use to select role and warehouse. Shows the currently-selected role and warehouse. If there are no defaults, displays PUBLIC and No warehouse selected.](../_images/snowsight-dashboards-context-selector.png)](../_images/snowsight-dashboards-context-selector.png) to specify the role and warehouse to use for running the queries in the dashboard.

  * Select Share to share the dashboard with other Snowsight users. See Share dashboards for details.

  * Select Run to run all the queries for the dashboard tiles.

### Add a tile to a dashboard¶

To add a tile to a dashboard, complete the following steps:

  1. Open a dashboard.

  2. Select + ([![Add a dashboard tile](../_images/snowsight-dashboards-add-tile-icon.png)](../_images/snowsight-dashboards-add-tile-icon.png)).

  3. Select New Tile from Worksheet.

[![For assistive technology, the add tile button.](../_images/snowsight-
dashboards-add-tile.png)](../_images/snowsight-dashboards-add-tile.png)

A blank worksheet opens, overlaying the dashboard.

  4. Use the worksheet to build your query.

To learn more about queries and worksheets, see [Querying data using
worksheets](ui-snowsight-query).

  5. When you finish writing your query, select Return to <dashboard name> to save your worksheet and add it to the dashboard.

### Add an existing worksheet to a dashboard¶

To add an existing worksheet as a tile, complete the following steps:

  1. [Open a worksheet](ui-snowsight-worksheets-gs.html#label-snowsight-open-worksheet).

  2. On the worksheet tab, select [![More options](../_images/snowsight-worksheet-explorer-ellipsis.png)](../_images/snowsight-worksheet-explorer-ellipsis.png), and then select Move to.

  3. Select an existing dashboard.

The worksheet is added to the dashboard and removed from the list of
worksheets. A tile showing a chart for the worksheet displays on the
dashboard.

### Rearrange the order of tiles¶

By default, tiles are added to the bottom of the dashboard.

To rearrange the tiles on a dashboard, drag a tile to a new position. As you
drag the tile, a preview of the new position appears.

### Edit charts¶

To edit a chart that appears in a tile, complete the following steps:

  1. From the tile menu ([![More options](../_images/snowsight-worksheets-gs-options.png)](../_images/snowsight-worksheets-gs-options.png)), select View Chart.

The chart opens in a worksheet.

  2. Make changes to the chart. To learn more about charts, see [Visualizing worksheet data](ui-snowsight-visualizations).

  3. When you are finished editing the chart, select Return to <dashboard name> to save your changes and return to the dashboard.

### Edit queries¶

To edit the query used for a tile, complete the following steps:

  1. From the tile menu ([![More options](../_images/snowsight-worksheets-gs-options.png)](../_images/snowsight-worksheets-gs-options.png)), select Edit query.

The query opens in a worksheet window.

  2. Make changes to the query. For more about editing queries in worksheets, see [Querying data using worksheets](ui-snowsight-query).

  3. When you finish editing the query, select Return to <dashboard name> to save your changes and return to the dashboard.

### Configure a tile display¶

By default, when you move a worksheet to a dashboard, the corresponding tile
displays a chart.

To change the tile from a chart to a table of the query results, complete the
following steps:

  1. Remove the tile.

  2. Add a tile and drag the table version of your query to your dashboard.

If a tile displays a table and you want to add a chart tile based on the same
query, edit the query of the tile by completing the following steps:

  1. From the tile menu ([![More options](../_images/snowsight-worksheets-gs-options.png)](../_images/snowsight-worksheets-gs-options.png)), select Edit Query.

  2. Select Chart.

  3. Select Return to <dashboard name> to save your changes and return to the dashboard.

A new tile is added at the bottom of the dashboard with a chart view of the
table. For details on making changes to the chart, see Edit charts.

### Duplicate a tile¶

To duplicate a tile, complete the following steps:

  * From the tile menu ([![More options](../_images/snowsight-worksheets-gs-options.png)](../_images/snowsight-worksheets-gs-options.png)), select Duplicate Tile.

A copy of the tile appears at the bottom of the dashboard.

### Remove a tile¶

When you want to remove a tile from your dashboard, but still preserve the
underlying query, complete the following step:

  * To remove a tile, on the tile menu ([![More options](../_images/snowsight-worksheets-gs-options.png)](../_images/snowsight-worksheets-gs-options.png)), select Unplace Tile.

The tile is removed from the dashboard, but remains available to add to the
dashboard from the Add tile menu.

### Delete a tile¶

Warning

Deleting a tile from a dashboard also deletes the underlying queries. This
action cannot be undone. If you want to remove the tile but preserve the
query, see Remove a tile.

If you delete a tile with a query that is used by another tile, such as a
table and chart view of the same query results, both tiles are deleted.

To delete a tile, complete the following steps:

  1. From the tile menu ([![More options](../_images/snowsight-worksheets-gs-options.png)](../_images/snowsight-worksheets-gs-options.png)), select Delete.

  2. Select Delete to permanently delete the tile and its underlying query from the dashboard.

## Share dashboards¶

Editors and owners can share a dashboard with individual collaborators or by
enabling and using link sharing.

The queries that drive dashboards in Snowsight use unique sessions with
assigned roles and warehouses. To view shared dashboards, the Snowflake user
must use the same role as the session context for the queries that drive the
dashboard.

To share a dashboard, complete the following steps:

  1. Open a dashboard.

  2. Select Share.

  3. Enter the names or usernames of the Snowflake users you want to invite to use your dashboard. The list only shows users that have previously signed in to Snowsight. To share with someone who has not yet signed in to Snowsight, share a link instead (ensure that you have enabled link sharing).

  4. Optionally, set how people with the link can interact with the dashboard. By default, people with the link cannot view the dashboard. For example, you can choose to allow people to view the results on the dashboard, but not run the underlying queries.

  5. Optionally, select Get Link to get a link to your dashboard that you can share with others.

  6. Select Done.

Caution

When you run a dashboard, the results are cached. Anyone with access to the
dashboard can view these results if they have the same primary role that was
used to generate them. However, if the dashboard queries are data protected by
masking or row access policies, or if secondary roles are active when you
execute the query, the cached results may include data that other users with
access to the dashboard might not be able to generate themselves.

For more details about sharing permissions for dashboards and worksheets, see
[Permissions for shared worksheets](ui-snowsight-worksheets.html#label-
sharing-worksheets-permissions). You cannot organize dashboards into folders.

