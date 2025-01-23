# Common Setup for Snowpark Container Services Tutorials¶

[![Snowflake logo in black \(no text\)](../../../_images/logo-snowflake-
black.png)](../../../_images/logo-snowflake-black.png) Feature — Generally
Available

Available to accounts in [AWS and Microsoft Azure commercial
regions](../../../user-guide/intro-regions.html#label-na-general-regions),
with some exceptions. For more information, see [Available
regions](../overview.html#label-snowpark-containers-overview-available-
regions).

## Introduction¶

This topic provides instructions for the common setup required for all
Snowpark Container Services tutorials provided in this documentation.

## Configure prerequisites¶

Review the following prerequisites to ensure you can complete the tutorials:

  * **A Snowflake account:** Note that trial accounts are not supported.

  * **SnowSQL, the command-line client for executing SQL commands (optional):** You can use any Snowflake client that supports executing SQL commands and uploading files to a Snowflake stage. The tutorials are tested using the SnowSQL and the [Snowsight](../../../user-guide/ui-snowsight) web interface. For instructions to install this command-line client, see [Installing SnowSQL](../../../user-guide/snowsql-install-config).

  * **Docker Desktop:** These tutorials provide instructions for using Docker Desktop. For installation instructions, see <https://docs.docker.com/get-docker/>. Note that you can use any OCI-compliant clients to create images, such as Docker, Podman, or Nerdctl.

## Create Snowflake objects¶

Execute the SQL provided using either the SnowSQL or the Snowsight.

  1. Login to Snowflake as a user with the ACCOUNTADMIN role.

  2. Using the ACCOUNTADMIN role, execute the following script, replacing `_user_name_` with the name of your Snowflake user who will test the tutorials. For these tutorials, you might choose the same user who executes this script or another user in your Snowflake account. The script does the following:

     * Creates a role (`test_role`) and other Snowflake objects. To create the role and objects, you must use the ACCOUNTADMIN role. (This restriction helps to control costs and manage business information risks.) The script also grants the `test_role` role the privileges needed to manage the newly created objects.

     * Grants the role to the specified Snowflake user, who then uses the role to explore the tutorials.
    
        USE ROLE ACCOUNTADMIN;
    
    CREATE ROLE test_role;
    
    CREATE DATABASE IF NOT EXISTS tutorial_db;
    GRANT OWNERSHIP ON DATABASE tutorial_db TO ROLE test_role COPY CURRENT GRANTS;
    
    CREATE OR REPLACE WAREHOUSE tutorial_warehouse WITH
      WAREHOUSE_SIZE='X-SMALL';
    GRANT USAGE ON WAREHOUSE tutorial_warehouse TO ROLE test_role;
    
    GRANT BIND SERVICE ENDPOINT ON ACCOUNT TO ROLE test_role;
    
    CREATE COMPUTE POOL tutorial_compute_pool
      MIN_NODES = 1
      MAX_NODES = 1
      INSTANCE_FAMILY = CPU_X64_XS;
    GRANT USAGE, MONITOR ON COMPUTE POOL tutorial_compute_pool TO ROLE test_role;
    
    GRANT ROLE test_role TO USER <user_name>
    

Copy

Note that:

     * You create a warehouse because the services (including job services) can run SQL DML statements (such as SELECT and INSERT). Snowflake executes these statements in the warehouse.

     * In tutorial 1, you create a service that exposes an endpoint as public to allow users to access the service from the public web (ingress). To create this service:

       * The role `test_role` must have the BIND SERVICE ENDPOINT privilege on the account.

       * The current implementation requires a security integration, which the script creates.

     * A [compute pool](../working-with-compute-pool) is a collection of one or more virtual machine (VM) nodes on which Snowflake runs your services.

  3. Make sure you are logged in to Snowflake as the user specified in the preceding script.

  4. Using the `test_role` role, execute the following script to create database-scoped objects common to all the tutorials.
    
        USE ROLE test_role;
    USE DATABASE tutorial_db;
    USE WAREHOUSE tutorial_warehouse;
    
    CREATE SCHEMA IF NOT EXISTS data_schema;
    CREATE IMAGE REPOSITORY IF NOT EXISTS tutorial_repository;
    CREATE STAGE IF NOT EXISTS tutorial_stage
      DIRECTORY = ( ENABLE = true );
    

Copy

Note that:

     * You create an image repository to store your service code (container images).

     * You create a Snowflake stage to store your service specification files in tutorial 2 and 3.

## Verify that you are ready to continue¶

  1. To verify that you have the objects needed for the tutorials, execute the following commands:
    
        SHOW COMPUTE POOLS; --or DESCRIBE COMPUTE POOL tutorial_compute_pool;
    

Copy

    
        SHOW WAREHOUSES;
    

Copy

    
        SHOW IMAGE REPOSITORIES;
    

Copy

    
        SHOW STAGES;
    

Copy

  2. To verify that you have your account information (organization and account names), use one of the following methods:

     * Find the information on the Snowsight web interface, in the lower left corner of the Home page.

     * In the SnowSQL CLI, execute SHOW IMAGE REPOSITORIES. The command returns the repository URL, including the organization and account names.

**Example**

        
                <orgname>-<acctname>.registry.snowflakecomputing.com/tutorial_db/data_schema/tutorial_repository
        

Copy

### What’s next?¶

You can now explore [Tutorial 1](tutorial-1).

