# ODBC Driver¶

Note

This driver currently does not support GCP regional endpoints. Please ensure
that any workloads using through this driver do not require support for
regional endpoints on GCP. If you have questions about this, please contact
Snowflake Support.

Snowflake provides a driver for connecting to Snowflake using ODBC-based
client applications.

Important

The ODBC driver has different prerequisites depending on the platform where it
is installed. For details, see the individual installation and configuration
instructions for each platform.

In addition, different versions of the ODBC driver support the
[GET](../../sql-reference/sql/get) and [PUT](../../sql-reference/sql/put)
commands, depending on the cloud service that hosts your Snowflake account:

  * Amazon Web Services: Version 2.17.5 (and higher)

  * Google Cloud Platform: Version 2.21.5 (and higher)

  * Microsoft Azure: Version 2.20.2 (and higher)

**Next Topics:**

  * [Downloading the ODBC Driver](odbc-download)
  * [Installing and configuring the ODBC Driver for Windows](odbc-windows)
  * [Installing and configuring the ODBC Driver for macOS](odbc-mac)
  * [Installing and configuring the ODBC Driver for Linux](odbc-linux)
  * [ODBC configuration and connection parameters](odbc-parameters)
  * [ODBC Driver API support](odbc-api)
  * [Using the ODBC Driver](odbc-using)
  * [ODBC Driver diagnostic service](odbc-diagnostic-service)

