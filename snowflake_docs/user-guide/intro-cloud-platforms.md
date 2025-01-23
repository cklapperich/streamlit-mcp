# Supported Cloud Platforms¶

Snowflake is provided as a self-managed service that runs completely on cloud
infrastructure. This means that all three layers of [Snowflake’s
architecture](intro-key-concepts) (storage, compute, and cloud services) are
deployed and managed entirely on a selected cloud platform.

A Snowflake account can be hosted on any of the following cloud platforms:

  * [Amazon Web Services (AWS)](https://aws.amazon.com/)

  * [Google Cloud Platform (GCP)](https://cloud.google.com/)

  * [Microsoft Azure (Azure)](https://azure.microsoft.com/en-us/)

On each platform, Snowflake provides one or more [regions](intro-regions)
where the account is provisioned.

If your organization’s other cloud services are already hosted on one of these
platforms, you can choose to host all your Snowflake accounts on the same
platform. However, you can also choose to host your accounts on a different
platform.

Note

The cloud platform you choose for each Snowflake account is completely
independent from your other Snowflake accounts. In fact, you can choose to
host each Snowflake account on a different platform, although this may have
some impact on data transfer billing when loading data.

## Pricing¶

Differences in unit costs for credits and data storage are calculated by
[region](intro-regions) on each cloud platform. For more information about
pricing as it pertains to a specific region and platform, see the [pricing
page](http://www.snowflake.com/pricing) (on the Snowflake website).

## Data Loading¶

Snowflake supports loading data from files staged in any of the following
locations, regardless of the cloud platform for your Snowflake account:

  * Internal (i.e. Snowflake) stages

  * Amazon S3

  * Google Cloud Storage

  * Microsoft Azure blob storage

Snowflake supports both bulk data loading and continuous data loading
(Snowpipe). Likewise, Snowflake supports unloading data from tables into any
of the above staging locations.

For more information, see [Load data into Snowflake](../guides-overview-
loading-data).

Note

Some data transfer billing charges may apply when loading data from files
staged across different platforms. For more information, see [Understanding
data transfer cost](cost-understanding-data-transfer).

## HITRUST CSF Certification¶

This certification enhances Snowflake’s security posture in regulatory
compliance and risk management, and is applicable to Snowflake editions that
are Business Critical (or higher). For more information, see [Snowflake
Security and Trust Center](https://www.snowflake.com/product/security-and-
trust-center/).

## Partner Applications¶

Many partner applications work with Snowflake accounts. For more information,
refer to [Snowflake ecosystem](ecosystem).

## Current Limitations for Accounts on GCP¶

We strive to provide the same Snowflake experience regardless of the cloud
platform you choose for your account; however, some services and features are
currently unavailable (or have limited availability) for Snowflake accounts
hosted on Google Cloud Platform (GCP).

### Google Cloud Private Service Connect¶

See the [limitations](private-service-connect-google.html#label-gcp-psc-
limitations) section for using Google Cloud Private Service Connect and
Snowflake.

Note that following Snowflake system functions for self-service management are
not supported for Google Cloud Private Service Connect for your Snowflake
account on GCP:

  * [SYSTEM$AUTHORIZE_PRIVATELINK](../sql-reference/functions/system_authorize_privatelink)

  * [SYSTEM$REVOKE_PRIVATELINK](../sql-reference/functions/system_revoke_privatelink)

  * [SYSTEM$GET_PRIVATELINK](../sql-reference/functions/system_get_privatelink)

  * [SYSTEM$GET_PRIVATELINK_AUTHORIZED_ENDPOINTS](../sql-reference/functions/system_get_privatelink_authorized_endpoints)

### Network Rules¶

[Network rules](network-rules) are not supported on GCP.

### Private Connectivity to Internal Stages¶

Private connectivity to Snowflake internal stages is currently not supported
on GCP. You cannot prevent public IP addresses from accessing an internal
stage because there wouldn’t be a method of accessing the internal stage.

### Snowpark Container Services¶

[Snowpark Container Services](../developer-guide/snowpark-container-
services/overview) is currently not supported on GCP.

### Snowflake Open Catalog¶

[Snowflake Open Catalog](https://other-
docs.snowflake.com/en/opencatalog/overview) is currently not available in
government regions.

## Current Limitations for Accounts on AWS¶

We strive to provide the same Snowflake experience regardless of the cloud
platform you choose for your account; however, some services and features are
currently unavailable (or have limited availability) for Snowflake accounts
hosted on AWS.

### Access to External Network Locations¶

[Access to external network locations](../developer-guide/external-network-
access/external-network-access-overview) from UDF and procedure handler code
is currently not supported in the Gov region.

### Snowflake Open Catalog¶

[Snowflake Open Catalog](https://other-
docs.snowflake.com/en/opencatalog/overview) is currently not available in
government regions.

## Current limitations for accounts on Azure¶

We strive to provide the same Snowflake experience regardless of the cloud
platform you choose for your account; however, some services and features are
currently unavailable (or have limited availability) for Snowflake accounts
hosted on Microsoft Azure.

### Azure Private Link¶

See [Azure Private Link Requirements and Limitations](privatelink-
azure.html#label-pl-azure-reqs-limits).

### Snowflake Clients¶

Currently, using the account name URL format for private connectivity to the
Snowflake service with [SnowSQL](snowsql), [connectors](connectors) and
[drivers](../developer-guide/drivers) is not supported. As a workaround, use
the account locator format with SnowSQL, connectors, and drivers.

For details, see:

  * [Account identifiers](admin-account-identifier)

  * [Connecting to your accounts](organizations-connect)

### Access to External Network Locations¶

[Access to external network locations](../developer-guide/external-network-
access/external-network-access-overview) from UDF and procedure handler code
is currently not supported in the Gov region.

### Snowpark Container Services¶

[Snowpark Container Services](../developer-guide/snowpark-container-
services/overview) is currently not supported on Azure.

### Snowflake Open Catalog¶

[Snowflake Open Catalog](https://other-
docs.snowflake.com/en/opencatalog/overview) is currently not available in
government regions.

