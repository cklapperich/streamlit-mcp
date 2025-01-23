# Tutorial 1: Create a basic Snowflake Native App¶

[![Snowflake logo in black \(no text\)](../../../_images/logo-snowflake-
black.png)](../../../_images/logo-snowflake-black.png) Feature — Generally
Available

The Snowflake Native App Framework is generally available on supported cloud
platforms. For additional information, see [Support for private connectivity,
VPS, and government regions](../limitations.html#label-native-apps-supported-
clouds).

## Introduction¶

The Snowflake Native App Framework allows providers to build, sell, and
distribute a Snowflake Native App within the Snowflake Data Cloud. Providers
can create apps that leverage core Snowflake functionality to share data and
application logic with consumers. The logic of Snowflake Native App can
include features such as stored procedures, and user-defined functions (UDFs).
Providers can share their applications with consumers through listings in the
Snowflake Marketplace or through private listings.

This tutorial describes how to use the Snowflake Native App Framework to
create a basic Snowflake Native App to share data and related business logic
with other Snowflake accounts.

Note

The tutorial uses both Snowflake CLI and the Snowsight web interface.

### What you learn in this tutorial¶

In this tutorial, you learn how to:

  * Create an application package that contains the data and business logic of your app.

  * Share data with an application package.

  * Add business logic to an application package.

  * Test the app locally.

  * View and test the app in Snowsight.

  * Publish your app by creating a private listing.

  * Install the app from a private listing.

  * Use Snowflake CLI to perform many of the steps above.

### About providers and consumers¶

Within the context of the Snowflake Native App Framework, providers are the
roles and organizations who have data and business logic that they want to
share with other Snowflake users, who are the consumers. A consumer can be
another account within your organization, a different organization within your
company, or a Snowflake user in another company.

Within the context of this tutorial, most of the tasks you perform are those
typically performed by providers, but these include tasks that may be
performed by multiple roles within your organization including application
developers and database administrators.

In this tutorial, you also perform tasks that mimic the actions performed by
consumers to install an app.

### Prerequisites¶

  * You must have [Snowflake CLI](../../snowflake-cli/index) installed on your machine.

  * You must run all of the SQL commands in the same SQL command session because the session context is required.

To do this in Snowsight, for example, paste all of your code into the same
worksheet as you go along. As you progress from section to section, each
section builds on the previous.

  * You must be able to use the ACCOUNTADMIN role.

In this tutorial, you perform all the steps using the ACCOUNTADMIN role. In
general practice, however, you would use roles with privileges specifically
defined for the action you’re performing. For example, you might have separate
roles for developers who create UDFs and stored procedures, for database
administrators who manage roles and permissions, and for administrators who
[manage listings](https://other-
docs.snowflake.com/en/collaboration/collaboration-listings-about) using
Snowflake Collaboration.

  * To install your app from a private listing, you must have access to a second Snowflake account. You use this account to mimic how consumers would install an app.

Note

Although the Snowflake Native App Framework supports sharing apps with
accounts in different organizations, for the purposes of this tutorial, both
accounts must be in the same organization.

  * You must set a current warehouse. See [USE WAREHOUSE](../../../sql-reference/sql/use-warehouse).

## Create the application files¶

In this section, you create a setup script, a manifest file and a project
definition file. The first two of these files are required by the Snowflake
Native App Framework.

Setup script

    

An SQL script that runs automatically when a consumer installs an app in their
account.

Manifest file

    

A YAML file that contains basic configuration information about the app.

Project definition file

    

A YAML file that contains information about the Snowflake objects that you
want to create.

You learn more about these files, and their contents, throughout this
tutorial. You also create a readme file that is useful when viewing and
publishing your app in later sections of this tutorial.

### Initialize a new project folder¶

You use Snowflake CLI to initialize a new Snowflake Native App project in your
local filesystem.

To do this, execute the following command:

>
>     snow init --template app_basic tutorial
>  
>
> Copy

This command creates a folder named `tutorial` inside the current working
directory and populates it with a basic Snowflake Native App project based on
a basic template. This is the root directory for all of your application
files.

Note

You modify and add files and subfolders to this folder in later sections.

Note

There are other templates available to help you quickly get up-and-running
with Native Applications. Please consult `snow init --help` for more
information.

### Create the setup script¶

