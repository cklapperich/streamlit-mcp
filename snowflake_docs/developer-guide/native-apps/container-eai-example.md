# Example - Configure external access for services in an app with containers¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) Feature — Generally
Available

The Snowflake Native App Framework is generally available on supported cloud
platforms. For additional information, see [Support for private connectivity,
VPS, and government regions](limitations.html#label-native-apps-supported-
clouds).

This topic describes how to grant access to an endpoint that is external to
Snowflake in an app with containers. This example uses external access
integrations and secrets to allow access to the endpoint.

To grant access to an external endpoint in an app with containers, providers
must define reference to the following objects:

  * [EXTERNAL ACCESS INTEGRATION](../external-network-access/creating-using-external-network-access)

Defines a list of network rules that specify the domain names of external
endpoints. An external access integration can also specify a list of secrets
that store the credentials used to access these endpoints. Secrets are
optional and can be set to NONE or ALL.

In the context of an app with containers, external access integrations require
the USAGE privilege.

Note

The `multi_valued` property cannot be set to TRUE. Only single-valued
references are supported.

  * [SECRET](../external-network-access/creating-using-external-network-access.html#label-creating-using-external-access-integration-secret)

> Contains the credentials required to use the external access integration to
> connect to an external endpoint.
>
> In the context of an app with containers, secrets support the USAGE and READ
> privileges. At least one of these privileges must be specified. The READ
> privilege must be specified if the secret is used with a service or is
> attached to a stored procedure or user-defined function.

## Add an external access integration reference to the manifest file¶

The following example shows how a provider defines an external access
integration in the manifest file:

    
    
    references:
      ...
      - my_external_access:
          label: "Default External Access Integration"
          description: "This EAI is required to access xyz.com"
          privileges:
            - USAGE
          object_type: EXTERNAL ACCESS INTEGRATION
          required_at_setup: true
          register_callback: config.REGISTER_EAI_CALLBACK
          configuration_callback: config.get_config_for_ref
    

Copy

This example specifies the following properties, among others, under
`references`:

  * `my_external_access`: Specifies the name of the external reference.

    * `privileges`: Lists the privileges required by the external access integration. In this example, the USAGE privilege is required.

    * `object_type: EXTERNAL ACCESS INTEGRATION`: Indicates a reference to an external access integration.

    * `required_at_setup`: Indicates that the consumer must authorize access on the object before the app can create the object when set to `true`.

    * `register_callback`: Specifies the callback stored procedure used to register the reference with the app.

    * `configuration_callback`: Specifies the configuration callback function for the secret. See Add the configuration_callback function to the setup script for more information.

## Add a secret reference to the manifest file.¶

The following example shows how a provider defines a secret in the manifest
file:

    
    
    references:
     ...
     - consumer_secret:
         label: "Consumer secret"
         description: "Needed to authenticate with an external endpoint"
         privileges:
           - READ
         object_type: SECRET
         register_callback: config.register_my_secret
         configuration_callback: config.get_config_for_ref
    

Copy

This example specifies the following properties, among others, under
`references`:

  * `consumer_secret`: Specifies the name of the reference.

    * `privileges`: Lists the privileges required by the secret. In this example, the READ privilege is specified.

    * `object_type: SECRET`: Indicates that the reference is a secret.

    * `register_callback`: Specifies the callback stored procedure used to register the reference with the app.

    * `configuration_callback`: Specifies the configuration callback function for the secret. See Add the configuration_callback function to the setup script for more information.

## Add the configuration_callback function to the setup script¶

After adding references for the secret and external access integration, you
must add the `configuration_callback` function to the setup script. To create
an external access integration or secret, the app must be able to determine
values for the host port, secret type, the authorization and token endpoint
for OAuth, and so on. The `configuration_callback` function provides this
information from the consumer account to the app.

    
    
    CREATE OR REPLACE PROCEDURE CONFIG.GET_CONFIG_FOR_REFERENCE(ref_name STRING)
    RETURNS STRING
    LANGUAGE SQL
    AS
    $$
    BEGIN
     CASE (UPPER(ref_name))
       WHEN 'my_external_access' THEN
         RETURN '{
           "type": "CONFIGURATION",
           "payload":{
             "host_ports":["google.com"],
             "allowed_secrets" : "LIST",
             "secret_references":["CONSUMER_SECRET"]}}';
       WHEN 'consumer_secret' THEN
         RETURN '{
           "type": "CONFIGURATION",
           "payload":{
             "type" : "OAUTH2",
             "security_integration": {
               "oauth_scopes": ["https://www.googleapis.com/auth/analytics.readonly"],
               "oauth_token_endpoint": "https://oauth2.googleapis.com/token",
               "oauth_authorization_endpoint":
                   "https://accounts.google.com/o/oauth2/auth"}}}';
      END CASE;
      RETURN '';
    END;
    $$;
    

Copy

Snowsight runs this callback procedure to populate the configuration dialog
that prompts the user to configure the required objects.

Note

The `configuration_callback` function is only supported for external access
integration and secret objects.

The procedure needs to be granted to an app role for execution as shown in the
following example:

    
    
    GRANT USAGE ON PROCEDURE CONFIG.GET_CONFIG_FOR_REFERENCE(STRING)
      TO APPLICATION ROLE app_admin;
    

Copy

## Best practices when using external access integrations in an app with
containers¶

Snowflake recommends the following best practices when using external access
integrations in an app with containers:

  * Any reference to external access integrations that are specified in a [CREATE SERVICE](../../sql-reference/sql/create-service) or [ALTER SERVICE](../../sql-reference/sql/alter-service) command must be bound before the commands are run in the setup script. These commands fail when the reference is not bound.

  * Any references to secrets that are specified in the service specification must also be bound before the [CREATE SERVICE](../../sql-reference/sql/create-service) or [ALTER SERVICE](../../sql-reference/sql/alter-service) commands are run in the setup script. These commands fail when the reference is not bound.

  * If returning a payload of type ERROR in `configuration_callback` function, providers should return an informative error message that helps the consumer understand the cause of the error and how to resolve it. For example:

    * If there is an error in the app

    * If the reference is not required yet

    * If the reference is not ready to be allowed.

  * If the `configuration_callback` function contain references with the `required_at_setup` property set to TRUE, the `configuration_callback` function must succeed at setup time. In this context, the `configuration_callback` function can’t depend on information from the consumer.

  * When using a reference to an external access integration with a service, consider creating the service using ALLOWED_AUTHENTICATION_SECRETS = ALL if the app requires secrets provided by the consumer. This simplifies handling a secret within an external access integration.

  * If an app only needs to reach specific endpoints and does not require any secrets, use ALLOWED_AUTHENTICATION_SECRETS = NONE. NONE is the default value. See [CREATE EXTERNAL ACCESS INTEGRATION](../../sql-reference/sql/create-external-access-integration) for more information.

  * If the app needs to update a reference, first, unbind the reference, then prompt the consumer to create and bind a new object to the reference. A consumer can choose to edit and bind an existing object. See [CREATE EXTERNAL ACCESS INTEGRATION](../../sql-reference/sql/create-external-access-integration).

