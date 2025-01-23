# Controlling network traffic with network policies¶

You can use network policies to control _inbound_ access to the Snowflake
service and internal stage.

If you want to control _outbound_ traffic from Snowflake to an external
network destination, see [External network access overview](../developer-
guide/external-network-access/external-network-access-overview).

Note

Network policies that existed before the introduction of network rules can no
longer be modified in Snowsight. Use the [ALTER NETWORK POLICY](../sql-
reference/sql/alter-network-policy) command instead.

## About network policies¶

By default, Snowflake allows users to connect to the service and internal
stage from any computer or device. A security administrator (or higher) can
use a network policy to allow or deny access to a request based on its origin.
The _allowed list_ of the network policy controls which requests are allowed
to access the Snowflake service or internal stage, while the _blocked list_
controls which requests should be explicitly blocked.

A network policy does not directly specify the network identifiers in its
allowed list or blocked list. Rather, a network policy adds _network rules_ to
its allowed and blocked lists. These network rules group related identifiers
into logical units that are added to the allowed list and blocked list of a
network policy.

Important

Network policies that existed before the introduction of network rules still
work. However, all new network policies should use network rules, not the
`ALLOWED_IP_LIST` and `BLOCKED_IP_LIST` parameters, to control access from IP
addresses. Best practice is to avoid using both ways to restrict access in the
same network policy.

### Workflow¶

The general workflow of using network policies to control inbound network
traffic is:

  1. Create network rules based on their purpose and type of network identifier.

  2. Create one or more network policies that include the network rules that contain the identifiers to be allowed or blocked.

  3. Activate the network policy for an account, user, or security integration. A network policy does not restrict network traffic until it is activated.

### Interaction between allowed lists and blocked lists¶

When you add a network rule to the allowed list of a network policy, you do
not have to use the blocked list to explicitly block other identifiers of the
same type; only the allowed identifiers have access. For example, if you add
an IPv4 network rule with a single IP address to the allowed list, all other
IPv4 addresses are blocked. There is no need to use the blocked list to
restrict access from other IP addresses.

If a network policy has the same IP address values in both the
`ALLOWED_IP_LIST` and the `BLOCKED_IP_LIST` parameters, Snowflake applies the
values in the `BLOCKED_IP_LIST` parameter first. This behavior also applies to
the `ALLOWED_NETWORK_RULE_LIST` and the `BLOCKED_NETWORK_RULE_LIST`
parameters.

Over private connections, if a network policy has a VPCE ID (AWS) or LinkID
(Azure) network rule in the `ALLOWED_NETWORK_RULE_LIST` parameter, IP network
rules in the `BLOCKED_NETWORK_RULE_LIST` parameter are ignored, causing VPCE
ID or LinkID network rules to take precedence.

As an example, a network rule that uses private endpoint identifiers such as
Azure LinkIDs or AWS VPCE IDs to restrict access have no effect on requests
coming from the public network. If you want to restrict access based on
private endpoint identifiers, and then completely block requests from public
IPv4 addresses, you must create two separate network rules, one for the
allowed list and another for the blocked list.

The following network rules could be combined in a network policy to allow a
VPCE ID while blocking public network traffic.

    
    
    CREATE NETWORK RULE block_public_access
      MODE = INGRESS
      TYPE = IPV4
      VALUE_LIST = ('0.0.0.0/0');
    
    CREATE NETWORK RULE allow_vpceid_access
      MODE = INGRESS
      TYPE = AWSVPCEID
      VALUE_LIST = ('vpce-0fa383eb170331202');
    
    CREATE NETWORK POLICY allow_vpceid_block_public_policy
      ALLOWED_NETWORK_RULE_LIST = ('allow_vpceid_access')
      BLOCKED_NETWORK_RULE_LIST=('block_public_access');
    

Copy

#### IP ranges¶

If you want to allow a range of IP addresses with the exception of a single IP
address, you can create two network rules, one for the allowed list and
another for the blocked list.

