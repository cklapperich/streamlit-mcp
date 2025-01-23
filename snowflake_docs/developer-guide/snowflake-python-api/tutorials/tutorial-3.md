# Tutorial 3: Create and manage Snowpark Container Services¶

Feature — Generally Available

Not available in government regions.

## Introduction¶

Snowpark Container Services is a fully managed container offering designed to
facilitate the deployment, management, and scaling of containerized
applications within the Snowflake ecosystem. With this feature, you can run
containerized workloads directly within Snowflake.

In this tutorial, you learn how to use Snowflake Python APIs to manage
components in Snowpark Container Services.

Important

Snowpark Container Services is generally available to Snowflake accounts in
AWS. [Preview support](../../../release-notes/preview-features) is available
to accounts in Azure. For more information, see [Snowpark Container Services –
Available regions](../../snowpark-container-services/overview.html#label-
snowpark-containers-overview-available-regions).

### Prerequisites¶

Before you start this tutorial, you must complete these steps:

  1. Install Docker Desktop.

This tutorial provides instructions that require Docker Desktop. For
installation instructions, see <https://docs.docker.com/get-docker/>.

  2. Follow the [common setup](common-setup) instructions, which include the following steps:

     * Set up your development environment.

     * Install the Snowflake Python APIs package.

     * Configure your Snowflake connection.

     * Import all the modules required for the Python API tutorials.

     * Create an API `Root` object.

Note

If you have already completed the [common setup](common-setup), you can skip
this step and begin the tutorial.

After completing these prerequisites, you are ready to start using the API for
managing Snowpark Container Services.

## Set up your development environment¶

If you were using a notebook for the previous Snowflake Python APIs tutorials,
you switch to a new notebook in this tutorial. The notebook will contain
sample code that runs an NGINX web server using Snowpark Container Services,
all of which runs in Snowflake.

  1. Open a new notebook using your preferred code editor or by running the command `jupyter notebook`.

  2. In the first cell of your notebook, run the following code:
    
        from snowflake.core.database import Database
    from snowflake.core.schema import Schema
    
    database = root.databases.create(Database(name="spcs_python_api_db"), mode="orreplace")
    schema = database.schemas.create(Schema(name="public"), mode="orreplace")
    

Copy

Using the Snowflake connection and `root` object that you created previously
in the [common setup](common-setup), you create a database named
`spcs_python_api_db` and a schema named `public` in that database. You also
save references that represent these newly created objects. Your Snowpark
Container Services components will live in this database and schema.

## Overview of Snowpark Container Services¶

Before you continue with the tutorial, briefly review the main components of
Snowpark Container Services. To run containerized applications in Snowpark
Container Services, you typically work with the following objects:

  * **Image repository** : Provides a storage unit where you can upload your application images in your Snowflake account.

Snowpark Container Services provides an OCIv2-compliant image registry service
that enables OCI clients (such as Docker CLI and SnowSQL) to access an image
registry in your Snowflake account. Using these clients, you can upload your
application images to a repository.

For more information, see [Working with an image registry and
repository](../../snowpark-container-services/working-with-registry-
repository).

  * **Compute pool** : Represents a set of compute resources (virtual machine nodes).

These compute resources are analogous, but not equivalent, to Snowflake
virtual warehouses. The service (in this case, your NGINX service) will run in
the compute pool. Compute-intensive services require high-powered compute
pools with many cores and many GPUs, while less intensive services can run in
smaller compute pools with fewer cores.

For more information, see [Working with compute pools](../../snowpark-
container-services/working-with-compute-pool).

  * **Service** : Provides a way to run an application container.

At a minimum, services require a specification and a compute pool. A
specification contains the information needed to run the application
container, such as the path to a container image and the endpoints that the
services will expose. The specification is written in YAML. The compute pool
is the set of compute resources in which the service will run.

For more information, see [Working with services](../../snowpark-container-
services/working-with-services).

Continue to the next steps to create and set up these objects.

## Create an image repository¶

In this section, first you create an image repository using the Snowflake
Python APIs. Then you fetch an NGINX application image from Docker Hub and
upload the image to the image repository using the Docker CLI.

**Create a repository and get information about the repository**

  1. In the next cell of your notebook, run the following code:
    
        from snowflake.core.image_repository import ImageRepository
    
    my_repo = ImageRepository("MyImageRepository")
    schema.image_repositories.create(my_repo)
    

Copy

In this code example, you create an image repository in the database and
schema you created previously in this tutorial.

  2. To confirm the repository was created successfully by fetching its details and printing its name, run the following code:
    
        my_repo_res = schema.image_repositories["MyImageRepository"]
    my_repo = my_repo_res.fetch()
    print(my_repo.name)
    

Copy

  3. You will need information about the repository (the repository URL and the registry hostname) before you can upload the image.

