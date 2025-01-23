# PHP PDO Driver for Snowflake¶

Note

This driver currently does not support GCP regional endpoints. Please ensure
that any workloads using through this driver do not require support for
regional endpoints on GCP. If you have questions about this, please contact
Snowflake Support.

The PHP PDO driver for Snowflake provides an interface for developing PHP
applications that can connect to Snowflake and perform all standard
operations.

For a list of the operating systems supported by Snowflake clients, see
[Operating system support](../../release-notes/requirements.html#label-client-
operating-system-support).

For instructions on installing and using the driver, see the GitHub [PHP PDO
Driver for Snowflake repository](https://github.com/snowflakedb/pdo_snowflake)
in GitHub.

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

