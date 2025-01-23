# Tutorial 3: Upgrade an app with containers¶  
  
[![Snowflake logo in black \(no text\)](../../../_images/logo-snowflake-
black.png)](../../../_images/logo-snowflake-black.png) Feature — Generally
Available

The Snowflake Native App Framework is generally available on supported cloud
platforms. For additional information, see [Support for private connectivity,
VPS, and government regions](../limitations.html#label-native-apps-supported-
clouds).

## Introduction¶

The Snowflake Native App Framework allows providers to build, sell, and
distribute apps within the Snowflake Data Cloud. Providers can create apps
that leverage core Snowflake functionality to share data and application logic
with consumers. Apps can also implement Snowpark Container Services to
facilitate the deployment, management, and scaling of containerized apps
within the Snowflake ecosystem.

The Snowflake Native App Framework allows providers to make updates to an app
and publish new version or patch to consumers. This tutorial describes how to
perform the following tasks:

  * Add a version initializer to the app.

  * Create versions and patches for changes made to the app.

  * Upgrade the app in the consumer account.

### Prerequisite tutorials¶

This tutorial assumes that you know how to develop a basic Snowflake Native
App and can create a Snowflake Native App with Snowpark Container Services.
This tutorial builds on the knowledge gained from completing the following
tutorials:

  * [Tutorial 1: Create a basic Snowflake Native App](getting-started-tutorial)

  * [Tutorial 2: Create an app with containers](na-spcs-tutorial)

Before following this tutorial to upgrade an app with containers, ensure that
you have completed both of these tutorials.

Caution

This tutorial builds on the app you created in [Tutorial 2: Create an app with
containers](na-spcs-tutorial). If you do not have the application files and
Snowflake objects in your account, you must work through that tutorial again
before starting this tutorial. See Verify the app from the previous tutorial
exists in your account for more information.

### What you learn in this tutorial¶

This tutorial expands the app with containers you created in [Tutorial 2:
Create an app with containers](na-spcs-tutorial). In this tutorial you learn
how to:

  * Use the version initializer callback function to handle service upgrades and failures.

  * Create version definitions for an app.

  * Upgrade an app.

  * Simulate upgrade failure for an app.

  * Create a patch for the app to fix the failure.

## Verify the app from the previous tutorial exists in your account¶

To verify that the app with containers you created in [Tutorial 2: Create an
app with containers](na-spcs-tutorial) is still available in your account,
perform the following tasks:

Caution

If any of the following tasks does not complete successfully, you will need to
perform [Tutorial 2: Create an app with containers](na-spcs-tutorial) again.

  1. To verify that Snow CLI is configured correctly, run the following command:
    
        snow connection test -c tut-connection
    

Copy

The output of this command should be similar to the following:

    
        +----------------------------------------------------------------------------------+
    | key             | value                                                          |
    |-----------------+----------------------------------------------------------------|
    | Connection name | tut-connection                                                 |
    | Status          | OK                                                             |
    | Host            | USER_ACCOUNT.snowflakecomputing.com                            |
    | Account         | USER_ACCOUNT                                                   |
    | User            | tutorial_user                                                  |
    | Role            | TUTORIAL_ROLE                                                  |
    | Database        | TUTORIAL_IMAGE_DATABASE                                        |
    | Warehouse       | TUTORIAL_WAREHOUSE                                             |
    +----------------------------------------------------------------------------------+
    

Copy

This command verifies the following requirements:

     * The Snow CLI connection is working.

     * The TUTORIAL_ROLE exists.

     * The TUTORIAL_WAREHOUSE exists.

  2. To verify that the other required Snowflake objects exist, run the following commands from a worksheet:
    
        USE ROLE tutorial_role;
    

Copy

    
        SHOW DATABASES LIKE 'tutorial_image_database';
    

Copy

    
        SHOW SCHEMAS LIKE 'tutorial_image_schema';
    

Copy

    
        SHOW IMAGE REPOSITORIES LIKE 'tutorial_image_repo';
    

Copy

