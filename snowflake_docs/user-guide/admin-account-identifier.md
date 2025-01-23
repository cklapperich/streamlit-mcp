# Account identifiers¶

An account identifier uniquely identifies a Snowflake account within your
[organization](organizations), as well as throughout the global network of
Snowflake-supported [cloud platforms](intro-cloud-platforms) and [cloud
regions](intro-regions).

The preferred account identifier consists of the _name_ of the account
prefixed by its organization (e.g. `myorg-account123`). You can also use the
Snowflake-assigned _locator_ as the account identifier; however, the use of
this legacy format is discouraged.

## Where are account identifiers used?¶

Account identifiers are required in Snowflake wherever you need to specify the
account you are using, including:

  * URLs for accessing any of the Snowflake web interfaces.

  * SnowSQL and other clients (connectors, drivers, etc.) for connecting to Snowflake.

  * Third-party applications and services that comprise the Snowflake ecosystem.

  * Security features for protecting Snowflake internal operations and communication/interaction with external systems.

  * Global features such as [Secure Data Sharing](data-sharing-intro) and [Replication and Failover/Failback](replication-intro).

For example, the URL for an account uses the following format:

`_account_identifier_.snowflakecomputing.com`

If your organization uses the [Client Redirect](client-redirect) feature, the
name of a [connection object](client-redirect.html#label-intro-to-client-
redirect) can be used in place of the account name in the account identifier
to connect to a Snowflake account using a Snowflake client. For more
information, see [Using a connection URL](client-redirect.html#label-using-a-
connection-url).

For more information about using account identifiers and connections to
connect to a Snowflake account, see [Connecting to your
accounts](organizations-connect).

## Format 1 (preferred): Account name in your organization¶

An [organization](organizations) is a Snowflake object that links the accounts
owned by your business entity. Organizations enable organization
administrators (i.e. users with the ORGADMIN role) to view, create, and manage
all of your accounts across different cloud platforms and regions.

Account names must be unique within your organization, and can be changed,
which allows more flexibility and leads to shorter and more intuitive account
names. You specify an account name when you create a new account (see
[Creating an account](organizations-manage-accounts-create)). To change a name
for an existing account, see [Renaming an account](organizations-manage-
accounts-rename).

While an account name uniquely identifies an account within your organization,
it is not a unique identifier of an account across Snowflake organizations.

Account names with underscores also have a dashed version of the URL for
features that do not accept URLs with underscores, such as Okta SSO/SCIM.

### Using an account name as an identifier¶

The account identifier for an account in your organization takes one of the
following forms, depending on where and how you use the identifier:

  * Specifying the account name when connecting to Snowflake

  * Specifying the fully qualified account name in a SQL statement

#### Specifying the account name when connecting to Snowflake¶

The following table lists some of the commonly used forms of the account
identifier, based on the use case:

