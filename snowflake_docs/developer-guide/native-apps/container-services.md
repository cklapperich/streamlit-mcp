# Add services to an app¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) Feature — Generally
Available

The Snowflake Native App Framework is generally available on supported cloud
platforms. For additional information, see [Support for private connectivity,
VPS, and government regions](limitations.html#label-native-apps-supported-
clouds).

The topic describes how to configure and use services in a Snowflake Native
App with Snowpark Container Services. For information on using a job service
in an app, see [Add job services to an app](container-services-job).

## Privileges required to create a service in the consumer account¶

In order for an app to create a service in the consumer account, the consumer
must first grant the following privileges:

  * CREATE COMPUTE POOL

This privileges is required for all services. One or more compute pools are
required to create a service in the consumer account.

  * BIND SERVICE ENDPOINT

This privilege is required for any service that exposes endpoints. If a
service needs to make connections to URLs outside of Snowflake, this privilege
is required for the app to create the required external access integration.

## Considerations when creating services within an app¶

The following considerations apply when creating a service within a Snowflake
Native App with Snowpark Container Services:

  * References to warehouses. See Best practices when using services within an app for information on using in a Snowflake Native App with Snowpark Container Services.

  * Quoted names for a service within an app are not supported.

  * Services cannot not be created in a versioned schema.

  * Services may not be created outside of the application using a container image created within the app.

## Best practices when using services within an app¶

The following are best practices and considerations when using services within
a Snowflake Native App with Snowpark Container Services:

  * Create a Streamlit app or stored procedures that allows consumers to interact with a service.

In some situations, a consumer may need to create, start, stop, restart, and
manage the services provided by the app.

  * Use a single stored procedure to verify that the consumer has granted all the required privileges.

A service may require that the consumer grants multiple privileges to the app.
For example, a service may require the CREATE COMPUTE POOL, CREATE WAREHOUSE,
BIND SERVICE ENDPOINT and other privileges. An app may also require reference
to existing objects in the consumer account.

In this context, Snowflake recommends using a single stored procedure to
verify that all prerequisites have been met. After all prerequisites are
verified, this stored procedure would then create the service.

  * If a service requires a warehouse to execute queries, the app should create the warehouse directly in the consumer account. This requires that the consumer grant the CREATE WAREHOUSE global privilege to the app. See [Request global privileges from consumers](requesting-privs) for more information.

  * When creating a service using a specification template, store the arguments provided by the consumer inside your application instance. This allows them to be passed as arguments when upgrading a service.

## Create a service in an app¶

To create a service in an app, use the [CREATE SERVICE](../../sql-
reference/sql/create-service) command in the setup script. Providers should
always consider calling this command from within a stored procedure instead of
running it directly.

Within an app with containers, services can be created using specification
file or by using a [specification template](../snowpark-container-
services/working-with-services.html#label-spcs-working-with-services-using-
specification-templates).

### Create a service from a specification file¶

To create a service a service from a specification file, use the [CREATE
SERVICE](../../sql-reference/sql/create-service) command and include a
reference to the service specification file:

    
    
    CREATE SERVICE IF NOT EXISTS app_service
      IN COMPUTE POOL app_compute_pool
      FROM SPECIFICATION_FILE = '/containers/service1_spec.yaml';
    

Copy

This example shows how to create the service using the FROM SPECIFICATION_FILE
clause which uses a relative path to the file. The FROM SPECIFICATION_FILE
clause points to the service specification file that is specific to a version
of the app. This path is relative to the app root directory.

However, you can also use a specification file on a stage. See [CREATE
SERVICE](../../sql-reference/sql/create-service) for more information.

### Create a service with a specification template¶

To create a service using a [specification template](../snowpark-container-
services/working-with-services.html#label-spcs-working-with-services-using-
specification-templates), use the FROM SPECIFICATION_TEMPLATE_FILE clause of
the [CREATE SERVICE](../../sql-reference/sql/create-service) command as shown
in the following example:

    
    
    CREATE SERVICE IF NOT EXISTS app_service
      IN COMPUTE POOL app_compute_pool
      FROM SPECIFICATION_TEMPLATE_FILE = '/containers/service1_spec.yaml';
    

