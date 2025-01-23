# Create a setup script¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) Feature — Generally
Available

The Snowflake Native App Framework is generally available on supported cloud
platforms. For additional information, see [Support for private connectivity,
VPS, and government regions](limitations.html#label-native-apps-supported-
clouds).

This topic describes how to use the setup script to create objects in the
application object when running the [CREATE APPLICATION](../../sql-
reference/sql/create-application) command.

It also describes application roles and how they are used within the setup
script.

## About the setup script¶

The setup script contains SQL statements that are run when the [CREATE
APPLICATION](../../sql-reference/sql/create-application) command is run in one
of following contexts:

  * A consumer installs or upgrades a Snowflake Native App.

  * A provider creates or upgrades an application object when testing an application package.

Note

The setup script only support using SQL commands. Other languages are not
supported.

The SQL statements in the setup script create objects within the application
object that are required by the app. This includes database objects, stored
procedures, views, and application roles.

The `manifest.yml` file specifies the filename and relative path to the setup
script. The setup script must exist on a named stage and be accessible by the
app package.

## Restrictions on the setup script¶

The following cannot be performed within a setup script:

  * [USE DATABASE](../../sql-reference/sql/use-database)

  * [USE SCHEMA](../../sql-reference/sql/use-schema)

  * [USE ROLE](../../sql-reference/sql/use-role)

  * [USE SECONDARY ROLES](../../sql-reference/sql/use-secondary-roles)

  * Setting the LOG_LEVEL or TRACE_LEVEL properties with the [ALTER <object>](../../sql-reference/sql/alter) command.

  * Creating or invoking procedures that are EXECUTE AS CALLER.

  * Creating Snowpark user-defined functions (UDFs) or procedures that use IMPORT to include files on a named stage.

  * Calling procedures, functions or anonymous code blocks that refer to code not included in the application package.

  * Importing code files from a named stage when using the [CREATE FUNCTION](../../sql-reference/sql/create-function) command.

  * Using [CALL](../../sql-reference/sql/call) to call a procedure that runs as EXECUTE AS CALLER.

There are additional restrictions on objects created within a versioned
schema.

## Visibility of objects created in the setup script¶

The setup script can create most types of database-level objects. Database
objects created by the setup script are internal to the application. When a
consumer installs an app, by default, these objects are invisible and
inaccessible to the consumer account directly.

Note

