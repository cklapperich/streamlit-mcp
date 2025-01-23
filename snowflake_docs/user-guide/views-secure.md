# Working with Secure Views¶

This topic covers concepts and syntax for defining views and materialized
views as secure.

## Overview of Secure Views¶

### Why Should I Use Secure Views?¶

  * For a non-secure view, internal optimizations can indirectly expose data.

Some of the internal optimizations for views require access to the underlying
data in the base tables for the view. This access might allow data that is
hidden from users of the view to be exposed through user code, such as user-
defined functions, or other programmatic methods. Secure views do not utilize
these optimizations, ensuring that users have no access to the underlying
data.

  * For a non-secure view, the view definition is visible to other users.

By default, the query expression used to create a standard view, also known as
the view definition or text, is visible to users in various commands and
interfaces. For details, see Interacting with Secure Views (in this topic).

For security or privacy reasons, you might not wish to expose the underlying
tables or internal structural details for a view. With secure views, the view
definition and details are visible only to authorized users (i.e. users who
are granted the role that owns the view).

### When Should I Use a Secure View?¶

Views should be defined as secure when they are specifically designated for
data privacy (i.e. to limit access to sensitive data that should not be
exposed to all users of the underlying table(s)).

Secure views should not be used for views that are defined solely for query
convenience, such as views created to simplify queries for which users do not
need to understand the underlying data representation. Secure views can
execute more slowly than non-secure views.

Tip

When deciding whether to use a secure view, you should consider the purpose of
the view and weigh the trade-off between data privacy/security and query
performance.

### How Might Data be Exposed by a Non-secure View?¶

Using the following widgets example, consider a user who has access to only
the red widgets. Suppose the user wonders if any purple widgets exist and
issues the following query:

    
    
    SELECT *
        FROM widgets_view
        WHERE 1/iff(color = 'Purple', 0, 1) = 1;
    

Copy

If any purple widgets exist, then the IFF() expression returns 0. The division
operation then fails due to a division-by-zero error, which allows the user to
infer that at least one purple widget exists.

## Creating Secure Views¶

Secure views are defined using the SECURE keyword with the standard DDL for
views:

  * To create a secure view, specify the SECURE keyword in the [CREATE VIEW](../sql-reference/sql/create-view) or [CREATE MATERIALIZED VIEW](../sql-reference/sql/create-materialized-view) command.

  * To convert an existing view to a secure view and back to a regular view, set/unset the SECURE keyword in the [ALTER VIEW](../sql-reference/sql/alter-view) or [ALTER MATERIALIZED VIEW](../sql-reference/sql/alter-materialized-view) command.

## Interacting with Secure Views¶

### Viewing the Definition for Secure Views¶

The definition of a secure view is only exposed to authorized users (i.e.
users who have been granted the role that owns the view). If an unauthorized
user uses any of the following commands or interfaces, the view definition is
not displayed:

  * [SHOW VIEWS](../sql-reference/sql/show-views) and [SHOW MATERIALIZED VIEWS](../sql-reference/sql/show-materialized-views) commands.

  * [GET_DDL](../sql-reference/functions/get_ddl) utility function.

  * [VIEWS](../sql-reference/info-schema/views) Information Schema view.

However, users that have been granted IMPORTED PRIVILEGES privilege on the
SNOWFLAKE database or another shared database have access to secure view
definitions via the [VIEWS](../sql-reference/account-usage/views) Account
Usage view.

Users granted the ACCOUNTADMIN role or the SNOWFLAKE.OBJECT_VIEWER database
role can also see secure view definitions via this view. The preferred, least-
privileged means of access is the SNOWFLAKE.OBJECT_VIEWER database role.

### Determining if a View is Secure¶

For non-materialized views, the `IS_SECURE` column in the Information Schema
and Account Usage views identifies whether a view is secure. For example, for
aview named `MYVIEW` in the `mydb` database:

> Information Schema:
>

>>

>>     select table_catalog, table_schema, table_name, is_secure

>>         from mydb.information_schema.views

>>         where table_name = 'MYVIEW';

>>  
>>

>> Copy

>
> Account Usage:
>

>>

>>     select table_catalog, table_schema, table_name, is_secure

>>         from snowflake.account_usage.views

>>         where table_name = 'MYVIEW';

>>  
>>

>> Copy

(For general information about the differences between INFORMATION_SCHEMA
views and ACCOUNT_USAGE views, see [Differences between Account Usage and
Information Schema](../sql-reference/account-usage.html#label-differences-
between-account-usage-and-information-schema).)

Alternatively, you can use the SHOW VIEWS command to view similar information
(note that the view name is case-insensitive):

>
>     SHOW VIEWS LIKE 'myview';
>  
>
> Copy

For materialized views, use the SHOW MATERIALIZED VIEWS command to identify
whether a view is secure. For example:

>
>     SHOW MATERIALIZED VIEWS LIKE 'my_mv';
>  
>
> Copy

### Viewing Secure View Details in Query Profile¶

