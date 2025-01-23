# External network access overview¶  
  
You can create secure access to specific network locations external to
Snowflake, then use that access from within the handler code for user-defined
functions (UDFs) and stored procedures. You can enable this access through an
external access integration.

With an external access integration, you can:

  * Write UDF and procedure handlers that access external locations.

  * Allow or block access to locations on a network external to Snowflake.

  * Use secrets that represent stored credentials, rather than using literal values, within handler code to authenticate with external network locations.

  * Specify which secrets are allowed for use with external network locations.

  * Choose whether your connectivity to the external network location uses the public Internet or a private network using Azure Private Link.

If you choose to use Azure Private Link, your Snowflake account must be
Business Critical Edition (or higher).

For more information, see [External network access and private connectivity on
Microsoft Azure](creating-using-private-azure).

## Get started¶

For an introduction to external network access, including code examples, refer
to [External network access examples](external-network-access-examples).

## References¶

  * [CREATE EXTERNAL ACCESS INTEGRATION](../../sql-reference/sql/create-external-access-integration)

  * [ALTER EXTERNAL ACCESS INTEGRATION](../../sql-reference/sql/alter-external-access-integration)

  * [DESCRIBE INTEGRATION](../../sql-reference/sql/desc-integration)

  * [DROP INTEGRATION](../../sql-reference/sql/drop-integration)

  * [SHOW INTEGRATIONS](../../sql-reference/sql/show-integrations)

