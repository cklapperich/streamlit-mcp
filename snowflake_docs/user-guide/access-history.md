# Access History¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Enterprise Edition
Feature](intro-editions)

Access History requires Enterprise Edition (or higher). To inquire about
upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-
guide/contacting-support).

This topic provides concepts on the user access history in Snowflake.

## Overview¶

Access History in Snowflake refers to when the user query reads data and when
the SQL statement performs a data write operation, such as INSERT, UPDATE, and
DELETE along with variations of the COPY command, from the source data object
to the target data object. The user access history can be found by querying
the ACCESS_HISTORY view in the ACCOUNT_USAGE and ORGANIZATION_USAGE schemas.
The records in these views facilitate regulatory compliance auditing and
provide insights on popular and frequently accessed tables and columns because
there is a direct link between the user (i.e. query operator), the query, the
table or view, the column, and the data.

Each row in the ACCESS_HISTORY view contains a single record per SQL
statement. The record contains the following kinds of information:

  * The _source columns_ the query accessed directly and indirectly, such as the underlying tables that the data for the query comes from.

  * The _projected columns_ the user sees in the query result, such as the columns specified in a SELECT statement.

  * The columns that are used to determine the query result but are not projected, such as columns in a WHERE clause to filter the result.

For example:

    
    
    CREATE OR REPLACE VIEW v1 (vc1, vc2) AS
    SELECT c1 as vc1,
           c2 as vc2
    FROM t
    WHERE t.c3 > 0
    ;
    

Copy

  * Columns C1 and C2 are source columns that the view accesses directly, which are recorded in the `base_objects_accessed` column of the ACCESS_HISTORY view.

  * Column C3 is used to filter the rows the view includes, which is recorded in the `base_objects_accessed` column of the ACCESS_HISTORY view.

  * Columns VC1 and VC2 are projected columns the user sees when querying the view, `SELECT * FROM v1;`, which are recorded in the `direct_objects_accessed` column of the ACCESS_HISTORY view.

The same behavior applies to a key column in a WHERE clause. For example:

    
    
    CREATE OR REPLACE VIEW join_v (vc1, vc2, c1) AS
      SELECT
          bt.c1 AS vc1,
          bt.c2 AS vc2,
          jt.c1
      FROM bt, jt
      WHERE bt.c3 = jt.c1;
    

Copy

  * Two different tables are required to create the view: `bt` (base table) and `jt` (join table.).

  * Columns C1, C2, and C3 from the base table and column C1 from the join table are all recorded in the `base_objects_accessed` column of the ACCESS_HISTORY view.

  * Columns VC1, VC2, and C1 are projected columns the user sees when querying the view, `SELECT * FROM join_v;`, which are recorded in the `direct_objects_accessed` column of the ACCESS_HISTORY view.

Note

Records in the Account Usage [QUERY_HISTORY](../sql-reference/account-
usage/query_history) view do not always get recorded in the ACCESS_HISTORY
view. The structure of the SQL statement determines whether Snowflake records
an entry in the ACCESS_HISTORY view.

