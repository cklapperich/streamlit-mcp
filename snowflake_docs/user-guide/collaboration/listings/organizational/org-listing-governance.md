# Organizational listing governance¶

[![Snowflake logo in black \(no text\)](../../../../_images/logo-snowflake-
black.png)](../../../../_images/logo-snowflake-black.png) [Preview
Feature](../../../../release-notes/preview-features) — Open

Available to all accounts that are Enterprise Edition (or higher).

To inquire about upgrading, please contact [Snowflake
Support](https://docs.snowflake.com/user-guide/contacting-support).

[Organization-level access history](../../../access-history.html#label-access-
history-org-level) provides data governors with the information they need to
track when a consumer’s query reads from a data product made available by a
provider through an organizational listing. The data governor can determine
which account provided the organizational listing and exactly which data
object was accessed. They can also determine if the data object provided by
the organizational listing is protected by a policy (such as a masking policy
or row access policy) in the provider’s account.

You can gain these insights into the consumer queries by using the
[organization account](../../../organization-accounts) to query the
ACCESS_HISTORY view of the ORGANIZATION_USAGE schema. This ACCESS_HISTORY view
contains the following columns related to the governance of organizational
listings:

  * `provider_base_accessed_objects` \- Specifies the data objects in the provider’s account that were accessed by the consumer query.

  * `provider_policies_referenced` \- If a consumer query accessed base objects that are protected by a policy in the provider’s account, this column lists the policy.

For example, if an organization administrator wants to know all the intra-
organization, cross-account queries that have accessed data objects via
organizational listings, they could execute the following query from the
organization account:

    
    
    SELECT * FROM snowflake.organization_usage.access_history
      WHERE provider_base_accessed_objects IS NOT NULL;
    

Copy