For example, the following would allow requests from all IP addresses in the
range of `192.168.1.0` to `192.168.1.255`, except `192.168.1.99`. IP addresses
outside the range are also blocked.

    
    
    CREATE NETWORK RULE allow_access_rule
      MODE = INGRESS
      TYPE = IPV4
      VALUE_LIST = ('192.168.1.0/24');
    
    CREATE NETWORK RULE block_access_rule
      MODE = INGRESS
      TYPE = IPV4
      VALUE_LIST = ('192.168.1.99');
    
    CREATE NETWORK POLICY public_network_policy
      ALLOWED_NETWORK_RULE_LIST = ('allow_access_rule')
      BLOCKED_NETWORK_RULE_LIST=('block_access_rule');
    

Copy

### Network policy precedence¶

You can apply a network policy to an account, a security integration, or a
user. If there are network policies applied to more than one of these, the
most specific network policy overrides more general network policies. The
following summarizes the order of precedence:

Account:

    

Network policies applied to an account are the most general network policies.
They are overridden by network policies applied to a security integration or
user.

Security Integration:

    

Network policies applied to a security integration override network policies
applied to the account, but are overridden by a network policy applied to a
user.

User:

    

Network policies applied to a user are the most specific network policies.
They override both accounts and security integrations.

### Bypassing a network policy¶