For details on the read and write operations Snowflake supports in the
ACCESS_HISTORY view, refer to the view [Usage notes](../sql-reference/account-
usage/access_history.html#label-acctuse-view-access-history-usage-notes).

## Tracking read and write operations¶

The ACCESS_HISTORY view in both the ACCOUNT_USAGE and the ORGANIZATION_USAGE
schemas includes the following columns:

    
    
    query_id | query_start_time | user_name | direct_objects_accessed | base_objects_accessed | objects_modified | object_modified_by_ddl | policies_referenced | parent_query_id | root_query_id
    

Copy

Read operations are tracked through the first five columns, while the last
column, `objects_modified`, specifies the data write information that involved
Snowflake columns, tables, and stages.

The query in Snowflake and how the database objects were created determines
the information Snowflake returns in the `direct_objects_accessed`,
`base_objects_accessed`, and `objects_modified` columns.

Similarly, if the query references an object protected by a row access policy
or a column protected by a masking policy, Snowflake records the policy
information in the `policies_referenced` column.

The `object_modified_by_ddl` column records the DDL operation on a database,
schema, table, view, and column. These operations also include statements that
specify a row access policy on a table or view, a masking policy on a column,
and tag updates (e.g. set a tag, change a tag value) on the object or column.

The `parent_query_id` and `root_query_id` columns record query IDs that
correspond to:

  * A query that performs a read or write operation on another object.

  * A query that performs a read or write operation on an object that calls a stored procedure, including nested stored procedure calls. For details, see ancestor queries (in this topic).

For column details, see the [Columns](../sql-reference/account-
usage/access_history.html#label-acctuse-view-access-history-columns) section
in the ACCESS_HISTORY view.

### Read¶

Consider the following scenario to understand a read query and how the
ACCESS_HISTORY view records this information:

  * A series of objects: `base_table` » `view_1` » `view_2` » `view_3`.

  * A read query on `view_2`, such as:
    
        select * from view_2;
    

Copy

In this example, Snowflake returns:

  * `view_2` in the `direct_objects_accessed` column because the query specifies `view_2`.

  * `base_table` in the `base_objects_accessed` column because that is the original source of the data in `view_2`.

Note that `view_1` and `view_3` are not included in the
`direct_objects_accessed` and `base_objects_accessed` columns because neither
of those views were included in the query and they are not the base object
that serves as the source for the data in `view_2`.

### Write¶

Consider the following scenario to understand a write operation and how the
ACCESS_HISTORY view records this information:

  * A data source: `base_table`

  * Create a table from the data source (i.e. CTAS):
    
        create table table_1 as select * from base_table;
    

Copy

In this example, Snowflake returns:

  * `base_table` in the `base_objects_accessed` and `direct_objects_accessed` columns because the table was accessed directly and is the source of the data.

  * `table_1` in the `objects_modified` column with the columns that were written to when creating the table.

### Supported operations¶

For a complete description of the read and write operations the ACCESS_HISTORY
view supports, see the usage notes sections in the [ACCESS_HISTORY
view](../sql-reference/account-usage/access_history).

### Multiple statements in a single request¶

Snowflake supports executing multiple statements simultaneously as a single
request. How you track the request in the access history depends on whether it
was executed in Snowsight or programmatically.

  * When you use Snowsight to execute multiple statements, it runs the queries one at a time and returns the `query_id` of the last executed query. You can find all executed statements and their return values in the ACCESS_HISTORY view.

  * Features like the Snowflake Python connector or the Snowflake SQL API combine multiple SQL statements into a single request and return a single `query_id` for all of the statements. This number is actually a parent query id for all of the individual statements. To return the `query_id` of each statement that comprised the request, you must query the ACCESS_HISTORY view using the `parent_query_id`. For example, if the request returned `query_id = 6789`, then you can return the query ids of the individual statements by executing the following:
    
        SELECT query_id, parent_query_id, direct_objects_accessed
    FROM snowflake.account_usage.access_history
    WHERE parent_query_id = 6789;
    

Copy

### Benefits¶

Access history in Snowflake provides the following benefits pertaining to read
and write operations:

Data discovery:

    

Discover unused data to determine whether to archive or delete the data.

Track how sensitive data moves:

    

Track data movement from an external cloud storage location (e.g. Amazon S3
bucket) to the target Snowflake table, and vice versa.

Track internal data movement from a Snowflake table to a different Snowflake
table.

After tracing the movement of sensitive data, apply policies
([masking](security-column-intro) and [row access](security-row-intro)) to
protect data, update [access control settings](security-access-control-
overview) to further regulate access to the stage and table, and set
[tags](object-tagging) to ensure stages, tables, and columns with sensitive
data can be tracked for compliance requirements.

Data validation:

    

The accuracy and integrity of reports, dashboards, and data visualization
products such as charts and graphs are validated since the data can be traced
to its original source.

Data stewards can also notify users prior to dropping or altering a given
table or view.

Compliance auditing:

    

Identify the Snowflake user who performed a write operation on a table or
stage and when the write operation occurred to meet compliance regulations,
such as [GDPR](https://gdpr-info.eu/) and
[CCPA](https://oag.ca.gov/privacy/ccpa).

Enhance overall data governance:

    

The ACCESS_HISTORY view provides a unified picture of what data was accessed,
when the data access took place, and how the accessed data moved from the data
source object to the data target object.

## Column lineage¶

Column lineage (i.e. access history for columns) extends the Account Usage
ACCESS_HISTORY view to specify how data flows from the source column to the
target column in a write operation. Snowflake tracks the data from the source
columns through all subsequent table objects that reference data from the
source columns (e.g. INSERT, MERGE, CTAS) provided that objects in the lineage
chain are not dropped. Snowflake makes column lineage accessible by enhancing
the `objects_modified` column in the ACCESS_HISTORY view.

Column lineage provides the following benefits:

Protect Derived Objects:

    

Data stewards can easily [tag](object-tagging) sensitive source columns
without having to do additional work after creating derived objects (e.g.
CTAS). Subsequently, the data steward can protect tables containing sensitive
columns with a [row access policy](security-row-intro) or protect the
sensitive columns themselves with either a [masking policy](security-column-
intro) or a [tag-based masking policy](tag-based-masking-policies).

Sensitive Column Copy Frequency:

    

Data privacy officers can quickly determine the object count (e.g. 1 table, 2
views) of a column containing sensitive data. By knowing how many times a
column with sensitive data appears in a table object, data privacy officers
can prove how they satisfy regulatory compliance standards (e.g. to meet
General Data Protection Regulation (GDPR) standards in the European Union).

Root Cause Analysis:

    

Column lineage provides a mechanism to trace the data to its source, which can
help to pinpoint points of failure resulting from poor data quality and reduce
the number of columns to analyze during the troubleshooting process.

For additional details about column lineage, see:

  * Example: Column lineage (in this topic)

  * [Column Lineage Usage Notes](../sql-reference/account-usage/access_history.html#label-access-history-column-notes)

## Masking and row access policy references¶

The POLICY_REFERENCED column specifies the object that has a row access policy
set on a table or a masking policy set on a column, including any intermediate
objects that are protected by either a row access policy or a masking policy.
Snowflake records the policy that is enforced on the table or column.

Consider these objects:

`t1` » `v1` » `v2`

Where:

  * `t1` is a base table.

  * `v1` is a view built from the base table.

  * `v2` is a view built from `v1`.

If the user queries `v2`, the `policies_referenced` column records either the
row access policy that protects `v2`, each masking policy that protects the
columns in `v2`, or both kinds of policy as applicable. Additionally, this
column records any masking or row access policies that protect `t1` and `v1`.

These records can help data governors understand how their policy-protected
objects are accessed.

The `policies_referenced` column provides additional benefits to the
ACCESS_HISTORY view:

  * Identify the policy-protected objects a user accesses in a given query.

  * Simplify the policy audit process.

Querying the ACCESS_HISTORY view eliminates the need for complex joins on
other Account Usage views (e.g. [POLICY_REFERENCES](../sql-reference/account-
usage/policy_references) and [QUERY_HISTORY](../sql-reference/account-
usage/query_history)), to obtain information about the protected objects and
protected columns a user accesses.

## Account-level vs. Organization-level access history¶

Administrators monitor access history at the account-level by querying the
[ACCESS_HISTORY view](../sql-reference/account-usage/access_history) in the
account’s ACCOUNT_USAGE schema. There is no additional cost associated with
the ACCOUNT_USAGE.ACCESS_HISTORY view.

The ACCESS_HISTORY view in the ORGANIZATION_USAGE schema gathers the access
history of all of the accounts in an organization into a single view to
provide an organization-level access history. This
ORGANIZATION_USAGE.ACCESS_HISTORY view is only found in the [organization
account](organization-accounts).

Organization-level access history in the ORGANIZATION_USAGE schema differs
from access history in the ACCOUNT_USAGE schema in the following ways:

Additional columns:

    

The ORGANIZATION_USAGE.ACCESS_HISTORY view in the organization account
contains additional columns that provide insights related to [organizational
listings](collaboration/listings/organizational/org-listing-about). These
columns can be used to determine which of the data products attached to an
organization listing were accessed by a consumer’s query, and whether those
data products are protected by a policy such as a masking policy. For more
information, see [Organizational listing
governance](collaboration/listings/organizational/org-listing-governance).

Additional cost:

    

The ORGANIZATION_USAGE.ACCESS_HISTORY view in the organization account is a
premium view that incurs the following costs:

  * Compute costs associated with the serverless tasks that populate the ACCESS_HISTORY view.

  * Storage costs associated with storing the data in the ACCESS_HISTORY view.

For more information about these costs, see [Costs associated with the
ORGANIZATION_USAGE schema](organization-accounts.html#label-org-account-views-
cost).

## Querying the ACCESS_HISTORY View¶

The following sections provide example queries for the ACCESS_HISTORY view.

Note that some of the example queries filter on the `query_start_time` column
to increase query performance. Another option to increase performance is to
query over narrower time ranges.

## Examples: Read Queries¶

The subsections below detail how to query the ACCESS_HISTORY view for read
operations for the following use cases:

  * Obtain the access history for a specific user.

  * Facilitate compliance audits for sensitive data access in the last 30 days, based on `object_id` (e.g. a table id), to answer the following questions:

    * Who accessed the data?

    * When was the data accessed?

    * What columns were accessed?

### Return the user access history¶

Return the user access history, ordered by user and query start time, starting
from the most recent access.

>
>     SELECT user_name
>            , query_id
>            , query_start_time
>            , direct_objects_accessed
>            , base_objects_accessed
>     FROM access_history
>     ORDER BY 1, 3 desc
>     ;
>  
>
> Copy

### Facilitate compliance audits¶

The following examples help to facilitate compliance audits:

  * Add the `object_id` value to determine who accessed a sensitive table in the last 30 days:
    
        SELECT distinct user_name
    FROM access_history
         , lateral flatten(base_objects_accessed) f1
    WHERE f1.value:"objectId"::int=<fill_in_object_id>
    AND f1.value:"objectDomain"::string='Table'
    AND query_start_time >= dateadd('day', -30, current_timestamp())
    ;
    

Copy

  * Using the `object_id` value of `32998411400350`, determine when the access occurred in the last 30 days:
    
        SELECT query_id
           , query_start_time
    FROM access_history
         , lateral flatten(base_objects_accessed) f1
    WHERE f1.value:"objectId"::int=32998411400350
    AND f1.value:"objectDomain"::string='Table'
    AND query_start_time >= dateadd('day', -30, current_timestamp())
    ;
    

Copy

  * Using the `object_id` value of `32998411400350`, determine which columns were accessed in the last 30 days:
    
        SELECT distinct f4.value AS column_name
    FROM access_history
         , lateral flatten(base_objects_accessed) f1
         , lateral flatten(f1.value) f2
         , lateral flatten(f2.value) f3
         , lateral flatten(f3.value) f4
    WHERE f1.value:"objectId"::int=32998411400350
    AND f1.value:"objectDomain"::string='Table'
    AND f4.key='columnName'
    ;
    

Copy

## Examples: Write operations¶

The subsections below detail how to query the ACCESS_HISTORY view for write
operations for the following use cases:

  * Load data from a stage to a table.

  * Unload data from a table to a stage.

  * Use the PUT command to upload a local file to a stage.

  * Use the GET command to retrieve data files from a stage to a local directory.

  * Tracking sensitive stage data movement.

### Load data from a stage to a table¶

Load a set of values from a data file in external cloud storage into columns
in a target table.

>
>     copy into table1(col1, col2)
>     from (select t.$1, t.$2 from @mystage1/data1.csv.gz);
>  
>
> Copy

The `direct_objects_accessed` and `base_objects_accessed` column specify that
an external named stage was accessed:

>
>     {
>       "objectDomain": STAGE
>       "objectName": "mystage1",
>       "objectId": 1,
>       "stageKind": "External Named"
>     }
>  
>
> Copy

The `objects_modified` column specifies that data was written to two columns
of the table:

>
>     {
>       "columns": [
>          {
>            "columnName": "col1",
>            "columnId": 1
>          },
>          {
>            "columnName": "col2",
>            "columnId": 2
>          }
>       ],
>       "objectId": 1,
>       "objectName": "TEST_DB.TEST_SCHEMA.TABLE1",
>       "objectDomain": TABLE
>     }
>  
>
> Copy

### Unload data from a table to a stage¶

Unload a set of values from a Snowflake table into cloud storage.

>
>     copy into @mystage1/data1.csv
>     from table1;
>  
>
> Copy

The `direct_objects_accessed` and `base_objects_accessed` columns specify the
table columns that were accessed:

>
>     {
>       "objectDomain": TABLE
>       "objectName": "TEST_DB.TEST_SCHEMA.TABLE1",
>       "objectId": 123,
>       "columns": [
>          {
>            "columnName": "col1",
>            "columnId": 1
>          },
>          {
>            "columnName": "col2",
>            "columnId": 2
>          }
>       ]
>     }
>  
>
> Copy

The `objects_modified` column specifies the stage to which the accessed data
was written:

>
>     {
>       "objectId": 1,
>       "objectName": "mystage1",
>       "objectDomain": STAGE,
>       "stageKind": "External Named"
>     }
>  
>
> Copy

### Use the PUT Command to upload a local file to a stage¶

Copy a data file to an internal (i.e. Snowflake) stage.

>
>     put file:///tmp/data/mydata.csv @my_int_stage;
>  
>
> Copy

The `direct_objects_accessed` and `base_objects_accessed` columns specify the
local path to the file that was accessed:

>
>     {
>       "location": "file:///tmp/data/mydata.csv"
>     }
>  
>
> Copy

The `objects_modified` column specifies the stage where the accessed data was
written:

>
>     {
>       "objectId": 1,
>       "objectName": "my_int_stage",
>       "objectDomain": STAGE,
>       "stageKind": "Internal Named"
>     }
>  
>
> Copy

### Use the GET command to retrieve data files from a stage to a local
directory¶

Retrieve a data file from an internal stage to a directory on the local
machine.

>
>     get @%mytable file:///tmp/data/;
>  
>
> Copy

The `direct_objects_accessed` and `base_objects_accessed` columns specify the
stage and local directory that were accessed:

>
>     {
>       "objectDomain": Stage
>       "objectName": "mytable",
>       "objectId": 1,
>       "stageKind": "Table"
>     }
>  
>
> Copy

The `objects_modified` column specifies the directory to which the accessed
data was written:

>
>     {
>       "location": "file:///tmp/data/"
>     }
>  
>
> Copy

### Tracking Sensitive stage data movement¶

Track sensitive stage data as it moves through a series of queries executed in
chronological order.

Execute the following queries. Note that five of the statements access stage
data. Therefore, when you query the ACCESS_HISTORY view for stage access, the
result set should include five rows.

>
>     use test_db.test_schema;
>     create or replace table T1(content variant);
>     insert into T1(content) select parse_json('{"name": "A", "id":1}');
>  
>     -- T1 -> T6
>     insert into T6 select * from T1;
>  
>     -- S1 -> T1
>     copy into T1 from @S1;
>  
>     -- T1 -> T2
>     create table T2 as select content:"name" as name, content:"id" as id
> from T1;
>  
>     -- T1 -> S2
>     copy into @S2 from T1;
>  
>     -- S1 -> T3
>     create or replace table T3(customer_info variant);
>     copy into T3 from @S1;
>  
>     -- T1 -> T4
>     create or replace table T4(name string, id string, address string);
>     insert into T4(name, id) select content:"name", content:"id" from T1;
>  
>     -- T6 -> T7
>     create table T7 as select * from T6;
>  
>
> Copy
>
> Where:
>
>   * `T1`, `T2` … `T7` specify the names of tables.
>
>   * `S1` and `S2` specify the names of stages.
>
>

Query the access history to determine the access to stage `S1`.

> The data for the `direct_objects_accessed`, `base_objects_accessed`, and
> `objects_modified` columns are shown in the following table.
>
> `direct_objects_accessed` | `base_objects_accessed` | `objects_modified`  
> ---|---|---  
>  
>  
>     [
>       {
>         "columns": [
>           {
>             "columnId": 68610,
>             "columnName": "CONTENT"
>           }
>         ],
>         "objectDomain": "Table",
>         "objectId": 66564,
>         "objectName": "TEST_DB.TEST_SCHEMA.T1"
>       }
>     ]
>  
>
> Copy | 
>  
>  
>     [
>       {
>         "columns": [
>           {
>             "columnId": 68610,
>             "columnName": "CONTENT"
>           }
>         ],
>         "objectDomain": "Table",
>         "objectId": 66564,
>         "objectName": "TEST_DB.TEST_SCHEMA.T1"
>       }
>     ]
>  
>
> Copy | 
>  
>  
>     [
>       {
>         "columns": [
>           {
>             "columnId": 68611,
>             "columnName": "CONTENT"
>           }
>         ],
>         "objectDomain": "Table",
>         "objectId": 66566,
>         "objectName": "TEST_DB.TEST_SCHEMA.T6"
>       }
>     ]
>  
>
> Copy  
>  
>  
>     [
>       {
>         "objectDomain": "Stage",
>         "objectId": 117,
>         "objectName": "TEST_DB.TEST_SCHEMA.S1",
>         "stageKind": "External Named"
>       }
>     ]
>  
>
> Copy | 
>  
>  
>     [
>       {
>         "objectDomain": "Stage",
>         "objectId": 117,
>         "objectName": "TEST_DB.TEST_SCHEMA.S1",
>         "stageKind": "External Named"
>       }
>     ]
>  
>
> Copy | 
>  
>  
>     [
>       {
>         "columns": [
>           {
>             "columnId": 68610,
>             "columnName": "CONTENT"
>           }
>         ],
>         "objectDomain": "Table",
>         "objectId": 66564,
>         "objectName": "TEST_DB.TEST_SCHEMA.T1"
>       }
>     ]
>  
>
> Copy  
>  
>  
>     [
>       {
>         "columns": [
>           {
>             "columnId": 68610,
>             "columnName": "CONTENT"
>           }
>         ],
>         "objectDomain": "Table",
>         "objectId": 66564,
>         "objectName": "TEST_DB.TEST_SCHEMA.T1"
>       }
>     ]
>  
>
> Copy | 
>  
>  
>     [
>       {
>         "columns": [
>           {
>             "columnId": 68610,
>             "columnName": "CONTENT"
>           }
>         ],
>         "objectDomain": "Table",
>         "objectId": 66564,
>         "objectName": "TEST_DB.TEST_SCHEMA.T1"
>       }
>     ]
>  
>
> Copy | 
>  
>  
>     [
>       {
>         "columns": [
>           {
>             "columnId": 68613,
>             "columnName": "ID"
>           },
>           {
>             "columnId": 68612,
>             "columnName": "NAME"
>           }
>         ],
>         "objectDomain": "Table",
>         "objectId": 66568,
>         "objectName": "TEST_DB.TEST_SCHEMA.T2"
>       }
>     ]
>  
>
> Copy  
>  
>  
>     [
>       {
>         "columns": [
>           {
>             "columnId": 68610,
>             "columnName": "CONTENT"
>           }
>         ],
>         "objectDomain": "Table",
>         "objectId": 66564,
>         "objectName": "TEST_DB.TEST_SCHEMA.T1"
>       }
>     ]
>  
>
> Copy | 
>  
>  
>     [
>       {
>         "columns": [
>           {
>             "columnId": 68610,
>             "columnName": "CONTENT"
>           }
>         ],
>         "objectDomain": "Table",
>         "objectId": 66564,
>         "objectName": "TEST_DB.TEST_SCHEMA.T1"
>       }
>     ]
>  
>
> Copy | 
>  
>  
>     [
>       {
>         "objectDomain": "Stage",
>         "objectId": 118,
>         "objectName": "TEST_DB.TEST_SCHEMA.S2",
>         "stageKind": "External Named"
>       }
>     ]
>  
>
> Copy  
>  
>  
>     [
>       {
>         "objectDomain": "Stage",
>         "objectId": 117,
>         "objectName": "TEST_DB.TEST_SCHEMA.S1",
>         "stageKind": "External Named"
>       }
>     ]
>  
>
> Copy | 
>  
>  
>     [
>       {
>         "objectDomain": "Stage",
>         "objectId": 117,
>         "objectName": "TEST_DB.TEST_SCHEMA.S1",
>         "stageKind": "External Named"
>       }
>     ]
>  
>
> Copy | 
>  
>  
>     [
>       {
>         "columns": [
>           {
>             "columnId": 68614,
>             "columnName": "CUSTOMER_INFO"
>           }
>         ],
>         "objectDomain": "Table",
>         "objectId": 66570,
>         "objectName": "TEST_DB.TEST_SCHEMA.T3"
>       }
>     ]
>  
>
> Copy  
>  
>  
>     [
>       {
>         "columns": [
>           {
>             "columnId": 68610,
>             "columnName": "CONTENT"
>           }
>         ],
>         "objectDomain": "Table",
>         "objectId": 66564,
>         "objectName": "TEST_DB.TEST_SCHEMA.T1"
>       }
>     ]
>  
>
> Copy | 
>  
>  
>     [
>       {
>         "columns": [
>           {
>             "columnId": 68610,
>             "columnName": "CONTENT"
>           }
>         ],
>         "objectDomain": "Table",
>         "objectId": 66564,
>         "objectName": "TEST_DB.TEST_SCHEMA.T1"
>       }
>     ]
>  
>
> Copy | 
>  
>  
>     [
>       {
>         "columns": [
>           {
>             "columnId": 68615,
>             "columnName": "NAME"
>           },
>           {
>             "columnId": 68616,
>             "columnName": "ID"
>           }
>         ],
>         "objectDomain": "Table",
>         "objectId": 66572,
>         "objectName": "TEST_DB.TEST_SCHEMA.T4"
>       }
>     ]
>  
>
> Copy  
>  
>  
>     [
>       {
>         "columns": [
>           {
>             "columnId": 68611,
>             "columnName": "CONTENT"
>           }
>         ],
>         "objectDomain": "Table",
>         "objectId": 66566,
>         "objectName": "TEST_DB.TEST_SCHEMA.T6"
>       }
>     ]
>  
>
> Copy | 
>  
>  
>     [
>       {
>         "columns": [
>           {
>             "columnId": 68611,
>             "columnName": "CONTENT"
>           }
>         ],
>         "objectDomain": "Table",
>         "objectId": 66566,
>         "objectName": "TEST_DB.TEST_SCHEMA.T6"
>       }
>     ]
>  
>
> Copy | 
>  
>  
>     [
>       {
>         "columns": [
>           {
>             "columnId": 68618,
>             "columnName": "CONTENT"
>           }
>         ],
>         "objectDomain": "Table",
>         "objectId": 66574,
>         "objectName": "TEST_DB.TEST_SCHEMA.T7"
>       }
>     ]
>  
>
> Copy  
>  
> Note the following about the query example:
>
>   * Uses a [recursive common table expression](queries-cte).
>
>   * Uses a [JOIN](../sql-reference/constructs/join) construct rather than a
> [USING clause](../sql-reference/account-usage/access_history.html#label-
> acctuse-view-access-history-usage-notes).
>  
>     >     with access_history_flatten as (
>         select
>             r.value:"objectId" as source_id,
>             r.value:"objectName" as source_name,
>             r.value:"objectDomain" as source_domain,
>             w.value:"objectId" as target_id,
>             w.value:"objectName" as target_name,
>             w.value:"objectDomain" as target_domain,
>             c.value:"columnName" as target_column,
>             t.query_start_time as query_start_time
>         from
>             (select * from TEST_DB.ACCOUNT_USAGE.ACCESS_HISTORY) t,
>             lateral flatten(input => t.BASE_OBJECTS_ACCESSED) r,
>             lateral flatten(input => t.OBJECTS_MODIFIED) w,
>             lateral flatten(input => w.value:"columns", outer => true) c
>             ),
>         sensitive_data_movements(path, target_id, target_name,
> target_domain, target_column, query_start_time)
>         as
>           -- Common Table Expression
>           (
>             -- Anchor Clause: Get the objects that access S1 directly
>             select
>                 f.source_name || '-->' || f.target_name as path,
>                 f.target_id,
>                 f.target_name,
>                 f.target_domain,
>                 f.target_column,
>                 f.query_start_time
>             from
>                 access_history_flatten f
>             where
>             f.source_domain = 'Stage'
>             and f.source_name = 'TEST_DB.TEST_SCHEMA.S1'
>             and f.query_start_time >= dateadd(day, -30, date_trunc(day,
> current_date))
>             union all
>             -- Recursive Clause: Recursively get all the objects that access
> S1 indirectly
>             select sensitive_data_movements.path || '-->' || f.target_name
> as path, f.target_id, f.target_name, f.target_domain, f.target_column,
> f.query_start_time
>               from
>                  access_history_flatten f
>                 join sensitive_data_movements
>                 on f.source_id = sensitive_data_movements.target_id
>                     and f.source_domain =
> sensitive_data_movements.target_domain
>                     and f.query_start_time >=
> sensitive_data_movements.query_start_time
>           )
>     select path, target_name, target_id, target_domain, array_agg(distinct
> target_column) as target_columns
>     from sensitive_data_movements
>     group by path, target_id, target_name, target_domain;
>  
>
> Copy
>
>

>
> The query produces the following result set related to stage `S1` data
> movement:
>

>> PATH | TARGET_NAME | TARGET_ID | TARGET_DOMAIN | TARGET_COLUMNS  
>> ---|---|---|---|---  
>> TEST_DB.TEST_SCHEMA.S1–>TEST_DB.TEST_SCHEMA.T1 | TEST_DB.TEST_SCHEMA.T1 | 66564 | Table | [“CONTENT”]  
>> TEST_DB.TEST_SCHEMA.S1–>TEST_DB.TEST_SCHEMA.T1–>TEST_DB.TEST_SCHEMA.S2 | TEST_DB.TEST_SCHEMA.S2 | 118 | Stage | []  
>> TEST_DB.TEST_SCHEMA.S1–>TEST_DB.TEST_SCHEMA.T1–>TEST_DB.TEST_SCHEMA.T2 | TEST_DB.TEST_SCHEMA.T2 | 66568 | Table | [“NAME”,”ID”]  
>> TEST_DB.TEST_SCHEMA.S1–>TEST_DB.TEST_SCHEMA.T1–>TEST_DB.TEST_SCHEMA.T4 | TEST_DB.TEST_SCHEMA.T4 | 66572 | Table | [“ID”,”NAME”]  
>> TEST_DB.TEST_SCHEMA.S1–>TEST_DB.TEST_SCHEMA.T3 | TEST_DB.TEST_SCHEMA.T3 | 66570 | Table | [“CUSTOMER_INFO”]  
  
## Example: Column lineage¶

The following example queries the ACCESS_HISTORY view and uses the
[FLATTEN](../sql-reference/functions/flatten) function to flatten the
`objects_modified` column.

As a representative example, execute the following SQL query in your Snowflake
account to produce the table below, where the numbered comments indicate the
following:

  * `// 1`: Get the mapping between the `directSources` field and the target column.

  * `// 2`: Get the mapping between the `baseSources` field and the target column.

    
    
    // 1
    
    select
      directSources.value: "objectId" as source_object_id,
      directSources.value: "objectName" as source_object_name,
      directSources.value: "columnName" as source_column_name,
      'DIRECT' as source_column_type,
      om.value: "objectName" as target_object_name,
      columns_modified.value: "columnName" as target_column_name
    from
      (
        select
          *
        from
          snowflake.account_usage.access_history
      ) t,
      lateral flatten(input => t.OBJECTS_MODIFIED) om,
      lateral flatten(input => om.value: "columns", outer => true) columns_modified,
      lateral flatten(
        input => columns_modified.value: "directSources",
        outer => true
      ) directSources
    
    union
    
    // 2
    
    select
      baseSources.value: "objectId" as source_object_id,
      baseSources.value: "objectName" as source_object_name,
      baseSources.value: "columnName" as source_column_name,
      'BASE' as source_column_type,
      om.value: "objectName" as target_object_name,
      columns_modified.value: "columnName" as target_column_name
    from
      (
        select
          *
        from
          snowflake.account_usage.access_history
      ) t,
      lateral flatten(input => t.OBJECTS_MODIFIED) om,
      lateral flatten(input => om.value: "columns", outer => true) columns_modified,
      lateral flatten(
        input => columns_modified.value: "baseSources",
        outer => true
      ) baseSources
    ;
    

Copy

Returns:

> SOURCE_OBJECT_ID | SOURCE_OBJECT_NAME | SOURCE_COLUMN_NAME | SOURCE_COLUMN_TYPE | TARGET_OBJECT_NAME | TARGET_COLUMN_NAME  
> ---|---|---|---|---|---  
> 1 | D.S.T0 | NAME | BASE | D.S.T1 | NAME  
> 2 | D.S.V1 | NAME | DIRECT | D.S.T1 | NAME  
  
## Example: Track row access policy references¶

Return a row for each instance when a row access policy is set on a table,
view, or materialized view without duplicates:

>
>     use role accountadmin;
>     select distinct
>         obj_policy.value:"policyName"::VARCHAR as policy_name
>     from snowflake.account_usage.access_history as ah
>         , lateral flatten(ah.policies_referenced) as obj
>         , lateral flatten(obj.value:"policies") as obj_policy
>     ;
>  
>
> Copy

## Example: Track masking policy references¶

Return a row for each instance when a masking policy protects a column without
duplicates. Note that additional flattening is necessary because the
`policies_referenced` column specifies the masking policy on a column one
level deeper than the row access policy on a table:

>
>     use role accountadmin;
>     select distinct
>         policies.value:"policyName"::VARCHAR as policy_name
>     from snowflake.account_usage.access_history as ah
>         , lateral flatten(ah.policies_referenced) as obj
>         , lateral flatten(obj.value:"columns") as columns
>         , lateral flatten(columns.value:"policies") as policies
>     ;
>  
>
> Copy

## Example: Track the enforced policy in a query¶

Return the time when the policy was updated (POLICY_CHANGED_TIME) and the
policy conditions (POLICY_BODY) for a given query in a given time frame.

Prior to using this query, update the WHERE clause input values:

    
    
    where query_start_time > '2023-07-07' and
       query_start_time < '2023-07-08' and
       query_id = '01ad7987-0606-6e2c-0001-dd20f12a9777')
    

Copy

Where:

`query_start_time > '2023-07-07'`

    

Specifies the beginning timestamp.

`query_start_time < '2023-07-08'`

    

Specifies the end timestamp.

`query_id = '01ad7987-0606-6e2c-0001-dd20f12a9777'`

    

Specifies the query identifier in the Account Usage ACCESS_HISTORY view.

Run the query:

    
    
    SELECT *
    from(
      select j1.*,j2.QUERY_START_TIME as POLICY_CHANGED_TIME, POLICY_BODY
    from
    (
      select distinct t1.*,
          t4.value:"policyId"::number as PID
      from (select *
          from SNOWFLAKE.ACCOUNT_USAGE.ACCESS_HISTORY
          where query_start_time > '2023-07-07' and
             query_start_time < '2023-07-08' and
             query_id = '01ad7987-0606-6e2c-0001-dd20f12a9777') as t1, //
      lateral flatten (input => t1.POLICIES_REFERENCED,OUTER => TRUE) t2,
      lateral flatten (input => t2.value:"columns", OUTER => TRUE) t3,
      lateral flatten (input => t3.value:"policies",OUTER => TRUE) t4
    ) as j1
    left join
    (
      select OBJECT_MODIFIED_BY_DDL:"objectId"::number as PID,
          QUERY_START_TIME,
          OBJECT_MODIFIED_BY_DDL:"properties"."policyBody"."value" as POLICY_BODY
          from SNOWFLAKE.ACCOUNT_USAGE.ACCESS_HISTORY
          where OBJECT_MODIFIED_BY_DDL is not null and
          (OBJECT_MODIFIED_BY_DDL:"objectDomain" ilike '%masking%' or OBJECT_MODIFIED_BY_DDL:"objectDomain" ilike '%row%')
    ) as j2
    On j1.POLICIES_REFERENCED is not null and j1.pid = j2.pid and j1.QUERY_START_TIME>j2.QUERY_START_TIME) as j3
    QUALIFY ROW_NUMBER() OVER (PARTITION BY query_id,pid ORDER BY policy_changed_time DESC) = 1;
    

Copy

## Examples: UDFs¶

These UDF examples show how the Account Usage ACCESS_HISTORY view records:

  * Calling a UDF named `get_product`.

  * Insert the product of calling the `get_product` function into a table named `mydb.tables.t1`.

  * Shared UDFs.

### Call a UDF¶

Consider the following SQL UDF that calculates the product of two numbers and
assume it is stored in the schema named `mydb.udfs`:

>
>     CREATE FUNCTION MYDB.UDFS.GET_PRODUCT(num1 number, num2 number)
>     RETURNS number
>     AS
>     $$
>         NUM1 * NUM2
>     $$
>     ;
>  
>
> Copy

[Calling](../sql-reference/sql/call) `get_product` directly results in
recording the UDF details in the `direct_objects_accessed` column:

>
>     [
>       {
>         "objectDomain": "FUNCTION",
>         "objectName": "MYDB.UDFS.GET_PRODUCT",
>         "objectId": "2",
>         "argumentSignature": "(NUM1 NUMBER, NUM2 NUMBER)",
>         "dataType": "NUMBER(38,0)"
>       }
>     ]
>  
>
> Copy

This example is analogous to calling a stored procedure (in this topic).

### UDF with INSERT DML¶

Consider the following [INSERT](../sql-reference/sql/insert) statement to
update the columns named 1 and 2 in the table named `mydb.tables.t1`:

>
>     insert into t1(product)
>     select get_product(c1, c2) from mydb.tables.t1;
>  
>
> Copy

The ACCESS_HISTORY view records the `get_product` function in the:

  * `direct_objects_accessed` column because the function is explicitly named in the SQL statement, and

  * `objects_modified` column in the `directSources` array because the function is the source of the values that are inserted into the columns.

Similarly, the table `t1` is recorded in these same columns:

> `direct_objects_accessed` | `objects_modified`  
> ---|---  
>  
>  
>     [
>       {
>         "objectDomain": "FUNCTION",
>         "objectName": "MYDB.UDFS.GET_PRODUCT",
>         "objectId": "2",
>         "argumentSignature": "(NUM1 NUMBER, NUM2 NUMBER)",
>         "dataType": "NUMBER(38,0)"
>       },
>       {
>         "objectDomain": "TABLE",
>         "objectName": "MYDB.TABLES.T1",
>         "objectId": 1,
>         "columns":
>         [
>           {
>             "columnName": "c1",
>             "columnId": 1
>           },
>           {
>             "columnName": "c2",
>             "columnId": 2
>           }
>         ]
>       }
>     ]
>  
>
> Copy | 
>  
>  
>      [
>        {
>          "objectDomain": "TABLE",
>          "objectName": "MYDB.TABLES.T1",
>          "objectId": 2,
>          "columns":
>          [
>            {
>              "columnId": "product",
>              "columnName": "201",
>              "directSourceColumns":
>              [
>                {
>                  "objectDomain": "Table",
>                  "objectName": "MYDB.TABLES.T1",
>                  "objectId": "1",
>                  "columnName": "c1"
>                },
>                {
>                  "objectDomain": "Table",
>                  "objectName": "MYDB.TABLES.T1",
>                  "objectId": "1",
>                  "columnName": "c2"
>                },
>                {
>                  "objectDomain": "FUNCTION",
>                  "objectName": "MYDB.UDFS.GET_PRODUCT",
>                  "objectId": "2",
>                  "argumentSignature": "(NUM1 NUMBER, NUM2 NUMBER)",
>                  "dataType": "NUMBER(38,0)"
>                }
>              ],
>              "baseSourceColumns":[]
>            }
>          ]
>        }
>     ]
>  
>
> Copy  
  
### Shared UDFs¶

Shared UDFs can be referenced directly or indirectly:

  * A direct reference is the same as calling the UDF explicitly (in this topic) but results in the UDF being recorded in both the `base_objects_accessed` and `direct_objects_accessed` columns.

  * An example of an indirect reference is calling the UDF to create a view:

> >     create view v as
>     select get_product(c1, c2) as vc from t;
>  
>
> Copy

The `base_objects_accessed` column records the UDF and the table.

The `direct_objects_accessed` column records the view.

## Examples: Tracking objects modified by a DDL operation¶

### Create a tag with ALLOWED_VALUES¶

Create the tag:

>
>     create tag governance.tags.pii allowed_values 'sensitive','public';
>  
>
> Copy

Column value:

>
>     {
>       "objectDomain": "TAG",
>       "objectName": "governance.tags.pii",
>       "objectId": "1",
>       "operationType": "CREATE",
>       "properties": {
>         "allowedValues": {
>           "sensitive": {
>             "subOperationType": "ADD"
>           },
>           "public": {
>             "subOperationType": "ADD"
>           }
>         }
>       }
>     }
>  
>
> Copy

Note

If you do not specify allowed values when creating the tag, the `properties`
field is an empty array (i.e. `{}`).

### Create a table with a tag and masking policy¶

Create the table with a masking policy on the column, a tag on the column, and
a tag on the table:

>
>     create or replace table hr.data.user_info(
>       email string
>         with masking policy governance.policies.email_mask
>         with tag (governance.tags.pii = 'sensitive')
>       )
>     with tag (governance.tags.pii = 'sensitive');
>  
>
> Copy

Column value:

>
>     {
>       "objectDomain": "TABLE",
>       "objectName": "hr.data.user_info",
>       "objectId": "1",
>       "operationType": "CREATE",
>       "properties": {
>         "tags": {
>           "governance.tags.pii": {
>             "subOperationType": "ADD",
>             "objectId": {
>               "value": "1"
>             },
>             "tagValue": {
>               "value": "sensitive"
>             }
>           }
>         },
>         "columns": {
>           "email": {
>             objectId: {
>               "value": 1
>             },
>             "subOperationType": "ADD",
>             "tags": {
>               "governance.tags.pii": {
>                 "subOperationType": "ADD",
>                 "objectId": {
>                   "value": "1"
>                 },
>                 "tagValue": {
>                   "value": "sensitive"
>                 }
>               }
>             },
>             "maskingPolicies": {
>               "governance.policies.email_mask": {
>                 "subOperationType": "ADD",
>                 "objectId": {
>                   "value": 2
>                 }
>               }
>             }
>           }
>         }
>       }
>     }
>  
>
> Copy

### Set a masking policy on a tag¶

Set a masking policy on the tag (i.e. [tag-based masking](tag-based-masking-
policies)):

>
>     alter tag governance.tags.pii set masking policy
> governance.policies.email_mask;
>  
>
> Copy

Column value:

>
>     {
>       "objectDomain": "TAG",
>       "objectName": "governance.tags.pii",
>       "objectId": "1",
>       "operationType": "ALTER",
>       "properties": {
>         "maskingPolicies": {
>           "governance.policies.email_mask": {
>             "subOperationType": "ADD",
>             "objectId": {
>               "value": 2
>             }
>           }
>         }
>       }
>     }
>  
>
> Copy

### Swap a table¶

Swap the table named `t2` with the table named `t3`:

>
>     alter table governance.tables.t2 swap with governance.tables.t3;
>  
>
> Copy

Note the two different records in the view.

Record 1:

>
>     {
>       "objectDomain": "Table",
>       "objectId": 0,
>       "objectName": "GOVERNANCE.TABLES.T2",
>       "operationType": "ALTER",
>       "properties": {
>         "swapTargetDomain": {
>           "value": "Table"
>         },
>         "swapTargetId": {
>           "value": 0
>         },
>         "swapTargetName": {
>           "value": "GOVERNANCE.TABLES.T3"
>         }
>       }
>     }
>  
>
> Copy

Record 2:

>
>     {
>       "objectDomain": "Table",
>       "objectId": 0,
>       "objectName": "GOVERNANCE.TABLES.T3",
>       "operationType": "ALTER",
>       "properties": {
>         "swapTargetDomain": {
>           "value": "Table"
>         },
>         "swapTargetId": {
>           "value": 0
>         },
>         "swapTargetName": {
>           "value": "GOVERNANCE.TABLES.T2"
>         }
>       }
>     }
>  
>
> Copy

### Drop a masking policy¶

Drop the masking policy:

>
>     drop masking policy governance.policies.email_mask;
>  
>
> Copy

Column value:

>
>     {
>       "objectDomain" : "MASKING_POLICY",
>       "objectName": "governance.policies.email_mask",
>       "objectId" : "1",
>       "operationType": "DROP",
>       "properties" : {}
>     }
>  
>
> Copy
>
> Note
>
> The column value is representative and applies to a DROP operation on a tag
> and row access policy.
>
> The `properties` field is an empty array and does not provide any
> information on the policy prior to the DROP operation.

### Track tag references on a column¶

Query the `object_modified_by_ddl` column to monitor how a tag is set on a
column.

As the table administrator, set a tag on a column, unset the tag, and update
the tag with a different string value:

>
>     alter table hr.tables.empl_info
>       alter column email set tag governance.tags.test_tag = 'test';
>  
>     alter table hr.tables.empl_info
>       alter column email unset tag governance.tags.test_tag;
>  
>     alter table hr.tables.empl_info
>       alter column email set tag governance.tags.data_category =
> 'sensitive';
>  
>
> Copy

As the data engineer, change the tag value:

>
>     alter table hr.tables.empl_info
>       alter column email set tag governance.tags.data_category = 'public';
>  
>
> Copy

Query the ACCESS_HISTORY view to monitor the changes:

>
>     select
>       query_start_time,
>       user_name,
>       object_modified_by_ddl:"objectName"::string as table_name,
>       'EMAIL' as column_name,
>       tag_history.value:"subOperationType"::string as operation,
>       tag_history.key as tag_name,
>       nvl((tag_history.value:"tagValue"."value")::string, '') as value
>     from
>       TEST_DB.ACCOUNT_USAGE.access_history ah,
>       lateral flatten(input =>
> ah.OBJECT_MODIFIED_BY_DDL:"properties"."columns"."EMAIL"."tags") tag_history
>     where true
>       and object_modified_by_ddl:"objectDomain" = 'Table'
>       and object_modified_by_ddl:"objectName" = 'TEST_DB.TEST_SH.T'
>     order by query_start_time asc;
>  
>
> Copy

Returns:

>
>
> +-----------------------------------+---------------+---------------------+-------------+-----------+-------------------------------+-----------+
>     | QUERY_START_TIME                  | USER_NAME     | TABLE_NAME          | COLUMN_NAME | OPERATION | TAG_NAME                      | VALUE     |
>
> +-----------------------------------+---------------+---------------------+-------------+-----------+-------------------------------+-----------+
>     | Mon, Feb. 14, 2023 12:01:01 -0600 | TABLE_ADMIN   | HR.TABLES.EMPL_INFO | EMAIL       | ADD       | GOVERNANCE.TAGS.TEST_TAG      | test      |
>     | Mon, Feb. 14, 2023 12:02:01 -0600 | TABLE_ADMIN   | HR.TABLES.EMPL_INFO | EMAIL       | DROP      | GOVERNANCE.TAGS.TEST_TAG      |           |
>     | Mon, Feb. 14, 2023 12:03:01 -0600 | TABLE_ADMIN   | HR.TABLES.EMPL_INFO | EMAIL       | ADD       | GOVERNANCE.TAGS.DATA_CATEGORY | sensitive |
>     | Mon, Feb. 14, 2023 12:04:01 -0600 | DATA_ENGINEER | HR.TABLES.EMPL_INFO | EMAIL       | ADD       | GOVERNANCE.TAGS.DATA_CATEGORY | public    |
>
> +-----------------------------------+---------------+---------------------+-------------+-----------+-------------------------------+-----------+
>  

## Example: Call a stored procedure¶

Consider the following stored procedure and assume it is stored in the schema
named `mydb.procedures`:

>
>     create or replace procedure get_id_value(name string)
>     returns string not null
>     language javascript
>     as
>     $$
>       var my_sql_command = "select id from A where name = '" + NAME + "'";
>       var statement = snowflake.createStatement( {sqlText: my_sql_command}
> );
>       var result = statement.execute();
>       result.next();
>       return result.getColumnValue(1);
>     $$
>     ;
>  
>
> Copy

[Calling](../sql-reference/sql/call) `my_procedure` directly results in
recording the procedure details in both the `direct_objects_accessed` and
`base_objects_accessed` columns as follows:

>
>     [
>       {
>         "objectDomain": "PROCEDURE",
>         "objectName": "MYDB.PROCEDURES.GET_ID_VALUE",
>         "argumentSignature": "(NAME STRING)",
>         "dataType": "STRING"
>       }
>     ]
>  
>
> Copy

This example is analogous to calling a UDF (in this topic).

## Example: Ancestor queries with stored procedures¶

You can use the `parent_query_id` and `root_query_id` columns to understand
how stored procedure calls relate to each other.

Suppose that you have three different stored procedure statements and you run
them in the following order:

>
>     CREATE OR REPLACE PROCEDURE myproc_child()
>     RETURNS INTEGER
>     LANGUAGE SQL
>     AS
>     $$
>       BEGIN
>       SELECT * FROM mydb.mysch.mytable;
>       RETURN 1;
>       END
>     $$;
>  
>     CREATE OR REPLACE PROCEDURE myproc_parent()
>     RETURNS INTEGER
>     LANGUAGE SQL
>     AS
>     $$
>       BEGIN
>       CALL myproc_child();
>       RETURN 1;
>       END
>     $$;
>  
>     CALL myproc_parent();
>  
>
> Copy

A query on the ACCESS_HISTORY view records the information as follows:

>
>     SELECT
>       query_id,
>       parent_query_id,
>       root_query_id,
>       direct_objects_accessed
>     FROM
>       SNOWFLAKE.ACCOUNT_USAGE.ACCESS_HISTORY;
>  
>
> Copy
>  
>  
>
> +----------+-----------------+---------------+-----------------------------------+
>     | QUERY_ID | PARENT_QUERY_ID | ROOT_QUERY_ID | DIRECT_OBJECTS_ACCESSED           |
>
> +----------+-----------------+---------------+-----------------------------------+
>     |  1       | NULL            | NULL          | [{"objectName": "myproc_parent"}] |
>     |  2       | 1               | 1             | [{"objectName": "myproc_child"}]  |
>     |  3       | 2               | 1             | [{"objectName": "mytable"}]       |
>
> +----------+-----------------+---------------+-----------------------------------+
>  

  * The first row corresponds to calling the second procedure named `myproc_parent` as shown in the `direct_objects_accessed` column.

The `parent_query_id` and `root_query_id` columns return NULL because you
called this stored procedure directly.

  * The second row corresponds to the query that calls the first procedure named `myproc_child` as shown in the `direct_objects_accessed column`.

The `parent_query_id` and `root_query_id` columns return the same query ID
because the query calling `myproc_child` was initiated by the query calling
`myproc_parent`, which you called directly.

  * The third row corresponds to the query that accessed the table named `mytable` in the `myproc_child` procedure as shown in the `direct_objects_accessed` column.

The `parent_query_id` column returns the query ID of the query that accessed
`mytable`, which corresponds to calling `myproc_child`. That stored procedure
was initiated by the query calling `myproc_parent`, which is shown in the
`root_query_id` column.

## Example: Sequence¶

Consider the following SQL statement that creates a sequence:

    
    
    CREATE SEQUENCE SEQ
      START = 2
      INCREMENT = 7
      COMMENT = 'Comment on sequence';
    

Copy

Creating this sequence results in the following entry in the access history:

    
    
    {
      "objectDomain": "Sequence",
      "objectId": 1,
      "objectName": "TEST_DB.TEST_SCHEMA.SEQ",
      "operationType": "CREATE",
      "properties": {
        "start": {
          "value": "2"
        },
        "increment": {
            "value": "7"
        },
        "comment": {
              "value": "Comment on Sequence"
        }
      }
    }
    

Copy