Providers can access objects created by the setup script by using development
mode when testing an application package. See [About development
mode](installing-testing-application.html#label-native-apps-dev-mode) for more
information.

A provider can make these objects visible to the consumer using application
roles. An application role created within the setup script is automatically
granted to the role owning the application object. Application roles granted
by the setup script cannot be revoked.

Users granted a role that owns the application object can grant application
roles to other roles within their account. For example, the setup script can
define an application role, such as APP_ADMIN, and this role can grant
permission to access objects within the app.

## Set the log level for messages output by the setup script¶

A provider can specify the log level for messages generated when the setup
script runs. See [Logging messages in Snowflake Scripting](../logging-
tracing/logging-snowflake-scripting) for additional information.

To configure the log level for the setup script, use one of the following
system function:

  * [SYSTEM$LOG](../../sql-reference/functions/system_log)

  * [SYSTEM$LOG_<level>](../../sql-reference/functions/system_log)

For example, to configure the setup script to log error messages, add the
following command at the beginning of the setup script:

    
    
    SYSTEM$LOG('error', 'Error message');
    

Copy

## Create modular setup scripts¶

The setup script of a typical app can be large and complex. To make the setup
script more modular and easier to maintain, a provider can create a primary
setup script that calls multiple secondary setup scripts.

For example, a provider can create different setup scripts to handle different
types of tasks, for example, creating objects, creating views, creating stored
procedures, etc.

When the [CREATE APPLICATION](../../sql-reference/sql/create-application)
command runs, it runs the main setup script specified in the `manifest.yml`.
To run additional setup scripts from the main setup script, use the [EXECUTE
IMMEDIATE FROM](../../sql-reference/sql/execute-immediate-from) command.

Setup scripts included in the primary setup script are run in the order they
are encountered. These secondary setup scripts can also include instances of
the [EXECUTE IMMEDIATE FROM](../../sql-reference/sql/execute-immediate-from)
command.

### Add multiple setup scripts to an app¶

  1. Add the location of the primary setup script to the `manifest.yml`.
    
        artifacts:
      ...
      setup_script: scripts/setup.sql
      ...
    

Copy

  2. Create the primary setup script.

The following example shows a typical directory structure for an app:

    
        @test.schema1.stage1:
    └── /
        ├── manifest.yml
        ├── readme.md
        ├── scripts/setup_script.sql
    

Copy

Where `setup_script.sql` is the primary setup script.

  3. Create the secondary setup scripts.

The following example shows a typical directory structure for an app
containing multiple setup scripts:

    
        @test.schema1.stage1:
    └── /
        ├── manifest.yml
        ├── readme.md
        ├── scripts/setup_script.sql
        ├── scripts/secondary_script.sql
        ├── scripts/procs/setup_procs.sql
        ├── scripts/views/setup_views.sql
        ├── scripts/data/setup_data.sql
    

Copy

  4. Within the primary setup script, use the [EXECUTE IMMEDIATE FROM](../../sql-reference/sql/execute-immediate-from) command to specify a relative path to each secondary setup script:
    
        ...
    EXECUTE IMMEDIATE FROM 'secondary_script.sql';
    EXECUTE IMMEDIATE FROM './procs/setup_procs.sql';
    EXECUTE IMMEDIATE FROM '../scripts/views/setup_views.sql';
    EXECUTE IMMEDIATE FROM '/scripts/data/setup_data.sql';
    ...
    

Copy

The path provided to the [EXECUTE IMMEDIATE FROM](../../sql-
reference/sql/execute-immediate-from) command is case-sensitive and it can be
used with any setup script. Use a forward slash (`/`) to indicate the relative
path of the app root directory, use a period and a forward slash (`./`) to
indicate the current directory for the setup script, and use two periods and a
forward slash (`../`) to indicate the parent directory for the setup script.

A primary setup script is the script defined in the manifest. The [EXECUTE
IMMEDIATE FROM](../../sql-reference/sql/execute-immediate-from) command can be
used with any setup script.

### Limitations on using EXECUTE IMMEDIATE FROM in a setup script¶

The following limitations apply when using [EXECUTE IMMEDIATE FROM](../../sql-
reference/sql/execute-immediate-from) within a setup script:

  * Event logging is not supported in setup scripts called using [EXECUTE IMMEDIATE FROM](../../sql-reference/sql/execute-immediate-from).

  * Accessing files stored on encrypted external stages in the consumer account is not supported.

  * During app runtime, only the relative path format with a forward slash (`/`) is permitted. For example, `EXECUTE IMMEDIATE FROM '/scripts/data/setup_data.sql'`.

## Best practices when creating the setup script¶

Snowflake recommends the following best practices when creating the setup
script for an app.

### Use idempotent forms of CREATE statements¶

When using a CREATE command to create objects within the setup script,
Snowflake recommends using the following versions of these commands:

  * CREATE OR REPLACE

  * CREATE IF NOT EXISTS

The setup script can be run multiple times during installation and upgrade. In
cases where an error occurs, these objects might already exist, especially if
they are created within a versioned schema.

### Include the target schema when creating objects¶

The [CREATE SCHEMA](../../sql-reference/sql/create-schema) command does not
change the session context. Objects must be qualified with the target schema
when they are created. For example, to create a schema within the setup
script, use the following commands:

    
    
    CREATE SCHEMA IF NOT EXISTS app_config;
    CREATE TABLE IF NOT EXISTS app_config.params(...);
    

Copy

### Do not refer to objects in the application object from outside the
application object¶

Do not create objects outside the application object that refer to objects
within the application object. Although the Snowflake Native App Framework
does not prohibit creating these objects, it can lead to problems when a
consumer installs the Snowflake Native App.

For example, consider the context where a setup script creates a database,
schema, and view outside of the application object and the view refers to a
table within the application object. In this context, the view in the database
breaks when the consumer takes ownership of the database and drops the
application object.

This best practice applies to tables, stored procedures, user-defined
functions and references created by the setup script.

### Account for possible failures when using versioned or non-versioned
schemas¶

Objects in a versioned schema can refer to objects in a non-versioned schema
and vice versa. The setup script must account for what might happen in case of
failure during installation or upgrade. For example, a provider must account
for what happens if the setup script automatically runs again if the initial
run fails.

For example, consider creating objects using the following:

    
    
    CREATE OR REPLACE PROCEDURE app_state.proc()...;
    GRANT USAGE ON PROCEDURE app_state.proc()
      TO APPLICATION ROLE app_user;
    

Copy

In this example, the CREATE OR REPLACE statement replaces an existing
procedure, which implicitly removes privileges that had been previously
granted to that procedure. Although the grants might be restored later in the
script, if the script fails when it is run, consumers might lose the ability
to access the procedure.

If a setup script fails due to an issue that cannot be resolved by a retrying,
for example a syntax error, the consumer cannot access the procedure until the
app is upgraded to a new version or patch and the grant is restored.

Caution

The guidance in this section does not apply to [tags](../../user-guide/object-
tagging), [masking policies](../../user-guide/security-column-intro), and [row
access policies](../../user-guide/security-row-intro) outside the context of
the Snowflake Native App Framework.

Tag and policy assignments do not propagate to incremental versions of a
versioned schema. These scenarios trigger an error message (using a tag as an
example):

  * Create a tag in the versioned schema and assign the tag to an object in a different schema.

  * Create a tag in a non-versioned schema and assign the tag to an object in a versioned schema.

  * Create tables or views in the versioned schema and assign a tag to the tables or views when the tag exists in a non-versioned schema.

  * Create tables or views in a non-versioned schema and assign a tag to the tables or views when the tag exists in a versioned schema.

The error message is:

    
    
    A TAG in a versioned schema can only be assigned to the objects in the same schema. An object in a versioned schema can only have a TAG assigned that is defined in the same schema.
    

If the policy assignment triggers the error message, the error message
specifies `POLICY` instead of `TAG`.

To prevent the error message:

  * The Snowflake Native App provider should update the setup script to ensure that tags (or policies) are set on objects within the same schema as the tag when a versioned schema contains either the tag or the object on which the tag is set. If a non-versioned schema contains either the tag or the object on which the tag is set, it is not necessary to update the setup script.

  * If the Snowflake Native App consumer sees this error message when installing an application, the consumer should ask the provider to update their setup script. Additionally, the consumer should not assign any tag that exists in a versioned schema to any object in their account, such as a warehouse, or assign a policy that exists in a versioned schema to a table or column, or assign a policy or tag to an object that exists in a versioned schema inside the Snowflake Native App. If so, Snowflake returns the same error message.

### Define views within a versioned schema¶

Always define views on shared content in a versioned schema to ensure that any
code accessing the view during an upgrade uses a consistent view. You should
also use a versioned schema when adding or removing new columns or other
attributes.

### Ensure time-consuming operations are compatible¶

If the setup script must perform very long-running operations, such as
upgrading large state tables, ensure that these updates are compatible with
existing running code from the previous version.

## About application roles¶

By default the consumer has no privileges on objects created within the
application. Even the ACCOUNTADMIN role cannot view the objects **within** an
application. Objects that the application creates outside itself, for example
a database, are visible only to the ACCOUNTADMIN role of the consumer account.

Application roles are similar to database roles, but may only be created
within the application. Unlike database roles, application roles can be
granted privileges on objects that exist outside of the application.

Application roles should be created by the setup script when the application
is installed and are automatically granted to the application owner’s role,
who then can grant appropriate application roles to other roles in the
consumer account.

Note

Application roles are the only type of role that can be created within an
application. Database roles, for example are not permitted within the
application.

Likewise, application roles can only be created in an application and not, for
example, in a normal database or at the account level.

Any privileges granted to application roles is passed to the application
owner, which is the role used to install the application. The owner may
further delegate application roles to other roles within the consumer account.

The setup script can also define an application role (e.g. USER). Using this
role, consumers are granted access to use the functionality provided by the
application. The setup script can define an application role, such as
READ_ONLY, to provide restricted access to select areas of data within the
application.

Unlike database roles, application roles may also be granted privileges on
objects outside of the installed application. They may therefore be used to
grant privileges on objects outside of the application. However, the
application role itself must be created within the application.

## Supported SQL commands for working with application roles¶

The Snowflake Native App Framework provides the following SQL commands for
working with application roles:

  * [ALTER APPLICATION ROLE](../../sql-reference/sql/alter-application-role)

  * [CREATE APPLICATION ROLE](../../sql-reference/sql/create-application-role)

  * [DROP APPLICATION ROLE](../../sql-reference/sql/drop-application-role)

  * [GRANT APPLICATION ROLE](../../sql-reference/sql/grant-application-role)

  * [REVOKE APPLICATION ROLE](../../sql-reference/sql/revoke-application-role)

  * [SHOW APPLICATION ROLES](../../sql-reference/sql/show-application-roles)

## Using application roles in the setup script¶

Application roles defined in the setup script are automatically granted to the
role owning the application instance. When the application is installed, the
role used to installed the application is the owner of the application.
However, the application owner can grant privileges to other account roles in
the consumer account.

Application roles allow privileges on objects within the application to be
granted to the consumer. For example:

    
    
    CREATE APPLICATION ROLE admin;
    CREATE APPLICATION ROLE user;
    GRANT APPLICATION ROLE user TO APPLICATION ROLE admin;
    
    CREATE OR ALTER VERSIONED SCHEMA app_code;
    GRANT USAGE ON SCHEMA app_code TO APPLICATION ROLE admin;
    GRANT USAGE ON SCHEMA app_code TO APPLICATION ROLE user;
    CREATE OR REPLACE PROCEDURE app_code.config_app(...)
    GRANT USAGE ON PROCEDURE app_code.config_app(..)
      TO APPLICATION ROLE admin;
    
    CREATE OR REPLACE FUNCTION app_code.add(x INT, y INT)
    GRANT USAGE ON FUNCTION app_code.add(INT, INT)
      TO APPLICATION ROLE admin;
    GRANT USAGE ON FUNCTION app_code.add(INT, INT)
      TO APPLICATION ROLE user;
    

Copy

In this example, the setup script creates application roles named `admin` and
a `user`. The setup script then grants both application roles access to the
schema containing the application code. It also grants access to the `add`
function within the schema. The `admin` role is also granted access to the
`config_app` procedure.

## Application roles and versions¶

Application roles are not versioned. This means that dropping an application
role or revoking a permission from an object that is not in a versioned schema
can impact the current version of an application or the version being
upgraded. Application roles may only be safely dropped when you have dropped
all versions of the application that use those roles.

Note

Application roles cannot be granted ownership of objects. This means that an
application role defined in the setup script should only be used to allow
consumers to access objects within the installed Snowflake Native App.

