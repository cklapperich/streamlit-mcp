# Install and test an app locally¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) Feature — Generally
Available

The Snowflake Native App Framework is generally available on supported cloud
platforms. For additional information, see [Support for private connectivity,
VPS, and government regions](limitations.html#label-native-apps-supported-
clouds).

This topic describes how to create an APPLICATION object from an application
package.

## About creating and testing application objects¶

The Snowflake Native App Framework allows provider to create an APPLICATION
object within the same account as the application package. This allows
providers to test a Snowflake Native App before publishing it to consumers. It
also allows providers to test the Snowflake Native App in a single account
without having to alternate between provider and consumer accounts.

## Privileges Required to Create and Test an APPLICATION Object¶

To create an APPLICATION object from an application package you must have the
following privileges granted to your role:

  * The CREATE APPLICATION account-level privilege granted to your role.

  * The INSTALL object-level privilege granted on the application package.

The following examples show how to use the [GRANT <privileges>](../../sql-
reference/sql/grant-privilege) command to grant these privileges to your
account:

    
    
    GRANT CREATE APPLICATION ON ACCOUNT TO ROLE provider_role;
    GRANT INSTALL ON APPLICATION PACKAGE hello_snowflake_package
      TO ROLE provider_role;
    

Copy

### Use the DEVELOP privilege¶

By default, the role used to create an application package has permissions to
run the [CREATE APPLICATION](../../sql-reference/sql/create-application)
command to create an APPLICATION object based on the application package.

However, in some development environments you may need to allow users with
other roles to create and test an application package. To do this, grant the
DEVELOP object-level privilege on the application package to a role.

The DEVELOP account-level privilege provides the necessary privileges to
create and test an APPLICATION object based on an application package. The
DEVELOP privilege enables a user to perform the following tasks using the
application package on which they have been granted access:

  * Create a version of an APPLICATION object based on a version or patch level specified in the application package.

  * Upgrade a version of an application package using the [ALTER APPLICATION](../../sql-reference/sql/alter-application) command.

  * Create and upgrade an APPLICATION object using files on a named stage.

  * Enable debug mode on an APPLICATION object created in development mode.

To grant the DEVELOP privilege to a specific role, use the [GRANT
<privileges>](../../sql-reference/sql/grant-privilege) command as shown in the
following example:

    
    
    GRANT DEVELOP ON APPLICATION PACKAGE hello_snowflake_package TO ROLE other_dev_role;
    

Copy

Note

The DEVELOP object-level privilege is specific to a single application
package. You must run [GRANT <privileges>](../../sql-reference/sql/grant-
privilege) for each application on which you want to assign the DEVELOP
privilege.

## Workflow for Creating and Testing an Application¶

The Snowflake Native App Framework provides different ways of creating an
APPLICATION object from an application package. This allows you to test a
Snowflake Native App before publishing it to consumers. The method you use
depends on what parts of the APPLICATION object you want to test.

The following steps outline a typical workflow for testing an APPLICATION
object:

  1. Create an APPLICATION object using contents on a stage.

This allows you to quickly test a new version of a setup script or application
code file. Refer to Create an application using staged files for more
information.

  2. Create an APPLICATION object from a version or patch.

After defining a version or patch for an application package, you can test
this version by creating an APPLICATION object using this version. Refer to
Create an application object from a version or patch level.

  3. Upgrade an APPLICATION object.

After verifying that a version of an application package is working correctly,
you can upgrade an existing APPLICATION object to the new version. You can
upgrade in one of two ways:

     * Upgrading an Application Using a Stage (Single Account)

     * Upgrading an Application from a Version (Single Account)

  4. Create an APPLICATION object directly from an application package.

After verifying that the APPLICATION object works correctly, you can create an
APPLICATION object from an application package without specifying a version or
stage files. This creates the APPLICATION object using the default release
directive.

Refer to Create an application using staged files for more information.

  5. Install an Snowflake Native App from a listing.

After verifying in your account that both the application package and
APPLICATION object are working correctly, you can add the application package
to a listing and test the installation using Snowsight.

Refer to Create an application using staged files for more information.

## Create an application object¶

The Snowflake Native App Framework allows you to install an APPLICATION object
directly in your account to test a Snowflake Native App before it is shared
with customers. The [CREATE APPLICATION](../../sql-reference/sql/create-
application) command supports different syntax for creating an APPLICATION
object.

Note

The following sections assume that you have created an application package and
the required manifest file and setup script.

### Create an application using staged files¶

You can create an APPLICATION object using a manifest file and setup script
uploaded to a named stage. This allows you to test changes to these files
without having to add a version to an application package.

Use the [CREATE APPLICATION](../../sql-reference/sql/create-application)
command to create an APPLICATION object using staged files as shown in the
following example:

    
    
    CREATE APPLICATION hello_snowflake_app FROM APPLICATION PACKAGE hello_snowflake_package
      USING '@hello_snowflake_code.core.hello_snowflake_stage';
    

Copy

### Create an application object from a version or patch level¶

