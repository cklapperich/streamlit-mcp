# Tutorial 2: Create an app with containers¶

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
with consumers. The logic of a Snowflake Native App can include features such
as stored procedures and user-defined functions (UDFs). Providers can share
their applications with consumers through listings in the Snowflake
Marketplace or through private listings.

A Snowflake Native App can implement Snowpark Container Services to facilitate
the deployment, management, and scaling of containerized apps within the
Snowflake ecosystem. This tutorial describes how to create a Snowflake Native
App with Snowpark Container Services, which is a Snowflake Native App that
runs container workloads in Snowflake. Snowflake Native Apps with Snowpark
Container Services can run any containerized services, while leveraging all of
the features of the Snowflake Native App Framework, including security,
logging, shared data content and application logic.

Note

This tutorial uses both Snowflake CLI and Snowsight to perform the required
tasks.

### What you learn in this tutorial¶

In this tutorial, you learn how to:

  * Use Snowflake CLI to initialize a Snowflake Native App with Snowpark Container Services project.

  * Build a Docker image for an app.

  * Create the application package and required application files for a Snowflake Native App with Snowpark Container Services.

  * Test a Snowflake Native App with Snowpark Container Services by calling the service function within the container.

### Set up your Snowflake environment¶

To perform this tutorial, you must meet the following prerequisites:

  * Access to a Snowflake account that supports Snowpark Container Services.

  * You must be able to use the ACCOUNTADMIN role to create the role used in this tutorial and grant the required privileges to that role.

  * You must have [Snowflake CLI](../../snowflake-cli/index) version `3.0.0` or greater installed on your local machine.

  * You must have Docker Desktop installed on your local machine.

## Set up a role for this tutorial¶

This tutorial walks you through the process of creating a Snowflake Native App
with Snowpark Container Services using the `tutorial_role` role. Before
working through this tutorial, a Snowflake user with the ACCOUNTADMIN role
must perform the following steps to configure this role.

To create and set up the `tutorial_role` role, follow these steps:

  1. To create the `tutorial_role` role, run the following command:
    
        CREATE ROLE tutorial_role;
    

Copy

  2. To grant the `tutorial_role` to the Snowflake user who performs the tutorial, run the following command:
    
        GRANT ROLE tutorial_role TO USER <user_name>;
    

Copy

Where:

> `_user_name_`
>  
>
> Specifies the name of the user who performs the tutorial.

  3. To grant the privileges required to create and use the Snowflake objects required by a container app, run the following commands:
    
        GRANT CREATE INTEGRATION ON ACCOUNT TO ROLE tutorial_role;
    GRANT CREATE WAREHOUSE ON ACCOUNT TO ROLE tutorial_role;
    GRANT CREATE DATABASE ON ACCOUNT TO ROLE tutorial_role;
    GRANT CREATE APPLICATION PACKAGE ON ACCOUNT TO ROLE tutorial_role;
    GRANT CREATE APPLICATION ON ACCOUNT TO ROLE tutorial_role;
    GRANT CREATE COMPUTE POOL ON ACCOUNT TO ROLE tutorial_role WITH GRANT OPTION;
    GRANT BIND SERVICE ENDPOINT ON ACCOUNT TO ROLE tutorial_role WITH GRANT OPTION;
    

Copy

After performing the tasks in this section, the user that has the
`tutorial_role` role granted to their account has the permissions to create
all of the Snowflake objects required to create a Snowflake Native App with
Snowpark Container Services.

You use this role through the rest of this tutorial.

In a real-world situation, a provider may need similar privileges or access to
existing objects to develop an app with containers, including a compute pool,
warehouse, and database.

## Create the required objects in your account¶

In this section, you create the Snowflake objects required by an app with
containers.

### Create a warehouse and image repository¶

To create the required objects, perform the following either through Snowsight
or Snowflake CLI.

  1. To set the current context in Snowsight to use the `tutorial_role` role, run the following command:
    
        USE ROLE tutorial_role;
    

Copy

