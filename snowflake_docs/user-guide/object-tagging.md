# Object Tagging¶

This topic provides concepts and instructions on how to use tags in Snowflake.

To learn more about using a masking policy with a tag, see [Tag-based masking
policies](tag-based-masking-policies).

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Enterprise Edition
Feature](intro-editions)

This feature requires Enterprise Edition or higher. To inquire about
upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-
guide/contacting-support).

## What is a tag?¶

Tags enable data stewards to monitor sensitive data for compliance, discovery,
protection, and resource usage use cases through either a centralized or
decentralized data governance management approach.

A tag is a schema-level object that can be assigned to another Snowflake
object. A tag can be assigned an arbitrary string value upon assigning the tag
to a Snowflake object. Snowflake stores the tag and its string value as a key-
value pair. The tag must be unique for your schema, and the tag value is
always a string.

You create a tag using a [CREATE TAG](../sql-reference/sql/create-tag)
statement, and you specify the tag string value when assigning the tag to an
object. The tag can be assigned to an object while creating the object, using
a [CREATE <object>](../sql-reference/sql/create) statement, assuming that the
tag already exists. Alternatively, you can assign the tag to an existing
object using an [ALTER <object>](../sql-reference/sql/alter) statement.

A single tag can be assigned to different object types at the same time (e.g.
warehouse and table simultaneously). At the time of assignment, the tag string
value can be duplicated or remain unique. For example, multiple tables can be
assigned the cost_center tag and the tag can always have the string value be
sales. Alternatively, the string value could be different (e.g. engineering,
marketing, finance). After defining the tags and assigning the tags to
Snowflake objects, tags can be queried to monitor usage on the objects to
facilitate data governance operations, such as monitoring, auditing, and
reporting.

Because tags can be assigned to tables, views, and columns, setting a tag and
then querying the tag enables the discovery of a multitude of database objects
and columns that contain sensitive information. Upon discovery, data stewards
can determine how best to make that data available, such as selective
filtering using [row access policies](security-row-intro), or using [masking
policies](security-column-intro) to determine whether the data is tokenized,
fully masked, partially masked, or unmasked.

Assigning tags to warehouses enables accurate resource usage monitoring.
Querying tags on resources allows for easy resource grouping by cost center or
other organization units. Additionally, the tag can facilitate analyzing
relatively short-term business activities, such as projects, to provide a more
granular insight into what, when, and how resources were used.

### Tag quotas for objects and columns¶

The string value for each tag can be up to 256 characters, with the option to
specify allowed values for a tag.

The following description applies to all objects that are not tables and
views:

Snowflake allows a maximum number of 50 unique tags that can be set on a
single object. In a CREATE _< object>_ or ALTER _< object>_ statement, 100 is
the maximum number of tags that can be specified in a single statement.

The maximum number of unique tags is slightly different for tables and views,
including the columns in those tables and views.

#### Tables, views, and columns¶

For a table or view and its columns, the maximum number of unique tags that
can be specified in a single CREATE _< object>_ or ALTER _< object>_ statement
is 100. This total value has the following limits:

  * A single table or view object: 50 unique tags.

  * All columns combined in a single table or view: 50 unique tags.

For example, if a single column in a table has 10 unique tags set on the
column, Snowflake allows:

  * Setting 40 additional unique tags on either that same column, other columns in the table, or some combination of the columns in the table.

  * Setting 50 additional unique tags on the table itself.

Once the limit of 50 unique tags is met for the table itself and its columns,
no additional tags can be set on the table or its columns. At this point, if
there is a desire to set additional tags on the table or its columns, the next
step to consider is how to manage the tag quotas for an object.

#### Manage tag quotas¶

The maximum number of 50 unique tags includes dropped tags for a time period
of 24 hours starting from when the tag is dropped using a [DROP TAG](../sql-
reference/sql/drop-tag) statement. The reason for this time period is to allow
the user who dropped the tag to execute an [UNDROP TAG](../sql-
reference/sql/undrop-tag) statement, if necessary. When the UNDROP TAG
operation executes within the 24-hour time interval, Snowflake restores the
tag assignments (i.e. references) that were current prior to the drop
operation.

