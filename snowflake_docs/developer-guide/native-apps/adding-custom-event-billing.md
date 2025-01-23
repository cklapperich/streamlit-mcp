# Add billable events to an application package¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) Feature — Generally
Available

The Snowflake Native App Framework is generally available on supported cloud
platforms. For additional information, see [Support for private connectivity,
VPS, and government regions](limitations.html#label-native-apps-supported-
clouds).

When you use Custom Event Billing for a Snowflake Native App, you can charge
for specific types of application usage in addition to the existing usage-
based pricing plans. To set it up, you must perform two high-level steps:

  1. Set up your application package to emit billable events by following the steps in this topic.

  2. [Select a usage-based pricing plan with billable events](https://other-docs.snowflake.com/en/collaboration/provider-listings-pricing-model) for the listing you use to publish your Snowflake Native App to consumers.

This topic describes how to set up your application package to emit billable
events using the [SYSTEM$CREATE_BILLING_EVENT](../../sql-
reference/functions/system_create_billing_event) and
[SYSTEM$CREATE_BILLING_EVENTS](../../sql-
reference/functions/system_create_billing_events) system functions.

## Overview of billable events in an application package¶

You can set up your application package to emit billable events in response to
specific usage events so that you can charge consumers based on how much they
use your Snowflake Native App.

For example, you can add a billable event to charge a consumer a specific
amount for each call to a stored procedure in your Snowflake Native App.

To add billable events to an application package, do the following:

  1. Create stored procedures to define which usage events trigger calls to the [SYSTEM$CREATE_BILLING_EVENT](../../sql-reference/functions/system_create_billing_event) and [SYSTEM$CREATE_BILLING_EVENTS](../../sql-reference/functions/system_create_billing_events) system functions.

Note

You cannot test the output of the system function at this stage. This system
function can only be called from a Snowflake Native App installed in a
consumer account.

  2. Add those stored procedures to the setup script of the application package.

Important

Snowflake supports billable events that are emitted by calling the system
function within a stored procedure in the application, as outlined by the
examples in this topic.

Snowflake does not support other methods of calculating the base charge for
billable events, such as methods that use the output of a table or user-
defined function that outputs consumer activity or methods that use telemetry
logged in an event table.

If you’re uncertain whether a proposed implementation will be supported,
contact your Snowflake account representative.

## Billable event examples¶

The examples in this section show how to create stored procedures to emit
billable events for common billing scenarios. Each of these examples calls the
`createBillingEvent` function.

### Call the SYSTEM$CREATE_BILLING_EVENT system function¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) [Preview
Feature](../../release-notes/preview-features) — Open

Available to all accounts.

The following example shows how to create a wrapper function in a stored
procedure to call the [SYSTEM$CREATE_BILLING_EVENT](../../sql-
reference/functions/system_create_billing_event) system function.

Note

You can call this system function in a stored procedure written in JavaScript,
Python, or Java.

This example creates a JavaScript stored procedure named
`custom_event_billing` in the schema version that is accessible to the
procedures that emit billing. The stored procedure creates a helper function
called `createBillingEvent` which takes arguments that correspond to the typed
parameters expected by the SYSTEM$CREATE_BILLING_EVENT system function.

For more details about the parameters and the required types, see
[SYSTEM$CREATE_BILLING_EVENT](../../sql-
reference/functions/system_create_billing_event).

    
    
     CREATE OR REPLACE PROCEDURE <schema_name>.custom_event_billing()
     RETURNS NULL
     LANGUAGE JAVASCRIPT
     AS
     $$
       /**
        * Helper method to add a billable event
        * Format timestamps as Unix timestamps in milliseconds
        */
    
       function createBillingEvent(className, subclassName, startTimestampVal, timestampVal, baseCharge, objects, additionalInfo) {
            try {
                var res = snowflake.createStatement({
                sqlText: `SELECT SYSTEM$CREATE_BILLING_EVENT('${className}',
                                                          '${subclassName}',
                                                          ${startTimestampVal},
                                                          ${timestampVal},
                                                          ${baseCharge},
                                                          '${objects}',
                                                          '${additionalInfo}')`
                }).execute();
    
                res.next();
    
                return res.getColumnValue(1);
            } catch(err) {
                return err.message;
            }
        }
    $$;
    

Copy

The examples in this topic call this helper function.

### Batch multiple billing events with the SYSTEM$CREATE_BILLING_EVENTS system
function¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) [Preview
Feature](../../release-notes/preview-features) — Open

Available to all accounts.

The following example stored procedure shows how to batch multiple Snowflake
Native App billing events with the SYSTEM$CREATE_BILLING_EVENTS system
function. By using batches, you save time, reduce the likelihood of exceeding
call limits, and ensure your billing events are set up correctly.

