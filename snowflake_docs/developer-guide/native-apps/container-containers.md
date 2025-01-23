# Set up the containers and services managed by an app¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) Feature — Generally
Available

The Snowflake Native App Framework is generally available on supported cloud
platforms. For additional information, see [Support for private connectivity,
VPS, and government regions](limitations.html#label-native-apps-supported-
clouds).

The topic describes how to set up the containers and services for a Snowflake
Native App with Snowpark Container Services.

## Create an image repository¶

To manage containers with a Snowflake Native App, providers must create an
[image repository](../snowpark-container-services/working-with-registry-
repository) in the provider account to store the images required by the app.

The image repository must exist within a database and schema. The following
example shows how to create an image repository using the [CREATE IMAGE
REPOSITORY](../../sql-reference/sql/create-image-repository) command.

    
    
    CREATE DATABASE provider_db;
    CREATE SCHEMA provider_schema;
    CREATE IMAGE REPOSITORY provider_repo;
    

Copy

Note

Snowflake recommends that providers create the image repository outside the
application package.

If the application package is attached to a listing and the listing is
configured to use [Cross-Cloud Auto-Fulfillment](https://other-
docs.snowflake.com/en/collaboration/provider-listings-auto-fulfillment) an
image repository within the application package would be replicated and
additional costs incurred.

The images uploaded to this repository are accessible to the application
package when adding a version definition. The app has can only access the
images in this repository that are specified in the manifest file of the
application package.

The following consideration apply to image repositories in the context of an
app with containers:

  * External image repositories are not supported. Image repositories that are outside Snowflake cannot be referenced by any services within the container. This is applicable to services that exist in or outside of the app.

  * Providers cannot directly share an image repository with an app. For example, providers cannot use the GRANT TO SHARE IN APPLICATION PACKAGE command.

  * Providers can store multiple container images in an image repository. However, container images that are not explicitly listed in the manifest are not accessible by the app in the consumer’s account.

  * When a provider adds a version definition to an application package the container images included in that version cannot be modified. The images for that version are immutable and persist throughout the life cycle of the version. To alter the containers within an app, providers must use a new version.

## Upload container images to the image repository¶

After creating an image repository, providers use Docker commands to upload
the container images required by the app to the image repository. The specific
commands required depend on the provider’s environment. However, the general
workflow is:

  1. docker login

  2. docker build

  3. docker tag

  4. docker push

The following shows a typical example of how to use these commands:

    
    
    $ docker login org-provider-account.registry.snowflakecomputing.com
    $ docker build --rm --platform linux/amd64 -t service:1.0 .
    $ docker tag service:1.0 org-provider-account.registry.snowflakecomputing.com/provider_db/provider_schema/provider_repo/service:1.0
    $ docker push org-provider-account.registry.snowflakecomputing.comprovider_db/provider_schema/provider_repo/service:1.0
    

Copy

## Create the service specification file¶

The service specification is a YAML file that Snowpark Container Services uses
to configure and run a service. See [Service specification
reference](../snowpark-container-services/specification-reference) for general
information on the syntax of this file. See [Create a service from a
specification file](container-services.html#label-native-apps-container-
service-create-spec) for an example of creating a service in the setup script.

The following example shows the fields in the service specification file that
are required by an app with containers.

    
    
    spec:
      containers:
      - image: /provider_db/provider_schema/provider_repo/server:prod
        name: server
        ...
      - image: /provider_db/provider_schema/provider_repo/web:1.0
        name: web
        ...
      endpoints:
      - name: invoke
        port: 8000
      - name: ui
        port: 5000
        public: true
    

Copy

Note

The service specification file references container images using the original
database, schema and image repository names. During installation or upgrade, a
service is created from the service specification file..

Explicit registry URLs, for example `org-
provider.registry.snowflakecomputing.com/db/schema/repo/img:123` are not
supported and result in an error. The location of the image must always a
full-qualified name in the provider account.

## Use a specifciation template¶

Providers can also use a [specification template](../snowpark-container-
services/working-with-services.html#label-spcs-working-with-services-using-
specification-templates) by adding a reference to a template in the service
specification file:

    
    
    spec:
      containers:
      - image: /provider_db/provider_schema/provider_repo/server:prod
        name: my_app_container
      endpoints:
      - name: invoke
        port: 8000
      - name: ui
        port: 5000
        public: true
    

Copy

See [Create a service with a specification template](container-
services.html#label-native-apps-container-service-create-template) for an
example of creating a service in an app using a specification template.