After the 24-hour time period expires, Snowflake purges any references
pertaining to the dropped tag. At this point, a new tag can be assigned to the
object or column that once referenced the dropped tag.

Use the following procedure to manage the tag quotas for an object:

  1. Query the [TAG_REFERENCES](../sql-reference/account-usage/tag_references) view (in Account Usage) to determine the tag assignments.

  2. Unset the tag from the object or column. For example:

For objects, use the corresponding `ALTER <object> ... UNSET TAG` command.

For a table or view column, use the corresponding `ALTER { TABLE | VIEW } ... { ALTER | MODIFY } COLUMN ... UNSET TAG` command.

  3. Drop the tag using a DROP TAG statement.

### Specify tag values¶

The `ALLOWED_VALUES` tag property enables specifying the possible string
values that can be assigned to the tag when the tag is set on an object. The
maximum number of possible string values for a single tag is 300.

You can specify these values when creating or replacing a tag with a [CREATE
TAG](../sql-reference/sql/create-tag) statement, or while modifying an
existing tag key with an [ALTER TAG](../sql-reference/sql/alter-tag)
statement. Note that the ALTER TAG statement supports adding allowed values
for a tag and dropping existing values for a tag.

To determine the list of allowed values for a tag, call the [GET_DDL](../sql-
reference/functions/get_ddl) function or the
[SYSTEM$GET_TAG_ALLOWED_VALUES](../sql-
reference/functions/system_get_tag_allowed_values) function.

For example:

> Create a tag named `cost_center` with `'finance'` and `'engineering'` as the
> only two allowed string values:
>

>>

>>     create tag cost_center

>>         allowed_values 'finance', 'engineering';

>>  
>>

>> Copy

>>

>> Verify the allowed values:

>>

>>>

>>>     select get_ddl('tag', 'cost_center')

>>>  
>>>
+------------------------------------------------------------------------------+

>>>     | GET_DDL('tag', 'cost_center')                                                |
>>>
|------------------------------------------------------------------------------|

>>>     | create or replace tag cost_center allowed_values = 'finance', 'engineering'; |
>>>
+------------------------------------------------------------------------------+

>>>  
>>>

>>> Copy

>
> Modify the tag named `cost_center` to add `'marketing'` as an allowed string
> value:
>

>>

>>     alter tag cost_center

>>         add allowed_values 'marketing';

>>  
>>

>> Copy

>
> Modify the tag named `cost_center` to drop `'engineering'` as an allowed
> string value:
>

>>

>>     alter tag cost_center

>>         drop allowed_values 'engineering';

>>  
>>

>> Copy

To obtain the list of allowed string values for a given tag, call either the
[GET_DDL](../sql-reference/functions/get_ddl) function or the
[SYSTEM$GET_TAG_ALLOWED_VALUES](../sql-
reference/functions/system_get_tag_allowed_values) function. For example,
assuming that the tag `cost_center` is stored in a database named `governance`
and a schema named `tags`:

>
>     select system$get_tag_allowed_values('governance.tags.cost_center');
>  
>     +--------------------------------------------------------------+
>     | SYSTEM$GET_TAG_ALLOWED_VALUES('GOVERNANCE.TAGS.COST_CENTER') |
>     |--------------------------------------------------------------|
>     | ["finance","marketing"]                                      |
>     +--------------------------------------------------------------+
>  
>
> Copy

### Tag lineage¶

A tag is inherited based on the Snowflake securable object hierarchy.
Snowflake recommends defining the tag keys as closely as possible to the
[securable object](security-access-control-overview.html#label-access-control-
securable-objects) hierarchy in your Snowflake environment.

> [![The tag administrator can apply masking policies to tables and
> views.](../_images/securable-object-hierarchy-org-to-
> column.png)](../_images/securable-object-hierarchy-org-to-column.png)

Tag inheritance means that if a tag is applied to a table, the tag also
applies to the columns in that table. This behavior is referred to as tag
lineage.

It is possible to override an inherited tag on a given object. For example, if
a table column inherits the tag named cost_center with a string value called
sales, the tag can be updated with a more specific tag string value such as
sales_na, to specify the North America sales cost center. Additionally, a new
tag can be applied to the table column. Use an [ALTER TABLE … ALTER
COLUMN](../sql-reference/sql/alter-table-column) statement to update the tag
string value on the column and to set one or more additional tags on a column.

