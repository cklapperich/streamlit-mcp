# Overview of Key Features¶

This topic lists the notable/significant features supported in the current
release. Note that it does not list every feature provided by Snowflake.

## Security, Governance, and Data Protection¶

  * Choose the geographical location where your data is stored, based on your [region](intro-regions).

  * [User authentication](admin-user-management) through standard user/password credentials.

  * Enhanced authentication:

    * [Multi-factor authentication (MFA)](security-mfa).

    * [Federated authentication and single sign-on (SSO)](admin-security-fed-auth-overview).

    * [Snowflake OAuth](oauth-snowflake-overview).

    * [External OAuth](oauth-ext-overview).

  * All communication between clients, including all Snowflake connectors and drivers, and the server is protected through TLS.

  * Deployment inside a cloud platform VPC (AWS or GCP) or VNet (Azure).

  * Isolation of data (for loading and unloading) using:

    * [Amazon S3 policy controls](data-load-s3-config).

    * [Azure storage access controls](data-load-azure-config).

    * [Google Cloud Storage access permissions](data-load-gcs-config).

  * Support for PHI data (in compliance with HIPAA and [HITRUST CSF](intro-cloud-platforms.html#label-hitrust-csf-cert) regulations) — requires Business Critical Edition (or higher).

  * Automatic [data encryption](security-encryption-end-to-end) by Snowflake using Snowflake-managed keys.

  * [Object-level access control](security-access-control-overview).

  * [Snowflake Time Travel](data-time-travel) (1 day standard for all accounts; additional days, up to 90, allowed with Snowflake Enterprise) for:

    * Querying historical data in tables.

    * Restoring and cloning historical data in databases, schemas, and tables.

  * [Snowflake Fail-safe](data-failsafe) (7 days standard for all accounts) for disaster recovery of historical data.

  * [Column-level Security](security-column-intro) to apply masking policies to columns in tables or views — requires Enterprise Edition (or higher).

  * [Row-level Security](security-row-intro) to apply row access policies to tables and views — requires Enterprise Edition (or higher).

  * [Object Tagging](object-tagging) to apply tags to Snowflake objects to facilitate tracking sensitive data and resource usage — requires Enterprise Edition (or higher).

  * [Differential privacy](diff-privacy/differential-privacy-overview) to protect data against targeted privacy attacks. — requires Enterprise Edition (or higher).

## Standard and Extended SQL Support¶

  * Most DDL defined in SQL:1999, including:

    * [Databases, schemas, tables, and related objects](../sql-reference/sql-ddl-summary).

    * [Core data types](../sql-reference-data-types).

    * [SET operations](../sql-reference/constructs).

    * [CAST functions](../sql-reference/functions-conversion).

  * [Standard DML](../sql-reference/sql-dml) such as UPDATE, DELETE, and INSERT, as well as more advanced DML:

    * [Multi-table INSERT, MERGE, and multi-merge](../sql-reference/sql-dml).

    * [DML for bulk data loading/unloading](../sql-reference/sql-dml).

  * [Iceberg tables](tables-iceberg).

  * [Transactions](../sql-reference/transactions).

  * [Temporary and transient tables](../sql-reference/sql/create-table) for transitory data.

  * [Lateral views](../sql-reference/constructs/from).

  * [Materialized views](views-materialized).

  * [Statistical aggregate functions](../sql-reference/functions-aggregation).

  * [Analytical aggregates (Group by cube, rollup, and grouping sets)](../sql-reference/constructs/group-by).

  * Parts of the SQL:2003 analytic extensions:

    * [Window functions](../sql-reference/functions-window).

    * [Grouping sets](../sql-reference/constructs/group-by).

  * Scalar and tabular [user-defined functions (UDFs)](../developer-guide/udf/udf-overview), with support for Java, JavaScript, Python, Scala, and SQL.

  * [Stored procedures](../developer-guide/stored-procedure/stored-procedures-overview) and procedural language support ([Snowflake Scripting](../developer-guide/snowflake-scripting/index))

  * [Snowflake Information Schema](../sql-reference/info-schema) for querying object and account metadata, as well as query and warehouse usage history data.

  * Recursive queries, including:

    * [CONNECT BY](../sql-reference/constructs/connect-by).

    * [Recursive CTE (common table expressions)](../sql-reference/constructs/with).

  * [Collation support](../sql-reference/collation).

  * [Geospatial data support](../sql-reference/data-types-geospatial).

## Tools and Interfaces¶

  * [Snowsight](ui-snowsight-quick-tour) for account and general management, monitoring of resources and system usage, and querying data.

  * [SnowSQL (Python-based command line client)](snowsql).

  * Virtual warehouse management from the GUI or command line, including [creating, resizing (with zero downtime), suspending, and dropping](warehouses) warehouses.

  * [Snowflake Extension for Visual Studio Code](vscode-ext) \- Detailed instructions for installing, configuring and using the Snowflake Extension for Visual Studio Code.

## Apps and Extensibility¶

  * [APIs for Java, Python, and Scala](../developer-guide/snowpark/index) with which you can build applications that process data in Snowflake without moving data to the system where your application code runs.

  * A [framework for creating applications](../developer-guide/native-apps/native-apps-about) to share data content and application logic with other Snowflake accounts.

  * A [RESTful API](../developer-guide/sql-api/index) for accessing and updating data.

  * Support for running [Streamlit apps natively in Snowflake](../developer-guide/streamlit/about-streamlit) to create and share custom web apps for machine learning and data science.

  * Support for [developing procedures and user-defined functions (UDFs)](../developer-guide/extensibility) with a handler in one of several programming languages.

  * Extensive set of client connectors and drivers provided by Snowflake:

    * [Python connector](../developer-guide/python-connector/python-connector)

    * [Spark connector](spark-connector)

    * [Node.js driver](../developer-guide/node-js/nodejs-driver)

    * [Go Snowflake driver](../developer-guide/golang/go-driver)

    * [.NET driver](../developer-guide/dotnet/dotnet-driver)

    * [JDBC client driver](../developer-guide/jdbc/jdbc)

    * [ODBC client driver](../developer-guide/odbc/odbc)

    * [PHP PDO driver](../developer-guide/php-pdo/php-pdo-driver)

  * [Snowpark Container Services](../developer-guide/snowpark-container-services/overview) is a fully managed container offering that helps you easily deploy, manage, and scale containerized applications.

## Connectivity¶

  * Broad [ecosystem](ecosystem) of supported 3rd-party partners and technologies.

  * Support for using free trials to [connect to selected partners](ecosystem-partner-connect).

## Data Import and Export¶

  * Support for bulk [loading](../guides-overview-loading-data) and [unloading](data-unload-overview) data into/out of tables, including:

    * Load any data that uses a supported character encoding.

    * Load data from compressed files.

    * Load most flat, delimited data files (CSV, TSV, etc.).

    * Load data files in JSON, Avro, ORC, Parquet, and XML format.

    * Load from files in cloud storage or local files using the Snowflake web interface or command line client.

  * Support for continuous data loading from files:

    * Use [Snowpipe](data-load-snowpipe-intro) to load data in micro-batches from internal (i.e. Snowflake) stages or external (Amazon S3, Google Cloud Storage, or Microsoft Azure) stages.

  * Support for accessing data in [S3-compatible storage](data-load-s3-compatible-storage).

## Data Sharing¶

  * Support for both [sharing data in secured objects](../guides-overview-sharing) and [sharing data in non-secure views](../guides-overview-sharing) with other Snowflake accounts:

    * Provide data to other accounts to consume.

    * Consume data provided by other accounts.

  * Support for collaborators using [Snowflake Data Clean Rooms](cleanrooms/introduction) to share data in a privacy-preserving environment.

## Replication and Failover¶

  * Support for [replication and failover](account-replication-intro) across multiple Snowflake accounts in different [regions](intro-regions) and [cloud platforms](intro-cloud-platforms):

    * Replicate objects between Snowflake accounts (within the same organization) and keep the objects and stored data synchronized.

    * Configure failover to one or more Snowflake accounts for business continuity and disaster recovery.

