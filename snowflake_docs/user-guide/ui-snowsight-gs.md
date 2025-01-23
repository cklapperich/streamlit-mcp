# Getting started with Snowsight¶

This topic describes how to get started with Snowsight, the Snowflake web
interface.

If you want to upgrade to Snowsight from the Classic Console, see [About the
Snowsight upgrade](ui-snowsight-upgrade-guide).

Note

Some Snowsight features require a warehouse to run SQL queries for retrieving
data, such as Task Run History or Data Preview for a table. An X-Small
warehouse is recommended and generally sufficient for most of these queries.
For information, see [Warehouse considerations](warehouses-considerations).

## Signing in to Snowsight¶

You can access Snowsight over the internet or through private connectivity to
the Snowflake service:

  * Using the internet

  * Using private connectivity

After signing in to Snowsight, you see your recently updated worksheets. See
[Getting started with worksheets](ui-snowsight-worksheets-gs).

### Using the internet¶

To access Snowsight over the public Internet, do the following:

  1. In a supported web browser, navigate to <https://app.snowflake.com>.

  2. Provide your [account identifier](admin-account-identifier) or account URL. If you’ve previously signed in to Snowsight, you might see an account name that you can select.

  3. Sign in using your Snowflake account credentials.

You can also access Snowsight from the Classic Console:

  1. Sign in to the Classic Console.

  2. In the navigation menu, select Snowsight [![Snowsight](../_images/ui-navigation-worksheets-icon.png)](../_images/ui-navigation-worksheets-icon.png).

Snowsight opens in a new tab.

### Using private connectivity¶

After completing the configuration to use private connectivity, access
Snowsight:

  * To sign in to Snowsight with private connectivity directly, without having been logged in to the Classic Console previously:

    1. Enter either of the following URLs in the browser location bar:

       * `https://app-_orgname_ -_account_name_.privatelink.snowflakecomputing.com`

       * `https://app._cloud_region_id_.privatelink.snowflakecomputing.com`

Where:

       * `_orgname_` is the name of your Snowflake organization.

       * `_account_name_` is the unique name of your account within your organization.

       * `_cloud_region_id_` is the identifier for the cloud region (controlled by the cloud platform).

After signing in, you can find these details in the account selector in
Snowsight.

For details, see Locate your Snowflake account information in Snowsight and
[Format 1 (preferred): Account name in your organization](admin-account-
identifier.html#label-account-name).

Note

If you are unsure of the values to enter, please contact your internal
Snowflake administrator before contacting Snowflake Support.

    2. Enter your Snowflake credentials.

  * Starting from the Classic Console, to sign in to Snowsight using private connectivity to the Snowflake service:

    1. Sign in to the Classic Console.

    2. In the upper-right corner of the Classic Console, select Snowsight [![Snowsight](../_images/ui-navigation-worksheets-icon.png)](../_images/ui-navigation-worksheets-icon.png).

Snowsight opens in a new tab or window.

## Snowsight and MFA¶

Snowflake takes security very seriously and strongly encourages all users to
configure multi-factor authentication (MFA). Users signing in to Snowsight who
have not yet configured multi-factor authentication will be prompted to do so.
You can dismiss the request to configure MFA, however you will be re-prompted
every three days.

To configure MFA:

  1. Select your username, and then select My Profile.

  2. In the Multi-factor authentication section, select Enroll.

  3. Follow the prompts to configure MFA for your device type.

For more information see [Enroll in multi-factor authentication (MFA)](ui-
snowsight-profile.html#label-snowsight-set-up-mfa).

### Switch to a different Snowflake account¶

You can sign in to a different Snowflake account by following these steps:

  1. While signed in to Snowsight, select your username at the bottom of the navigation bar.

  2. Select an account that you have previously signed in to, or select Sign Into Another Account.

You’re prompted to sign in to the selected account.

[![Switch Account](../_images/snowsight-gs-account-
selector.png)](../_images/snowsight-gs-account-selector.png)

## Supported browsers for using Snowsight¶

Snowsight supports the latest three major versions of the following browsers:

  * Apple Safari for macOS

  * Google Chrome

  * Microsoft Edge

  * Mozilla Firefox

## Access Snowsight through a proxy or firewall¶

To access Snowsight through a proxy or firewall, you might need to add the
fully qualified URL and port values to the proxy servers or firewall
configuration.

To determine the fully qualified URL and port for Snowsight, run the
[SYSTEM$ALLOWLIST](../sql-reference/functions/system_allowlist) function and
review the `SNOWSIGHT_DEPLOYMENT` entry in the return value.

## Locate your Snowflake account information in Snowsight¶

To locate account information, such as the account identifier or URL, for
either your current account or one that you have previously signed in to,
follow these steps:

  1. Open the account selector and review the list of accounts that you previously signed in to.

> [![Screenshot of the account selector open and listing multiple accounts.
> The account selector is labeled with the name of the currently-selected
> account.](../_images/snowsight-gs-account-
> selector.png)](../_images/snowsight-gs-account-selector.png)

  2. Locate the account for which you want to copy the account name.

  3. Hover over the account to view additional details, and then select the copy icon to copy the account identifier in the format `_orgname_._account_name_` to your clipboard.

> [![Screenshot of the account selector open and listing multiple accounts,
> with a cursor hovering over an account to display an additional pane of
> information about the account and hovering over the option to copy the
> account identifier.](../_images/ui-snowsight-account-
> identifier.png)](../_images/ui-snowsight-account-identifier.png)

Note

The account identifier is copied in the format `_orgname_._account_name_`,
which is used for SQL commands and operations.

If you need to use the account identifier with a Snowflake driver (for
example, JDBC or ODBC), you need to replace the period (`.`) with a hyphen
(`-`) so the identifier is formatted as `_orgname_ -_account_name_`.

To copy your account URL, select [![Copy account URL](../_images/snowsight-
account-url.png)](../_images/snowsight-account-url.png) (Copy account URL).

## Switch your active role¶

While using Snowsight, you can change the active role in your current session.
Your active role determines which pages in Snowsight you can access, as well
as which databases, tables, and other objects you can see and the actions you
can perform on them.

To switch your active role:

  1. To open the user menu, in the navigation menu, select your username.

  2. Select the active role. For example, PUBLIC.

The role selector appears.

  3. Select the role that you want to use. For example, ACCOUNTADMIN.

To learn more about roles and privileges, see [Overview of Access
Control](security-access-control-overview).

## Configuring private connectivity for Snowsight¶

Before you can set up private connectivity for Snowsight, you must set up
private connectivity for your Snowflake account. Follow the guide specific to
the cloud platform that hosts your Snowflake account:

  * [AWS](admin-security-privatelink)

  * [Azure](privatelink-azure)

  * [Google Cloud Platform](private-service-connect-google)

To use private connectivity with Snowsight, configure your DNS and ensure
firewalls allow access to the relevant values:

  1. Using the ACCOUNTADMIN role, call the [SYSTEM$GET_PRIVATELINK_CONFIG](../sql-reference/functions/system_get_privatelink_config) function in your Snowflake account and identify the values for the following:

>      * `privatelink-account-url`
>
>      * `snowsight-privatelink-url`
>
>      * `regionless-snowsight-privatelink-url`

  2. Confirm that your DNS settings can resolve the values.

  3. Confirm that you can connect to Snowsight using each of those URLs from your browser.

  4. If you want to use the account name URL (the value for `regionless-snowsight-privatelink-url`) as your primary URL to access Snowsight, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) and request that all URL redirects point to the URL specified by `regionless-snowsight-privatelink-url`.

