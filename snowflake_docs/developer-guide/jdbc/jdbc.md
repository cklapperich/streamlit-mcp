# JDBC Driver¶

Note

Version 3.21.0 introduced support for Google Cloud Storage regional endpoints.

Earlier versions of the driver do not support Google Cloud Storage regional
endpoints. Please ensure that any workloads that use this driver do not
require support for regional endpoints on Google Cloud. If you have questions
about this, please contact Snowflake Support.

Snowflake provides a JDBC type 4 driver that supports core JDBC functionality.
The JDBC driver must be installed in a 64-bit environment and requires Java
LTS (Long-Term Support) versions 1.8 or higher.

The driver can be used with most client tools/applications that support JDBC
for connecting to a database server. [sfsql](../../user-guide/sfsql), the now-
deprecated command line client provided by Snowflake, is an example of a JDBC-
based application.

**Next Topics:**

  * [Java requirements for the JDBC Driver](java-install)
  * [Downloading / integrating the JDBC Driver](jdbc-download)
  * [Configuring the JDBC Driver](jdbc-configure)
  * [Using the JDBC Driver](jdbc-using)
  * [JDBC Driver diagnostic service](jdbc-diagnostic-service)
  * [JDBC Driver connection parameter reference](jdbc-parameters)
  * [JDBC Driver API support](jdbc-api)

