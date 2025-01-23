# REST API for unstructured data support¶

This topic describes the REST API used to access staged files.

## `GET /api/files/`¶

Retrieves (downloads) a data file from an internal or external stage.

### Authentication¶

Authenticate to the REST API endpoint using OAuth for custom clients. Create a
security integration (using [CREATE SECURITY INTEGRATION](../sql-
reference/sql/create-security-integration-oauth-snowflake)) to enable an HTTP
client that supports OAuth (such as [cURL](https://curl.se/)) to redirect
users to an authorization page and generate access tokens for access to the
REST API endpoint. For information on configuring OAuth for custom clients,
see [Configure Snowflake OAuth for custom clients](oauth-custom).

### Usage notes¶

  * Send the scoped URL or file URL for a staged file in the GET request.

    * Generate a scoped URL by calling the [BUILD_SCOPED_FILE_URL](../sql-reference/functions/build_scoped_file_url) SQL function.

    * Generate a file URL by calling the [BUILD_STAGE_FILE_URL](../sql-reference/functions/build_stage_file_url) SQL function. Alternatively, query the directory table for the stage, if available.

  * Authenticate to Snowflake via the Snowflake SQL API using OAuth or key pair authentication. For instructions, see [Authenticating to the server](../developer-guide/sql-api/authenticating).

  * The authorization to access files differs depending on whether a scoped URL or file URL is sent in the GET request:

Scoped URL:

    

Only the user who generated the scoped URL can use the URL to access the
referenced file.

File URL:

    

Any role that has sufficient privileges on the stage can access the file:

    * External stage: USAGE

    * Internal stage: READ

  * An HTTP client that sends a URL (either scoped URL or file URL) to the REST API must be configured to allow redirects.

  * If files downloaded from an internal stage are corrupted, verify with the stage creator that `ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')` is set for the stage.

### Request headers¶

The following request headers apply to all operations:

Header | Description  
---|---  
`Authorization` | Set this to `Bearer`, followed by the generated OAuth token used to authenticate to Snowflake. For more information, see [Authenticating to the Server Using OAuth](../developer-guide/sql-api/authenticating.html#label-sql-api-authenticating-oauth). For example:

> `Authorization: Bearer _token_`  
  
`Accept` | Set this to `*/*`.  
`User-Agent` | Set this to the name and version of your application (e.g. `applicationName/applicationVersion`). You must use a value that complies with [RFC 7231](https://tools.ietf.org/html/rfc7231#section-5.5.3).  
`X-Snowflake-Authorization-Token-Type` | Set this to `OAUTH`.  
  
### Example¶

The following Python example issues an HTTP request for client `myApplication`
version 1.0:

    
    
    import requests
    response = requests.get(url,
        headers={
          "User-Agent": "reg-tests",
          "Accept": "*/*",
          "X-Snowflake-Authorization-Token-Type": "OAUTH",
          "Authorization": """Bearer {}""".format(token)
          },
        allow_redirects=True)
    print(response.status_code)
    print(response.content)
    

Copy

