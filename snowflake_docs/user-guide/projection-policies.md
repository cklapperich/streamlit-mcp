# Projection policies¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Enterprise Edition
Feature](intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about
upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-
guide/contacting-support).

This topic shows how to use projection policies to allow or prevent column
projection in the final output of a SQL query result.

## Overview¶

A projection policy is a first-class, schema-level object that defines whether
a column can be projected in the output of a SQL query result. A column with a
projection policy assigned to it is said to be _projection constrained_.
Projection policies can be used to constrain sensitive or private information
(for example, name or phone number) when sharing when [sharing data
securely](data-sharing-gs) between partners.

However, note that columns that are hidden by projection policies can still be
used in inner queries or in WHERE clauses, which can disclose information
about a given field. For details, see the Considerations section (in this
topic).

After creating the projection policy, a policy administrator can assign the
projection policy to a column. A column can only have one projection policy
assigned to it at any given time. A user can project the column only if their
active role matches a projection policy condition that allows the column to be
projected.

Note that a projection constrained column can also be protected by a masking
policy and the table containing the projection constrained column can be
protected by a row access policy. For more details, see Masking & row access
policies (in this topic).

### Column usage¶

Snowflake tracks column usage. Indirect references to a column, such as a view
definition, UDF (in this topic), and common table expression, impact column
projection when a projection policy is set on a column.

When a projection policy is set on the column and the column cannot be
projected, the column:

  * Is not included in the output of a query result.

  * Cannot be inserted into another table.

  * Cannot be an argument for an external function or stored procedure.

### Limitations¶

  * For limitations regarding user-defined functions (UDFs), see User-defined functions (UDFs) (in this topic).

  * A projection policy cannot be applied to:

    * A tag assigned to a table or column (that is, a tag-based projection policy).

    * A virtual column or to the VALUE column in an external table. As a workaround, create a view and assign a projection policy to each column that should not be projected.

    * The `_value_column_` in a [PIVOT](../sql-reference/constructs/pivot) construct. For related details, see UNPIVOT (in this topic).

  * A projection policy `_body_` cannot reference a column protected by a masking policy or a table protected by a row access policy. For additional details, see Masking & row access policies (in this topic).

### Considerations¶

Use projection policies when the use case calls for querying a sensitive
column without directly exposing the column value to an analyst or similar
role. The column value within a projection constrained column can be analyzed
with greater flexibility than a masked or tokenized value. However, consider
the following prior to setting a projection policy on a column:

  * A projection policy does not prevent the targeting of an individual.

For example, a user can filter rows where the `name` column corresponds to a
particular individual, even if the column is projection constrained. However,
the user cannot run a SELECT statement to view names of the individuals in the
table.

  * When a projection constrained column is the join key for a query that combines data from the protected table with data from an unprotected table, nothing prevents the user from projecting values from the column in the unprotected table. As a result, if a value in the unprotected table matches a value in the protected column, the user can obtain that value by projecting it from the unprotected table.

For example, suppose a projection policy was assigned to the `email` column of
the `t_protected` table. A user can still ascertain values in the
`t_protected.email` column by executing:

> >     SELECT t_unprotected.email
>       FROM t_unprotected JOIN t_protected ON t_unprotected.email =
> t_protected.email;
>  
>
> Copy

  * A projection constraint does not guarantee that a malicious actor could not use deliberate queries to obtain potentially sensitive data from a projection-constrained column. Projection policies are best suited for use with partners and customers with whom you have an existing level of trust. In addition, providers should be vigilant about potential misuses of their data (e.g. reviewing the access history for their listings).

  * For all of these reasons, if you need to prevent leakage about a specific column or entity, you should omit the column entirely from your data, or employ [differential privacy](diff-privacy/differential-privacy-overview).

## Create a projection policy¶

A projection policy contains a `_body_` that calls the internal
PROJECTION_CONSTRAINT function to determine whether to project a column.

