# Tutorial: Create and manage an organizational listing¶

Organizational listings in Snowflake allow you to share data products securely
within your organization, making it easier for internal teams to discover and
use trusted resources. As a provider, you can create listings that centralize
access to datasets, Native Apps, and other resources, simplifying data sharing
and collaboration across your teams. This guide will help you understand the
steps and requirements to create and manage organizational listings
effectively, ensuring that your data products are accessible while maintaining
control over who can see and use them.

Before you begin, make sure you have the necessary privileges to create and
manage organizational listings.

In this tutorial, we create a custom role (ORG_LISTING_PROVIDER) to manage
listings on behalf of the organization.

## Create a role to manage organizational listings¶

Switch to the ORGADMIN role (or ACCOUNTADMIN) to create a new role and add one
or more users. These users will be the administrators for organizational
listings. Then GRANT the new role the required privileges to create and share
organizational listings.

    
    
    USE ROLE ACCOUNTADMIN;
    CREATE ROLE ORG_LISTING_PROVIDER;
    GRANT ROLE ORG_LISTING_PROVIDER TO USER <user_name>;
    GRANT CREATE SHARE ON ACCOUNT TO ROLE ORG_LISTING_PROVIDER;
    

Copy

## Create a share and grant usage to it¶

Switch to the ORG_LISTING_PROVIDER custom role that you just created to create
a share and grant usage to the share.

    
    
    USE ROLE ORG_LISTING_PROVIDER;
    CREATE OR REPLACE DATABASE DEVORGDB;
    USE DATABASE DEVORGDB;
    CREATE SHARE ORG_SHARE SECURE_OBJECTS_ONLY=FALSE;
    GRANT USAGE ON DATABASE DEVORGDB TO SHARE ORG_SHARE;
    GRANT USAGE ON SCHEMA PUBLIC TO SHARE ORG_SHARE;
    CREATE OR REPLACE TABLE TUTORIAL_TABLE ( item_id INT, item_name STRING );
    GRANT SELECT ON TABLE DEVORGDB.PUBLIC.TUTORIAL_TABLE TO SHARE ORG_SHARE;
    INSERT INTO TUTORIAL_TABLE (item_id, item_name) VALUES (1,'Tutorial table');
    

Copy

## Create an organizational listing¶

Create an organizational listings from the share with the required attributes
included in YAML (entered in $$ delimiters).

This example shares the listing with all accounts in the organization:

    
    
    USE ROLE ORG_LISTING_PROVIDER;
    CREATE ORGANIZATION LISTING ORG_LISTING
    SHARE ORG_SHARE AS
    $$
    title : 'My title'
    organization_profile: INTERNAL
    organization_targets:
        access:
        - all_accounts : false 
    locations:
      access_regions:
      - name: "ALL"
    auto_fulfillment:
      refresh_type: "SUB_DATABASE"
      refresh_schedule: "10 MINUTE"
    $$;
    

Copy

## Alter an organizational listing¶

Alter the organizational listings by including any changes or additional
attributes in the YAML.

This example shares the listing one account only. It also adds a description
to the listing:

    
    
    USE ROLE ORG_LISTING_PROVIDER;
    ALTER LISTING ORG_LISTING
    AS
    $$
    title : 'My title'
    organization_profile: INTERNAL
    organization_targets:
        access:
        - all_accounts : false 
    locations:
      access_regions:
      - name: "ALL"
    auto_fulfillment:
      refresh_type: "SUB_DATABASE"
      refresh_schedule: "10 MINUTE"
    $$;
    

Copy

## View a list of organizational listings¶

To view organizational listings, run the following command:

    
    
    SHOW LISTINGS;
    DESCRIBE LISTING ORG_LISTING;
    

Copy

## (Optional) Add auto-fulfillment for organizational listings¶

To enable auto-fulfillment for your organizational listings, run the following
commands:

Important

Before you run the command to enable auto-fulfillment, check to see if it’s
already enabled and note the current settings. If it’s already turned on, you
don’t need to run the command.

    
    
    USE ROLE ACCOUNTADMIN;
    GRANT MANAGE LISTING AUTO FULFILLMENT ON ACCOUNT TO ROLE ORG_LISTING_PROVIDER;
    
    USE ROLE ORG_LISTING_PROVIDER;
    SHOW ORGANIZATION ACCOUNTS;
    SELECT SYSTEM$IS_GLOBAL_DATA_SHARING_ENABLED_FOR_ACCOUNT('<ORGACCOUNT>');
    
    CALL SYSTEM$ENABLE_GLOBAL_DATA_SHARING_FOR_ACCOUNT('<ORGACCOUNT>');
    

Copy

## Clean up after the tutorial¶

To drop any unwanted objects you created during this tutorial, run one or more
of the following commands as needed:

Important

If auto-fulfillment was enabled when you ran the last step, DO NOT disable it
when you clean up after the query. Doing so will stop all auto-fulfillment on
your account!

    
    
    DROP LISTING <organizational_listing_name>;
    DROP SHARE org_listing1_share1;
    DROP DATABASE org_listing_db1;
    --CALL SYSTEM$DISABLE_GLOBAL_DATA_SHARING_FOR_ACCOUNT('ORGACCOUNT');
    DROP ROLE ORG_LISTING_PROVIDER;
    

Copy

