# Private notebooks¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) [Preview
Feature](../../release-notes/preview-features) — Open

Available to all accounts.

## Introduction¶

In Snowsight, you can create a private, user-owned notebook. This private
notebook is stored in your personal database: a dedicated workspace where you
can create, modify, and manage your private notebooks. Unlike with role-based
ownership, objects within a personal database are owned by an individual user.
The lifecycle of a user’s personal database is tied to the user. For example,
if a user is deleted in the Snowflake account, their personal database is also
deleted. You can create private notebooks in a personal database without
having to wait for someone to grant you the appropriate privileges.

Your personal database is named after your username in the form
`USER$_username_` (for example, `USER$JOHNDOE`). You can also reference it
with the prefix `USER$`. You can view details for your personal database in
Data » Databases.

A private notebook enables you to do the following tasks:

  * Privately develop code interactively and experiment with data and models.

  * Deploy these projects by duplicating notebooks from personal databases to regular, non-personal databases.

For details on private notebook prerequisites, see [Prerequisites for using
private notebooks](notebooks-setup.html#label-notebooks-prerequisites-private-
notebooks).

For details on creating a private notebook, see [Create a new
notebook](notebooks-create.html#label-notebooks-create).

## Activating all secondary roles for private notebook users¶

Before you create a private notebook, secondary roles must be enabled. This is
because private notebooks are owned by the user, not their primary role.

The 2024_07 BCR bundle (enabled by default) enabled all secondary roles, but
if the account administrator disabled the bundle, you must either:

  * Enable the 2024_07 or 2024_08 BCR bundle.

  * Set the [DEFAULT_SECONDARY_ROLES](../../sql-reference/sql/create-user.html#label-create-user-default-secondary-roles) object to `('ALL')` for the user.

To activate all secondary roles of a user by default, the user or an
administrator can use the [ALTER USER](../../sql-reference/sql/alter-user)
command to set the DEFAULT_SECONDARY_ROLES object property to `('ALL')` for
the user.

For example, administrators can execute the following SQL statement to
activate all secondary roles of a user by default:

    
    
    ALTER USER my_user SET DEFAULT_SECONDARY_ROLES = ('ALL');
    

Copy

After an administrator executes the SQL statement above, the user can choose
Projects » Notebooks in Snowsight or execute SQL commands in a new worksheet
to create a private notebook.

A user who wants to execute SQL commands in an existing worksheet must execute
the following SQL statement before creating a private notebook:

    
    
    USE SECONDARY ROLES ALL;
    

Copy

## Private notebook limitations¶

  * Private notebooks cannot be scheduled.

## Personal database restrictions¶

  * Users can only create private notebooks and schemas inside a personal database. For example, tables cannot be created and loaded.

  * Users cannot alter, clone, or replicate their personal database.

  * Users cannot move schemas between personal and non-personal databases.

  * Administrators cannot add a personal database to a replication group for the purpose of replication.

  * Users cannot add a personal database to native apps (app package).

  * Users and administrators cannot drop and/or rename the `USER$.PUBLIC` schema.

  * Collaboration limitations:

    * Administrators cannot create database roles.

    * Users and administrators cannot grant any `CREATE <object>` privileges on their schemas to others.

    * Users cannot grant privileges on their objects to shares or to application packages.

    * Users cannot grant the `REFERENCE_USAGE` privilege on their personal database to shares or packages.

    * Users cannot add a personal database to a share (for the purpose of sharing across accounts).

## Organizing your private notebooks¶

You can create and use schemas as a means of organizing your private
notebooks. By default, personal databases contain the standard schemas named
PUBLIC and INFORMATION_SCHEMA.

Create and use new schemas in the usual way, but make sure you are using your
personal database when you create schemas. For example:

    
    
    USE DATABASE USER$bobr;
    CREATE SCHEMA bobr_schema;
    USE SCHEMA bobr_schema;
    

Copy

You can also use the [ALTER SCHEMA](../../sql-reference/sql/alter-schema)
command on schemas in personal databases, and you can use the [SHOW
SCHEMAS](../../sql-reference/sql/show-schemas) command to see the schemas that
belong to personal databases. For example:

    
    
    ALTER SCHEMA bobr_schema RENAME TO bobr_personal_schema;
    SHOW TERSE SCHEMAS;
    

Copy

    
    
    +-------------------------------+----------------------+------+---------------+-------------+
    | created_on                    | name                 | kind | database_name | schema_name |
    |-------------------------------+----------------------+------+---------------+-------------|
    | 2024-10-28 19:33:18.437 -0700 | BOBR_PERSONAL_SCHEMA | NULL | USER$BOBR     | NULL        |
    | 2024-10-29 14:11:33.267 -0700 | INFORMATION_SCHEMA   | NULL | USER$BOBR     | NULL        |
    | 2024-10-28 12:47:21.502 -0700 | PUBLIC               | NULL | USER$BOBR     | NULL        |
    +-------------------------------+----------------------+------+---------------+-------------+
    

## Making a private notebook available for general use¶

At some point in its development, you may want to recreate your notebook
outside your personal database. To make this change, duplicate the original
notebook using a [CREATE NOTEBOOK](../../sql-reference/sql/create-notebook)
command. When you do this, the notebook becomes visible to other users.

For example:

    
    
    CREATE NOTEBOOK bobr_prod_notebook
      FROM 'snow://notebook/USER$BOBR.PUBLIC.bobr_private_notebook/versions/version$1/'
      QUERY_WAREHOUSE = 'PUBLIC_WH'
      MAIN_FILE = 'notebook_app.ipynb'
      COMMENT = 'Duplicated from personal database';
    

Copy

    
    
    Notebook BOBR_PROD_NOTEBOOK successfully created.
    

You can also create a private notebook from a notebook that was created in a
production database.

Note

You cannot complete this task via the Snowsight user interface; you must use
an explicit SQL command (in a SQL cell of a notebook or in a worksheet, for
example).

## Viewing information about private notebooks and personal databases¶

Individual users can use Snowsight to view information about notebooks. Go to
Projects » Notebooks. The owner of the notebook is listed as the user.

For information about databases, including personal databases, go to Data »
Databases. You can easily see which databases are personal databases because
they have the `USER$` prefix.

You can also use the following SHOW and DESCRIBE commands to view information
about private notebooks, personal databases, and schemas inside those personal
databases:

  * [DESCRIBE NOTEBOOK](../../sql-reference/sql/desc-notebook)

  * [SHOW DATABASES](../../sql-reference/sql/show-databases)

  * [SHOW NOTEBOOKS](../../sql-reference/sql/show-notebooks)

Note

Currently, administrators cannot see private notebook objects that belong to
other users.

For example, describe a private notebook:

    
    
    DESCRIBE NOTEBOOK USER$.PUBLIC.bobr_private_notebook;
    

Copy

For example, show information about one or more private notebooks:

    
    
    SHOW NOTEBOOKS;
    

Copy

    
    
    SHOW NOTEBOOKS LIKE 'bobr_private_notebook';
    

Copy

For example, show the current user’s personal database:

    
    
    SHOW DATABASES LIKE 'USER$BOBR';
    

Copy

For personal databases, the value in the `kind` column is `PERSONAL DATABASE`.

