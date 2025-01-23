# Create the manifest file for an application package¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) Feature — Generally
Available

The Snowflake Native App Framework is generally available on supported cloud
platforms. For additional information, see [Support for private connectivity,
VPS, and government regions](limitations.html#label-native-apps-supported-
clouds).

This topic describes how to create the manifest file for an application
package.

## About the manifest file¶

The manifest file contains information that the application package requires
to create and manage a Snowflake Native App. This includes the location of the
setup script, version definitions, and configuration information for the app.

The manifest file has the following requirements:

  * The name of the manifest file must be `manifest.yml`.

  * The manifest file must be uploaded to a named stage so that it is accessible to the application package.

  * The manifest file must exist at the root of the directory structure on the named stage where other application files are stored.

## Manifest file reference¶

The following are the valid properties that the `manifest.yml` file can
contain:

manifest_version:

    

Specifies the version of the manifest file.

Required

version:

    

Defines a block containing parameters related to a version. For more
information about versions and patches, see [Update an app](update-app).

Optional

name:

    

Specifies the logical name of the version. This name is used in SQL commands
that manage versions.

Optional

patch:

    

Specifies the default patch number. This number is used in SQL commands that
manage versions. Patch numbers specified using SQL take priority. For more
information about versions and patches, see [About app versions and
patches](update-app-overview.html#label-native-apps-versioning-about).

Optional

label:

    

Specifies a name for the version that is displayed to consumers.

Optional

comment:

    

Specifies a comment for the version. This comment is only visible when the
provider runs the [SHOW VERSIONS](../../sql-reference/sql/show-versions)
command.

Optional

artifacts:

    

Defines a block related to resources that are distributed from this version of
the package.

Optional

readme:

    

Specifies a path to a readme file that provides an overview of the Snowflake
Native App in markdown format. In the case of a Streamlit app, if no value is
specified for the `default_streamlit` property, the contents of this file is
displayed to consumers when viewing the installed Snowflake Native App.

The location of this file is specified relative to the location of the
`manifest.yml` file.

Optional

setup_script:

    

Specifies the path and filename of the SQL script that is run when the
Snowflake Native App is installed. If you do not specify a value, the default
value is `setup.sql` in the same directory as the `manifest.yml` file.

Optional

default_streamlit:

    

If the Snowflake Native App includes a Streamlit app, this property specifies
the schema and name of the default Streamlit app available to consumers.

Optional

configuration:

    

Specifies a block containing configuration properties for the Snowflake Native
App.

Optional

log_level:

    

Specifies the logging level to use for the installed Snowflake Native App. For
information about supported values for this property, see [Setting levels for
logging, metrics, and tracing](../logging-tracing/telemetry-levels).

Optional

Default: Off

trace_level:

    

Specifies the trace event level to use for the installed Snowflake Native App.
When a provider enables tracing, a Snowflake Native App automatically captures
the start and end times for all queries and stored procedure calls.

Note

Publishing a Snowflake Native App with the `trace_level` property set to a
value other than `OFF` might expose calls to hidden stored procedures to any
user in the consumer account who can view the event table.

For the supported values of the `trace_level` property, see [Setting levels
for logging, metrics, and tracing](../logging-tracing/telemetry-levels).

Optional

Default: Off

privileges:

    

Defines a block containing the privileges that the consumer must grant when
the Snowflake Native App is installed.

Optional

Default: an empty list

<privilege name>:

    

Specifies the name of the privilege.

description:

    

Provides a description of the privilege being requested. The text specified in
`description` is displayed to the consumer when the privilege is displayed in
Snowsight using the Python Permission SDK, or when the [SHOW
PRIVILEGES](../../sql-reference/sql/show-privileges) command is run.

Provide as much information as possible about why the Snowflake Native App
needs this privilege and if the privilege is required or optional.

Required if `privileges` is specified.

references:

    

Defines a block containing the references defined by the provider. The
consumer must bind these references to objects within their account.

Optional

\- <reference name>:

    

Specifies the name of the reference.

label:

    

Provides a description of the reference that the consumer can view when the
Snowflake Native App is installed.

Required if `references` is specified.

description:

    

Provides a description of the reference being requested. The text specified in
`description` is displayed to the consumer when the reference is displayed in
Snowsight using the Python Permission SDK.

You should provide as much information possible about why the Snowflake Native
App needs this reference and if the privilege is required or optional.

Required if `privileges` is specified.

privileges:

    

Specifies the privileges required by the reference.

Required if `references` is specified.

object_type:

    

Specifies the type of object associated with the reference, for example, an a
schema and table, or an API integration.

Required if `references` is specified.

multi_valued:

    

Specifies that more than one object is associated with the reference. Use this
property to bind multiple consumer objects to the same reference. When this
property is specified, the same operations are performed on objects with a
single value reference. The property can also be used with objects with multi-
valued references. See [Request references and object-level privileges from
consumers](requesting-refs) to learn more about Snowflake Native App Framework
reference operations.

Optional

Default: false

register_callback:

    

Specifies the name of the callback function used to call the reference.

Required if `references` is specified.

configuration_callback:

    

Specifies the name of the callback function that will provide the desired
configuration for the object to bind to this reference.

This property is required if `object_type` is `EXTERNAL ACCESS INTEGRATION` or
`SECRET`. This property is not applicable to other types of objects.

required_at_setup:

    

Indicates that references must be bound when the app is installed. Accepts
TRUE or FALSE. The default is FALSE.

Required if `references` is specified.

## Manifest file example¶

The following example shows a typical manifest file with values specified for
all supported properties:

    
    
    manifest_version: 1 # required
    version:
      name: hello_snowflake
      patch: 3
      label: "v1.0"
      comment: "The first version of a Snowflake Native App"
    
    artifacts:
      readme: readme.md
      setup_script: scripts/setup.sql
      default_streamlit: streamlit/ux_schema.homepage_streamlit
    
    configuration:
      log_level: debug
      trace_level: always
    
    privileges:
      - EXECUTE TASK:
          description: "Run ingestion tasks for replicating Redshift data"
      - EXECUTE MANAGED TASK:
          description: "To run serverless ingestion tasks for replicating Redshift data"
      - CREATE WAREHOUSE:
          description: "To create warehouses for executing tasks"
      - MANAGE WAREHOUSES:
          description: "To manage warehouses for optimizing the efficiency of your accounts"
      - CREATE DATABASE:
          description: "To create sink databases for replicating Redshift data"
      - IMPORTED PRIVILEGES ON SNOWFLAKE DB:
          description: "To access account_usage views"
      - READ SESSION:
          description: "To allow Streamlit to access some context functions"
    
    references:
      - consumer_table:
          label: "Consumer table"
          description: "A table in the consumer account that exists outside the APPLICATION object."
          privileges:
            - SELECT
            - INSERT
            - UPDATE
          object_type: Table
          multi_valued: true
          register_callback: config.register_reference
      - consumer_external_access:
          label: "Consumer external access integration"
          description: "An external access integration in the consumer account that exists outside the APPLICATION object."
          privileges:
            - USAGE
          object_type: EXTERNAL ACCESS INTEGRATION
          register_callback: config.register_reference
          configuration_callback: config.get_configuration_for_reference
          required_at_setup: true
    

Copy

