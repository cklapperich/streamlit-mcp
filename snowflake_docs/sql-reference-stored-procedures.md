# Stored procedures¶

Snowflake provides stored procedures to facilitate using certain Snowflake
features. To find the stored procedures that are associated with a particular
Snowflake Class, see [SQL class reference](sql-reference-classes).

Use [CALL](sql-reference/sql/call) to call a stored procedure. For example:

>
>     CALL SYSTEM$CLASSIFY('hr.tables.empl_info', null);
>  
>
> Copy

Snowflake supports the following stored procedures, grouped by feature:

Feature | Stored procedure  
---|---  
[Data Classification](user-guide/classify-intro) | 

  * [ASSOCIATE_SEMANTIC_CATEGORY_TAGS](sql-reference/stored-procedures/associate_semantic_category_tags)
  * [SYSTEM$CLASSIFY](sql-reference/stored-procedures/system_classify)
  * [SYSTEM$CLASSIFY_SCHEMA](sql-reference/stored-procedures/system_classify_schema)
  * [SYSTEM$CANCEL_CLASSIFY_SCHEMA](sql-reference/stored-procedures/system_cancel_classify_schema)

  
[Differential privacy](user-guide/diff-privacy/differential-privacy-overview) | 

  * [RESET_PRIVACY_BUDGET](sql-reference/stored-procedures/reset_privacy_budget)

  
[Synthetic data](user-guide/synthetic-data) | 

  * [GENERATE_SYNTHETIC_DATA](sql-reference/stored-procedures/generate_synthetic_data)

  
[Notifications](user-guide/notifications/about-notifications) | 

  * [SYSTEM$SEND_SNOWFLAKE_NOTIFICATION](sql-reference/stored-procedures/system_send_snowflake_notification)
  * [SYSTEM$SEND_EMAIL](sql-reference/stored-procedures/system_send_email)

  
[Data sharing and collaboration](guides-overview-sharing) | 

  * [SYSTEM$REQUEST_LISTING_AND_WAIT](sql-reference/stored-procedures/system_request_listing_and_wait)

  
[Default event table](developer-guide/logging-tracing/event-table-setting-up) | 

  * [ADD_ROW_ACCESS_POLICY_ON_EVENTS_VIEW](sql-reference/stored-procedures/snowflake_telemetry_add_row_access_policy_on_events_view)
  * [DROP_ROW_ACCESS_POLICY_ON_EVENTS_VIEW](sql-reference/stored-procedures/snowflake_telemetry_drop_row_access_policy_on_events_view)

