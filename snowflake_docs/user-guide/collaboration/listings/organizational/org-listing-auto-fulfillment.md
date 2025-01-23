# Configure organizational listings for auto-fulfillment¶

Auto-fulfillment ensures that data products in organizational listings are
propagated across regions automatically, eliminating the need for manual
replication. This mechanism provides seamless regional availability for data
consumers, enhancing consistency and reducing administrative overhead in
multi-region data environments.

Before you begin, make sure you have the necessary privileges to manage auto-
fulfillment settings for organizational listing.

If your organization spans multiple regions, you can enable auto-fulfillment
for your organizational listings to ensure that data products are available in
all regions where your organization has a presence. Auto-fulfillment happens
automatically if it’s enabled for your organization.

To find your account name (`account_name`), run this command:

    
    
    SHOW ACCOUNTS;
    

Copy

To check if global data sharing is enabled for your organization account, run
this command:

    
    
    SELECT SYSTEM$IS_GLOBAL_DATA_SHARING_ENABLED_FOR_ACCOUNT('<account_name>');
    

Copy

To enable global data sharing for an organization account, run this command:

    
    
    CALL SYSTEM$ENABLE_GLOBAL_DATA_SHARING_FOR_ACCOUNT('<account_name>');
    

Copy

To disable global data sharing for an organization account, run this command:

    
    
    CALL SYSTEM$DISABLE_GLOBAL_DATA_SHARING_FOR_ACCOUNT('<account_name>');
    

Copy

