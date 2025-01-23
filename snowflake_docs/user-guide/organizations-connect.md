# Connecting to your accounts¶

This topic provides the URL and [account identifier](admin-account-identifier)
formats that you use to connect to the Snowflake accounts in your
organization.

Note

If you are an organization administrator and want to delete old URLs for an
account that has changed, see [Managing account URLs](organizations-manage-
accounts-urls).

## Connecting to the Snowflake web interface¶

To connect to Snowsight using your web browser, see [Signing in to
Snowsight](ui-snowsight-gs.html#label-snowsight-getting-started-sign-in).

## Connecting with a URL¶

Snowflake supports multiple URL formats when connecting to a Snowflake account
without a browser. For example, an identity provider might use a direct URL to
communicate with Snowflake.

  * The **account name** format uses the name of the account and its [organization](organizations) to identify the account. To find the name of your organization and account, see [Finding the organization and account name for an account](admin-account-identifier.html#label-account-name-find).

  * The **connection name** format, which replaces the account name with the name of a connection, is required when using the [Client Redirect](client-redirect) feature. To find the name of your connection, execute the [SHOW CONNECTIONS](../sql-reference/sql/show-connections) command.

  * The legacy **account locator** format is currently supported, but its use is discouraged.

### Standard account URLs¶

The standard URL format can be used in most cases where a Snowflake account
URL is required, including:

>   * SSO connections (except Okta)
>
>   * SCIM base URL (except Okta)
>
>   * OAuth connections with third-party identity providers (except Okta)
>
>   * OAuth base URL for a Snowflake Authorization Server
>
>

The standard URL formats are:

>   * Account name: `https://<orgname>-<account_name>.snowflakecomputing.com`
>
>   * Connection name:
> `https://<orgname>-<connectionname>.snowflakecomputing.com`
>
>   * Account locator (legacy):
> `https://<accountlocator>.<region>.<cloud>.snowflakecomputing.com`
>
>

### Private connectivity URLs¶

When connecting to Snowflake using private connectivity to the Snowflake
service (e.g. AWS PrivateLink), the string `privatelink` must be appended to
the [account identifier](admin-account-identifier) in the Snowflake account
URL.

>   * Account Name:
> `https://<orgname>-<account_name>.privatelink.snowflakecomputing.com`
>
>   * Connection Name:
> `https://<orgname>-<connectionname>.privatelink.snowflakecomputing.com`
>
>   * Account Locator (legacy):
> `https://<account_locator>.<region>.privatelink.snowflakecomputing.com`
>
>

Note that using private connectivity requires updating DNS records to include
the private connectivity URL. For more information, see:

>   * [AWS PrivateLink CNAME Records](admin-security-privatelink.html#label-
> aws-pl-additional-cname-records).
>
>   * Azure Private Link DNS setup in the [configuration
> procedure](privatelink-azure.html#label-azure-pl-config-procedure).
>
>   * Google Cloud Private Service Connect DNS setup in [Step 8](private-
> service-connect-google.html#label-gcp-psc-config).
>
>

### Okta URLs¶

When using Okta for SSO, SCIM, or OAuth, you must use a special account name
format if the account name contains an underscore. Because Okta does not
support underscores in URLs, the underscore in the account name must be
converted to a hyphen.

>   * Account name: `https://<orgname>-<account-name>.snowflakecomputing.com`
>
>   * Connection name: Use the standard URL
>
>   * Account locator (legacy): Use the standard URL
>
>

## Connecting from clients, connectors, and drivers¶

See [Configuring a client, driver, library, or third-party application to
connect to Snowflake](gen-conn-config).

## Backwards compatibility¶

Using the legacy account locator in an account identifier or account URL is
still supported, though discouraged.