Each of these commands should return the name of each Snowflake object.

  3. To verify that the service is still running, run the following command from a worksheet:
    
        CALL na_spcs_tutorial_app.app_public.service_status();
    

Copy

  4. Ensure that your local directory structure looks like the following example:
    
        ├── app
        └── manifest.yml
        └── README.md
        └── setup_script.sql
    ├── README.md
    ├── service
        └── echo_service.py
        ├── echo_spec.yaml
        ├── Dockerfile
        └── templates
            └── basic_ui.html
    ├── snowflake.yml
    

Copy

You may also see a folder called `output` that contains the app files
generated by the `snow app run` command.

### Drop the application object¶

If the app you created when working through [Tutorial 2: Create an app with
containers](na-spcs-tutorial) still exists in your account, you must drop the
application object before proceeding with this tutorial.

Note

You must drop the existing app because an app created in development mode
directly from staged files cannot be upgraded.

  1. To determine whether the app from the previous tutorial (`na_spcs_tutorial_app`) exists in your account, run the following command from a worksheet:
    
        SHOW APPLICATIONS LIKE 'na_spcs_tutorial_app';
    

Copy

  2. If the `na_spcs_tutorial_app` app appears in the output of this command, drop the app by running the following commands from a worksheet:
    
        USE ROLE tutorial_role;
    DROP APPLICATION IF EXISTS na_spcs_tutorial_app CASCADE;
    

Copy

### What you completed in this section¶

In this section, you verified that the application files and Snowflake objects
from the previous tutorial are still working in your account.

In the next section, you will learn more about versions and upgrades in the
Snowflake Native App Framework.

## Understand versions, patches and upgrades¶

The section introduces you to the concepts covered in this tutorial,
including:

  * Versions and patches

  * Upgrades

  * The version initializer

### About versions and patches¶

Versions in the Snowflake Native App Framework are combinations of version and
patch numbers. These are defined in the application package.

. rst-class:: bulleted-definition-list

Version

    

Generally contains major updates to a Snowflake Native App. Versions are
defined in an application package.

Patch

    

Generally contains smaller updates to a Snowflake Native App. Like versions,
patches are defined in the application package.

Note

An application package can only have two active versions at one time. A single
version of an app can have up to 130 patches.

### About upgrades¶

Within the context of the Snowflake Native App Framework, upgrades are updates
to a version or patch of a Snowflake Native App that is installed in the
consumer account. The Snowflake Native App Framework supports two types of
upgrades:

Automated upgrades

    

Automated upgrades are upgrades that are initiated by the provider. When a new
version or patch is available, the provider modifies the release directive on
the application package. This triggers an automatic upgrade of all installed
instances of the app specified by the release directive.

Manual upgrades

    

Manual upgrades are upgrades that are initiated by the consumer in response to
communication from the provider. Manual upgrades are useful when a provider
needs to quickly release an update, such as a bug fix, to a consumer.

Note

This tutorials describes how to perform a manual upgrade for an app with
containers.

When a new version or patch is available, the provider modifies the release
directive on the application package and then notifies the consumer that a new
version is available.

The consumer performs the upgrade by running the [ALTER
APPLICATION](../../../sql-reference/sql/alter-application) command in their
account to perform the upgrade. In general, manual upgrades allow the consumer
to upgrade their installed app faster than automated upgrades.

### About the version initializer¶

A version initializer is used to start or upgrade services or other related
processes. The version initializer is a callback stored procedure defined in
the manifest file and implemented in the setup script. The version initializer
callback function is invoked in the following contexts:

  * During installation, the version initializer is called as soon as the setup script of the app finishes without errors.

  * During upgrade, there are two possible scenarios where the version initializer is called:

    * If the setup script of the new version succeeds, then the new version of the version initializer is called.

    * If the setup script or the version initializer of the new version fails, then the version initializer of the previous version is called. This allows the version initializer of the previous version to use the [ALTER SERVICE](../../../sql-reference/sql/alter-service) command to revert the services to the previous version.

## Add a version initializer to the app¶

In the previous tutorial, you created a basic app with containers. In this
section you update this app to add a version initializer to the app. You also
add a version to the application package.

### Add the version initializer to the manifest file¶

