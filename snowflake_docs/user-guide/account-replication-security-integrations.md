# Replication of security integrations & network policies across multiple
accounts¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Business Critical
Feature](intro-editions)

Account object replication and failover/failback require Business Critical
Edition (or higher). To inquire about upgrading, please contact [Snowflake
Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic provides information on how to replicate security integrations,
along with using failover/failback with each of these objects, and assumes
familiarity with replication and failover/failback with other account-level
objects (e.g. users, roles, warehouses).

For details, see [Introduction to replication and failover across multiple
accounts](account-replication-intro).

These objects and services are supported across [regions](intro-regions) and
across [cloud platforms](intro-cloud-platforms).

## Overview¶

Snowflake supports replicating network policies and security integrations for
federated SSO (i.e. SAML2), OAuth, and SCIM along with enabling
failover/failback for each network policy and integration.

The general approach to test replication and failover/failback with each
network policy and security integration is as follows:

  1. Identify the source account and target account for replication, and identify the connection URL.

  2. Complete steps in the source account.

  3. Complete steps in the target account.

  4. Test failover/failback.

Note that because network policies and security integrations have different
use cases, the exact steps for the source account and target account with
respect to each object differ slightly.

For details, see:

  * Replicating SAML2 security integrations

  * Replicating SCIM security integrations

  * Replicating OAuth security integrations

  * Replicating network policies

  * Replicating integrations and objects for the Snowflake Connector for ServiceNow

## Replicating SAML2 security integrations¶

Replicating a SAML2 security integration links the source account and the
target account to the identity provider by specifying the [connection
URL](client-redirect) in the SAML2 security integration definition.

It is important to update the identity provider to specify the connection URL
and that users exist in the source account. Without these updates, user
verification cannot occur, which will result in the inability of the user to
access the target account.

Current Limitation:

    

For SAML SSO to Snowflake, replicating a SAML2 security integration that
specifies the connection URL is only supported on the current primary
connection and not supported on the secondary connection. Note that for
failover, the result is promoting a secondary connection to serve as the
primary connection. After failover, SAML SSO works on the new primary
connection.

If SAML SSO is needed for both primary and secondary connections, then create
and manage SAML2 security integrations independently on both Snowflake
accounts.

For this procedure, assume the following:

  * Source account: `https://example-northamericawest.snowflakecomputing.com/`

  * Target account: `https://example-northamericaeast.snowflakecomputing.com/`

  * Connection URL: `https://example-global.snowflakecomputing.com`

  * A secondary connection does not exist in the target account.

This procedure is a representative example to do the following:

  * Replicate a SAML2 security integration from the source account to the target account.

  * Test failover.

  * Promote the secondary connection in the source account to serve as the primary connection.

**Source account steps (includes IdP steps):**

  1. If the source account is already configured for [Database Failover/Failback and Client Redirect](replication-intro), skip to the next step.

Otherwise, enable failover using an [ALTER CONNECTION](../sql-
reference/sql/alter-connection) command:

> >     alter connection global
>     enable failover to accounts example.northamericaeast;
>  
>
> Copy

  2. Using Okta as a representative example for the identity provider, create a [Snowflake application in Okta](https://www.okta.com/integrations/snowflake/#capabilities) that specifies the connection URL. Update the Okta fields as follows:

     * Label: `Snowflake`

     * Subdomain: `example-global`

     * Browser plugin auto-submit: Check the box to enable automatic login when a user lands on the login page.

  3. In the source account, update the SAML2 security integration to specify the connection URL for the `saml2_snowflake_issuer_url` and `saml2_snowflake_acs_url` security integration properties.

> >     create or replace security integration my_idp
>       type = saml2
>       enabled = true
>       saml2_issuer = 'http://www.okta.com/exk6e8mmrgJPj68PH4x7'
>       saml2_sso_url =
> 'https://example.okta.com/app/snowflake/exk6e8mmrgJPj68PH4x7/sso/saml'
>       saml2_provider = 'OKTA'
>       saml2_x509_cert='MIIDp...'
>       saml2_sp_initiated_login_page_label = 'OKTA'
>       saml2_enable_sp_initiated = true
>       saml2_snowflake_issuer_url = 'https://example-
> global.snowflakecomputing.com'
>       saml2_snowflake_acs_url = 'https://example-
> global.snowflakecomputing.com/fed/login';
>  
>
> Copy

  4. In Okta, assign the Snowflake application to users. For details, see [Assign an app integration to a user](https://help.okta.com/en/prod/Content/Topics/Provisioning/lcm/lcm-assign-app-user.htm).

  5. Verify that SSO to the source account works for users that are specified in the Snowflake application in Okta and users in the source account.

Note that SSO should work for both IdP-initiated and Snowflake-initiated SSO
flows. For details, see [Supported SSO workflows](admin-security-fed-auth-
overview.html#label-fed-auth-sso-workflow).

  6. In the source account, if a failover group does not already exist, [create](../sql-reference/sql/create-failover-group.html#label-create-failover-group) a failover group to include security integrations. Note that this example is representative and includes other account objects that might or might not be necessary to replicate.

If a failover group already exists, [alter](../sql-reference/sql/alter-
failover-group.html#label-alter-failover-group) the failover group to include
integrations.

> >     create failover group FG
>       object_types = users, roles, warehouses, resource monitors,
> integrations
>       allowed_integration_types = security integrations
>       allowed_accounts = example.northamericaeast
>       replication_schedule = '10 MINUTE';
>  
>
> Copy

**Target Account Steps:**

  1. Prior to replication, verify the number of users and security integrations that are present in the target account by executing the [SHOW USERS](../sql-reference/sql/show-users) and [SHOW INTEGRATIONS](../sql-reference/sql/show-integrations) commands, respectively.

  2. Create a secondary connection. For details, see [CREATE CONNECTION](../sql-reference/sql/create-connection).

> >     create connection GLOBAL as replica of
> example.northamericawest.global;
>  
>
> Copy

  3. Create a secondary failover group in the target account. For details, see [CREATE FAILOVER GROUP](../sql-reference/sql/create-failover-group.html#label-create-failover-group).

> >     create failover group fg
>     as replica of example.northamericawest.fg;
>  
>
> Copy

  4. When creating a secondary failover group, an initial refresh is automatically executed.

To manually refresh a secondary failover group in the target account, execute
the following statement. For details, see [ALTER FAILOVER GROUP](../sql-
reference/sql/alter-failover-group) command.

> >     alter failover group fg refresh;
>  
>
> Copy

  5. If the refresh operation was successful, the target account should include new users that were added to the source account and not previously present in the target account. Similarly, the target account should include the SAML2 security integration that specifies the connection URL.

Verify the refresh operation was successful by executing the following
commands:

     * [SHOW INTEGRATIONS](../sql-reference/sql/show-integrations) (should include 1 new integration)

     * [SHOW USERS](../sql-reference/sql/show-users) (should include the number of new users added)

     * [DESCRIBE INTEGRATION](../sql-reference/sql/desc-integration) (for the integration `myidp`)

  6. Promote the secondary connection in the target account to serve as the primary connection. After executing the following command, users can use SAML SSO to authenticate to the new target account.

> >     alter connection global primary;
>  
>
> Copy

## Replicating SCIM security integrations¶

Replicating a SCIM security integration allows the target account to
incorporate SCIM updates that are made to the source account (e.g. adding new
users, adding new roles) after refreshing the target account.

After replicating the SCIM security integration, both Snowflake accounts have
the ability to receive SCIM updates from the identity provider. However,
Snowflake allows specifying only one account as the _primary_ (i.e. source)
account and it is the primary account that receives SCIM updates from the
identity provider.

You can optionally designate a different account as the primary account to
receive SCIM updates after replicating the SCIM integration. Note that the
target account can receive SCIM updates from the source account only after
refreshing the target account.

For this procedure, assume the following:

  * Source account: `https://example-northamericawest.snowflakecomputing.com/`

  * Target account: `https://example-northamericaeast.snowflakecomputing.com/`

  * Connection URL: `https://example-global.snowflakecomputing.com`

  * A secondary connection exists in the target account (i.e. only refresh operations are needed).

This procedure is a representative example to do the following:

  * Replicate a SCIM security integration from the source account to the target account.

  * Add a new user in Okta, push the new user to the source account, and replicate the new user to the target account.

  * Refresh the failover group.

  * Promote the secondary connection in the target account to serve as the primary connection.

**Source account steps:**

  1. Execute [SHOW CONNECTIONS](../sql-reference/sql/show-connections) to verify that the connection in the source account is the primary connection. If it is not the primary connection, use the [ALTER CONNECTION](../sql-reference/sql/alter-connection) command to promote the connection in the source account to serve as the primary connection.

  2. If an Okta SCIM security integration is already configured in the source account, skip to the next step.

Otherwise, configure an [Okta SCIM](scim-okta) security integration in the
source account.

> >     create role if not exists okta_provisioner;
>     grant create user on account to role okta_provisioner;
>     grant create role on account to role okta_provisioner;
>     grant role okta_provisioner to role accountadmin;
>     create or replace security integration okta_provisioning
>        type = scim
>        scim_client = 'okta'
>        run_as_role = 'OKTA_PROVISIONER';
>  
>     select system$generate_scim_access_token('OKTA_PROVISIONING');
>  
>
> Copy

Be sure to update the Okta SCIM application for Snowflake. For details, see
[Okta configuration](scim-okta.html#label-scim-okta-configuration).

  3. In Okta, [create a new user](https://www.okta.com/integrations/snowflake/#capabilities) in the Okta application for Snowflake.

Verify the user is pushed to Snowflake by executing a [SHOW USERS](../sql-
reference/sql/show-users) command in Snowflake.

  4. If the failover group already specifies `security integrations`, skip to the next step. This would be true if you have already configured the failover group for the purposes of SAML SSO in the target account (in this topic).

Otherwise, modify the existing failover group using an ALTER FAILOVER GROUP
command to specify `security integrations`.

> >     alter failover group fG set
>       object_types = users, roles, warehouses, resource monitors,
> integrations
>       allowed_integration_types = security integrations;
>  
>
> Copy

  5. At this point, you can optionally refresh the secondary failover group as shown in the target account steps for SCIM to ensure the new user in the source account is in the target account.

Choosing to refresh the secondary failover group now allows for an easy check
to make sure that the change to the source account, adding a new user in this
sequence, is visible in the target account.

However, if you need or prefer to do additional work in the identity provider,
such as modifying other users or updating role assignments, you can continue
doing that work now and then refresh the secondary failover group in one
operation later.

**Target account steps:**

  1. Prior to replication, verify the number of users and security integrations that are present in the target account by executing the [SHOW USERS](../sql-reference/sql/show-users) and [SHOW INTEGRATIONS](../sql-reference/sql/show-integrations) commands, respectively.

  2. Refresh the secondary failover group to update the target account to include the new user (and any other changes that were made in Okta and the source account).

> >     alter failover group fg refresh;
>  
>
> Copy

  3. Verify that the new user is added to the target account by executing a [SHOW USERS](../sql-reference/sql/show-users) command.

  4. Optionally, promote the secondary failover group and the secondary connection in the target account to primary. This will promote the target account to serve as the new source account.

Failover group:

> >     alter failover group fg primary;
>  
>
> Copy

Connection:

> >     alter connection global primary;
>  
>
> Copy

## Replicating OAuth security integrations¶

Replicating OAuth security integrations includes both Snowflake OAuth security
integrations and External OAuth security integrations.

Note the following:

Snowflake OAuth:

    

After replication and configuring failover/failback, a user connecting to
either the source account or target account via an OAuth client does not need
to re-authenticate to the target account.

External OAuth:

    

After replication and configuring failover/failback, a user connecting to
either the source account or target account via an OAuth client _might_ need
to re-authenticate to the target account.

Re-authentication is likely to be necessary if the OAuth authorization server
is not configured to issue a refresh token. Therefore, ensure that the OAuth
authorization server issues refresh tokens so that the OAuth client can
connect to the source and target Snowflake accounts.

For this procedure, assume the following:

  * Source account: `https://example-northamericawest.snowflakecomputing.com/`

  * Target account: `https://example-northamericaeast.snowflakecomputing.com/`

  * Connection URL: `https://example-global.snowflakecomputing.com`

  * A secondary connection exists in the target account (i.e. only refresh operations are needed).

  * The Snowflake OAuth or External OAuth security integrations already exist in the source account.

This procedure is a representative example to do the following:

  * Replicate an OAuth security integration.

  * Refresh the failover group.

  * Promote the secondary connection in the target account to serve as the primary connection.

**Source account steps:**

  1. If the failover group already specifies `security integrations`, skip to the next step. This would be true if you have already configured the failover group for the purposes of SAML SSO in the target account (in this topic) or SCIM (also in this topic).

Otherwise, modify the existing failover group using an ALTER FAILOVER GROUP
command to specify `security integrations`.

> >     alter failover group fG set
>       object_types = users, roles, warehouses, resource monitors,
> integrations
>       allowed_integration_types = security integrations;
>  
>
> Copy

**Target account steps:**

  1. Refresh the secondary failover group to update the target account to include the OAuth security integration objects.
    
        alter failover group fg refresh;
    

Copy

  2. Verify connecting to each Snowflake account using the OAuth client of your choice.

  3. Optionally, promote the secondary failover group and the secondary connection in the target account to primary. This will promote the target account to serve as the new source account.

Failover group:

> >     alter failover group fg primary;
>  
>
> Copy

Connection:

> >     alter connection global primary;
>  
>
> Copy

  4. If you completed the previous step, reverify that you can connect to each Snowflake account using the OAuth client of your choice.

## Replicating network policies¶

Replicating a network policy from the source account to the target account
allows administrators to restrict access to the target account based on the
network identifier of the origin of an incoming request.

### Replicating network policy references and assignments¶

Replicating a network policy replicates the network policy object and any
network policy references/assignments. For example, if a network policy
references a network rule in the source account, and both objects exist in the
target account, then the network policy uses the same network rule in the
target account. Similarly, if a network policy is assigned to a user and the
user exists in both the source and target accounts, replicating the network
policy assigns the network policy to the user in the target account.

Replicating network policy references and assignments assumes referenced
objects and objects to which the network policy is assigned are also
replicated. If you do not replicate the supporting object types properly,
Snowflake fails the refresh operation in the target account.

If a referenced object or object to which the network policy is assigned does
not already exist in the target account, include its object type in the same
replication or failover group as the network policy. The following examples
demonstrate the required settings if the supporting objects do not already
exist in the target account.

Network policies that use network rules

    

The replication or failover group must include `network policies` and
`databases`. Network rules are schema-level objects and are replicated with
the database in which they are contained. For example:

    
    
    CREATE FAILOVER GROUP fg
       OBJECT_TYPES = network policies, databases
       ALLOWED_DATABASES = testdb2
       ALLOWED_ACCOUNTS = myorg.myaccount2;
    

Copy

Network policies assigned to an account

    

The replication or failover group must include `network policies` and `account
parameters`. If the network policy uses network rules, you must also include
`databases`. For example:

    
    
    CREATE FAILOVER GROUP fg
       OBJECT_TYPES = network policies, account parameters, databases
       ALLOWED_DATABASES = testdb2
       ALLOWED_ACCOUNTS = myorg.myaccount2;
    

Copy

Network policies assigned to a user

    

The replication or failover group must include `network policies` and `users`.
If the network policy uses network rules, you must also include `databases`.
For example:

    
    
    CREATE FAILOVER GROUP fg
       OBJECT_TYPES = network policies, users, databases
       ALLOWED_DATABASES = testdb2
       ALLOWED_ACCOUNTS = myorg.myaccount2;
    

Copy

Network policies assigned to a security integration

    

Network policy replication applies to network policies that are specified in
Snowflake OAuth and SCIM [security integrations](../sql-reference/sql/create-
security-integration), provided that the replication or failover group
includes `integrations`, `security integrations` and `network policies`. If
the network policy uses network rules, you must also include `databases`.

>
>     CREATE FAILOVER GROUP fg
>        OBJECT_TYPES = network policies, integrations, databases
>        ALLOWED_DATABASES = testdb2
>        ALLOWED_INTEGRATION_TYPES = security integrations
>        ALLOWED_ACCOUNTS = myorg.myaccount2;
>  
>
> Copy

### Example¶

For this example, assume the following:

  * Source account: `https://example-northamericawest.snowflakecomputing.com/`

  * Target account: `https://example-northamericaeast.snowflakecomputing.com/`

  * Connection URL: `https://example-global.snowflakecomputing.com`

  * A secondary connection exists in the target account (i.e. only refresh operations are needed).

  * Network policies exist in the source account.

  * The Snowflake OAuth and/or SCIM security integration already exists in the source account and the integration specifies a network policy.

This procedural example does the following:

  * Replicates network policies along with the network rules that is uses to restrict network traffic.

  * Replicates a security integration to which the network policy is assigned.

  * Refreshes the failover group.

  * Verifies the network policy activation.

  * Promotes the secondary connection in the source account to serve as the primary connection.

**Source account steps:**

  1. Verify that network policies exist in the source Snowflake account by executing a [SHOW NETWORK POLICIES](../sql-reference/sql/show-network-policies) command.

  2. Verify the Snowflake OAuth and/or SCIM security integrations include a network policy by executing a [SHOW INTEGRATIONS](../sql-reference/sql/show-integrations) command to identify the security integration and then execute a [DESCRIBE INTEGRATION](../sql-reference/sql/desc-integration) command on the Snowflake OAuth security integration.

  3. Update the failover group to include `network policies` and `account parameters` using an ALTER FAILOVER GROUP command.

> >     alter failover group fG set
>       object_types = users, roles, warehouses, resource monitors,
> integrations, network policies, account parameters
>       allowed_integration_types = security integrations;
>  
>
> Copy

**Target account steps:**

  1. Refresh the secondary failover group to update the target account to include the network policy objects and the Snowflake OAuth security integration that specifies the network policy.

> >     alter failover group fg refresh;
>  
>
> Copy

  2. Verify the network policy object exists by executing a SHOW NETWORK POLICIES command, and verify the Snowflake OAuth security integration specifies the replicated network policy by executing a DESCRIBE SECURITY INTEGRATION command on the security integration.

  3. Verify the network policy activation as shown in [Identify an activated network policy](network-policies.html#label-verify-network-policy-activation).

  4. Verify connecting to each Snowflake account using the Snowflake OAuth client of your choice.

  5. Optionally promote the secondary failover group and the secondary connection in the target account to primary. This will promote the target account to serve as the new source account.

Failover group:

> >     alter failover group fg primary;
>  
>
> Copy

Connection:

> >     alter connection global primary;
>  
>
> Copy

  6. If you completed the previous step, reverify that you can connect to each Snowflake account using the Snowflake OAuth client of your choice.

## Replicating integrations and objects for the Snowflake Connector for
ServiceNow¶

The [Snowflake Connector for ServiceNow](https://other-
docs.snowflake.com/connectors/servicenow/about.html) allows Snowflake to
ingest data from ServiceNow. The connector requires the following objects in
your Snowflake account:

  * Secret.

  * Security integration of `type = api_authentication`.

  * API integration.

  * Database to store the ingested data.

  * Warehouse for the connector to use.

  * Account roles to manage the access to these objects.

You create these objects prior to installing the connector and you can
replicate these objects to the target account. After replicating these
objects, you can install the connector in the target account. The connector
must be installed in the target account because the installation depends on a
share that Snowflake provides. You need to create a database from the share
during the connector installation and you cannot replicate a database that is
created from a share.

Depending on how you want to manage the replication of account objects, you
can have one or more replication or failover groups. A single replication
group centralizes the replication management of the objects and avoids
scenarios where some objects are replicated and other objects are not
replicated. Otherwise, you must coordinate the replication operation carefully
to ensure that all objects are replicated to the target account.

For example, you can have a replication group for databases. This replication
group (e.g. `rg1`) specifies the database that contains the secret and the
database to store the ServiceNow data. The other replication group (e.g.
`rg2`) specifies the user, role, and integration objects and the grants of
these roles to users. In this scenario, if you replicate the integrations
first and then decide to refresh the target account to include the secret
database, users, and roles, the replication refresh operation is successful.

However, if you replicate the users and roles and the database that contains
the secret in a group before you replicate the integration, then a placeholder
secret is used until the security integration is replicated; the placeholder
secret prevents a dangling reference. Once the security integration is
replicated, the placeholder secret is replaced with the real secret.

This procedure is a representative example to do the following:

  * Replicate the integrations and the databases containing the secret and ingested data.

  * Refresh the failover group.

  * Promote the secondary connection in the source account to serve as the primary connection.

  * Install and use the connector after replication.

For this procedure, assume the following:

  * Source account: `https://example-northamericawest.snowflakecomputing.com/`

  * Target account: `https://example-northamericaeast.snowflakecomputing.com/`

  * Connection URL: `https://example-global.snowflakecomputing.com`

  * A secondary connection exists in the target account (i.e. only refresh operations are needed).

  * Other security integrations for authentication and network policies to restrict access are already replicated.

**Source account steps:**

  1. Verify that the objects for the connector exist in the source Snowflake account by executing SHOW commands on each of these object types.

> >     show secrets in database secretsdb;
>     show security integrations;
>     show api integrations;
>     show tables in database destdb;
>     show warehouses;
>     show roles;
>  
>
> Copy

Note that `secretsdb` is the name of the database that contains the secret and
`destdb` is the name of the database that contains the ingested data from
ServiceNow.

  2. Update the failover group to include API integrations and the databases containing the secret and ingested data using an ALTER FAILOVER GROUP command.

> >     alter failover group fg set
>       object_types = databases, users, roles, warehouses, resource monitors,
> integrations, network policies, account parameters
>       allowed_databases = secretsdb, destdb
>       allowed_integration_types = security integrations, api integrations;
>  
>
> Copy

**Target account steps:**

  1. Refresh the secondary failover group to replicate the integrations and databases to the target account.

> >     alter failover group fg refresh;
>  
>
> Copy

  2. Verify the replicated objects exist using the following SHOW commands.
    
        show secrets;
    show security integrations;
    show api integrations;
    show database;
    show tables in database destdb;
    show roles;
    

Copy

  3. Verify connecting to each Snowflake account using the method of your choice (e.g. browser, SnowSQL).

  4. Optionally promote the secondary failover group and the secondary connection in the target account to primary. This will promote the target account to serve as the new source account.

Failover group:

> >     alter failover group fg primary;
>  
>
> Copy

Connection:

> >     alter connection global primary;
>  
>
> Copy

  5. If you completed the previous step, reverify that you can connect to each Snowflake account.

At this point, the target account contains the replicated objects and users
can login. However, there are additional steps in the target account to use
the connector.

  6. Update the remote service associated with the API integration in the cloud platform that hosts your Snowflake account.

For details, refer to [Updating the remote service for API
integrations](account-replication-config.html#label-update-remote-service-for-
api-integrations).

  7. Install the connector manually or with Snowsight. For details, refer to:

     * [Install the connector manually](https://other-docs.snowflake.com/connectors/servicenow/installing-sql.html)

     * [Install the connector with Snowsight](https://other-docs.snowflake.com/connectors/servicenow/installing-snowsight.html)

  8. [Access the ServiceNow Data in Snowflake](https://other-docs.snowflake.com/connectors/servicenow/accessing-data.html).