Use cases | Format to use  
---|---  
Using a URL to [sign in to Snowsight](ui-snowsight-gs.html#label-snowsight-getting-started-sign-in). | `_orgname_ -_account_name_.snowflakecomputing.com`  
Specifying the Snowflake account URL when configuring a third-party tool (such as Tableau or PowerBI) to [connect to Snowflake](gen-conn-config): | `_orgname_ -_account_name_.snowflakecomputing.com`  
Specifying the Snowflake account when configuring a client, driver, or library
to [connect to Snowflake](gen-conn-config):

  * Specifying the account in a configuration file for a client (such as [Snowflake CLI](../developer-guide/snowflake-cli/index) or [SnowSQL](snowsql))
  * Specifying the when configuring a driver (such as the [ODBC](../developer-guide/odbc/odbc) or [JDBC](../developer-guide/jdbc/jdbc) driver) or library to

| `_orgname_ -_account_name_`  
  
Where:

  * `_orgname_` is the name of your Snowflake organization.

  * `_account_name_` is the unique name of your account within your organization.

Note

For scenarios/features where underscores in an account name are not supported,
use hyphens instead of underscores.

For example, in a [configuration file for Snowflake CLI](../developer-
guide/snowflake-cli/connecting/configure-cli), if your organization is
`myorganization` and your account is `myaccount`, set `account` to:

    
    
    [connections]
    [connections.myconnection]
    account = "myorganization-myaccount"
    

Copy

#### Specifying the fully qualified account name in a SQL statement¶

In a SQL statement, when specifying the fully qualified account name, use a
period between the organization name and account name:

> `_orgname_._account_name_`

### Finding the organization and account name for an account¶

To find the organization and account name for an account, you can use
Snowsight or SQL.

Snowsight:

    

  1. Open the account selector and review the list of accounts that you previously signed in to.

> [![Screenshot of the account selector open and listing multiple accounts.
> The account selector is labeled with the name of the currently-selected
> account.](../_images/snowsight-gs-account-
> selector.png)](../_images/snowsight-gs-account-selector.png)

  2. Locate the account for which you want to copy the account name.

  3. Hover over the account to view additional details, and then select the copy icon to copy the account identifier in the format `_orgname_._account_name_` to your clipboard.

> [![Screenshot of the account selector open and listing multiple accounts,
> with a cursor hovering over an account to display an additional pane of
> information about the account and hovering over the option to copy the
> account identifier.](../_images/ui-snowsight-account-
> identifier.png)](../_images/ui-snowsight-account-identifier.png)

Note

The account identifier is copied in the format `_orgname_._account_name_`,
which is used for SQL commands and operations.

If you need to use the account identifier with a Snowflake driver (for
example, JDBC or ODBC), you need to replace the period (`.`) with a hyphen
(`-`) so the identifier is formatted as `_orgname_ -_account_name_`.

SQL:

    

  * To retrieve the organization of the current account, call the [CURRENT_ORGANIZATION_NAME](../sql-reference/functions/current_organization_name) function.

  * To retrieve the name of the current account, call the [CURRENT_ACCOUNT_NAME](../sql-reference/functions/current_account_name) function.

For example, to get the account identifier for configuring a client, driver,
or library to connect to Snowflake, run:

    
    
    SELECT CURRENT_ORGANIZATION_NAME() || '-' || CURRENT_ACCOUNT_NAME();
    

Copy

### Organization and account names¶

#### Organization name¶

For users who sign up for a Snowflake account using the self-service option,
an organization is automatically created with a system-generated name when the
account is created. For entities who work directly with Snowflake personnel to
set up accounts, Snowflake can assign the organization a custom name. This
custom name must be unique across all other organizations in Snowflake. The
name must start with a letter and can only contain letters (lowercase and
uppercase) and numbers. The name cannot contain underscores or other
delimiters.

If you want to change the name of an organization, for example to change a
system-generated name to a more user-friendly one, contact [Snowflake
Support](https://docs.snowflake.com/user-guide/contacting-support).

As a best practice, review and change your organization name, if needed,
before using the name in any account identifiers. Renaming the organization
name in the future will result in changing all the URLs for your Snowflake
accounts to match the new name.

To view the name of your organization, see [Viewing the name of your
organization and its accounts](organizations-gs.html#label-viewing-
organization-name).

#### Account name¶

Each account name must be unique within your organization. You specify an
account name when you create the account (see [Creating an
account](organizations-manage-accounts-create)).

While an account name uniquely identifies an account within your organization,
it is not a unique identifier of an account across Snowflake organizations. To
uniquely identify an account in Snowflake, you must prepend your organization
name to the account name. For example:

`_orgname_ -_account_name_`

Consistent with SQL standards for identifiers, account names can include
underscores as separators between words (e.g. `MARKETING_TEST_ACCOUNT`).

URLs that include underscores can sometimes cause issues for certain features,
such as Okta SSO/SCIM. For this reason, Snowflake also supports a version of
the account name that substitutes the hyphen character (`-`) in place of the
underscore character. For example both of the following URLs are supported:

> URL with underscores: `https://acme-
> marketing_test_account.snowflakecomputing.com`
>
> URL with dashes: `https://acme-marketing-test-
> account.snowflakecomputing.com`

#### Existing accounts¶

If you have any accounts that existed before the Organizations feature was
enabled, the Format 2: Account locator in a region is used as the account
name.

In addition, if you have existing accounts with the same name in different
regions, the cloud and region names are appended to the account name in the
new URL format.

For example, if your organization name is `ACME`, and there are two accounts
named `TEST`, one in the AWS `us-east-2` region and the other in the Azure
`west-us-2` region, the new URLs will use the following structure:

  * First account:

Original URL:

    

`https://test.us-east-2.aws.snowflakecomputing.com`

New URL:

    

`https://acme-test_aws_us_east_2.snowflakecomputing.com`

  * Second account:

Original URL:

    

`https://test.west-us-2.azure.snowflakecomputing.com`

New URL:

    

`https://acme-test_azure_west_us_2.snowflakecomputing.com`

These account names can be changed as long as the new names are unique. For
instructions on how to change an account name, see [Renaming an
account](organizations-manage-accounts-rename).

## Format 2: Account locator in a region¶

An account locator is an identifier assigned by Snowflake when the account is
created:

  * If the account is created by a Snowflake representative, you may be able to request a specific value for the locator, such as a company name, acronym, or other recognizable string.

  * If the account is created through self-service or an automated/background process, the locator is a random string of unique characters and numbers (e.g. `xy12345`).

The locator for an account cannot be changed once the account is created.

Note

Account locators continue to be supported for identifying accounts in
Snowflake, but this is no longer the preferred method. The preferred method
for identifying accounts is now the account name within your organization (as
described earlier in this topic).

### Using an account locator as an identifier¶

Each Snowflake account is hosted on a [cloud platform](intro-cloud-platforms)
in a geographical [region](intro-regions).

The region determines where the data in the account is stored and where the
compute resources used by the account are provisioned.

When using an account locator to identify an account, the locator by itself is
not always sufficient to identify the account. Depending on the region and
cloud platform for the account, additional segments may be required, in the
form of:

`_account_locator_._cloud_region_id_` or

`_account_locator_._cloud_region_id_._cloud_` or

`_account_locator_._gov_compliance_._cloud_region_id_._cloud_`

Where:

  * `_cloud_region_id_` is the identifier for the cloud region (dictated by the cloud platform).

  * `_cloud_` is the identifier for the cloud platform (`aws`, `azure`, or `gcp`).

  * `_compliance_` is for SnowGov regions only and specifies the level of U.S. government compliance supported by the region (`fhplus` or `dod`).

For example, if your account locator is `xy12345`:

  * If the account is located in the AWS US West (Oregon) region, no additional segments are required and the URL would be `xy12345.snowflakecomputing.com`.

  * If the account is located in the AWS US East (Ohio) region, additional segments are required and the URL would be `xy12345.us-east-2.aws.snowflakecomputing.com`.

For a complete list of regions and locator formats, see Non-VPS Account
Locator Formats by Cloud Platform and Region (in this topic).

Note

If your Snowflake Edition is [VPS](intro-editions.html#label-snowflake-
editions-vps), the account locator uses a different format. See Finding the
account locator format for a VPS account (in this topic).

### Finding the region and locator for an account¶

If you can connect to your Snowflake account, you can query the following
context functions to identify the region and account locator for the Snowflake
account you are connected to:

  * [CURRENT_REGION](../sql-reference/functions/current_region) retrieves the region in which your account is located.

  * [CURRENT_ACCOUNT](../sql-reference/functions/current_account) retrieves the account locator.

If you are unable to connect to Snowflake, contact the Snowflake administrator
for your account to retrieve this information.

### Finding the account locator format for a VPS account¶

If your Snowflake Edition is [VPS](intro-editions.html#label-snowflake-
editions-vps), the account locator format uses different naming conventions
than the accounts for other Snowflake Editions. This results in a different
structure for the hostnames and URLs used to access VPS accounts.

For details, please contact [Snowflake
Support](https://docs.snowflake.com/user-guide/contacting-support) or your
Snowflake representative.

As an alternative, you can use the preferred format of `_organization_name_
-_account_name_` as your account identifier. This format works for accounts
that use the VPS edition. For details, see Format 1 (preferred): Account name
in your organization (in this topic).

### Non-VPS account locator formats by cloud platform and region¶

The following table lists the account locator formats across all the supported
non-VPS regions, including whether the account locator for a given region
requires additional segments:

If your account locator is `xy12345`:

Cloud Platform / Region | Account Identifier | Notes  
---|---|---  
**Amazon Web Services (AWS)** |  |   
US West (Oregon)  | `xy12345` | No additional segments required.  
US West (Commercial Gov - Oregon)  | `xy12345.us-west-2-gov.aws` |   
US Gov West 1 (FedRAMP High Plus)  | `xy12345.fhplus.us-gov-west-1.aws` | Additional `fhplus` segment required after the account locator.  
US Gov West 1 (DoD)  | `xy12345.dod.us-gov-west-1.aws` | Additional `dod` segment required after the account locator.  
US East (Ohio)  | `xy12345.us-east-2.aws` |   
US East (N. Virginia)  | `xy12345.us-east-1` | Cloud region ID is the only additional segment required.  
US East (Commercial Gov - N. Virginia)  | `xy12345.us-east-1-gov.aws` |   
US Gov East 1 (FedRAMP High Plus)  | `xy12345.fhplus.us-gov-east-1.aws` | Additional `fhplus` segment required after the account locator.  
Canada (Central)  | `xy12345.ca-central-1.aws` |   
South America (Sao Paulo)  | `xy12345.sa-east-1.aws` |   
EU (Ireland)  | `xy12345.eu-west-1` | Cloud region ID is the only additional segment required.  
Europe (London)  | `xy12345.eu-west-2.aws` |   
EU (Paris)  | `xy12345.eu-west-3.aws` |   
EU (Frankfurt)  | `xy12345.eu-central-1` | Cloud region ID is the only additional segment required.  
EU (Zurich)  | `xy12345.eu-central-2.aws` |   
EU (Stockholm)  | `xy12345.eu-north-1.aws` |   
Asia Pacific (Tokyo)  | `xy12345.ap-northeast-1.aws` |   
Asia Pacific (Osaka)  | `xy12345.ap-northeast-3.aws` |   
Asia Pacific (Seoul)  | `xy12345.ap-northeast-2.aws` |   
Asia Pacific (Mumbai)  | `xy12345.ap-south-1.aws` |   
Asia Pacific (Singapore)  | `xy12345.ap-southeast-1.aws` |   
Asia Pacific (Sydney)  | `xy12345.ap-southeast-2` | Cloud region ID is the only additional segment required.  
Asia Pacific (Jakarta)  | `xy12345.ap-southeast-3.aws` |   
China (Ningxia)  | `xy12345.cn-northwest-1.aws` | This region utilizes the `snowflakecomputing.cn` domain instead of the `snowflakecomputing.com` domain utilized by the other regions.  
**Google Cloud Platform (GCP)** |  |   
US Central1 (Iowa)  | `xy12345.us-central1.gcp` |   
US East4 (N. Virginia)  | `xy12345.us-east4.gcp` |   
Europe West2 (London)  | `xy12345.europe-west2.gcp` |   
Europe West3 (Frankfurt)  | `xy12345.europe-west3.gcp` |   
Europe West4 (Netherlands)  | `xy12345.europe-west4.gcp` |   
Middle East Central2 (Dammam)  | `xy12345.me-central2.gcp` |   
**Microsoft Azure** |  | Snowflake added hyphens to the Azure region IDs for consistency with AWS and GCP.  
West US 2 (Washington)  | `xy12345.west-us-2.azure` |   
Central US (Iowa)  | `xy12345.central-us.azure` |   
South Central US (Texas)  | `xy12345.south-central-us.azure` |   
East US 2 (Virginia)  | `xy12345.east-us-2.azure` |   
US Gov Virginia (FedRAMP High Plus)  | `xy12345.fhplus.us-gov-virginia.azure` |   
US Gov Virginia  | `xy12345.us-gov-virginia.azure` |   
Canada Central (Toronto)  | `xy12345.canada-central.azure` |   
UK South (London)  | `xy12345.uk-south.azure` |   
North Europe (Ireland)  | `xy12345.north-europe.azure` |   
West Europe (Netherlands)  | `xy12345.west-europe.azure` |   
Switzerland North (Zurich)  | `xy12345.switzerland-north.azure` |   
UAE North (Dubai)  | `xy12345.uae-north.azure` |   
Central India (Pune)  | `xy12345.central-india.azure` |   
Japan East (Tokyo)  | `xy12345.japan-east.azure` |   
Southeast Asia (Singapore)  | `xy12345.southeast-asia.azure` |   
Australia East (New South Wales)  | `xy12345.australia-east.azure` |   
  
## Account identifiers for private connectivity¶

If private connectivity to the Snowflake service is enabled for your account
and you wish to use the feature to connect to Snowflake, run the
[SYSTEM$GET_PRIVATELINK_CONFIG](../sql-
reference/functions/system_get_privatelink_config) function to determine the
private connectivity URL to use. You can use either the account name or
account locator in the URL to connect to the Snowflake web interface.

If you want to connect to Snowsight using private connectivity, use the
following instructions in the [Signing in to Snowsight](ui-snowsight-
gs.html#label-snowsight-getting-started-sign-in).

## Account identifiers for replication and failover¶

The preferred method of identifying an account in replication and failover
related SQL commands uses the organization name and account name as the
account identifier. If you decide to use the legacy account locator instead,
it may need to contain additional segments in order to uniquely identify the
account. See the table below for reference:

> Account Identifier | Location of the Remote Account  
> ---|---  
> `_organization_name_._account_name_` | Preferred account identifier that can be used regardless of the region or region group of the account that stores the primary database.  
> `_account_locator_` | Same region but a different account from the account that stores the primary database.  
> `_snowflake_region_._account_locator_` | Same region group but a different region from the account that stores the primary database.  
> `_region_group_._snowflake_region_._account_locator_` | Different region group from the account that stores the primary database.  
  
The values for `_snowflake_region_` and `_region_group_` can be found in the
output of [SHOW REPLICATION ACCOUNTS](../sql-reference/sql/show-replication-
accounts).

## Snowflake region IDs and region groups¶

A Snowflake Region is a distinct region (deployed within an AWS, Azure, or GCP
cloud region) that is isolated from other Snowflake Regions. A Snowflake
Region can be either multi-tenant (containing accounts for multiple
organizations) or single-tenant (aka Virtual Private Snowflake for a single
organization).

Each Snowflake Region has an unique identifier and belongs to a region group,
which enables global features such as data sharing and replication.

### Region IDs¶

Because each cloud platform utilizes different conventions and formats for
naming their regions, Snowflake assigns a canonical ID to each Snowflake
Region that uniquely identifies it across all the cloud platforms and their
regions.

If the Organizations feature is enabled, specifying the Snowflake Region ID as
part of an account identifier is required when you create a new account, as
well as when you configure replication and failover.

The following table displays the complete list of Snowflake Region IDs:

Cloud Region | Cloud Region ID | Snowflake Region ID | Notes  
---|---|---|---  
**Amazon Web Services (AWS)** |  |  |   
US West (Oregon)  | `us-west-2` | `aws_us_west_2` |   
US West (Commercial Gov - Oregon)  | `us-west-2` | `aws_us_gov_west_2` | Available only for accounts on Business Critical (or higher); located in US West 2, not [AWS GovCloud (US)](https://aws.amazon.com/govcloud-us/).  
US Gov West 1 (FedRAMP High Plus)  | `us-gov-west-1` | `aws_us_gov_west_1_fhplus` | Available only for accounts on Business Critical (or higher); located in [AWS GovCloud (US)](https://aws.amazon.com/govcloud-us/).  
US Gov West 1 (DoD)  | `us-gov-west-1` | `aws_us_gov_west_1_dod` | Available only for accounts on Business Critical (or higher); located in [AWS GovCloud (US)](https://aws.amazon.com/govcloud-us/).  
US East (Ohio)  | `us-east-2` | `aws_us_east_2` |   
US East (N. Virginia)  | `us-east-1` | `aws_us_east_1` |   
US East (Commercial Gov - N. Virginia)  | `us-east-1` | `aws_us_gov_east_1` | Available only for accounts on Business Critical (or higher); located in US East 1, not [AWS GovCloud (US)](https://aws.amazon.com/govcloud-us/).  
US Gov East 1 (FedRAMP High Plus)  | `us-gov-east-1` | `aws_us_gov_east_1_fhplus` | Available only for accounts on Business Critical (or higher); located in [AWS GovCloud (US)](https://aws.amazon.com/govcloud-us/).  
Canada (Central)  | `ca-central-1` | `aws_ca_central_1` |   
South America (Sao Paulo)  | `sa-east-1` | `aws_sa_east_1` |   
EU (Ireland)  | `eu-west-1` | `aws_eu_west_1` |   
Europe (London)  | `eu-west-2` | `aws_eu_west_2` |   
EU (Paris)  | `eu-west-3` | `aws_eu_west_3` |   
EU (Frankfurt)  | `eu-central-1` | `aws_eu_central_1` |   
EU (Zurich)  | `eu-central-2` | `aws_eu_central_2` |   
EU (Stockholm)  | `eu-north-1` | `aws_eu_north_1` |   
Asia Pacific (Tokyo)  | `ap-northeast-1` | `aws_ap_northeast_1` |   
Asia Pacific (Osaka)  | `ap-northeast-3` | `aws_ap_northeast_3` |   
Asia Pacific (Seoul)  | `ap-northeast-2` | `aws_ap_northeast_2` |   
Asia Pacific (Mumbai)  | `ap-south-1` | `aws_ap_south_1` |   
Asia Pacific (Singapore)  | `ap-southeast-1` | `aws_ap_southeast_1` |   
Asia Pacific (Sydney)  | `ap-southeast-2` | `aws_ap_southeast_2` |   
Asia Pacific (Jakarta)  | `ap-southeast-3` | `aws_ap_southeast_3` |   
China (Ningxia)  | `cn-northwest-1` | `aws_cn_northwest_1` | Utilizes a different domain name (`snowflakecomputing.cn`) and is operated by Digital China Cloud Technology Limited (DCC), an authorized operating partner of Snowflake.  
**Google Cloud Platform (GCP)** |  |  |   
US Central1 (Iowa)  | `us-central1` | `gcp_us_central1` |   
US East4 (N. Virginia)  | `us-east4` | `gcp_us_east4` |   
Europe West2 (London)  | `europe-west2` | `gcp_europe_west2` |   
Europe West3 (Frankfurt)  | `europe-west3` | `gcp_europe_west3` |   
Europe West4 (Netherlands)  | `europe-west4` | `gcp_europe_west4` |   
Middle East Central2 (Dammam)  | `me-central2` | `gcp_me_central2` |   
**Microsoft Azure** |  |  |   
West US 2 (Washington)  | `westus2` | `azure_westus2` |   
Central US (Iowa)  | `centralus` | `azure_centralus` |   
South Central US (Texas)  | `southcentralus` | `azure_southcentralus` |   
East US 2 (Virginia)  | `eastus2` | `azure_eastus2` |   
US Gov Virginia (FedRAMP High Plus)  | `usgovvirginia` | `azure_usgovvirginia_fhplus` | Available only for accounts on Business Critical (or higher); located in [Microsoft Azure Government](https://docs.microsoft.com/en-us/azure/azure-government/).  
US Gov Virginia  | `usgovvirginia` | `azure_usgovvirginia` | Available only for accounts on Business Critical (or higher); located in [Microsoft Azure Government](https://docs.microsoft.com/en-us/azure/azure-government/).  
Canada Central (Toronto)  | `canadacentral` | `azure_canadacentral` |   
UK South (London)  | `uk-south` | `azure_uksouth` |   
North Europe (Ireland)  | `northeurope` | `azure_northeurope` |   
West Europe (Netherlands)  | `westeurope` | `azure_westeurope` |   
Switzerland North (Zurich)  | `switzerlandnorth` | `azure_switzerlandnorth` |   
UAE North (Dubai)  | `uaenorth` | `azure_uaenorth` |   
Central India (Pune)  | `centralindia` | `azure_centralindia` |   
Japan East (Tokyo)  | `japaneast` | `azure_japaneast` |   
Southeast Asia (Singapore)  | `southeastasia` | `azure_southeastasia` |   
Australia East (New South Wales)  | `australiaeast` | `azure_australiaeast` |   
  
### Region groups¶

A region group is a group of Snowflake Regions that offer similar security
controls, isolation, and compliance. The region group to which a Snowflake
Region belongs differs depending on the region:

  * All Snowflake multi-tenant commercial regions (across all the supported cloud platforms) are in the same shared/general `PUBLIC` group.

  * Each Snowflake multi-tenant government region is in a separate group specific to the region.

  * Each single-tenant Virtual Private Snowflake (VPS) is in a separate region group specific to the VPS. If your organization has more than one VPS, you can have one VPS per region group or multiple VPSs can share the same region group.

Specifying the region group as part of an account identifier is required when
you want to create accounts in different region groups.