If you are using Snowflake CLI, you can use `--role tutorial_role` instead.

  2. To create a warehouse for the Snowflake Native App with Snowpark Container Services, run the following command:
    
        CREATE OR REPLACE WAREHOUSE tutorial_warehouse WITH
      WAREHOUSE_SIZE = 'X-SMALL'
      AUTO_SUSPEND = 180
      AUTO_RESUME = true
      INITIALLY_SUSPENDED = false;
    

Copy

A warehouse is required by the Snowflake Native App to run SQL commands and
stored procedures.

  3. To create the image repository used to store the container, run the following command:
    
        CREATE DATABASE tutorial_image_database;
    CREATE SCHEMA tutorial_image_schema;
    CREATE IMAGE REPOSITORY tutorial_image_repo;
    

Copy

In this section, you created a warehouse that is used to execute queries for
the app you create, as well as an image repository to host container images.

In the next section you create an image for the container and upload it to the
image repository you created above.

## Create a Snowflake CLI connection for the tutorial¶

To run the Snowflake CLI commands in this tutorial, you must setup a Snowflake
CLI connection for the tutorial.

To create a connection, perform the following tasks:

  1. From the terminal, run the following command:
    
        snow connection add
    

Copy

  2. Enter `tut-connection` for the name of the connection.

  3. Enter additional information for the Snowflake CLI connection.

The specific values you use depend on your Snowflake account. However, you
must use the following values for the role, warehouse, database, and schema
properties:

Parameter | Required value  
---|---  
Role for the connection | tutorial_role  
Warehouse for the connection | tutorial_warehouse  
Database for the connection | tutorial_image_database  
Schema for the connection | tutorial_image_schema  
  4. Verify the connection by running the following command:
    
        snow connection test -c tut-connection
    

Copy

The output of this command should look similar to the following:

    
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

Caution

If you do not create the `tut-connection` connection, you must use a
connection that specifies the correct values for the role, database, and
warehouse connection properties.

## Setup a project for the app¶

In the previous section, you set up a Snowflake CLI connection for the
tutorial.

In this section, you use Snowflake CLI to create a project for your app. A
project contains all of the assets required by an app. These files are stored
on your local file system and can be managed by a version control system as
part of your development workflow.

### Create a project file using the Snowflake CLI¶

  1. To create a project file, run the following command:
    
        snow init --template app_basic na-spcs-tutorial
    

Copy

  2. Enter a value for the project identifier.

> You add additional files and subfolders to this folder and edit the files
> this command created in later subsections.

This command creates a folder named `na-spcs-tutorial` using the `app_basic`
project template.

Within the `na-spcs-tutorial` folder, this command creates the following files
and folders:

    
    
    ├── README.md
    ├── app
        └── manifest.yml
        └── README.md
        └── setup_script.sql
    ├── snowflake.yml
    

Copy

In later sections you modify these files and add additional resources to your
app.

### Add the service files to the app project¶

In the previous section you created a project which includes the default
application files required by your app. In this section, you add the files
required to create the container for your app.

  1. Create a folder called `service` inside the `na-spcs-tutorial` folder.

This folder contains the source code for the container-based service we are
about to build and publish to Snowflake.

  2. To obtain the Docker files required for the tutorial, download the [`na_spcs_tutorial.zip`](../../../_downloads/af07363a9484a0281a50e9a0556f78cb/na-spcs-tutorial.zip) file to your local file system.

  3. Unzip the contents of the zip file into the `na-spcs-tutorial/service` folder. This folder should container the following files:

     * `echo_service.py`

     * `Dockerfile`

     * `templates/basic_ui.html`

     * `echo_spec.yaml`

### Verify the directory structure of your project¶

After create the project for your app and adding the files for the service and
Docker container, the project should have the following structure within the
`na-spcs-tutorial` folder:

    
    
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

## Build an image for a Snowpark Container Services service¶

In this section, you build a Docker image and upload it to the image
repository you created in the previous section.

### Build a Docker image and upload it to the image repository¶

