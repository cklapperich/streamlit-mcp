# Create an application package¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) Feature — Generally
Available

The Snowflake Native App Framework is generally available on supported cloud
platforms. For additional information, see [Support for private connectivity,
VPS, and government regions](limitations.html#label-native-apps-supported-
clouds).

This topic describes how to create and manage an application package with the
Snowflake Native App Framework.

## About application packages¶

An application package is a container that encapsulates the data content,
application logic, metadata, and setup script required by an application. An
application package also contains information about versions and patch levels
defined for the application.

## Create an application package¶

The Snowflake Native App Framework supports creating an application package
using Snowsight or alternatively you can create an application running SQL
commands.

### Privileges required to create an application package¶

To create an application package you must have the global CREATE APPLICATION
PACKAGE privilege granted to your role.

### Upload the manifest file and setup script to a named stage¶

There are two ways to upload files to a named stage:

  * Using Snowsight. For details, refer to [Staging files using Snowsight](../../user-guide/data-load-local-file-system-stage-ui)

  * Using the [PUT](../../sql-reference/sql/put) command.

### Create an application package using Snowsight¶

  1. Sign in to [Snowsight](../../user-guide/ui-snowsight).

  2. In the navigation menu, select Projects » App Packages.

  3. Select Create and then click App Package in the right pane.

  4. Enter a name for your application package.

  5. Select the intended consumer for the application package:

     * Select Distribute to accounts outside of your organization to make the application package available outside your organization. Selecting this option initiates an [automated security scan](security-overview) for each version and patch defined in your application package.

     * Select Distribute to accounts in your organization to make the application package available within your organization. The automated security scan is not initiated.

  6. (Optional) Enter comments for the application package. These comments are not visible to the consumer.

  7. Select Add.

### Create an application package using SQL commands¶

To create an application package using SQL, use the [CREATE APPLICATION
PACKAGE](../../sql-reference/sql/create-application-package) command as shown
in the following example:

    
    
    CREATE APPLICATION PACKAGE HelloSnowflakePackage;
    

Copy

After creating an application package, use the [SHOW APPLICATION
PACKAGES](../../sql-reference/sql/show-application-packages) command to view
the list of available application packages.

## Grant privileges on an application package¶

Some tasks related to developing an application package that you require have
specific privileges set on the application package. The following table
describes the privileges required to perform these tasks:

Privilege | Task  
---|---  
ATTACH LISTING | Add an application package to a listing.  
DEVELOP | Create an APPLICATION object in development mode from the application package.  
INSTALL | Create an APPLICATION object based on the application package.  
MANAGE RELEASES | Specify a release directive, view the version and patch level.  
MANAGE VERSIONS | Add a version and patch level to an application package.  
OWNERSHIP | Perform all of the tasks above.  
  
### Grant privileges on an application package using Snowsight¶

  1. Sign in to [Snowsight](../../user-guide/ui-snowsight).

  2. In the navigation menu, select Projects » App Packages.

  3. Select the application package, then select the Settings tab.

  4. In the Privileges section, select the edit icon next to the privilege you want to grant.

  5. Select Add Role, then select the role to which you want to grant the privilege.

  6. Select Save.

The role appears next to the privilege.

### Grant privileges on an application package using SQL commands¶

To grant a privilege on the application package to a role using SQL, use the
[GRANT <privileges>](../../sql-reference/sql/grant-privilege) command as shown
in the following example:

    
    
    GRANT MANAGE RELEASES ON APPLICATION PACKAGE hello_snowflake_package TO ROLE app_release_mgr;
    

Copy

This command grants the MANAGE RELEASES privilege to the `app_release_mgr`
role. You can use the same command to grant the other privileges available on
an application package.

## Set the default release directive for an application package¶

A release directive determines the version and patch of an app that is
available to a consumer when they install the app or when an installed app is
automatically upgraded. To set the release directive on the application
package, use the [ALTER APPLICATION PACKAGE](../../sql-reference/sql/alter-
application-package) command.

See [Set the release directive for an app](update-app-release-directive) for
more information.

## Allow consumers to install multiple instances of an app¶

Providers can configure an application package to allow consumers to install
multiple instances of an app.

To enable multiple instances of an app, use the `MULTIPLE_INSTANCES = TRUE`
clause of the [CREATE APPLICATION PACKAGE](../../sql-reference/sql/create-
application-package) or [ALTER APPLICATION PACKAGE](../../sql-
reference/sql/alter-application-package) commands.

If multiple instances are allows for an app, consumers can install a maximum
of 10 instances of the app in their account.

You cannot set this property for an application package that is included in a
trial or monetized listing.

Caution

After setting the `MULTIPLE_INSTANCES` property to `TRUE`, it cannot be unset
or set to `FALSE`.

## Transfer ownership of an application package¶

After creating an application package, you can transfer ownership of the
application package to another account-level role.

### Transfer ownership using Snowsight¶

  1. Sign in to [Snowsight](../../user-guide/ui-snowsight).

  2. In the navigation menu, select Projects » App Packages.

  3. Select … next to the application package you want to transfer ownership, then select Transfer Ownership.

  4. Under Transfer to, select the new account-level role.

  5. Select Transfer.

### Transfer ownership using SQL Commands¶

To transfer ownership of an application package to a different account-level
role using SQL, use the [GRANT OWNERSHIP](../../sql-reference/sql/grant-
ownership) command as shown in the following example:

    
    
    GRANT OWNERSHIP ON APPLICATION PACKAGE hello_snowflake_package TO ROLE native_app_dev;
    

Copy

## Delete an application package¶

Users with the OWNERSHIP privilege on an application package can remove it
from an account. However, you cannot remove an application package that is
currently associated with a listing.

After removing an application package, it is no longer available within the
provider account.

Note

After removing a listing and the attached application package, the consumer
can view but not access the Snowflake Native App created from the application
package. If a consumer tries to access the Snowflake Native App, they receive
an error indicating the application package has been removed.

### Remove an application package using Snowsight¶

  1. Sign in to Snowsight.

  2. In the navigation menu, select Projects » App Packages.

  3. Select … next to the application package you want to remove, then select Drop.

### Remove an application package using SQL commands¶

To remove an application package using SQL, run the [DROP APPLICATION
PACKAGE](../../sql-reference/sql/drop-application-package) command as shown in
the following example:

    
    
    DROP APPLICATION PACKAGE hello_snowflake_package;
    

Copy

