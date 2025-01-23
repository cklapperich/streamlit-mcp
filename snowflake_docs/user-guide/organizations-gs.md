# Getting started with organizations¶

This topic discusses how to work with organizations, including how to assign
the ORGADMIN role to organization administrators.

## Organization creation¶

Snowflake customers never directly create an organization. For users who sign-
up for a Snowflake account using the self-service option, an organization is
automatically created with a system-generated name when the account is
created. For entities who work directly with Snowflake personnel to set up
accounts, Snowflake creates the organization to which the accounts belong
using a custom name. In either case, users can create additional accounts that
belong to the organization after it is created with the initial account.

## Viewing the name of your organization and its accounts¶

If you are the organization administrator, you can view the name of your
organization and its accounts through the web interface or using SQL:

> SQL:
>  
>
> Execute a [SHOW ACCOUNTS](../sql-reference/sql/show-accounts) command.
>
> [Snowsight](ui-snowsight):
>  
>
> Select Admin » Accounts. The organization name is listed above the account
> names.

Users with any role, not just ORGADMIN, can execute the
[CURRENT_ORGANIZATION_NAME](../sql-
reference/functions/current_organization_name) function to return the
organization of the current account.

Users with any role can also find the organization name and account name for a
specific account that they have previously signed in to. See [Finding the
organization and account name for an account](admin-account-
identifier.html#label-account-name-find).

## Changing the name of your organization¶

If you want to change the name of an organization, for example to change a
system-generated name to a more user-friendly one, contact [Snowflake
Support](https://docs.snowflake.com/user-guide/contacting-support).

When you contact Snowflake Support, you must decide whether users can
temporarily access accounts in the organization using the original [account
URL](organizations-connect.html#label-connecting-via-url). If you keep the
original account URL, it is automatically dropped after 90 days, at which time
users must use the new account URL to access the account. If you want to drop
the account URL before the 90 days expire, see [Deleting an organization
URL](organizations-manage-accounts-urls.html#label-drop-org-access-url).

## Deleting an organization¶

To delete your Snowflake organization:

  1. Use an ORGADMIN-enabled account to [delete all accounts in the organization](organizations-manage-accounts-delete), except the account being used for the deletion.

  2. Contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) to delete the last account and the organization.

## Enabling the ORGADMIN role in an account¶

An organization administrator uses an account with the ORGADMIN role enabled
to work with data and features that pertain to all accounts in the
organization. Once the ORGADMIN role is enabled, the organization
administrator can log in to the account and use the role to perform
organization-focused tasks like listing all accounts in the organization and
creating new accounts.

Every organization has at least one account with the ORGADMIN role enabled.
The organization administrator can use the [ALTER ACCOUNT … SET
IS_ORG_ADMIN](../sql-reference/sql/alter-account) command to enable the role
in additional accounts.

For example, to enable the ORGADMIN role for existing account `my_account1`,
the organization administrator can execute the following command from an
account that already has the ORGADMIN role enabled:

    
    
    USE ROLE orgadmin;
    
    ALTER ACCOUNT my_account1 SET IS_ORG_ADMIN = TRUE;
    

Copy

Keep the following in mind when enabling the ORGADMIN role:

  * The ALTER ACCOUNT syntax only accepts the [account name format](admin-account-identifier.html#label-account-name) of the account identifier. You cannot use the account locator to specify the account.

  * By default, the ORGADMIN role can be enabled in a maximum of 8 accounts. If your organization requires more accounts with the ORGADMIN role, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

  * The ORGADMIN role cannot be enabled for a [reader account](data-sharing-reader-create).

## Disabling the ORGADMIN role¶

An organization administrator can use the ALTER ACCOUNT command to remove the
ORGADMIN role from an account by setting the IS_ORG_ADMIN property to `FALSE`.
For example:

    
    
    ALTER ACCOUNT my_account1 SET IS_ORG_ADMIN = FALSE;
    

Copy

Tip

The ORGADMIN role cannot be removed for the current account. As a workaround,
enable the role in a different account, and then switch to that account before
executing the ALTER ACCOUNT command.

## Assigning the ORGADMIN role to a user or role¶

Once enabled in an account, the ORGADMIN role can be granted to any user or
role in the account by an ACCOUNTADMIN using the [GRANT ROLE](../sql-
reference/sql/grant-role) command. For more information about system roles and
best practices for managing access control, see [Access control
considerations](security-access-control-considerations).

### Examples¶

    
    
    -- Assume the ACCOUNTADMIN role
    USE ROLE accountadmin;
    
    -- Grant the ORGADMIN role to a user
    GRANT ROLE orgadmin TO USER user1;
    
    -- Grant ORGADMIN to a role
    GRANT ROLE orgadmin TO ROLE custom_role;
    

Copy