After defining the tag keys and assigning tags to Snowflake objects, monitor
the tags, tag references, and tag lineage using the specified table functions
or query the views as shown in Monitor tags with SQL (in this topic).

Note

Tag lineage does not include _propagation_ to nested objects. For example:

> `table_1` » `view_1` » `materialized_view_1`

If nested objects already exist relative to an underlying table or view, a tag
set on underlying object does not automatically result in a tag being set on
the nested object. In this example, a tag set on `table_1` does not result in
the same tag being set on `view_1` and `materialized_view_1`. This behavior is
also true for columns.

If it is necessary to have tags on underlying objects or columns carry over to
nested objects, execute a CREATE OR REPLACE statement on the nested object and
make sure the SQL statement specifies the tag on the nested object or column.

### Benefits¶

Ease of Use:

    

Define a tag once and apply it to as many different objects as desirable.

Tag Lineage:

    

Since tags are inherited, applying the tag to objects higher in the securable
objects hierarchy results in the tag being applied to all child objects. For
example, if a tag is set on a table, the tag will be inherited by all columns
in that table.

Consistent Assignment with Replication:

    

Snowflake replicates tags and their assignments within the primary database to
the secondary database.

For more information, see Replication (in this topic).

Sensitive Data Tracking and Resource Usage:

    

Tags simplify identifying sensitive data (e.g. PII, Secret) and bring
visibility to Snowflake resource usage. With data and metadata in the same
system, analysts can quickly determine which resources consume the most
Snowflake credits based on the tag definition (e.g. `cost_center`,
`department`).

Centralized or Decentralized Management:

    

Tags supports different management approaches to facilitate compliance with
internal and external regulatory requirements.

In a centralized approach, the `tag_admin` custom role creates and applies
tags to Snowflake objects.

In a decentralized approach, individual teams apply tags to Snowflake objects
and the `tag_admin` custom role creates tags to ensure consistent tag naming.

### Considerations¶

Future grants:

    

[Future grants](../sql-reference/sql/grant-privilege.html#label-grant-
privilege-schema-future-grants) of privileges on tags are not supported.

As a workaround, grant the APPLY TAG privilege to a custom role to allow that
role to apply tags to another object.

Snowflake Native App:

    

Use caution when creating the setup script when tags exist in a versioned
schema. For details, see [version schema considerations](../developer-
guide/native-apps/creating-setup-script.html#label-setup-script-versioned-
schema-failures).

## Use tags with Snowflake objects and features¶

The following describes how tags affect objects and features in Snowflake.

### Supported objects¶

The following table lists the supported objects for tags, including columns,
based on the Snowflake securable object hierarchy.

A tag can be set on an object with a [CREATE <object>](../sql-
reference/sql/create) statement or an [ALTER <object>](../sql-
reference/sql/alter) statement unless specified otherwise in the table below.

A tag can be set on a column using a either a CREATE TABLE, CREATE VIEW, ALTER
TABLE … MODIFY COLUMN, or ALTER VIEW statement.