The internals of a secure view are not exposed in [Query Profile](ui-
snowsight-activity) (in the web interface). This is the case even for the
owner of the secure view, because non-owners might have access to an owner’s
Query Profile.

## Using Secure Views with Snowflake Access Control¶

View security can be integrated with Snowflake users and roles using the
[CURRENT_ROLE](../sql-reference/functions/current_role) and
[CURRENT_USER](../sql-reference/functions/current_user) context functions. The
following example illustrates using roles to control access to the rows of a
table. In addition to the table that contains the data (`widgets`), the
example uses an access table (`widget_access_rules`) to track which roles have
access to which rows in the data table:

    
    
    CREATE TABLE widgets (
        id NUMBER(38,0) DEFAULT widget_id_sequence.nextval, 
        name VARCHAR,
        color VARCHAR,
        price NUMBER(38,0),
        created_on TIMESTAMP_LTZ(9));
    CREATE TABLE widget_access_rules (
        widget_id NUMBER(38,0),
        role_name VARCHAR);
    CREATE OR REPLACE SECURE VIEW widgets_view AS
        SELECT w.*
            FROM widgets AS w
            WHERE w.id IN (SELECT widget_id
                               FROM widget_access_rules AS a
                               WHERE upper(role_name) = CURRENT_ROLE()
                          )
        ;
    

Copy

The WHERE clause limits which widgets each role can see.

Suppose that a user who has access only to red widgets executes the query
shown earlier:

    
    
    SELECT *
        FROM widgets_view
        WHERE 1/iff(color = 'Purple', 0, 1) = 1;
    

Copy

The secure view’s WHERE clause is executed before any WHERE clause in the
user’s query. Because purple widgets are excluded by the view, the user’s
query never generates a division-by-zero error.

If the view were not secure, then the Snowflake optimizer could re-order the
predicates in the WHERE clauses. This could allow the predicate in the user’s
query to execute first, which would allow the division-by-zero error to occur.

## Best Practices for Using Secure Views¶

Secure views prevent users from possibly being exposed to data from rows of
tables that are filtered by the view. However, there are still ways that a
data owner might inadvertently expose information about the underlying data if
views are not constructed carefully. This section discusses some potential
pitfalls to avoid.

To illustrate these pitfalls, this section uses the sample `widgets` tables
and view defined in the earlier examples in this topic.

### Sequence-generated Columns¶

A common practice for generating surrogate keys is to use a sequence or auto-
increment column. If these keys are exposed to users who do not have access to
all of the underlying data, then a user might be able to guess details of the
underlying data distribution. For example, `widgets_view` exposes the ID
column. If ID is generated from a sequence, then a user of `widgets_view`
could deduce the total number of widgets created between the creation
timestamps of two widgets that the user has access to. Consider the following
query and result:

>
>     select * from widgets_view order by created_on;
>  
>
> ------+-----------------------+-------+-------+-------------------------------+
>       ID  |         NAME          | COLOR | PRICE |          CREATED_ON           |
>
> ------+-----------------------+-------+-------+-------------------------------+
>     ...
>      315  | Small round widget    | Red   | 1     | 2017-01-07 15:22:14.810 -0700 |
>      1455 | Small cylinder widget | Blue  | 2     | 2017-01-15 03:00:12.106 -0700 |
>     ...
>  
>
> Copy

Based on the result, the user might suspect that 1139 widgets (1455 - 315)
were created between January 7 and January 15. If this information is too
sensitive to expose to users of a view, you can use any of the following
alternatives:

  * Do not expose the sequence-generated column as part of the view.

  * Use randomized identifiers (e.g. generated by [UUID_STRING](../sql-reference/functions/uuid_string)) instead of sequence-generated values.

  * Programmatically obfuscate the identifiers.

### Scanned Data Size¶

For queries containing secure views, Snowflake does not expose the amount of
data scanned (either in terms of bytes or micro-partitions) or the total
amount of data. This is to protect the information from users who only have
access to a subset of the data. However, users might still be able to make
observations about the quantity of underlying data based on performance
characteristics of queries. For example, a query that runs twice as long might
process twice as much data. While any such observations are approximate at
best, in some cases it might be undesirable for even this level of information
to be exposed.

In such cases, it is best to materialize data per user/role instead of
exposing views on the base data to users. In the case of the `widgets` table,
a table would be created for each role that has access to widgets, which
contains only the widgets accessible by that role, and a role would be granted
access to its table. This is much more cumbersome than using a single view,
but for extremely high-security situations, this might be warranted.

### Secure Views and Data Sharing¶

When using secure views with [Secure Data Sharing](../guides-overview-
sharing), use the [CURRENT_ACCOUNT](../sql-
reference/functions/current_account) function to authorize users from a
specific account to access rows in a base table.

> Note
>
> When using the [CURRENT_ROLE](../sql-reference/functions/current_role) and
> [CURRENT_USER](../sql-reference/functions/current_user) functions with
> secure views that will be shared to other Snowflake accounts, Snowflake
> returns a NULL value for these functions. The reason is that the owner of
> the data being shared does not typically control the users or roles in the
> account with which the view is being shared.

