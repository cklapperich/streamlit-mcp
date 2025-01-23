# Node.js Driver¶

Note

This driver currently does not support GCP regional endpoints. Please ensure
that any workloads using through this driver do not require support for
regional endpoints on GCP. If you have questions about this, please contact
Snowflake Support.

Written in pure JavaScript, the Node.js driver provides a native asynchronous
Node.js interface to Snowflake.

For more information about Node.js, see [nodejs.org](https://nodejs.org).

The driver supports the versions of Node.js supported by the Node.js
Foundation. The driver supports the following Node.js versions:

  * v18

  * v20

  * v22

See the [driver release timeline](https://nodejs.org/en/about/previous-
releases) for more information.

The typical workflow for using the driver is:

  1. Establish a connection with Snowflake.

  2. Execute statements, e.g. queries and DDL/DML commands.

  3. Consume the results.

  4. Terminate the connection.

Important

To upload and download files from a Snowflake stage, you must use the
following minimum versions of the driver:

  * Version 1.6.2 to upload files (using the [PUT](../../sql-reference/sql/put) command)

  * Version 1.6.6 to download files (using the [GET](../../sql-reference/sql/get) command)

**Next topics:**

  * [Installing the Node.js Driver](nodejs-driver-install)
  * [Managing connections](nodejs-driver-connect)
  * [Authenticating connections](nodejs-driver-authenticate)
  * [Executing statements](nodejs-driver-execute)
  * [Consuming results](nodejs-driver-consume)
  * [Configuring log levels and files](nodejs-driver-logs)
  * [Node.js options reference](nodejs-driver-options)