Modify or replace the contents of the `app/setup_script.sql` file as shown in
the following example:

>
>     -- Setup script for the Hello Snowflake! app.
>  
>
> Copy

This line is a placeholder because the setup script cannot be empty.

> Note
>
> This tutorial refers a particular structure and filename for the setup
> script. However, when building your own app you can choose your own name and
> directory structure for this file.

### Create a README file for your app¶

A readme file provides a description of what your application does. You see
the readme when you view your app in Snowsight.

Modify or replace the contents of `app/README.md` with the following:

>
>     This is the readme file for the Hello Snowflake app.
>  
>
> Copy

### Create the manifest file¶

The Snowflake Native App Framework requires a manifest file for each app. The
manifest file contains metadata and configuration parameters for an app and
influences the run-time behavior of your app.

Note

This file must be named `manifest.yml`. Paths to other files, including the
setup script, are relative to the location of this file.

Modify or replace the contents of the `app/manifest.yml` with the following:

    
    
    manifest_version: 1
    artifacts:
       setup_script: setup_script.sql
       readme: README.md
    

Copy

The `setup_script` property specifies the location of the setup script
relative to the location of the manifest file. The path and file name
specified here must be the same as the relative location of the setup script
you modified above. The `readme` property follows the same rules.

Note

The `manifest_version`, `artifacts`, and `setup_script` properties are
required. The `readme` property is optional.

### Create the project definition file¶

Snowflake CLI uses a project definition file to describe objects that can be
deployed to Snowflake. This file must be named `snowflake.yml`. This file
controls the name of the deployed application package and object, as well as
which files are uploaded to the project stage.

> Note
>
> This file must be named `snowflake.yml` and it must exist at the root level
> of your project. Paths to other files, such as the `manifest.yml` and the
> setup script are relative to the location of this file.

Modify or replace the contents of the `snowflake.yml` with the following:

