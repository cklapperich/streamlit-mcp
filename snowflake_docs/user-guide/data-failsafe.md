# Understanding and viewing Fail-safe¶

Separate and distinct from Time Travel, Fail-safe ensures historical data is
protected in the event of a system failure or other event (e.g. a security
breach).

## What is Fail-safe?¶

![Fail-safe in Continuous Data Protection lifecycle](../_images/cdp-lifecycle-
fs.png)

Fail-safe provides a (non-configurable) 7-day period during which historical
data may be recoverable by Snowflake. This period starts immediately after the
Time Travel retention period ends. Note, however, that a long-running Time
Travel query will delay moving any data and objects (tables, schemas, and
databases) in the account into Fail-safe, until the query completes.

Attention

Fail-safe is a data recovery service that is provided on a best effort basis
and is intended only for use when all other recovery options have been
attempted.

Fail-safe is not provided as a means for accessing historical data after the
Time Travel retention period has ended. It is for use only by Snowflake to
recover data that may have been lost or damaged due to extreme operational
failures.

Data recovery through Fail-safe may take from several hours to several days to
complete.

## View Fail-safe storage for your account¶

When you review the total data storage usage for your account in Snowsight and
Classic Console, you can view the historical data storage in Fail-safe.

You must use the ACCOUNTADMIN role to view the amount of data that is stored
in Snowflake.

In Snowsight, follow these steps:

  1. Select Admin » Cost Management » Consumption.

  2. Use the All Usage Types filter to select Storage.

  3. Review the graph and table for Fail-safe storage.

In Classic Console, follow these steps:

  1. Select Account » Billing & Usage.

  2. Select Average Storage Used and then select Fail Safe to view only Fail-safe storage usage.