To build a Docker image and upload it to the image repository, follow these
steps:

  1. From a terminal window, change to the `na-spcs-tutorial/service` folder.

  2. Run the following Docker CLI command. Note that you must specify the current working directory (.) in the command:
    
        docker build --rm --platform linux/amd64 -t my_echo_service_image:tutorial .
    

Copy

This command performs the following:

     * Builds a Docker image using the Docker file included in the zip file that you downloaded

     * Names the image `my_echo_service_image`

     * Applies the `tutorial` tag to the image.

  3. To identify the URL of the image repository you created in a previous section, run the following command:
    
        REPO_URL=$(snow spcs image-repository url tutorial_image_database.tutorial_image_schema.tutorial_image_repo -c tut-connection)
    echo $REPO_URL
    

Copy

The URL of the image repository is captured in the `$REPO_URL` variable, then
printed to the console. You use this value in the next step.

  4. To create a tag for the image that includes the image URL, run the following Docker CLI command:
    
        docker tag <image_name> <image_url>/<image_name>
    

Copy

This command requires two parameters:

     * `<image_name>` Specifies the name of the image and tag.

     * `<image_url>/<image_name>` Specifies the URL of the image repository where the image is uploaded and the image name and tag where it should be stored in the remote repository.

For this tutorial, use `$REPO_URL` and `my_echo_service_image:tutorial`:

    
        docker tag my_echo_service_image:tutorial $REPO_URL/my_echo_service_image:tutorial
    

Copy

  5. To authenticate with the Snowflake registry, run the following Snowflake CLI command:
    
        snow spcs image-registry login -c tut-connection
    

Copy

This command loads necessary credentials required for the Docker CLI to use
the image repositories in your Snowflake account. You must specify the
connection name, if you are not using the default.

The message `Login Succeeded` displays if everything was successful.

  6. To upload the Docker image to the image repository, run the following `docker push` command:
    
        docker push $REPO_URL/<image_name>
    

Copy

Using the same value as `<image_name>` from previous steps, this command is:

    
        docker push $REPO_URL/my_echo_service_image:tutorial
    

Copy

  7. Confirm the image was uploaded successfully by running the following command:
    
        snow spcs image-repository list-images tutorial_image_database.tutorial_image_schema.tutorial_image_repo -c tut-connection
    

Copy

In this section, you created a Docker image containing the echo service and
pushed it to the `tutorial_repository` image repository you created earlier in
the tutorial.

In the next section, you create an application package that uses this image.

## Develop your Snowflake Native App¶

In a previous section, you used the Snowflake CLI to create a project file
based on a project template. This template created default versions of the
files required by the app.

In this section, you update these default files for your app:

Project Definition file

    

A YAML file that contains information about the Snowflake object(s) that you
want to create. This file is called `snowflake.yml` and is used by Snowflake
CLI to deploy the application package and object into your account.

Manifest file

    

A YAML file that contains basic configuration and callback information about
the application. This file is called `manifest.yml`.

Setup Script

    

An SQL script that runs automatically when a consumer installs an application
in their account. This file can be called whatever you like, as long as it is
referenced by your manifest.

The first file is used by Snowflake CLI, while the latter two are required by
the Snowflake Native App Framework.

You learn more about these files, and their contents, throughout this
tutorial.

In this section, you also create a readme file that is useful when viewing and
publishing your app.

### Modify the defaul manifest file¶

To modify the manifest file for the app, follow these steps:

  1. Modify `na-spcs-tutorial/app/manifest.yml` to look like the following:
    
        manifest_version: 1
    
    artifacts:
       setup_script: setup_script.sql
       readme: README.md
       container_services:
          images:
          - /tutorial_image_database/tutorial_image_schema/tutorial_image_repo/my_echo_service_image:tutorial
    
    privileges:
    - BIND SERVICE ENDPOINT:
         description: "A service that can respond to requests from public endpoints."
    - CREATE COMPUTE POOL:
         description: "Permission to create compute pools for running services"
    

Copy

This example includes the following:

     * The `artifacts` property specifies the locations of resources required by an app with containers, including the location of the Docker image you created in a previous step, as well as the project README that is visible in Snowsight.

     * The `privileges` property allows a service to respond to public requests as well as to create its own compute pool. These properties are required for instantiating our service in the next step of the tutorial.

