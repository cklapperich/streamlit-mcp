# Tutorial: Service-to-Service Communications with Snowpark Container
Services¶

[![Snowflake logo in black \(no text\)](../../../../_images/logo-snowflake-
black.png)](../../../../_images/logo-snowflake-black.png) Feature — Generally
Available

Available to accounts in [AWS and Microsoft Azure commercial
regions](../../../../user-guide/intro-regions.html#label-na-general-regions),
with some exceptions. For more information, see [Available
regions](../../overview.html#label-snowpark-containers-overview-available-
regions).

## Introduction¶

In this tutorial, you create a Snowpark Container Services job service that
communicates with the Echo service you created in [Tutorial 1](../tutorial-1).
When the job service runs, it sends a POST request to the Echo service URL
(that you provide in the service specification) with a “Hello” string in the
request body. The Echo service returns a response with the “Bob said Hello”
string in the response body. You access the job service container logs to
verify that the communications succeeded.

There are two parts to this tutorial:

  * **Part 1: Create and test a job service.** You download code provided for this tutorial and follow step-by-step instructions:

    1. Download the job service code for this tutorial.

    2. Build a Docker image for Snowpark Container Services, and upload the image to a repository in your account.

    3. Stage the specification file, which gives Snowflake the container configuration information. In addition to the name of the image to use to start a container, the specification sets the environment variable (`SERVICE_URL`) to the Echo service URL. The application code reads this environment variable to send requests to the Echo service.

    4. Execute the job service. Using the EXECUTE JOB SERVICE command, you can execute the job service by providing the specification file and the compute pool where Snowflake can run the container. And finally, access logs from the job service container to verify that the communication between the job service and service succeeded.

  * **Part 2: Understand the job service code**. This section provides an overview of the service code and highlights how different components collaborate.

## Prerequisites¶

Complete [Tutorial 1](../tutorial-1). To verify the service is running,
execute the [DESCRIBE SERVICE](../../../../sql-reference/sql/desc-service)
command.

    
    
    DESC SERVICE echo_service;
    

Copy

Verify the `status` column shows the service status as RUNNING; if the status
is PENDING, it indicates the service is still starting. To investigate why the
service is not RUNNING, execute the [SHOW SERVICE CONTAINERS IN
SERVICE](../../../../sql-reference/sql/show-service-containers-in-service)
command and review the `status` of individual containers:

    
    
    SHOW SERVICE CONTAINERS IN SERVICE echo_service;
    

Copy

You need the service running before you can proceed.

## 1: Download the service code¶

Code (a Python application) is provided to create a job service.

  1. Download [`SnowparkContainerServices-Tutorials.zip`](../../../../_downloads/c3a8f6109048f2ecca7734c7fd3b0b3b/SnowparkContainerServices-Tutorials.zip).

  2. Unzip the content, which includes one directory for each tutorial. The `Tutorial-3` directory has the following files:

     * `service_to_service.py`

     * `Dockerfile`

     * `service_to_service_spec.yaml`

## 2: Build and upload an image¶

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
        

     * The host name in the repository URL is registry host name. An example is shown:
        
                <orgname>-<acctname>.registry.snowflakecomputing.com
        

**Build image and upload it to the repository**

  1. Open a terminal window, and change to the directory containing the files you unzipped.

  2. To build a Docker image, execute the following `docker build` command using the Docker CLI. Note the command specifies the current working directory (.) as the `PATH` for files to use for building the image.
    
        docker build --rm --platform linux/amd64 -t <repository_url>/<image_name> .
    

Copy

     * For `_image_name_`, use `service_to_service:latest`.

**Example**

    
        docker build --rm --platform linux/amd64 -t myorg-myacct.registry.snowflakecomputing.com/tutorial_db/data_schema/tutorial_repository/service_to_service:latest .
    

Copy

  3. Upload the image to the repository in your Snowflake account. In order for Docker to upload an image on your behalf to your repository, you must first [authenticate Docker with the registry](../../working-with-registry-repository.html#label-registry-and-repository-authentication).

    1. To authenticate Docker with the Snowflake registry, execute the following command.
        
                docker login <registry_hostname> -u <username>
        

Copy

       * For `_username_`, specify your Snowflake username. Docker will prompt you for your password.

    2. To upload the image execute the following command:
        
                docker push <repository_url>/<image_name>
        

Copy

**Example**

        
                docker push myorg-myacct.registry.snowflakecomputing.com/tutorial_db/data_schema/tutorial_repository/service_to_service:latest
        

Copy

## 3: Stage the specification file¶

  * To upload your service specification file (`service_to_service_spec.yaml`) to the stage, use one of the following options:

    * **The Snowsight web interface**. For instructions, see [Choosing an internal stage for local files](../../../../user-guide/data-load-local-file-system-create-stage).

    * **The SnowSQL CLI.** Execute the following [PUT](../../../../sql-reference/sql/put) command:
        
                PUT file://<absolute-path-to-spec.yaml> @tutorial_stage
          AUTO_COMPRESS=FALSE
          OVERWRITE=TRUE;
        

Copy

> The command sets OVERWRITE=TRUE so that you can upload the file again, if
> needed (for example, if you fixed an error in your specification file). If
> the PUT command is executed successfully, information about the uploaded
> file is printed out.

## 4: Execute the job service¶

Now you are ready to test the Snowflake job service you created. When the job
service is executed, Snowflake collects anything that your code in the
container outputs to standard output or standard error as logs. You can use
the `SYSTEM$GET_SERVICE_LOGS` system function to access the logs. For more
information, see [Snowpark Container Services: Additional considerations for
services](../../additional-considerations-services-jobs).

  1. To start a job service, run the EXECUTE JOB SERVICE command:
    
        EXECUTE JOB SERVICE
      IN COMPUTE POOL tutorial_compute_pool
      NAME=tutorial_db.data_schema.tutorial3_job_service
      FROM @tutorial_stage
      SPEC='service_to_service_spec.yaml';
    

Copy

Note the following:

     * FROM and SPEC provide the stage name and the name of the service specification file.

     * COMPUTE_POOL provides the compute resources where Snowflake executes the job service.

Snowflake runs the container identified in the specification file. The
container reads the `SERVICE_URL` environment variable value (`http://echo-
service:8000/echo`) and sends a request to the Echo service at port 8000 at
`/echo` HTTP path.

Snowflake starts the job service and returns the following output:

    
        +------------------------------------------------------------------------+
    | status                                                                 |
    |------------------------------------------------------------------------|
    | Job TUTORIAL3_JOB_SERVICE completed successfully with status: DONE     |
    +------------------------------------------------------------------------+
    

Note that the response includes the job service name.

  2. (optional) After the job service completes, you can get more information about the job service that executed. This is useful for debugging job service failure. To get the job service status, execute [SHOW SERVICE CONTAINERS IN SERVICE](../../../../sql-reference/sql/show-service-containers-in-service).
    
        SHOW SERVICE CONTAINERS IN SERVICE tutorial_3_job_service;
    

Copy

Sample output:

    
        +---------------+-------------+------------------------+-------------+----------------+--------+------------------------+----------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+---------------+------------+
    | database_name | schema_name | service_name           | instance_id | container_name | status | message                | image_name                                                                                                                             | image_digest                                                            | restart_count | start_time |
    |---------------+-------------+------------------------+-------------+----------------+--------+------------------------+----------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+---------------+------------|
    | TUTORIAL_DB   | DATA_SCHEMA | TUTORIAL_3_JOB_SERVICE | 0           | main           | DONE   | Completed successfully | myorg-myacct.registry.snowflakecomputing.com/tutorial_db/data_schema/tutorial_repository/service_to_service:latest | sha256:aa3fa2e5c1552d16904a5bbc97d400316ebb4a608bb110467410485491d9d8d0 |             0 |            |
    +---------------+-------------+------------------------+-------------+----------------+--------+------------------------+----------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------------------------------+---------------+------------+
    

  3. To read the job service logs call [SYSTEM$GET_SERVICE_LOGS](../../../../sql-reference/functions/system_get_service_logs):
    
        CALL SYSTEM$GET_SERVICE_LOGS('tutorial_3_job_service', 0, 'main');
    

Copy

`main` is the name of the container you retrieve the log from. You set this
container name for the container in the service specification file.

Sample log:

    
        +--------------------------------------------------------------------------------------------------------------------------+
    | SYSTEM$GET_JOB_LOGS                                                                                                      |
    |--------------------------------------------------------------------------------------------------------------------------|
    | service-to-service [2023-04-29 21:52:09,208] [INFO] Calling http://echo-service:8000/echo with input Hello               |
    | service-to-service [2023-04-29 21:52:09,212] [INFO] Received response from http://echo-service:8000/echo: Bob said Hello |
    +--------------------------------------------------------------------------------------------------------------------------+
    

## 5: Clean up¶

Snowflake charges for the Compute Pool nodes that are active for your account.
(See [Working With Compute Pools](../../working-with-compute-pool)). To
prevent unwanted charges, first stop all services that are currently running
on a compute pool. Then, either suspend the compute pool (if you intend to use
it again later) or drop it.

  1. Stop all services and job services on the compute pool.
    
        ALTER COMPUTE POOL tutorial_compute_pool STOP ALL;
    

Copy

  2. Delete the compute pool.
    
        DROP COMPUTE POOL tutorial_compute_pool;
    

Copy

You can also clean up the image registry (remove all images) and the internal
stage (remove specifications).

    
    
    DROP IMAGE REPOSITORY tutorial_repository;
    DROP STAGE tutorial_stage;
    

Copy

## 6: Reviewing the job service code¶

This section covers the following topics:

  * Examining the files provided: Review various code files that implement the job service.

  * Building and testing an image locally. Learn how to locally test the Docker image before uploading it to a repository in your Snowflake account.

### Examining the files provided¶

The zip file you downloaded includes the following files:

  * `service_to_service.py`

  * `Dockerfile`

  * `service_to_service_spec.yaml`

This section provides an overview of how the code implements job service.

#### service_to_service.py file¶

    
    
    import json
    import logging
    import os
    import requests
    import sys
    
    SERVICE_URL = os.getenv('SERVICE_URL', 'http://localhost:8080/echo')
    ECHO_TEXT = 'Hello'
    
    def get_logger(logger_name):
      logger = logging.getLogger(logger_name)
      logger.setLevel(logging.DEBUG)
      handler = logging.StreamHandler(sys.stdout)
      handler.setLevel(logging.DEBUG)
      handler.setFormatter(
        logging.Formatter(
          '%(name)s [%(asctime)s] [%(levelname)s] %(message)s'))
      logger.addHandler(handler)
      return logger
    
    logger = get_logger('service-to-service')
    
    def call_service(service_url, echo_input):
      logger.info(f'Calling {service_url} with input {echo_input}')
    
      row_to_send = {"data": [[0, echo_input]]}
      response = requests.post(url=service_url,
                               data=json.dumps(row_to_send),
                               headers={"Content-Type": "application/json"})
    
      message = response.json()
      if message is None or not message["data"]:
        logger.error('Received empty response from service ' + service_url)
    
      response_row = message["data"][0]
      if len(response_row) != 2:
        logger.error('Unexpected response format: ' + response_row)
    
      echo_reponse = response_row[1]
      logger.info(f'Received response from {service_url}: ' + echo_reponse)
    
    if __name__ == '__main__':
      call_service(SERVICE_URL, ECHO_TEXT)
    

Copy

When the job service runs:

  1. Snowflake uses the value provided in the specification file to set the SERVICE_URL environment variable in the container.

  2. The code reads the environment variable.
    
        SERVICE_URL = os.getenv('SERVICE_URL', 'http://localhost:8080/echo').
    

Copy

  3. The `call_service()` function uses the `SERVICE_URL` to communicate with the Echo service.

#### Dockerfile¶

This file contains all the commands to build an image using Docker.

    
    
    ARG BASE_IMAGE=python:3.10-slim-buster
    FROM $BASE_IMAGE
    COPY service_to_service.py ./
    RUN pip install --upgrade pip && \
      pip install requests
    CMD ["python3", "service_to_service.py"]
    

Copy

#### service_to_service_spec.yaml file (service specification)¶

Snowflake uses information you provide in this specification to configure and
run your service.

    
    
    spec:
    container:
       - name: main
          image: /tutorial_db/data_schema/tutorial_repository/service_to_service:latest
          env:
          SERVICE_URL: "http://echo-service:8000/echo"
    

Copy

This specification provides information to Snowflake for configuring and
running your job. To communicate with the Echo service, the job needs the
following:

  * DNS name of the Echo service to send requests to.

  * HTTP port on which the Echo service is listening.

  * HTTP path where the Echo service expects the request to be sent.

To get this information:

  1. To get the DNS name of the Echo service ([Tutorial 1](../tutorial-1)), execute the [DESCRIBE SERVICE](../../../../sql-reference/sql/desc-service) SQL command:
    
        DESCRIBE SERVICE echo_service;
    

Copy

Resulting DNS name for the Echo service:

    
        echo-service.fsvv.svc.spcs.internal
    

Copy

Note that, in this tutorial, you create the job service in the same database
schema (`data-schema`) where the Echo service ([Tutorial 1](../tutorial-1)) is
created. Therefore, you only need the “echo-service” portion of the preceding
DNS name for constructing the `SERVICE_URL`.

  2. Get the port number (8000) where Echo service is listening from the Echo service specification file ([Tutorial 1](../tutorial-1)). You can also use the [SHOW ENDPOINTS](../../../../sql-reference/sql/show-endpoints) SQL command.

You then create the preceding specification file
(`service_to_service_spec.yaml`). In addition to the required
`containers.name` and `containers.image` fields, you also include the optional
`containers.env` field to specify environment variables used by the service.

### Building and testing an image locally¶

You can test the Docker image locally before uploading it to a repository in
your Snowflake account. In local testing, your container runs standalone (it
is not a job service that Snowflake executes).

Note

The Python code provided for this tutorial uses the `requests` library to send
requests to another Snowpark Containers service. If you don’t have this
library installed, run pip (for example, `pip3 install requests`).

Use the following steps to test the Tutorial 3 Docker image:

  1. You need the Echo service running ([Tutorial 1](../tutorial-1)). To start the Tutorial 1 Echo service, in a terminal window, execute the following Python command:
    
        SERVER_PORT=8000 python3 echo_service.py
    

Copy

  2. Open another terminal window and, run the Python code provided for this tutorial:
    
        SERVICE_URL=http://localhost:8000/echo python3 service_to_service.py
    

Copy

Note that the `SERVICE_URL` is an environment variable. For local testing, you
need to explicitly set this variable. This URL matches the port and HTTP path
explicitly specified when you started the Echo service.

When the job is executed, it sends a POST request to the Echo service
listening on port 8000 with the “Hello” string in the request body. The Echo
service echoes the input back and returns a response - “I said Hello”.

Sample response:

    
        service-to-service
      [2023-04-23 22:30:41,278]
      [INFO] Calling http://localhost:8000/echo with input Hello
    
    
    service-to-service
      [2023-04-23 22:30:41,287]
      [INFO] Received response from http://localhost:8000/echo: I said Hello
    

Review the log to verify that the service-to-service communication succeeded.

## What’s next?¶

[Create a service with a block storage volume mounted](tutorial-4-block-
storage)

