# Snowpark Container Services¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) Feature — Generally
Available

Available to accounts in [AWS and Microsoft Azure commercial
regions](../../user-guide/intro-regions.html#label-na-general-regions), with
some exceptions. For more information, see Available regions.

## About Snowpark Container Services¶

Snowpark Container Services is a fully managed container offering designed to
facilitate the deployment, management, and scaling of containerized
applications within the Snowflake ecosystem. This service enables users to run
containerized workloads directly within Snowflake, ensuring that data doesn’t
need to be moved out of the Snowflake environment for processing. Unlike
traditional container orchestration platforms like Docker or Kubernetes,
Snowpark Container Services offers an OCI runtime execution environment
specifically optimized for Snowflake. This integration allows for the seamless
execution of OCI images, leveraging Snowflake’s robust data platform.

As a fully managed service, Snowpark Container Services streamlines
operational tasks. It handles the intricacies of container management,
including security and configuration, in line with best practices. This
ensures that users can focus on developing and deploying their applications
without the overhead of managing the underlying infrastructure.

Snowpark Container Services is fully integrated with Snowflake. For example,
your application can easily perform these tasks:

  * Connect to Snowflake and run SQL in a Snowflake virtual warehouse.

  * Access data files in a Snowflake stage.

  * Process data sent from SQL queries.

Snowpark Container Services is also integrated with third-party tools. It lets
you use third-party clients (such as Docker) to easily upload your application
images to Snowflake. Seamless integration makes it easier for teams to focus
on building data applications.

You can run and scale your application container workloads across Snowflake
regions and cloud platforms without the complexity of managing a control plane
or worker nodes, and you have quick and easy access to your Snowflake data.

Snowpark Container Services unlocks a wide array of new functionality,
including these features:

  * Create long-running services.

  * Use GPUs to boost the speed and processing capabilities of a system.

  * Write your application code in any language (for example, C++).

  * Use any libraries with your application.

All of this comes with Snowflake platform benefits, most notably ease-of-use,
security, and governance features. And you now have a scalable, flexible
compute layer next to the powerful Snowflake data layer without needing to
move data off the platform.

## How does it work?¶

To run containerized applications in Snowpark Container Services, in addition
to working with the basic Snowflake objects, such as databases and warehouses,
you work with these objects: [image repository](working-with-registry-
repository), [compute pool](working-with-compute-pool), and [service](working-
with-services).

Snowflake offers _image registry_ , an
[OCIv2](https://github.com/opencontainers/distribution-spec/blob/main/spec.md)
compliant service, for storing your images. This enables OCI clients (such as
Docker CLI and SnowSQL) to access an image registry in your Snowflake account.
Using these clients, you can upload your application images to a _repository_
(a storage unit) in your Snowflake account. For more information, see [Working
with an image registry and repository](working-with-registry-repository).

After you upload your application image to a repository, you can run your
application by creating a long-running _service_ or executing a _job service_.

  * A service is long-running and, as with a web service, you explicitly stop it when it is no longer needed. If a service container exits (for whatever reason), Snowflake restarts that container. To create a service, such as a full stack web application, use the [CREATE SERVICE](../../sql-reference/sql/create-service) command.

  * A job service has a finite lifespan, similar to a stored procedure. When all containers exit, the job service is done. Snowflake does not restart any job service containers. To start a job service, such as training a machine learning model with GPUs, use the [EXECUTE JOB SERVICE](../../sql-reference/sql/execute-job-service) command.

For more information, see [Working with services](working-with-services).

Your services (including job services) run in a _compute pool_ , which is a
collection of one or more virtual machine (VM) nodes. You first create a
compute pool using the [CREATE COMPUTE POOL](../../sql-reference/sql/create-
compute-pool) command, and then specify the compute pool when you create a
service or a job service. The required information to create a compute pool
includes the machine type, the minimum number of nodes to launch the compute
pool with, and the maximum number of nodes the compute pool can scale to. Some
of the supported machine types provide GPU. For more information, see [Working
with compute pools](working-with-compute-pool).

You can use [service functions](working-with-services.html#label-snowpark-
containers-service-communicating-service-function) to communicate with a
service from a SQL query. You can configure public endpoints to allow access
with the service from outside Snowflake, with Snowflake-managed access
control. Snowpark Container Services also supports service-to-service
communications. For more information, see [Using a service](working-with-
services.html#label-snowpark-containers-service-communicating).

Note

The Snowpark Container Services documentation primarily uses SQL commands and
functions in explanations of concepts and in examples. Snowflake also provides
other interfaces, including [Python APIs](../snowflake-python-api/snowflake-
python-overview), [REST APIs](../snowflake-rest-api/snowflake-rest-api), and
the [Snowflake CLI](../snowflake-cli/index) command-line tool for most
operations.

## Available regions¶

Snowpark Container Services is in all [regions](../../user-guide/intro-
regions) except the following:

  * Snowpark Container Services is not available for Google Cloud Platform (GCP).

  * Snowpark Container Services is not available for Government regions in AWS or Azure.

## What’s next?¶

If you’re new to Snowpark Container Services, we suggest that you first
explore the tutorials and then continue with other topics to learn more and
create your own containerized applications. The following topics provide more
information:

  * **Tutorials:** These [introductory tutorials](overview-tutorials) provide step-by-step instructions for you to explore Snowpark Container Services. After initial exploration, you can continue with [advanced tutorials](overview-advanced-tutorials).

  * **Service specification reference:** This reference explains the [YAML syntax](specification-reference) to create a service specification.

  * **Working with services and job services:** These topics provide details about the Snowpark Container Services components that you use in developing services and job services:

    * [Working with an image registry and repository](working-with-registry-repository)

    * [Working with compute pools](working-with-compute-pool)

    * [Working with services](working-with-services)

    * [Troubleshooting](troubleshooting)

  * **Reference:** Snowpark Container Services provides the following SQL commands and system functions:

    * For SQL commands, see [Snowpark Container Services commands](../../sql-reference/commands-snowpark-container-services) and [CREATE FUNCTION (Snowpark Container Services)](../../sql-reference/sql/create-function-spcs)

    * For SQL functions: [SYSTEM$GET_SERVICE_LOGS](../../sql-reference/functions/system_get_service_logs).

  * **Billing:** This topic explains costs associated with using Snowpark Container Services:

    * [Snowpark Container Services costs](accounts-orgs-usage-views)

