# Snowflake client connectivity and troubleshooting¶

This topic provides an architecture overview explaining the various service
endpoints required for normal client operations. It also provides a
methodology for self-service troubleshooting general connectivity issues and
error patterns for JDBC, ODBC, and for Snowflake Connector for Python and
SnowSQL as additional references.

  * Architecture

  * [Common connectivity issues and resolutions](common-issues)

  * [Troubleshooting steps](troubleshooting-steps)

  * [Error messages](error-messages)

Note

The term client as used in this article refers to any custom or third-party
application using a Snowflake command-line client (e.g.,
[SnowSQL](../snowsql)), driver (e.g., [Go](../../developer-guide/golang/go-
driver), [JDBC](../../developer-guide/jdbc/jdbc), [NodeJs](../../developer-
guide/node-js/nodejs-driver), [ODBC](../../developer-guide/odbc/odbc),
[PHP](../../developer-guide/php-pdo/php-pdo-driver), [Python](../../developer-
guide/python-connector/python-connector)), or API (e.g., [Snowpipe REST
API](../data-load-snowpipe-rest-apis), [SQL API](../../developer-guide/sql-
api/index)). For completeness, it also includes browser access to the
Snowflake Web Interface (e.g., [Classic](../ui-using), [Snowsight](../ui-
snowsight)).

## Architecture¶

For more information regarding the configuration steps for the architectures,
refer to [Securing Snowflake](../../guides-overview-secure).

![Non-private client connectivity to Snowflake](../../_images/arch-non-client-
connectivity.png)

Non-private client connectivity to Snowflake¶

![Private client connectivity to Snowflake \(without private connectivity to
Snowflake internal stages\)](../../_images/arch-private-client-
connectivity-1.png)

Private client connectivity to Snowflake (without private connectivity to
Snowflake internal stages 1)¶

![Private client connectivity to Snowflake \(with private connectivity to
Snowflake internal stages\)](../../_images/arch-private-client-
connectivity-2.png)

Private client connectivity to Snowflake (without private connectivity to
Snowflake internal stages 1)¶

1 Configuration details for this feature are out of scope for this article.
For more information, refer to [Securing Snowflake](../../guides-overview-
secure).