### Modify the default setup script¶

To modify the default setup script for the application package, follow these
steps:

  1. Modify the `na-spcs-tutorial/app/setup_script.sql` file to include the following:
    
        CREATE APPLICATION ROLE IF NOT EXISTS app_user;
    
    CREATE SCHEMA IF NOT EXISTS core;
    GRANT USAGE ON SCHEMA core TO APPLICATION ROLE app_user;
    
    CREATE OR ALTER VERSIONED SCHEMA app_public;
    GRANT USAGE ON SCHEMA app_public TO APPLICATION ROLE app_user;
    
    CREATE OR REPLACE PROCEDURE app_public.start_app()
       RETURNS string
       LANGUAGE sql
       AS
    $$
    BEGIN
       -- account-level compute pool object prefixed with app name to prevent clashes
       LET pool_name := (SELECT CURRENT_DATABASE()) || '_compute_pool';
    
       CREATE COMPUTE POOL IF NOT EXISTS IDENTIFIER(:pool_name)
          MIN_NODES = 1
          MAX_NODES = 1
          INSTANCE_FAMILY = CPU_X64_XS
          AUTO_RESUME = true;
    
       CREATE SERVICE IF NOT EXISTS core.echo_service
          IN COMPUTE POOL identifier(:pool_name)
          FROM spec='service/echo_spec.yaml';
    
       CREATE OR REPLACE FUNCTION core.my_echo_udf (TEXT VARCHAR)
          RETURNS varchar
          SERVICE=core.echo_service
          ENDPOINT=echoendpoint
          AS '/echo';
    
       GRANT USAGE ON FUNCTION core.my_echo_udf (varchar) TO APPLICATION ROLE app_user;
    
       RETURN 'Service successfully created';
    END;
    $$;
    
    GRANT USAGE ON PROCEDURE app_public.start_app() TO APPLICATION ROLE app_user;
    
    CREATE OR REPLACE PROCEDURE app_public.service_status()
    RETURNS TABLE ()
    LANGUAGE SQL
    EXECUTE AS OWNER
    AS $$
       BEGIN
             LET stmt VARCHAR := 'SHOW SERVICE CONTAINERS IN SERVICE core.echo_service;
             LET res RESULTSET := (EXECUTE IMMEDIATE :stmt);
             RETURN TABLE(res);
       END;
    $$;
    
    GRANT USAGE ON PROCEDURE app_public.service_status() TO APPLICATION ROLE app_user;
    

Copy

### Modify the default README¶

To modify the README file for the app, follow these steps:

  1. Modify `na-spcs-tutorial/app/README.md` to look like the following:
    
        Welcome to your first app with containers!
    

Copy

This README file is visible to consumers after they install your app.

### Modify the default project definition file¶

