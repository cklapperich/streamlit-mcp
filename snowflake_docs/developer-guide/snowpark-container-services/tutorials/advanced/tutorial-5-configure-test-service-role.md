# Configure and test service endpoint privileges¶

[![Snowflake logo in black \(no text\)](../../../../_images/logo-snowflake-
black.png)](../../../../_images/logo-snowflake-black.png) Feature — Generally
Available

Available to accounts in [AWS and Microsoft Azure commercial
regions](../../../../user-guide/intro-regions.html#label-na-general-regions),
with some exceptions. For more information, see [Available
regions](../../overview.html#label-snowpark-containers-overview-available-
regions).

## Introduction¶

In Tutorial 1, you use the same role to create and test a service. The role
that creates the service is the service’s owner role, so you’re able to
communicate with the service using that role.

In this tutorial, you explore using a different role to communicate with the
service.

You grant this role the USAGE privilege using a [service role](../../working-
with-services.html#label-snowpark-containers-service-endpoint-access) that you
define in the service specification.

In this tutorial, you modify the [Tutorial 1](../tutorial-1) as follows:

  1. Create a new role that you will use to communicate with the service.

  2. Modify the service specification as follows:

     * Define two endpoints, instead of just one endpoint. Note that the second endpoint is added only to demonstrate how endpoint permissions work.

     * Define a service role that is allowed to access only one of the two endpoints.

  3. Grant the service role to the new role you created to allow access to one of the service endpoints.

  4. Use the new role to communicate with the service endpoint.

## Prepare¶

Follow [Common Setup](../common-setup) with the following modifications:

  1. Complete the common setup steps.

  2. Using the ACCOUNTADMIN role, execute the following script to create another role (`service_function_user_role`), replacing `user_name` with the name of your Snowflake user. After creating the echo service, you use this role to communicate with the service.
    
        USE ROLE ACCOUNTADMIN;
    CREATE ROLE service_function_user_role;
    GRANT ROLE service_function_user_role TO USER <user-name>;
    GRANT USAGE ON WAREHOUSE tutorial_warehouse TO ROLE service_function_user_role;
    

Copy

  3. Follow [Tutorial 1](../tutorial-1), steps 1 and 2, to build and upload an image to a repository in your account. Do not proceed with step 3 because you will create the service as part of this tutorial.

## Create a service¶

  1. To ensure you’re in the right context for the SQL statements in this step, execute the following:
    
        USE ROLE test_role;
    USE DATABASE tutorial_db;
    USE SCHEMA data_schema;
    USE WAREHOUSE tutorial_warehouse;
    

Copy

  2. To create the service, execute the following command using `test_role` (the service’s owner role).
    
        CREATE SERVICE echo_service
      IN COMPUTE POOL tutorial_compute_pool
      FROM SPECIFICATION $$
        spec:
          containers:
          - name: echo
            image: /tutorial_db/data_schema/tutorial_repository/my_echo_service_image:latest
            env:
              SERVER_PORT: 8000
              CHARACTER_NAME: Bob
            readinessProbe:
              port: 8000
              path: /healthcheck
          endpoints:
          - name: echoendpoint
            port: 8000
            public: true
          - name: echoendpoint2
            port: 8002
            public: true
        serviceRoles:
        - name: echoendpoint_role
          endpoints:
          - echoendpoint
          $$;
    

Copy

Per the inline specification, the `echo_service` exposes two public endpoints
but the service role (`echoendpoint_role`) grants USAGE privilege only on one
of the endpoints.

  3. Verify the service is running.
    
        SHOW SERVICES;
    SHOW SERVICE CONTAINERS IN SERVICE echo_service;
    DESCRIBE SERVICE echo_service;
    

Copy

  4. Using `test_role` (the service’s owner role), grant the service role defined in the specification to the new role (`service_function_user_role`) you created as part of the common setup. Also grant USAGE privileges on the database and the schema.
    
        USE ROLE test_role;
    USE DATABASE tutorial_db;
    USE SCHEMA data_schema;
    
    GRANT USAGE ON DATABASE tutorial_db TO ROLE service_function_user_role;
    GRANT USAGE ON SCHEMA data_schema TO ROLE service_function_user_role;
    GRANT SERVICE ROLE echo_service!echoendpoint_Role TO ROLE service_function_user_role;
    

Copy

This service role grants the `service_function_user_role` USAGE privilege on
the `echoendpoint` endpoint.

To demonstrate that the service role name is case in-sensitive, the example
uses the `echoendpoint_Role` role name.

## Use the service¶

Create a service function to communicate with the service. You create a
service function using the `service_function_user_role` (not the service’s
owner role) and use the service.

  1. Create a service function.
    
        USE ROLE service_function_user_role;
    CREATE OR REPLACE FUNCTION my_echo_udf_try1 (InputText VARCHAR)
      RETURNS varchar
      SERVICE=echo_service
      ENDPOINT=echoendpoint
      AS '/echo';
    

Copy

  2. Try creating another service function that refers to the `echoservice2` endpoint for which the role has no access privilege. Therefore, the command should _fail_.
    
        CREATE OR REPLACE FUNCTION my_echo_udf_try2 (InputText varchar)
      RETURNS varchar
      SERVICE=echo_service
      ENDPOINT=echoendpoint2
      AS '/echo';
    

Copy

  3. Use the service function.
    
        SELECT my_echo_udf_try1('Hello');
    

Copy

## Clean up¶

To remove the resources you created, follow the steps in [Tutorial
1](../tutorial-1) steps to clean up other resources created in Tutorial 1.

## What’s next?¶

Now that you’ve completed this tutorial, you can return to [Working with
Services](../../working-with-services) to explore other topics.

