# Costs associated with apps with containers¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) Feature — Generally
Available

The Snowflake Native App Framework is generally available on supported cloud
platforms. For additional information, see [Support for private connectivity,
VPS, and government regions](limitations.html#label-native-apps-supported-
clouds).

This topic describes the costs associated with developing, publishing and
using a Snowflake Native App with Snowpark Container Services. It contains
information for both providers and consumers.

## Costs to consumers¶

A Snowflake Native App may incur costs in the consumer account. The total cost
of running a Snowflake Native App with Snowpark Container Services is
determined by the following:

  * Costs determined by the provider

  * Infrastructure costs

### Costs determined by the provider¶

A provider may monetize a Snowflake Native App using any of the [paid listing
pricing models](https://other-docs.snowflake.com/en/collaboration/provider-
becoming#label-monetization-provider-onboarding) that are available in the
Snowflake Marketplace. These models include subscription based and usage based
plans.

This cost to the consumer is determined by the provider. Consumers pay for
provider software via the Snowflake Marketplace in addition to costs
associated with running Snowflake infrastructure, including warehouses and
compute pools.

### Infrastructure costs¶

All infrastructure costs, including those related to compute pools, warehouse
compute, storage, and data transfer are the responsibility of the consumer of
a Snowflake Native App.

A consumer can use the IN ACCOUNT clause of the [SHOW COMPUTE
POOLS](../../sql-reference/sql/show-compute-pools) command to see all compute
pools in their account and the current state of the compute pool. Costs are
not incurred when a compute pool is suspended.

A Snowflake Native App with Snowpark Container Services requires at least one
compute pool and might require multiple compute pools to run as intended. A
consumer has full control over the compute resources that the app requires,
and may suspend a compute pool or drop an application at any time.

Separate charges for compute pool compute related to the Snowflake Native App
with Snowpark Container Services appear on the customer billing statement. A
consumer can determine the compute pool billing charges for a Snowflake Native
App with Snowpark Container Services using the [ACCOUNT USAGE
views](../snowpark-container-services/accounts-orgs-usage-views) provided by
Snowpark Container Services.

For more details, such as the consumption table for compute pools, contact
your account representative.

## Costs to providers¶

Providers can also incur costs when developing and maintaining a Snowflake
Native App with Snowpark Container Services, including the following:

  * Providers incur Snowpark Container Services compute costs associated with both initial development and ongoing testing and support for their Snowflake Native App. The compute cost may be controlled through orchestration of compute pools during provider-side development and testing.

  * The storage of container images can incur costs when a provider creates a new version or patch of a Snowflake Native App with Snowpark Container Services. In this context, the Docker images that the app requires are copied into an image repository that is not directly accessible or observable by the provider or the consumer.

Services in the consumer account are created from the versioned images that
are stored in this repository. Providers are responsible for the storage costs
for the images in this stage, which appear on their Snowflake bill. These
costs are aggregated with other storage costs that their account incurs.