In this section, you modify the project definition file used by the Snowflake
CLI.

  1. Modify `na-spcs-tutorial/snowflake.yml` to look like the following:
    
        definition_version: 2
    entities:
       na_spcs_tutorial_pkg:
          type: application package
          manifest: app/manifest.yml
          artifacts:
             - src: app/*
               dest: ./
             - service/echo_spec.yaml
          meta:
             role: tutorial_role
             warehouse: tutorial_warehouse
       na_spcs_tutorial_app:
          type: application
          from:
             target: na_spcs_tutorial_pkg
          debug: false
          meta:
             role: tutorial_role
             warehouse: tutorial_warehouse
    

Copy

In this section, you defined a local file structure that can be deployed to a
Snowflake account as a Snowflake Native App with Snowpark Container Services.
In the next section, you perform this deployment using Snowflake CLI.

## Create and test the app¶

After defining the manifest file, setup script, and service specification for
your Snowflake Native App with Snowpark Container Services, you can test the
app by deploying it to your account using Snowflake CLI.

### Upload files to the stage and create the application object¶

To create an app in development mode, follow these steps:

  1. In a terminal, change to the `na-spcs-tutorial` folder.

  2. Create the application package and object in your account by running the following command:
    
        snow app run -c tut-connection
    

Copy

This command displays a confirmation that an application package called
`na_spcs_tutorial_pkg` and an application object called `na_spcs_tutorial_app`
have been created in your account. These names correspond to the names in the
`snowflake.yml` project definition you modified in a previous section.

You can use the URL output to the console to view the application. However,
you must first ensure it has all necessary privileges to create its container-
based service.

### Grant the privileges and test the app¶

In this section, you grant the required privileges to the app and test the app
by calling the services in the container.

You can run SQL commands using either Snowsight or the Snowflake CLI.

To grant the privileges and test the app, perform the following steps from a
Snowflake worksheet:

  1. Grant the `CREATE COMPUTE POOL` privilege to the app by running the following:
    
        GRANT CREATE COMPUTE POOL ON ACCOUNT TO APPLICATION na_spcs_tutorial_app;
    GRANT BIND SERVICE ENDPOINT ON ACCOUNT TO APPLICATION na_spcs_tutorial_app;
    

Copy

  2. Run the `app_public.start_app` procedure we defined in the `setup_script.sql` file.
    
        CALL na_spcs_tutorial_app.app_public.start_app();
    

Copy

This procedure creates the compute pool, instantiate the service, and creates
the service function.

  3. Confirm the function was created by running the following:
    
        SHOW FUNCTIONS LIKE '%my_echo_udf%' IN APPLICATION na_spcs_tutorial_app;
    

Copy

Note

Consumers cannot see the running service because it runs as part of the
Snowflake Native App. For example, running `SHOW SERVICES IN APPLICATION
na_spcs_tutorial_app;` does not return anything.

  4. To verify that the service has been created and healthy, run the following command:
    
        CALL na_spcs_tutorial_app.app_public.service_status();
    

Copy

This statement calls the `app_public.service_status` procedure that you
defined in the setup script. The procedure returns information about the
containers for this service.

If the value in the `status` column is not `READY`, execute the statement
again, until the status of the service container is `READY`.

  5. To call the service function to send a request to the service and verify the response, run the following command:
    
        SELECT na_spcs_tutorial_app.core.my_echo_udf('hello');
    

Copy

You see the following message from the service you configured in an earlier
section:

    
        ``Bob said hello``
    

Copy

## Teardown the app and objects created in the tutorial¶

Caution

If you plan to perform the [Tutorial 3: Upgrade an app with containers](na-
upgrade-tutorial) after completing this tutorial, do not perform the steps in
this section. The app with containers you created in this tutorial is a
prerequisite for the upgrade tutorial.

Because the app uses a compute pool, it accrues credits in your account and
costs money to run. To stop the app from consuming resources, you must tear
down both the application object and any of the account-level objects it
created, for example the compute pool.

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

Congratulations! Not only have you finished this tutorial, but you have worked
through the development and publishing life cycle of a Snowflake Native App
with Snowpark Container Services.

Along the way, you:

  * Used Snowsight and Snowflake CLI to build an application using the Snowflake Native App Framework.

    * See [Configuring Snowflake CLI and connecting to Snowflake](../../snowflake-cli/connecting/connect) for more information on how to configure the connections used by Snowflake CLI.

    * For more information about Snowsight, refer to [Getting started with worksheets](../../../user-guide/ui-snowsight-worksheets-gs) and [Work with worksheets in Snowsight](../../../user-guide/ui-snowsight-worksheets).

    * For more information about Native Apps in Snowflake CLI, refer to [Using Snowflake Native App in Snowflake CLI](../../snowflake-cli/native-apps/overview).

  * Created the manifest and setup script that are required by all applications.

    * Refer to [Create the manifest file for an application package](../creating-manifest) and [Create a setup script](../creating-setup-script) for details.

  * Created an application package that works as a container for the application logic and data content of your application.

    * Refer to [Create an application package](../creating-app-package) for details.

  * Used Docker CLI and Snowflake CLI to build and upload a container to Snowflake.

  * Used Snowpark Container Services to create a `COMPUTE POOL` and instantiate the container inside of a Snowflake Native App.