For more details about the parameters and the required types, see
[SYSTEM$CREATE_BILLING_EVENTS](../../sql-
reference/functions/system_create_billing_events).

    
    
     CREATE OR REPLACE PROCEDURE <app_provider_db_1><app_provider_schema_1>.external_proc_batch()
     RETURNS STRING
     LANGUAGE JAVASCRIPT
     EXECUTE AS OWNER
     AS
     $$
       function createBillingEventsBulk(events) {
         try {
           var res = snowflake.execute({
                        sqlText: `call SYSTEM$CREATE_BILLING_EVENTS('${events}')`
                     });
           res.next();
           return res.getColumnValueAsString(1);
         } catch (err) {
           return err.message;
         }
       }
    
       return createBillingEventsBulk(`
                                       [
                                         {
                                           "class": "class_1",
                                           "subclass": "subclass_1",
                                           "start_timestamp": ${Date.now()},
                                           "timestamp": ${Date.now()},
                                           "base_charge": 6.1,
                                           "objects": "obj1",
                                           "additional_info": "info1"
                                         },
                                         {
                                           "class": "class_2",
                                           "subclass": "subclass_2",
                                           "start_timestamp": ${Date.now()},
                                           "timestamp": ${Date.now()},
                                           "base_charge": 9.1,
                                           "objects": "obj2",
                                           "additional_info": "info2"
                                         }
                                       ]
                                     `);
    $$;
    

Copy

### Example: Billing based on calls to a stored procedure¶

The following example shows how to create a stored procedure to emit a
billable event when a consumer calls that stored procedure in a Snowflake
Native App.

Add this example code to your setup script in the same stored procedure that
defines the helper function:

    
    
    ...
      //
      // Send a billable event when a stored procedure is called.
      //
      var event_ts = Date.now();
      var billing_quantity = 1.0;
      var base_charge = billing_quantity;
      var objects = "[ \"db_1.public.procedure_1\" ]";
      var retVal = createBillingEvent("PROCEDURE_CALL", "", event_ts, event_ts, base_charge, objects, "");
      // Run the rest of the procedure ...
    $$;
    

Copy

This example code creates a stored procedure that calls the
`createBillingEvent` function to emit a billable event with the class name
`PROCEDURE_CALL` and a base charge of `1.0`.

Note

The types of the arguments passed to the `createBillingEvent` function must
correspond to the typed parameters expected by the
[SYSTEM$CREATE_BILLING_EVENT](../../sql-
reference/functions/system_create_billing_event) system function.

### Example: Billing based on rows consumed by a Snowflake Native App¶

The following example shows how to create a stored procedure to emit a
billable event based on the number of rows consumed within a table in the
consumer account.

Add this example code to your setup script in the same stored procedure that
defines the helper function:

    
    
    ...
      // Run a query and get the number of rows in the result
      var select_query = "select i from db_1.public.t1";
      res = snowflake.execute ({sqlText: select_query});
      res.next();
      //
      // Send a billable event for rows returned from the select query
      //
      var event_ts = Date.now();
      var billing_quantity = 2.5;
      var base_charge = res.getRowcount() * billing_quantity;
      var objects = "[ \"db_1.public.t1\" ]";
      createBillingEvent("ROWS_CONSUMED", "", event_ts, event_ts, base_charge, objects, "");
      // Run the rest of the procedure ...
    $$;
    

Copy

This example code creates a stored procedure that calls the
`createBillingEvent` function to emit a billable event with the class name
`ROWS_CONSUMED` and a calculated base charge of `2.5` multiplied by the number
of rows in the `db_1.public.t1` table in the consumer account.

Note

The types of the arguments passed to the `createBillingEvent` function must
correspond to the typed parameters expected by the
[SYSTEM$CREATE_BILLING_EVENT](../../sql-
reference/functions/system_create_billing_event) system function.

### Example: Billing based on the number of rows ingested¶

The following example shows how to create a stored procedure to emit a
billable event based on the number of rows ingested into a table.

Add this example code to your setup script in the same stored procedure that
defines the helper function:

    
    
    ...
        // Run the merge query
        var merge_query = "MERGE INTO target_table USING source_table ON target_table.i = source_table.i
            WHEN MATCHED THEN UPDATE SET target_table.j = source_table.j
            WHEN NOT MATCHED
            THEN INSERT (i, j)
            VALUES (source_table.i, source_table.j)";
        res = snowflake.execute ({sqlText: merge_query});
        res.next();
        // rows ingested = rows inserted + rows updated
        var numRowsIngested = res.getColumnValue(1) + res.getColumnValue(2);
    
        //
        // Send a billable event for rows changed by the merge query
        //
        var event_ts = Date.now();
        var billing_quantity = 2.5;
        var base_charge = numRowsIngested * billing_quantity;
        var objects = "[ \"db_1.public.target_table\" ]";
        createBillingEvent("ROWS_CHANGED", "", event_ts, event_ts, base_charge, objects, "");
        // Run the rest of the procedure ...
    $$;
    

