# Create a Snowpark Container Services service that uses caller’s rights¶

[![Snowflake logo in black \(no text\)](../../../../_images/logo-snowflake-
black.png)](../../../../_images/logo-snowflake-black.png) [Preview
Feature](../../../../release-notes/preview-features) — Open

Configuring caller’s rights for your service is a [preview
feature](../../../../release-notes/preview-features).

## Introduction¶

In this tutorial you explore building a service, presenting a web UI, that
uses the caller’s rights feature when executing SQL queries on behalf of the
users.

You create a service (named `query_service`) that executes a query provided in
the request. By default, application containers connect to Snowflake as the
service user using the service’s owner role. But this application uses the
caller’s rights feature to connect to the service endpoint as the end user and
using privileges granted to that user.

When testing, you use the service from a web browser because the caller’s
rights feature is only supported when accessing a service using network
ingress. The caller’s rights feature is not available when accessing a service
using a service function.

The service does the following:

  * Exposes one public endpoint.

  * When a user logs in to the endpoint, the service provides a Web UI to provide a query. The service executes the query in Snowflake and returns the results. In this tutorial you execute the following SQL command:
    
        SELECT CURRENT_USER(), CURRENT_ROLE();
    

Copy

The command returns the name of the currently logged-in user and the currently
active role, both of which depend on whether caller’s rights is used.

    * When caller’s rights is used, the service connects to Snowflake as the calling user and the user’s default role. The command returns your user name and default role.

    * When caller’s rights is not used, the default behavior kicks in where the service connects to Snowflake as the service user and the service’s owner role. Therefore, the command returns the service user name in the form: `SF$SERVICE$unique-id`, `TEST_ROLE`.

There are two parts to this tutorial:

**Part 1: Create and test a service.** You download code provided for this
tutorial and follow step-by-step instructions:

  1. Download the service code for this tutorial.

  2. Build a Docker image for Snowpark Container Services, and upload the image to a repository in your account.

  3. Create a service.

  4. Communicate with the service using network ingress to connect with the public endpoint that the service exposes. Using a web browser, you login to the public endpoint and execute the SELECT CURRENT_USER(); command. Verify the command output to ensure that the container executed the command as the logged-in user.

**Part 2: Understand the service**. This section provides an overview of the
service code and highlights how the application code uses the caller’s rights.

## Prepare¶

Follow [Common Setup](../common-setup) to configure prerequisites and create
snowflake resources that are required for all Snowpark Container Services
tutorials provided in this documentation.

## Download the service code¶

Code (a Python application) is provided to create the query service.

  1. Download [`SnowparkContainerServices-Tutorials.zip`](../../../../_downloads/c3a8f6109048f2ecca7734c7fd3b0b3b/SnowparkContainerServices-Tutorials.zip).

  2. Unzip the content, which includes one directory for each tutorial. The `Tutorial-6-callers-rights` directory has the following files:

     * `Dockerfile`

     * `main.py`

     * `templates/basic_ui.html`

## Build an image and upload¶

Build an image for the linux/amd64 platform that Snowpark Container Services
supports, and then upload the image to the image repository in your account
(see [Common Setup](../common-setup)).

You will need information about the repository (the repository URL and the
registry hostname) before you can build and upload the image. For more
information, see [Registry and Repositories](../../working-with-registry-
repository).

**Get information about the repository**

  1. To get the repository URL, execute the [SHOW IMAGE REPOSITORIES](../../../../sql-reference/sql/show-image-repositories) SQL command.
    
        SHOW IMAGE REPOSITORIES;
    

Copy

     * The `repository_url` column in the output provides the URL. An example is shown:
        
                <orgname>-<acctname>.registry.snowflakecomputing.com/tutorial_db/data_schema/tutorial_repository
        

     * The host name in the repository URL is the registry host name. An example is shown:
        
                <orgname>-<acctname>.registry.snowflakecomputing.com
        