The version initializer is defined in the manifest file of the app. To define
the version initializer, add the following code to the end of the
`manifest.yml` file:

    
    
    lifecycle_callbacks:
      version_initializer: app_public.version_init
    

Copy

This specifies the schema and name of the stored procedure used as the version
initializer. In the next section, you implement the `version_init` stored
procedure.

### Add the version initializer as a stored procedure to the setup script¶

In the previous section, you added the name of the version initializer to the
manifest file. In this section, you add the code for the stored procedure to
the setup script.

  1. Add the following code at the end of the `setup_script.sql` file:

    
    
    CREATE OR REPLACE PROCEDURE app_public.version_init()
    RETURNS STRING
    LANGUAGE SQL
    AS
    $$
    DECLARE
    can_create_compute_pool BOOLEAN;  -- Flag to check if 'CREATE COMPUTE POOL' privilege is held
    BEGIN
    -- Check if the account holds the 'CREATE COMPUTE POOL' privilege
       SELECT SYSTEM$HOLD_PRIVILEGE_ON_ACCOUNT('CREATE COMPUTE POOL')
          INTO can_create_compute_pool;
    
       ALTER SERVICE IF EXISTS core.echo_service
          FROM SPECIFICATION_FILE = 'service/echo_spec.yaml';
       IF (can_create_compute_pool) THEN
          -- When installing app, the app has no 'CREATE COMPUTE POOL' privilege at that time,
          -- so it will not execute the code below
    
          -- Since the ALTER SERVICE is an async process, wait for the service to be ready
          SELECT SYSTEM$WAIT_FOR_SERVICES(120, 'core.echo_service');
       END IF;
       RETURN 'DONE';
    END;
    $$;
    

Copy

### Upload the changed files and create a version¶

After modifying the setup script, upload the modified files to the stage and
create a version by performing the following procedure:

  1. Run the following command to upload the files and create a version:
    
        snow app version create v1 -c tut-connection
    

Copy

The `snow app version` command uploads the updated files to the stage. If the
application package and files already exist, this command only uploads files
that have changed.

This command creates a new version of the app called v1 with the default patch
set to 0.

### Set the default release directive for the app¶

In the previous section, you uploaded the changed files and created version
`v1` of the app. In this section, you set the default release directive to use
version `v1`.

To update the default release directive run the following command from a
worksheet:

    
    
    ALTER APPLICATION PACKAGE na_spcs_tutorial_pkg
      SET DEFAULT RELEASE DIRECTIVE VERSION=v1 PATCH=0;
    

Copy

When you set the default release directive for an app, consumers automatically
install that version when they install the app in their account. In the next
section, you create the app in your local account based on the release
directive.

### Create and test the app¶

Now that you have added a version and set the default release directive, you
can create the app and grant the required privileges:

  1. Create the app from the release directive by running the following command:
    
        snow app run --from-release-directive -c tut-connection
    

Copy

This command creates the app using the release directive you defined in the
previous section.

  2. After creating the app, grant the required privileges to the app to be able to run it by running the following commands from a worksheet.
    
        GRANT CREATE COMPUTE POOL ON ACCOUNT TO APPLICATION na_spcs_tutorial_app;
    GRANT BIND SERVICE ENDPOINT ON ACCOUNT TO APPLICATION na_spcs_tutorial_app;
    

Copy

  3. Call the `app_public.start_app` procedure that you defined in the `setup_script.sql` file: by running the following command from a worksheet:
    
        CALL na_spcs_tutorial_app.app_public.start_app();
    

Copy

  4. Confirm the function was created by running the following command from a worksheet:
    
        SHOW FUNCTIONS LIKE '%my_echo_udf%' IN APPLICATION na_spcs_tutorial_app;
    

Copy

  5. To verify that the service has been created and healthy, run the following command from a worksheet:
    
        CALL na_spcs_tutorial_app.app_public.service_status();
    

Copy

  6. To call the service function to send a request to the service and verify the response, run the following command from a worksheet:
    
        SELECT na_spcs_tutorial_app.core.my_echo_udf('hello');
    