>
>     definition_version: 2
>     entities:
>        hello_snowflake_package:
>           type: application package
>           stage: stage_content.hello_snowflake_stage
>           manifest: app/manifest.yml
>           identifier: hello_snowflake_package
>           artifacts:
>              - src: app/*
>                dest: ./
>        hello_snowflake_app:
>           type: application
>           from:
>              target: hello_snowflake_package
>           debug: false
>  
>
> Copy

The next section of this tutorial describe how to use each of these
properties.

### Review what you learned in this section¶

After performing the steps in this section, you should now have a directory
structure that looks like the following:

    
    
    /tutorial
      snowflake.yml
      README.md
      /app/
        manifest.yml
        README.md
        setup_script.sql
    

Copy

In this section you learned how to create the setup script and manifest files
that are required by the Snowflake Native App Framework and the project
definition file that is required by the Snowflake CLI.

Although the content you added to both the setup script and manifest file is
basic, all apps must have these files.

You also added a readme file that is displayed when viewing your app in
Snowsight or when publishing your app as a listing.

## Understanding the project definition file¶

In this section you learn about the contents of the [project
definition](../../snowflake-cli/native-apps/project-definitions.html#label-
native-apps-project-definition) file (`snowflake.yml`) you created in the
previous section. You also perform additional setup tasks for your provider
account.

At its core, an application package is a Snowflake database that is extended
to include additional information about an app. In that sense, it is a
container for an app that includes:

  * Shared data content

  * Application files

To create an application package, your role must have the CREATE APPLICATION
PACKAGE privilege. To grant this privilege using the Snowflake CLI, run the
following command:

>
>     snow sql -q 'GRANT CREATE APPLICATION PACKAGE ON ACCOUNT TO ROLE
> accountadmin' -c connection_name
>  
>
> Copy
>
> where `connection_name` is the name of the connection you specified in your
> `config.toml` file when you installed the Snowflake CLI.

Note

Although the ACCOUNTADMIN role has this privilege by default, to be able to
create an application package, you must ensure that your role has been granted
this privilege.

The project definition file (`snowflake.yml`) defines the names of objects
that are created in your Snowflake account:

  * The application package (`hello_snowflake_package`)

  * The application object (`hello_snowflake_app`) that is created from the application package

  * The stage that holds application files (`stage_content.hello_snowflake_stage`)

Note that the name of the stage is specified as a schema-qualified name. This
schema is created inside the application package. This named stage is used to
store the files required by the Snowflake Native App Framework. This stage
must include any files you want available to the setup script of your app
setup script or at runtime.

There is also a section called `artifacts` in the project definition file
which is a list of rules that specify which files are copied to the named
stage.

The rule specifies that anything in the `app/` subfolder is copied to the root
of the stage. This means the following:

  * `tutorial/app/manifest.yml` is uploaded to the root of `@hello_snowflake_package.stage_content.hello_snowflake_stage`.

  * `tutorial/app/README.md` is uploaded to the root of `@hello_snowflake_package.stage_content.hello_snowflake_stage`.

  * `tutorial/app/setup_script.sql` is uploaded to the root of `@hello_snowflake_package.stage_content.hello_snowflake_stage`.

You are not yet creating the application package or executing any SQL commands
that perform these tasks. In a later section, you run the Snowflake CLI
command to perform these tasks.

Finally, you set `debug: false` inside of the app definition. For applications
deployed using the Snowflake CLI, debug mode is enabled by default.

In this section you learned that an application package is a container for the
resources used by an app. You also learned the how to set the fields in the
project definition file.

## Add application logic and install your first app¶

In this section, you add code to the application package and install your
first app. To do this, you perform the following tasks:

  * Add a stored procedure to the setup script.

  * Install and test the app in stage dev mode.

### Add a stored procedure to the setup script¶

In this section, you add a stored procedure to the app by adding the code for
the stored procedure to the setup script on your local file system.

To add a stored procedure to the setup script:

  1. Add the following SQL statements at the end of the `setup_script.sql` file that you created in an earlier section of this tutorial:
    
        CREATE APPLICATION ROLE IF NOT EXISTS app_public;
    CREATE SCHEMA IF NOT EXISTS core;
    GRANT USAGE ON SCHEMA core TO APPLICATION ROLE app_public;
    

Copy

When the setup script runs during app installation, these statements create an
application role named `app_public`. Application roles are similar to database
roles, but they can only be used within the context of an app. They are used
to grant access to objects within the application object that is created in
the consumer account.

This example also creates a schema to contain the stored procedure and grants
the USAGE privilege on the schema to the application role. Creating an
application role and granting privileges on an object, for example a schema,
to the application role is a common pattern within the setup script.

  2. Add the code for the stored procedure at the end of the `setup_script.sql` file:
    
        CREATE OR REPLACE PROCEDURE CORE.HELLO()
      RETURNS STRING
      LANGUAGE SQL
      EXECUTE AS OWNER
      AS
      BEGIN
        RETURN 'Hello Snowflake!';
      END;
    

Copy

This example creates a stored procedure that outputs the string “Hello
Snowflake!”.

  3. Add the following statement to the end of the `setup_script.sql` file:
    
        GRANT USAGE ON PROCEDURE core.hello() TO APPLICATION ROLE app_public;
    

Copy

This example grants the USAGE privilege on the stored procedure to the
application role.

In this section you added a stored procedure to the setup script. You also
created an application role and granted the USAGE privilege to this role. This
allows the setup script to create the stored procedure when the app is
installed. It also gives the app permission to run the stored procedure.

### Install and test the app in stage development mode¶

You are now ready to create the application package, the app and all the other
entities you specified in the project definition file.

To perform these tasks, run the following Snowflake CLI command:

>
>     snow app run -c connection_name
>  
>
> Copy
>
> where `connection_name` is the name of the connection you specified in your
> `config.toml` file whe you installed the Snowflake CLI.

This command performs the following tasks:

  1. Create an application package name `hello_snowflake_package` with schema `stage_content` and stage `hello_snowflake_stage`.

  2. Upload all required files to the named stage.

  3. Create or upgrade the app `hello_snowflake_app` using files from this stage.

If the command runs successfully, it outputs a URL where you can see your app
in Snowsight. To run the `HELLO` stored procedure that you added to
`setup_script.sql` in a previous section, run the following Snowflake CLI
command:

    
    
    snow sql -q "call hello_snowflake_app.core.hello()" -c connection_name
    

Copy

You should see the following output after running this command:

    
    
    +------------------+
    | HELLO            |
    |------------------|
    | Hello Snowflake! |
    +------------------+
    

Copy

### Review what you learned in this section¶

Congratulations! You have created, installed, and tested your first Snowflake
Native App using the Snowflake Native App Framework! Although the app only has
basic functionality, the components you used to build the app are the same for
more complex apps.

In this section you completed the following:

  * Added a stored procedure to the setup script. The setup script specifies how your app is installed in the consumer account. In later sections you add data content and other types of application logic to your app.

  * Deployed your app for the first time using Snowflake CLI.

  * Tested your installed app by running a stored procedure.

In later sections you learn about other ways to view and test your app.

## Add data content to your app¶

In the previous section you created an app that contains a stored procedure
that demonstrates how you would add application logic to an app.

In this section you include data content in your app by creating a database
within the `HELLO_SNOWFLAKE_PACKAGE` application package and granting
privileges to share this database with the app.

### Create a table to share with an app¶

In this section you learn how to share data content with an app. Specifically,
you share a table in the provider account by granting privileges on the schema
and table to the application package.

  1. To create a table and insert the sample data in the application package, create a folder `tutorial/scripts`, then a file `shared_content.sql` inside the folder. Add the following contents to this file:
    
        USE APPLICATION PACKAGE <% ctx.entities.hello_snowflake_package.identifier %>;
    
    CREATE SCHEMA IF NOT EXISTS shared_data;
    USE SCHEMA shared_data;
    CREATE TABLE IF NOT EXISTS accounts (ID INT, NAME VARCHAR, VALUE VARCHAR);
    TRUNCATE TABLE accounts;
    INSERT INTO accounts VALUES
      (1, 'Joe', 'Snowflake'),
      (2, 'Nima', 'Snowflake'),
      (3, 'Sally', 'Snowflake'),
      (4, 'Juan', 'Acme');
    -- grant usage on the ``ACCOUNTS`` table
    GRANT USAGE ON SCHEMA shared_data TO SHARE IN APPLICATION PACKAGE <% ctx.entities.hello_snowflake_package.identifier %>;
    GRANT SELECT ON TABLE accounts TO SHARE IN APPLICATION PACKAGE <% ctx.entities.hello_snowflake_package.identifier %>;
    

Copy

In this example, `<% ctx.entities.hello_snowflake_package.identifier %>` is a
template that is replaced by the resolved identifier of your `application
package` from the `snowflake.yml` file when you execute a Snowflake CLI
command.

Granting these privileges on the objects within the application package makes
the `shared_data.accounts` table available to all objects created from this
application package. This sharing takes place due to the privileges GRANT TO
SHARE command at the end of the script.

Note

You must grant the USAGE privilege on each schema to an application package
for each schema you want to share with a consumer in an app. You must then
grant the SELECT privilege on the objects within the schema that you want to
share.

  2. Add an entry to the project definition file to ensure that this script runs when you update your application package. The final project definition file should be:
    
        definition_version: 2
    entities:
       hello_snowflake_package:
          type: application package
          stage: stage_content.hello_snowflake_stage
          manifest: app/manifest.yml
          identifier: hello_snowflake_package
          artifacts:
             - src: app/*
               dest: ./
          meta:
             post_deploy:
                - sql_script: scripts/shared_content.sql
       hello_snowflake_app:
          type: application
          from:
             target: hello_snowflake_package
          debug: false
    

Copy

Note

Because the script is executed directly from your local machine, it is not
necessary (nor recommended) to add post-deploy hooks to the `artifacts`
section of your project definition file.

Note

Because post-deploy hooks are executed every time you deploy an app, they must
be written in an idempotent manner.

### Add a view to access data content¶

In this section you update the setup script to add a view that allows the
consumer who installed the app to access the data in the `ACCOUNTS` table that
you created in the previous section.

To add a view to access data content:

  1. To create a schema for the view, add the following to the setup script:
    
        CREATE OR ALTER VERSIONED SCHEMA code_schema;
    GRANT USAGE ON SCHEMA code_schema TO APPLICATION ROLE app_public;
    

Copy

These statements create a versioned schema to contain the view and grant the
USAGE privilege on the schema. The Snowflake Native App Framework uses
versioned schema to handle different versions of stored procedures and
functions.

  2. To create the view, add the following to the setup script:
    
        CREATE VIEW IF NOT EXISTS code_schema.accounts_view
      AS SELECT ID, NAME, VALUE
      FROM shared_data.accounts;
    GRANT SELECT ON VIEW code_schema.accounts_view TO APPLICATION ROLE app_public;
    

Copy

These statements create the view in the `code_schema` schema and grant the
required privilege on the view to the application role.

This updated setup script is also uploaded to the stage the next time you
deploy your app using Snowflake CLI.

### Test the updated app¶

In this subsection, you upgrade the app and query the example table using the
view within the installed app.

To test the updated app, follow these steps:

  1. To update the application package and the application object installed in the consumer account, run the following command:
    
        snow app run -c connection_name
    

Copy

where `connection_name` is the name of the connection you specified in the
`config.toml` file when you installed the Snowflake CLI.

This uploads all the edited files to the stage, runs the
`scripts/shared_content.sql` script, and upgrade the app using those files on
the stage.

  2. To verify that the view works correctly, run the following command:
    
        snow sql -q "SELECT * FROM hello_snowflake_app.code_schema.accounts_view" -c connection_name
    

Copy

The output of this command should be:

    
        +----+----------+-----------+
    | ID | NAME     | VALUE     |
    |----+----------+-----------|
    |  1 | Joe      | Snowflake |
    |  2 | Nima     | Snowflake |
    |  3 | Sally    | Snowflake |
    |  4 | Juan     | Acme      |
    +----+----------+-----------+
    

Copy

### Review what you learned in this section¶

In this section you learned how to include shared data content in your app by
performing the following tasks:

  * Created the `ACCOUNTS` table within the application package and inserted data into the table.

  * Granted reference usage on the `ACCOUNTS` table to the application package.

  * Created a schema and view that references the `ACCOUNTS` table in the application package.

  * Granted usage on the schema to the application role.

  * Granted select on the view to the application role.

You also updated the setup script to perform the following when the
application is installed:

  * Created a schema and view that the app uses to access the example data.

  * Granted usage on the schema to the application role.

  * Granted select on the view to the application role.

## Add python code to your app¶

In this section, you expand the functionality of your app by adding Python
code to enhance the application logic. In this section you include Python code
as the following:

  * An inline Python UDF that is a self-contained function in the setup script.

  * A Python UDF that references a Python file outside the setup script.

Note

Although this section introduces examples using Python, the same techniques
are applicable to Java and JavaScript.

### Add an inline python function as a user-defined function (UDF)¶

In this section you add a Python function as a UDF.

To include a Python UDF in your app, add the following code to your setup
file.

>
>     CREATE OR REPLACE FUNCTION code_schema.addone(i int)
>     RETURNS INT
>     LANGUAGE PYTHON
>     RUNTIME_VERSION = '3.11'
>     HANDLER = 'addone_py'
>     AS
>     $$
>     def addone_py(i):
>       return i+1
>     $$;
>  
>     GRANT USAGE ON FUNCTION code_schema.addone(int) TO APPLICATION ROLE
> app_public;
>  
>
> Copy

These commands perform the following tasks when the app is installed:

  * Create a versioned schema named `code_schema`.

  * Grant the usage privilege on the schema to the `APP_PUBLIC` application role.

  * Create the `ADDONE()` UDF in the `code_schema` schema.

  * Grant the usage privilege on the function to the `APP_PUBLIC` application role.

Note that the schema created in the code example above is a versioned schema.
User-defined functions and stored procedures must be defined in a versioned
schema instead of a normal schema. This prevents app upgrades from interfering
with concurrent code execution.

### Add an external python module¶

To add an external python module to your app:

  1. Add the following Python function to your setup script:
    
        CREATE or REPLACE FUNCTION code_schema.multiply(num1 float, num2 float)
      RETURNS float
      LANGUAGE PYTHON
      RUNTIME_VERSION = 3.9
      IMPORTS = ('/python/hello_python.py')
      HANDLER='hello_python.multiply';
    
    GRANT USAGE ON FUNCTION code_schema.multiply(FLOAT, FLOAT) TO APPLICATION ROLE app_public;
    

Copy

Similar to the previous example, these statement create a Python UDF in a
schema and grants privileges on the function to the application role. However,
this example contains an IMPORTS clause that refers to an external Python file
that you create and include in your named stage.

  2. In the `tutorial` folder create a subfolder named `python`.

  3. In the `python` subfolder, create a file named `hello_python.py`.

  4. Add the following to the `hello_python.py` file:
    
        def multiply(num1, num2):
      return num1*num2
    

Copy

The function defined in this external file matches the inline function defined
in the setup script.

  5. Add the following to the existing `artifacts` section of the project definition file:
    
        - python/hello_python.py
    

Copy

In this section, you added a Python UDF to your app. This UDF refers to an
external Python module that can be referenced by your application package.

### Install and test the updated app¶

To install and test an app:

  1. To update the application package and the app, run the following command:
    
        snow app run -c connection_name
    

Copy

where `connection_name` is the name of the connection you specified in your
`config.toml` when you installed the Snowflake CLI.

This command uploads the edited and new files to the stage and upgrades your
app using the files on the stage.

  2. To test the Python stored procedure, run the following command:
    
        snow sql -q "SELECT hello_snowflake_app.code_schema.addone(1)" -c connection_name
    

Copy

  3. To test the referenced Python function, run the following command:
    
        snow sql -q "SELECT hello_snowflake_app.code_schema.multiply(1,2)" -c connection_name
    

Copy

### Review what you learned in this section¶

In this section, you added the following new functionality to your app:

  * A Python function defined as an inline UDF.

  * A Python function defined as a UDF that references external code.

You also tested each of these examples by installing an updated version of
your app and running each of the functions.

## Add a streamlit app to your app¶

In this section, you complete your Snowflake Native App by adding a Streamlit
user interface. Streamlit is an open source Python framework for developing
data science and machine learning applications. You can include Streamlit apps
within a app to add user interaction and data visualization.

### Create the streamlit app file¶

To create a Streamlit app, follow these steps:

  1. In the `tutorial` folder, create a subfolder named `streamlit`.

  2. In the `streamlit` folder, create a file named `hello_snowflake.py`.

  3. Add the following code to this file:
    
        # Import python packages
    import streamlit as st
    from snowflake.snowpark import Session
    
    # Write directly to the app
    st.title("Hello Snowflake - Streamlit Edition")
    st.write(
       """The following data is from the accounts table in the application package.
          However, the Streamlit app queries this data from a view called
          code_schema.accounts_view.
       """
    )
    
    # Get the current credentials
    session = Session.builder.getOrCreate()
    
    #  Create an example data frame
    data_frame = session.sql("SELECT * FROM code_schema.accounts_view")
    
    # Execute the query and convert it into a Pandas data frame
    queried_data = data_frame.to_pandas()
    
    # Display the Pandas data frame as a Streamlit data frame.
    st.dataframe(queried_data, use_container_width=True)
    

Copy

  4. Add the following to the existing `artifacts` section of the project definition file:
    
        - streamlit/hello_snowflake.py
    

Copy

### Add the streamlit object to the setup script¶

To create the Streamlit object in the app, follow these steps:

  1. Add the following statement at the end of the `setup_script.sql` file to create the Streamlit object:
    
        CREATE STREAMLIT IF NOT EXISTS code_schema.hello_snowflake_streamlit
      FROM '/streamlit'
      MAIN_FILE = '/hello_snowflake.py'
    ;
    

Copy

This statement creates a STREAMLIT object in the core schema.

  2. Add the following statement at the end of the `setup_script.sql` file to allow the APP_PUBLIC role to access the Streamlit object:
    
        GRANT USAGE ON STREAMLIT code_schema.hello_snowflake_streamlit TO APPLICATION ROLE app_public;
    

Copy

### Install the updated app¶

  1. To update the application package and the app, run the following command:
    
        snow app run -c connection_name
    

Copy

where `connection_name` is the name of the connection you specified in the
`config.toml` file when you installed the Snowflake CLI.

This command uploads the edited and new files to the stage and upgrades your
app using those files on the stage. You can then navigate to the URL this
command prints out to see your new Streamlit in action; once you are there,
click on the tab named HELLO_SNOWFLAKE_STREAMLIT that appears beside the name
of your application.

### Review what you learned in this section¶

In this section you added a Streamlit app to your Snowflake Native App by
doing the following:

  * Created a python file that uses the Streamlit library to render a user interface.

  * Created a Streamlit app in your Snowflake Native App that displays shared data.

## Add a version to your app¶

In previous sections, you have been using a “stage development” mode to push
changes. The stage development mode allows you to quickly iterate app
development without having to create new versions or patches. However, you
must create a version of the app to list your application package and share it
with other Snowflake users.

In this section, you add a version to your app that includes all of the
functionality you have added in this tutorial.

  1. To add a version to the `HELLO_SNOWFLAKE_PACKAGE` application package, run the following command:
    
        snow app version create v1_0 -c connection_name
    

Copy

In this command, you modified your application package to add a version based
on the application files that you uploaded to the named stage in an earlier
section.

Note

The value specified for VERSION is a label, not a numerical value or string.

Note

The patch number for the new version you added is automatically created at
`0`. As you add additional patches for a version, these are automatically
incremented. However, when you create a new version, for example `V1_1`, the
patch number for that version is reset to `0`.

  2. To verify that the version was added to the application package, run the following command:
    
        snow app version list -c connection_name
    

Copy

This command shows additional information about the version as shown in the
following output:

    
        +---------+-------+-------+---------+-------------------------------+------------+-----------+-------------+-------+---------------+
    | version | patch | label | comment | created_on                    | dropped_on | log_level | trace_level | state | review_status |
    |---------+-------+-------+---------+-------------------------------+------------+-----------+-------------+-------+---------------|
    | V1_0    | 0     | NULL  | NULL    | 2024-05-09 10:33:39.768 -0700 | NULL       | OFF       | OFF         | READY | NOT_REVIEWED  |
    +---------+-------+-------+---------+-------------------------------+------------+-----------+-------------+-------+---------------+
    

Copy

  3. To install the app based on a version, run the following command:
    
        snow app run --version V1_0 -c connection_name
    

Copy

Because the existing app was created using files on the named stage, upgrading
the app using a version requires the existing app to be dropped and recreated
with this version. Answer yes to the prompt accordingly.

In this section, you modified the application package to include a version for
your app and re-created the application object using versioned development
mode.

## View your app in Snowsight¶

In this section, you view your app in Snowsight. In previous sections, you
used SQL statements to test or find information about your app. However, you
can also view information about your app in Snowsight. You can also view your
deployed Streamlit app.

To view your app in Snowsight, follow these steps:

  1. Sign in to Snowsight.

  2. Switch to the ACCOUNTADMIN role by doing the following:

    1. In the navigation menu, select your username to open the account menu.

    2. Select the active role. For example, PUBLIC.

The role selector appears.

    3. Select the ACCOUNTADMIN role.

  3. Select Data Products » Apps.

  4. Select `HELLO_SNOWFLAKE_APP`.

The `Read Me` tab displays the content you added to the `app/README.md` file
in an earlier section.

  5. To view your Streamlit app, select HELLO_SNOWFLAKE_STREAMLIT.

The content of the `HELLO_SNOWFLAKE_DATA` database displays in a Streamlit
data frame.

  6. To open the app in a worksheet, select Projects » Worksheets.

  7. Select HELLO_SNOWFLAKE_APP from the list of worksheets.

  8. If necessary, select the warehouse where you installed the app.

From the Snowflake worksheet you can test your app using SQL commands. For
example, you can re-run the commands you ran in previous sections to test the
features you added to your application:

    
    
    LIST @hello_snowflake_package.stage_content.hello_snowflake_stage;
    CALL core.hello();
    SELECT * FROM code_schema.accounts_view;
    SELECT code_schema.addone(10);
    SELECT code_schema.multiply(2,3);
    

Copy

Note

Any SQL statements that you add to this worksheet are lost when you navigate
to a different page in Snowsight.

Note

You can also directly view your app’s user interface by using the `snow app
open` command in Snowflake CLI. This command opens the appropriate URL in your
system-configured web browser.

## Publish and install your app¶

In this section, you publish your app by creating a private listing that uses
the application package as the data content. After creating the listing, you
login to another account to install the listing.

### Set the default release directive¶

Before you can create a listing for your application package, you must set the
release directive. A release directive specifies which version and patch of
your app is available to consumers.

In this tutorial you set the default release directive using the version you
added in a previous section.

To set the default release directive on the application package, follow these
steps:

  1. To view the versions and patches defined for your application package, run the following command:
    
        snow app version list -c connection_name
    

Copy

This command displays the versions and patches defined for the application
package.

  2. To set the default release directive to version `v1_0` and patch `0`, run the following command:
    
        snow sql -q "ALTER APPLICATION PACKAGE hello_snowflake_package SET DEFAULT RELEASE DIRECTIVE VERSION = v1_0 PATCH = 0"
    

Copy

The output of this command is shown in the following example:

    
        +-----------------------------------------------------------+
    | status                                                    |
    |-----------------------------------------------------------|
    | Default release directive set to version 'V1_0', patch 0. |
    +-----------------------------------------------------------+
    

Copy

In this section, you verified what versions and patches exist in your
application package. Using this information, you defined the default release
directive for the application package.

### Create a listing for your application¶

Now that you have specified a release directive for your application package,
you create a listing and add the application package as the data content of
the listing. This allows you to share your app with other Snowflake users and
allows them to install and use the app in their account.

To create a listing for your app:

  1. Sign in to Snowsight.

  2. In the navigation menu, select Data Products » Provider Studio.

  3. Select \+ Listing. The Create Listing window opens.

  4. Enter a name for your listing.

  5. In the Who can discover the listing section, select Only specified consumers to privately share the listing with specific accounts.

  6. Click \+ Select to select the application package for the listing.

  7. Enter a description for your listing.

  8. In the Add consumer accounts section, add the account identifier for the account you are using to test the consumer experience of installing the app from a listing.

In this section you created a private listing containing your application
package as the shared data content.

### Install the app in a consumer account¶

In this section you install the app associated with the listing you created in
the previous section. You install the listing in a different account which
mimics how a consumer would install the app in their account.

To install your app from the listing, follow these steps:

  1. Sign in to [Snowsight](../../../user-guide/ui-snowsight).

  2. In the navigation menu, select Data Products » Apps.

  3. Select the tile for the listing under Recently shared with you.

  4. Select Get.

  5. Enter a customer-facing name for the app. For this tutorial, use “Hello Snowflake App”.

  6. Select the warehouse where you want to install the app.

  7. Select Get.

  8. Select Open to view your listing or Done to finish.

In this section you learned how to publish and install a listing that allows
you to share your app with other Snowflake users.

## Learn more¶

Congratulations! Not only have you finished this tutorial, but you have worked
through development and publishing life cycle of an app using the Snowflake
Native App Framework.

Along the way, you:

  * Used Snowsight and Snowflake CLI to build an app using the Snowflake Native App Framework.

    * For more information about Snowsight, refer to [Getting started with worksheets](../../../user-guide/ui-snowsight-worksheets-gs) and [Work with worksheets in Snowsight](../../../user-guide/ui-snowsight-worksheets).

    * For more information about Snowflake Native App in Snowflake CLI, refer to [Using Snowflake Native App in Snowflake CLI](../../snowflake-cli/native-apps/overview).

  * Created the manifest and setup script that are required by all apps.

    * Refer to [Create the manifest file for an application package](../creating-manifest) and [Create a setup script](../creating-setup-script) for details.

  * Created an application package that works as a container for the application logic and data content of your app.

    * Refer to [Create an application package](../creating-app-package) for details.

  * Added logic to your app using stored procedures and UDFs written in Python.

    * Refer to [Add application logic to an application package](../adding-application-logic) for information on using stored procedures, UDFs, and external function in the Snowflake Native App Framework.

    * Refer to [Snowpark API](../../snowpark/index), [Extending Snowflake with Functions and Procedures](../../extensibility) and [Writing external functions](../../../sql-reference/external-functions) for general information on each type of procedure and function.

  * Added shared data content to your app.

    * Refer to [Share data content in a Snowflake Native App](../preparing-data-content) for additional information.

  * Included a Streamlit app in your app.

Refer to [Add a Streamlit app](../adding-streamlit) for additional
information.

  * Viewed your app in Snowsight.

    * Refer to [Working with Apps as a Consumer](https://other-docs.snowflake.com/en/native-apps/consumer-about)

  * Created a private listing for your app and installed the app in a separate Snowflake account.

    * Refer to [Sharing an App with Consumers](https://other-docs.snowflake.com/en/native-apps/provider-publishing-app-package) for information on publish a listing containing an application package.

    * Refer to [Installing an App from a Listing](https://other-docs.snowflake.com/en/native-apps/consumer-installing) for information on how consumers install an app from a listing.

