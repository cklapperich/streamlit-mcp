# Supported Cloud Regions¶

Regions let your organization choose where your data is geographically stored
across your regional, national, and international operations. Regions also
determine where your compute resources are provisioned.

Snowflake supports regions across all of the Snowflake-supported [cloud
platforms](intro-cloud-platforms), grouped into three global geographic
segments (North/South America, Europe/Middle East, and Asia Pacific/China).

[![World map of cloud regions supported by Snowflake](../_images/snowflake-
regions.png)](../_images/snowflake-regions.png)

Important

Each Snowflake account is hosted in a single region. If you wish to use
Snowflake across multiple regions, you must maintain a Snowflake account in
each of the desired regions.

## North & South America¶

These regions are supported for organizations that prefer or require their
data to be stored in the United States, Canada, or Brazil. Multiple regions
are provided to allow your organization to meet its individual compliance
requirements for general purpose use.

Additional regions are provided in the United States for organizations that
must comply with US government regulations.

### Commercial Regions¶

[![Map of North and South American commercial cloud regions supported by
Snowflake](../_images/snowflake-regions-americas.png)](../_images/snowflake-
regions-americas.png)

Snowflake supports the following regions in North America (U.S. and Canada)
and South America (Brazil) for general commercial use:

Cloud Platform | Cloud Region ID [1] | Region Name | Additional Notes  
---|---|---|---  
**Amazon Web Services (AWS)**  
[![Amazon Web Services \(AWS\) region](../_images/pin-aws.png)](../_images/pin-aws.png) | ca-central-1 | Canada (Central) |   
sa-east-1 | South America (Sao Paulo) |   
us-west-2 | US West (Oregon) |   
us-east-2 | US East (Ohio) |   
us-east-1 | US East (N. Virginia) | Also supports some U.S. government compliance (see next section for details).  
**Google** **Cloud** **Platform** **(GCP)**  
[![Google Cloud Platform \(GCP\) region](../_images/pin-gcp.png)](../_images/pin-gcp.png) | us-central1 | US Central1 (Iowa) |   
us-east4 | US East4 (N. Virginia) |   
**Microsoft Azure**  
[![Microsoft Azure region](../_images/pin-msazure.png)](../_images/pin-msazure.png) | canadacentral | Canada Central (Toronto) |   
centralus | Central US (Iowa) |   
eastus2 | East US 2 (Virginia) |   
southcentralus | South Central US (Texas) | Also supports some U.S. government compliance (see next section for details).  
westus2 | West US 2 (Washington) |   
  
[1] See the map preceding this table for the location of each supported
region, labeled by cloud region ID.

### U.S. Regions Supporting Public Sector Workloads¶

[![Map of U.S. cloud regions that support public sector/government
workloads](../_images/snowflake-regions-us-gov.png)](../_images/snowflake-
regions-us-gov.png)

Snowflake makes the following regions available to customers that require
compliance with common U.S. Federal and state government standards. These
regions are only supported for Snowflake accounts on Business Critical Edition
(or higher).

Note

If your Snowflake account is in a U.S. government region and you want to
access data products that are offered privately or on the Snowflake
Marketplace, or offer listings either privately or on the Snowflake
Marketplace, you must review and acknowledge a cross-region disclaimer for
your [organization](organizations).

