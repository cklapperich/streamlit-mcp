# Overview of Access Control¶

This topic provides information on the main access control topics in
Snowflake.

## Access control framework¶

Snowflake’s approach to access control combines aspects from both of the
following models:

  * **Discretionary Access Control (DAC):** Each object has an owner, who can in turn grant access to that object.

  * **Role-based Access Control (RBAC):** Access privileges are assigned to roles, which are in turn assigned to users.

The key concepts to understanding access control in Snowflake are:

  * **Securable object:** An entity to which access can be granted. Unless allowed by a grant, access is denied.

  * **Role:** An entity to which privileges can be granted. Roles are in turn assigned to users. Note that roles can also be assigned to other roles, creating a role hierarchy.

  * **Privilege:** A defined level of access to an object. Multiple distinct privileges may be used to control the granularity of access granted.

  * **User:** A user identity recognized by Snowflake, whether associated with a person or program.

In the Snowflake model, access to securable objects is allowed via privileges
assigned to roles, which are in turn assigned to users or other roles.
Granting a role to another role creates a role hierarchy, which is explained
in the Role hierarchy and privilege inheritance section (in this topic).

In addition, each securable object has an owner that can grant access to other
roles. This model is different from a user-based access control model in which
rights and privileges are assigned to each user or groups of users. The
Snowflake model is designed to provide a significant amount of both control
and flexibility.

> ![Access control relationships](../_images/access-control-relationships.png)

## Securable objects¶

Every securable object resides within a logical container in a hierarchy of
containers. The top-most container is the customer organization. Securable
objects such as tables, views, functions, and stages are contained in a schema
object, which are in turn contained in a database. All databases for your
Snowflake account are contained in the account object. This hierarchy of
objects and containers is illustrated below:

> [![Hierarchy of securable database objects](../_images/securable-objects-
> hierarchy.png)](../_images/securable-objects-hierarchy.png)

To _own_ an object means that a role has the OWNERSHIP privilege on the
object. Each securable object is owned by a single role, which by default is
the role used to create the object. When this role is assigned to users, they
effectively have shared control over the object. The [GRANT OWNERSHIP](../sql-
reference/sql/grant-ownership) command lets you transfer the ownership of an
object from one role to another role, including to database roles. This
command also specifies the securable objects in each container.

Note

[Private notebooks](ui-snowsight/notebooks-private) are owned by a user, and
not by their primary role.

