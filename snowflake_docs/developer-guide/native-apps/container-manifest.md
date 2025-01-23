# Create the manifest file for an app with containers¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) Feature — Generally
Available

The Snowflake Native App Framework is generally available on supported cloud
platforms. For additional information, see [Support for private connectivity,
VPS, and government regions](limitations.html#label-native-apps-supported-
clouds).

The topic describes the components of the `manifest.yml` file in a Snowflake
Native Apps with Snowpark Container Services. For general information about
the `manifest.yml` file, see [Create the manifest file for an application
package](creating-manifest).

## Specify the container images used by the app¶

To specify location of the container images used by the app with containers,
add the `images` property to the `artifacts.container_services` block.

You must include an entry for each image. The path specified includes the name
of the database, schema, and image repository. This path has the following
form:

    
    
    /<database>/<schema>/<image_repository>/<image_name>:tag
    

Copy

The following example shows how to specify the `images` property:

    
    
    artifacts
    ...
      container_services
        ...
        images
          - /dev_db/dev_schema/dev_repo/image1
          - /dev_db/dev_schema/dev_repo/image2
    

Copy

## Specify the user interface endpoint for an app¶

To specify the endpoint for the user interface of the app with containers, add
the `default_web_endpoint` property to the `artifacts` block.

The `default_web_endpoint` property is optional. If this property is
specified, the endpoint must also be defined in the service specification
file.

Note

Only one of the `default_web_endpoint` and `default_streamlit` can be
specified.

This entry in the manifest file has two additional properties:

  * `service`
    

Specifies the name of the service of the user interface.

  * `endpoint`
    

Specifies the name of the endpoint.

The following example shows how to specify the `default_web_endpoint`
property.

    
    
    default_web_endpoint:
      service: ux_schema.ux_service
      endpoint: ui
    

Copy

## Specify the privileges required by the app¶

Like other apps, the `references` property of the `manifest.yml` file
specifies the references that an app requests from consumers. The following
privileges are specific to an app with containers:

  * CREATE COMPUTE POOL

This privilege is required to allow the app to create a compute pool in the
consumer account. It is not required if the consumer creates the compute pool
manually.

  * BIND SERVICE ENDPOINT

This privilege is required to allow an endpoint to be accessible outside of
Snowflake.

The following example shows how to add these privileges to the `privileges`
block:

    
    
    privileges:
    - CREATE COMPUTE POOL
      description: 'Required to allow the app to create a compute pool in the consumer account.'
    - BIND SERVICE ENDPOINT
      description: 'Required to allow endpoints to be externally accessible.'
    

Copy

## Example manifest file for an app with containers¶

The Snowflake Native App Framework supports entries in the manifest file that
are specific to an app with containers. The following example `manifest.yml`
shows a typical manifest file for an app with containers:

    
    
    manifest_version: 1
    
    version:
      name: v1
    
    artifacts:
      readme: readme.md
      setup_script: setup.sql
      container_services:
        images
          - /dev_db/dev_schema/dev_repo/image1
          - /dev_db/dev_schema/dev_repo/image2
    
      default_web_endpoint:
        service: ux_schema.ux_service
        endpoint: ui
    
    privileges:
     - CREATE COMPUTE POOL
       description: "...”
     - BIND SERVICE ENDPOINT
       description: "...”
    

Copy