Copy

  7. To view information about the app, run the following command from a worksheet:
    
        DESC APPLICATION na_spcs_tutorial_app;
    

Copy

### Review what you learned in this section¶

In this section, you completed the following tasks:

  * Learned about the version initializer and how you can add it to the manifest file and the setup script.

  * Learned the basics of versions and patches in the Snowflake Native App Framework.

  * Set the default release directive to point to a specific version of an app.

  * Installed the app based on the release directive.

  * Tested the app by calling a stored procedure and used the [DESCRIBE APPLICATION](../../../sql-reference/sql/desc-application) command to view the status of the app.

Note

In this tutorial you created the application object in your local account and
used the [DESCRIBE APPLICATION](../../../sql-reference/sql/desc-application)
command. This mimics the behavior of the app in the consumer account.

## Update the app and upgrade to a new version¶

In the previous section, you modified the original app by adding the version
initializer as a stored procedure. You also created a new version of the app,
version v1, based on the default release directive.

In this section, you make another change to the app, create version v2, update
the default release directive, and upgrade the installed app from version v1
to version v2.

### Add a new table to the app¶

To simulate adding a new feature to your app, add a new table to the setup
script.

  1. Add the following commands to the end of the `setup_script.yml`
    
        CREATE TABLE IF NOT EXISTS core.setup_script_run(run_at TIMESTAMP);
    GRANT SELECT ON TABLE core.setup_script_run to APPLICATION ROLE app_user;
    INSERT INTO core.setup_script_run(run_at) values(current_timestamp());
    

Copy

### Create a version of the app¶

To upload the modified setup script to the stage and create version v2 of the
app:

  1. Run the following command inside the `na-spcs-tutorial` folder:

    
    
    snow app version create v2 -c tut-connection
    

Copy

This command creates a new version of the app called v2 with the default patch
set to 0.

The `snow app version` command uploads the updated files to the stage. If the
application package and files already exist, this command only uploads files
that have changed.

### Set the default release directive for the app¶

After creating version `v2` of the app, set the release directive for the
application package by running the following command from a worksheet:

    
    
    ALTER APPLICATION PACKAGE na_spcs_tutorial_pkg
      SET DEFAULT RELEASE DIRECTIVE VERSION=v2 PATCH=0;
    

Copy

This command sets the release directive to version `v2` and patch `0`.

### Upgrade the app from v1 to v2¶

Now that you have updated the release directive to point to the new version,
upgrade the app by running the following command from a worksheet:

    
    
    snow app run --from-release-directive -c tut-connection
    

Copy

### Test the upgraded app¶

After upgrading the app, test the app by running the following command from a
worksheet:

    
    
    SELECT na_spcs_tutorial_app.core.my_echo_udf('hello');
    

Copy

### Review what you learned in this section¶

Congratulations! You successfully upgraded the app from version `v1` to
version `v2`.

In this section, you completed the following tasks:

  * Updated the app to include a table.

  * Created a new version for the app based on this update.

  * Updated the default release directive to point to the new version.

  * Manually upgraded the app.

In the next section, you upgrade the service of the app and simulate an error
in the upgrade process by intentionally adding an error in the setup script.

## Simulate an upgrade error¶

In the previous section, you added a new table to the app, created a new
version, and upgraded the app.

In this section you update the service specification to simulate an update to
the service. You also add an intentional error to the setup script to simulate
an upgrade failure, which shows you how the version initializer handles
service upgrades when the upgrade fails.

### Update the service specification file¶

In this section, you update the service specification of the app to simulate a
change to the service.

  1. In the `service/echo_spec.yaml` file, change the value of `CHARACTER_NAME` from `Bob` to `Tom`.

This change causes the service to return the following message:

    
        `Tom said hello.`
    

Copy

The purpose of this change is to allow you to see which version of the service
is running after attempting an upgrade in the following sections.

### Update the setup script to include an intentional error¶

To simulate an error during the upgrade process, introduce an intentional
error in the setup script by adding a SELECT statement for a table that does
not exist.

Add the following statement to the end of the `app_public.version_init()`
procedure in the `setup_script.sql`.

    
    
    SELECT * FROM table_does_not_exist;
    