Copy

See [specification template](../snowpark-container-services/working-with-
services.html#label-spcs-working-with-services-using-specification-templates)
for more information.

## Add the CREATE SERVICE command to a stored procedure¶

A Snowflake Native Apps with Snowpark Container Services supports multiple
ways of creating a service within a stored procedure.

  * Create a service by using the grant_callback property

  * Create a service based on a reference definition

  * Create a service using a stored procedure

A provider can use any combination of these methods to create services in the
consumer account.

### Create a service by using the `grant_callback` property¶

`grant_callback` is a property in the manifest file that allows providers to
specify a callback function. The callback function is a stored procedure that
can create compute pools, services and perform other setup tasks required by
the application.

Note

Using the `grant_callback` property to specify the callback function is only
supported by Snowflake Native Apps with Snowpark Container Services.

The advantage of specifying a callback function with `grant_callback` is that
the stored procedure is not called until the consumer grants the required
privileges to the app. This ensures that the app has the privileges required
to create services and other objects in the consumer account.

To use `grant_callback` add it to the `configuration` section of the
`manifest.yml` file:

    
    
    configuration:
      log_level: INFO
      trace_level: ALWAYS
      grant_callback: core.grant_callback
    

Copy

Then, in the setup script, define a call back function as shown in the
following example:

    
    
     CREATE SCHEMA core;
     CREATE APPLICATION ROLE app_public;
    
     CREATE OR REPLACE PROCEDURE core.grant_callback(privileges array)
     RETURNS STRING
     AS $$
     BEGIN
       IF (ARRAY_CONTAINS('CREATE COMPUTE POOL'::VARIANT, privileges)) THEN
          CREATE COMPUTE POOL IF NOT EXISTS app_compute_pool
              MIN_NODES = 1
              MAX_NODES = 3
              INSTANCE_FAMILY = GPU_NV_M;
       END IF;
       IF (ARRAY_CONTAINS('BIND SERVICE ENDPOINT'::VARIANT, privileges)) THEN
          CREATE SERVICE IF NOT EXISTS core.app_service
           IN COMPUTE POOL my_compute_pool
           FROM SPECIFICATION_FILE = '/containers/service1_spec.yaml';
       END IF;
       RETURN 'DONE';
     END;
     $$;
    
    GRANT USAGE ON PROCEDURE core.grant_callback(array) TO APPLICATION ROLE app_public;
    

Copy

This example creates a `grant_callback` procedure that does the following:

  * Tests whether the consumer has granted the CREATE COMPUTE POOL privilege to the app. If the consumer has granted this privilege, the `grant_callback` procedure creates the compute pool.

  * Tests whether the consumer has granted the BIND SERVICE ENDPOINT privilege to the app. If the consumer has granted this privilege, the `grant_callback` procedure creates the service.

This example shows a pattern for creating services and a compute pool in an
app with containers. In this example, the app first tests whether the consumer
has granted the required privileges and then creates the service or compute
pool.

### Create a service based on a reference definition¶

An app can create services using a reference definition by using the
`register_callback` property in the `manifest.yml` file. This property
specifies a stored procedure used to bind an object in the consumer account to
the reference definition.

For more information on using references in an app, see [Request references
and object-level privileges from consumers](requesting-refs)

An app can use the `register_callback` of the reference to create a service
after all the required references are bound. If a service is created before
all the references to an external access integrations or secret is allowed,
the service creation fails.

### Create a service using a stored procedure¶

An app can create a service directly within a stored procedure. As with other
stored procedures, providers can define them in the application setup script.
This stored procedure would use the [CREATE SERVICE](../../sql-
reference/sql/create-service) command to create the service, then grant the
necessary privileges on the stored procedure to an application role.

The consumer would call this stored procedure to create the service in their
account after they have given the app the required privileges and references.

## Determine the status of a service¶

To determine the status of a service, an app can call the
[SYSTEM$GET_SERVICE_STATUS — Deprecated](../../sql-
reference/functions/system_get_service_status) system function from the setup
script.

This system function returns a JSON object for each container in each service
instance.

