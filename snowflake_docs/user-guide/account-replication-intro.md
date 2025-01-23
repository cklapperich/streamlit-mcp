# Introduction to replication and failover across multiple accounts¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Standard & Business Critical
Feature](intro-editions)

  * Database and share replication are available to all accounts.

  * Replication of other account objects & failover/failback require Business Critical Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This feature enables the replication of objects from a _source_ account to one
or more _target_ accounts in the same organization. Replicated objects in each
target account are referred to as _secondary_ objects and are replicas of the
_primary_ objects in the source account. Replication is supported across
[regions](intro-regions) and across [cloud platforms](intro-cloud-platforms).

## Region support for replication and failover/failback¶

All Snowflake regions across Amazon Web Services, Google Cloud Platform, and
Microsoft Azure support replication.

Customers can replicate across all regions within a [region group](admin-
account-identifier.html#label-region-groups). To replicate between regions in
different region groups, (i.e. from a Snowflake commercial region to a
Snowflake government or Virtual Private Snowflake region), please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## Replication groups and failover groups¶

A _replication group_ is a defined collection of objects in a source account
that are replicated as a unit to one or more target accounts. Replication
groups provide read-only access for the replicated objects.

A _failover group_ is a replication group that can also fail over. A secondary
failover group in a target account provides read-only access for the
replicated objects. When a secondary failover group is promoted to become the
primary failover group, read-write access is available. Any target account
specified in the list of allowed accounts in a failover group can be promoted
to serve as the primary failover group.

Replication and failover groups provide point-in-time consistency for the
objects on the target account. The objects that can be included in a
replication or failover group are listed below in Replicated objects.

### Replication feature / edition matrix¶

Note that some replication features are only available for Business Critical
Edition (or higher). The following table lists the availability of replication
features for each Snowflake edition:

Feature | Standard | Enterprise | Business Critical | VPS  
---|---|---|---|---  
Database replication | ✔ | ✔ | ✔ | ✔  
Share replication | ✔ | ✔ | ✔ | ✔  
Replication Group | ✔ | ✔ | ✔ | ✔  
Account object (other than database and share) replication |  |  | ✔ | ✔  
Failover Group |  |  | ✔ | ✔  
Data protected with Tri-Secret Secure |  |  | ✔ | ✔  
  
## Replicated objects¶

This feature supports replicating the objects listed below. Database
replication and share replication are available on all editions. Replication
of all other objects is only available for Business Critical Edition (or
higher). For details on feature availability, see the Replication feature /
edition matrix.

Object | Type or Feature | Replicated | Notes  
---|---|---|---  
Databases |  | ✔ | Replication of some databases is not supported or might fail the refresh operation. For more information, see Current limitations of replication.  
Integrations | Security, API, Notification, Storage, External Access | ✔ | For additional caveats and details on the supported types, see Integration replication. Requires Business Critical Edition (or higher).  
Network policies |  | ✔ | Requires Business Critical Edition (or higher).  
Parameters (account level) |  | ✔ | Requires Business Critical Edition (or higher).  
Resource monitors |  | ✔ | Resource monitor notifications for non-administrator users are replicated if you include `users` in the group, however account administrator notification settings are not replicated. For more information, see Replication of resource monitor email notification settings. Requires Business Critical Edition (or higher).  
Roles |  | ✔ | 

  * Includes [account and database roles](security-access-control-overview.html#label-access-control-overview-role-types).
  * Includes privileges granted to roles, as well as roles granted to roles (i.e. hierarchies of roles).
  * If users and roles are replicated, roles granted to users are also replicated.
  * The REPLICATE and FAILOVER privileges are _not_ replicated.
  * Requires Business Critical Edition (or higher).

  
Shares |  | ✔ | Replication of [inbound shares](data-share-consumers) (shares from providers) is _not_ supported.  
Users |  | ✔ | Requires Business Critical Edition (or higher).  
Warehouses |  | ✔ | Requires Business Critical Edition (or higher).  
  
### Database Replication¶

This feature supports replicating databases. A snapshot includes changes to
the objects and data. If `roles` are replicated (in the same or different
replication or failover group), the database refresh also synchronizes the
privilege grants on the secondary database and the objects in the database
(schemas, tables, views, etc.) to roles in the account. Refer to Grants for
database objects for more details.

Replication of some databases is not supported or might fail the refresh
operation. For more information, see Current limitations of replication.

#### Replicated database objects¶

When a primary database is replicated, a snapshot of its database objects and
data is transferred to the secondary database. However, some database objects
are not replicated. The following table indicates which database objects are
replicated to a secondary database.

For specific usage information about these objects, see [Replication
considerations](account-replication-considerations).

Note

Objects that are _not_ supported for replication are skipped during the
refresh operation.

Object | Type or Feature | Replicated | Notes  
---|---|---|---  
Tables | Permanent tables | ✔ |   
| Transient tables | ✔ |   
| Temporary tables |  |   
| Automatic Clustering of clustered tables | ✔ |   
| Dynamic tables | ✔ | For more information, see [Replication and dynamic tables](account-replication-considerations.html#label-replication-and-dynamic-tables).  
| External tables |  |   
| Hybrid tables |  |   
| Apache Iceberg™ tables |  |   
| Table constraints | ✔ | Except if a foreign key in the database references a primary/unique key in another database. .  
Event tables |  |  |   
Sequences |  | ✔ |   
Views | Views | ✔ | If a view references any object in another database (e.g. table columns, other views, UDFs, or stages), . both databases must be replicated.  
| Materialized views | ✔ |   
| Secure views | ✔ |   
File formats |  | ✔ |   
Stages | Stages | ✔ | Supported for replication and failover groups only. Not supported for database replication. . For more information, see [Stage, pipe, and load history replication](account-replication-stages-pipes-load-history).  
| Temporary stages |  |   
Pipes |  | ✔ | Supported for replication and failover groups only. Not supported for database replication. . For more information, see [Stage, pipe, and load history replication](account-replication-stages-pipes-load-history).  
Stored procedures |  | ✔ | For more information, see [Replication of stored procedures and user-defined functions (UDFs)](account-replication-considerations.html#label-replication-stored-procedures-udfs).  
Streams |  | ✔ | For more information, see [Replication and streams](account-replication-considerations.html#label-replication-and-streams).  
Tasks |  | ✔ | For more information, see [Replication and tasks](account-replication-considerations.html#label-replication-and-tasks).  
Data metric functions (DMFs) | Data Quality | ✔ | For more information, see [Replication of data metric functions (DMFs)](account-replication-considerations.html#label-replication-data-quality).  
UDFs |  | ✔ | For more information, see [Replication of stored procedures and user-defined functions (UDFs)](account-replication-considerations.html#label-replication-stored-procedures-udfs).  
Policies | Aggregation policies | ✔ |   
| Authentication policies | ✔ |   
| Column-level Security (masking) | ✔ | For masking, row access, and tag-based masking policies, see [policy replication considerations](database-replication-considerations.html#label-database-replication-considerations-masking-row-policies).  
| Password policies | ✔ |   
| Privacy policies | ✔ | For more information, see [Privacy policies](account-replication-considerations.html#label-account-replication-considerations-privacy-policy).  
| Projection policies | ✔ |   
| Row access policies | ✔ |   
| Session policies | ✔ | For session, password, and authentication policies, see [replication and security policies](account-replication-considerations.html#label-account-replication-considerations-security-policies).  
| Tag-based masking policies | ✔ |   
Tags | Object Tagging | ✔ | For tags, see [Replication and tags](account-replication-considerations.html#label-replication-and-tags).  
Alerts |  | ✔ |   
Secrets | Secrets for External API Authentication | ✔ | You can replicate secrets by using a replication group and failover group. For additional details, see [Replication and secrets](account-replication-considerations.html#label-account-replication-considerations-secrets).  
Network rules |  | ✔ | For replication of network policies that use network rules, see [Replicating network policies](account-replication-security-integrations.html#label-account-replication-network-policy).  
Class instances | CUSTOM_CLASSIFIER | ✔ | Replication is supported for instances of the [CUSTOM_CLASSIFIER](../sql-reference/classes/custom_classifier) class. Instances of all other Snowflake [classes](../sql-reference/snowflake-db-classes) are _not_ replicated. For the full list of Snowflake classes, see [Available classes](../sql-reference-classes.html#label-available-classes).  
Packages policies | Python UDF, UDTF, stored procedures | ✔ | If there is a [packages policy](../developer-guide/udf/python/packages-policy) set on the source account, in order to successfully replicate account objects, the database containing the packages policy _must_ be replicated to the target account in the same or different replication or failover group. Otherwise, the refresh operation fails with a [dangling references error](account-replication-considerations.html#label-dangling-references-packages-policies).  
  
#### Database replication and encryption¶

Snowflake protects metadata and data sets at rest and in transit between the
source and target accounts. The account [master
key](https://csrc.nist.gov/glossary/term/master_key) (AMK) encrypts the key
hierarchy within the account as shown in the [hierarchical key
model](security-encryption-manage). Snowflake encrypts replicated data in the
target account using the account master key and the key hierarchy in the
target account, regardless of whether you enable Tri-Secret Secure in the
target account.

When you enable Tri-Secret Secure in the target account, Snowflake uses the
composite master key and the corresponding key hierarchy in the target account
to encrypt the data. Note that target accounts do not have Tri-Secret Secure
enabled by default; you must enable this feature.

For more information about data encryption in Snowflake, see [Understanding
end-to-end encryption in Snowflake](security-encryption-end-to-end).

### Integration replication¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Business Critical
Feature](intro-editions)

Requires Business Critical Edition (or higher). To inquire about upgrading,
please contact [Snowflake Support](https://docs.snowflake.com/user-
guide/contacting-support).

Account replication supports the replication of integrations for the following
features:

  * Security integrations of the following types:

    * Federated Authentication & SSO (i.e. SAML2)

    * SCIM

    * Snowflake OAuth

    * External OAuth

For more information about security integrations, see [Replication of security
integrations & network policies across multiple accounts](account-replication-
security-integrations).

  * API integrations.

After replicating API integrations to a target account, you must grant access
to the remote service to the replicated external functions. For more
information, see [Updating the remote service for API integrations](account-
replication-config.html#label-update-remote-service-for-api-integrations).

  * Notification integrations of the following types:

    * TYPE = EMAIL

    * TYPE = QUEUE with DIRECTION = OUTBOUND

    * TYPE = WEBHOOK

  * Storage integrations.

When you replicate a storage integration, you must establish a new trust
relationship for your cloud storage in the target accounts. To learn more, see
[Configure cloud storage access for secondary storage integrations](account-
replication-config.html#label-configure-cloud-storage-access-secondary-
storage-integrations).

  * External access integrations.

For more information about external access integrations, see [External network
access overview](../developer-guide/external-network-access/external-network-
access-overview).

### Network policy replication¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Business Critical
Feature](intro-editions)

Requires Business Critical Edition (or higher).

The feature supports replicating network policies.

For more information, see [Replication of security integrations & network
policies across multiple accounts](account-replication-security-integrations).

### Parameter replication¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Business Critical
Feature](intro-editions)

Requires Business Critical Edition (or higher).

This feature supports replicating account-level parameters and object
parameters. Object parameters are replicated when the object is included in
the replication group. For example, if `WAREHOUSES` are replicated, warehouse-
specific parameters (e.g. [STATEMENT_TIMEOUT_IN_SECONDS](../sql-
reference/parameters.html#label-statement-timeout-in-seconds)) are replicated.
For a full list, see [Object parameters](../sql-
reference/parameters.html#label-object-parameters).

Account-level parameter replication includes all [Account parameters](../sql-
reference/parameters.html#label-account-parameters) and [parameters set on the
account](admin-account-management). Account-level parameters (e.g.
[DATA_RETENTION_TIME_IN_DAYS](../sql-reference/parameters.html#label-data-
retention-time-in-days)) are replicated when `ACCOUNT PARAMETERS` is included
in the list of object types for a replication group.

### Resource monitor replication¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Business Critical
Feature](intro-editions)

Requires Business Critical Edition (or higher).

This feature supports replicating resource monitors and privileges granted on
resource monitors to roles. A secondary resource monitor follows the same
quota reset schedule as its primary. For example, if the quota on the primary
resource monitor resets on the first of the month, and the secondary is first
replicated on the 15th of the month, its quota will reset on the first of the
next month along with the primary.

#### Replication of resource monitor email notification settings¶

Email notification settings for resource monitors are not included with
resource monitor replication. Email notifications for non-administrator users
can be replicated with resource monitors. However, account administrator
notification settings are currently not replicated:

  * If `users` and `resource monitors` are included in the `object_types` list for the replication or failover group, notification settings for non-administrator users are replicated:

    * The `notify_users` list for a warehouse-level resource monitor is replicated to target accounts.

    * [Email notifications for non-administrator users](resource-monitors.html#label-resource-monitors-enabling-nonadministrator-notifications) are sent on the target account.

  * If `resource monitors` is included in the `object_types` list for the replication or failover group, but `users` is not included, the `notify_users` list for a secondary warehouse-level resource monitor is empty.

  * Account administrator notification settings are _not_ replicated:

    * An account administrator must [enable email notifications](resource-monitors.html#label-enabling-notifications) in each account using the web interface.

    * Resource monitor notifications are sent to account administrators if they have enabled email notifications in the source and/or target accounts.

### Role replication¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Business Critical
Feature](intro-editions)

Requires Business Critical Edition (or higher).

This feature supports replicating roles, including role hierarchies. Role
objects must be replicated to replicate access privileges. Replicated access
privileges are listed in Replication of roles and grants below.

Note

All roles are replicated, including the ORGADMIN role.

### Share replication¶

This feature supports replication of share objects as well as access
privileges granted to shares on database objects.

Replication of [inbound shares](data-share-consumers) (shares from providers)
is not supported.

### User replication¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Business Critical
Feature](intro-editions)

Requires Business Critical Edition (or higher).

This feature supports replicating users and their properties to target
accounts, the following user authentication methods, and provisioning users
and groups with SCIM:

Authentication Method | Works in Target Accounts | Notes  
---|---|---  
Password | ✔ |   
Password with MFA (multi-factor authentication) | ✔ | Users who are enrolled in MFA in the source account must separately enroll in MFA when they log in to each target account.  
[Multi-factor authentication (MFA)](security-mfa) | ✔ | Users who are enrolled in MFA in the source account must separately enroll in MFA when they log in to each target account.  
Key-pair authentication | ✔ |   
[Federated Authentication](admin-security-fed-auth-overview) | ✔ | Refer to [Replication of security integrations & network policies across multiple accounts](account-replication-security-integrations) for details on replicating federated SSO (i.e. SAML2) security integrations.  
[Snowflake OAuth](oauth-snowflake-overview) | ✔ | Refer to [Replication of security integrations & network policies across multiple accounts](account-replication-security-integrations) for details on replicating OAuth security integrations.  
[External OAuth](oauth-ext-overview) | ✔ | Refer to [Replication of security integrations & network policies across multiple accounts](account-replication-security-integrations) for details on replicating OAuth security integrations.  
[SCIM](scim-intro) | ✔ | Refer to [Replication of security integrations & network policies across multiple accounts](account-replication-security-integrations) for details on replicating SCIM security integrations.  
  
Note

If `USERS` and `ROLES` objects are replicated to a target account, these
object types are read-only in the target account and cannot be modified. Users
and roles must be created in the source account, then replicated to each
target account. Refer to [Replication and read-only secondary
objects](account-replication-considerations.html#label-replication-and-
secondary-objects).

### Warehouse replication¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Business Critical
Feature](intro-editions)

Requires Business Critical Edition (or higher). To inquire about upgrading,
please contact [Snowflake Support](https://docs.snowflake.com/user-
guide/contacting-support).

This feature supports replicating warehouses and privileges granted on
warehouses to roles (if `roles` are replicated). The state of the primary
warehouse is not replicated. Warehouses are replicated in the suspended state
to each target account and can be resumed in the target account.

### Replication of roles and grants¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Business Critical
Feature](intro-editions)

Requires Business Critical Edition (or higher).

In order to replicate grants on objects to roles, roles must be replicated
from the source account to the target account. To replicate roles in a
replication or failover group, you must include `roles` in the `object_types`
list. Roles can be in a separate replication or failover group from the data
objects on which the privileges are granted.

When `roles` are replicated, grants on objects are only replicated to a target
account if:

  * The privilege was granted by the owner of the object or indirectly by a role that was granted the privilege with the [WITH GRANT OPTION](../sql-reference/sql/grant-privilege) parameter by the owner of the object.

  * Both the grantee and grantor role for a privilege grant are located in the target account.

  * The object is replicated (i.e. the object type is included in the `object_types` list).

Otherwise the grant on the object is not replicated.

For information about replicating secondary roles and session policies, see
[Session policies with secondary roles](account-replication-
considerations.html#label-account-replication-session-policy-secondary-roles).

Note

  * If a role is dropped that has the OWNERSHIP privilege on an active pipe in the target account, the refresh operation fails.

  * Privileges on replication groups and failover groups are not replicated. If the REPLICATE or FAILOVER privilege has been granted on replication groups or failover groups, these privileges need to be granted in both the source and target accounts. Refer to [Replication privileges](account-replication-considerations.html#label-replication-privileges) for details on these privileges.

#### Grants for database objects¶

If `roles` and `databases` are replicated to a target account (in the same or
different replication or failover group), refreshing a secondary database
synchronizes the privilege grants on the database and the objects in the
database (schemas, tables, views, etc.) to existing roles in the target
account (i.e. roles that have been replicated to the target account). Note
that only privilege grants on objects supported by database replication are
synchronized. For the list of supported objects, see Replicated database
objects.

External tables are not currently supported for replication. As a result,
privilege grants on external tables are also not replicated.

#### Future grants for objects¶

If roles are replicated to the target account, [future grants](security-
access-control-considerations.html#label-grant-management-future-grants) that
are granted at the database or schema level are replicated to the target
account. This also includes future grants on non-replication supported
objects. For example, external table replication is not yet supported, however
future grants on external tables are replicated. When you create an external
table in a target account, the privileges granted on future external tables
materialize as intended.

#### Object creation and ownership¶

If new objects are created in a target account during a refresh from the
source account, and roles are not replicated to the target account, the
OWNERSHIP privilege for the new objects is granted to the ACCOUNTADMIN role.

If roles are replicated to the target account, the OWNERSHIP privilege is
granted to the same role on the target account as the role with the OWNERSHIP
privilege in the source account when roles are next replicated. The roles may
be replicated at the same time the new objects are created in the target
account if the objects and roles are in the same replication (or failover)
group.

#### Grants for shares¶

In order to enable secure data sharing, grants on objects to shares are
replicated even if `roles` are not replicated to target accounts. This section
provides information on how grants on objects to shares are replicated.

If `roles` are replicated from the source account to the target account,
grants to objects on shares are replicated if:

  * The grantor role exists in the target account or

  * The grantor role in the source account has the OWNERSHIP privilege on the primary object.

If `roles` are not replicated from the source account to the target account,
then:

  * Grants on objects to shares are replicated.

  * The grantor role for grants on replicated objects to shares is the role with the OWNERSHIP privilege on the object.

### User who refreshes objects in a target account¶

A user who executes the [ALTER FAILOVER GROUP … REFRESH](../sql-
reference/sql/alter-failover-group.html#label-alter-failover-group) command to
refresh objects in a target account from the source account must use a role
with the REPLICATE privilege on the failover group. Snowflake protects this
user in the target account by failing in the following scenarios:

  * If the user does not exist in the source account, the refresh operation fails.

  * If the user exists in the source account, but a role with the REPLICATE privilege was not granted to the user, the refresh operation fails.

## Replication schedule¶

As a best practice, Snowflake recommends scheduling automatic refreshes using
the REPLICATION_SCHEDULE parameter. The schedule can be defined when creating
a new replication or failover group with CREATE _< object>_ or later (using
ALTER _< object>_).

When you create a secondary replication or failover group, Snowflake
automatically executes an initial refresh. The next refresh is scheduled based
on when the prior refresh started and the scheduling interval, or the next
valid time based on the cron expression. For example, if the refresh schedule
interval is 10 minutes and the prior refresh operation (either a scheduled
refresh or manually triggered refresh) starts at 12:01, the next refresh is
scheduled for 12:11.

Snowflake ensures only one refresh is executed at any given time. If a refresh
is still executing when the next refresh is scheduled, the next refresh is
delayed to start when the currently executing refresh completes. For example,
if a refresh is scheduled to execute 15 minutes after the hour, every hour,
and the prior refresh completes at 12:16, the next refresh is scheduled to
execute when the previously executing refresh is completed.

Note

Automatically scheduled refresh operations are executed using the role with
the OWNERSHIP privilege on the replication or failover group. If a scheduled
refresh operation fails due to insufficient privileges, grant the required
privileges to the role with the OWNERSHIP privilege on the group.

### Suspend and resume scheduled replication¶

A secondary failover group cannot be promoted to the primary group while a
refresh is executing. To fail over gracefully, suspend scheduled replication
in the target account. After the failover is completed, resume the scheduled
replication. For more information, see [ALTER FAILOVER GROUP](../sql-
reference/sql/alter-failover-group).

## Replication to accounts on lower editions¶

If either of the following conditions is true, Snowflake displays an error
message:

  * A primary replication group with only database and/or share objects is in a Business Critical (or higher) account but one or more of the accounts approved for replication are on lower editions. Business Critical Edition is intended for Snowflake accounts with extremely sensitive data.

  * A primary replication or failover group with any [object types](../sql-reference/sql/create-replication-group.html#label-create-replication-group-object-types) is in a Business Critical (or higher) account and a signed business associate agreement is in place to store PHI data in the account per HIPAA and [HITRUST CSF](intro-cloud-platforms.html#label-hitrust-csf-cert) regulations. However, no such agreement is in place for one or more of the accounts enabled for replication, regardless if they are Business Critical (or higher) accounts.

This behavior is implemented in an effort to help prevent account
administrators for Business Critical (or higher) accounts from inadvertently
replicating sensitive data to accounts on lower editions.

An account administrator (a user with the ACCOUNTADMIN role) or a user with a
role with the CREATE REPLICATION GROUP/CREATE FAILOVER GROUP or OWNERSHIP
privilege can override this default behavior by including the IGNORE EDITION
CHECK clause when executing the CREATE _< object>_ or ALTER _< object>_
statement. If IGNORE EDITION CHECK is set, the primary replication or failover
group may be replicated to the specified accounts on lower Snowflake editions
in these specific scenarios.

Note

Failover groups can only be created in a Business Critical Edition (or higher)
account. Therefore failover groups can only be replicated to an account that
is a Business Critical Edition (or higher) account.

## Current limitations of replication¶

  * Databases created from shares cannot be replicated.

  * Refresh operations fail if the primary database includes a stream with an unsupported source object. The operation also fails if the source object for any stream has been dropped.

  * Append-only streams are not supported on replicated source objects.

Note

Database replication does not work for task graphs if the graph is owned by a
different role than the role that performs replication.