Copy

This statement is syntactically correct, but refers to a table that does not
exist. This causes an error when the setup script runs during upgrade.

After making this change, the `app_public.version_init()` function should look
like the following example:

    
    
    GRANT USAGE ON PROCEDURE app_public.service_status() TO APPLICATION ROLE app_user;
    
    CREATE OR REPLACE PROCEDURE app_public.version_init()
    RETURNS STRING
    LANGUAGE SQL
    AS
    $$
    DECLARE
      -- Flag to check if 'CREATE COMPUTE POOL' privilege is held
      can_create_compute_pool BOOLEAN;
    BEGIN
       -- Check if the account holds the 'CREATE COMPUTE POOL' privilege
       SELECT SYSTEM$HOLD_PRIVILEGE_ON_ACCOUNT('CREATE COMPUTE POOL')
         INTO can_create_compute_pool;
    
       ALTER SERVICE IF EXISTS core.echo_service
         FROM SPECIFICATION_FILE = 'service/echo_spec.yaml';
       IF (can_create_compute_pool) THEN
         -- When installing app, the app has no 'CREATE COMPUTE POOL' privilege at that time,
         -- so it will not execute the code below
    
         -- Since the ALTER SERVICE is an async process, wait for the service to be ready
         SELECT SYSTEM$WAIT_FOR_SERVICES(120, 'core.echo_service');
       END IF;
    
       -- trigger an error. The upgrade fails
       SELECT * FROM non_exist_table;
    
       RETURN 'DONE';
    END;
    $$;
    

Copy

### Upload the revised files and create a new patch¶

In previous sections, you updated the service specification and setup script
of the app.

To upload the files and create a new patch for the app, perform the following
tasks:

  1. Run the following command to add a patch to the application package.

    
    
    snow app version create v2 --patch 1 -c tut-connection
    

Copy

  1. When prompted, enter `y` to add a new patch to the application package.

### Set the default release directive for the app¶

In the previous section, you uploaded the files and created a patch for the
updates. To set the default release directive for the patch, run the following
command from a worksheet:

    
    
    ALTER APPLICATION PACKAGE na_spcs_tutorial_pkg
      SET DEFAULT RELEASE DIRECTIVE VERSION=v2 PATCH=1;
    

Copy

This command sets that patch for the app to patch `1`.

### Upgrade the app¶

In the previous sections, you made updates to the app and created a new patch.
In this section, you upgrade the app with the expectation that it fails due to
the error you introduced in previous sections.

To upgrade the app, run the following command:

    
    
    snow app run --from-release-directive -c tut-connection
    

Copy

To view the upgrade state of the app, run the following command from a
worksheet:

    
    
    DESC APPLICATION na_spcs_tutorial_app;
    

Copy

This command displays information about the app including the upgrade state,
the number of upgrade attempts, and the reason for an upgrade failure.

After the upgrade fails, Snowflake CLI returns the following message:

    
    
    Object 'TABLE_DOES_NOT_EXIST' does not exist or not authorized.'
    

Copy

Also, after the upgrade fails, the DESC APPLICATION command displays the
following properties related to upgrades:

> Property | Value  
> ---|---  
> upgrade_state | FAILED  
> upgrade_failure_reason | upgrade_failure_reason[ErrorCode 2003] Uncaught exception of type ‘STATEMENT_ERROR’ on line 89 at position 0 : Uncaught exception of type ‘STATEMENT_ERROR’ on line 19 at position 3 : SQL compilation error: Object ‘TABLE_DOES_NOT_EXIST’ does not exist or not authorized.  
  
### Run app service to see which version of the service is running¶

In the previous section, you simulated a failure when upgrading from version
v2, patch 0 to version v2, patch 1.

To determine which version of the service is currently running, run the
following command from a worksheet.

    
    
    SELECT na_spcs_tutorial_app.core.my_echo_udf('hello');
    

Copy

This command returns the following string:

    
    
    Bob said hello
    

Copy

Here, you see that since the upgrade failed, the app continues to run the
service from v2, patch 0.

