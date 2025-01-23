# Snowflake Partner Connect¶

Partner Connect lets you easily create trial accounts with selected Snowflake
business partners and integrate these accounts with Snowflake. This feature
provides a convenient option for trying various 3rd-party tools and services,
and then adopting the ones that best meet your business needs.

## Supported Partners¶

Important

Snowflake neither determines nor dictates the conditions or terms (length,
supported features, etc.) for partner trial accounts; these policies are set
by each Snowflake partner and vary according to the partner.

For details about a specific trial, please contact the partner directly.

Currently, Partner Connect includes the following partners:

Partner | Category | Notes  
---|---|---  
[![Alation](../_images/logo-alation.png)](https://alation.com/) | [Security, Governance & Observability](ecosystem-security) |   
[![Alteryx](../_images/logo-alteryx.svg)](https://www.alteryx.com) | [Machine Learning & Data Science](ecosystem-analytics) |   
[![Alteryx](../_images/logo-alteryx.svg)](https://www.alteryx.com) | [Data Integration](ecosystem-etl) | Alteryx Designer Cloud  
[![ALTR](../_images/logo-altr.svg)](https://www.altr.com/) | [Security, Governance & Observability](ecosystem-security) | Free forever plan  
[![Ascend.io](../_images/logo-ascend.svg)](https://www.ascend.io/) | [Data Integration](ecosystem-etl) |   
[![CARTO](../_images/logo-carto.svg)](https://carto.com/) | [Business Intelligence (BI)](ecosystem-bi) |   
[![CData Software](../_images/logo-cdata.png)](https://www.cdata.com/) | [Data Integration](ecosystem-etl) |   
[![Census](../_images/logo-census.svg)](https://www.getcensus.com/) | [Data Integration](ecosystem-etl) |   
[![Coalesce](../_images/logo-coalesce.png)](https://coalesce.io/) | [Data Integration](ecosystem-etl) |   
[![DataRobot](../_images/logo-datarobot.svg)](https://www.datarobot.com/) | [Machine Learning & Data Science](ecosystem-analytics) |   
[![data.world](../_images/logo-dataworld.svg)](https://data.world/) | [Security, Governance & Observability](ecosystem-security) |   
[![Dataiku](../_images/logo-dataiku.svg)](https://www.dataiku.com/dss/editions/) | [Machine Learning & Data Science](ecosystem-analytics) |   
[![DataOps.live](../_images/logo-dataops.svg)](https://www.dataops.live/) | [SQL Development & Management](ecosystem-editors) |   
[![dbt Labs](../_images/logo-dbtlabs.png)](https://www.getdbt.com/) | [Data Integration](ecosystem-etl) | dbt Cloud  
[![Domo](../_images/logo-domo.svg)](https://www.domo.com/) | [Business Intelligence (BI)](ecosystem-bi) |   
[![Etleap](../_images/logo-etleap.svg)](https://etleap.com/) | [Data Integration](ecosystem-etl) |   
[![Fivetran](../_images/logo-fivetran.svg)](https://www.fivetran.com) | [Data Integration](ecosystem-etl) |   
[![H2O.ai](../_images/logo-h2o.svg)](https://www.h2o.ai/) | [Machine Learning & Data Science](ecosystem-analytics) |   
[![Hevo Data](../_images/logo-hevo.png)](https://hevodata.com/) | [Data Integration](ecosystem-etl) | Hevo Data CDC for ETL  
[![Hex](../_images/logo-hex.png)](https://hex.tech/) | [Machine Learning & Data Science](ecosystem-analytics) |   
[![Hightouch](../_images/logo-hightouch.png)](https://hightouch.com/) | [Data Integration](ecosystem-etl) |   
[![Hunters](../_images/logo-hunters.svg)](https://hunters.ai/) | [Security, Governance & Observability](ecosystem-security) |   
[![Informatica](../_images/logo-informatica.svg)](https://www.informatica.com) | [Data Integration](ecosystem-etl) | Informatica Cloud  
[![Informatica Data Loader](../_images/logo-informatica.svg)](https://marketplace.informatica.com/forms/data-loader.html) | [Data Integration](ecosystem-etl) | Informatica Data Loader  
[![Keboola](../_images/logo-keboola.png)](http://www.keboola.com/) | [Data Integration](ecosystem-etl) |   
[![Knoema](../_images/logo-knoema.svg)](https://knoema.com/) | [Data Integration](ecosystem-etl) |   
[![Matillion Data Productivity Cloud](../_images/logo-matillion.png)](https://www.matillion.com/products/data-loader/) | [Data Integration](ecosystem-etl) | Matillion Data Productivity Cloud  
[![Matillion ETL](../_images/logo-matillion.png)](https://www.matillion.com/products/etl-software/) | [Data Integration](ecosystem-etl) | Matillion ETL  
[![Nexla](../_images/logo-nexla.png)](https://www.nexla.com/) | [Data Integration](ecosystem-etl) |   
[![Qlik](../_images/logo-qlik.svg)](http://www.qlik.com/) | [Data Integration](ecosystem-etl) | Qlik Replicate  
[![Rivery](../_images/logo-rivery.svg)](https://rivery.io/) | [Data Integration](ecosystem-etl) |   
[![Sigma Computing](../_images/logo-sigma.png)](https://sigmacomputing.com/) | [Business Intelligence (BI)](ecosystem-bi) |   
[![Sisense](../_images/logo-sisense.png)](https://www.sisense.com/) | [Business Intelligence (BI)](ecosystem-bi) | Sisense for Cloud Data Teams  
[![SnapLogic](../_images/logo-snaplogic.svg)](https://www.snaplogic.com/) | [Data Integration](ecosystem-etl) |   
[![SqlDBM](../_images/logo-sqldbm.svg)](https://sqldbm.com/Home/) | [SQL Development & Management](ecosystem-editors) |   
[![Stitch](../_images/logo-stitch.svg)](https://www.stitchdata.com/) | [Data Integration](ecosystem-etl) |   
[![StreamSets](../_images/logo-streamsets.png)](https://streamsets.com/) | [Data Integration](ecosystem-etl) |   
[![Striim](../_images/logo-striim.svg)](https://www.striim.com/) | [Data Integration](ecosystem-etl) |   
[![Talend](../_images/logo-talend.svg)](https://www.talend.com) | [Data Integration](ecosystem-etl) |   
[![ThoughtSpot](../_images/logo-thoughtspot.svg)](https://www.thoughtspot.com/) | [Business Intelligence (BI)](ecosystem-bi) |   
  
## Security Requirements¶

Partner Connect is limited to account administrators (i.e. users with the
ACCOUNTADMIN role) who have a verified email address in Snowflake:

  * To use Partner Connect, you must switch to the ACCOUNTADMIN role or contact someone in your organization who has the role.

  * To verify your email address:

Snowsight:

    

In some cases, you automatically receive an email prompting you to Please
Validate Your Email. If you did not, follow these steps to verify your email
address:

    1. Sign in to Snowsight.

    2. Select your username, and then select Profile.

    3. Configure your email address:

       * If you do not have an email address listed, enter an email address in the Email field, and then select Save.

       * If you cannot enter an email address, an account administrator must either add an email address on your behalf or grant your user the role with the OWNERSHIP privilege on your user.

       * If you did not receive an email, select Resend verification email. Snowflake sends a verification email to the address listed.

    4. Open your email, and then select the link in the email to validate your email address.

Classic Console:

    
    1. Select the dropdown menu next to your login name » Preferences » General.

    2. In the User Information area, add or verify your email address by selecting the appropriate link(s) in the Email Address field.

## Connecting with a Snowflake Partner¶

To initiate a trial account with any Snowflake partner currently in Partner
Connect:

  1. Log into either [Snowsight](ui-snowsight) or the Classic Console.

  2. Make ACCOUNTADMIN the active role in the interface:

> Either Interface:
>  
>
> Click the dropdown menu next to your login name, then click Switch Role »
> ACCOUNTADMIN to change to the account administrator role.

  3. Open the Partner Connect page:

> Snowsight:
>  
>
> Select Data Products » Partner Connect.
>
> Classic Console:
>  
>
> Select Partner Connect [![Partner Connect tab](../_images/ui-navigation-
> partner-icon.svg)](../_images/ui-navigation-partner-icon.svg). The Snowflake
> Partner Connect page opens.

  4. Click on the corresponding tile for the partner to which you wish to connect.

A dialog displays the requirements for connecting to the partner, as well as a
list of the objects automatically created in Snowflake during the connection
process, including an empty database, warehouse, default user, and custom
role. The partner application uses these objects when reading from or writing
to your account.

  5. Optionally specify one or more existing databases in Snowflake to automatically use with the trial. This creates an additional custom role that makes existing data in Snowflake quickly and easily available to the partner application.

If you do not specify any databases during the initial connection process, you
can specify them later; however, specifying them later is a manual task.

Attention

Currently, you cannot use the Classic Console to specify shared databases
(i.e. databases shared from provider accounts to your account) for your
Partner Connect trial during the initial connection process. If you select a
shared database, the Classic Console returns an error when you click the
Connect button to complete the process.

To use shared databases with a trial:

     * Use [Snowsight](ui-snowsight) to complete the initial connection process.

     * Manually specify the shared database after the process completes.

  6. Click the Connect button below the partner description to initiate creating a trial account with the partner and connecting the partner application to Snowflake.

When the process is complete and the objects have been created, the partner
tile is updated with a checkmark.

### Objects Created for the Partner¶

During the connection process, the following Snowflake objects for the partner
application are created in your account:

Object Name | Type | Notes  
---|---|---  
PC_<_partner_ >_DB | Database | This database is empty and can be used to load/store data for querying. If you wish to use existing databases that already contain data, during the initial connection process, you can specify any non-shared databases to use in the field provided. You can also manually specify other databases after the process completes.  
PC_<_partner_ >_WH | Warehouse | The default size of the warehouse is X-Small, but can be changed if needed.  
PC_<_partner_ >_USER | System User | This is the user that connects to Snowflake from the partner application. As noted in the dialog, a random password for the user is automatically generated.  
PC_<_partner_ >_ROLE | Role | The PUBLIC role is granted to this custom role, which enables the role to access any objects owned/granted to the PUBLIC role. In addition, this role is granted to the SYSADMIN role, which enables users with the SYSADMIN role (or higher) to also access any Snowflake objects created for partner access.  
  
In addition, if you optionally chose to specify one or more existing databases
during the initial connection process, a second custom role is created with
all of the necessary privileges to access the tables in the databases:

PC_<_partner_ >_DB_PICKER_ROLE

  

This role is then granted to the PC_<_partner_ >_ROLE, which enables all the
tables in the specified databases to be used by the partner application with
minimal (or no) additional configuration.

Note that this second role is not displayed in the dialog, but the role is
created automatically after all the other objects listed in the dialog are
created.

Tip

The above objects are created to enable a quick, convenient setup:

  * If you prefer to use existing Snowflake objects (databases, warehouses, users, etc.), you can update the preferences in the partner application to reference the desired objects in Snowflake.

  * An account administrator can use [ALTER USER](../sql-reference/sql/alter-user) to change the generated password for PC_<_partner_ >_USER.

  * To enable access to objects owned by (or granted to) roles other than PUBLIC, grant the other roles to PC_<_partner_ >_ROLE.

### Automated Application Features and Resource Usage¶

Partner applications may include automated features such as dashboards that
run on a schedule and consume compute resources. We encourage you to read the
product documentation for a partner application and to [monitor
usage](warehouses-load-monitoring) of the PC_<_partner_ >_WH warehouse to
avoid unexpected Snowflake credit usage by the application.

## Adding Partner IP Addresses to Network Policies¶

If you use a [network policy](network-policies) to restrict access to your
Snowflake account based on user IP address, partner applications will not be
able to access your account unless you add the partner’s IP addresses to the
list of allowed IP addresses in the network policy. For detailed instructions,
see [Modify a network policy](network-policies.html#label-modifying-network-
policies).

The following table lists the IP addresses to add for each partner (if
available and supported) or provides links to pages on the partner sites for
this information:

Partner | IP Addresses | Notes  
---|---|---  
Alation | N/A |   
Alteryx | `44.225.50.233` |   
ALTR | `3.145.219.176/28` . `35.89.45.128/28` . `44.203.133.160/28` |   
Ascend.io | N/A |   
CARTO | N/A |   
CData Software | TBD |   
Census | N/A |   
Coalesce | N/A |   
data.world | `52.3.83.134` . `52.205.195.10` . `52.205.207.86` |   
Dataiku | N/A |   
DataOps.live | N/A |   
DataRobot | TBD |   
dbt Labs | `52.22.161.231` . `52.45.144.63` . `54.81.134.249` |   
Domo | N/A |   
Etleap | N/A |   
Fivetran | `52.0.2.4` | For more setup details, see the [Fivetran Documentation](https://fivetran.com/docs/warehouses/snowflake).  
H2O.ai | N/A |   
Hunters | `18.192.165.147` . `34.223.20.125` . `34.223.186.164` . `34.223.221.217` . `52.32.222.121` . `52.35.55.27` . `52.35.219.75` . `52.40.78.172` . `54.68.155.124` . `54.72.125.231` . `54.73.199.243` . `54.75.50.99` . `54.212.81.93` . `54.214.94.117` . `54.220.191.11` |   
Hevo Data CDC for ETL | TBD |   
Hex | N/A |   
Hightouch | N/A |   
Informatica | N/A |   
Informatica Data Loader | N/A |   
Keboola | N/A |   
Knoema | N/A |   
Matillion Data Productivity Cloud | N/A |   
Matillion ETL | N/A |   
Nexla | `34.231.167.112` . `54.209.27.1` |   
Qlik | N/A |   
Rivery | `13.58.140.165/32` . `34.254.56.182/32` . `52.14.86.20/32` . `52.14.192.86/32` |   
Sigma | `104.197.169.18` . `104.197.193.23` |   
Sisense | Various | For the IP addresses, see the [Sisense Documentation](https://dtdocs.sisense.com/article/connecting-to-periscope-menu).  
SnapLogic | Various | For the IP addresses, see the [SnapLogic Documentation](https://docs-snaplogic.atlassian.net/wiki/spaces/SD/pages/1439269/Network+Setup#NetworkSetup-IPAddressWhitelisting).  
SqlDBM | N/A |   
Stitch | Various | For the IP addresses, see the [Stitch Documentation](https://www.stitchdata.com/docs/destinations/snowflake/connecting-a-snowflake-data-warehouse-to-stitch#setup-requirements).  
StreamSets | N/A |   
Striim | N/A |   
Talend | N/A |   
ThoughtSpot | `35.164.213.211` |   
  
## Launching a Partner Application¶

After a partner application is connected to Snowflake:

  1. On the Snowflake Partner Connect page, click the corresponding tile.

  2. Click the Launch button to open the partner web site.

## Disconnecting from a Partner Account¶

If you decide to discontinue a trial account initiated through Partner Connect
for any reason, complete the following steps:

  1. Log into either [Snowsight](ui-snowsight) or the Classic Console.

  2. Make ACCOUNTADMIN the active role in the interface.

> Either Interface:
>  
>
> Click the dropdown menu next to your login name, then click Switch Role »
> ACCOUNTADMIN to change to the account administrator role.

  3. Open the Partner Connect page:

> Snowsight:
>  
>
> Select Data Products » Partner Connect.
>
> Classic Console:
>  
>
> Click on Partner Connect [![Partner Connect tab](../_images/ui-navigation-
> partner-icon.svg)](../_images/ui-navigation-partner-icon.svg). The Snowflake
> Partner Connect page opens.

  4. Click the tile for the partner application you are disconnecting from. In the dialog that opens, note the names of the database, warehouse, system user, and custom role objects that were created for the partner application during the initial connection process.

  5. Use the appropriate [DROP <object>](../sql-reference/sql/drop) command to remove each of the objects created for the partner application.

Tip

During the initial connection process, if you specified existing databases to
use with the partner application, remember to also drop the PC_<_partner_
>_DB_PICKER_ROLE role that was automatically created along with the other
objects.

  6. Contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) to clear the partner connection and remove the checkmark from the partner tile in Partner Connect.

  7. If the trial does not expire on its own, contact the partner to end your participation in the trial.

## Troubleshooting a Connection¶

### Connection Already Exists¶

If your organization already has an account with the partner, initiated either
with the partner directly or using Partner Connect on another one of your
Snowflake accounts, initiating another trial account might fail with a message
that a connection already exists.

In this case, the trial for this account must be initiated directly through
the partner.