It is possible to temporarily bypass a network policy for a set number of
minutes by configuring the user object property
`MINS_TO_BYPASS_NETWORK_POLICY`, which can be viewed by executing [DESCRIBE
USER](../sql-reference/sql/desc-user). Only Snowflake can set the value for
this object property. Please contact [Snowflake
Support](https://docs.snowflake.com/user-guide/contacting-support) to set a
value for this property.

## About network rules¶

While restrictions on incoming requests to Snowflake are ultimately applied to
an account, user, or security integration with a network policy, the
administrator can organize these restrictions using [network rules](network-
rules), which are schema-level objects.

Each network rule groups together the identifiers for a particular type of
request origin. For example, one network rule might include all of the IPv4
addresses that should be allowed to access Snowflake while another groups
together all of the private endpoints that should be blocked.

A network rule, however, does not specify whether it is allowing or blocking
the origin of a request. It simply organizes related origins into a logical
unit. Administrators specify whether that unit should be allowed or blocked
when they create or modify a network policy.

If you already understand the strategies for using network rules with network
policies, see Working with network rules.

### Best practices¶

  * **Limit the scope**. Network rules are designed to group together small units of related network identifiers. Previously, network policies often contained a large, monolithic list of IP addresses that should be allowed or blocked. The introduction of network rules changes this strategy. For example, you could break up network identifiers by:

    * Creating a network rule to contain client IP addresses for the North American region, and a different rule for the Europe and Middle Eastern region.

    * Creating a network rule whose purpose is to allow access for a special population, such as highly privileged users and service account users. This network rule can be added to a network policy that is applied to individual users.

    * Creating a network rule that is scoped to one or more data apps.

With the introduction of network rules, Snowflake recommends that you also
limit the scope of network policies. Whenever possible, narrowly scope a
network policy to a group of users or a security integration rather than an
entire account.

  * **Add comments**. When creating a network rule, use the `COMMENT` property to keep track of what the rule is supposed to do. Comments are important because Snowflake encourages a large number of small targeted rules over fewer monolithic ones.

You can use the SHOW NETWORK RULES command to list all of the network rules,
including their comments.

### Supported identifiers¶

Each network rule contains a list of one or more network identifiers of the
same type (e.g. an IPv4 address rule or a private endpoint rule).

A network rule’s `TYPE` property identifies what type of identifiers the
network rule contains.

For a complete list of the types of identifiers that can be restricted using
network rules, see [Supported network identifiers](network-rules.html#label-
network-rule-identifiers).

### Protecting the Snowflake service¶

This section discusses how to use network rules to restrict access to the
Snowflake service only. If you want to restrict access to both the service and
the internal stage of an account on AWS, see Protecting internal stages on
AWS.

To restrict access to the Snowflake service, set the `MODE` property of the
network rule to `INGRESS`.

You can then use the `TYPE` property to specify the [identifiers](network-
rules.html#label-network-rule-identifiers) that should be allowed or blocked.

### Protecting internal stages on AWS¶

This section discusses how to use network rules to restrict access to internal
stages on AWS, including how to simultaneously restrict access to the
Snowflake service and internal stage. It includes:

  * Limitations

  * Prerequisite: Enabling internal stage restrictions

  * Guidelines for internal stages

  * Strategy for protecting the internal stage only

  * Strategies for protecting both service and internal stage

Note

You cannot use a network rule to restrict access to an internal stage on
Microsoft Azure. However, you can block all public access to an internal stage
on Azure if you are using [Azure Private Link](https://learn.microsoft.com/en-
us/azure/private-link/private-link-overview). For details, see [Blocking
public access — Recommended](private-internal-stages-azure.html#label-private-
internal-stage-azure-block-public).

#### Limitations¶

  * A network policy that is activated for a security integration does not restrict access to an internal stage.

#### Prerequisite: Enabling internal stage restrictions¶

To use network rules to restrict access to the internal stage of an account,
the account administrator must enable the
[ENFORCE_NETWORK_RULES_FOR_INTERNAL_STAGES](../sql-
reference/parameters.html#label-enforce-network-rules-for-internal-stages)
parameter . Network rules do not protect an internal stage until this
parameter is enabled, regardless of the rule’s mode.

To allow network rules to restrict access to internal stages, execute:

    
    
    USE ROLE ACCOUNTADMIN;
    ALTER ACCOUNT SET ENFORCE_NETWORK_RULES_FOR_INTERNAL_STAGES = true;
    

Copy

#### Guidelines for internal stages¶

In addition to the best practices for network rules, you should adhere to the
following guidelines when creating network policies and network rules to
restrict access to internal stages.

  * **Limit the number of identifiers**. Network policies used to protect an internal stage cannot contain an unlimited number of network identifiers. The limits vary depending on your Snowflake edition.

Note

If a network policy has more than one network rule, the combined number of
identifiers from all network rules cannot exceed the limit for the network
policy.

    * **Standard and Enterprise editions** :

      * Maximum number of IPv4 address ranges is 10 per network rule.

      * Maximum number of VPCE IDs is 7 per network policy.

    * **Business Critical edition and higher** :

      * Maximum number of IPv4 address ranges is approximately 250 per network policy.

      * Maximum number of VPCE IDs is approximately 200 per network policy.

      * Maximum number of network policies is 50. If you need to increase this limit, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

  * **Use same rule to protect both service and internal stage**. When a rule contains IPv4 addresses and the mode of a network rule is `INGRESS`, a single rule can protect both the Snowflake service and the internal stage of the account. Snowflake recommends using a single rule even when the IP addresses accessing the service are different from the IP addresses accessing the internal stage. This approach improves organization, manageability, and auditing.

  * **Test Network Policies**. Snowflake recommends testing network rules using user-level network policies. If you encounter `PolicySizeExceeded` exceptions when fetching the scoped credentials from AWS STS, break up the network identifiers into smaller network rules.

#### Strategy for protecting the internal stage only¶

To restrict access to an AWS internal stage without affecting how network
traffic accesses the Snowflake service, create a network rule with the
following settings:

  * Set the `MODE` parameter to `INTERNAL_STAGE`.

  * Set the `TYPE` parameter to `AWSVPCEID`.

Note

You cannot restrict access to the internal stage based on the IP address of
the request without also restricting access to the Snowflake service.

#### Strategies for protecting both service and internal stage¶

When restricting access to both the Snowflake service and internal stage, the
implementation strategy varies based on whether network traffic is traversing
the public internet or AWS Private Link.

In the following comparison, “Public” indicates that traffic to the service or
internal stage is traversing the public internet while “Private” indicates
traffic is using AWS Private Link. Find the combination that matches your
environment, and then choose the implementation strategy accordingly.

Service Connection | Internal Stage Connection | Implementation Strategy  
---|---|---  
Public | Public | Create a single network rule with `TYPE=IPV4` and `MODE=INGRESS`. Include all IP addresses that access the service and internal stage.  
Private | Private | Strategy depends on whether you want to restrict access using private IP addresses or the VPCE ID of the VPC endpoints:

  * **(Recommended)** If using VPCE IDs, you must create two network rules, even if the same VPC endpoint is connecting to both the service and the internal stage.
    * For the service, create a network rule with `TYPE=AWSVPCEID` and `MODE=INGRESS`.
    * For the internal stage, create a network rule with `TYPE=AWSVPCEID` and `MODE=INTERNAL_STAGE`.
  * If using private IP addresses, create a network rule with `TYPE=IPV4` and `MODE=INGRESS`. Include all private IP addresses that access the service and internal stage.

  
Public [1] | Private | Strategy depends on whether you want to restrict access to the internal stage using private IP addresses or VPCE ID of the VPC endpoints:

  * **(Recommended)** If using VPCE IDs, create two network rules, one for the service and one for the internal stage.
    * For the service, create a network with `TYPE=IPV4` and `MODE=INGRESS`.
    * For the internal stage, create a network rule with `TYPE=AWSVPCEID` and `MODE=INTERNAL_STAGE`.
  * If using private IP addresses, create a single network rule with `TYPE=IPV4` and `MODE=INGRESS`. Include all IP addresses that access the service and internal stage.

  
Private | Public [1] | You must use private IPs for the service (cannot use VPCE IDs). Create a single network rule with `TYPE=IPV4` and `MODE=INGRESS`. Include all IP addresses that access the service and internal stage.  
[1] (1,2)

If you have implemented private connectivity to either the service or the
internal stage, Snowflake recommends implementing it for both.

## Working with network rules¶

You can use Snowsight or SQL to manage the lifecycle of a network rule.

### Create a network rule¶

You need the CREATE NETWORK RULE privilege on the schema to create a network
rule. By default, only the ACCOUNTADMIN and SECURITYADMIN roles, along with
the schema owner, have this privilege.

The mode of a network rule that will be used by a network policy must be
`INGRESS` or `INTERNAL STAGE`.

To gain a better understand of best practices and strategies for creating
network rules, see About network rules.

You can create a network rule using Snowsight or by executing a SQL command:

Snowsight:

    

  1. Sign in to Snowsight.

  2. Select Admin » Security.

  3. Select the Network Rules tab.

  4. Select \+ Network Rule.

  5. Enter the name of the network rule.

  6. Select the schema of the network rule. Network rule are schema-level objects.

  7. Optionally, add a descriptive comment for the network rule to help organize and maintain network rules in the schema.

  8. In the Type drop-down, select the [type of identifier](network-rules.html#label-network-rule-identifiers) being defined in the network rule. The Host Port type is not a valid option for network rules being used with network policies.

  9. In the Mode drop-down, select Ingress or Internal Stage. The Egress mode is not a valid option for network rules being used with network policies.

  10. Enter a comma-separated list of the identifiers that will be allowed or blocked when the network rule is added to a network policy. The identifiers in this list must all be of the type specified in the Type drop-down.

  11. Select Create Network Rule.

SQL:

    

An administrator can execute the [CREATE NETWORK RULE](../sql-
reference/sql/create-network-rule) command to create a new network rule,
specifying a list of network identifiers along with the type of those
identifiers.

For example, to use a custom role to create a network rule that can be used to
allow or block traffic from a range of IP addresses:

    
    
    GRANT USAGE ON DATABASE securitydb TO ROLE network_admin;
    GRANT USAGE ON SCHEMA securitydb.myrules TO ROLE network_admin;
    GRANT CREATE NETWORK RULE ON SCHEMA securitydb.myrules TO ROLE network_admin;
    USE ROLE network_admin;
    
    CREATE NETWORK RULE cloud_network TYPE = IPV4 VALUE_LIST = ('47.88.25.32/27');
    

Copy

### Modify a network rule¶

You can modify the network rule using Snowsight or SQL.

Snowsight:

    

  1. Sign in to Snowsight.

  2. Select Admin » Security.

  3. Select the Network Rules tab.

  4. Find the network rule, select the … button, and then select Edit.

  5. Modify the network rule as needed.

  6. Select Update Network Rule.

SQL:

    

Execute an [ALTER NETWORK RULE](../sql-reference/sql/alter-network-rule)
statement.

## Working with network policies¶

Once you have grouped network identifiers into network rules, you are ready to
add those network rules to the allowed list and blocked list of a new or
existing network policy. There is no limit on how many network rules can be
added to a network policy.

For general information about how network policies control inbound access to
the Snowflake service and internal stage, see About network policies.

Network policies that were accessible from the [Classic Console](ui-using) are
no longer available in Snowsight. To access these network policies in
Snowsight, do the following:

  1. Log into the Classic Console and view your network policies.

  2. Call the [POLICY_REFERENCES](../sql-reference/functions/policy_references) function to determine whether the network policy is set on your account or a user in your account.

  3. Run the [DESCRIBE NETWORK POLICY](../sql-reference/sql/desc-network-policy) command to view the network policy details.

  4. Recreate the network policy to specify network rules.

  5. If the old network policy was assigned to either your account or a user in the account, reassign the new network policy to the same account or user to activate the network policy.

### Create a network policy¶

Only security administrators (i.e. users with the SECURITYADMIN role) or
higher or a role with the global CREATE NETWORK POLICY privilege can create
network policies. Ownership of a network policy can be transferred to another
role.

Caution

`0.0.0.0/0` refers to all public and private IPv4 address ranges. Use a
network rule to block public access and add the network rule to the
`BLOCKED_NETWORK_RULE_LIST` property of the network policy.

The network policy evaluation considers any network rule properties before the
`ALLOWED_IP_LIST` and `BLOCKED_IP_LIST` network policy properties:

  * The network rule `TYPE` property for `AWSVPCEID` and `AZURELINKID` takes precedence over any `TYPE = IPV4` value.

  * If there are no network rules, the network policy evaluation considers the `ALLOWED_IP_LIST` and `BLOCKED_IP_LIST` network policy properties and their values.

Before you block all public access with a network rule, ensure that you have a
network rule added to a network policy to allow access to Snowflake. If you
are using private connectivity to the Snowflake service, such as AWS
PrivateLink, configure this service and update the network rule and network
policy accordingly.

If you try to create an empty network policy, no IPv4 addresses are allowed to
access your Snowflake account.

Caution

When defining the network policy for a Snowflake Open Catalog account, ensure
the allowed list of the network policy includes at least one IP address that
you intend to use to access the account. Otherwise, you may get locked out of
the account.

You can create a network policy using [Snowsight](ui-snowsight) or SQL:

Snowsight:

    

  1. Sign in to Snowsight.

  2. Select Admin » Security.

  3. Select the Network Policies tab.

  4. Select \+ Network Policy.

  5. Enter the name of the network policy.

  6. Optionally, enter a descriptive comment.

  7. To add a network rule to the allowed list, select Allowed, and then select Select rule. You can add multiple network rules to the allowed list by re-selecting Select rule.

  8. To add a network rule to the blocked list, select Blocked, and then select Select rule. You can add multiple network rules to the blocked list by re-selecting Select rule.

  9. Select Create Network Policy.

SQL:

    

Execute a [CREATE NETWORK POLICY](../sql-reference/sql/create-network-policy)
statement.

### Identify network policies in your account¶

You can identify the network policies in your account using Snowsight or SQL.

Snowsight:

    

  1. Sign in to Snowsight.

  2. Select Admin » Security.

  3. Select the Network Policies tab.

SQL:

    

Do one of the following:

  * Call the [POLICY_REFERENCES](../sql-reference/functions/policy_references) Information Schema table function.

  * Query the [POLICY_REFERENCES](../sql-reference/account-usage/policy_references) or [NETWORK_POLICIES](../sql-reference/account-usage/network_policies) Account Usage view.

  * Run the [SHOW PARAMETERS](../sql-reference/sql/show-parameters) command as follows:
    
        SHOW PARAMETERS LIKE 'network_policy' IN ACCOUNT;
    

Copy

### Modify a network policy¶

You can add or remove network rules from the allowed list and blocked list of
an existing network policy using Snowsight or SQL. If you are editing a
network policy that uses the `ALLOWED_IP_LIST` and `BLOCKED_IP_LIST`
parameters instead of a network rule, you must use SQL to modify the network
policy.

Snowsight:

    

  1. Sign in to Snowsight.

  2. Select Admin » Security.

  3. Select the Network Policies tab.

  4. Find the network policy, select the … button, and then select Edit.

  5. To add a network rule to the allowed list, select Allowed, and then select Select rule. You can add multiple network rules to the allowed list by re-selecting Select rule.

  6. To add a network rule to the blocked list, select Blocked, and then select Select rule. You can add multiple network rules to the blocked list by re-selecting Select rule.

  7. To remove a network rule from the allowed list or blocked list of the network policy:

    1. Select Allowed or Blocked.

    2. Find the network rule in the list and select X to remove.

SQL:

    

Use the [ALTER NETWORK POLICY](../sql-reference/sql/alter-network-policy)
command to add or remove network rules from an existing network policy.

When adding a network rule to the allowed list or blocked list, you can either
replace all existing network rules in the list or add the new rule while
keeping the existing list. The following examples show each of these options:

  * Use the SET clause to replace network rules in the blocked list with a new network rule named `other_network`:

> >     ALTER NETWORK POLICY my_policy SET BLOCKED_NETWORK_RULE_LIST = (
> 'other_network' );
>  
>
> Copy

  * Use the ADD clause to add a single network rule to the allowed list of an existing network policy. Network rules that were previously added to the policy’s allowed list remain in effect.

> >     ALTER NETWORK POLICY my_policy ADD ALLOWED_NETWORK_RULE_LIST = (
> 'new_rule' );
>  
>
> Copy

You can also remove a network rule from an existing list without replacing the
entire list. For example, to remove a network rule from the network policy’s
blocked list:

    
    
    ALTER NETWORK POLICY my_policy REMOVE BLOCKED_NETWORK_RULE_LIST = ( 'other_network' );
    

Copy

## Activating a network policy¶

A network rule does not restrict inbound network traffic until it has been
activated for an account, user, or security integration. For instructions on
how to activate at each level, see:

  * Activate a network policy for your account

  * Activate network policies for individual users

  * Activate network policies for security integrations

If you are activating multiple network policies at different levels (for
example, both account- and user-level network policies), see Network policy
precedence.

### Activate a network policy for your account¶

Activating a network policy for an account enforces the policy for all users
in the account.

Only security administrators (i.e. users with the SECURITYADMIN role) or
higher or a role with the global ATTACH POLICY privilege can activate a
network policy for an account.

Once the policy is associated with your account, Snowflake restricts access to
your account based on the allowed list and blocked list. Any user who attempts
to log in from an network origin restricted by the rules is denied access. In
addition, when a network policy is associated with your account, any
restricted users who are already logged into Snowflake are prevented from
executing further queries.

You can create multiple network policies, however only one network policy can
be associated with an account at any one time. Associating a network policy
with your account automatically removes the currently-associated network
policy (if any).

Note that your current IP address or private endpoint identifier must be
included in the allowed list in the policy. Otherwise, when you activate the
policy, Snowflake returns an error. In addition, your current identifier
cannot be included in the blocked list.

If you want to determine whether there is already an account-level network
policy before activating a new one, see Identify an activated network policy.

You can activate a network policy for your account using Snowsight or SQL:

Snowsight:

    

  1. Select Admin » Security.

  2. Select the Network Policies tab.

  3. Find the network policy, select the … button, and then select Activate.

  4. Select Activate policy.

SQL:

    

Execute the [ALTER ACCOUNT](../sql-reference/sql/alter-account) statement to
set the [NETWORK_POLICY](../sql-reference/parameters.html#label-network-
policy) parameter for the account. For example:

    
    
    ALTER ACCOUNT SET NETWORK_POLICY = my_policy;
    

Copy

### Activate network policies for individual users¶

To enforce a network policy for a specific user in your Snowflake account,
activate the network policy for the user. Only a single network policy can be
activated for each user at a time. The ability to activate different network
policies for different users allows for granular control. Associating a
network policy with a user automatically removes the currently-associated
network policy (if any).

Note

Only the role with the OWNERSHIP privilege on both the user and the network
policy, or a higher role, can activate a network policy for an individual
user.

Once the policy is associated with the user, Snowflake restricts access to the
user based on the allowed list and blocked list. If the user with an activated
user-level network policy attempts to log in from a network location
restricted by the rules, the user is denied access to Snowflake.

In addition, when a user-level network policy is associated with the user and
the user is already logged into Snowflake, if the user’s network location does
not match the user-level network policy rules, Snowflake prevents the user
from executing further queries.

If you want to determine whether there is already a user-level network policy
before activating a new one, see Identify an activated network policy.

To activate a network policy for an individual user, execute the [ALTER
USER](../sql-reference/sql/alter-user) command to set the
[NETWORK_POLICY](../sql-reference/parameters.html#label-network-policy)
parameter for the user. For example, execute:

    
    
    ALTER USER joe SET NETWORK_POLICY = my_policy;
    

Copy

### Activate network policies for security integrations¶

Some security integrations support activating a network policy to control
network traffic that is governed by that integration. These security
integrations have a NETWORK_POLICY parameter that activates the network policy
for the integration. Currently, SCIM and Snowflake OAuth support integration-
level network policies.

Note

A network policy that is activated for a security integration does not
restrict access to an internal stage.

For example, you could activate a network policy when creating a new Snowflake
OAuth security integration. The network policy would restrict the access of
requests trying to authenticate.

>
>     CREATE SECURITY INTEGRATION oauth_kp_int
>       TYPE = oauth
>       ENABLED = true
>       OAUTH_CLIENT = custom
>       OAUTH_CLIENT_TYPE = 'CONFIDENTIAL'
>       OAUTH_REDIRECT_URI = 'https://example.com'
>       NETWORK_POLICY = mypolicy;
>  
>
> Copy

You can execute the ALTER SECURITY INTEGRATION … SET NETWORK_POLICY statement
to activate a network policy for an existing security integration.

### Identify an activated network policy¶

You can identify which network policy is activated at the account, user, or
integration level.

Account:

    

  1. Select Admin » Security.

  2. Select the Network Policies tab.

  3. Sort the Status column to view the network policies.

The Status column shows active and inactive network policies. Select the
column value to view more details about the network policy, edit the policy,
and delete the network policy. You can activate and deactivate a network
policy that is set on your account.

Alternatively, you can call the [POLICY_REFERENCES](../sql-
reference/functions/policy_references) function and specify a network policy.
The values in the `ref_entity_name` and `ref_entity_domain` columns for an
individual row indicate the object on which the network policy is set.

## Using replication with network policies and network rules¶

Snowflake supports replication and failover/failback for network policies and
network rules, including the assignment of the network policy.

For details, refer to [Replication of security integrations & network policies
across multiple accounts](account-replication-security-integrations).

## Using the Classic Console¶

Note

New features are not being released for Classic Console. Snowflake recommends
using Snowsight or SQL so you can use network rules in conjunction with
network policies.

### Creating a network policy with Classic Console¶

Only security administrators (i.e. users with the SECURITYADMIN role) or
higher or a role with the global CREATE NETWORK POLICY privilege can create
network policies. Ownership of a network policy can be transferred to another
role.

  1. Click Account [![Account tab](../_images/ui-navigation-account-icon.svg)](../_images/ui-navigation-account-icon.svg) » Policies. The Policies page appears.

  2. Click the Create button. The Create Network Policy dialog appears.

  3. In the Name field, enter a name for the network policy.

  4. In the Allowed IP Addresses field, enter one or more IPv4 addresses that are allowed access to this Snowflake account, separated by commas.

> Note
>
> To block all IP addresses except for a set of specific addresses, you only
> need to define an allowed IP address list. Snowflake automatically blocks
> all IP addresses not included in the allowed list.

  5. In the Blocked IP Addresses field, optionally enter one or more IPv4 addresses that are denied access to this Snowflake account, separated by commas. Note that this field is not required and is used primarily to deny specific addresses in a range of addresses in the allowed list.

  6. Enter other information for the network policy, as needed, and click Finish.

### Modifying a network policy with Classic Console¶

If you are using the Classic Console, do the following to modify a network
policy:

  1. Click Account [![Account tab](../_images/ui-navigation-account-icon.svg)](../_images/ui-navigation-account-icon.svg) » Policies.

  2. Click on a policy to select it and populate the side panel on the right.

  3. Click the Edit button in the right panel.

  4. Modify the fields as necessary:

>      * To remove an IP address from the Allowed IP Addresses or Blocked IP
> Addresses list, click the x next to the entry.
>
>      * To add an IP address to either list, enter one or more comma-
> separated IPv4 addresses in the appropriate field, and click the Add button.

  5. Click Save.

### Activating a network policy with Classic Console¶

If you are using the Classic Console, you can enforce a network policy for all
users in your Snowflake account by activating the network policy for your
account.

  1. Click Account [![Account tab](../_images/ui-navigation-account-icon.svg)](../_images/ui-navigation-account-icon.svg) » Policies.

  2. Click on a policy to select it and populate the side panel on the right.

  3. Click the Activate button in the right panel.

