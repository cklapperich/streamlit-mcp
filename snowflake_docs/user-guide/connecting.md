# Logging in to Snowflake¶

You can log in to Snowflake in many ways.

If you’re getting started with Snowflake, start by using Snowsight or SnowSQL,
the command line client that you can download. After you get comfortable using
Snowflake, you can explore connecting to Snowflake with other methods.

## Your Snowflake account identifier¶

All access to Snowflake is through your account identifier. See [Account
identifiers](admin-account-identifier) for details.

## Signing in using Snowsight¶

You can access Snowsight over the internet or through private connectivity to
the Snowflake service:

  * Using the internet

  * Using private connectivity

For more information about the tasks you can perform in Snowsight, refer to
[Snowsight quick tour](ui-snowsight-quick-tour).

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

After [completing the configuration to use private connectivity](ui-snowsight-
gs.html#label-ui-snowsight-config-private-connectivity), access Snowsight:

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

For details, see [Locate your Snowflake account information in Snowsight](ui-
snowsight-gs.html#label-snowsight-account-details) and [Format 1 (preferred):
Account name in your organization](admin-account-identifier.html#label-
account-name).

Note

If you are unsure of the values to enter, please contact your internal
Snowflake administrator before contacting Snowflake Support.

    2. Enter your Snowflake credentials.

  * Starting from the Classic Console, to sign in to Snowsight using private connectivity to the Snowflake service:

    1. Sign in to the Classic Console.

    2. In the upper-right corner of the Classic Console, select Snowsight [![Snowsight](../_images/ui-navigation-worksheets-icon.png)](../_images/ui-navigation-worksheets-icon.png).

Snowsight opens in a new tab or window.

## Logging in using SnowSQL¶

SnowSQL is the command line client for connecting to Snowflake to execute SQL
queries and perform all DDL and DML operations, including loading data into
and unloading data out of database tables.

### Step 1: Download and install SnowSQL¶

You can download the SnowSQL installer from the [SnowSQL
Download](https://developers.snowflake.com/snowsql/) page. No authentication
is required. This version of the SnowSQL installer enables auto-upgrade for
patches.

For more detailed instructions, see [Installing SnowSQL](snowsql-install-
config).

#### Configuring the Z shell alias (macOS only)¶

If Z shell (also known as zsh) is your default terminal shell, set an alias to
the SnowSQL executable so that you can run SnowSQL on the command line in
Terminal. The SnowSQL installer installs the executable in
`/Applications/SnowSQL.app/Contents/MacOS/snowsql` and appends this path to
the PATH or alias entry in `~/.profile`. Because zsh does not normally read
this file, add an alias to this path in `~/.zshrc`, which zsh does read.

To add an alias to the SnowSQL executable:

  1. Open (or create, if missing) the `~/.zshrc` file.

  2. Add the following line:
    
        alias snowsql=/Applications/SnowSQL.app/Contents/MacOS/snowsql
    

Copy

  3. Save the file.

### Step 2: Connect to Snowflake and initiate a session¶

  1. From a terminal window, start SnowSQL from the command prompt using the following command:

> >     $ snowsql -a <account_identifier>
>  
>
> Copy

Where `<account_identifier>` is your [account identifier](admin-account-
identifier). Note that when you specify your account identifier, do not
include the `snowflakecomputing.com` domain name.

You can further streamline login by specifying the `-u` option followed by
your user login name:

> >     $ snowsql -a <account_identifier> -u <user_login_name>
>  
>
> Copy

  2. When prompted, enter your login name (if you didn’t provide it when executing SnowSQL) and your password.

If you specified a valid account identifier, user login name, and password,
the SnowSQL prompt appears.

Tip

For security reasons, you cannot specify your password as an option on the
command line; you must wait for SnowSQL to prompt you for your password.

However, if you would like to skip entering information on the command line or
you need to automate login, you can provide all the required account and user
credential information, as well as additional Snowflake default usage
information, as options in the SnowSQL `config` file.

For more detailed installation, configuration, login, and usage information,
see [SnowSQL (CLI client)](snowsql).

## Connecting using other methods¶

In addition to the Snowflake web interface and SnowSQL, Snowflake supports
numerous other methods for connecting, including:

  * Using 3rd-party client services and applications that support JDBC or ODBC.

  * Developing applications that connect through the Snowflake connectors/drivers for Python, Node.js, Spark, etc.

However, connecting to Snowflake using these other methods requires additional
installation, configuration, and development tasks. For more information, see
[Applications and tools for connecting to Snowflake](../guides-overview-
connecting).

