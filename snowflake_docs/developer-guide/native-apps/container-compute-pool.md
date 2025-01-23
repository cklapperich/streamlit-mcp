# Add a compute pool to an app with containers¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) Feature — Generally
Available

The Snowflake Native App Framework is generally available on supported cloud
platforms. For additional information, see [Support for private connectivity,
VPS, and government regions](limitations.html#label-native-apps-supported-
clouds).

The topic describes how to use compute pools in a Snowflake Native Apps with
Snowpark Container Services.

## About compute pools in apps with containers¶

A [compute pool](../snowpark-container-services/working-with-compute-pool) is
a collection of one or more virtual machine (VM) nodes on which Snowflake runs
Snowpark Container Services. Apps with containers uses a compute pool in the
consumer account to manage the container images required by the app.

An app can create multiple compute pools and each compute pool is exclusive to
the app. Compute pools used by the app cannot be used for other purposes.

Containers within an app can directly access each other, even if they are in
different compute pools.

However, using different compute pools allows providers to separate types of
services. For example, a provider can separate their frontend services from
backend services.

Compute pools are account-level objects, meaning the name of each compute pool
must be unique within the consumer account.

## Best practices for using compute pools in an app with containers¶

Providers should consider the following best practices when creating compute
pools a consumer account:

  * Compute pools have cost implications. It is important to set values for the `min_nodes`, `max_nodes`, and `instance_family` properties to consume the correct amount of resources. Providers should also set the AUTO_SUSPEND_SECS property to automatically suspend inactive compute pools.

See [CREATE COMPUTE POOL](../../sql-reference/sql/create-compute-pool) for
more information.

  * Compute pools are account-level objects, as such their pool names must be unique within a consumer account. Consider using the application name as a prefix of the compute pool name to ensure uniqueness.

  * When adding a computer pool to an app with containers that is installed on different cloud service providers, the code used to create the compute pool must account for differences in the instance families across different cloud service providers. For example, the `HIGHMEM_X64_L` instance family has a different configuration for each cloud service provider.

See [CREATE COMPUTE POOL](../../sql-reference/sql/create-compute-pool) for
more information on available instance families. See Choose different instance
families for each provider for an example of how to set the instance family
for different cloud service providers.

  * Set the `uses_gpu` property to TRUE only if the app with containers uses a GPU as the instance family of the compute pool. See Set the uses_gpu property in the manifest file for more information.

## Create a compute pool for an app¶

There are two ways to create a compute pool for an app with containers:

  * The app creates the compute pools required during installation. This requires that the consumer grants the CREATE COMPUTE POOL privilege on the compute pool to the app. A provider can configure the app to request these privileges using Snowsight.

See Configure an app to request the CREATE COMPUTE POOL privilege for more
information.

  * The consumer manually creates the compute pools required by the app. The consumer must run the [CREATE COMPUTE POOL](../../sql-reference/sql/create-compute-pool) to create the compute pool, then manually grant the CREATE COMPUTE POOL privilege on the compute pool to the app.

## Set the `uses_gpu` property in the manifest file¶

If an app with containers specifies a GPU as the instance family for the
Compute Pool, providers must set the `uses_gpu` flag to `true` in the
manifest. The following example shows how to set this flag in the `artifacts`
block:

    
    
    artifacts:
      readme: readme.md
      setup_script: scripts/setup.sql
      container_services:
        uses_gpu: true|false
        images:
        - /provider_db/provider_schema/provider_repo/server:prod
        - /provider_db/provider_schema/provider_repo/web:1.0
    

Copy

The automated security scan uses this flag security scanning framework to
validate behavior during the app version scanning process.

Caution

To publish an app with containers on the Snowflake Marketplace, the app must
create the required compute pools during installation. See [Enforced
requirements](publish-guidelines.html#label-native-apps-marketplace-
guidelines) for the Snowflake Marketplace publication requirements.

## Configure an app to request the CREATE COMPUTE POOL privilege¶

