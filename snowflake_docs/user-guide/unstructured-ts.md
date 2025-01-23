# Troubleshooting processing of unstructured data¶

This topic provides instructions for resolving issues specific to processing
unstructured data.

## Downloaded files cannot be opened¶

When attempting to open a file downloaded from a stage using a URL, you could
encounter an error such as `invalid format`.

Verify that the ENCRYPTION property for the stage is configured for server-
side encryption. Server-side encryption is required to access staged files
using a URL. For more information, see [Server-side encryption for
unstructured data access](unstructured-intro.html#label-file-url-server-side-
encryption).

For external stages, the server-side encryption setting varies by cloud
storage provider. For internal stages, set the ENCRYPTION property value to
`SNOWFLAKE_SSE`.

The encryption type is specified when creating a stage (using [CREATE
STAGE](../sql-reference/sql/create-stage)) or later (using [ALTER
STAGE](../sql-reference/sql/alter-stage)).