>
>     CREATE OR REPLACE PROJECTION POLICY <name>
>       AS () RETURNS PROJECTION_CONSTRAINT -> <body>
>  
>
> Copy
>
> Where:
>
>   * `_name_` specifies the name of the policy.
>
>   * `AS () RETURNS PROJECTION_CONSTRAINT` is the signature and return type
> of the policy. The signature does not accept any arguments and the return
> type is PROJECTION_CONSTRAINT, which is an internal data type. All
> projection policies have the same signature and return type.
>
>   * `_body_` is a SQL expression that determines whether to project the
> column. This can include CASE and other valid SQL statements, and can also
> include SELECT clauses that evaluate to TRUE or FALSE. **Do not return NULL
> to disallow projection.** You must return the internal PROJECTION_CONSTRAINT
> function with a parameter value that allows or prevents the projection of a
> column:
>
>     * `PROJECTION_CONSTRAINT(ALLOW => true)` allows projecting a column.
>
>     * `PROJECTION_CONSTRAINT(ALLOW => false)` does not allow projecting a
> column.
>
>

### Example policies¶

The simplest projection policies call the PROJECTION_CONSTRAINT function
directly:

Allow column projection

    
    
    
    CREATE OR REPLACE PROJECTION POLICY mypolicy
    AS () RETURNS PROJECTION_CONSTRAINT ->
    PROJECTION_CONSTRAINT(ALLOW => true)
    

Copy

Prevent column projection

    
    
    
    CREATE OR REPLACE PROJECTION POLICY mypolicy
    AS () RETURNS PROJECTION_CONSTRAINT ->
    PROJECTION_CONSTRAINT(ALLOW => false)
    

Copy

More complicated SQL expressions can be written to call the
PROJECTION_CONSTRAINT function. The expression can use [Conditional expression
functions](../sql-reference/expressions-conditional) and [Context
functions](../sql-reference/functions-context) to introduce logic to allow
certain users with a particular role to project a column and prevent all other
users from projecting a column.

> Tip
>
> You can use the following strategies when using context functions in a
> conditional policy:
>
>   * Context functions return strings, so comparisons using them are case-
> sensitive. You can use [LOWER](../sql-reference/functions/lower) to convert
> strings to all lowercase if you’d like to do a case-insensitive comparison.
>
>   * The [POLICY_CONTEXT](../sql-reference/functions/policy_context) function
> helps you evaluate whether a policy body is returning the correct value when
> a context function returns a certain value. The POLICY_CONTEXT function
> simulates query results based upon a specified value of one or more context
> functions.
>
>

The following example includes a [CASE](../sql-reference/functions/case)
expression and [CURRENT_ROLE](../sql-reference/functions/current_role) context
function to create a conditional policy that only allows users with the
`analyst` custom role to project a column:

>
>     CREATE OR REPLACE PROJECTION POLICY mypolicy
>     AS () RETURNS PROJECTION_CONSTRAINT ->
>     CASE
>       WHEN CURRENT_ROLE() = 'ANALYST'
>         THEN PROJECTION_CONSTRAINT(ALLOW => true)
>       ELSE PROJECTION_CONSTRAINT(ALLOW => false)
>     END;
>  
>
> Copy

The following example uses the [SYSTEM$GET_TAG_ON_CURRENT_COLUMN](../sql-
reference/functions/system_get_tag_on_current_column) function so that a tag
that is assigned to a column determines whether the column can be projected.
In this case, when the policy is assigned to a column, the value of the
`tags.accounting_col` tag on that column must be `public` in order to project
the column.

    
    
    CREATE PROJECTION POLICY mypolicy
    AS () RETURNS PROJECTION_CONSTRAINT ->
    CASE
      WHEN SYSTEM$GET_TAG_ON_CURRENT_COLUMN('tags.accounting_col') = 'public'
        THEN PROJECTION_CONSTRAINT(ALLOW => true)
      ELSE PROJECTION_CONSTRAINT(ALLOW => false)
    END;
    

Copy