For details, see:

  * [Prepare to provide listings from accounts in U.S. government regions](https://other-docs.snowflake.com/en/collaboration/provider-becoming#label-listings-setup-gov-provider)

  * [Prepare to access listings from accounts in U.S. government regions](https://other-docs.snowflake.com/en/collaboration/consumer-becoming#label-listings-setup-gov-consumer)

  * [Limitations for accessing listings from accounts in U.S. government regions](https://other-docs.snowflake.com/en/collaboration/consumer-listings-access#label-listings-gov-consumer-limitations)

U.S. commercial regions with some support for government standards

    

The following commercial regions meet the requirements for Snowflake’s
compliance with the U.S. government standards set forth in the table below. By
uploading workloads covered by the below compliance standards, customers agree
to [Snowflake’s U.S. Government Commercial Compliance
Addendum](https://www.snowflake.com/legal-gov/us-gov-commercial-compliance-
addendum/).

Cloud Region ID | Region Name | Compliance standards  
---|---|---  
**Amazon** **Web** **Services** |  |   
us-east-1 | US East (Commercial Gov - N. Virginia) | 

  * [FedRAMP](cert-fedramp) (Moderate)
  * [StateRAMP](cert-stateramp) (Moderate)
  * TX-RAMP (Level 2)
  * FIPS 140-2

  
us-east-1 | US East (N. Virginia) | 

  * TX-RAMP (Level 2, Provisional)

  
us-west-2 | US West (Commercial Gov - Oregon) | 

  * [FedRAMP](cert-fedramp) (Moderate)
  * [StateRAMP](cert-stateramp) (Moderate)
  * TX-RAMP (Level 2)
  * FIPS 140-2

  
**Microsoft Azure** |  |   
southcentralus | South Central US (Texas) | 

  * TX-RAMP (Level 2)

  
  
U.S. SnowGov Regions

    

Snowflake makes the following SnowGov Regions on AWS GovCloud (US) (us-gov-
west-1 and us-gov-east-1) and Microsoft Azure Government (usgovvirginia)
available to customers who require additional security designed for US
government regulated workloads and other types of sensitive data. These
regions are operated by Snowflake personnel who are U.S. persons located
within the U.S. Certain features that are available in Snowflake’s commercial
regions may not be available or may be different in its SnowGov Regions. Use
of and access to Snowflake in any of the SnowGov Regions are limited solely to
U.S. Government Customers or U.S. Government Contractors (unless otherwise
agreed upon by Snowflake in its sole discretion) and are subject to
Snowflake’s U.S. SnowGov Region Terms of Service. As used here, a “U.S.
Government Customer” means a Snowflake customer that is: (a) a U.S. Federal,
state, or local government entity or (b) a tribal government entity; and a
“U.S. Government Contractor” means a commercial entity that is required to
process data provided by a U.S. Government Customer to perform a prime
contract or subcontract with or for such entity.

The SnowGov Regions support U.S. government standards, such as FedRAMP, DoD
Impact Levels, StateRAMP, TX-RAMP, FIPS-140-2, and the International Traffic
in Arms Regulations (ITAR) by default. As noted in the table below, certain
standards require the customer to accept supplemental contract terms. You must
contact Snowflake and agree to the supplemental terms before uploading
workloads covered by these standards.

Self-provisioning of initial Snowflake accounts is not available in the
SnowGov Regions. To provision an initial account in these regions, you must
contact Snowflake.

Cloud Region ID | Region Name | Workloads Supported by Default | Workloads Requiring Supplemental Contract Terms  
---|---|---|---  
**Amazon** **Web** **Services** |  |  |   
us-gov-east-1 | US Gov East 1 (FedRAMP High Plus) | 

  * [FedRAMP](cert-fedramp) (High)
  * Department of Defense (DoD) Impact Level 4 (IL4)
  * [StateRAMP](cert-stateramp) (High)
  * TX-RAMP (Level 2)
  * FIPS 140-2
  * NIST 800-171
  * [ITAR](cert-itar)

|

  * DFARS 252.204-7012
  * DFARS 252.239-7010
  * Department of Justice (DoJ) Criminal Justice Information Systems ([CJIS](cert-cjis)) Security Policy
  * IRS Publication 1075

  
us-gov-west-1 | US Gov West 1 (FedRAMP High Plus) | 

  * [FedRAMP](cert-fedramp) (High)
  * DoD IL4
  * [StateRAMP](cert-stateramp) (High)
  * TX-RAMP (Level 2)
  * FIPS 140-2
  * NIST 800-171
  * [ITAR](cert-itar)

|

  * DFARS 252.204-7012
  * DFARS 252.239-7010
  * DoJ [CJIS](cert-cjis) Security Policy
  * IRS Publication 1075

  
us-gov-west-1 | US Gov West 1 (DoD) | 

  * DoD IL4
  * BCAP
  * FIPS 140-2
  * NIST 800-171
  * [ITAR](cert-itar)

|

  * DFARS 252.204-7012
  * DFARS 252.239-7010
  * DoJ [CJIS](cert-cjis) Security Policy
  * IRS Publication 1075

  
**Microsoft Azure Government** |  |  |   
usgovvirginia | US Gov Virginia (FedRAMP High Plus) | 

  * FedRAMP (High) — _Planned_
  * StateRAMP (High) — _Planned_
  * TX-RAMP (Level 2) — _Planned_
  * FIPS 140-2
  * NIST 800-171
  * [ITAR](cert-itar)

|

  * DFARS 252.204-7012
  * DOJ [CJIS](cert-cjis) Security Policy
  * IRS Publication 1075

  
usgovvirginia | US Gov Virginia | 

  * [FedRAMP](cert-fedramp) (Medium)
  * [StateRAMP](cert-stateramp) (Moderate)
  * TX-RAMP (Level 2)
  * FIPS 140-2
  * NIST 800-171
  * [ITAR](cert-itar)

|

  * DFARS 252.204-7012
  * DOJ [CJIS](cert-cjis) Security Policy
  * IRS Publication 1075

  
  
Note that the government regions of the cloud providers do not allow event
notifications to be sent to or from other commercial regions. For more
information, see [AWS GovCloud (US)](https://docs.aws.amazon.com/govcloud-
us/latest/UserGuide/govcloud-s3.html) and [Azure
Government](https://learn.microsoft.com/en-us/azure/azure-government/).

## Europe & Middle East¶

These regions are supported for organizations that prefer or require their
data to be stored in the European Union (EU), United Kingdom (UK), or Middle
East. Multiple regions are provided to allow your organization to meet its
individual compliance and data sovereignty requirements.

[![Map of Europe and Middle East cloud regions supported by
Snowflake](../_images/snowflake-regions-europe.png)](../_images/snowflake-
regions-europe.png)

Snowflake supports the following European and Middle East regions:

Cloud Platform | Cloud Region ID [1] | Region Name | Additional Notes  
---|---|---|---  
**Amazon Web Services (AWS)**  
[![Amazon Web Services \(AWS\) region](../_images/pin-aws.png)](../_images/pin-aws.png) | eu-central-1 | EU (Frankfurt) |   
eu-central-2 | EU (Zurich) |   
eu-north-1 | EU (Stockholm) |   
eu-west-1 | EU (Ireland) |   
eu-west-2 | Europe (London) |   
eu-west-3 | EU (Paris) |   
**Google Cloud Platform (GCP)**  
[![Google Cloud Platform \(GCP\) region](../_images/pin-gcp.png)](../_images/pin-gcp.png) | me-central2 | Middle East Central2 (Dammam) |   
europe-west2 | Europe West2 (London) |   
europe-west3 | Europe West3 (Frankfurt) |   
europe-west4 | Europe West4 (Netherlands) |   
**Microsoft Azure**  
[![Microsoft Azure region](../_images/pin-msazure.png)](../_images/pin-msazure.png) | northeurope | North Europe (Ireland) |   
switzerlandnorth | Switzerland North (Zurich) |   
westeurope | West Europe (Netherlands) |   
uaenorth | UAE North (Dubai) |   
uksouth | UK South (London) |   
  
[1] See the map preceding this table for the location of each supported
region, labeled by cloud region ID.

## Asia Pacific & China¶

These regions are supported for organizations that prefer or require their
data to be stored in Japan, Korea, India, Southeast Asia, Australia, and
China. Multiple regions are provided to allow your organization to meet its
individual compliance and data sovereignty requirements.

[![Map of Asia Pacific and China cloud regions supported by
Snowflake](../_images/snowflake-regions-
asiapacific.png)](../_images/snowflake-regions-asiapacific.png)

Snowflake supports the following Asia Pacific and China regions:

Cloud Platform | Cloud Region ID [1] | Region Name | Additional Notes  
---|---|---|---  
**Amazon Web Services (AWS)**  
[![Amazon Web Services \(AWS\) region](../_images/pin-aws.png)](../_images/pin-aws.png) | ap-northeast-1 | Asia Pacific (Tokyo) |   
ap-northeast-2 | Asia Pacific (Seoul) |   
ap-northeast-3 | Asia Pacific (Osaka) |   
ap-south-1 | Asia Pacific (Mumbai) |   
ap-southeast-1 | Asia Pacific (Singapore) |   
ap-southeast-2 | Asia Pacific (Sydney) | This region can be used by government agencies that require compliance with Australian privacy and security standards, such as IRAP (Protected).  
ap-southeast-3 | Asia Pacific (Jakarta) |   
cn-northwest-1 | China (Ningxia) | The China region is separate from other Snowflake regions. It utilizes a separate domain name (`snowflakecomputing.cn`) and is wholly operated by Digital China Cloud Technology Limited (DCC), an authorized operating partner of Snowflake, Inc. Customers who wish to create and use Snowflake accounts in the China region must sign a separate agreement with DCC in accordance with all applicable rules and regulations. Additionally, customers cannot use self-service to create their initial account in the China region. Instead, they must request the account through [DCC](mailto:snowflake.hosting%40dcclouds.com). Once the initial account is created within their org, they can create additional accounts in the org using all other supported methods. Customers with existing Snowflake accounts ae not able to access resources in the China region, and vice versa. Some features may not be available in the China region.  
**Microsoft Azure**  
[![Microsoft Azure region](../_images/pin-msazure.png)](../_images/pin-msazure.png) | australiaeast | Australia East (New South Wales) | This region can be used by government agencies that require compliance with Australian privacy and security standards, such as IRAP (Protected).  
centralindia | Central India (Pune) |   
japaneast | Japan East (Tokyo) |   
southeastasia | Southeast Asia (Singapore) |   
  
[1] See the map preceding this table for the location of each supported
region, labeled by cloud region ID.

## Region Time Zones for Support¶

Snowflake supports multiple [editions](intro-editions) with each edition
offering different levels of service.

Effective May 1, 2020:

  * All new accounts, regardless of Snowflake Edition, receive Premier support, which includes 24/7 coverage.

  * Standard Edition accounts that were provisioned before this date will continue to receive Standard support until the accounts are transitioned to Premier support.

Standard support hours are Monday - Friday, 6:00 AM - 6:00 PM, across all
regions, but the time zones vary depending on the geographic location of the
region:

> North America:
>  
>
> Pacific Time (PST or PDT)
>
> Europe & Middle East:
>  
>
> Central Europe Time (CET or CEST)
>
> Asia Pacific:
>  
>
> Australian Eastern Time (AEST or AEDT)

## Differences Between Regions¶

Snowflake features and services are identical across regions except for some
newly-introduced features (based on cloud platform or region). However, there
are some differences in unit costs for credits and data storage between
regions.

Another factor that impacts unit costs is whether your Snowflake account is
_On Demand_ or _Capacity_.

For more information about pricing as it pertains to a specific region and
account type, see the [pricing page](http://www.snowflake.com/pricing) (on the
Snowflake website).

## Viewing a List of Regions Available for an Organization¶

A organization administrator (i.e. user with the ORGADMIN role) can view a
list of regions available for an organization through [Snowsight](ui-
snowsight) or using SQL:

> Snowsight:
>  
>
> Select Admin » Accounts » Create New Account » Choose Your Region.
>
> SQL:
>  
>
> Execute the [SHOW REGIONS](../sql-reference/sql/show-regions) command.

## Considerations for Choosing a Region for Your Account¶

When you request a Snowflake account, either through self-service or a
Snowflake representative, you can choose the region where the account is
located. For example, you can decide to locate an account in a particular
region on a particular cloud platform to address latency concerns and/or
provide additional backup and disaster recovery beyond the standard recovery
support provided by Snowflake. Snowflake does not place any restrictions on
the region where you choose to locate each account.

If latency is a concern, you should choose the available region with the
closest geographic proximity to your end users; however, this may have cost
implications, due to pricing differences between the regions. For more
details, see the [pricing page](http://www.snowflake.com/pricing) (on the
Snowflake website).

If you are a government agency or a commercial organization that must comply
with specific privacy and security requirements of the US government, you can
choose between two dedicated government regions provided by Snowflake.

Important

Regions do not limit user access to Snowflake; they only dictate the
geographic location where data is stored and compute resources are
provisioned.

In addition, Snowflake does not move data between accounts, so any data in an
account in a region remains in the region unless users explicitly choose to
copy, move, or [replicate](account-replication-intro) the data.

## Specifying Region Information in Your Account Hostname¶

A hostname for a Snowflake account starts with an _account identifier_ and
ends with the Snowflake domain (`snowflakecomputing.com`). Snowflake supports
two formats to use as the [account identifier](admin-account-identifier) in
your hostname:

  * Account name (preferred)

  * Account locator

Important

If you choose the account locator as your account identifier, you may need to
include additional segments in the locator that specify the cloud region and
[cloud platform](intro-cloud-platforms) where your account is hosted.

For more details, see [Format 2: Account locator in a region](admin-account-
identifier.html#label-account-locator).

