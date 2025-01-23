# Go Snowflake Driver¶

Note

This driver currently does not support GCP regional endpoints. Please ensure
that any workloads using through this driver do not require support for
regional endpoints on GCP. If you have questions about this, please contact
Snowflake Support.

The Go Snowflake Driver provides an interface for developing applications
using the Go programming language to connect to Snowflake and perform all
standard operations. The driver implements the Go
[database/sql](https://golang.org/pkg/database/sql) package.

For a list of the operating systems supported by Snowflake clients, see
[Operating system support](../../release-notes/requirements.html#label-client-
operating-system-support).

For complete installation instructions, as well as developer notes and the
source code, see the GitHub [Go Snowflake Driver
repo](https://github.com/snowflakedb/gosnowflake).

For usage information, see the GoDoc [gosnowflake
documentation](https://godoc.org/github.com/snowflakedb/gosnowflake).

## Verifying the network connection to Snowflake with SnowCD¶

After configuring your driver, you can evaluate and troubleshoot your network
connectivity to Snowflake using [SnowCD](../../user-guide/snowcd).

You can use SnowCD during the initial configuration process and on-demand at
any time to evaluate and troubleshoot your network connection to Snowflake.

Important

Beginning with Snowflake version 8.24, network administrators have the option
to require multi-factor authentication (MFA) for all connections to Snowflake.
If your administrator decides to enable this feature, you must configure your
client or driver to use MFA when connecting to Snowflake. For more
information, see the following resources:

  * [8.24 release notes](../../release-notes/2024/8_24.html#label-authentication-policies-new-multi-factor-authentication-parameters)

  * [Multi-factor authentication (MFA)](../../user-guide/security-mfa)

  * [Troubleshooting service users authentication issues with Snowflake MFA](https://community.snowflake.com/s/article/Troubleshooting-service-users-authentication-issues-with-Snowflake-MFA) Knowledge Base article