However, if you did not include a version initializer in the app, the upgrade
process would have upgraded the service to v2, patch 1 although the app
upgrade failed. If an app upgrade fails, the version initializer ensures that
the version of the service does not upgrade and continues to be in sync with
the app.

### Review what you learned in this section¶

In this section, you completed the following tasks:

  * Introduced an error in the setup script to simulate an error in the upgrade process.

  * Verified the version of both the app and service after the failure.

  * Learned how the version initializer ensures that the version of a service is in synch with the version of the app when an upgrade fails.

## Create a patch to fix the upgrade error¶

In the previous section, you introduced an error in the setup script of the
app. When you upgraded the app, you were able to verify that both the app and
the service were continuing to run using version v2 patch 0.

In this section, you modify the setup script of the app to fix the error,
create a patch for the update, and upgrade the app.

### Modify the setup script¶

To fix the intentional error you introduced in a previous section, remove the
following statement from the `setup_script.yaml` file:

    
    
    SELECT * FROM table_does_not_exist;
    

Copy

### Upload the updated files and create a new patch¶

To upload the modified setup script to a stage and create a new patch, perform
the following tasks:

  1. Run the following command to create a new patch for the app:

  2. When prompted, enter `y` to add a new patch to the application package.

### Update the default release directive¶

In the previous section, you created patch `2` for the app. To set the default
release directive for the patch, run the following command from a worksheet:

    
    
    ALTER APPLICATION PACKAGE na_spcs_tutorial_pkg
      SET DEFAULT RELEASE DIRECTIVE VERSION=v2 PATCH=2;
    

Copy

### Upgrade the app and verify the version of the service¶

After creating a new version and setting the default release directive,
upgrade the app and test the service by performing the following tasks:

  1. To upgrade the app from version `v2` patch `0` to version `v2` patch `2`, run the following command:
    
        snow app run --from-release-directive -c tut-connection
    

Copy

  2. To verify the version of the service that is currently running, run the following command from a worksheet:
    
        SELECT na_spcs_tutorial_app.core.my_echo_udf('hello');
    

Copy

  3. To view the status of the app, including the version that is currently installed, run the following command:
    
        DESC APPLICATION na_spcs_tutorial_app;
    

Copy

In the output the `version` property is `v2` and the patch property is `2`.

### Review what you learned in this section¶

Congratulations! You successfully upgraded the app after the upgrade failure.

In this section, you completed the following tasks:

  * Fixed the error in the setup script.

  * Created a new patch, `p2`, to update the app.

  * Upgraded the app to the new patch.

## Tear down the app and objects created in the tutorial¶

Because the app uses a compute pool, it uses credits in your account and costs
money to run. To stop the app from consuming resources, you must tear down
both the application object and any of the account-level objects it created,
such as the compute pool.

  1. To confirm that the compute pool is currently running, run the following command:
    
        snow object list compute-pool -l "na_spcs_tutorial_app_%"
    

Copy

If the compute pool is running, a row with an `ACTIVE` compute pool that was
created by the application object is displayed.

  2. Run the following Snowflake CLI command to tear down the app:
    
        snow app teardown --cascade --force -c tut-connection
    

Copy

This command removes all of the Snowflake objects created by the app. Without
the `--force` option, this command does not drop the application package
because it contains versions.

  3. To confirm that the compute pool was dropped run the following command again:
    
        snow object list compute-pool -l "na_spcs_tutorial_app_%"
    

Copy

This command returns `no data` if the compute pool has been dropped
successfully.

Note

The `snow app teardown` command drops both the application package and
application object. Therefore, any stateful data is lost.

## Learn more¶

Congratulations! In this tutorial, you learned how to manually upgrade an app
with containers.

### Summary¶

In this tutorial, you completed the following tasks:

  * Added a version initializer stored procedure to handle services during upgrades and failures.

  * Created a new version definition of the app in the application package. Version definitions specify the version number and patch of the app.

  * Set the default release directive for an app. Release directives determine which version and patch is installed when a consumer installs or upgrades an app.

  * Upgraded an app and verified what happens during upgrade failure.