Copy

This example code creates a stored procedure that calls the
`createBillingEvent` function to emit a billable event with the class name
`ROWS_CHANGED` and a calculated base charge of `2.5` multiplied by the number
of rows ingested in the `db_1.target_table` table.

Note

The types of the arguments passed to the `createBillingEvent` function must
correspond to the typed parameters expected by the
[SYSTEM$CREATE_BILLING_EVENT](../../sql-
reference/functions/system_create_billing_event) system function.

### Example: Billing based on monthly active rows¶

Monthly active rows are the number of rows inserted or updated for the first
time within a calendar month. Some providers use this metric to only charge
consumers for unique rows updated in a month. You can modify this example to
instead count unique users, or identify a unique data load location to
determine a base charge.

The following example shows how to create a stored procedure to emit a
billable event based on the number of monthly active rows. Add this example
code to your setup script in the same stored procedure that defines the helper
function:

    
    
    ...
        //
        // Get monthly active rows
        //
        var monthly_active_rows_query = "
         SELECT
             count(*)
         FROM
             source_table
         WHERE
             source_table.i not in
             (
               SELECT
                 i
               FROM
                 target_table
               WHERE
                 updated_on >= DATE_TRUNC('MONTH', CURRENT_TIMESTAMP)
             )";
        res = snowflake.execute ({sqlText: monthly_active_rows_query});
        res.next();
        var monthlyActiveRows = parseInt(res.getColumnValue(1));
        //
        // Run the merge query and update the updated_on values for the rows
        //
        var merge_query = "
            MERGE INTO
                target_table
            USING
                source_table
            ON
                target_table.i = source_table.i
            WHEN MATCHED THEN
             UPDATE SET target_table.j = source_table.j
                        ,target_table.updated_on = current_timestamp
            WHEN NOT MATCHED THEN
                INSERT (i, j, updated_on) VALUES (source_table.i, source_table.j, current_timestamp)";
        res = snowflake.execute ({sqlText: merge_query});
        res.next();
        //
        // Emit a billable event for monthly active rows changed by the merge query
        //
        var event_ts = Date.now();
        var billing_quantity = 0.02
        var base_charge = monthlyActiveRows * billing_quantity;
        var objects = "[ \"db_1.public.target_table\" ]";
        createBillingEvent("MONTHLY_ACTIVE_ROWS", "", event_ts, event_ts, base_charge, objects, "");
        // Run the rest of the procedure ...
    $$;
    

Copy

This example code creates a stored procedure that determines the number of
monthly active rows using a merge query to identify unique rows. The example
then calculates the base charge using the value of the `monthlyActiveRows`
variable and the `billing_quantity`. The base charge is then passed to the
`createBillingEvent` function.

Note

The types of the arguments passed to the `createBillingEvent` function must
correspond to the typed parameters expected by the
[SYSTEM$CREATE_BILLING_EVENT](../../sql-
reference/functions/system_create_billing_event) system function.

In your setup script, add this stored procedure after the stored procedure
that calls the SYSTEM$CREATE_BILLING_EVENT system function.

### Snowpark Python example: Billing based on rows consumed¶

To write your stored procedure in Snowpark Python to bill based on rows
consumed by your Snowflake Native App, use the following example:

    
    
    CREATE OR REPLACE PROCEDURE app_schema.billing_event_rows()
       RETURNS STRING
       LANGUAGE PYTHON
       RUNTIME_VERSION = '3.9'
       PACKAGES = ('snowflake-snowpark-python')
       HANDLER = 'run'
       EXECUTE AS OWNER
       AS $$
    import time
    
    # Helper method that calls the system function for billing
    def createBillingEvent(session, class_name, subclass_name, start_timestamp, timestamp, base_charge, objects, additional_info):
       session.sql(f"SELECT SYSTEM$CREATE_BILLING_EVENT('{class_name}', '{subclass_name}', {start_timestamp}, {timestamp}, {base_charge}, '{objects}', '{additional_info}')").collect()
       return "Success"
    
    # Handler function for the stored procedure
    def run(session):
       # insert code to identify monthly active rows and calculate a charge
       try:
    
          # Run a query to select rows from a table
          query =  "select i from db_1.public.t1"
          res = session.sql(query).collect()
    
          # Define the price to charge per row
          billing_quantity = 2.5
    
          # Calculate the base charge based on number of rows in the result
          charge = len(res) * billing_quantity
    
          # Current time in Unix timestamp (epoch) time in milliseconds
          current_time_epoch = int(time.time() * 1000)
    
          return createBillingEvent(session, 'ROWS_CONSUMED', '', current_time_epoch, current_time_epoch, charge, '["billing_event_rows"]', '')
       except Exception as ex:
          return "Error " + ex
    $$;
    

