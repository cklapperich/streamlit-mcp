# Aggregation policies¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Enterprise Edition
Feature](intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about
upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-
guide/contacting-support).

An aggregation policy is a schema-level object that controls what type of
query can access data from a table or view. When an aggregation policy is
applied to a table, queries against that table must aggregate data into groups
of a minimum size in order to return results, thereby preventing a query from
returning information from an individual record. A table or view with an
aggregation policy assigned to it is said to be _aggregation-constrained_.

Aggregation policies can be used with or without an entity key. When
aggregation policies are used without an entity key, they protect the privacy
of individual rows in the data set (that is, row-level privacy). If you use an
aggregation policy with an entity key, it protects the privacy of an entity,
even if information about that entity appears in multiple rows (that is,
entity-level privacy).

For more information about combining aggregation policies with an entity key,
see [Implementing entity-level privacy with aggregation policies](aggregation-
policies-entity-privacy).

## Overview¶

A core feature of Snowflake is the ability to share data sets with other
entities. Aggregation policies allow a provider (data owner) to exercise
control over what can be done with their data even after it is shared with a
consumer. Specifically, the provider can require a consumer of a table to
aggregate the data rather than retrieve individual records.

When creating an aggregation policy, the provider’s policy administrator
specifies a minimum group size (i.e. the number of rows that must be
aggregated together into a group). The larger the minimum group size, the less
likely it is that a consumer could use the query results to deduce the
contents of a single record. Once the aggregation policy is applied to a table
or view, a query against it must conform to two requirements:

  * The query must aggregate the data. If the query uses an aggregation function, it must be one of the allowed aggregation functions.

  * Each group created by the query must include the aggregate of at least X records, where X is the minimum group size of the aggregation policy.

If the query returns a group that contains fewer records than the minimum
group size of the policy, then Snowflake combines those groups into a
_remainder group_. Snowflake applies the aggregation function to the
appropriate column to return a value for the remainder group. However, because
that value is calculated from rows that belong to more than one group, the
value of the GROUP BY key column is NULL. For example, if the query includes
the clause `GROUP BY state`, then the value of `state` in the remainder group
is NULL.

A query that does not return enough results to populate a remainder group
still works, but returns a NULL value in every field of the results.