For data sharing use cases, the provider can write a projection policy to
constrain column projection for all consumer accounts using the
[CURRENT_ACCOUNT](../sql-reference/functions/current_account) context
function, or selectively restrict column projection in specific shares using
the [INVOKER_SHARE](../sql-reference/functions/invoker_share) context
function. For example:

Restrict all consumer accounts

    

In this example, `provider.account` is the [account identifier](admin-account-
identifier.html#label-account-name) in the account name format:

    
    
    CREATE OR REPLACE PROJECTION POLICY restrict_consumer_accounts
    AS () RETURNS PROJECTION_CONSTRAINT ->
    CASE
      WHEN CURRENT_ACCOUNT() = 'provider.account'
        THEN PROJECTION_CONSTRAINT(ALLOW => true)
      ELSE PROJECTION_CONSTRAINT(ALLOW => false)
    END;
    

Copy

Restrict to specific shares

    

Consider a data sharing provider account that has a projection policy set on a
column of a secure view. There are two different shares (`SHARE1` and
`SHARE2`) that can access the secure view to support two different data
sharing consumers.

If a user in the data sharing consumer account attempts to project the column
through either share they can project the column, otherwise the column cannot
be projected:

    
    
    CREATE OR REPLACE PROJECTION POLICY projection_share
    AS () RETURNS PROJECTION_CONSTRAINT ->
    CASE
      WHEN INVOKER_SHARE() IN ('SHARE1', 'SHARE2')
        THEN PROJECTION_CONSTRAINT(ALLOW => true)
      ELSE PROJECTION_CONSTRAINT(ALLOW => false)
    END;
    

Copy

Query a separate table to determine the projection policy

    

You can use a SELECT query in your policy logic to help determine whether to
allow or block projection. If you query a table (a _mapping table_) in this
way, we recommend puting the mapping table in the same database as the
protected table. This is particularly important if the `_body_` section calls
[IS_DATABASE_ROLE_IN_SESSION](../sql-
reference/functions/is_database_role_in_session).

Here is an extended example of creating and populating a simple mapping table
of role names and projection permission, and then querying that table to
determine whether a column can be projected to the current user according to
their role.

    
    
    -- Create mapping table with two columns: role name, whether that role can project the column
    CREATE OR REPLACE TABLE roles_with_access(role string, allowed boolean)
    AS SELECT * FROM VALUES ('ACCOUNTADMIN', true), ('RANDOM_ROLE', false);
    
    -- Create a policy that queries the mapping table, and allows projection when current
    -- user role has an `allowed` value of TRUE.
    -- Note that the logic is written to default to FALSE in all other cases, including the
    -- current role not being in the queried table.
    CREATE OR REPLACE PROJECTION POLICY pp AS () RETURNS projection_constraint ->
      CASE WHEN
        exists(
          SELECT 1 FROM roles_with_access WHERE role = current_role() AND allowed = true
        ) THEN projection_constraint(ALLOW=>true)
      ELSE projection_constraint(ALLOW=>false) END;
    
    -- Create a new table with the policy and query it in one step.
    CREATE OR REPLACE TABLE t(user string, address string WITH PROJECTION POLICY pp)
      AS SELECT * FROM VALUES ('Carson', 'CA'), ('Emily', 'NY'), ('John', 'NV');
    
    -- Succeeds
    USE ROLE ACCOUNTADMIN;
    SELECT * FROM t;
    
    -- Fails with projection policy error on column ADDRESS
    USE ROLE any_other_role;
    SELECT * FROM t;
    

Copy

## Assign a projection policy¶

A projection policy is applied to a table column using an [ALTER TABLE … ALTER
COLUMN](../sql-reference/sql/alter-table-column) command and a view column
using an [ALTER VIEW](../sql-reference/sql/alter-view) command. Each column
supports only one projection policy.

>
>     ALTER { TABLE | VIEW } <name>
>     { ALTER | MODIFY } COLUMN <col1_name>
>     SET PROJECTION POLICY <policy_name> [ FORCE ]
>     [ , <col2_name> SET PROJECTION POLICY <policy_name> [ FORCE ] ... ]
>  
>
> Copy

Where:

  * `_name_` specifies the name of the table or view.

  * `_col1_name_` specifies the name of the column in the table or view.

  * `_col2_name_` specifies the name of an additional column in the table or view.

  * `_policy_name_` specifies the name of the projection policy set on the column.

  * `FORCE` is an optional parameter that allows the command to assign the projection policy to a column that already has a projection policy assigned to it. The new projection policy atomically replaces the existing one.

For example, to set a projection policy `proj_policy_acctnumber` on the
`account_number` column of a table:

>
>     ALTER TABLE finance.accounting.customers
>      MODIFY COLUMN account_number
>      SET PROJECTION POLICY proj_policy_acctnumber;
>  
>
> Copy

You can also use the WITH clause of the [CREATE TABLE](../sql-
reference/sql/create-table) and [CREATE VIEW](../sql-reference/sql/create-
view) commands to assign a projection policy to a column when the table or
view is created. For example, to assign the policy `my_proj_policy` to the
`account_number` column of a new table, execute:

>
>     CREATE TABLE t1 (account_number NUMBER WITH PROJECTION POLICY
> my_proj_policy);
>  
>
> Copy

You can also use the WITH clause when adding a new column to an existing
table. For example, to assign the policy `my_proj_policy` to the `zipcode`
column, which is being added to the existing table `customers`, execute:

>
>     ALTER TABLE customers ADD COLUMN account_number NUMBER WITH PROJECTION
> POLICY my_proj_policy;
>  
>
> Copy

### Replace a projection policy¶

The recommended method of replacing a projection policy is to use the `FORCE`
parameter to detach the existing projection policy and assign the new one in a
single command. This allows you to atomically replace the old policy, leaving
no gap in protection.

For example, to assign a new projection policy to a column that is already
projection-constrained:

    
    
    ALTER TABLE finance.accounting.customers
      MODIFY COLUMN account_number
      SET PROJECTION POLICY proj_policy2 FORCE;
    

Copy

You can also detach the projection policy from a column in one statement (…
UNSET PROJECTION POLICY) and then set a new policy on the column in a
different statement (… SET PROJECTION POLICY <name>). If you choose this
method, the column is not protected by a projection policy in between
detaching one policy and assigning another. A query could potentially access
sensitive data during this time.

## Detach a projection policy¶

Use the UNSET PROJECTION POLICY clause of an ALTER TABLE or ALTER VIEW command
to detach a projection policy from the column of a table or view. The name of
the projection policy is not required because a column cannot have more than
one projection policy attached.

>
>     ALTER { TABLE | VIEW } <name>
>     { ALTER | MODIFY } COLUMN <col1_name>
>     UNSET PROJECTION POLICY
>     [ , <col2_name> UNSET PROJECTION POLICY ... ]
>  
>
> Copy

Where:

  * `_name_` specifies the name of the table or view.

  * `_col1_name_` specifies the name of the column in the table or view.

  * `_col2_name_` specifies the name of an additional column in the table or view.

For example, to remove the projection policy from the `account_number` column:

>
>     ALTER TABLE finance.accounting.customers
>      MODIFY COLUMN account_number
>      UNSET PROJECTION POLICY;
>  
>
> Copy

## Monitor projection policies with SQL¶

It can be helpful to think of two general approaches to determine how to
monitor projection policy usage.

  * Discover projection policies

  * Identify projection policy references

### Discover projection policies¶

You can use the [PROJECTION_POLICIES](../sql-reference/account-
usage/projection_policies) view in the Account Usage schema of the shared
SNOWFLAKE database. This view is a _catalog_ for all projection policies in
your Snowflake account. For example:

>
>     SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.PROJECTION_POLICIES
>     ORDER BY POLICY_NAME;
>  
>
> Copy

### Identify projection policy references¶

The [POLICY_REFERENCES](../sql-reference/functions/policy_references)
Information Schema table function can identify projection policy references.
There are two different syntax options:

  1. Return a row for each object (i.e. table or view) that has the specified projection policy set on a column:
    
        USE DATABASE my_db;
    SELECT policy_name,
           policy_kind,
           ref_entity_name,
           ref_entity_domain,
           ref_column_name,
           ref_arg_column_names,
           policy_status
    FROM TABLE(information_schema.policy_references(policy_name => 'my_db.my_schema.projpolicy'));
    

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

## Extended example¶

Creating a projection policy and assigning the projection policy to a column
follows the same general procedure as creating and assigning other policies,
such as masking and row access policies:

  1. For a centralized management approach, create a custom role (e.g. `proj_policy_admin`) to manage the policy.

  2. Grant this role the privileges to create and assign a projection policy.

  3. Create the projection policy.

  4. Assign the projection policy to a column.

Based on this general procedure, complete the following steps to assign a
projection policy to a column:

  1. Create a custom role to manage the projection policy:
    
        USE ROLE useradmin;
    
    CREATE ROLE proj_policy_admin;
    

Copy

  2. Grant the `proj_policy_admin` custom role the privileges to create a projection policy in a schema and assign the projection policy to any table or view column in the Snowflake account.

This step assumes the projection policy will be stored in a database and
schema named `privacy.projpolicies` and this database and schema already
exist:

    
        GRANT USAGE ON DATABASE privacy TO ROLE proj_policy_admin;
    GRANT USAGE ON SCHEMA privacy.projpolicies TO ROLE proj_policy_admin;
    
    GRANT CREATE PROJECTION POLICY
      ON SCHEMA privacy.projpolicies TO ROLE proj_policy_admin;
    
    GRANT APPLY PROJECTION POLICY ON ACCOUNT TO ROLE proj_policy_admin;
    

Copy

For details, see Privileges and commands (in this topic).

  3. Create a projection policy to prevent column projection:
    
        USE ROLE proj_policy_admin;
    USE SCHEMA privacy.projpolicies;
    
    CREATE OR REPLACE PROJECTION POLICY proj_policy_false
    AS () RETURNS PROJECTION_CONSTRAINT ->
    PROJECTION_CONSTRAINT(ALLOW => false);
    

Copy

  4. Assign the projection policy to a table column:
    
        ALTER TABLE customers MODIFY COLUMN active
    SET PROJECTION POLICY privacy.projpolicies.proj_policy_false;
    

Copy

## Projection policies with Snowflake features¶

The following subsections briefly summarize how projection policies interact
with various Snowflake features and services.

### Masking & row access policies¶

This section describes how a projection policy interacts with a [masking
policy](security-column-intro) and a [row access policy](security-row-intro).

Multiple policies:

    

A column can have a masking policy and a projection policy at the same time,
and the table containing this column can be protected by a row access policy.
If all three policies are present, Snowflake processes the table and policies
as follows:

  1. Apply row filters according to the row access policy.

  2. Determine if the query is attempting to project any columns that are restricted by the projection policy, and if so, reject the query.

  3. Apply column masks according to the masking policy.

A column protected by a masking policy can also be projection constrained. For
example, a masking policy set on a column containing account numbers can have
a condition that allows users with the `finance_admin` custom role to see the
account numbers and another condition to replace the account numbers with a
hash for all other roles.

A projection policy can further restrict the column such that users with the
`analyst` custom role cannot project the column. Note that users with the
`analyst` custom role can still analyze the column by grouping hashes or
joining on these hashes.

Snowflake recommends that policy administrators work with internal compliance
and regulatory officers to determine the columns that should be projection
constrained.

Policy evaluation:

    

A projection constrained column cannot be referenced by a masking policy or a
row access policy when:

  * Assigning a row access policy to a table.

  * Enumerating one or more columns in a [conditional masking policy](security-column-intro.html#label-security-column-intro-cond-cols).

  * Performing a mapping table lookup.

As mentioned in the Limitations (in this topic), a projection policy `_body_`
cannot reference a column protected by a masking policy or a table protected
by a row access policy.

### Dependent objects with other projection policies¶

Consider the following series of objects:

> `base_table` » `v1` » `v2`
>
> Where:
>
>   * `v1` is a view built from the table named `base_table`.
>
>   * `v2` is a view built from `v1`.
>
>

If there is a query on a column in a view that is projection-constrained and
that column depends on a projection constrained column in `base_table`, the
view column will be projected only if both projection policies allow the
column to be projected.

Snowflake checks the column lineage chain all the way to the base table to
ensure that any references to the column are not projection constrained. If
any column in the lineage chain is projection constrained and the column is
not allowed to be projected, Snowflake blocks the query.

### Views & materialized views¶

A projection policy on a view column constrains the view column and not the
underlying base table column.

Regarding references, a projection policy that constrains a table column
carries over to a view that references the constrained table column.

### Streams & tasks¶

Projection policies on columns in a table carry over to a stream on the same
table. Note that a projection policy cannot be set on a stream.

Similarly, a projection constrained column remains constrained when a task
references the constrained column.

### UNPIVOT¶

The result of an [UNPIVOT](../sql-reference/constructs/unpivot) construct
depends on whether a column was initially constrained by a projection policy.
Note:

  * Constrained columns prior to and after executing UNPIVOT remain projection constrained.

  * The `_name_column_` always appears in the query result.

  * If any columns in the `_column_list_` are projection constrained, the `_value_column_` is also projection constrained.

### Cloned objects¶

The following approach helps to safeguard data from users with the SELECT
privilege on a cloned table or view that is stored in the cloned database or
schema:

  * Cloning an individual projection policy object is not supported.

  * Cloning a schema results in the cloning of all projection policies within the schema.

  * A cloned table maps to the same projection policies as the source table.

    * When a table is cloned in the context of its parent schema cloning, if the source table has a reference to a projection policy in the same parent schema (i.e. a local reference), the cloned table will have a reference to the cloned projection policy.

    * If the source table refers to a projection policy in a different schema (i.e. a foreign reference), then the cloned table retains the foreign reference.

For more information, see [CREATE <object> … CLONE](../sql-
reference/sql/create-clone).

### Replication¶

Projection policies and their assignments can be replicated using database
replication and replication groups.

For [database replication](database-replication-considerations), the
replication operation fails if either of the following conditions is true:

  * The primary database is in an Enterprise (or higher) account and contains a policy but one or more of the accounts approved for replication are on lower editions.

  * A table or view contained in the primary database has a [dangling reference](database-replication-considerations.html#label-database-replication-dangling-references) to a projection policy in another database.

The dangling reference behavior for database replication can be avoided when
replicating multiple databases in a [replication group](account-replication-
intro.html#label-replication-and-failover-groups).

### User-defined functions (UDFs)¶

Note the following regarding projection constraints and UDFs:

Scalar SQL UDFs:

    

Snowflake evaluates the UDF and then applies the projection policy to the
projection constrained column.

If a column in a SELECT statement is transitively derived from a UDF, which is
also derived from a projection constrained column, Snowflake blocks the query.
In other words:

`pc_column` » UDF » column (in SELECT statement)

Where:

  * `pc_column` refers to a projection constrained column.

Because the column in the SELECT statement can be traced to a projection
constrained column, Snowflake blocks the query.

SQL UDTFs:

    

SQL user-defined table functions (UDTF) follow the same behavior as SQL UDFs,
except that because rows are returned in the function output, Snowflake
evaluates each table column independently to determine whether to project the
column in the function output.

Other UDFs:

    

The following applies to [Introduction to Java UDFs](../developer-
guide/udf/java/udf-java-introduction), [Introduction to JavaScript
UDFs](../developer-guide/udf/javascript/udf-javascript-introduction),
[Introduction to Python UDFs](../developer-guide/udf/python/udf-python-
introduction):

  * A projection constrained column is constrained in the UDTF output.

Logging & Event Tables:

    

When a UDF, UDTF, or JavaScript UDF has a projection-constrained argument,
Snowflake does not capture log and event details in the corresponding event
table. However, Snowflake allows the UDF/UDTF to execute and does not fail the
statement calling the UDF/UDTF due to logging reasons.

## Privileges and commands¶

The following subsections provide information to help manage projection
policies.

### Projection policy privileges¶

Snowflake supports the following privileges on the projection policy object.

The USAGE privilege on the parent database and schema are required to perform
operations on any object in a schema.

Privilege | Usage  
---|---  
APPLY | Enables the set and unset operations for a projection policy on a column.  
OWNERSHIP | Transfers ownership of the projection policy, which grants full control over the projection policy. Required to alter most properties of a projection policy.  
  
For details, see Summary of DDL commands, operations, and privileges (in this
topic).

### Projection policy DDL reference¶

Snowflake supports the following DDL to create and manage projection policies.

  * [CREATE PROJECTION POLICY](../sql-reference/sql/create-projection-policy)

  * [ALTER PROJECTION POLICY](../sql-reference/sql/alter-projection-policy)

  * [DESCRIBE PROJECTION POLICY](../sql-reference/sql/desc-projection-policy)

  * [DROP PROJECTION POLICY](../sql-reference/sql/drop-projection-policy)

  * [SHOW PROJECTION POLICIES](../sql-reference/sql/show-projection-policies)

### Summary of DDL commands, operations, and privileges¶

The following table summarizes the relationship between projection policy
privileges and DDL operations.

The USAGE privilege on the parent database and schema are required to perform
operations on any object in a schema.

Operation | Privilege required  
---|---  
Create projection policy. | A role with the CREATE PROJECTION POLICY privilege in the same schema.  
Alter projection policy. | The role with the OWNERSHIP privilege on the projection policy.  
Describe projection policy | One of the following:

  * A role with the global APPLY PROJECTION POLICY privilege, or
  * A role with the OWNERSHIP privilege on the projection policy, or
  * A role with the APPLY privilege on the projection policy.

  
Drop projection policy. | A role with the OWNERSHIP privilege on the projection policy.  
Show projection policies. | One of the following:

  * A role with the USAGE privilege on the schema in which the projection policy exists, or
  * A role with the APPLY PROJECTION POLICY on the account.

  
Set or unset a projection policy on a column. | One of the following:

  * A role with the APPLY PROJECTION POLICY privilege on the account, or
  * A role with the APPLY privilege on the projection policy and the OWNERSHIP privilege on the table or view.

  
  
Snowflake supports different permissions to create and set a projection policy
on an object.

  1. For a centralized projection policy management approach in which the `projection_policy_admin` custom role creates and sets projection policies on all columns, the following permissions are necessary:
    
        USE ROLE securityadmin;
    GRANT USAGE ON DATABASE mydb TO ROLE projection_policy_admin;
    GRANT USAGE ON SCHEMA mydb.schema TO ROLE projection_policy_admin;
    
    GRANT CREATE PROJECTION POLICY ON SCHEMA mydb.schema TO ROLE projection_policy_admin;
    GRANT APPLY ON PROJECTION POLICY ON ACCOUNT TO ROLE projection_policy_admin;
    

Copy

  2. In a hybrid management approach, a single role has the CREATE PROJECTION POLICY privilege to ensure projection policies are named consistently and individual teams or roles have the APPLY privilege for a specific projection policy.

For example, the custom role `finance_role` role can be granted the permission
to set the projection policy `cost_center` on tables and views the role owns
(i.e. the role has the OWNERSHIP privilege on the table or view):

    
        USE ROLE securityadmin;
    GRANT CREATE PROJECTION POLICY ON SCHEMA mydb.schema TO ROLE projection_policy_admin;
    GRANT APPLY ON PROJECTION POLICY cost_center TO ROLE finance_role;
    

Copy

