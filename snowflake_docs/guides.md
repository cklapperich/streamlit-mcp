# User Guides

Instructions on performing various Snowflake operations

## Connecting to Snowflake

Snowflake provides a variety of mechanisms for connecting to Snowflake and
executing database commands. Choose between the web interface or the command
line tool to connect to your Snowflake account. Learn how to use connectors to
integrate third-party data into Snowflake.

[See all](/en/guides-overview-connecting)

Web Interface

Snowsight distills Snowflake’s powerful SQL support into a unified, easy-to-
use experience. Use Snowsight to perform your critical Snowflake operations.

[Learn more](/en/user-guide/ui-snowsight)

Command Line

Detailed instructions for installing, configuring, and using the Snowflake
command-line client, snowsql.

[Learn more](/en/user-guide/snowsql)

Connectors

The Snowflake Connectors provide native integration of third-party
applications and database systems in Snowflake. The connectors provide instant
access to current data without the need to manually integrate against API
endpoints.

[Learn more](https://other-docs.snowflake.com/en/connectors)

## Snowflake Fundamentals

Learn the basics of warehouses, tables, and views in Snowflake.

## Snowflake Warehouses

Learn how to set up and use virtual data warehouses to process the SQL
statements that you execute.

[Overview of Warehouses](/en/user-guide/warehouses-overview)

[Multi-cluster Warehouses](/en/user-guide/warehouses-multicluster)

[Warehouse Considerations](/en/user-guide/warehouses-considerations)

[Working with Warehouses](/en/user-guide/warehouses-tasks)

[Using the Query Acceleration Service](/en/user-guide/query-acceleration-
service)

[See all](/en/user-guide/warehouses)

## Basics of Snowflake Tables and Views

Learn how to design and create tables and views for your data.

[Understanding Snowflake Table Structures](/en/user-guide/tables-micro-
partitions)

[Table Design Considerations](/en/user-guide/table-considerations)

[Overview of Views](/en/user-guide/views-introduction)

[Working with Secure Views](/en/user-guide/views-secure)

[Cloning Considerations](/en/user-guide/object-clone)

[Table Storage Considerations](/en/user-guide/tables-storage-considerations)

[See all](/en/guides-overview-db)

## Basics of Data Types

Learn about Snowflake data types and their uses

[Introduction to Snowflake Data Types](/en/sql-reference/intro-summary-data-
types)

[Numeric Data Types](/en/sql-reference/data-types-numeric)

[String and Binary Data Types](/en/sql-reference/data-types-text)

[Logical Data Types](/en/sql-reference/data-types-logical)

[Date & Time Data Types](/en/sql-reference/data-types-datetime)

[Geospatial Data Types](/en/sql-reference/data-types-geospatial)

[See all](/en/sql-reference-data-types)

## Getting data in to Snowflake

Snowflake provides several different methods to load data in to Snowflake,
such as by using Snowpipe, loading from cloud storage, or uploading files
using Snowsight.

[![](/images/guides/GettingDataIntoSnowflake1Light.svg)Understanding Data
LoadingData can be loaded into Snowflake in a number of ways. Learn about data
loading concepts, different tasks, tools, and techniques to quickly and easily
load data into Snowflake.](/en/guides-overview-loading-data)

[![](/images/guides/GettingDataIntoSnowflake2Light.svg)Bulk Data LoadingLearn
to use the COPY command to load data on-demand directly from an AWS S3 bucket,
Google Cloud Share, or a Microsoft Azure storage container into
Snowflake.](/en/user-guide/data-load-local-file-system)

[![](/images/guides/GettingDataIntoSnowflake3Light.svg)SnowpipeUse Snowflake
Snowpipe to load data automatically as it arrives.](/en/user-guide/data-load-
snowpipe-intro)

## Working with data

Queries and other standard database features are just the beginning when you
work with your data in Snowflake. You also use machine learning functions to
analyze data in Snowflake.

[See all](/en/guides-overview-db)

Queries

Snowflake supports standard SQL, including a subset of ANSI SQL:1999 and the
SQL:2003 analytic extensions. Learn how to use queries to interact with
Snowflake using simple queries, joins, and more.

[Learn more](/en/guides-overview-queries)

Views, Materialized Views, & Dynamic Tables

Views are just the beginning of how you can examine data. Snowflake provides a
number of mechanism for joining data including Materialized Views and Dynamic
Tables.

[Learn more](/en/user-guide/overview-view-mview-dts)

Streams and Tasks

Streams and tasks make executing complex task based solutions simple and easy.
Streams allow you to track changes to database objects and tasks provide a
mechanism to then execute SQL when those events occur.

[Learn more](/en/user-guide/streams-intro)

ML Functions

ML Functions are Snowflake’s intelligent, fully-managed service that enables
organizations to quickly analyze data within Snowflake.

[Learn more](/en/guides-overview-ai-features)

## Collaborating

Share data and applications with other Snowflake users. Discover and publish
listings of data products on the Snowflake Marketplace, share data products
privately, or use a direct share to quickly share data with someone in the
same region.

[What are listings?With listings, you can provide data and other information
to other Snowflake users, and you can access data and other information shared
by Snowflake providers.](https://other-
docs.snowflake.com/en/collaboration/collaboration-listings-about)

[Becoming a listing providerBecoming a provider of listings in Snowflake makes
it easier to manage sharing from your account to other Snowflake
accounts.](https://other-docs.snowflake.com/en/collaboration/provider-
becoming)

[Becoming a listing consumerGet access to data products shared privately or on
the Snowflake Marketplace by becoming a consumer of listings.](https://other-
docs.snowflake.com/en/collaboration/consumer-becoming)

## More Guides

## Alerts and Notifications

[Setting Up Alerts Based on Data in Snowflake](/en/user-guide/alerts)

[Sending Email Notifications](/en/user-guide/email-stored-procedures)

[See all](/en/guides-overview-alerts)

## Security

[Authentication](/en/user-guide/admin-security-fed-auth-overview)

[Access Control](/en/user-guide/security-access-control-overview)

[Encryption key management](/en/user-guide/security-encryption-manage)

[Encryption](/en/user-guide/security-encryption-end-to-end)

[Networking](/en/user-guide/network-policies)

[See all](/en/guides-overview-secure)

## Governance and Compliance

[Data Lineage and Dependencies](/en/user-guide/access-history)

[Data Access Policies](/en/user-guide/security-column-intro)

[Data Sensitivity](/en/user-guide/object-tagging)

[Classification](/en/user-guide/governance-classify-concepts)

[Compliance](/en/user-guide/intro-compliance)

[See all](/en/guides-overview-govern)

## Privacy

[Aggregation Policies](/en/user-guide/aggregation-policies)

[Projection Policies](/en/user-guide/projection-policies)

[See all](/en/guides-overview-privacy)

## Organizations and Accounts

[Organizations](/en/user-guide/organizations)

[Account identifiers](/en/user-guide/admin-account-identifier)

[See all](/en/guides-overview-manage)

## Business Continuity & Data Recovery

[Replication & Failover](/en/user-guide/account-replication-intro)

[Client Redirect](/en/user-guide/client-redirect)

[Time Travel](/en/user-guide/data-time-travel)

[Fail-safe](/en/user-guide/data-failsafe)

[See all](/en/user-guide/replication-intro)

## Performance and Cost

[Cost Management](/en/guides-overview-cost)

[Query Performance](/en/guides-overview-performance)

[See all](/en/guides-overview-performance)