After specifying a version or patch level in an application package you can
create an APPLICATION object based on that version or patch level.

To create a an APPLICATION object from a specific version, use the [CREATE
APPLICATION](../../sql-reference/sql/create-application) command as shown in
the following example:

    
    
    CREATE APPLICATION hello_snowflake_app FROM APPLICATION PACKAGE hello_snowflake_package
      USING VERSION v1_0;
    

Copy

To create an APPLICATION object from a specific patch level, use the [CREATE
APPLICATION](../../sql-reference/sql/create-application) command as shown in
the following example:

    
    
    CREATE APPLICATION hello_snowflake_app FROM APPLICATION PACKAGE hello_snowflake_package
      USING VERSION v1_0 PATCH 2;
    

Copy

### Create an application based on a release directive¶

After specifying a release directive in an application package you can create
an APPLICATION object based on the release directive. This can be a custom
release directive or the default release directive.

To create an application package based on a release directive use the [CREATE
APPLICATION](../../sql-reference/sql/create-application) command as shown in
the following example:

    
    
    CREATE APPLICATION hello_snowflake_app FROM APPLICATION PACKAGE hello_snowflake_package;
    

Copy

### Upgrade an application using a stage¶

To upgrade an APPLICATION object using files on a named stage, use the [ALTER
APPLICATION](../../sql-reference/sql/alter-application) command as shown in
the following example:

    
    
    ALTER APPLICATION HelloSnowflake
      UPGRADE USING @CODEDATABASE.CODESCHEMA.AppCodeStage;
    

Copy

### Upgrade an application from a version or patch¶

To upgrade an APPLICATION object that was created using a specific a version,
use the [ALTER APPLICATION](../../sql-reference/sql/alter-application) command
as shown in the following example:

    
    
    ALTER APPLICATION HelloSnowflake
     UPGRADE USING VERSION "v1_1";
    

Copy

## View application objects¶

To see a list of APPLICATION objects available to your account, use the [SHOW
APPLICATIONS](../../sql-reference/sql/show-applications) command as shown in
the following example:

    
    
    SHOW APPLICATIONS
    

Copy

## About development mode¶

When you create an APPLICATION object from an application package by
specifying a version or application files on a named stage, the APPLICATION
object is considered to be in development mode.

Development mode allows you to test and troubleshoot an APPLICATION object
within a single account. In development mode you can create and test an
APPLICATION object based on a specific version of an application package. You
can also create and test an APPLICATION object using application files on a
stage. This enables you to quickly test changes to the setup script or
application logic.

Development mode provides an additional debug mode that allows you to verify
the internal state of an APPLICATION object that a consumer would otherwise
not be able to view.

In development mode, for example, running the SHOW or DESC commands on objects
within the APPLICATION object will only display those objects that the
consumer has been granted permissions to view. However in DEBUG mode, you can
see all objects within the APPLICATION object.

## Enable debug mode¶

The Snowflake Native App Framework allows you to test an APPLICATION object in
debug mode. Debug mode allows you to view and modify all of the objects within
the APPLICATION object. Objects that are not visible to a consumer, for
example, objects not granted to a database role or shared content objects, are
visible while in this mode.

Using an APPLICATION object in debug mode requires the following:

  * The APPLICATION object must be created in development mode, meaning it must be based on a specific version or files on a stage.

  * You must explicitly set debug mode on the APPLICATION object.

Note

Debug mode can only be toggled on and off for APPLICATION object created in
development mode within the same account containing the application package.

To enable debug mode on an APPLICATION object, use the [ALTER
APPLICATION](../../sql-reference/sql/alter-application) command as shown in
the following example:

    
    
    ALTER APPLICATION hello_snowflake_app SET DEBUG_MODE = TRUE;
    

Copy

This command turns on debug mode for an APPLICATION object named
`hello_snowflake_app`. Likewise, to turn off debug mode, use the same command
as shown in the following example:

    
    
    ALTER APPLICATION hello_snowflake_app SET DEBUG_MODE = FALSE;
    

Copy

This command turns off debug mode for the APPLICATION object named
`hello_snowflake_app`.

Note

To run this command, you must have the OWNERSHIP privilege on the APPLICATION
object . You must also have the DEVELOP privilege on the application package.

Additionally, the APPLICATION object must be created in development mode and
in the same account as the application package.

## Set an application object as the active context¶

To set an APPLICATION object as the active, current context for a session, run
the USE APPLICATION command as shown in the following example:

    
    
    USE APPlICATION hello_snowflake_app;
    

Copy

Note

To run this command, you must have the USAGE privilege granted on the
APPLICATION object to your role.

## View details of an application object¶

To view details of an application object, run the [DESCRIBE
APPLICATION](../../sql-reference/sql/desc-application) command as shown in the
following example:

    
    
    DESC APPLICATION hello_snowflake_app;
    

Copy

In development mode, this command displays the schemas allowed by the
consumer’s application roles.

In debug mode, this command displays all schemas in the instance and
application package.

