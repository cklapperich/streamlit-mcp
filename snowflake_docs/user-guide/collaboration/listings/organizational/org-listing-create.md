# Create an organizational listing¶

Before you create an organizational listing, make sure you review the
prerequisites, known limitations, and considerations.

## Prerequisites¶

  * You have access to the ORGADMIN role ([Organization accounts](../../../organization-accounts) are optional).

  * Your organization administrator (ORGADMIN) has signed the terms for listings.

## Known limitations¶

  * This feature is not available in government regions.

  * You must use the API to target specific regions.

  * Data products supported: Snowflake Native App Framework and shares.

  * The following features are not supported when using organizational listings:

    * Custom creation of profiles.

    * Marketplace analytics.

    * Reader accounts.

## Considerations¶

  * Before you target an entire organization, check for external tenants. Adjust the target accounts for your data products before adding them to an organizational listing unless you intend to share with external tenants.

  * Each share can be attached to one listing.

  * Each Native App can be attached to one or more listings.

  * For organization changes (such as mergers) with accounts containing organization listings, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## Access control requirements¶

Use the information provided here to determine the specific roles and
privileges that you must have to execute organizational listing SQL commands.

### CREATE ORGANIZATION LISTING¶

A [role](../../../security-access-control-overview.html#label-access-control-
overview-roles) used to execute this SQL command must have the following
[privileges](../../../security-access-control-overview.html#label-access-
control-overview-privileges) at a minimum:

Privilege | Object | Notes  
---|---|---  
CREATE ORGANIZATION LISTING | ACCOUNT | To create and alter organizational listings.  
  
A [role](../../../security-access-control-overview.html#label-access-control-
overview-roles) used to execute this SQL command must have at least one of the
following [privileges](../../../security-access-control-overview.html#label-
access-control-overview-privileges) at a minimum:

Privilege | Object | Notes  
---|---|---  
USAGE | SHARE | To attach the specified share to a listing.  
USAGE | APPLICATION | To attach the specified Snowflake Native App Framework to a listing.  
  
### MANAGE LISTING AUTO FULFILLMENT¶

A [role](../../../security-access-control-overview.html#label-access-control-
overview-roles) used to execute this SQL command must have the following
[privileges](../../../security-access-control-overview.html#label-access-
control-overview-privileges) at a minimum:

Privilege | Object | Notes  
---|---|---  
MANAGE LISTING AUTO FULFILLMENT | ACCOUNT | To configure the auto-fulfillment settings.  
  
### Share creation and management¶

To create and manage objects inside a share, and to create the share itself, a
role should have privileges on relevant data objects, schemas, and the CREATE
SHARE command.

Privilege | Object | Notes  
---|---|---  
CREATE SHARE | ACCOUNT | To `CREATE` a share.  
USAGE | DATABASE | To see and `USE` the specified database.  
USAGE | SCHEMA | To see the specified schema.  
SELECT | SCHEMA | To query specified tables in the specified schema.  
CREATE | SCHEMA | To `CREATE` tables or views in the specified schema.  
MODIFY | SCHEMA | To `ALTER` tables or views in the specified schema.  
  
The USAGE privilege on the parent database and schema are required to perform
operations on any object in a schema.

For instructions on creating a custom role with a specified set of privileges,
see [Creating custom roles](../../../security-access-control-
configure.html#label-security-custom-role).

For general information about roles and privilege grants for performing SQL
actions on [securable objects](../../../security-access-control-
overview.html#label-access-control-securable-objects), see [Overview of Access
Control](../../../security-access-control-overview).

## Create an organizational listing¶

SnowsightSQL

>   1. Create an organizational listing.
>
>     1. Sign in to [Snowsight](../../../ui-snowsight).
>
>     2. Select Data Products » Provider Studio in the left-side navigation
> menu.
>
>     3. Click \+ Listing » Internal Marketplace.
>
>     4. Click \+ Data Product.
>
>     5. In the \+ Data Product dialog, click \+ Select.
>
>     6. Navigate to a data product such as a table, a view or other data
> product.
>
> Alternatively, search for and choose a data product to share.
>
>     7. Select Done when complete.
>
>     8. Select Save.
>
>   2. Specify who can access the listing (the target accounts, roles, and
> regions).
>
>     1. Click \+ Access Control. The Access and discovery dialog displays.
>
>     2. In the Grant access section, enter values for the following:
>
> Field | Description  
> ---|---  
> Who can access this data product? | Select one of:
>        * Entire organization Anyone in the organization can access the
> listing.
>        * Selected accounts and roles Only selected accounts and roles can
> access.
>        * No accounts or roles are pre-approved (Default) Data product will
> only be available by request.  
> Accounts | If Select accounts and roles is selected, select one or more accounts. Click \+ Add another account to add second and subsequent accounts.  
> Selected user roles | If Selected roles is selected, enter one or more roles to grant access.  
>     3. In the Allow discovery section, enter values for the following:
>
> [![Snowflake logo in black \(no text\)](../../../../_images/logo-snowflake-
> black.png)](../../../../_images/logo-snowflake-black.png) [Preview
> Feature](../../../../release-notes/preview-features) — Open
>
> `discovery` is a preview feature and is available to all accounts.
>
> Field | Description  
> ---|---  
> Who else can discover the listing and request access? | Select one of:
>        * Entire organization (Default) Anyone in the organization can
> discover listing and request access.
>        * Selected accounts and roles Only selected accounts and roles can
> discover listing and request access.
>        * Not discoverable by users without access Only users with access can
> discover this listing.  
> Accounts | If Select accounts and roles is selected, select one or more accounts. Click \+ Add another account to add second and subsequent accounts.  
> Selected user roles | If Selected roles is selected, enter one or more roles to grant access.  
>     4. In the Request approval section, enter the email address of the
> request approver or link to the internal ticketing system.
>
>

  3. Provide a title and Uniform Listing Locator (ULL).

Changing a listings title is optional but recommended. See [Uniform Listing
Locator](org-listing-configure.html#label-olisting-im-ull) for more
information.

    1. Select Untitled Listing.

    2. For Listing title, enter a descriptive title for your data product.

    3. Select Save or Cancel.

  4. Complete the listing.

Enter addition information about listing page to guide consumers, such as
description, data dictionary, usage examples and more.

Note that Support Contact is required

    1. Click Publish to make the listing available in the Internal Marketplace. If you exit without publishing, the listing is saved as a draft, ready for review or the addition of descriptive metadata.

Create an organizational listing from the share with the required attributes
included in YAML (entered in $$ delimiters).

This part of the manifest yaml specifies the accounts that will be able to use
the organizational listing:

    
    
    organization_targets:
      access:
    

Copy

This example creates a listing using the required settings in the manifest
YAML. It targets one role in one account in one region and includes support
and approver contacts:

Note

`support_contact` is required. `approver_contact` is required if a `discovery`
target is provided.

    
    
    USE ROLE <organizational_listing_role>;
    
    CREATE ORGANIZATION LISTING <organizational_listing_name>
    SHARE <share_name> AS
    $$
    title: "My title"
    description: "One region, all accounts"
    organization_profile: "INTERNAL"
    organization_targets:
      discovery:
      - account: "<account_name>"
        roles:
        - "<role>"
    
      access:
      - account: "<account_name>"
        roles:
        - "<role>"
    
    support_contact: "support@somedomain.com"
    approver_contact: "approver@somedomain.com"
    locations:
      access_regions:
      - name: "PUBLIC.<snowflake_region>"
    $$;
    

Copy

For additional examples see [Set who can discover and access an organizational
listing](org-listing-configure.html#label-organizational-listing-discovery-
and-access).

