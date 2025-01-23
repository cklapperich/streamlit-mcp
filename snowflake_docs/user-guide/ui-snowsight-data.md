# Explore and manage database objects in Snowsight¶

You can explore and manage your database objects in Snowsight using the
_database object explorer_. The database object explorer contains a
hierarchical view of all databases in your account, the schemas for each
database, and the objects contained in each database and schema, organized by
type.

[![Snowsight database object explorer, rendered as a tree view, with
expandable objects such as schemas, tables, views, stages, and
more.](../_images/snowsight-data-database-object-
explorer.png)](../_images/snowsight-data-database-object-explorer.png)

To open the database object explorer:

  1. Sign in to Snowsight.

  2. Select Data » Databases.

  3. Explore your database objects in the database object explorer.

You can only see objects on which your active role has been granted, at a
minimum, the USAGE privilege. For more information about object privileges,
see [Access control privileges](security-access-control-privileges).

You can also explore database objects from the context of a worksheet. See
[Refer to database object names in worksheets](ui-snowsight-query.html#label-
worksheets-db-objects).

## Working with databases in Snowsight¶

When you select a database in the database object explorer, you can view
details about the database.

You must have the relevant [database privileges](security-access-control-
privileges.html#label-database-privileges) to access and manage the database
in Snowsight.

After opening a database in Snowsight, you can do the following:

  * Identify whether the database is a shared database.

  * Review the source of the database, such as local, share, Snowflake Marketplace, a data exchange, or privately shared by a provider.

  * Determine the owner role for the database.

  * Identify when the database was created. You can hover over the time details to see the exact creation date and time.

### Manage a shared database in Snowsight¶

For a shared database, you can review the Source details to learn more about
the sharing source:

  * For a direct share, you can see the name of the share from which the database was created, and the provider account name.

  * For a listing published on the Snowflake Marketplace or in a data exchange, you can see the name of the provider and the listing from which the database was created. Select the provider name to open the provider profile, or listing name to open the listing details on the Snowflake Marketplace or in the data exchange.

  * For a private listing, you can see the name of the provider and the listing from which the database was created. Select the listing name to open the listing details on the Private Sharing » Shared with You page.

You can perform the following basic management tasks for a shared database in
Snowsight:

  * To edit the database name or add a comment, select [![More options](../_images/snowsight-worksheet-explorer-ellipsis.png)](../_images/snowsight-worksheet-explorer-ellipsis.png) » Edit.

  * To drop the database, select [![More options](../_images/snowsight-worksheet-explorer-ellipsis.png)](../_images/snowsight-worksheet-explorer-ellipsis.png) » Drop. This removes the database created from the share or listing.

  * Review and manage privileges in the Privileges section of the Database Details tab. To manage privileges, see [Manage object privileges with Snowsight](security-access-control-configure.html#label-snowsight-manage-object-privileges).

### Manage a local database in Snowsight¶

You can perform the following basic management tasks for a database in
Snowsight:

  * To edit the database name or add a comment, select [![More options](../_images/snowsight-worksheet-explorer-ellipsis.png)](../_images/snowsight-worksheet-explorer-ellipsis.png) » Edit.

  * To drop the database, select [![More options](../_images/snowsight-worksheet-explorer-ellipsis.png)](../_images/snowsight-worksheet-explorer-ellipsis.png) » Drop.

  * To transfer ownership of the database to another role, select [![More options](../_images/snowsight-worksheet-explorer-ellipsis.png)](../_images/snowsight-worksheet-explorer-ellipsis.png) » Transfer Ownership

  * Review and manage privileges for the database in the Privileges section of the Database Details tab. To manage privileges, see [Manage object privileges with Snowsight](security-access-control-configure.html#label-snowsight-manage-object-privileges).

  * To create a schema for the database, select \+ Schema. For more information, see [CREATE SCHEMA](../sql-reference/sql/create-schema).

For accounts using private connectivity, you can also select [![More
options](../_images/snowsight-worksheet-explorer-
ellipsis.png)](../_images/snowsight-worksheet-explorer-ellipsis.png) » Enable
Replication to enable replication of the database to another account. For all
other accounts, use a [replication or failover group](account-replication-
intro.html#label-replication-and-failover-groups). For more information, see
[Create a replication or failover group using Snowsight](account-replication-
config.html#label-create-replication-failover-group-using-ui).

### Review the schemas in a database¶

To review the schemas in the database, select the Schemas tab. A table of
schemas contained in the database appears. On this tab, you can do the
following:

  * Search for a schema name.

  * Review and sort by schema name, owner role, or date created.

  * Manage the schema.

  * Hover over the [![Comment icon](../_images/snowsight-admin-user-comment.png)](../_images/snowsight-admin-user-comment.png) to read a comment on the schema.

Select a schema in the table to open the Schema Details page. See Explore
schema details in Snowsight.

## Explore schema details in Snowsight¶

For any Snowflake schema, you can navigate to Data » Databases to open the
database object explorer and search for or browse to the database schema.
Select the schema to explore details about the schema, the objects contained
in the schema, and create objects in the schema.

You can work with schemas in SQL or in Snowsight. For details about the
available SQL commands for working with schemas, see [Database, schema, and
share commands](../sql-reference/commands-database).

You must have the relevant [schema privileges](security-access-control-
privileges.html#label-security-access-control-privileges-schema-privileges) to
access and manage the database schema in Snowsight.

For each schema, you can view basic details for the objects contained in the
schema. See Review and manage schema objects.

### Manage a schema in Snowsight¶

You can perform the following basic management tasks for a schema in
Snowsight:

  * To edit the schema name or add a comment, select [![More options](../_images/snowsight-worksheet-explorer-ellipsis.png)](../_images/snowsight-worksheet-explorer-ellipsis.png) » Edit.

  * To clone the schema, select [![More options](../_images/snowsight-worksheet-explorer-ellipsis.png)](../_images/snowsight-worksheet-explorer-ellipsis.png) » Clone.

  * To drop the schema, select [![More options](../_images/snowsight-worksheet-explorer-ellipsis.png)](../_images/snowsight-worksheet-explorer-ellipsis.png) » Drop.

  * To transfer ownership of the schema to another role, select [![More options](../_images/snowsight-worksheet-explorer-ellipsis.png)](../_images/snowsight-worksheet-explorer-ellipsis.png) » Transfer Ownership.

  * Review and manage privileges for the schema in the Privileges section of the Schema Details tab. To manage privileges, see [Manage object privileges with Snowsight](security-access-control-configure.html#label-snowsight-manage-object-privileges).

### Create schema objects in Snowsight¶

To create objects in a database schema using Snowsight, do the following:

Note

You must use a role granted the relevant privileges to create objects in the
schema. See [Schema privileges](security-access-control-privileges.html#label-
security-access-control-privileges-schema-privileges).

  1. Sign in to Snowsight.

  2. Select Data » Databases.

  3. Locate and select the database schema in which you want to create an object.

  4. On the schema details page, select Create and then select the object that you want to create.

For most objects, a worksheet opens with template SQL to create the object you
selected. Customize the SQL and create the object.

     * If you choose to create a table from a file, see [Create a new table using Snowsight](data-load-web-ui.html#label-data-load-ui-new-table).

     * If you choose to create a stage, see [Staging files using Snowsight](data-load-local-file-system-stage-ui).

### Review and manage schema objects¶

For each type of database object contained in a database schema, you can
select a tab and review, sort, and search a table of those objects.

  * For Tables, review the name, type, classification, owner role, number of rows, bytes, and date created. You can also filter by the type of table.

  * For Views, review the name, type, owner role, and date created. You can also filter by the type of view.

  * For Stages, review the name, cloud and region for an external stage, storage integration associated with the stage, owner role, and date created.

  * For File Formats, review the name, type, owner role, and date created.

  * For Sequences, review the name, next value, interval, owner role, and date created.

  * For Dynamic Tables, review the name, state, target lag, warehouse used, rows, owner role, and date created.

  * For Streams, review the name, table name to which the stream is associated, owner role, and date created.

  * For Tasks, review the name, state, schedule, condition, warehouse used, and owner role.

  * For Pipes, review the name, notification channel, owner role, and date created.

  * For Functions, review the name, arguments, and date created.

  * For Procedures, review the name, arguments, and date created.

For any object, you can hover over the [![Comment icon](../_images/snowsight-
admin-user-comment.png)](../_images/snowsight-admin-user-comment.png) to read
the comment on the object. If you have the relevant privileges for an object,
you can also select [![More options](../_images/snowsight-worksheet-explorer-
ellipsis.png)](../_images/snowsight-worksheet-explorer-ellipsis.png) and
manage the object.

To view details about an object, select the row for the object and open the
object details page.

