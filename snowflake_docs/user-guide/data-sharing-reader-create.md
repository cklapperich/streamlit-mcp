# Manage reader accounts¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) Provider sharing not enabled
for all accounts

Provider sharing is enabled by default for most, but not all accounts.

If you encounter errors when attempting to share data with consumers, the
feature may not be enabled for your account. To inquire about enabling it,
please contact [Snowflake Support](https://docs.snowflake.com/user-
guide/contacting-support).

Reader accounts (formerly known as “read-only accounts”) enable providers to
share data with consumers who are not already Snowflake customers, without
requiring the consumers to become Snowflake customers.

Note

All tasks described in this topic must be performed using the ACCOUNTADMIN
role or a role granted the CREATE ACCOUNT global privilege.

## Overview¶

A reader account enables data consumers to access and query data shared by the
provider of the account, with no setup or usage costs for the consumer, and no
requirements for the consumer to sign a licensing agreement with Snowflake.

The reader account is created, owned, and managed by the provider account,
which assumes all responsibility for credit charges incurred by users in the
reader account. Similar to standard consumer accounts, the provider account
uses _shares_ to share databases with reader accounts; however, a reader
account can only consume data from the provider account that created it.

![Overview of data sharing reader accounts, where reader accounts exist within
the context of a provider account while consumer accounts are external to the
provider account.](../_images/data-sharing-reader.png)

Note

Warehouses in a reader account can consume an unlimited number of credits each
month, which will be charged to your provider account. To limit usage, set up
a [resource monitor for the warehouse](data-sharing-reader-config.html#label-
reader-create-resource-monitor).

### What is restricted/allowed in a reader account?¶

A reader account is intended primarily for querying data shared by the
provider of the account. You can work with data, for example, by creating
materialized views.

You cannot perform the following tasks in a reader account:

  * Set a [data metric function](data-quality-intro) on objects in the reader account.

  * Upload new data.

  * Modify existing data.

  * Unload data using a storage integration. However, you can use the [COPY INTO <location>](../sql-reference/sql/copy-into-location) command with your connection credentials to unload data into a cloud storage location.

Additionally, you cannot execute the following commands in a reader account:

  * [INSERT](../sql-reference/sql/insert)

  * [UPDATE](../sql-reference/sql/update)

  * [DELETE](../sql-reference/sql/delete)

  * [MERGE](../sql-reference/sql/merge)

  * [CREATE IMAGE REPOSITORY](../sql-reference/sql/create-image-repository)

  * [COPY INTO <table>](../sql-reference/sql/copy-into-table)

  * [CREATE MASKING POLICY](../sql-reference/sql/create-masking-policy)

  * [CREATE PIPE](../sql-reference/sql/create-pipe)

  * [CREATE ROW ACCESS POLICY](../sql-reference/sql/create-row-access-policy)

  * [CREATE SERVICE](../sql-reference/sql/create-service)

  * [CREATE SHARE](../sql-reference/sql/create-share)

  * [CREATE STAGE](../sql-reference/sql/create-stage)

  * [SHOW PROCEDURES](../sql-reference/sql/show-procedures)

All other operations are allowed.

### Who provides support for a reader account?¶

Because a reader account does not have a licensing agreement with Snowflake,
support services are not available to the general users in the account.
Instead, as the provider of the account, you field questions and requests from
users in the account and respond as appropriate.

If you are unable to directly answer their questions or resolve their
requests/issues, you can open a Snowflake Support ticket through the normal
channels (as outlined in your support agreement). Once a response has been
provided by Snowflake Support, you then communicate the information back to
the appropriate users in the reader account.

## Managing and creating reader accounts using the web interface¶

If you have the ACCOUNTADMIN role (or have a role that has been granted the
CREATE ACCOUNT privilege), you can use Snowsight or Classic Console to perform
most tasks related to creating and managing reader accounts.

### Using Snowsight¶

To create or manage reader accounts in Snowsight, do the following:

  1. Sign in to Snowsight.

  2. In the navigation menu, select Data Products » Private Sharing.

  3. Select the Reader accounts tab.

On this page, you can do the following:

  * Create a reader account by selecting \+ New.

  * Review existing reader accounts.

  * Drop a reader account by selecting … » Drop.

Note

By default, the total number of reader accounts a provider can create is 20.
If you reach the limit and require creating additional accounts, please
contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-
support).

If you dropped a reader account in order to create a new account without
exceeding this limit, you cannot create the new reader account for 7 days,
which is the retention period for deleted reader accounts.

### Using Classic Console¶

To create or manage reader accounts in Classic Console, use the Account
[![Account tab](../_images/ui-navigation-account-icon.svg)](../_images/ui-
navigation-account-icon.svg) page.

On this page, you can perform the following tasks:

  * Create a reader account.

  * Drop a reader account.

## DDL for reader accounts¶