To get the repository URL, in your next cell, run the following code:

    
        repositories = schema.image_repositories
      for repo_obj in repositories.iter():
        print(repo_obj.repository_url)
    

Copy

     * The `repository_url` attribute in the output provides the URL. For example:
        
                <orgname>-<acctname>.registry.snowflakecomputing.com/spcs_python_api_db/public/myimagerepository
        

     * The hostname in the repository URL is the registry hostname. For example:
        
                <orgname>-<acctname>.registry.snowflakecomputing.com
        

**Fetch the NGINX image and upload it to the repository**

  1. For Docker to upload an image to your repository on your behalf, you must first authenticate Docker with Snowflake.

To authenticate Docker with the Snowflake registry, open a command line
terminal and run the following `docker login` command using the Docker CLI:

    
        docker login <registry_hostname> -u <username>
    

Copy

     * `_registry_hostname_`: Specify the hostname in `repository_url` from the result of the previous step.

     * `_username_`: Specify your Snowflake username. Docker will prompt you for your password.

**Example**

    
        docker login myorg-myacct.registry.snowflakecomputing.com -u admin
    

Copy

  2. Fetch the AMD64 build of the [NGINX image from Docker Hub](https://hub.docker.com/r/amd64/nginx/):
    
        docker pull --platform linux/amd64 amd64/nginx
    

Copy

  3. Tag the `amd64/nginx` image with the Snowflake image repository URL:
    
        docker tag docker.io/amd64/nginx:latest <repository_url>/<image_name>
    

Copy

**Example**

    
        docker tag docker.io/amd64/nginx:latest myorg-myacct.registry.snowflakecomputing.com/spcs_python_api_db/public/myimagerepository/amd64/nginx:latest
    

Copy

A tag is a custom, human-readable identifier that you can optionally use to
identify a specific version or variant of an image.

  4. Upload the image to the repository in your Snowflake account:
    
        docker push <repository_url>/<image_name>
    

Copy

**Example**

    
        docker push myorg-myacct.registry.snowflakecomputing.com/spcs_python_api_db/public/myimagerepository/amd64/nginx:latest
    

Copy

## Create a compute pool¶

To define and create a compute pool, in the next cell of your notebook, run
the following code:

    
    
    new_compute_pool_def = ComputePool(
        name="MyComputePool",
        instance_family="CPU_X64_XS",
        min_nodes=1,
        max_nodes=2,
    )
    
    new_compute_pool = root.compute_pools.create(new_compute_pool_def)
    

Copy

In this cell, you define a compute pool using the `ComputePool` constructor by
providing values for the following attributes:

  * `instance_family`: The instance family identifies the type of machine you want to provision for the nodes in the compute pool.

Each machine type provides a different amount of compute resources to their
compute pools. In this cell, you use the smallest available machine type,
`CPU_X64_XS`. For more information, see [CREATE COMPUTE POOL](../../../sql-
reference/sql/create-compute-pool).

  * `min_nodes`: The minimum number of nodes to launch the compute pool with.

  * `max_nodes`: The maximum number of nodes the compute pool can scale to.

When you create a compute pool, Snowflake launches it with the minimum number
of nodes specified. Snowflake then manages the scaling automatically and
creates new nodes—up to the maximum number specified—when the running nodes
can’t take any additional workload.

Then you create the compute pool by passing the compute pool definition to
`compute_pools.create()`.

## Create a service¶

Using the image repository and compute pool you set up, you can now define and
create your service. A service refers to a collection of containers running in
a compute pool, which are all orchestrated in Snowflake.

  1. To retrieve the repository containing your container image, in the next cell of your notebook, run the following code:
    
        image_repository = schema.image_repositories["MyImageRepository"]
    

Copy

This repository is in your Snowflake account, listed as a stage in the PUBLIC
schema. You need this reference to fetch the container image information in
the next step.

  2. To define and create your service, in your next cell, run the following code:
    
        from textwrap import dedent
    from io import BytesIO
    from snowflake.core.service import Service, ServiceSpecInlineText
    
    specification = dedent(f"""\
        spec:
          containers:
          - name: web-server
            image: {image_repository.fetch().repository_url}/amd64/nginx:latest
          endpoints:
          - name: ui
            port: 80
            public: true
        """)
    
    service_def = Service(
        name="MyService",
        compute_pool="MyComputePool",
        spec=ServiceSpecInlineText(spec_text=specification),
        min_instances=1,
        max_instances=1,
    )
    
    nginx_service = schema.services.create(service_def)
    

Copy

This cell defines the service specification and the service, and then creates
the service for your NGINX web server. The definitions for the specification
and the service have the following properties:

     * `specification` – You define the specification using a Python _formatted string literal_ (f-string). The string is formatted as YAML.

The specification contains the name of the container, a path to the container
image, and the endpoints that the service will expose for public access. In
this example, you define the specification inline, but you can also define a
specification as a reference to a `.yml` file in a stage.

     * `service_def` – You define a service with the `Service` constructor, passing in a name for the service, the compute pool it will run in, a path to the specification, and the total number of instances for the service.

In this cell, you use `ServiceSpecInlineText` to set the value of `spec`
because you define the specification inline as an f-string. You can specify
the service to run multiple instances, but in this example you specify only
one instance of the service to run by setting `min_instances` and
`max_instances` to `1`.

  3. To check the status of the service, in your next cell, run the following code:
    
        from pprint import pprint
    
    pprint(nginx_service.get_service_status(timeout=5))
    

Copy

The output should be similar to this:

    
        {'auto_resume': True,
    'auto_suspend_secs': 3600,
    'instance_family': 'CPU_X64_XS',
    'max_nodes': 1,
    'min_nodes': 1,
    'name': 'MyService'}
    

## Use your service¶

After you create the service, Snowpark Container Services will take a few
minutes to provision the endpoints that are needed to access the service.

  1. To check the status of the endpoints, in the next cell of your notebook, run the following code:
    
        import json, time
    
    while True:
        public_endpoints = nginx_service.fetch().public_endpoints
        try:
            endpoints = json.loads(public_endpoints)
        except json.JSONDecodeError:
            print(public_endpoints)
            time.sleep(15)
        else:
            break
    

Copy

The code example isn’t specific to Snowpark Container Services or the
Snowflake Python APIs – it simply provides a handy way to check whether the
endpoints are ready. Note that you fetch the endpoints by calling
`.fetch().public_endpoints` on your service object.

The output should be similar to this:

    
        Endpoints provisioning in progress... check back in a few minutes
    Endpoints provisioning in progress... check back in a few minutes
    Endpoints provisioning in progress... check back in a few minutes
    

  2. After the endpoints are provisioned, you can open the public endpoints in your browser.

In your next cell, run the following code:

    
        import webbrowser
    
    print(f"Visiting {endpoints['ui']} in your browser. You might need to log in there.")
    webbrowser.open(f"https://{endpoints['ui']}")
    

Copy

The output should be similar to this:

    
        Visiting myorg-myacct.snowflakecomputing.app in your browser. You might need to log in there.
    

If successful, you’ll see the following NGINX success page in your browser
when visiting the endpoint:

![Screenshot of the NGINX web server success page in a
browser](../../../_images/snowflake-python-api-spcs-nginx-success.png)

  3. You can use the Python API to manage your new service.

For example, to suspend the service and then check its status, run the
following code:

    
        from time import sleep
    
    nginx_service.suspend()
    sleep(3)
    print(nginx_service.get_service_status(timeout=5))
    

Copy

  4. To resume the service, run the following code:
    
        nginx_service.resume()
    sleep(3)
    print(nginx_service.get_service_status(timeout=5))
    

Copy

With just a few lines of Python, you were able to run an NGINX web server in
Snowflake using Snowpark Container Services.

## Clean up¶

Snowflake charges for active compute pool nodes in your account. To prevent
unwanted charges, first suspend the service and the compute pool, and then
drop both objects.

  1. To suspend the compute pool and the service, in the next cell of your notebook, run the following code:
    
        new_compute_pool_def.suspend()
    nginx_service.suspend()
    

Copy

  2. To drop the compute pool and the service, run the following code:
    
        new_compute_pool_def.drop()
    nginx_service.drop()
    

Copy

## What’s next?¶

Congratulations! In this tutorial, you learned the fundamentals for managing
components in Snowpark Container Services using the Snowflake Python APIs.

### Summary¶

Along the way, you completed these steps:

  * Create an image repository where you upload your application images.

  * Create a compute pool where your service runs.

  * Create a service to run your application container.

  * Use and manage your service.

  * Clean up your Snowpark Container Services resource objects by suspending and dropping them.

### Additional resources¶

For more examples of using the API to manage other types of objects in
Snowflake, see the following developer guides:

Guide | Description  
---|---  
[Managing Snowflake databases, schemas, tables, and views with Python](../snowflake-python-managing-databases) | Use the API to create and manage databases, schemas, and tables.  
[Managing Snowflake users, roles, and grants with Python](../snowflake-python-managing-user-roles) | Use the API to create and manage users, roles, and grants.  
[Managing data loading and unloading resources with Python](../snowflake-python-managing-data-loading) | Use the API to create and manage data loading and unloading resources, including external volumes, pipes, and stages.  
[Managing Snowflake tasks and task graphs with Python](../snowflake-python-managing-tasks) | Use the API to create, execute, and manage tasks and task graphs.