### Limitations¶

  * You cannot protect an external table with an aggregation policy.

  * If the query uses an explicit grouping construct, it must be a [GROUP BY](../sql-reference/constructs/group-by) clause. The query cannot use related constructs like [GROUP BY ROLLUP](../sql-reference/constructs/group-by-rollup), [GROUP BY CUBE](../sql-reference/constructs/group-by-cube), or [GROUP BY GROUPING SETS](../sql-reference/constructs/group-by-grouping-sets).

  * Most [set operators](../sql-reference/operators-query) are not allowed when one of the queries acts on an aggregation-constrained table. As an exception, UNION ALL is supported, but each result group must satisfy the minimum group size of the aggregation-constrained tables being queried (see Query requirements for details).

  * If a column of an aggregation-constrained table is protected by a [projection policy](projection-policies), a query against that table cannot use the column as an argument of the COUNT function.

  * [Recursive CTEs](queries-cte.html#label-recursive-common-table-expression) are not allowed in queries against an aggregation-constrained table or view.

  * [Window functions](../sql-reference/functions-window) are not allowed in queries against an aggregation-constrained table or view.

  * A query against an aggregation-constrained table cannot use a [correlated subquery](querying-subqueries.html#label-correlated-vs-uncorrelated-subqueries) or [lateral join](../sql-reference/constructs/join-lateral) when there are references to or from the portion of the query that meets the requirements of the aggregation policy. The following examples illustrate the types of queries that are prohibited.

Example 1

    

Assuming `protected_table` is aggregation-constrained, the following query is
not allowed because the portion of the query that aggregates data references
another part of the query outside of the subquery:

    
        SELECT c1, c2
    FROM open_table
    WHERE c1 = (SELECT x FROM protected_table WHERE y = open_table.c2);
    

Copy

Example 2

    

Assuming `protected_table` is aggregation-constrained, the following query is
not allowed because the subquery references the part of the query that
aggregates data, which is outside of the subquery:

    
        SELECT
      SUM(SELECT COUNT(*) FROM open_table ot WHERE pt.id = ot.id)
    FROM protected_table pt;
    

Copy

### Considerations¶

Consider the following when using aggregation policies to protect sensitive
data:

  * Aggregation policies protect data for an individual record, not an entity. If a data set contains multiple records belonging to the same entity, an aggregation policy only protects the privacy of a specific record pertaining to that entity, not the entire entity.

  * While aggregation policies limit access to individual records, they do not guarantee a malicious actor could not use deliberate queries to obtain potentially sensitive data from an aggregation-constrained table. With enough query attempts, a malicious actor could potentially work around the aggregation requirements to ascertain a value from an individual row. Aggregation policies are best suited for use with partners and customers with whom you have an existing level of trust. In addition, providers should be vigilant about potential misuses of their data (for example, reviewing the access history for their listings).

## Create an aggregation policy¶

The syntax for creating an aggregation policy is:

>
>     CREATE [ OR REPLACE ] AGGREGATION POLICY <name>
>       AS () RETURNS AGGREGATION_CONSTRAINT -> <body>
>       [ COMMENT = '<string_literal>' ];
>  
>
> Copy

Where:

  * `_name_` specifies the name of the policy.

  * `AS () RETURNS AGGREGATION_CONSTRAINT` is the signature and return type of the policy. The signature does not accept any arguments and the return type is AGGREGATION_CONSTRAINT, which is an internal data type. All aggregation policies have the same signature and return type.

  * `_body_` is a SQL expression that determines the restrictions of an aggregation policy.

### Calling functions from the body¶

The body of an aggregation policy uses two functions to define the constraints
of the policy: NO_AGGREGATION_CONSTRAINT and AGGREGATION_CONSTRAINT. When the
conditions of the body call one of these functions, the return value from the
function determines how queries against the aggregation-constrained table or
view must be formulated to return results.

NO_AGGREGATION_CONSTRAINT

    

Use the body’s expression to call the NO_AGGREGATION_CONSTRAINT function when
you want a query to have unrestricted access to the table or view to which the
aggregation policy is assigned.

AGGREGATION_CONSTRAINT

    

Use the body’s expression to call the AGGREGATION_CONSTRAINT function to
require that queries aggregate data in order to return results. Use the
MIN_GROUP_SIZE argument to specify how many rows or [entities](aggregation-
policies-entity-privacy) must be included in each aggregation group.

For the complete syntax for the NO_AGGREGATION_CONSTRAINT and
AGGREGATION_CONSTRAINT functions, see [CREATE AGGREGATION POLICY](../sql-
reference/sql/create-aggregation-policy).

Note

The body of an aggregation policy cannot reference a user-defined function,
table, or view.

### Example policies¶

Fixed minimum group size

    

The simplest aggregation policy calls the AGGREGATION_CONSTRAINT function
directly and defines a constant minimum group size that is applied to all
queries against the table. For example, the following command creates an
aggregation policy with a minimum group size of 5:

>
>     CREATE AGGREGATION POLICY my_agg_policy
>       AS () RETURNS AGGREGATION_CONSTRAINT ->
> AGGREGATION_CONSTRAINT(MIN_GROUP_SIZE => 5);
>  
>
> Copy

Conditional policy

    

Policy administrators can define the SQL expression of an aggregation policy
so different queries have different restrictions based on factors such as the
role of the user executing the query. This strategy can allow one user to
query a table without restriction while requiring others to aggregate results.

For example, the following aggregation policy gives users with the role
`ADMIN` unrestricted access to a table while requiring all other queries to
aggregate data into groups of at least 5 rows or entities.

    
    
    CREATE AGGREGATION POLICY my_agg_policy
      AS () RETURNS AGGREGATION_CONSTRAINT ->
        CASE
          WHEN CURRENT_ROLE() = 'ADMIN'
            THEN NO_AGGREGATION_CONSTRAINT()
          ELSE AGGREGATION_CONSTRAINT(MIN_GROUP_SIZE => 5)
        END;
    

Copy

Tip

You can use the following strategies when using context functions like
[CURRENT_ROLE](../sql-reference/functions/current_role) in a conditional
policy:

  * Context functions return strings, so comparisons using them are case-sensitive. You can use [LOWER](../sql-reference/functions/lower) to convert strings to all lowercase if you’d like to do a case-insensitive comparison.

  * The [POLICY_CONTEXT](../sql-reference/functions/policy_context) function helps you evaluate whether a policy body is returning the correct value when a context function returns a certain value. The POLICY_CONTEXT function simulates query results based upon a specified value of one or more context functions.

## Modify an aggregation policy¶

You can use the [ALTER AGGREGATION POLICY](../sql-reference/sql/alter-
aggregation-policy) command to modify the SQL expression that determines the
minimum group size of the aggregation policy. You can also rename the policy
or change its comment.

Before modifying an aggregation policy, you can execute the [DESCRIBE
AGGREGATION POLICY](../sql-reference/sql/desc-aggregation-policy) command or
[GET_DDL](../sql-reference/functions/get_ddl) function to review the current
SQL expression of the policy. The SQL expression that determines the minimum
group size appears in the `BODY` column.

As an example, you can execute the following command to change the SQL
expression of the aggregation policy `my_policy` to require a minimum group
size of 2 rows in all circumstances:

>
>     ALTER AGGREGATION POLICY my_policy SET BODY ->
> AGGREGATION_CONSTRAINT(MIN_GROUP_SIZE=>2);
>  
>
> Copy

## Assign an aggregation policy¶

Once created, an aggregation policy can be applied to one or more tables or
views to make it aggregation-constrained. A table or view can only have one
aggregation policy attached.

Use the SET AGGREGATION POLICY clause of a [ALTER TABLE](../sql-
reference/sql/alter-table) or [ALTER VIEW](../sql-reference/sql/alter-view)
command to assign an aggregation policy to an existing table or view:

>
>     ALTER { TABLE | VIEW } <name> SET AGGREGATION POLICY <policy_name> [ FORCE ]
>  
>
> Copy

Where:

  * `_name_` specifies the name of the table or view.

  * `_policy_name_` specifies the name of the aggregation policy.

  * `FORCE` is an optional parameter that allows the command to assign the aggregation policy to a table or view that already has an aggregation policy assigned to it. The new aggregation policy atomically replaces the existing one.

For example, to assign the policy `my_agg_policy` to the table `t1`, execute:

>
>     ALTER TABLE t1 SET AGGREGATION POLICY my_agg_policy;
>  
>
> Copy

You can also use the WITH clause of the [CREATE TABLE](../sql-
reference/sql/create-table) and [CREATE VIEW](../sql-reference/sql/create-
view) commands to assign an aggregation policy to a table or view at creation
time. For example, to assign the policy `my_agg_policy` to a new table,
execute:

>
>     CREATE TABLE t1 WITH AGGREGATION POLICY my_agg_policy;
>  
>
> Copy

### Replace an aggregation policy¶

The recommended method of replacing an aggregation policy is to use the
`FORCE` parameter to detach the existing aggregation policy and assign the new
one in a single command. This allows you to atomically replace the old policy,
leaving no gap in protection.

For example, to assign a new aggregation policy to a table that is already
aggregation-constrained:

    
    
    ALTER TABLE privacy SET AGGREGATION POLICY agg_policy_2 FORCE;
    

Copy

You can also detach the aggregation policy from a table or view in one
statement (… UNSET AGGREGATION POLICY) and then set a new policy on the table
or view in a different statement (… SET AGGREGATION POLICY <name>). If you
choose this method, the table is not protected by an aggregation policy in
between detaching one policy and assigning another. A query could potentially
access sensitive data during this time.

## Detach an aggregation policy¶

Use the UNSET AGGREGATION POLICY clause of an ALTER TABLE or ALTER VIEW
command to detach an aggregation policy from a table or view in order to
remove the need to aggregate data. The name of the aggregation policy is not
required because a table or view cannot have more than one aggregation policy
attached.

>
>     ALTER {TABLE | VIEW} <name> UNSET AGGREGATION POLICY
>  
>
> Copy

Where:

  * `_name_` specifies the name of the table or view.

For example, to detach an aggregation policy from view `v1`, execute:

>
>     ALTER VIEW v1 UNSET AGGREGATION POLICY;
>  
>
> Copy

## Monitor aggregation policies¶

It can be helpful to think of two general approaches to determine how to
monitor aggregation policy usage.

  * Discover aggregation policies

  * Identify aggregation policy references

### Discover aggregation policies¶

You can use the [AGGREGATION_POLICIES](../sql-reference/account-
usage/aggregation_policies) view in the Account Usage schema of the shared
SNOWFLAKE database. This view is a _catalog_ for all aggregation policies in
your Snowflake account. For example:

>
>     SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.AGGREGATION_POLICIES
>     ORDER BY POLICY_NAME;
>  
>
> Copy

### Identify aggregation policy references¶

The [POLICY_REFERENCES](../sql-reference/functions/policy_references)
Information Schema table function can identify aggregation policy references.
There are two different syntax options:

  1. Return a row for each object (i.e. table or view) that has the specified aggregation policy set on it:
    
        USE DATABASE my_db;
    USE SCHEMA information_schema;
    SELECT policy_name,
           policy_kind,
           ref_entity_name,
           ref_entity_domain,
           ref_column_name,
           ref_arg_column_names,
           policy_status
    FROM TABLE(information_schema.policy_references(policy_name => 'my_db.my_schema.aggpolicy'));
    

Copy

  2. Return a row for each policy assigned to the table named `my_table`:
    
        USE DATABASE my_db;
    USE SCHEMA information_schema;
    SELECT policy_name,
           policy_kind,
           ref_entity_name,
           ref_entity_domain,
           ref_column_name,
           ref_arg_column_names,
           policy_status
    FROM TABLE(information_schema.policy_references(ref_entity_name => 'my_db.my_schema.my_table', ref_entity_domain => 'table'));
    

Copy

## Query requirements¶

After an aggregation policy has been applied to a table or view, queries
against that table or view must conform to certain requirements. This section
discusses what is and isn’t allowed in a query against an aggregation-
constrained table or view.

Note

Once part of the query properly aggregates data to satisfy the requirements of
the aggregation policy, these query restrictions do not apply, and another
part of the query can include things that are otherwise prohibited.

For example, the following query can use a SELECT statement that does not
aggregate results because another part of the query has already satisfied the
aggregation requirements of the policy that is assigned to `protected_table`:

    
    
    SELECT * FROM open_table ot WHERE ot.a > (SELECT SUM(id) FROM protected_table pt)
    

Copy

For additional restrictions on what can be included in a query, refer to
Limitations.

Aggregation Functions

    

The following aggregation functions are allowed in a query against an
aggregation-constrained table:

  * [AVG](../sql-reference/functions/avg)

  * [COUNT [DISTINCT]](../sql-reference/functions/count)

  * [HLL](../sql-reference/functions/hll)

  * [SUM](../sql-reference/functions/sum)

A query can contain more than one of these allowed aggregation functions. A
query fails if it attempts to use an aggregation function that is not allowed.

Grouping Statement

    

A query against an aggregation-constrained table must aggregate data into
groups of a minimum size. It can use an explicit grouping statement (i.e. a
GROUP BY clause) or a scalar aggregation function that aggregates the entire
data set (e.g. `COUNT(*)`).

Filters

    

In general, Snowflake does not restrict how a query uses WHERE and ON clauses
to filter the aggregation-constrained table as long as it aggregates the rows
selected by the filter.

Joins

    

A query can join an aggregation-constrained table with another table,
including another aggregation-constrained table.

Snowflake checks each aggregation group to make sure that the number of rows
taken from an aggregation-constrained table meets or exceeds the minimum group
size of that table. For example, if an aggregation-constrained table `table_a`
with a minimum group size of 5 is joined with `table_b` with a minimum group
size of 3, each group returned by the query must be created using at least 5
rows from `table_a` and 3 rows from `table_b`.

Whether a query with a join meets the requirements of an aggregation-
constrained table is determined by the number of rows taken from the table,
not the size of a group. As a result, the size of a group created from the
joined data could be greater than the minimum group size of the aggregation-
constrained table, but still result in filtered data. For example, suppose:

  * `agg_t` is aggregation constrained with a minimum group size of 2. This table contains a single integer column `c` that has the following content: { `1`, `2`, `2` }.

  * `open_t` is unconstrained, and contains an integer column `c` with the following content: { `1`, `1`, `1`, `2` }.

A user executes the following query that joins the two tables:

    
    
    SELECT c, COUNT(*)
    FROM agg_t, open_t
    WHERE agg_t.c = open_t.c
    GROUP BY agg_t.c;
    

Copy

The query will return:

    
    
    +-----------------+
    |  c   | COUNT(*) |
    |------+----------|
    |  2   |  2       |
    |------+----------|
    | null |  3       |
    +-----------------+
    

Even though the second group has 3 records, which is greater than the minimum
group size, all of those records correspond to a single record in the
aggregation-constrained table, so the value is filtered out.

UNION ALL

    

A query can use [UNION ALL](../sql-reference/operators-query.html#label-query-
operators-union) to combine results of two subqueries, even if one or more of
the queried tables are aggregation-constrained. Similar to joins, each group
in the results must satisfy the minimum group size of every aggregation-
constrained table being queried. For example, suppose:

  * Table `protected_table1` has a minimum group size of 2.

  * Table `protected_table2` has a minimum group size of 5.

If you run the query:

    
    
    SELECT a, COUNT(*)
    FROM (
        SELECT a, b FROM protected_table1
        UNION ALL
        SELECT a, b FROM protected_table2
    )
    GROUP BY a;
    

Copy

Each group formed by the key `a` must contain 2 records from
`protected_table1` and 5 records from `protected_table2`, otherwise the
records are placed in a remainder group.

External Functions

    

A query cannot call an [external function](../sql-reference/external-
functions-introduction) unless another part of the query has properly
aggregated results to meet the requirements of the aggregation-constrained
table.

Logging & Metrics

    

A query cannot log a column of an aggregation-constrained table via UDF
logging or metrics.

Data Type Conversions

    

A query that includes a data type conversion function in the SELECT statement
must use the TRY version of the function. For example, the TRY_CAST function
is allowed, but the CAST function is prohibited. The following data type
conversion functions are allowed for numeric types:

  * [TRY_CAST](../sql-reference/functions/try_cast)

  * [TRY_TO_DECIMAL](../sql-reference/functions/try_to_decimal)

  * [TRY_TO_DOUBLE](../sql-reference/functions/try_to_double)

  * [TRY_TO_NUMBER](../sql-reference/functions/try_to_decimal)

  * [TRY_TO_NUMERIC](../sql-reference/functions/try_to_decimal)

PIVOT

    

A query cannot use the [PIVOT](../sql-reference/constructs/pivot) operator
against a column in an aggregation-constrained table.

## Extended example¶

Creating an aggregation policy and assigning the aggregation policy to a table
follows the same general procedure as creating and assigning other policies,
such as masking and projection policies:

  1. If you are using a centralized management approach, create a custom role (e.g. `agg_policy_admin`) to manage the policy. Alternatively, you can use an existing role.

  2. Grant this role the privileges to create and assign an aggregation policy.

  3. Create the aggregation policy.

  4. Assign the aggregation policy to a table.

Once the aggregation policy is assigned to a table, successful queries against
the table must aggregate its data.

The following extended example provides insight into each step in this
process, from the provider’s access control administrator creating a custom
role to a data consumer executing a query to return aggregated results.

Access Control Administrator Tasks

    

  1. Create a custom role to manage the aggregation policy. You could also re-use an existing role.
    
        USE ROLE USERADMIN;
    
    CREATE ROLE AGG_POLICY_ADMIN;
    

Copy

  2. Grant the `agg_policy_admin` custom role the privileges to create an aggregation policy in a schema and assign the aggregation policy to a table or view in the Snowflake account.

This step assumes the aggregation policy will be stored in a database and
schema named `privacy.agg_policies` and this database and schema already
exist:

    
        GRANT USAGE ON DATABASE privacy TO ROLE agg_policy_admin;
    GRANT USAGE ON SCHEMA privacy.agg_policies TO ROLE agg_policy_admin;
    
    GRANT CREATE AGGREGATION POLICY
      ON SCHEMA privacy.agg_policies TO ROLE agg_policy_admin;
    
    GRANT APPLY AGGREGATION POLICY ON ACCOUNT TO ROLE agg_policy_admin;
    

Copy

The `agg_policy_admin` role can now be assigned to one or more users.

For details about the privileges needed to work with aggregation policies,
refer to Privileges and commands (in this topic).

Aggregation Policy Administrator Tasks

    

  1. Create an aggregation policy to require aggregation and define a minimum group size of 3:

> >     USE ROLE agg_policy_admin;
>     USE SCHEMA privacy.aggpolicies;
>  
>     CREATE AGGREGATION POLICY my_policy
>       AS () RETURNS AGGREGATION_CONSTRAINT ->
> AGGREGATION_CONSTRAINT(MIN_GROUP_SIZE => 3);
>  
>
> Copy

  2. Assign the aggregation policy to a table `t1`:

> >     ALTER TABLE t1 SET AGGREGATION POLICY my_policy;
>  
>
> Copy

Consumer Query

    

Once the provider shares the aggregation-constrained table, the data consumer
can execute queries against it. For this example, assume the aggregation-
constrained table `t1` contains the following rows:

peak | state | elevation  
---|---|---  
washington | NH | 6288  
cannon | NH | 4080  
kearsarge | NH | 2937  
mansfield | VT | 4395  
killington | VT | 4229  
wachusett | MA | 2006  
  
Now, assume that the consumer executes the following query against `t1`:

>
>     SELECT state, AVG(elevation) AS avg_elevation
>     FROM t1
>     GROUP BY state;
>  
>
> Copy

The results are:

>
>     +----------+-----------------+
>     |  STATE   |  AVG_ELEVATION  |
>     |----------+-----------------+
>     |  NH      |  4435           |
>     |  NULL    |  3543           |
>     +----------+-----------------+
>  

Note that the value of `state` in the second group is `NULL` because it is a
remainder group that averages the elevation of peaks in both `VT` and `MA`.

## Aggregation policies with Snowflake features¶

The following subsections briefly summarize how aggregation policies interact
with various Snowflake features and services.

### Other policies¶

This section describes how an aggregation policy interacts with other
policies, including [masking policies](security-column-intro), [row access
policies](security-row-intro), and [projection policies](projection-policies).

You can attach other policies to an aggregation-constrained table. A
successful query against the table must meet the requirements of all policies.

If a row access policy is assigned to an aggregation-constrained table, a row
excluded from the query results based on the row access policy is not included
when calculating the aggregated results.

The body of a masking policy, row access policy, or projection policy cannot
reference an aggregation-constrained table, including its columns. Similarly,
the body of the other policy cannot include a UDF that references the
aggregation-constrained table.

### Views and materialized views¶

You can assign an aggregation policy to both views and materialized views.
When an aggregation policy is applied to a view, the underlying table does not
become aggregation-constrained. This base table can still be queried without
restriction.

To avoid the possibility of exposing sensitive data, all aggregation-
constrained views are treated as if they are [secure views](views-secure) even
if they are not.

Whether you can create a view from an aggregation-constrained table depends on
the type of view:

>   * You can create a regular view from one or more aggregation-constrained
> tables, however queries against that view must aggregate data in a way that
> meets the restrictions of those base tables.
>
>   * You cannot create a materialized view based on an aggregation-
> constrained table or view, nor can you assign an aggregation policy to a
> table or view upon which a materialized view is based.
>
>

### Cloned objects¶

The following approach helps to safeguard data from users with the SELECT
privilege on a cloned table or view that is stored in the cloned database or
schema:

  * Cloning an individual aggregation policy object is not supported.

  * Cloning a database results in the cloning of all aggregation policies within the database.

  * Cloning a schema results in the cloning of all aggregation policies within the schema.

  * A cloned table maps to the same aggregation policies as the source table.

    * When a table is cloned in the context of its parent schema cloning, if the source table has a reference to an aggregation policy in the same parent schema (i.e. a local reference), the cloned table will have a reference to the cloned aggregation policy.

    * If the source table refers to an aggregation policy in a different schema (i.e. a foreign reference), then the cloned table retains the foreign reference.

For more information, see [CREATE <object> … CLONE](../sql-
reference/sql/create-clone).

### Replication¶

Aggregation policies and their assignments can be replicated using database
replication and replication groups.

For [database replication](database-replication-considerations), the
replication operation fails if either of the following conditions is true:

  * The primary database is in an Enterprise (or higher) account and contains a policy but one or more of the accounts approved for replication are on lower editions.

  * A table or view contained in the primary database has a [dangling reference](database-replication-considerations.html#label-database-replication-dangling-references) to an aggregation policy in another database.

The dangling reference behavior for database replication can be avoided when
replicating multiple databases in a [replication group](account-replication-
intro.html#label-replication-and-failover-groups).

## Privileges and commands¶

The following subsections provide information to help manage aggregation
policies.

### Aggregation policy privileges¶

Snowflake supports the following privileges on the aggregation policy object.

The USAGE privilege on the parent database and schema are required to perform
operations on any object in a schema.

Privilege | Usage  
---|---  
APPLY | Enables the set and unset operations for an aggregation policy on a table.  
OWNERSHIP | Transfers ownership of the aggregation policy, which grants full control over the aggregation policy. Required to alter most properties of an aggregation policy.  
  
For details, see Summary of DDL commands, operations, and privileges (in this
topic).

### Aggregation policy DDL reference¶

Snowflake supports the following DDL to create and manage aggregation
policies.

  * [CREATE AGGREGATION POLICY](../sql-reference/sql/create-aggregation-policy)

  * [ALTER AGGREGATION POLICY](../sql-reference/sql/alter-aggregation-policy)

  * [DESCRIBE AGGREGATION POLICY](../sql-reference/sql/desc-aggregation-policy)

  * [DROP AGGREGATION POLICY](../sql-reference/sql/drop-aggregation-policy)

  * [SHOW AGGREGATION POLICIES](../sql-reference/sql/show-aggregation-policies)

### Summary of DDL commands, operations, and privileges¶

The following table summarizes the relationship between aggregation policy
privileges and DDL operations.

The USAGE privilege on the parent database and schema are required to perform
operations on any object in a schema.

Operation | Privilege required  
---|---  
Create aggregation policy. | A role with the CREATE AGGREGATION POLICY privilege in the same schema.  
Alter aggregation policy. | The role with the OWNERSHIP privilege on the aggregation policy.  
Describe aggregation policy | One of the following:

  * A role with the global APPLY AGGREGATION POLICY privilege, or
  * A role with the OWNERSHIP privilege on the aggregation policy, or
  * A role with the APPLY privilege on the aggregation policy.

  
Drop aggregation policy. | A role with the OWNERSHIP privilege on the aggregation policy.  
Show aggregation policies. | One of the following:

  * A role with the USAGE privilege on the schema in which the aggregation policy exists, or
  * A role with the APPLY AGGREGATION POLICY on the account.

  
Set or unset an aggregation policy on a table. | One of the following:

  * A role with the APPLY AGGREGATION POLICY privilege on the account, or
  * A role with the APPLY privilege on the aggregation policy and the OWNERSHIP privilege on the table or view.

  
  
Snowflake supports different permissions to create and set an aggregation
policy on an object.

  1. For a centralized aggregation policy management approach in which the `aggregation_policy_admin` custom role creates and sets aggregation policies on all tables, the following permissions are necessary:
    
        USE ROLE securityadmin;
    GRANT USAGE ON DATABASE mydb TO ROLE agg_policy_admin;
    GRANT USAGE ON SCHEMA mydb.schema TO ROLE proj_policy_admin;
    GRANT CREATE AGGREGATION POLICY ON SCHEMA mydb.schema TO ROLE aggregation_policy_admin;
    GRANT APPLY ON AGGREGATION POLICY ON ACCOUNT TO ROLE aggregation_policy_admin;
    

Copy

  2. In a hybrid management approach, a single role has the CREATE AGGREGATION POLICY privilege to ensure aggregation policies are named consistently and individual teams or roles have the APPLY privilege for a specific aggregation policy.

For example, the custom role `finance_role` role can be granted the permission
to set the aggregation policy `cost_center` on tables and views the role owns
(i.e. the role has the OWNERSHIP privilege on the table or view):

    
        USE ROLE securityadmin;
    GRANT CREATE AGGREGATION POLICY ON SCHEMA mydb.schema TO ROLE aggregation_policy_admin;
    GRANT APPLY ON AGGREGATION POLICY cost_center TO ROLE finance_role;
    

Copy

