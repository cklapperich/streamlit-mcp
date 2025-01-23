# Configure organizational listings¶

This page introduces configurations for organizational listings in Snowflake.
You’ll find details on targeting accounts, adding roles, access regions, and
auto-fulfillment settings.

## Set the Uniform Listing Locator or listing name¶

The Uniform Listing Locator (ULL) is a unique identifier that represents the
listing and its data product, treating them as one. The listing name is
different from the title of the listing: multiple listings can have the same
title, but each listing must have a unique listing name or ULL. The complete
ULL is formed by three elements delimited by the symbol ‘$’. The first element
is the provider’s organization name, the second element is the provider
profile `INTERNAL`, and the third element is the listing name. The ULL cannot
be changed after the listing is published. Although it has three parts, the
ULL is treated as a single name in queries. For example, you can query a table
in a listing like this:

    
    
    SELECT * FROM "ORGDATACLOUD$INTERNAL$MY_LISTING_NAME_123".PUBLIC.TABLE_FROM_LISTING;
    

Copy

When creating a listing, give it a clear, descriptive name. Consumers can find
listings faster by name rather than title, and a descriptive name is easier to
use in queries.

## Set who can discover and access an organizational listing¶

The target audience of your organizational listings is always your internal
marketplace.

Despite the restriction of an internal listing, you can still control who can
discover and access the listing. You can mark a listing discoverable and
accessibly individually. That is you may be able to discover an listing but
not access it.

In general you can specify access or discovery at the following levels:

  * Everyone in your account

  * Specific accounts

  * Specific accounts, but limited by specific roles

For example the `access` element defines who can access a listing. Likewise,
the `discovery` element defines who can discover a listing.

Allow all accounts to access the listing.

    
    
    organization_targets:
       access:
       - all_accounts : true
    

Copy

Allow specific accounts to access the listing.

    
    
    organization_targets:
       access:
       - account: 'Account1'
       - account: 'Account2'
    

Copy

Allow specific accounts to access the listing, but only for the given roles.

    
    
    organization_targets:
       access:
          - account: 'Account1'
             roles: [<role1>, <role2>, <role3>]
    

Copy

Allow all accounts to discover the listing.

    
    
    organization_targets:
       discovery:
       - all_accounts : true
    

Copy

Allow specific accounts to discover the listing.

    
    
    organization_targets:
       discovery:
       - account: 'Account1'
       - account: 'Account2'
    

Copy

Allow specific accounts to discover the listing, but only for the given roles.

    
    
    organization_targets:
       discovery:
          - account: 'Account1'
             roles: [<role1>, <role2>, <role3>]
    

Copy

In a similar way, regions are set up the access regions_attribute:

    
    
    locations:
      access_regions:
         - name: "ALL"
    

Copy

    
    
    locations:
       access_regions:
         - name: "AWS_US_WEST_2"
         - name: "AZURE_CENTRALINDIAUS-EAST"
    

Copy

## Specify approver and support contact¶

Optionally, you can specify an email address or link to internal ticketing
system for both approver and support contact.

    
    
    support_contact: "support@somedomain.com"
    approver_contact: "approver@somedomain.com"
    

Copy

## Set auto-fulfillment options for an organizational listing¶

Organizational listings that have attached data shares and apps both use auto-
fulfillment, however they each use different methods. For this reason, the
refresh schedules for each are different. For shares, the refresh schedule is
set on the database level. For apps, it’s set on the account level.

If you need to use auto-fulfillment, you can set it when your run `CREATE
ORGANIZATIONAL LISTING` OR `ALTER LISTING` by changing the auto_fulfillment
attribute in the [listing manifest fields](https://other-
docs.snowflake.com/en/sql-reference/sql/create-listing#parameters).

    
    
    auto_fulfillment:
       refresh_type: SUB_DATABASE
       refresh_schedule: '10 MINUTE'
    

Copy

