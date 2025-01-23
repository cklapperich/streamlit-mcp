# Limits on Query Text Size¶

Snowflake recommends you limit the size of query text (i.e. SQL statements)
submitted through Snowflake clients to 1 MB per statement. Larger queries
process normally, but you could not rerun or retry the larger queries, as
Snowflake truncates queries larger than 1MB per statement before persisting
them to the metadata store.

This limit includes any literals, such as string literals or binary literals,
that are part of the statement, whether as part of a WHERE clause, SET clause
(in an UPDATE statement), etc.

This limit also applies when binding values in client applications that use
Snowflake connectors and drivers, such as the JDBC Driver.

If multiple SQL statements are combined into a single string (separated by
semicolons), the length limit applies to the entire string, not to individual
statements within the string.

Similarly, if data is batched, for example by using the JDBC
`PreparedStatement.addBatch()` method, the entire batch must fit within the
limit.

Note

Snowflake compresses data when sending it between client and server. The limit
applies to the size after compression. However, since the compression ratio
for data varies widely, it is safest to keep the uncompressed size within the
limit.

To load data that exceeds the limit, load from data files as described in
[Load data into Snowflake](../guides-overview-loading-data).