Providers can configure an app to request the CREATE COMPUTE POOL privilege.
They can also create the compute pool from the setup script when the app is
installed or upgraded.

Note

An app can create a maximum of five compute pools in a consumer account.
Contact Snowflake support if your app needs to create additional compute
pools.

### Request the CREATE COMPUTE POOL privilege¶

An app can request the CREATE COMPUTE POOL privileges from a consumer. This
privilege allows the app to create a compute pool in the consumer account. See
[Request global privileges from consumers](requesting-privs) for general
information about requesting global privileges from the consumer.

To request the CREATE COMPUTE POOL privilege from a consumer, add the CREATE
COMPUTE POOL privilege to the `manifest.yml` file as shown in the following
example:

    
    
    ...
    privileges:
     - CREATE COMPUTE POOL
       description: "Enable application to create one to five compute pools"
     ...
    

Copy

See [Create the manifest file for an app with containers](container-manifest)
for more information on creating the `manifest.yml` file for an app with
containers.

Note

The behavior for the CREATE COMPUTE POOL privilege request within a container
app is different than other privilege requests. When you add this privilege to
the `manifest.yml` file, Snowsight displays an interface that allows a
consumer to grant the required privileges.

### Add the CREATE COMPUTE POOL command to the setup script¶

To create a compute pool in the consumer account add the [CREATE COMPUTE
POOL](../../sql-reference/sql/create-compute-pool) command to the setup script
of the app.

The following example shows how to create a compute pool within a stored
procedure in the setup script:

    
    
    CREATE COMPUTE POOL IF NOT EXISTS app_compute_pool
      MIN_NODES = 1
      MAX_NODES = 1
      INSTANCE_FAMILY = standard_1
      AUTO_RESUME = true;
    

Copy

Note

When creating a compute pool within the app, providers should check that the
provider has granted the CREATE COMPUTE POOL privilege before creating the
compute pool.

Compute pools that an app creates are owned exclusively by that app. They
cannot be used by other applications or by the consumer directly.

In general, users in the consumer account can only see compute pools created
by the app in the following situations:

  * The user has been granted the MANAGE GRANTS privilege.

  * The app grants access to the compute pool using application roles.

Application developers can allow users with active roles specific privileges
on applications owned by compute pools. In addition, administrators with the
ACCOUNTADMIN role can grant themselves the privileges necessary to control the
applications owned by compute pools. For more information about compute pool
access requirements, see [ALTER COMPUTE POOL](../../sql-reference/sql/alter-
compute-pool).

### Prefix the compute pool within the setup script¶

Because compute pools are account-level objects, compute pool names must be
unique within the consumer account. The following example shows how to use the
application name as a prefix of the compute pool name:

    
    
    LET POOL_NAME := (select current_database()) || '_app_pool';
    CREATE COMPUTE POOL IF NOT EXISTS identifier(:pool_name)
      MIN_NODES = 1
      MAX_NODES = 1
      INSTANCE_FAMILY = STANDARD_2;
    

Copy

## Choose different instance families for each provider¶

When creating a compute pool for an app that is published across multiple
cloud service providers, the code that creates the setup script must be
written to account for differences in how instance families are configured.

The following example shows how to write a stored procedure to create a
compute pool based on the cloud service provider where the app is being
installed:

    
    
     CREATE OR REPLACE PROCEDURE public.create_cp()
     RETURNS VARCHAR
     LANGUAGE SQL
     EXECUTE AS OWNER
     AS $$
      BEGIN
          LET POOL_NAME := (select current_database()) || '_app_pool';
          LET INSTANCE_FAMILY := IFF( CONTAINS(current_region(), 'AZURE') , 'GPU_NV_XS' , 'GPU_NV_S' );
          CREATE COMPUTE POOL IF NOT EXISTS identifier(:pool_name)
              MIN_NODES = 1
              MAX_NODES = 1
              INSTANCE_FAMILY = :instance_family;
          RETURN 'Compute Pool Created';
      END;
    $$;
    

Copy

