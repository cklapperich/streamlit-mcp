# .NET Driver¶

Note

This driver currently does not support GCP regional endpoints. Please ensure
that any workloads using through this driver do not require support for
regional endpoints on GCP. If you have questions about this, please contact
Snowflake Support.

The Snowflake .NET driver provides an interface to the Microsoft .NET open
source software framework for developing applications. The driver was
developed using Visual Studio.

For more information, see the [.NET](https://www.microsoft.com/net/) website.

For complete installation and usage instructions, as well as developer notes
and the source code, see the GitHub [Snowflake .NET driver
repo](https://github.com/snowflakedb/snowflake-connector-net).

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

