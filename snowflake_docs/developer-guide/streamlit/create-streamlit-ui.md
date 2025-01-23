# Create and deploy Streamlit apps using Snowsight¶

Streamlit in Snowflake provides a Python editor in Snowsight where you can
write, edit, and run code for a Streamlit app. The editor provides auto-
completion and displays documentation for Streamlit and Snowpark functions.

Ensure that you’ve reviewed the [prerequisites](getting-started.html#label-
streamlit-prereqs) before you use Snowsight to work with Streamlit apps.

Note

You can create single-page Streamlit apps by using Snowsight, but to deploy a
multi-page Streamlit app, you must use SQL commands. See [Create and deploy
Streamlit apps using SQL](create-streamlit-sql) for details.

After deploying a Streamlit app, you can view the multi-page app in Snowsight.
See View a Streamlit app for more information.

## Create a Streamlit app by using Snowsight¶

  1. Sign in to [Snowsight](../../user-guide/ui-snowsight).

  2. In the left navigation bar, select Projects » Streamlit.

  3. Select \+ Streamlit.

The Create Streamlit App window opens.

  4. Enter a name for your app.

  5. In the Warehouse dropdown, select the warehouse where you want to run your app and execute queries.

  6. In the App location dropdown, select the database and schema for your app.

  7. Select Create.

The Streamlit in Snowflake editor opens an example Streamlit app in Viewer
mode. Viewer mode allows you to see how the Streamlit application appears to
users.

The Streamlit in Snowflake interface is divided into three panes:

  * Object browser: Allows you to see the databases, schemas, and views you have permissions to access.

  * Streamlit editor: Provides a Python editor for your Streamlit code.

  * Streamlit preview: Displays the running Streamlit app.

By default, only the Streamlit editor and preview panes are displayed. To
change the display, use the show/hide buttons in the lower-left corner of the
Streamlit in Snowflake editor.

## Run a Streamlit app in Streamlit in Snowflake¶

  * To update the content in the Streamlit preview pane, select Run.

## Manage packages for a Streamlit app¶

You can view, add, and remove external Python packages for your Streamlit app
by using the Streamlit editor in Snowsight.

### View the packages installed for a Streamlit app¶

  1. Sign in to [Snowsight](../../user-guide/ui-snowsight).

  2. In the navigation menu, select Projects » Streamlit.

  3. Select the Streamlit app whose packages you want to view.

  4. At the top of the Streamlit editor, select Packages.

Snowsight displays a list of installed packages.

### Select the Streamlit version to use in the Streamlit app¶

  1. Sign in to [Snowsight](../../user-guide/ui-snowsight).

  2. In the navigation menu, select Projects » Streamlit.

  3. Select the Streamlit app.

  4. Select Edit.

  5. At the top of the Streamlit editor, select Packages.

  6. Select the Streamlit version.

### Add a supported Python package to a Streamlit app¶

By default, Streamlit in Snowflake installs the `python`, `snowflake-
snowpark`, and `streamlit` packages in your environment. You can use Snowsight
to add other packages. For a list of supported packages, see the [Snowflake
Anaconda Channel](https://repo.anaconda.com/pkgs/snowflake/).

  1. Sign in to [Snowsight](../../user-guide/ui-snowsight).

  2. In the navigation menu, select Projects » Streamlit.

  3. Select the Streamlit app to which you want to add a Python package.

  4. At the top of the Streamlit editor, select Packages.

  5. In the search text field, select a package from the list of supported packages, or enter the name of the package.

### Remove a package from a Streamlit app¶

  1. Sign in to [Snowsight](../../user-guide/ui-snowsight).

  2. In the navigation menu, select Projects » Streamlit.

  3. Select the Streamlit app from which you want to remove a Python package.

  4. At the top of the Streamlit editor, select Packages.

  5. Select X next to the package you want to remove.

Note

The `python`, `snowflake-snowpark`, and `streamlit` packages are installed by
default and cannot be removed.

## View a Streamlit app¶

For information about the privileges required to view a Streamlit app, see
[Privileges required to view a Streamlit app](getting-started.html#label-
streamlit-access-privs-view).

  1. Sign in to [Snowsight](../../user-guide/ui-snowsight).

  2. In the navigation menu, select Projects » Streamlit.

  3. Select the Streamlit app you want to view.

The main Streamlit app opens in the Streamlit in Snowflake viewer.

  4. Optional: If you are viewing a multi-page Streamlit app, select a tab to view additional pages.

## Manage Streamlit apps¶

After creating a Streamlit app, you can perform additional related tasks that
are described in the following sections.

### Edit a Streamlit app¶

  1. Sign in to [Snowsight](../../user-guide/ui-snowsight).

  2. In the navigation menu, select Projects » Streamlit.

  3. Select the Streamlit app you want to edit.

The main Streamlit app opens in the Streamlit in Snowflake viewer.

  4. Select Edit.

The Streamlit editor opens.

  5. Update your application code.

  6. To view the changes you made to the app, select Run.

### Share a Streamlit app¶

You can share your Streamlit app with other Snowflake users assigned to a
specific role. Sharing your Streamlit app lets other users interact with your
application when it is running.

  1. Sign in to [Snowsight](../../user-guide/ui-snowsight).

  2. In the navigation menu, select Projects » Streamlit.

  3. Select the Streamlit app you want to share.

  4. Select Share.

The Share Streamlit window opens.

  5. Begin typing the name of the role you want to share your Streamlit app with.

  6. Select the name of the role.

The new role appears in the list of roles. Add additional roles as necessary.

  7. To copy the URL to your Streamlit app, select Copy to clipboard.

You can then send this URL through email or text.

  8. Select Done.

### Rename a Streamlit app¶

  1. Sign in to [Snowsight](../../user-guide/ui-snowsight).

  2. In the navigation menu, select Projects » Streamlit.

  3. Select the Streamlit app you want to rename.

  4. Select Edit.

  5. Select the name of the app in the upper-left corner.

  6. Enter the new name in the text box.

  7. Click outside the text box to commit the change.

### Change the warehouse of a Streamlit app¶

While developing, testing, and running a Streamlit app, you might want to
modify the warehouse used to run the app and queries. For example, you might
need to use a warehouse with more capacity to handle queries run by the app.

  1. Sign in to [Snowsight](../../user-guide/ui-snowsight).

  2. In the navigation menu, select Projects » Streamlit.

  3. Select the Streamlit app whose warehouse you want to change.

  4. Select the name of the app in the upper-left corner.

  5. Select the new warehouse from the dropdown list.

### Delete a Streamlit app¶

Deleting a Streamlit app permanently removes it from Snowflake. Any users with
whom you have shared the app will no longer be able to view and interact with
the Streamlit app. Before deleting a Streamlit app, ensure that you have saved
your application code outside of Snowflake.

  1. Sign in to [Snowsight](../../user-guide/ui-snowsight).

  2. In the navigation menu, select Projects » Streamlit.

  3. Select the Streamlit app you want to delete.

  4. Select Edit.

  5. Select the name of the app in the upper-left corner.

  6. Select Delete, and then select Delete App.

Snowflake deletes the Streamlit app and displays the updated list of available
apps.