In a regular schema, the owner role has all privileges on the object by
default, including the ability to grant or revoke privileges on the object to
other roles. In addition, ownership can be transferred from one role to
another. However, in a [managed access schema](security-access-control-
configure.html#label-managed-access-schemas), object owners lose the ability
to make grant decisions. Only the schema owner (i.e. the role with the
OWNERSHIP privilege on the schema) or a role with the MANAGE GRANTS privilege
can grant privileges on objects in the schema.

The ability to perform SQL actions on objects is defined by the privileges
granted to the active role in a user session. The following are examples of
SQL actions available on various objects in Snowflake:

  * Ability to create a warehouse.

  * Ability to list tables contained in a schema.

  * Ability to add data to a table.

## Roles¶

Roles are the entities to which privileges on securable objects can be granted
and revoked. Roles are assigned to users to allow them to perform actions
required for business functions in their organization. A user can be assigned
multiple roles. This allows users to switch roles (i.e. choose which role is
active in the current Snowflake session) to perform different actions using
separate sets of privileges.

There are a small number of system-defined roles in a Snowflake account.
System-defined roles cannot be dropped. In addition, the privileges granted to
these roles by Snowflake cannot be revoked.

Users who have been granted a role with the necessary privileges can create
custom roles to meet specific business and security needs.

Roles can be also granted to other roles, creating a hierarchy of roles. The
privileges associated with a role are inherited by any roles above that role
in the hierarchy. For more information about role hierarchies and privilege
inheritance, see Role Hierarchy and Privilege Inheritance (in this topic).

Note

A role owner (i.e. the role that has the OWNERSHIP privilege on the role) does
not inherit the privileges of the owned role. Privilege inheritance is only
possible within a role hierarchy.

Although additional privileges can be granted to the system-defined roles, it
is not recommended. System-defined roles are created with privileges related
to account-management. As a best practice, it is not recommended to mix
account-management privileges and entity-specific privileges in the same role.
If additional privileges are needed, Snowflake recommends granting the
additional privileges to a custom role and assigning the custom role to the
system-defined role.

### Types of roles¶

The following role types vary in their scope, which enable administrators to
authorize and restrict access to objects in your account.

Note

Except where noted in the product documentation, the term _role_ refers to
either type.

Account roles:

    

To permit SQL actions on any object in your account, grant privileges on the
object to an account role.

Database roles:

    

To limit SQL actions to a single database, as well as any object in the
database, grant privileges on the object to a database role in the same
database.

Note that database roles cannot be activated directly in a session. Grant
database roles to account roles, which can be activated in a session.

For more information about database roles, see:

  * Role hierarchy and privilege inheritance (in this topic)

  * Database roles and role hierarchies (in this topic)

  * [Managing database object access using database roles](security-access-control-considerations.html#label-access-control-considerations-database-roles)

  * Database roles in the shared [SNOWFLAKE database](../sql-reference/snowflake-db-roles).

  * [CREATE <object> … CLONE](../sql-reference/sql/create-clone)

Instance roles:

    

To permit access to an instance of a [class](../sql-reference/snowflake-db-
classes), grant an instance role to an account role.

A class may have one or more class roles with different privileges granted to
each role. When an instance of a class is created, the instance role(s) can be
granted to account roles to grant access to instance methods.

Note that instance roles cannot be activated directly in a session. Grant
instance roles to account roles, which can be activated in a session.

For more information, see [Instance roles](../sql-reference/snowflake-db-
classes.html#label-instance-roles).

Application roles:

    

To enable consumer access to objects in a Snowflake Native App, the provider
creates the application role and grants privileges to the application role in
the [set up script](../developer-guide/native-apps/creating-setup-script).

However, to support specific functionality for a particular feature, such as
granting access to objects in which Snowflake is the owner, Snowflake can
provide one or more _system application roles_. You can grant the system
application roles to account roles at your discretion.

System application roles are discussed in the context of a specific feature
because that specific feature is the only place where you can use the system
application role(s). For example:

  * Budgets: [Application roles to manage the account budget](budgets.html#label-budgets-application-roles).

  * Data Quality and data metric functions (DMFs): [View the DMF results](data-quality-working.html#label-data-quality-view-results).

Service roles:

    

To allow a role access to service endpoints, grant the service role to that
role. You can grant a service role to an account role, an application role, or
a database role. For more information, see [Managing access to service
endpoints](../developer-guide/snowpark-container-services/working-with-
services.html#label-snowpark-containers-service-endpoint-access).

### Active roles¶

_Active roles_ serve as the source of authorization for any action taken by a
user in a session. Both the primary role and any secondary roles can be
activated in a user session.

A role becomes an active role in either of the following ways:

  * When a session is first established, the user’s default role and default secondary roles are activated as the session primary and secondary roles, respectively.

Note that client connection properties used to establish the session could
explicitly override the primary role or secondary roles to use.

  * Executing a [USE ROLE](../sql-reference/sql/use-role) or [USE SECONDARY ROLES](../sql-reference/sql/use-secondary-roles) statement activates a different primary role or secondary roles, respectively. These roles can change over the course of a session if either command is executed again.

### System-defined roles¶

GLOBALORGADMIN:

    

(aka Organization Administrator in an [organization account](organization-
accounts))

Role that manages operations of a multi-account organization at the
organization level, including managing the lifecycle of accounts and viewing
organization-level usage information.

ORGADMIN:

    

(aka Organization Administrator in a regular account)

Role that manages operations at the organization level. More specifically,
this role:

  * Can [create accounts](organizations-manage-accounts-create) in the organization.

  * Can view all accounts in the organization (using [SHOW ACCOUNTS](../sql-reference/sql/show-accounts)) as well as all regions enabled for the organization (using [SHOW REGIONS](../sql-reference/sql/show-regions)).

  * Can view [usage information](../sql-reference/organization-usage) across the organization.

ACCOUNTADMIN:

    

(aka Account Administrator)

Role that encapsulates the SYSADMIN and SECURITYADMIN system-defined roles. It
is the top-level role in the system and should be granted only to a
limited/controlled number of users in your account.

SECURITYADMIN:

    

(aka Security Administrator)

Role that can manage any object grant globally, as well as create, monitor,
and manage users and roles. More specifically, this role:

  * Is granted the MANAGE GRANTS security privilege to be able to modify any grant, including revoking it.

Note

The MANAGE GRANTS privilege provides the ability to grant and revoke
privileges. It does not give the SECURITYADMIN the ability to perform other
actions such as creating objects. To create an object, the SECURITYADMIN role
must also be granted the privileges needed to create the object. For example,
to create a database role, the SECURITYADMIN must also be granted the CREATE
DATABASE ROLE privilege, as described in [CREATE DATABASE ROLE Access control
requirements](../sql-reference/sql/create-database-role.html#label-create-
database-role-access-control-reqs).

  * Inherits the privileges of the USERADMIN role via the system role hierarchy (i.e. USERADMIN role is granted to SECURITYADMIN).

USERADMIN:

    

(aka User and Role Administrator)

Role that is dedicated to user and role management only. More specifically,
this role:

  * Is granted the CREATE USER and CREATE ROLE security privileges.

  * Can create users and roles in the account.

This role can also manage users and roles that it owns. Only the role with the
OWNERSHIP privilege on an object (i.e. user or role), or a higher role, can
modify the object properties.

SYSADMIN:

    

(aka System Administrator)

Role that has privileges to create warehouses and databases (and other
objects) in an account.

If, as [recommended](security-access-control-considerations), you create a
role hierarchy that ultimately assigns all custom roles to the SYSADMIN role,
this role also has the ability to grant privileges on warehouses, databases,
and other objects to other roles.

PUBLIC:

    

Pseudo-role that is automatically granted to every user and every role in your
account. The PUBLIC role can own securable objects, just like any other role;
however, the objects owned by the role are, by definition, available to every
other user and role in your account.

This role is typically used in cases where explicit access control is not
needed and all users are viewed as equal with regard to their access rights.

### Custom roles¶

Custom account roles can be created using the USERADMIN role (or a higher
role) as well as by any role to which the CREATE ROLE privilege has been
granted.

Custom database roles can be created by the database owner (i.e. the role that
has the OWNERSHIP privilege on the database).

By default, a newly-created role is not assigned to any user, nor granted to
any other role.

When creating roles that will serve as the owners of securable objects in the
system, Snowflake recommends creating a hierarchy of custom roles, with the
top-most custom role assigned to the system role SYSADMIN. This role structure
allows system administrators to manage all objects in the account, such as
warehouses and database objects, while restricting management of users and
roles to the USERADMIN role.

Conversely, if a custom role is not assigned to SYSADMIN through a role
hierarchy, the system administrators cannot manage the objects owned by the
role. Only those roles granted the MANAGE GRANTS privilege (only the
SECURITYADMIN role by default) can view the objects and modify their access
grants.

For instructions to create custom roles, see [Creating custom roles](security-
access-control-configure.html#label-security-custom-role).

## Privileges¶

Access control privileges determine who can access and perform operations on
specific objects in Snowflake. For each securable object, there is a set of
privileges that can be granted on it. For existing objects, privileges must be
granted on individual objects (e.g. the SELECT privilege on the `mytable`
table). To simplify grant management, [future grants](security-access-control-
considerations.html#label-grant-management-future-grants) allow defining an
initial set of privileges on objects created in a schema (i.e. grant the
SELECT privilege on all _new_ tables created in the `myschema` schema to a
specified role).

Privileges are managed using the [GRANT <privileges>](../sql-
reference/sql/grant-privilege) and [REVOKE <privileges>](../sql-
reference/sql/revoke-privilege) commands.

  * In regular (i.e. non-managed) schemas, use of these commands is restricted to the role that owns an object (i.e. has the OWNERSHIP privilege on the object) or any roles that have the MANAGE GRANTS global privilege for the object (only the SECURITYADMIN role by default).

  * In [managed access schemas](security-access-control-configure.html#label-managed-access-schemas), object owners lose the ability to make grant decisions. Only the schema owner or a role with the MANAGE GRANTS privilege can grant privileges on objects in the schema, including future grants, centralizing privilege management.

Note that a role that holds the global MANAGE GRANTS privilege can grant
additional privileges to the current (grantor) role.

For more details, see [Access control privileges](security-access-control-
privileges).

## Role hierarchy and privilege inheritance¶

The following diagram illustrates the hierarchy for the system-defined roles,
as well as the recommended structure for additional, user-defined account
roles and database roles. The highest-level database role in the example
hierarchy is granted to a custom (i.e. user-defined) account role. In turn,
this role is granted to another custom role in a recommended structure that
allows the system-defined SYSADMIN role to inherit the privileges of custom
account roles and database roles:

[![Role hierarchy example](../_images/system-role-
hierarchy.png)](../_images/system-role-hierarchy.png)

Note

ORGADMIN is a separate system role that manages operations at the organization
level. This role is not included in the hierarchy of system roles.

For a more specific example of role hierarchy and privilege inheritance,
consider the following scenario:

>   * Role 3 has been granted to Role 2.
>
>   * Role 2 has been granted to Role 1.
>
>   * Role 1 has been granted to User 1.
>
>

![Privilege inheritance for granted roles](../_images/role-hierarchy.png)

In this scenario:

>   * Role 2 inherits Privilege C.
>
>   * Role 1 inherits Privileges B and C.
>
>   * User 1 has all three privileges.
>
>

### Database roles and role hierarchies¶

The following limitations currently apply to database roles:

  * If a database role is granted to a [share](data-sharing-gs.html#label-data-sharing-provider-option2), then no other database roles can be granted to that database role. For example, if database role `d1.r1` is granted to a share, then attempting to grant database role `d1.r2` to `d1.r1` is blocked.

In addition, if a database role is granted to another database role, the
grantee database role cannot be granted to a share.

Database roles that are granted to a share can be granted to other database
roles, as well as account roles.

  * Account roles cannot be granted to database roles in a role hierarchy.

Note

Currently, Snowsight does not recognize inherited privileges from database
roles or application roles. For more information on this limitation, see
[Snowsight Limitations](ui-snowsight-limitations).

## Enforcement model with primary role and secondary roles¶

Every active user session has a “current role,” also referred to as a _primary
role_. When a session is initiated (e.g. a user connects via JDBC/ODBC or logs
in to the Snowflake web interface), the current role is determined based on
the following criteria:

  1. If a role was specified as part of the connection and that role is a role that has already been granted to the connecting user, the specified role becomes the current role.

  2. If no role was specified and a default role has been set for the connecting user, that role becomes the current role.

  3. If no role was specified and a default role has not been set for the connecting user, the system role PUBLIC is used.

In addition, a set of _secondary_ roles can be activated in a user session. A
user can perform SQL actions on objects in a session using the aggregate
privileges granted to the primary and secondary roles. The roles must be
granted to the user before they can be activated in a session. Note that while
a session must have exactly one active primary role at a time, one can
activate any number of secondary roles at the same time.

Note

A database role can neither be a primary nor a secondary role. To assume the
privileges granted to a database role, grant the database role to an account
role. Only account roles can be activated in a session.

Authorization to execute [CREATE <object>](../sql-reference/sql/create)
statements comes from the primary role only. When an object is created, its
ownership is set to the currently active primary role. However, for any other
SQL action, any permission granted to any active primary or secondary role can
be used to authorize the action. For example, if any role in a secondary role
hierarchy owns an object (i.e. has the OWNERSHIP privilege on the object), the
secondary roles would authorize performing any DDL actions on the object. Both
the primary role as well as all secondary roles inherit privileges from any
roles lower in their role hierarchies.

[![Primary and Secondary Role Operations](../_images/primary-secondary-roles-
operations.png)](../_images/primary-secondary-roles-operations.png)

For organizations whose security model includes a large number of roles, each
with a fine granularity of authorization via permissions, the use of secondary
roles simplifies role management. All roles that were granted to a user can be
activated in a session. Secondary roles are particularly useful for SQL
operations such as cross-database joins that would otherwise require creating
a parent role of the roles that have permissions to access the objects in each
database.

During the course of a session, the user can use the [USE ROLE](../sql-
reference/sql/use-role) or [USE SECONDARY ROLES](../sql-reference/sql/use-
secondary-roles) command to change the current primary or secondary roles,
respectively. The user can use the [CURRENT_SECONDARY_ROLES](../sql-
reference/functions/current_secondary_roles) function to show all active
secondary roles for the current session.

When you create an object that requires one or more privileges to use, only
the primary role and those roles that it directly or indirectly inherits are
considered when searching for the grants of those privileges.

For any other statement that requires one or more privileges (e.g. querying a
table requires the SELECT privilege on a table with the USAGE privilege on the
database and schema), the primary role, the secondary roles, and any other
roles that are inherited are considered when searching for the grants of those
privileges.

Note

There is no concept of a “super-user” or “super-role” in Snowflake that can
bypass authorization checks. All access requires appropriate access
privileges.