Object hierarchy | Supported objects | Notes  
---|---|---  
Organization | Account | A tag can be [set](../sql-reference/sql/alter-account) on your [current account](../sql-reference/functions/current_account) by a role with the global APPLY TAG privilege.  
Account | Application |   
| Application package |   
| Database |   
| Failover group |   
| Integration | All [types](../sql-reference/sql/create-integration) are supported. Use an [ALTER INTEGRATION](../sql-reference/sql/alter-integration) command to set a tag on the integration.  
| Network policy | Use an [ALTER NETWORK POLICY](../sql-reference/sql/alter-network-policy) command to set a tag on a network policy.  
| Replication group |   
| Role |   
| Share | Tags are set on the share by the data sharing provider. These tags are not visible to the data sharing consumer. Use an [ALTER SHARE](../sql-reference/sql/alter-share) command to set a tag on the share.  
| User |   
| Warehouse |   
Database | Database role | Use an [ALTER DATABASE ROLE](../sql-reference/sql/alter-database-role) command to set a tag on a database role.  
| Schema |   
Schema | Alert |   
| BUDGET instance | Use an [ALTER BUDGET](../sql-reference/classes/budget/commands/alter-budget) command to set a tag on an instance of the SNOWFLAKE.CORE.BUDGET class.  
| CLASSIFICATION instance | Use an [ALTER SNOWFLAKE.ML.CLASSIFICATION](../sql-reference/classes/classification/commands/alter-classification) command to set a tag on an instance of the SNOWFLAKE.ML.CLASSIFICATION class.  
| External function and UDF | Use an [ALTER FUNCTION](../sql-reference/sql/alter-function) command to set a tag on an external function or UDF.  
| External table | You can create an external table with a tag using a [CREATE EXTERNAL TABLE](../sql-reference/sql/create-external-table) statement. To manage tag assignments on an external table, use the [ALTER TABLE](../sql-reference/sql/alter-table) command.  
| Git repository |   
| Apache Iceberg™ table |   
| Materialized view |   
| Pipe | Set a tag on a pipe with an [ALTER PIPE](../sql-reference/sql/alter-pipe) statement.  
| Policy | Set a tag on a [masking](../sql-reference/sql/alter-masking-policy), [password](../sql-reference/sql/alter-password-policy), [row access](../sql-reference/sql/alter-row-access-policy), and [session](../sql-reference/sql/alter-session-policy) policy with the corresponding ALTER _< policy>_ statement.  
| Procedure | Set a tag on a stored procedure with an [ALTER PROCEDURE](../sql-reference/sql/alter-procedure) statement.  
| Stage | Set a tag on a stage with an [ALTER STAGE](../sql-reference/sql/alter-stage) statement.  
| Stream |   
| Table |   
| Task | Set a tag on a task with an [ALTER TASK](../sql-reference/sql/alter-task) statement.  
| View |   
Table or View | Column | Includes [event tables](../sql-reference/sql/alter-table-event-table).  
  
### Object Tagging and masking policies¶

For details, see [Tag-based masking policies](tag-based-masking-policies).

Note that a masking policy that is directly assigned to a column takes
precedence over a tag-based masking policy.

### CREATE TABLE statements¶

With [CREATE TABLE … LIKE](../sql-reference/sql/create-table), tags assigned
to the source table are assigned to the target table.

### Dynamic tables¶

