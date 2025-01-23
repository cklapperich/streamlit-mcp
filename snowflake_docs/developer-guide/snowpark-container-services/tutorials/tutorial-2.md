# Tutorial 2: Create a Snowpark Container Services Job Service¶

[![Snowflake logo in black \(no text\)](../../../_images/logo-snowflake-
black.png)](../../../_images/logo-snowflake-black.png) Feature — Generally
Available

Available to accounts in [AWS and Microsoft Azure commercial
regions](../../../user-guide/intro-regions.html#label-na-general-regions),
with some exceptions. For more information, see [Available
regions](../overview.html#label-snowpark-containers-overview-available-
regions).

## Introduction¶

After completing the [Tutorial Common Setup](common-setup), you are ready to
create a job service. In this tutorial, you create a simple job service that
connects to Snowflake, executes a SQL SELECT query, and saves the result to a
table.

There are two parts to this tutorial:

**Part 1: Create and test a job service.** You download code provided for this
tutorial and follow step-by-step instructions:

  1. Download the job service code for this tutorial.

  2. Build a Docker image for Snowpark Container Services, and upload the image to a repository in your account.

  3. Stage the service specification file, which gives Snowflake the container configuration information. In addition to the name of the image to use to start a container, the specification file specifies three arguments: a SELECT query, a virtual warehouse to execute the query, and the name of the table to save the result to.

  4. Execute the job service. Using the EXECUTE JOB SERVICE command, you can execute the job service by providing the specification file and the compute pool where Snowflake can run the container. And finally, verify the service results.

**Part 2: Understand the job service code**. This section provides an overview
of the job service code and highlights how different components collaborate.

## 1: Download the job service code¶

Code (a Python application) is provided to implement a job service.

  1. Download [`SnowparkContainerServices-Tutorials.zip`](../../../_downloads/c3a8f6109048f2ecca7734c7fd3b0b3b/SnowparkContainerServices-Tutorials.zip).

  2. Unzip the content, which includes one directory for each tutorial. The `Tutorial-2` directory has the following files:

     * `main.py`

     * `Dockerfile`

     * `my_job_spec.yaml`

## 2: Build and upload an image¶

Build an image for the linux/amd64 platform that Snowpark Container Services
supports, and then upload the image to the image repository in your account
(see [Common Setup](common-setup)).

You will need information about the repository (the repository URL and the
registry hostname) before you can build and upload the image. For more
information, see [Registry and Repositories](../working-with-registry-
repository).

**Get information about the repository**

  1. To get the repository URL, execute the [SHOW IMAGE REPOSITORIES](../../../sql-reference/sql/show-image-repositories) SQL command.
    
        SHOW IMAGE REPOSITORIES;
    

Copy

     * The `repository_url` column in the output provides the URL. An example is shown:
        
                <orgname>-<acctname>.registry.snowflakecomputing.com/tutorial_db/data_schema/tutorial_repository
        

     * The host name in the repository URL is registry host name. An example is shown:
        
                <orgname>-<acctname>.registry.snowflakecomputing.com
        

**Build image and upload it to the repository**

  1. Open a terminal window, and change to the directory containing the files you unzipped.

  2. To build a Docker image, execute the following `docker build` command using the Docker CLI. Note the command specifies current working directory (.) as the `PATH` for files to use for building the image.
    
        docker build --rm --platform linux/amd64 -t <repository_url>/<image_name> .
    

Copy

     * For `_image_name_`, use `my_job_image:latest`.

**Example**

    
        docker build --rm --platform linux/amd64 -t myorg-myacct.registry.snowflakecomputing.com/tutorial_db/data_schema/tutorial_repository/my_job_image:latest .
    

Copy

  3. Upload the image to the repository in your Snowflake account. In order for Docker to upload an image on your behalf to your repository, you must first [authenticate Docker with the registry](../working-with-registry-repository.html#label-registry-and-repository-authentication).

    1. To authenticate Docker with the Snowflake registry, execute the following command.
        
                docker login <registry_hostname> -u <username>
        

Copy

       * For `_username_`, specify your Snowflake username. Docker will prompt you for your password.

    2. To upload the image execute the following command:
        
                docker push <repository_url>/<image_name>
        

Copy

**Example**

        
                docker push myorg-myacct.registry.snowflakecomputing.com/tutorial_db/data_schema/tutorial_repository/my_job_image:latest
        

Copy

## 3: Stage the specification file¶

  * To upload your service specification file (`my_job_spec.yaml`) to the stage, use one of the following options:

    * **The Snowsight web interface:** For instructions, see [Choosing an internal stage for local files](../../../user-guide/data-load-local-file-system-create-stage).

    * **The SnowSQL CLI:** Execute the following [PUT](../../../sql-reference/sql/put) command:
        
                PUT file://<file-path>[/\]my_job_spec.yaml @tutorial_stage
          AUTO_COMPRESS=FALSE
          OVERWRITE=TRUE;
        

Copy

For example:

      * Linux or macOS
            
                        PUT file:///tmp/my_job_spec.yaml @tutorial_stage
              AUTO_COMPRESS=FALSE
              OVERWRITE=TRUE;
            

Copy

      * Windows
            
                        PUT file://C:\temp\my_job_spec.yaml @tutorial_stage
              AUTO_COMPRESS=FALSE
              OVERWRITE=TRUE;
            

Copy

You can also specify a relative path.

        
                PUT file://./my_job_spec.yaml @tutorial_stage
          AUTO_COMPRESS=FALSE
          OVERWRITE=TRUE;
        

Copy

The command sets OVERWRITE=TRUE so that you can upload the file again, if
needed (for example, if you fixed an error in your specification file). If the
PUT command is executed successfully, information about the uploaded file is
printed out.

## 4: Execute the job service¶

Now you are ready to create a job.

  1. To start a job service, run the EXECUTE JOB SERVICE command:
    
        EXECUTE JOB SERVICE
      IN COMPUTE POOL tutorial_compute_pool
      NAME=tutorial_2_job_service
      FROM @tutorial_stage
      SPEC='my_job_spec.yaml';
    

Copy

Note the following:

     * FROM and SPEC provide the stage name and the name of the job service specification file. When the job service is executed, it runs the SQL statement and saves the result to a table as specified in `my_job_spec.yaml`.

The SQL statement is not executed within the Docker container. Instead, the
running container connects to Snowflake and runs the SQL statement in a
Snowflake warehouse.

     * COMPUTE_POOL provides the compute resources where Snowflake executes the job service.

     * EXECUTE JOB SERVICE returns output that includes the job name, as shown in the following sample output:
        
                +------------------------------------------------------------------------------------+
        |                      status                                                        |
        -------------------------------------------------------------------------------------+
        | Job TUTORIAL_2_JOB_SERVICE completed successfully with status: DONE.               |
        +------------------------------------------------------------------------------------+
        

  2. The job service runs a simple query and saves result to the results table. You can verify the job service successfully completed by querying the results table:
    
        SELECT * FROM results;
    

Copy

Sample output:

    
        +----------+-----------+
    | TIME     | TEXT      |
    |----------+-----------|
    | 10:56:52 | hello     |
    +----------+-----------+
    

  3. If you want to debug execution of your job service, execute SHOW SERVICE CONTAINERS IN SERVICE to determine if the job service is still running, if it failed to start, or why it failed if it did. Also, assuming your code outputs useful logs to standard output or standard error, you can access the logs using SYSTEM$GET_SERVICE_LOGS.

>     1. To get the job service status, execute [SHOW SERVICE CONTAINERS IN
> SERVICE](../../../sql-reference/sql/show-service-containers-in-service):
>  
>         >         SHOW SERVICE CONTAINERS IN SERVICE tutorial_2_job_service;
>  
>
> Copy
>
> Sample output:
>  
>         >
> +---------------+-------------+------------------------+-------------+----------------+--------+------------------------+----------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+---------------+------------+
>         | database_name | schema_name | service_name           | instance_id | container_name | status | message                | image_name                                                                                                                             | image_digest                                                            | restart_count | start_time |
>
> |---------------+-------------+------------------------+-------------+----------------+--------+------------------------+----------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+---------------+------------|
>         | TUTORIAL_DB   | DATA_SCHEMA | TUTORIAL_2_JOB_SERVICE | 0           | main           | DONE   | Completed successfully | myorg-myacct.registry.snowflakecomputing.com/tutorial_db/tutorial_db/data_schema/tutorial_repository/my_job_image:latest | sha256:aa3fa2e5c1552d16904a5bbc97d400316ebb4a608bb110467410485491d9d8d0 |             0 |            |
>
> +---------------+-------------+------------------------+-------------+----------------+--------+------------------------+----------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+---------------+------------+
>  
>
>     2. To get the job service log information, use the system function
> [SYSTEM$GET_SERVICE_LOGS](../../../sql-
> reference/functions/system_get_service_logs):
>  
>         >         SELECT SYSTEM$GET_SERVICE_LOGS('tutorial_2_job_service',
> 0, 'main')
>  
>
> Copy
>  
>         >         job-tutorial - INFO - Job started
>         job-tutorial - INFO - Connection succeeded. Current session context:
> database="TUTORIAL_DB", schema="DATA_SCHEMA",
> warehouse="TUTORIAL_WAREHOUSE", role="TEST_ROLE"
>         job-tutorial - INFO - Executing query [select current_time() as
> time,'hello'] and writing result to table [results]
>         job-tutorial - INFO - Job finished
>  

## 5: Clean up¶

If you do not plan to continue with [Tutorial 3](advanced/tutorial-3), you
should remove billable resources you created. For more information, see Step 5
in [Tutorial 3](advanced/tutorial-3).

## 6: Reviewing the job service code¶

This section covers the following topics:

  * Examining the files provided: Review various code files that implement the job service.

  * Building and testing an image locally. The section provides an explanation of how you can locally test the Docker image before uploading it to a repository in your Snowflake account.

### Examining the files provided¶

The zip file you downloaded at the beginning of the tutorial includes the
following files:

  * `main.py`

  * `Dockerfile`

  * `my_job_spec.yaml`

This section provides an overview of the code.

#### main.py file¶

    
    
    #!/opt/conda/bin/python3
    
    import argparse
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
    
    
    def get_arg_parser():
      """
      Input argument list.
      """
      parser = argparse.ArgumentParser()
      parser.add_argument("--query", required=True, help="query text to execute")
      parser.add_argument(
        "--result_table",
        required=True,
        help="name of the table to store result of query specified by flag --query")
    
      return parser
    
    
    def get_logger():
      """
      Get a logger for local logging.
      """
      logger = logging.getLogger("job-tutorial")
      logger.setLevel(logging.DEBUG)
      handler = logging.StreamHandler(sys.stdout)
      handler.setLevel(logging.DEBUG)
      formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
      handler.setFormatter(formatter)
      logger.addHandler(handler)
      return logger
    
    
    def get_login_token():
      """
      Read the login token supplied automatically by Snowflake. These tokens
      are short lived and should always be read right before creating any new connection.
      """
      with open("/snowflake/session/token", "r") as f:
        return f.read()
    
    
    def get_connection_params():
      """
      Construct Snowflake connection params from environment variables.
      """
      if os.path.exists("/snowflake/session/token"):
        return {
          "account": SNOWFLAKE_ACCOUNT,
          "host": SNOWFLAKE_HOST,
          "authenticator": "oauth",
          "token": get_login_token(),
          "warehouse": SNOWFLAKE_WAREHOUSE,
          "database": SNOWFLAKE_DATABASE,
          "schema": SNOWFLAKE_SCHEMA
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
          "schema": SNOWFLAKE_SCHEMA
        }
    
    def run_job():
      """
      Main body of this job.
      """
      logger = get_logger()
      logger.info("Job started")
    
      # Parse input arguments
      args = get_arg_parser().parse_args()
      query = args.query
      result_table = args.result_table
    
      # Start a Snowflake session, run the query and write results to specified table
      with Session.builder.configs(get_connection_params()).create() as session:
        # Print out current session context information.
        database = session.get_current_database()
        schema = session.get_current_schema()
        warehouse = session.get_current_warehouse()
        role = session.get_current_role()
        logger.info(
          f"Connection succeeded. Current session context: database={database}, schema={schema}, warehouse={warehouse}, role={role}"
        )
    
        # Execute query and persist results in a table.
        logger.info(
          f"Executing query [{query}] and writing result to table [{result_table}]"
        )
        res = session.sql(query)
        # If the table already exists, the query result must match the table scheme.
        # If the table does not exist, this will create a new table.
        res.write.mode("append").save_as_table(result_table)
    
      logger.info("Job finished")
    
    
    if __name__ == "__main__":
      run_job()
    

Copy

In the code:

  * Python code executes at `main`, which then executes the `run_job()` function:
    
        if __name__ == "__main__":
      run_job()
    

Copy

  * The `run_job()` function reads the environment variables and uses them to set default values for various parameters. The container uses these parameters to connect to Snowflake. Note that:

    * You can override the parameter values, used in the service, using the `containers.env` and `containers.args` fields in the service specification. For more information, see [Service specification reference](../specification-reference).

    * When the image runs in Snowflake, Snowflake populates some of these parameters (see source code) automatically. However, when testing the image locally, you need to explicitly provide these parameters (as shown in the next section, Building and testing an image locally).

#### Dockerfile¶

This file contains all the commands to build an image using Docker.

    
    
    ARG BASE_IMAGE=continuumio/miniconda3:4.12.0
    FROM $BASE_IMAGE
    RUN conda install python=3.8 && \
      conda install snowflake-snowpark-python
    COPY main.py ./
    ENTRYPOINT ["python3", "main.py"]
    

Copy

#### my_job_spec.yaml File (Service Specification)¶

Snowflake uses information you provide in this specification to configure and
run your job service.

    
    
    spec:
      containers:
      - name: main
        image: /tutorial_db/data_schema/tutorial_repository/my_job_image:latest
        env:
          SNOWFLAKE_WAREHOUSE: tutorial_warehouse
        args:
        - "--query=select current_time() as time,'hello'"
        - "--result_table=results"
    

Copy

In addition to the `container.name` and `container.image` required fields (see
[Service specification reference](../specification-reference)), the
specification includes the optional `container.args` field to list the
arguments:

  * `--query` provides the query to execute when the service runs.

  * `--result_table` identifies the table to save the query results.

### Building and testing an image locally¶

You can test the Docker image locally before uploading it to a repository in
your Snowflake account. In local testing, your container runs standalone (it
is not a job service that Snowflake executes).

Use the following steps to test the Tutorial 2 Docker image:

  1. To create a Docker image, in the Docker CLI, execute the `docker build` command:
    
        docker build --rm -t my_service:local .
    

Copy

  2. To launch your code, execute the `docker run` command, providing `<orgname>-<acctname>`, `<username>`, and `<password>`:
    
        docker run --rm \
      -e SNOWFLAKE_ACCOUNT=<orgname>-<acctname> \
      -e SNOWFLAKE_HOST=<orgname>-<acctname>.snowflakecomputing.com \
      -e SNOWFLAKE_DATABASE=tutorial_db \
      -e SNOWFLAKE_SCHEMA=data_schema \
      -e SNOWFLAKE_ROLE=test_role \
      -e SNOWFLAKE_USER=<username> \
      -e SNOWFLAKE_PASSWORD=<password> \
      -e SNOWFLAKE_WAREHOUSE=tutorial_warehouse \
      my_job:local \
      --query="select current_time() as time,'hello'" \
      --result_table=tutorial_db.data_schema.results
    

Copy

When testing the image locally, note that, in addition to the three arguments
(a query, the warehouse to run the query, and a table to save the result to),
you also provide the connection parameters for the container running locally
to connect to Snowflake.

When you run the container as a service, Snowflake provides these parameters
to the container as the environment variables. For more information, see
[Configure Snowflake Client](../additional-considerations-services-
jobs.html#label-snowpark-containers-connect-to-snowflake-from-container).

The job service executes the query (`select current_time() as time,'hello'`)
and writes result to the table (`tutorial_db.data_schema.results`). If the
table does not exist, it is created. If the table exists, the job service adds
a row.

Sample result of querying the results table:

    
        +----------+----------+
    | TIME     | TEXT     |
    |----------+----------|
    | 10:56:52 | hello    |
    +----------+----------+
    

## What’s next?¶

You can now test [Tutorial 3](advanced/tutorial-3), which shows how service-
to-service communication works.