Copy

This example code creates a stored procedure that defines a helper method that
calls the SYSTEM$CREATE_BILLING_EVENT system function, as well as a method
that calls that helper method, `createBillingEvent`, to emit a billable event
with the class name `ROWS_CONSUMED` and a base charge calculated by
multiplying a price of `2.5` US dollars by the number of rows in the
`db_1.public.t1` table in the consumer account.

Note

The types of the arguments passed to the `createBillingEvent` function must
correspond to the typed parameters expected by the
[SYSTEM$CREATE_BILLING_EVENT](../../sql-
reference/functions/system_create_billing_event) system function.

## Test custom event billing¶

To make sure that you set up Custom Event Billing properly and that billable
events are emitted for usage events as you expect, do the following:

  1. Update your application package:

    1. Update your setup script to include the stored procedures that emit billable events.

    2. Update your application package with the new setup script.

    3. Update the version and release directive for your application package.

  2. Share the application package with a consumer account in your organization that you have access to:

    1. [Create a private listing](https://other-docs.snowflake.com/en/collaboration/provider-listings-creating-publishing#label-listings-create).

    2. Add [Custom Event Billing as the pricing plan](https://other-docs.snowflake.com/en/collaboration/provider-listings-pricing-model#label-nativeapps-provider-listings-monetize) for the listing.

    3. Share it with the consumer account.

    4. Sign in to the consumer account using Snowsight.

    5. Install the Snowflake Native App.

  3. Confirm that the stored procedures successfully emit billable events.

  4. Confirm that the listing is set up properly.

Note

When you test Custom Event Billing, you must [set up a payment
method](https://other-docs.snowflake.com/en/collaboration/consumer-listings-
paying#set-up-payment-method) but you will not be charged for usage within
your organization.

### Validate whether the stored procedures emit billable events¶

While signed in to the consumer account with which you shared your listing,
call the stored procedures that you added to your Snowflake Native App.

For example, to test the stored procedure created for billing based on monthly
active rows, do the following:

  1. Sign in to the consumer account in Snowsight.

  2. Open a worksheet and set the context to `db_1.public`.

  3. Run the following SQL statement:
    
        CALL merge_procedure()
    

Copy

If the stored procedure returns `Success`, your code is working.

Note

If you run these SQL commands in the provider account that you used to create
the application package, you see an error.

### Validate the custom event billing pricing plan¶

To validate the consumer experience of a Snowflake Native App and confirm that
the listing and application package are set up properly, you can query the
[MARKETPLACE_PAID_USAGE_DAILY view](https://other-
docs.snowflake.com/en/collaboration/views/marketplace-paid-usage-daily-ds) in
the DATA_SHARING_USAGE schema of the shared SNOWFLAKE database.

Note

Due to latency in the view, run these queries at least two days after first
using the Snowflake Native App.

To confirm that billable events are successfully generated by a Snowflake
Native App and listing, run the following SQL statement in the consumer
account that you shared the listing with:

Note

Replace the PROVIDER_ACCOUNT_NAME and PROVIDER_ORGANIZATION_NAME values with
those of the provider account.

    
    
    SELECT listing_global_name,
       listing_display_name,
       charge_type,
       charge
    FROM SNOWFLAKE.DATA_SHARING_USAGE.MARKETPLACE_PAID_USAGE_DAILY
    WHERE charge_type='MONETIZABLE_BILLING_EVENTS'
          AND PROVIDER_ACCOUNT_NAME = <account_name>
          AND PROVIDER_ORGANIZATION_NAME= <organization_name>;
    

Copy

    
    
    +---------------------+------------------------+----------------------------+--------+
    | LISTING_GLOBAL_NAME |  LISTING_DISPLAY_NAME  |        CHARGE_TYPE         | CHARGE |
    +---------------------+------------------------+----------------------------+--------+
    | AAAA0BBB1CC         | Snowy Mountain Listing | MONETIZABLE_BILLING_EVENTS |   18.6 |
    +---------------------+------------------------+----------------------------+--------+
    