To enable creating and managing reader accounts, Snowflake provides a first-
class object, MANAGED ACCOUNT, that supports the following DDL commands:

  * [CREATE MANAGED ACCOUNT](../sql-reference/sql/create-managed-account)

  * [DROP MANAGED ACCOUNT](../sql-reference/sql/drop-managed-account)

  * [SHOW MANAGED ACCOUNTS](../sql-reference/sql/show-managed-accounts)

## Enabling other roles to create and manage reader accounts¶

By default, only users with the ACCOUNTADMIN role can create reader accounts
and therefore, as the owner of the account, manage the accounts. To support
delegating these tasks to other users, the CREATE ACCOUNT global privilege can
be granted to other roles (system-defined or custom). Then, users with the
role can create reader accounts and perform all tasks associated with managing
the accounts created using the role.

For example, to grant the privilege to the SYSADMIN role:

>
>     USE ROLE ACCOUNTADMIN;
>  
>     GRANT CREATE ACCOUNT ON ACCOUNT TO ROLE SYSADMIN;
>  
>
> Copy

## Creating and managing reader accounts using SQL¶

In addition to using the web interface to manage and create reader accounts,
you can also use SQL.

### Creating a reader account¶

To create a reader account, use the ACCOUNTADMIN role (or a role granted the
CREATE ACCOUNT global privilege) and the [CREATE MANAGED ACCOUNT](../sql-
reference/sql/create-managed-account) command.

In the command, specify the identifier for the account and the user who will
serve as the administrator for the account. For example, use the following
syntax:

    
    
    USE ROLE ACCOUNTADMIN;
    
    CREATE MANAGED ACCOUNT <account_name>
        ADMIN_NAME = <username> , ADMIN_PASSWORD = '<password>' ,
        TYPE = READER;
    

Copy

After running the command, you see the account name and login URL for the
account:

    
    
    +-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | status                                                                                                                                                                            |
    |-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | {"accountName":"READER_ACCT1","accountLocator":"IIB88126","url":"https://myorg-reader_acct1.snowflakecomputing.com","accountLocatorUrl":"https://iib88126.snowflakecomputing.com"}|
    +-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    

Note:

  * By default, the total number of reader accounts a provider can create is 20. If you reach the limit and require creating additional accounts, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

If you dropped a reader account in order to create a new account without
exceeding this limit, you cannot create the new reader account for 7 days,
which is the retention period for deleted reader accounts.

  * The `url` is the preferred [account URL](organizations-connect.html#label-connecting-via-url) for the new reader account. The account locator is a legacy identifier for the account.

  * The reader account utilizes the same [Snowflake Edition](intro-editions) as the provider account and is created in the same [region](intro-regions).

Important

After creating a reader account, wait for up to five minutes to ensure that
the account is fully provisioned. Then, you must perform the following
additional tasks before the account is ready to use:

  1. [Add the account to one or more shares](data-sharing-provider.html#label-share-create) so that the Snowflake objects in the shares can be shared with the account.

  2. [Configure the account](data-sharing-reader-config).

### Dropping a reader account¶

To drop a reader account, use the [DROP MANAGED ACCOUNT](../sql-
reference/sql/drop-managed-account) command. For example:

>
>     USE ROLE ACCOUNTADMIN;
>  
>     DROP MANAGED ACCOUNT reader_acct1;
>  
>
> Copy

Attention

Dropping a reader account drops all the objects created in the account and
immediately restricts all access to the account. It also removes the account
from your total number of reader accounts.

This operation can not be undone. Before you drop a reader account, please
take this into consideration.

### Viewing reader accounts¶

To view all the reader accounts that have been created for your account, use
the [SHOW MANAGED ACCOUNTS](../sql-reference/sql/show-managed-accounts)
command. For example:

>
>     USE ROLE ACCOUNTADMIN;
>  
>     SHOW MANAGED ACCOUNTS;
>  
>
> Copy

This command can be used to monitor the total number of reader accounts for
your account. If the total number reaches the limit (20), you may need to drop
some accounts or contact [Snowflake Support](https://docs.snowflake.com/user-
guide/contacting-support) to request the limit be increased.

In addition, you can use the views in the READER_ACCOUNT_USAGE schema (in the
SNOWFLAKE shared database) to query information about the reader accounts
created for your account. For more details, see [Account Usage](../sql-
reference/account-usage).

## Redirecting client connections in case of failover¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Business Critical
Feature](intro-editions)

Client Redirect requires Business Critical (or higher). To inquire about
upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-
guide/contacting-support).

In the event of an outage in a region, you can use [Client Redirect](client-
redirect) to provide continued access to data consumers using reader accounts.
Create two reader accounts in different regions and designate one to act as
the primary connection. In the event of an outage in a region, you can
redirect client connections to the reader account in another region. For more
information, see [Configuring Client Redirect and reader accounts](client-
redirect.html#label-client-redirect-reader-accounts).