You can create a dynamic table with a row access policy, masking policy, and
tag. For more information, see:

  * [CREATE DYNAMIC TABLE](../sql-reference/sql/create-dynamic-table)

  * [Additional limitations with incremental refresh](dynamic-tables-limitations.html#label-dynamic-tables-limits-incremental-refresh-features)

### Replication¶

Tags and their assignments can be replicated from a source account to a target
account.

Tag assignments cannot be modified in the target account after the initial
replication from the source account. For example, setting a tag on a secondary
(i.e. replicated) database is not allowed. To modify tag assignments in the
target account, modify them in the source account and replicate them to the
target account.

For [database replication](database-replication-considerations), the
replication operation fails if either of the following conditions is true:

  * The primary database is in an Enterprise (or higher) account and contains a tag but one or more of the accounts approved for replication are on lower editions.

  * An object contained in the primary database has a [dangling reference](database-replication-considerations.html#label-database-replication-dangling-references) to a tag in a different database.

To avoid a dangling reference error, replicate the database and account-level
objects using a [replication or failover group](account-replication-
intro.html#label-replication-and-failover-groups). Ensure that the replication
group includes:

  * The database containing the tags in the `ALLOWED_DATABASES` property.

  * Other account-level objects that have a tag in the `OBJECT_TYPES` property (e.g. `ROLES`, `WAREHOUSES`).

For details, refer to [CREATE REPLICATION GROUP](../sql-reference/sql/create-
replication-group) and [CREATE FAILOVER GROUP](../sql-reference/sql/create-
failover-group).

Note

When using replication and failover groups or database replication:

  * Failover/failback features are only available to Snowflake accounts that are Business Critical Edition (or higher).

For more information, refer to [Introduction to replication and failover
across multiple accounts](account-replication-intro).

  * If you specify the `IGNORE EDITION CHECK` clause for database replication in an [ALTER DATABASE](../sql-reference/sql/alter-database) statement or in a CREATE OR ALTER statement for a replication or failover group, tag replication can occur when the target account is a lower edition than [Business Critical](intro-editions).

For details, refer to the clause description in these commands.

### Cloning¶

  * Tag associations in the source object (e.g. table) are maintained in the cloned objects.

  * For a database or a schema:

The tags stored in that database or schema are also cloned.

When a database or schema is cloned, tags that reside in that schema or
database are also cloned.

If a table or view exists in the source schema/database and has references to
tags in the same schema or database, the cloned table or view is mapped to the
corresponding cloned tag (in the target schema/database) instead of the tag in
the source schema or database.

### Data Sharing¶

  * When the shared view and tag exist in different databases, grant the REFERENCE_USAGE privilege on the database containing the tag to the share. For details, see [Share data from multiple databases](data-sharing-multiple-db).

  * In the data sharing consumer account:

    * Executing the [SHOW TAGS](../sql-reference/sql/show-tags) returns the shared tag, provided that the role executing the SHOW TAGS command has the USAGE privilege on the schema containing the shared tag.

If the provider grants the READ privilege on the tag to the share or to a
shared database role, the consumer can view the tag assignments for the shared
tag. For details, see [shared tag references](data-sharing-
provider.html#label-share-tag-references).

    * If a tag from the data sharing provider account is assigned to a shared table, the data sharing consumer cannot call the [SYSTEM$GET_TAG](../sql-reference/functions/system_get_tag) function or the [TAG_REFERENCES](../sql-reference/functions/tag_references) Information Schema table function to view the tag assignment.

## Create and assign tags¶

The following is a high-level overview to use tags in Snowflake:

  * Create a tag using a [CREATE TAG](../sql-reference/sql/create-tag) statement.

  * Assign a tag to an existing Snowflake object using Snowsight or an [ALTER <object>](../sql-reference/sql/alter) command.

> Note that you can assign a tag to a new object using a [CREATE
> <object>](../sql-reference/sql/create) command. Refer to the Supported
> objects section in this topic to evaluate the objects that support setting a
> tag with the ALTER _< object>_ command only.

After assigning tags, you can monitor tag usage using SQL or Snowsight. For
details, refer to Monitor tags with SQL and Monitor tags with Snowsight (in
this topic).

For simplicity, the workflow assumes a centralized management approach to
tags, where the `tag_admin` custom role has both the CREATE TAG and the global
APPLY TAG privileges.

  1. Create a custom role and assign privileges.

In a centralized management approach, the `tag_admin` custom role is
responsible for creating and assigning tags to Snowflake objects.

Note that this example uses the ACCOUNTADMIN system role. If using this
higher-privileged role in a production environment is not desirable, verify
that the role assigning privileges to the `tag_admin` custom role has the
necessary privileges to qualify the `tag_admin` custom role. For more
information, see Managing tags (in this topic).

    
        USE ROLE USERADMIN;
    CREATE ROLE tag_admin;
    USE ROLE ACCOUNTADMIN;
    GRANT CREATE TAG ON SCHEMA mydb.mysch TO ROLE tag_admin;
    GRANT APPLY TAG ON ACCOUNT TO ROLE tag_admin;
    

Copy

  2. Grant the `tag_admin` custom role to a user serving as the tag administrator.
    
        USE ROLE USERADMIN;
    GRANT ROLE tag_admin TO USER jsmith;
    

Copy

  3. Execute a [CREATE TAG](../sql-reference/sql/create-tag) statement to create a tag.
    
        USE ROLE tag_admin;
    USE SCHEMA mydb.mysch;
    CREATE TAG cost_center;
    

Copy

  4. Assign a tag to a Snowflake object or column.

SQL:

    

You can set a tag on all supported objects and columns that exist with an
ALTER _< object>_ command. Some objects support setting a tag when you create
or replace the object. For details, refer to the table in the Supported
objects section in this topic.

For example:

     * To set a tag on a new warehouse use the [CREATE WAREHOUSE](../sql-reference/sql/create-warehouse) command.
        
                USE ROLE tag_admin;
        CREATE WAREHOUSE mywarehouse WITH TAG (cost_center = 'sales');
        

Copy

     * To set a tag on an existing warehouse, use the [ALTER WAREHOUSE](../sql-reference/sql/alter-warehouse) command.
        
                USE ROLE tag_admin;
        ALTER WAREHOUSE wh1 SET TAG cost_center = 'sales';
        

Copy

     * To set a tag on an existing column, use the [ALTER TABLE … MODIFY COLUMN](../sql-reference/sql/alter-table-column) command for a table column or the [ALTER VIEW … MODIFY COLUMN](../sql-reference/sql/alter-view) command for a view column. Note that more than one tag can be set or unset in a single statement.
        
                ALTER TABLE hr.tables.empl_info
          MODIFY COLUMN job_title
          SET TAG visibility = 'public';
        

Copy

Snowsight:

    

You can set a tag on existing tables, views, and columns using Snowsight.

There are several options to set a tag:

     * Navigate to the desired table, view, or column using the object explorer (i.e. Data » Databases).

Select the More menu (i.e. `...`) » Edit, and select \+ Tag. Follow the
prompts to manage the tag assignment.

     * Navigate to the Governance area (i.e. Monitoring » Governance) in Snowsight and do the following:

       * Select a tile, distribution percentage, and one of the most used tags or tables. When you select an item in the Dashboard, Snowsight redirects you to the Tagged Objects tab.

       * Modify the filters as needed. When you select an object or column, Snowsight redirects you to its location in the object explorer. Update the tag assignment as needed.

     * Navigate to the Tagged Objects tab directly. Modify the filters, select an object or column, and manage the tag assignment.

Note

To access the Governance area, do one of the following:

     * Use the ACCOUNTADMIN role.

     * Use to a role that is granted the GOVERNANCE_VIEWER and OBJECT_VIEWER database roles.

For details about these database roles, see [SNOWFLAKE database roles](../sql-
reference/snowflake-db-roles).

## Monitor tags with SQL¶

You can monitor tags with SQL by using two different Account Usage views, two
Information Schema table functions, an Account Usage table function, and a
system function.

It can be helpful to think of two general approaches to determine how to
monitor tag usage.

  * Discover Tags

  * Identify Assignments

### Discover tags¶

Snowflake supports the following options to list tags and to identify the tag
string value for a given tag key.

  * Identify tags in your account:

Use the [TAGS](../sql-reference/account-usage/tags) view in the Account Usage
schema of the shared SNOWFLAKE database. This view can be thought of as a
_catalog_ for all tags in your Snowflake account that provides information on
current and deleted tags. For example:

> >     SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.TAGS
>     ORDER BY TAG_NAME;
>  
>
> Copy

  * Identify a value for a given tag:

Use the [SYSTEM$GET_TAG](../sql-reference/functions/system_get_tag) system
function to return the tag value assigned to the specified tag, and the
Snowflake object or column.

> >     SELECT SYSTEM$GET_TAG('cost_center', 'my_table', 'table');
>  
>
> Copy

### Identify assignments¶

Snowflake supports different options to identify tag assignments, depending on
whether the query needs to target the account or a specific database, and
whether tag lineage is necessary.

  * Account-level query with lineage:

Use the Account Usage table function [TAG_REFERENCES_WITH_LINEAGE](../sql-
reference/functions/tag_references_with_lineage) to determine all of the
objects that have a given tag key and tag value that also includes the tag
lineage:

> >     SELECT *
>     FROM TABLE(
>       snowflake.account_usage.tag_references_with_lineage(
>         'my_db.my_schema.cost_center'
>       )
>     );
>  
>
> Copy

  * Account-level query without lineage:

Use the Account Usage [TAG_REFERENCES](../sql-reference/account-
usage/tag_references) view to determine all of the objects that have a given
tag key and tag value, but does not include the tag lineage:

> >     SELECT * FROM snowflake.account_usage.tag_references
>     ORDER BY TAG_NAME, DOMAIN, OBJECT_ID;
>  
>
> Copy

  * Database-level query, with lineage:

Every Snowflake database includes an [Snowflake Information Schema](../sql-
reference/info-schema). Use the Information Schema table function
[TAG_REFERENCES](../sql-reference/functions/tag_references) to determine all
of the objects that have a given tag that also includes the tag lineage in a
given database:

> >     SELECT *
>     FROM TABLE(
>       my_db.INFORMATION_SCHEMA.TAG_REFERENCES(
>         'my_table',
>         'table'
>       )
>     );
>  
>
> Copy

  * Database-level query for all of the tags on every column in a table or view, with lineage:

Use the Information Schema table function [TAG_REFERENCES_ALL_COLUMNS](../sql-
reference/functions/tag_references_all_columns) to obtain all of the tags that
are set on every column in a given table or view.

Note that the domain `TABLE` must be used for all objects that contain
columns, even if the object name is a view (i.e. view, materialized view).

> >     SELECT *
>     FROM TABLE(
>       INFORMATION_SCHEMA.TAG_REFERENCES_ALL_COLUMNS(
>         'my_table',
>         'table'
>       )
>     );
>  
>
> Copy

## Monitor tags with Snowsight¶

You can use the Snowsight Monitoring » Governance area to monitor and report
on the usage of policies and tags with tables, views, and columns. There are
two different interfaces: Dashboard and Tagged Objects.

When using the Dashboard and the Tagged Objects interface, note the following
details.

  * The Dashboard and Tagged Objects interfaces require a running warehouse.

  * Snowsight updates the Dashboard every 12 hours.

  * The Tagged Objects information latency can be up to two hours and returns up to 1000 objects.

### Accessing the Governance area in Snowsight¶

To access the Governance area, your Snowflake account must be [Enterprise
Edition or higher](intro-editions). Additionally, you must do either of the
following:

  * Use the ACCOUNTADMIN role.

  * Use an account role that is directly granted the GOVERNANCE_VIEWER and OBJECT_VIEWER database roles.

You must use an account role with these database role grants. Currently,
Snowsight does not evaluate role hierarchies and user-defined database roles
that have access to tables, views, data access policies, and tags.

To determine if your account role is granted these two database roles, use a
[SHOW GRANTS](../sql-reference/sql/show-grants) command:

> >     SHOW GRANTS LIKE '%VIEWER%' TO ROLE data_engineer;
>  
>
> Copy
>  
>     >
> |-------------------------------+-----------+---------------+-----------------------------+------------+-----------------+--------------+------------|
>     | created_on                    | privilege | granted_on    | name                        | granted_to | grantee_name    | grant_option | granted_by |
>
> |-------------------------------+-----------+---------------+-----------------------------+------------+-----------------+--------------+------------|
>     | 2024-01-24 17:12:26.984 +0000 | USAGE     | DATABASE_ROLE | SNOWFLAKE.GOVERNANCE_VIEWER | ROLE       | DATA_ENGINEER   | false        |            |
>     | 2024-01-24 17:12:47.967 +0000 | USAGE     | DATABASE_ROLE | SNOWFLAKE.OBJECT_VIEWER     | ROLE       | DATA_ENGINEER   | false        |            |
>
> |-------------------------------+-----------+---------------+-----------------------------+------------+-----------------+--------------+------------|
>  

  

If your account role is not granted either or both of these database roles,
use the [GRANT DATABASE ROLE](../sql-reference/sql/grant-database-role)
command and run the SHOW GRANTS command again to confirm the grants:

> >     USE ROLE ACCOUNTADMIN;
>     GRANT DATABASE ROLE SNOWFLAKE.GOVERNANCE_VIEWER TO ROLE data_engineer;
>     GRANT DATABASE ROLE SNOWFLAKE.OBJECT_VIEWER TO ROLE data_engineer;
>     SHOW GRANTS LIKE '%VIEWER%' TO ROLE data_engineer;
>  
>
> Copy

For details about these database roles, see [SNOWFLAKE database roles](../sql-
reference/snowflake-db-roles).

### Dashboard¶

As a data administrator, you can use the Dashboard interface to monitor tag
and policy usage in the following ways.

  * Coverage: specifies the count and percentage based on whether a table, view, or column has a policy or tag.

  * Prevalence: lists and counts the most frequently used policies and tags.

The coverage and prevalence provide a snapshot as to how well the data is
protected and tagged.

When you select a count number, percentage, policy name, or tag name, the
Tagged Objects interface opens. The Tagged Objects interface updates the
filters automatically based on your selection in the Dashboard.

The monitoring information is an alternative or complement to running complex
and query-intensive operations on multiple Account Usage views.

These views might include, but are not limited to, the [COLUMNS](../sql-
reference/account-usage/columns), [POLICY_REFERENCES](../sql-
reference/account-usage/policy_references), [TABLES](../sql-reference/account-
usage/tables), [TAG_REFERENCES](../sql-reference/account-
usage/tag_references), and [VIEWS](../sql-reference/account-usage/views)
views.

### Tagged Objects¶

As a data administrator, you can use this table to associate the coverage and
prevalence in the Dashboard to a list of specific tables, view, or columns
quickly. You can also filter the table results manually as follows.

  * Choose Tables or Columns.

  * For tags, you can filter with tags, without tags, or by a specific tag.

  * For policies, you can filter with policies, without policies, or by a specific policy.

When you select a row in the table, the Table Details or Columns tab in Data »
Databases opens. You can edit the tag and policy assignments as needed.

## Managing tags¶

### Tag privileges¶

Snowflake supports the following privileges to determine whether users can
create, set, and own tags.

The USAGE privilege on the parent database and schema are required to perform
operations on any object in a schema.

Privilege | Usage  
---|---  
CREATE | Enables creating a new tag in a schema.  
APPLY | Enables the set and unset operations for the tag on a Snowflake object. For syntax examples, see: Summary of DDL commands, operations, and privileges.  
OWNERSHIP | Transfers ownership of the tag, which grants full control over the tag. Required to alter most properties of a tag.  
  
### Tag DDL reference¶

Snowflake supports the following DDL to create and manage tags:

  * [CREATE TAG](../sql-reference/sql/create-tag)

  * [ALTER TAG](../sql-reference/sql/alter-tag)

  * [ALTER <object>](../sql-reference/sql/alter) (to set a tag on a Snowflake object)

  * [SHOW TAGS](../sql-reference/sql/show-tags)

  * [DROP TAG](../sql-reference/sql/drop-tag)

  * [UNDROP TAG](../sql-reference/sql/undrop-tag)

Note that Snowflake does not support the [describe](../sql-reference/sql/desc)
operation for the tag object.

### Summary of DDL commands, operations, and privileges¶

The following table summarizes the relationship between tag privileges and DDL
operations.

Operation | Privilege required  
---|---  
Create tag. | A role with the CREATE TAG privilege in the same schema.  
Alter tag. | The role with the OWNERSHIP privilege on the tag.  
Drop & Undrop tag. | A role with the OWNERSHIP privilege on the tag and the USAGE privilege on the database and schema in which the tag exists.  
Show tags. | One of the following: . A role with the USAGE privilege on the schema in which the tags exist, or . A role with the APPLY TAG on ACCOUNT permission.  
Set or unset a tag on an object. | For individual objects, a role with the APPLY TAG privilege on the account, or the APPLY TAG privilege on the tag and the OWNERSHIP privilege on the object on which the tag is set. See Supported objects.  
Set or unset a tag on a column. | A role with the APPLY TAG privilege on the account, or a role with the APPLY privilege on the tag and the OWNERSHIP privilege on the table or view.  
Get tags on an object. | See [SYSTEM$GET_TAG](../sql-reference/functions/system_get_tag), [TAG_REFERENCES](../sql-reference/functions/tag_references), and [TAG_REFERENCES_WITH_LINEAGE](../sql-reference/functions/tag_references_with_lineage).  
  
Snowflake supports different permissions to create and set a tag on an object.

  1. For a centralized tag management approach in which the `tag_admin` custom role creates and sets tags on all objects/columns, the following permissions are necessary:
    
        use role securityadmin;
    grant create tag on schema <db_name.schema_name> to role tag_admin;
    grant apply tag on account to role tag_admin;
    

Copy

  2. In a hybrid management approach, a single role has the CREATE TAG privilege to ensure tags are named consistently and individual teams or roles have the APPLY privilege for a specific tag.

For example, the custom role `finance_role` role can be granted the permission
to set the tag `cost_center` on tables and views the role owns (i.e. the role
has the OWNERSHIP privilege on the table or view):

    
        use role securityadmin;
    grant create tag on schema <db_name.schema_name> to role tag_admin;
    grant apply on tag cost_center to role finance_role;
    

Copy

