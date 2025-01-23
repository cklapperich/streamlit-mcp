# Data sharing and collaboration in Snowflake¶

There are many ways to share data from your Snowflake account with users in
other Snowflake accounts, including collaborating with other parties in a
secure environment.

## Why share data with Snowflake¶

When you use Snowflake to share data as a provider, you can manage who has
access to your data, and avoid challenges keeping your data synchronized
across different people and groups.

As a data consumer, you can reduce the data transformations you need to
perform because the data stays in Snowflake, making it easy to join datasets
shared with you with your own data.

If you share your data using listings, you can include metadata with your data
share, such as a title and description, and usage examples to help consumers
use the data quickly. In addition to the benefits for consumers, as a provider
you get access to usage data, automatically replicate your data to other
regions, and can even decide to charge for access to your data or offer some
datasets publicly on the Snowflake Marketplace.

## Options for sharing¶

Listings let you share data with people in any Snowflake region, across
clouds, without performing manual replication tasks. If you use listings, you
can provide additional metadata for the data that you share, view customer
data usage, and for listings offered publicly on the Snowflake Marketplace,
gauge consumer interest in your listings.

If you don’t want to share data using a listing, you can use a direct share
instead, see [Secure data sharing](user-guide/data-sharing-intro) and [Non-
secure data sharing](user-guide/data-sharing-views). No matter which option
you choose, you can share with people who don’t have Snowflake accounts by
using [Reader Accounts](user-guide/data-sharing-reader-create).

Data Sharing Mechanism | Share With Whom? | Auto-fulfill Across Clouds? | Optionally Charge for Data? | Optionally Offer Data Publicly? | Get Consumer Usage Metrics?  
---|---|---|---|---|---  
Listing | One or more accounts in any region | Yes | Yes | Yes | Yes  
Direct share | One or more accounts in your region | No | No | No | No  
  
If you want to manage a group of accounts, and control who can publish and
consume listings in that group, consider using a Data Exchange.

## Listing¶

You can offer a listing privately to specific accounts, or publicly on the
Snowflake Marketplace. For more about the Snowflake Marketplace, see [About
Snowflake Marketplace](https://other-
docs.snowflake.com/en/collaboration/collaboration-marketplace-about.html).

After you accept the provider and consumer terms, you can start sharing and
consuming data shared with you with a listing. For more information, see
[About Listings](https://other-
docs.snowflake.com/en/collaboration/collaboration-listings-about.html).

Note

To learn more about sharing listings to or from [Virtual Private Snowflake
(VPS)](user-guide/intro-editions.html#label-snowflake-editions-vps), see
[About collaborating in VPS accounts](https://other-
docs.snowflake.com/en/collaboration/virtual-private-snowflake/about-vps-
collaboration.html).

## Direct share¶

Use a direct share to share data with one or more accounts in the same
Snowflake region. You don’t need to copy or move data shared with a direct
share.

If you want to convert a direct share with active consumers to a listing, see
[Convert a direct share to a listing](https://other-
docs.snowflake.com/en/collaboration/provider-listings-creating-
publishing#convert-a-direct-share-to-a-private-listing).

For more information, see [Share secure database objects](user-guide/data-
sharing-gs).

## Data Exchange¶

If creating listings that you offer privately to specific accounts isn’t an
option, you can use a data exchange to share data with a selected group of
accounts that you invite.

You must request that a data exchange be provisioned and configured for your
account, then you can invite members to the exchange and specify whether they
can consume data, provide data, or both.

For more information, see [About Data Exchange](user-guide/data-exchange).

## Collaborating with shared data in a secure environment¶

When you use listings, direct shares, and Data Exchange to share data with
another party, they can directly access the data. If you want to share data
with other parties, but want to control how that data is accessed, you can use
a Snowflake Data Clean Room to collaborate. The provider who is sharing their
data in a clean room defines what analyses can be run against the shared data,
which allows the consumer to gather insights from the data without having
unrestricted access to it.

For more information, see [About Snowflake Data Clean Rooms](user-
guide/cleanrooms/introduction).

