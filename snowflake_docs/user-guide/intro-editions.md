# Snowflake Editions¶

Snowflake offers multiple editions to choose from, ensuring that your usage
fits your organization’s specific requirements. Each successive edition builds
on the previous edition through the addition of edition-specific features
and/or higher levels of service. As your organization’s needs change and grow,
changing editions is easy.

For information about working with editions, including viewing and changing an
account’s edition, see [Working with account editions](organizations-manage-
accounts-editions).

Note

The Snowflake Edition that your organization chooses determines the unit costs
for the credits and the data storage you use. Other factors that impact unit
costs are the [region](intro-regions) where your Snowflake account is located
and whether it is an _On Demand_ or _Capacity_ account:

  * On Demand: Usage-based pricing with no long-term licensing requirements.

  * Capacity: Discounted pricing based on an upfront Capacity commitment.

For pricing details, see the [pricing page](http://www.snowflake.com/pricing)
(on the Snowflake website).

## Overview of Editions¶

### Standard Edition¶

Standard Edition is our introductory level offering, providing full, unlimited
access to all of Snowflake’s standard features. It provides a strong balance
between features, level of support, and cost.

### Enterprise Edition¶

Enterprise Edition provides all the features and services of Standard Edition,
with additional features designed specifically for the needs of large-scale
enterprises and organizations.

### Business Critical Edition¶

Business Critical Edition, formerly known as Enterprise for Sensitive Data
(ESD), offers even higher levels of data protection to support the needs of
organizations with extremely sensitive data, particularly PHI data that must
comply with HIPAA and [HITRUST CSF](intro-cloud-platforms.html#label-hitrust-
csf-cert) regulations.

It includes all the features and services of Enterprise Edition, with the
addition of enhanced security and data protection. In addition, database
failover/failback adds support for business continuity and disaster recovery.

Note

As required by HIPAA and [HITRUST CSF](intro-cloud-platforms.html#label-
hitrust-csf-cert) regulations, before any PHI data can be stored in Snowflake,
a signed business associate agreement (BAA) must be in place between your
agency/organization and Snowflake Inc.

### Virtual Private Snowflake (VPS)¶

Virtual Private Snowflake offers our highest level of security for
organizations that have the strictest requirements, such as financial
institutions and any other large enterprises that collect, analyze, and share
highly sensitive data.

It includes all the features and services of Business Critical Edition, but in
a completely separate Snowflake environment, isolated from all other Snowflake
accounts (i.e. VPS accounts do not share any type of hardware resources with
accounts outside the VPS).

Note

To access your account, you can use an [account identifier](admin-account-
identifier) that specifies your organization name and account name.

If you instead choose to use an [account locator](admin-account-
identifier.html#label-account-locator) as the account identifier, note that
the account locator for VPS accounts uses a different format than the accounts
for other Snowflake Editions. For details, see [Finding the account locator
format for a VPS account](admin-account-identifier.html#label-account-
identifier-for-vps).

## Feature / Edition Matrix¶

The following tables provide a list of the major features and services
included with each edition.

Note

This is only a partial list of the features. For a more complete and detailed
list, see [Overview of Key Features](intro-supported-features).

### Release Management¶

Feature/Service | Standard | Enterprise | Business Critical | VPS  
---|---|---|---|---  
24-hour [early access to weekly new releases](intro-releases), which can be used for additional testing or validation before each release is deployed to your production accounts. |  | ✔ | ✔ | ✔  
  
### Security, Governance, and Data Protection¶

Feature/Service | Standard | Enterprise | Business Critical | VPS  
---|---|---|---|---  
SOC 2 Type II certification.  | ✔ | ✔ | ✔ | ✔  
[Federated authentication and SSO](admin-security-fed-auth-overview) for centralizing and streamlining user authentication.  | ✔ | ✔ | ✔ | ✔  
[OAuth](oauth-intro) for authorizing account access without sharing or storing user login credentials.  | ✔ | ✔ | ✔ | ✔  
[Network policies](network-policies) for limiting/controlling site access by user IP address.  | ✔ | ✔ | ✔ | ✔  
Automatic [encryption of all data](../guides-overview-secure).  | ✔ | ✔ | ✔ | ✔  
Support for [multi-factor authentication](security-mfa).  | ✔ | ✔ | ✔ | ✔  
Object-level [access control](security-access-control-overview).  | ✔ | ✔ | ✔ | ✔  
Standard [Time Travel](data-time-travel) (up to 1 day) for accessing/restoring modified and deleted data.  | ✔ | ✔ | ✔ | ✔  
Disaster recovery of modified/deleted data (for 7 days beyond Time Travel) through [Fail-safe](data-failsafe).  | ✔ | ✔ | ✔ | ✔  
[Generating synthetic data](synthetic-data) |  | ✔ | ✔ | ✔  
[Extended Time Travel](data-time-travel.html#label-data-retention-specifying) (up to 90 days).  |  | ✔ | ✔ | ✔  
[Periodic rekeying of encrypted data](security-encryption-manage.html#label-periodic-rekeying) for increased protection.  |  | ✔ | ✔ | ✔  
[Column-level Security](security-column-intro) to apply masking policies to columns in tables or views.  |  | ✔ | ✔ | ✔  
[Row-level Security](security-row-intro) to apply row access policies to determine which rows are visible in a query result.  |  | ✔ | ✔ | ✔  
[Aggregation policies](aggregation-policies) that enforce privacy by requiring queries to aggregate data to return results.  |  | ✔ | ✔ | ✔  
[Projection policies](projection-policies) that restrict who can use a SELECT statement to project a column.  |  | ✔ | ✔ | ✔  
[Differential privacy](diff-privacy/differential-privacy-overview) to protect data against targeted privacy attacks.  |  | ✔ | ✔ | ✔  
[Object Tagging](object-tagging) to apply tags to Snowflake objects to facilitate tracking sensitive data and resource usage.  |  | ✔ | ✔ | ✔  
Support for classifying potentially sensitive data using [classification](classify-intro).  |  | ✔ | ✔ | ✔  
Audit the user access history through the Account Usage [ACCESS_HISTORY](../sql-reference/account-usage/access_history) view.  |  | ✔ | ✔ | ✔  
Customer-managed encryption keys through [Tri-Secret Secure](security-encryption-manage.html#label-customer-managed-keys).  |  |  | ✔ | ✔  
Support for private connectivity to the Snowflake service using AWS PrivateLink, Azure Private Link, or Google Cloud Private Service Connect.  |  |  | ✔ | ✔  
Support for private connectivity to Snowflake internal stages using AWS PrivateLink and Azure Private Link.  |  |  | ✔ | ✔  
Support for PHI data (in accordance with HIPAA and [HITRUST CSF](intro-cloud-platforms.html#label-hitrust-csf-cert) regulations).  |  |  | ✔ | ✔  
Support for PCI DSS.  |  |  | ✔ | ✔  
Support for public sector workloads that meet U.S. Federal and state government requirements, such as [FedRAMP and ITAR](intro-regions.html#label-us-gov-regions).  |  |  | ✔ | ✔  
Support for IRAP - Protected (P) data (in specified [Asia Pacific regions](intro-regions.html#label-asia-pacific-regions)).  |  |  | ✔ | ✔  
Dedicated metadata store and pool of compute resources (used in virtual warehouses).  |  |  |  | ✔  
[Data Quality and data metric functions](data-quality-intro) to monitor the state and integrity of data.  |  | ✔ | ✔ | ✔  
  
### Compute Resource Management¶

Feature/Service | Standard | Enterprise | Business Critical | VPS  
---|---|---|---|---  
[Virtual warehouses](warehouses), separate compute clusters for isolating query and data loading workloads. | ✔ | ✔ | ✔ | ✔  
[Resource monitors](resource-monitors) for monitoring virtual warehouse credit usage. | ✔ | ✔ | ✔ | ✔  
[Multi-cluster virtual warehouses](warehouses-multicluster) for scaling compute resources to meet concurrency needs. |  | ✔ | ✔ | ✔  
  
### SQL Support¶

Feature/Service | Standard | Enterprise | Business Critical | VPS  
---|---|---|---|---  
[Standard SQL](../sql-reference-commands), including most DDL and DML defined in SQL:1999. | ✔ | ✔ | ✔ | ✔  
[Advanced DML](../sql-reference/sql-dml) such as multi-table INSERT, MERGE, and multi-merge. | ✔ | ✔ | ✔ | ✔  
Broad support for standard [data types](../sql-reference-data-types). | ✔ | ✔ | ✔ | ✔  
Native support for [semi-structured data](semistructured-intro) (JSON, Avro, ORC, Parquet, and XML). | ✔ | ✔ | ✔ | ✔  
Native support for [geospatial data](../sql-reference/data-types-geospatial). | ✔ | ✔ | ✔ | ✔  
Native support for [unstructured data](unstructured-intro). | ✔ | ✔ | ✔ | ✔  
[Collation rules](../sql-reference/collation) for string/text data in table columns. | ✔ | ✔ | ✔ | ✔  
[Integrity constraints](../sql-reference/constraints) (not enforced) on table columns for informational and modeling purposes. | ✔ | ✔ | ✔ | ✔  
Multi-statement [transactions](../sql-reference/transactions). | ✔ | ✔ | ✔ | ✔  
[User-defined functions (UDFs)](../developer-guide/udf/udf-overview) with support for Java, JavaScript, Python, and SQL. | ✔ | ✔ | ✔ | ✔  
[External functions](../sql-reference/external-functions) for extending Snowflake to other development platforms. | ✔ | ✔ | ✔ | ✔  
[Amazon API Gateway private endpoints for external functions](../sql-reference/external-functions-creating-aws-planning.html#label-external-functions-aws-endpoint-type). |  |  | ✔ | ✔  
[Stored procedures](../developer-guide/stored-procedure/stored-procedures-overview) with support for Java, JavaScript, Python, Scala, and SQL (Snowflake Scripting). | ✔ | ✔ | ✔ | ✔  
[Dynamic tables](dynamic-tables-intro) for automatically materializing the results of a specified SQL query and keeping them up to date to meet your data freshness target. | ✔ | ✔ | ✔ | ✔  
[External tables](tables-external) for referencing data in a cloud storage data lake. | ✔ | ✔ | ✔ | ✔  
[Hybrid tables](tables-hybrid) for data in transactional and analytical workloads. | ✔ | ✔ | ✔ | ✔  
Support for [clustering data](tables-clustering-keys) in very large tables to improve query performance, with automatic maintenance of clustering. | ✔ | ✔ | ✔ | ✔  
[Query acceleration](query-acceleration-service) for parallel processing portions of eligible queries. |  | ✔ | ✔ | ✔  
[Search optimization](search-optimization-service) for point lookup queries, with automatic maintenance. |  | ✔ | ✔ | ✔  
[Materialized views](views-materialized), with automatic maintenance of results. |  | ✔ | ✔ | ✔  
[Iceberg tables](tables-iceberg) for referencing data in a cloud storage data lake. | ✔ | ✔ | ✔ | ✔  
[Schema detection](data-load-overview.html#label-detect-column-definitions-in-semi-structured-data-files) for automatically detecting the schema in a set of staged semi-structured data files and retrieving the column definitions. | ✔ | ✔ | ✔ | ✔  
[Schema evolution](data-load-schema-evolution) for automatically evolving tables to support the structure of new data received from the data sources. | ✔ | ✔ | ✔ | ✔  
  
### Interfaces and Tools¶

Feature/Service | Standard | Enterprise | Business Critical | VPS  
---|---|---|---|---  
[Snowsight](ui-snowsight), the next-generation SQL worksheet for advanced query development, data analysis, and visualization. | ✔ | ✔ | ✔ | ✔  
[SnowSQL](snowsql), a command line client for building/testing queries, loading/unloading bulk data, and automating DDL operations. | ✔ | ✔ | ✔ | ✔  
[SnowCD](snowcd), a command line diagnostic tool for identifying and fixing client connectivity issues. | ✔ | ✔ | ✔ | ✔  
Programmatic interfaces for [Python](../developer-guide/python-connector/python-connector), [Spark](spark-connector), [Node.js](../developer-guide/node-js/nodejs-driver), [.NET.js](../developer-guide/dotnet/dotnet-driver), [PHP](../developer-guide/php-pdo/php-pdo-driver), and [Go](../developer-guide/golang/go-driver). | ✔ | ✔ | ✔ | ✔  
Native support for [JDBC](../developer-guide/jdbc/jdbc) and [ODBC](../developer-guide/odbc/odbc). | ✔ | ✔ | ✔ | ✔  
[Snowflake SQL API](../developer-guide/sql-api/index), a REST API for accessing and updating data in a Snowflake database. | ✔ | ✔ | ✔ | ✔  
Extensive [ecosystem](ecosystem) for connecting to ETL, BI, and other third-party vendors and technologies. | ✔ | ✔ | ✔ | ✔  
[Snowflake Partner Connect](ecosystem-partner-connect) for initiating free software/service trials with a growing network of partners in the Snowflake ecosystem. | ✔ | ✔ | ✔ | ✔  
[Snowpark](../developer-guide/snowpark/index), the set of libraries and runtimes that securely deploy and process non-SQL code, including Python, Java, and Scala. | ✔ | ✔ | ✔ | ✔  
[Streamlit in Snowflake](../developer-guide/streamlit/about-streamlit) for building, deploying, and sharing Streamlit apps on Snowflake data cloud. | ✔ | ✔ | ✔ | ✔  
  
### Data Import and Export¶

Feature/Service | Standard | Enterprise | Business Critical | VPS  
---|---|---|---|---  
[Bulk loading](../guides-overview-loading-data) from delimited flat files (CSV, TSV, etc.) and semi-structured data files (JSON, Avro, ORC, Parquet, and XML). | ✔ | ✔ | ✔ | ✔  
[Bulk unloading](data-unload-overview) to delimited flat files and JSON files. | ✔ | ✔ | ✔ | ✔  
[Snowpipe](data-load-snowpipe-intro) for continuous micro-batch loading. | ✔ | ✔ | ✔ | ✔  
[Snowpipe Streaming](data-load-snowpipe-streaming-overview) for low-latency loading of streaming data. | ✔ | ✔ | ✔ | ✔  
[Snowflake Connector for Kafka](kafka-connector) for loading data from Apache Kafka topics. | ✔ | ✔ | ✔ | ✔  
  
### Data Pipelines¶

Feature/Service | Standard | Enterprise | Business Critical | VPS  
---|---|---|---|---  
[Streams](streams-intro) for tracking table changes. | ✔ | ✔ | ✔ | ✔  
[Tasks](tasks-intro) for scheduling the execution of SQL statements, often in conjunction with table streams. | ✔ | ✔ | ✔ | ✔  
  
### Data Replication and Failover¶

Feature/Service | Standard | Enterprise | Business Critical | VPS  
---|---|---|---|---  
[Database and share replication](account-replication-intro) between Snowflake accounts (within an organization) to synchronize databases, shared objects, and stored data. | ✔ | ✔ | ✔ | ✔  
[Failover and failback](account-replication-failover-failback) between Snowflake accounts for business continuity and disaster recovery. |  |  | ✔ | ✔  
[Redirecting client connections](client-redirect) between Snowflake accounts for business continuity and disaster recovery. |  |  | ✔ | ✔  
  
### Data Sharing¶

Feature/Service | Standard | Enterprise | Business Critical | VPS  
---|---|---|---|---  
Snowflake Marketplace | ✔ | ✔ | ✔ |   
Universal Search | ✔ | ✔ | ✔ | ✔  
Build data products, monetize listings, and analyze your successes in Snowflake Marketplace. | ✔ | ✔ | ✔ |   
Public Listings | ✔ | ✔ | ✔ |   
Private Listings | ✔ | ✔ | ✔ | ✔  
With VPS, collaborate privately while strictly upholding requirements for security and isolation. |  |  |  | ✔  
Make data accessible without moving it using cross-cloud auto-fulfillment powered by Snowgrid™. | ✔ | ✔ | ✔ | ✔  
Collaborate with [Snowflake Data Clean Rooms](cleanrooms/introduction). | ✔ | ✔ | ✔ |   
Create and manage your own Snowflake Data Clean Rooms. |  | ✔ | ✔ | ✔  
Collaborate using one of Snowflake’s many collaborative technologies. | ✔ | ✔ | ✔ | ✔  
Replicate shared data to keep it synchronized within your organization. | ✔ | ✔ | ✔ | ✔  
  
### Artificial Intelligence and Machine Learning¶

Feature/Service | Standard | Enterprise | Business Critical | VPS  
---|---|---|---|---  
Use [Snowflake Cortex LLM functions](snowflake-cortex/llm-functions) to respond to plain-language prompts, answer questions, summarize or translate text, find similar documents, and more. | ✔ | ✔ | ✔ | ✔  
Use [Snowflake Copilot](snowflake-copilot) to engage in conversations about your structured data. | ✔ | ✔ | ✔ | ✔  
Use [Cortex Analyst](snowflake-cortex/cortex-analyst) to help write applications that can engage in conversations about your structured data. | ✔ | ✔ | ✔ | ✔  
Use [Cortex Fine-tuning](snowflake-cortex/cortex-finetuning) to create large language models specialized for your needs without the usual training costs. | ✔ | ✔ | ✔ | ✔  
Use [Cortex Search](snowflake-cortex/cortex-search/cortex-search-overview) to enable high-quality semantic search over your Snowflake data. | ✔ | ✔ | ✔ | ✔  
Use [Document AI](snowflake-cortex/document-ai/overview) to extract data from PDFs and other documents and to create pipelines for processing documents of a specific type. | ✔ | ✔ | ✔ | ✔  
Use [ML Functions](../guides-overview-ml-functions) to analyze your data using our machine-learning models trained on your data. | ✔ | ✔ | ✔ | ✔  
Use the [Snowflake Model Registry](../developer-guide/snowflake-ml/model-registry/overview) as a central repository for machine learning models within your organization. | ✔ | ✔ | ✔ | ✔  
Use the [Snowflake Feature Store](../developer-guide/snowflake-ml/feature-store/overview) to create a repository of data transformations that can be used to train machine learning models. |  | ✔ | ✔ | ✔  
  
### Customer Support¶

Feature/Service | Standard | Enterprise | Business Critical | VPS  
---|---|---|---|---  
[Snowflake Community](https://community.snowflake.com), Snowflake’s online Knowledge Base and support portal (for logging and tracking Snowflake Support tickets). | ✔ | ✔ | ✔ | ✔  
[Premier support](https://www.snowflake.com/wp-content/uploads/2019/02/Snowflake-Support-Policy-02202019.pdf), which includes 24/7 coverage and 1-hour response window for Severity 1 issues. | ✔ [1] | ✔ | ✔ | ✔  
  
[1] Applies only to Standard accounts provisioned after May 1, 2020; Standard
accounts provisioned before May 1 will continue to receive Standard support
(as defined in ‘Support Policy and Service Level Agreement’) until the account
is transitioned to Premier support.

