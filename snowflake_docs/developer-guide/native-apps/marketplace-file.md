# Specify the resources required by an app¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) Feature — Generally
Available

The Snowflake Native App Framework is generally available on supported cloud
platforms. For additional information, see [Support for private connectivity,
VPS, and government regions](limitations.html#label-native-apps-supported-
clouds).

This topic describes how to use the `marketplace.yml` file to declare the
resource requirements for an Snowflake Native App.

The `marketplace.yml` is a configuration file similar to the `manifest.yml`
file of an app. Snowflake uses this file in the following contexts:

  * The objects specified in `required_compute_pools` and `connections` properties appear in the listing in Snowsight. This give the consumer to see the resources the app may require.

  * This file can help avoid creating or using unnecessary resources, for example replicating an application package to a regions where it cannot be installed by a consumer. Before consumer requests the listing in a remote region, Snowflake ensures that the consumer meets the resource requirements declared in the `marketplace.yml` file. This helps prevent unnecessary replication costs.

  * Before installing and upgrading the application, Snowsight ensures the requirements are satisfied, to prevent installing a broken/unusable application or upgrading a working application into a unusable state.

This optional file must be at the root directory of an app at the same level
as the `manifest.yml` file. If this file is not present, no action is taken.

## Specify the compute pools required by an app¶

The following example shows how to specify the compute pool resources required
for a specific version of an app:

    
    
    required_compute_pools:
      - HIGH_MEM_POOL_1:
          label: "High memory pool"
          description: "A compute pool for computational tasks."
          compatible_instance_families:
            - HIGHMEM_X64_M
            - HIGHMEM_X64_L
    

Copy

In this example, the `required_compute_pools` a compute pool named
`HIGH_MEM_POOL_1`.

The `compatible_instance_families` property specifies the type of machine to
provision for the compute pool. You must specify at least one value declared
for each compute pool. See [CREATE COMPUTE POOL](../../sql-
reference/sql/create-compute-pool) for more information.

Note

If the `compatible_instance_families` property is missing or the values are
invalid, version creation fails.

## Specify the external endpoints required by an app¶

The following example shows how to declare the external endpoints required by
an app:

    
    
    connections:
      - LAUNCH_DARKLY:
         label: "Launch Darkly"
         description: "Feature flag and configuration"
         required: true
         endpoints:
           - "mobile.launchdarkly.com"
           - "stream.launchdarkly.com"
      - OPEN_AI:
         label: "OpenAPI"
         description: "LLM Connection"
         required: false
         endpoints:
           - "openai.com"
    

Copy

In this example, the `connection` property specifies two external endpoints,
`LAUNCH_DARKLY` and `OPEN_AI`. The `required` property indicates to the
consumer in Snowsight that the connection is required.

If you specify the `connection` in this file, the `endpoints`, and `required`
properties are required. If these properties are not present, version creation
fails. The `endpoints` property requires at least one URL.