**Build image and upload it to the repository**

  1. Open a terminal window, and change to the directory containing the files you unzipped.

  2. To build a Docker image, execute the following `docker build` command using the Docker CLI. Note that the command specifies the current working directory (`.`) as the `PATH` for files to use to build the image.
    
        docker build --rm --platform linux/amd64 -t <repository_url>/<image_name> .
    

Copy

     * For `_image_name_`, use `query_service:latest`.

**Example**

    
        docker build --rm --platform linux/amd64 -t myorg-myacct.registry.snowflakecomputing.com/tutorial_db/data_schema/tutorial_repository/query_service:latest .
    

Copy

  3. Upload the image to the repository in your Snowflake account. For Docker to upload an image on your behalf to your repository, you must first authenticate Docker with Snowflake.

    1. To authenticate Docker with the Snowflake registry, execute the following command:
        
                docker login <registry_hostname> -u <username>
        

Copy

       * For `_username_`, specify your Snowflake username. Docker will prompt you for your password.

    2. To upload the image, execute the following command:
        
                docker push <repository_url>/<image_name>
        

Copy

**Example**

        
                docker push myorg-myacct.registry.snowflakecomputing.com/tutorial_db/data_schema/tutorial_repository/query_service:latest
        

Copy

## Create a service¶

In this section you create a service (query_service).

  1. Verify that the compute pool is ready and that you are in the right context to create the service.

    1. Previously, you set the context in the [Common Setup](../common-setup.html#label-snowpark-containers-common-setup-create-objects) step. To ensure that you’re in the right context for the SQL statements in this step, execute the following:

> >     USE ROLE test_role;
>     USE DATABASE tutorial_db;
>     USE SCHEMA data_schema;
>     USE WAREHOUSE tutorial_warehouse;
>  
>
> Copy

    1. To ensure that the compute pool you created in the [common setup](../common-setup.html#label-snowpark-containers-common-setup-create-objects) is ready, execute `DESCRIBE COMPUTE POOL`, and verify that the `state` is `ACTIVE` or `IDLE`. If the `state` is `STARTING`, you need to wait until the `state` changes to either `ACTIVE` or `IDLE`.

> >     DESCRIBE COMPUTE POOL tutorial_compute_pool;
>  
>
> Copy

  2. To create the service, execute the following command using `test_role`:
    
        CREATE SERVICE query_service
      IN COMPUTE POOL tutorial_compute_pool
      FROM SPECIFICATION $$
        spec:
          containers:
          - name: main
            image: /tutorial_db/data_schema/tutorial_repository/query_service:latest
            env:
              SERVER_PORT: 8000
            readinessProbe:
              port: 8000
              path: /healthcheck
          endpoints:
          - name: execute
            port: 8000
            public: true
        capabilities:
          securityContext:
            executeAsCaller: true
        serviceRoles:
        - name: ui_usage
          endpoints:
          - execute
    $$;
    

Copy

Note

If a service with that name already exists, use the DROP SERVICE command to
delete the previously created service, and then create this service.

  3. Execute the following SQL commands to get detailed information about the service you just created. For more information, see [Snowpark Container Services: Working with services](../../working-with-services).

     * To list services in your account, execute the SHOW SERVICES command:
        
                SHOW SERVICES;
        

Copy

     * To get the status of your service, execute the SHOW SERVICE CONTAINERS IN SERVICE command:
        
                SHOW SERVICE CONTAINERS IN SERVICE query_service;
        

Copy

     * To get information about your service, execute the DESCRIBE SERVICE command:
        
                DESCRIBE SERVICE query_service;
        

Copy

## Use the service¶

In this section you verify that the [caller’s rights](../../additional-
considerations-services-jobs.html#label-spcs-additional-considerations-
configuring-callers-rights) configured for the service work. You log in to the
public endpoint from a browser, execute a query, and verify that the Snowflake
session that the service created operates as the calling user, instead of as
the service user.

First, to set up the context for the SQL statements in this section, execute
the following:

    
    
    USE ROLE test_role;
    USE DATABASE tutorial_db;
    USE SCHEMA data_schema;
    USE WAREHOUSE tutorial_warehouse;
    

Copy

The service exposes a public endpoint (see the inline specification provided
in the CREATE SERVICE command); therefore, first log in to the endpoint using
a web browser, then use the web UI that the service exposes to the internet to
send query requests to the service endpoint.

  1. Find the URL of the public endpoint that the service exposes:
    
        SHOW ENDPOINTS IN SERVICE query_service;
    

Copy

The `ingress_url` column in the response provides the URL.

**Example**

    
        p6bye-myorg-myacct.snowflakecomputing.app
    

  2. Append `/ui` to the endpoint URL, and paste it in the web browser. This causes the service to execute the `ui()` function (see `main.py`).

Note that the first time you access the endpoint URL, you will be asked to log
in to Snowflake.

  3. Use the same user that you used to create the service. Upon successful login, the service shows the following Web UI.

[![Web form to communicate with query service.](../../../../_images/spcs-
tutorial-query-service-10.png)](../../../../_images/spcs-tutorial-query-
service-10.png)

Enter the following command in the text box and press enter to see the
results.

    
        SELECT CURRENT_USER(), CURRENT_ROLE()DONE;
    

Copy

Because you included the `executeAsCaller` capability in the service
specification, when a request arrives, Snowflake inserts the `Sf-Context-
Current-User-Token` header in the request and then forwards the request to
your service endpoint.

For illustration purposes, the service code in this tutorial executes the
query both as the caller and the service user.

[![Web form to communicate with the query service.](../../../../_images/spcs-
tutorial-query-service-20.png)](../../../../_images/spcs-tutorial-query-
service-20.png)

     * **Executes the query on behalf of the caller (ingress user):** In this case, the code uses the user token that Snowflake provides to construct a login token for connecting with Snowflake. Thus, the service uses the caller’s rights. Snowflake executes the query on behalf of the caller, displaying the caller’s name and active role name in the query result. For example:
        
                ['TESTUSER, PUBLIC']
        

     * **Executes the query on behalf of the service user:** In this case, the code doesn’t use the user token that Snowflake provides in the request when constructing the login token to connect with Snowflake. Thus, the service doesn’t utilize the caller’s rights, causing Snowflake to execute the query on behalf of the service user. The query result shows the service user’s name (which is the same as the service name) and the active role.
        
                ['QUERY_SERVICE, TEST_ROLE']
        

When the service executes the query (`SELECT CURRENT_USER(), CURRENT_ROLE();`)
on behalf of the caller, Snowflake doesn’t need the user’s warehouse to
execute this simple query. Therefore, the service didn’t need any [caller
grants](../../additional-considerations-services-jobs.html#label-spcs-
granting-caller-permissions-to-service). In the next section, the service
executes a non-trivial query on behalf of the calling user that requires you
to grant [caller grants](../../additional-considerations-services-
jobs.html#label-spcs-granting-caller-permissions-to-service) to the service.

Note

You can access the ingress endpoint programmatically. For sample code, see
[Public endpoint access from outside Snowflake and
authentication](../../working-with-services.html#label-snowpark-containers-
service-public-endpoint-access). Note that you need to append `/ui` to the
endpoint URL in the code so that Snowflake can route the request to the `ui()`
function in the service code.

## Use the service with caller grants¶

In this section, the service executes the following query on behalf of the
caller (the user who logs in the service’s ingress endpoint).

    
    
    SELECT * FROM ingress_user_db.ingress_user_schema.ingress_user_table;
    

Copy

The service doesn’t have permissions to access the table and doesn’t have
permission to run the query in the default warehouse. To enable the service to
execute this query on behalf of the caller, you grant the required [caller
grants](../../additional-considerations-services-jobs.html#label-spcs-
granting-caller-permissions-to-service) to the service.

To demonstrate the scenario, you create a new role (`ingress_user_role`) and a
table (`ingress_user_table`) that’s accessible to the new role but not to the
service’s owner role (`test_role`). Therefore, when the service attempts to
execute the query using the service credentials, Snowflake returns an error.
But when the service executes the query on behalf of the user, Snowflake
executes the query and returns the result.

### Create roles and resources¶

  1. Create a role (`ingress_user_role`) and a database (`ingress_user_db`) that only this role can access. You then grant this role to the your user, so that the user can log in to the service’s public endpoint and query this table.
    
        USE ROLE accountadmin;
    
    CREATE ROLE ingress_user_role;
    GRANT ROLE ingress_user_role TO USER <your_user_name>;
    
    GRANT USAGE ON WAREHOUSE tutorial_warehouse TO ROLE ingress_user_role;
    
    CREATE DATABASE IF NOT EXISTS ingress_user_db;
    GRANT OWNERSHIP ON DATABASE ingress_user_db TO ROLE ingress_user_role COPY CURRENT GRANTS;
    

Copy

  2. Create a table (`ingress_user_table`) that only the `ingress_user_role` role can access.
    
        USE ROLE ingress_user_role;
    
    CREATE SCHEMA IF NOT EXISTS ingress_user_db.ingress_user_schema;
    USE WAREHOUSE tutorial_warehouse;
    CREATE TABLE ingress_user_db.ingress_user_schema.ingress_user_table (col string) AS (
        SELECT 'this table is only accessible to the ingress_user_role'
    );
    

Copy

Note that when the service tries to query the table on behalf of the caller,
the service operates only as a `test_role`, the role that was used to create
the service (the service’s owner role). This role does not have permissions to
access the user table.

  3. Grant caller grants to the service’s owner role (`test_role`) to query tables in the `ingress_user_db` database. This privilege allows the service to query tables in this database only if the following are true:

     * The service is using a [caller’s rights session](../../additional-considerations-services-jobs.html#label-spcs-granting-caller-permissions-to-service).

     * In the session, the caller also has permission to execute these queries.
    
        USE ROLE accountadmin;
    
    GRANT CALLER USAGE ON DATABASE ingress_user_db TO ROLE test_role;
    GRANT INHERITED CALLER USAGE ON ALL SCHEMAS IN DATABASE ingress_user_db TO ROLE test_role;
    GRANT INHERITED CALLER SELECT ON ALL TABLES IN DATABASE ingress_user_db TO ROLE test_role;
    GRANT CALLER USAGE ON WAREHOUSE tutorial_warehouse TO ROLE test_role;
    SHOW CALLER GRANTS TO ROLE test_role;
    

Copy

  4. Configure the default warehouse and default secondary roles.

When a session is created for a user, Snowflake activates the default primary
role, default secondary roles, and the default warehouse of the logged-in
user. In this tutorial,

     * You set the `DEFAULT_SECONDARY_ROLES` to ALL so that when a session is created for the current user, Snowflake sets the current secondary roles to be all roles granted to the user.

     * You also set the default warehouse to `tutorial_warehouse` where the `ingress_user_table` queries are executed.
    
        ALTER USER SET DEFAULT_SECONDARY_ROLES = ('ALL');
    ALTER USER SET DEFAULT_WAREHOUSE = TUTORIAL_WAREHOUSE;
    

Copy

Note the following:

     * In this tutorial, you log in to the public endpoint of the service. The user has `test_role` as the primary role and the `ingress_user_role` as the secondary role. This allows the session to do anything that the `ingress_user_role` allows.

     * The default role and default warehouse only affect the role and warehouse activated when the service establishes a session on behalf of your user. After a caller’s rights session is established you cannot change the role, but you can change the warehouse.

### Use the service and test the caller grants¶

  1. Find the URL of the public endpoint that the service exposes:
    
        SHOW ENDPOINTS IN SERVICE tutorial_db.data_schema.query_service;
    

Copy

The `ingress_url` column in the response provides the URL.

**Example**

    
        p6bye-myorg-myacct.snowflakecomputing.app
    

  2. Append `/ui` to the endpoint URL, and paste it in the web browser. This causes the service to execute the `ui()` function (see `echo_service.py`).: Note that the first time you access the endpoint URL, you will be asked to log in to Snowflake. For this test, use the same user that you used to create the service to ensure that the user has the necessary privileges.:

  3. Use the same user that you used to create the service. Upon successful login, the service shows the following Web UI.

[![Web form to communicate with the query service.](../../../../_images/spcs-
tutorial-query-service-10.png)](../../../../_images/spcs-tutorial-query-
service-10.png)

Enter the following command in the text box and press enter to see the
results.

    
        SELECT * FROM ingress_user_db.ingress_user_schema.ingress_user_table;
    

Copy

For illustration purposes the service code in this tutorial executes the query
both as the caller and the service user.

     * **Executes the query on behalf of the caller (ingress user):** In this case, the code uses the user token provided by Snowflake to construct a login token for connecting with Snowflake. Thus, the service uses the caller’s rights. Snowflake executes the query on behalf of the caller. Because the caller is using the `ingress_user_role role` that has the privilege to query the `ingress_user_table` table, the query returns one row in the result:
        
                ['this table is only accessible to ingress_user_role']
        

     * **Executes the query on behalf of the service user:** In this case, the code does not use the user token that Snowflake provides in the request when constructing the login token to connect with Snowflake. Thus, Snowflake executes the query on behalf of the service user. Because the service owner uses the default `test_role`, which does not have permission to query the table, you see an error:
        
                Encountered an error when executing query:... SQL compilation error: Database 'INGRESS_USER_DB' does not exist or not authorized.
        

[![Web form to communicate with echo
service.](../../../../_images/Tutorial-6-restricted-callers-
rights-10.png)](../../../../_images/Tutorial-6-restricted-callers-
rights-10.png)

## Cleanup¶

You should remove billable resources that you created. For more information,
see Step 5 in [Tutorial 3](tutorial-3).

## Reviewing the service code¶

This section covers the following topics:

  * Examining the tutorial code: Review the code files that implement the query service.

### Examining the tutorial code¶

The zip file you downloaded in Step 1 includes the following files:

  * `Dockerfile`

  * `main.py`

  * `templates/basic_ui.html`

You also use service specification when creating the service. The following
section explains how these code components work together to create the
service.

#### main.py file¶

This Python file contains the code that implements a minimal HTTP server that
executes a query in the request and returns query results. The code provides a
web user interface (UI) for submitting echo requests.

    
    
    from flask import Flask
    from flask import request
    from flask import render_template
    import logging
    import os
    import sys
    
    from snowflake.snowpark import Session
    from snowflake.snowpark.exceptions import *
    
    # Environment variables below will be automatically populated by Snowflake.
    SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
    SNOWFLAKE_HOST = os.getenv("SNOWFLAKE_HOST")
    SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
    SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")
    
    # Custom environment variables
    SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
    SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
    SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE")
    SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
    
    SERVICE_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT = os.getenv("SERVER_PORT", 8080)
    
    
    def get_logger(logger_name):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(
            logging.Formatter("%(name)s [%(asctime)s] [%(levelname)s] %(message)s")
        )
        logger.addHandler(handler)
        return logger
    
    
    def get_login_token():
        """
        Read the login token supplied automatically by Snowflake. These tokens
        are short lived and should always be read right before creating any new connection.
        """
        with open("/snowflake/session/token", "r") as f:
            return f.read()
    
    
    def get_connection_params(ingress_user_token=None):
        """
        Construct Snowflake connection params from environment variables.
        """
        if os.path.exists("/snowflake/session/token"):
            if ingress_user_token:
                logger.info("Creating a session on behalf of user.")
                token = get_login_token() + "." + ingress_user_token
            else:
                logger.info("Creating a session as service user.")
                token = get_login_token()
    
            return {
                "account": SNOWFLAKE_ACCOUNT,
                "host": SNOWFLAKE_HOST,
                "authenticator": "oauth",
                "token": token,
                "warehouse": SNOWFLAKE_WAREHOUSE,
                "database": SNOWFLAKE_DATABASE,
                "schema": SNOWFLAKE_SCHEMA,
            }
        else:
            return {
                "account": SNOWFLAKE_ACCOUNT,
                "host": SNOWFLAKE_HOST,
                "user": SNOWFLAKE_USER,
                "password": SNOWFLAKE_PASSWORD,
                "role": SNOWFLAKE_ROLE,
                "warehouse": SNOWFLAKE_WAREHOUSE,
                "database": SNOWFLAKE_DATABASE,
                "schema": SNOWFLAKE_SCHEMA,
            }
    
    
    logger = get_logger("query-service")
    app = Flask(__name__)
    
    
    @app.get("/healthcheck")
    def readiness_probe():
        return "I'm ready!"
    
    
    @app.route("/ui", methods=["GET", "POST"])
    def ui():
        """
        Main handler for providing a web UI.
        """
        if request.method == "POST":
            # get ingress user token
            ingress_user = request.headers.get("Sf-Context-Current-User")
            ingress_user_token = request.headers.get("Sf-Context-Current-User-Token")
    
            if ingress_user:
                logger.info(f"Received a request from user {ingress_user}")
    
            # getting input in HTML form
            query = request.form.get("query")
            if query:
                logger.info(f"Received a request for query: {query}.")
                query_result_ingress_user = (
                    run_query(query, ingress_user_token)
                    if ingress_user_token
                    else "Token is missing. Can't execute as ingress user."
                )
                query_result_service_user = run_query(query)
                return render_template(
                    "basic_ui.html",
                    query_input=query,
                    query_result_ingress_user=query_result_ingress_user,
                    query_result_service_user=query_result_service_user,
                )
        return render_template("basic_ui.html")
    
    
    @app.route("/query", methods=["GET"])
    def query():
        """
        Main handler for providing programmatic access.
        """
        # get ingress user token
        query = request.args.get("query")
        logger.info(f"Received query request: {query}.")
        if query:
            ingress_user = request.headers.get("Sf-Context-Current-User")
            ingress_user_token = request.headers.get("Sf-Context-Current-User-Token")
    
            if ingress_user:
                logger.info(f"Received a request from user {ingress_user}")
    
            res = run_query(query, ingress_user_token)
            return str(res)
        return "DONE"
    
    
    def run_query(query, ingress_user_token=None):
        # start a Snowflake session as the ingress user
        try:
            with Session.builder.configs(
                get_connection_params(ingress_user_token)
            ).create() as session:
                logger.info(
                    f"Snowflake connection established (id={session.session_id}). Now executing query: {query}."
                )
                try:
                    res = session.sql(query).collect()
                    logger.info(f"Query execution done: {query}.")
                    return (
                        "[Empty Result]"
                        if len(res) == 0
                        else [", ".join(row) for row in res]
                    )
                except Exception as e:
                    return "Encountered an error when executing query: " + str(e)
        except Exception as e:
            return "Encountered an error when connecting to Snowflake: " + str(e)
    
    if __name__ == '__main__':
      app.run(host=SERVICE_HOST, port=SERVER_PORT)
    

Copy

In the code:

  * The `ui` function displays the following web form and handles query requests submitted from the web form.

[![Web form to communicate with query service.](../../../../_images/spcs-
tutorial-query-service-10.png)](../../../../_images/spcs-tutorial-query-
service-10.png)

This function uses the `@app.route()` decorator to specify that requests for
`/ui` are handled by this function:

    
        @app.route("/ui", methods=["GET", "POST"])
    def ui():
    

Copy

The query service exposes the `execute` endpoint publicly (see the inline
service specification you provided when creating the service), enabling
communication with the service over the web. When you load the URL of the
public endpoint with /ui appended in your browser, the browser sends an HTTP
GET request for this path, and the server routes the request to this function.
The function executes and returns a simple HTML form for the user to enter a
query.

After the user enters a query and submits the form, the browser sends an HTTP
POST request for this path. Because the service specification includes the
`executeAsCaller` capability, Snowflake adds the `Sf-Context-Current-User-
Token` header to the incoming request and forwards the request to this same
function (see [Connecting to Snowflake using caller’s
rights](../../additional-considerations-services-jobs.html#label-spcs-
additional-considerations-configuring-callers-rights)).

The code executes the `run_query` function twice:

    * As the ingress user. In this case, the login token is concatenation of both OAuth token and ingress user token.
        
                token = get_login_token() + "." + ingress_user_token
        

Copy

    * As the service user. In this case the login token is only the OAuth token.

> >         token = get_login_token()
>  
>
> Copy

  * The `readiness_probe` function uses the `@app.get()` decorator to specify that requests for `/healthcheck` are handled by this function:
    
        @app.get("/healthcheck")
    def readiness_probe():
    

Copy

This function enables Snowflake to check the readiness of the service. When
the container starts, Snowflake wants to confirm that the application is
working and that the service is ready to serve the requests. Snowflake sends
an HTTP GET request with this path (as a health probe, readiness probe) to
ensure that only healthy containers serve traffic. The function can do
whatever you want.

  * The `get_logger` function helps set up logging.

#### Dockerfile¶

This file contains all the commands to build an image using Docker.

    
    
    ARG BASE_IMAGE=python:3.10-slim-buster
    FROM $BASE_IMAGE
    COPY main.py ./
    COPY templates/ ./templates/
    RUN pip install --upgrade pip && pip install flask snowflake-snowpark-python
    CMD ["python", "main.py"]
    

Copy

The Dockerfile contains instructions to install the Flask library ind the
Docker container. The code in `main.py` relies on the Flask library to handle
HTTP requests.

#### /template/basic_ui.html¶

The query service exposes the `echoendpoint` endpoint publicly (see service
specification), enabling communication with the service over the web. When you
load the public endpoint URL with `/ui` appended in your browser, the query
service displays this form.

[![Web form to communicate with query service.](../../../../_images/spcs-
tutorial-query-service-10.png)](../../../../_images/spcs-tutorial-query-
service-10.png)

You can enter a query in the form and submit the form, and the service returns
the results in an HTTP response.

    
    
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <title>Welcome to the query service!</title>
      </head>
      <body>
        <h1>Welcome to the query service!</h1>
        <form action="{{ url_for("ui") }}" method="post">
          <label for="query">query:<label><br>
          <input type="text" id="query" name="query" size="50"><br>
        </form>
        <h2>Query:</h2>
        {{ query_input }}
        <h2>Result (executed on behalf of ingress user):</h2>
        {{ query_result_ingress_user }}
        <h2>Result (executed as service user):</h2>
        {{ query_result_service_user }}
      </body>
    </html>
    

Copy

#### Service specification¶

Snowflake uses information you provide in this specification to configure and
run your service.

    
    
    spec:
      containers:
      - name: main
        image: /tutorial_db/data_schema/tutorial_repository/query_service:latest
        env:
          SERVER_PORT: 8000
        readinessProbe:
          port: 8000
          path: /healthcheck
      endpoints:
      - name: execute
        port: 8000
        public: true
    capabilities:
      securityContext:
        executeAsCaller: true
    serviceRoles:
    - name: ui_usage
      endpoints:
      - execute
    

Copy

In the service specification, the `spec`, `capabilities`, and `serviceRoles`
are the top-level fields.

  * `spec` provides specification details (see [Service specification reference](../../specification-reference)). Note that the service exposes one public endpoint (`execute`) that enables ingress access to the service from the public web.

  * `capabilities` Specifies the `executeAsCaller` capability. This tells Snowflake that the application intends to use [caller’s rights](../../additional-considerations-services-jobs.html#label-spcs-additional-considerations-configuring-callers-rights).

  * `serviceRoles` specifies one service role (`ui_usage`) and endpoint name (`execute`) to grant the USAGE privilege on.

  * The `readinessProbe` field identifies the `port` and `path` that Snowflake can use to send an HTTP GET request to the readiness probe to verify that the service is ready to handle traffic.

The service code (`echo_python.py`) implements the readiness probe as follows:

    
        @app.get("/healthcheck")
    def readiness_probe():
    

Copy

Therefore, the specification file includes the `container.readinessProbe`
field accordingly.

For more information about service specifications, see [Service specification
reference](../../specification-reference).

## What’s next?¶

Now that you’ve completed this tutorial, you can return to [Working with
Services](../../working-with-services) to explore other topics.

