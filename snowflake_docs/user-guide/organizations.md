# Introduction to organizations¶

An _organization_ is a first-class Snowflake object that links the accounts
owned by your business entity. Organizations simplify account management and
billing, [Replication and Failover/Failback](replication-intro), Snowflake
Secure Data Sharing, and other account administration tasks.

This feature allows organization administrators to view, create, and manage
all of your accounts across different regions and cloud platforms.

## Types of accounts¶

  * Regular Snowflake account

  * Organization account: Special account used by organization administrators to manage multi-account organizations and to access usage data from premium views in the ORGANIZATION_USAGE schema. For more information, see [Organization accounts](organization-accounts).

  * Snowflake Open Catalog account: Special account used by service admins and catalog admins to manage catalogs defined in Snowflake Open Catalog. For more information, see [Snowflake Open Catalog overview](https://other-docs.snowflake.com/en/opencatalog/overview).

Note

The introduction of the organization account for multi-account organizations
changes the way that organization administrators manage an organization and
its accounts. For more information, see [Organization accounts](organization-
accounts).

## Benefits¶

  * A central view of all accounts within your organization. For more information, refer to [Viewing accounts in your organization](organizations-manage-accounts-view).

  * Self-service account creation. For more information, refer to [Creating an account](organizations-manage-accounts-create).

  * Data availability and durability by leveraging data replication and failover. For more information, see [Introduction to replication and failover across multiple accounts](account-replication-intro).

  * Seamless data sharing with Snowflake consumers across regions. For more information, see [Share data securely across regions and cloud platforms](secure-data-sharing-across-regions-platforms).

  * Ability to monitor and understand usage across all accounts in the organization. For more information, see [Organization Usage](../sql-reference/organization-usage) views.

## ORGADMIN role¶

The organization administrator (ORGADMIN) system role is responsible for
managing operations at the organization level.

Note

If you are using an [organization account](organization-accounts) to manage a
multi-account organization, the administrator’s role is GLOBALORGADMIN.

A user with the ORGADMIN role can perform the following actions:

  * Create an account in the organization. For more information, refer to [Creating an account](organizations-manage-accounts-create).

  * View/show all accounts within the organization. For more information, refer to [Viewing accounts in your organization](organizations-manage-accounts-view).

  * View/show a list of regions enabled for the organization. For more information, see [Viewing a List of Regions Available for an Organization](intro-regions.html#label-show-organization-regions).

  * View usage information for all accounts in the organization. For more information, see [Organization Usage](../sql-reference/organization-usage).

  * Enable [replication](account-replication-intro) for an account in the organization. For more information, see [Prerequisite: Enable replication for accounts in the organization](account-replication-config.html#label-enabling-accounts-for-replication).

Note

After an account is created, ORGADMIN can view the account properties but does
not have access to the account data.

For information about working with the ORGADMIN role, see [Enabling the
ORGADMIN role in an account](organizations-gs.html#label-enabling-orgadmin-
role-for-account).

## Organization DDL¶

To help manage organizations, including creating and listing accounts in the
organization, Snowflake provides the following set of special DDL commands:

  * [CREATE ACCOUNT](../sql-reference/sql/create-account)

  * [DROP ACCOUNT](../sql-reference/sql/drop-account)

  * [SHOW ACCOUNTS](../sql-reference/sql/show-accounts)

  * [UNDROP ACCOUNT](../sql-reference/sql/undrop-account)

## Organization functions and views¶

Snowflake provides historical usage data for all accounts in your organization
via views in the ORGANIZATION_USAGE schema in a shared database named
SNOWFLAKE. For information, see [Organization Usage](../sql-
reference/organization-usage).

To enable database replication for an account in the organization, Snowflake
provides the [SYSTEM$GLOBAL_ACCOUNT_SET_PARAMETER](../sql-
reference/functions/system_global_account_set_parameter) function.

