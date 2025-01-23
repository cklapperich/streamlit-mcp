# Configuration for Snowpipe Streaming¶

## Snowpipe Streaming properties¶

Configure the API connection settings in a `profile.json` file. The properties
are described in this topic.

As shown in the [Java example](https://github.com/snowflakedb/snowflake-
ingest-
java/blob/master/src/main/java/net/snowflake/ingest/streaming/example/SnowflakeStreamingIngestExample.java)
(GitHub), you can load the settings from `profile.json` by specifying the file
path as the input to the variable `PROFILE_PATH`.

### Required properties¶

`authorization_type`

    

Configure the authentication and authorization method for the user. You can
use one of the following methods:

  * `JWT` : key pair authentication with JSON Web Token (JWT). This is the default method. If `authorization_type` is not configured, the default method `JWT` is used. Configure the following `private_key` for key pair authentication:

    * `private_key` Private key to authenticate the user. Include only the key, not the header or footer. If the key is split across multiple lines, remove the line breaks.

You can provide an unencrypted key, or you can provide an encrypted key and
provide the `snowflake.private.key.passphrase` parameter to enable Snowflake
to decrypt the key. Use this parameter _if and only if_ the
`snowflake.private.key` parameter value is encrypted.

  * `OAuth` : Snowflake OAuth. This option is only available with Snowflake Ingest SDK versions 2.0.3 and later. Configure the following parameters for Snowflake OAuth in the `profile.json` file:

    * `oauth_client_id` : The client ID of the OAuth integration.

    * `oauth_client_secret` : The client secret of the OAuth integration.

    * `oauth_refresh_token` : A valid refresh token of the OAuth integration.

To support token refresh on Snowflake/OKTA OAuth, you must configure three
parameters: `oauth_client_id`, `oauth_client_secret`, and
`oauth_refresh_token`. However, if you use a customized API endpoint for OAuth
that doesn’t require these values in the token refresh request, you can fill
in the fields for these parameters with any placeholders.

`url`

    

URL for accessing your Snowflake account. This URL must include your [account
identifier](admin-account-identifier). Note that the protocol (`https://`) and
port number are optional.

Note that `url` is not required if you are already using the Snowflake Ingest
SDK and have set the `host`, `scheme`, and `port` properties in the
`profile.json` file.

`user`

    

User login name for the Snowflake account.

### Optional properties¶

`snowflake.private.key.passphrase`

    

Passphrase to decrypt the private key when the key is encrypted. For
information, see Using key pair authentication and key rotation (in this
topic).

`role`

    

Access control role to use for the session after connecting to Snowflake.

Note that the `role` property is optional for Snowflake Ingest SDK versions
2.0.3 and later. It is required for earlier Ingest SDK versions.

## Authentication and authorization¶

### Using Snowflake OAuth¶

With Snowflake Ingest SDK versions 2.0.3 and later, or Snowflake Connector for
Kafka versions 2.1.2 and later, you can use Snowflake OAuth as an
authorization method.

Follow [the workflow](oauth-custom) to create a Snowflake OAuth integration
and to call OAuth endpoints to request authorization codes and refresh access
tokens. The response of token requests contains `oauth_refresh_token`. After a
Snowflake OAuth integration is created, run the
[SYSTEM$SHOW_OAUTH_CLIENT_SECRETS](../sql-
reference/functions/system_show_oauth_client_secrets) function to obtain
`oauth_client_id` and `oauth_client_secret`.

To enable Snowflake OAuth, in the `profile.json` file, set
`authorization_type` as `OAuth`, and complete the fields
`oauth_refresh_token`, `oauth_client_id`, and `oauth_client_secret` with the
parameters obtained above.

### Using key pair authentication and key rotation¶

API calls rely on key pair authentication with JSON Web Token (JWT). JWTs are
signed using a public/private key pair with RSA encryption. This
authentication method requires a 2048-bit (minimum) RSA key pair. Generate the
public-private key pair using OpenSSL. The public key is assigned to the
Snowflake user defined in the properties file.

Complete the key pair authentication instructions described in [key pair
rotation](key-pair-auth). Copy and paste the entire private key into the
`snowflake.private.key` field in the properties file. Save the file.

See [Java Example](../developer-guide/sql-api/authenticating.html#label-sql-
api-authenticating-key-pair-java) for an example of creating a fingerprint and
generating a JWT token.

Next, evaluate the recommendation for Externalizing secrets (in this topic).

### Externalizing secrets¶

Snowflake strongly recommends externalizing secrets such as the private key
and storing them in an encrypted form or in a key management service such as
AWS Key Management Service (KMS), Microsoft Azure Key Vault, or HashiCorp
Vault.

For more information, see the Confluent description of this
[service](https://docs.confluent.io/current/connect/security.html#externalizing-
secrets).

## Examples¶

  * For a simple example that shows how the client SDK could be used to build a Snowpipe Streaming application, see [this Java file](https://github.com/snowflakedb/snowflake-ingest-java/blob/master/src/main/java/net/snowflake/ingest/streaming/example/SnowflakeStreamingIngestExample.java) (GitHub).

  * Quick start examples:

    * [Streaming Data Integration with Snowflake](https://quickstarts.snowflake.com/guide/data_engineering_streaming_integration/index.html)

    * [Getting Started with Snowpipe Streaming and Amazon MSK](https://quickstarts.snowflake.com/guide/getting_started_with_snowpipe_streaming_aws_msk/index.html)

    * [Snowpipe Streaming and Dynamic Tables for Real-Time Ingestion (CDC Use Case)](https://quickstarts.snowflake.com/guide/CDC_SnowpipeStreaming_DynamicTables)

