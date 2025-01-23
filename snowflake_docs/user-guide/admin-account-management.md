# Parameter management¶

Snowflake provides three types of parameters that can be set for your account:

  * Account parameters that affect your entire account.

  * Session parameters that default to users and their sessions.

  * Object parameters that default to objects (warehouses, databases, schemas, and tables).

All parameters have default values, which can be overridden at the account
level. To override default values at the account level, you must be an account
administrator (i.e. user granted the ACCOUNTADMIN role).

In addition, the default values for session and object parameters can be
overridden at each level in the parameter hierarchy.

## Viewing parameters for your account¶

To see a list of the parameters and their current values for your account, as
well as their default values, use the [SHOW PARAMETERS](../sql-
reference/sql/show-parameters) command with the following syntax:

    
    
    SHOW PARAMETERS [ LIKE '<pattern>' ] IN ACCOUNT
    

Copy

For example, to see a complete list of all account-level parameters:

>
>     SHOW PARAMETERS IN ACCOUNT;
>  
>
> +-------------------------------------+----------------------------------+----------------------------------+---------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
>     | key                                 | value                            | default                          | level   | description                                                                                                                                                                         |
>
> |-------------------------------------+----------------------------------+----------------------------------+---------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
>     | ABORT_DETACHED_QUERY                | false                            | false                            |         | If true, Snowflake will automatically abort queries when it detects that the client has disappeared.                                                                                |
>     | AUTOCOMMIT                          | true                             | true                             |         | The autocommit property determines whether is statement should to be implicitly                                                                                                     |
>     |                                     |                                  |                                  |         | wrapped within a transaction or not. If autocommit is set to true, then a                                                                                                           |
>     |                                     |                                  |                                  |         | statement that requires a transaction is executed within a transaction                                                                                                              |
>     |                                     |                                  |                                  |         | implicitly. If autocommit is off then an explicit commit or rollback is required                                                                                                    |
>     |                                     |                                  |                                  |         | to close a transaction. The default autocommit value is true.                                                                                                                       |
>     | AUTOCOMMIT_API_SUPPORTED            | true                             | true                             |         | Whether autocommit feature is enabled for this client. This parameter is for                                                                                                        |
>     |                                     |                                  |                                  |         | Snowflake use only.                                                                                                                                                                 |
>     | BINARY_INPUT_FORMAT                 | HEX                              | HEX                              |         | input format for binary                                                                                                                                                             |
>     | BINARY_OUTPUT_FORMAT                | HEX                              | HEX                              |         | display format for binary                                                                                                                                                           |
>     | CLIENT_ENCRYPTION_KEY_SIZE          | 128                              | 128                              |         | Client-side encryption key size in bits. Either 128 or 256.                                                                                                                         |
>     | CLIENT_SESSION_KEEP_ALIVE           | false                            | false                            |         | If true, client session will not expire automatically                                                                                                                               |
>     | DATA_RETENTION_TIME_IN_DAYS         | 1                                | 1                                |         | number of days to retain the old version of deleted/updated data                                                                                                                    |
>     | DATE_INPUT_FORMAT                   | AUTO                             | AUTO                             |         | input format for date                                                                                                                                                               |
>     | DATE_OUTPUT_FORMAT                  | YYYY-MM-DD                       | YYYY-MM-DD                       |         | display format for date                                                                                                                                                             |
>     | ERROR_ON_NONDETERMINISTIC_MERGE     | true                             | true                             |         | raise an error when attempting to merge-update a row that joins many rows                                                                                                           |
>     | ERROR_ON_NONDETERMINISTIC_UPDATE    | false                            | false                            |         | raise an error when attempting to update a row that joins many rows                                                                                                                 |
>     | LOCK_TIMEOUT                        | 43200                            | 43200                            |         | Number of seconds to wait while trying to lock a resource, before timing out                                                                                                        |
>     |                                     |                                  |                                  |         | and aborting the statement. A value of 0 turns off lock waiting i.e. the                                                                                                            |
>     |                                     |                                  |                                  |         | statement must acquire the lock immediately or abort. If multiple resources                                                                                                         |
>     |                                     |                                  |                                  |         | need to be locked by the statement, the timeout applies separately to each                                                                                                          |
>     |                                     |                                  |                                  |         | lock attempt.                                                                                                                                                                       |
>     | MAX_CONCURRENCY_LEVEL               | 8                                | 8                                |         | Concurrency level for SQL statements (i.e. queries and DML) executed by a warehouse cluster (used to determine when statements are queued or additional clusters are started).      |
>     | NETWORK_POLICY                      |                                  |                                  |         | Network policy assigned for the given target.                                                                                                                                       |
>     | PERIODIC_DATA_REKEYING              | false                            | false                            |         | If true, Snowflake will re-encrypt data that was encrypted more than a year ago.                                                                                                    |
>     | QUERY_TAG                           |                                  |                                  |         | String (up to 2000 characters) used to tag statements executed by the session                                                                                                       |
>     | QUOTED_IDENTIFIERS_IGNORE_CASE      | false                            | false                            |         | If true, the case of quoted identifiers is ignored                                                                                                                                  |
>     | ROWS_PER_RESULTSET                  | 0                                | 0                                |         | maxium number of rows in a result set                                                                                                                                               |
>     | SAML_IDENTITY_PROVIDER              |                                  |                                  |         | Authentication attributes for the SAML Identity provider                                                                                                                            |
>     | SSO_LOGIN_PAGE                      | true                             | false                            | ACCOUNT | Enable federated authentication for console login and redirects preview page to console login                                                                                       |
>     | STATEMENT_QUEUED_TIMEOUT_IN_SECONDS | 0                                | 0                                |         | Timeout in seconds for queued statements: statements will automatically be canceled if they are queued on a warehouse for longer than this amount of time; disabled if set to zero. |
>     | STATEMENT_TIMEOUT_IN_SECONDS        | 0                                | 0                                |         | Timeout in seconds for statements: statements will automatically be canceled if they run for longer than this amount of time; disabled if set to zero.                              |
>     | TIMESTAMP_DAY_IS_ALWAYS_24H         | false                            | true                             | SYSTEM  | If set, arithmetic on days always uses 24 hours per day,                                                                                                                            |
>     |                                     |                                  |                                  |         | possibly not preserving the time (due to DST changes)                                                                                                                               |
>     | TIMESTAMP_INPUT_FORMAT              | AUTO                             | AUTO                             |         | input format for timestamp                                                                                                                                                          |
>     | TIMESTAMP_LTZ_OUTPUT_FORMAT         |                                  |                                  |         | Display format for TIMESTAMP_LTZ values. If empty, TIMESTAMP_OUTPUT_FORMAT is used.                                                                                                 |
>     | TIMESTAMP_NTZ_OUTPUT_FORMAT         | YYYY-MM-DD HH24:MI:SS.FF3        | YYYY-MM-DD HH24:MI:SS.FF3        | SYSTEM  | Display format for TIMESTAMP_NTZ values. If empty, TIMESTAMP_OUTPUT_FORMAT is used.                                                                                                 |
>     | TIMESTAMP_OUTPUT_FORMAT             | YYYY-MM-DD HH24:MI:SS.FF3 TZHTZM | YYYY-MM-DD HH24:MI:SS.FF3 TZHTZM | SYSTEM  | Default display format for all timestamp types.                                                                                                                                     |
>     | TIMESTAMP_TYPE_MAPPING              | TIMESTAMP_NTZ                    | TIMESTAMP_NTZ                    | SYSTEM  | If TIMESTAMP type is used, what specific TIMESTAMP* type it should map to:                                                                                                          |
>     |                                     |                                  |                                  |         |   TIMESTAMP_LTZ (default), TIMESTAMP_NTZ or TIMESTAMP_TZ                                                                                                                            |
>     | TIMESTAMP_TZ_OUTPUT_FORMAT          |                                  |                                  |         | Display format for TIMESTAMP_TZ values. If empty, TIMESTAMP_OUTPUT_FORMAT is used.                                                                                                  |
>     | TIMEZONE                            | America/Los_Angeles              | America/Los_Angeles              |         | time zone                                                                                                                                                                           |
>     | TIME_INPUT_FORMAT                   | AUTO                             | AUTO                             |         | input format for time                                                                                                                                                               |
>     | TIME_OUTPUT_FORMAT                  | HH24:MI:SS                       | HH24:MI:SS                       |         | display format for time                                                                                                                                                             |
>     | TRANSACTION_ABORT_ON_ERROR          | false                            | false                            |         | If this parameter is true, and a statement issued within a non-autocommit                                                                                                           |
>     |                                     |                                  |                                  |         | transaction returns with an error, then the non-autocommit transaction is                                                                                                           |
>     |                                     |                                  |                                  |         | aborted. All statements issued inside that transaction will fail until an                                                                                                           |
>     |                                     |                                  |                                  |         | commit or rollback statement is executed to close that transaction.                                                                                                                 |
>     | TRANSACTION_DEFAULT_ISOLATION_LEVEL | READ COMMITTED                   | READ COMMITTED                   |         | The default isolation level when starting a starting a transaction, when no                                                                                                         |
>     |                                     |                                  |                                  |         | isolation level was specified                                                                                                                                                       |
>     | TWO_DIGIT_CENTURY_START             | 1970                             | 1970                             |         | For 2-digit dates, defines a century-start year.                                                                                                                                    |
>     |                                     |                                  |                                  |         | For example, when set to 1980:                                                                                                                                                      |
>     |                                     |                                  |                                  |         |   - parsing a string '79' will produce 2079                                                                                                                                         |
>     |                                     |                                  |                                  |         |   - parsing a string '80' will produce 1980                                                                                                                                         |
>     | UNSUPPORTED_DDL_ACTION              | ignore                           | ignore                           |         | The action to take upon encountering an unsupported ddl statement                                                                                                                   |
>     | USE_CACHED_RESULT                   | true                             | true                             |         | If enabled, query results can be reused between successive invocations of the same query as long as the original result has not expired                                             |
>
> +-------------------------------------+----------------------------------+----------------------------------+---------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
>  
>
> Copy

In the output, note the `value` and `level` columns:

  * `value` specifies the current value for each parameter.

  * `level` specifies where the current value comes from. If the `level` column is empty for a parameter, the parameter is not explicitly set and the current value is the default value.

## Altering parameters for your account¶

To alter a parameter for your account, log into Snowflake as an account
administrator and use the [ALTER ACCOUNT](../sql-reference/sql/alter-account)
command with the following syntax:

    
    
    ALTER ACCOUNT SET <param> = <value>
    

Copy

For example, to set the [DATE_OUTPUT_FORMAT](../sql-
reference/parameters.html#label-date-output-format) session parameter:

>
>     ALTER ACCOUNT SET DATE_OUTPUT_FORMAT = 'DD/MM/YYYY';
>  
>     SHOW PARAMETERS LIKE 'DATE_OUTPUT%' IN ACCOUNT;
>  
>
> +--------------------+------------+------------+---------+-------------------------+
>     | key                | value      | default    | level   | description             |
>
> |--------------------+------------+------------+---------+-------------------------|
>     | DATE_OUTPUT_FORMAT | DD/MM/YYYY | YYYY-MM-DD | ACCOUNT | display format for date |
>
> +--------------------+------------+------------+---------+-------------------------+
>  
>
> Copy
>
> Note that the `level` column in the output shows the value for the parameter
> is currently set at the account level.

This specifies that the default display format for all dates in a session will
be DD/MM/YYYY instead of YYYY-MM-DD (e.g. 23/04/2016 instead of 2016-04-23).
Note that this date display format is only the default and can be overridden
for any individual user or session.

### Resetting parameters¶

To reset a parameter for your account back to the default, use [ALTER
ACCOUNT](../sql-reference/sql/alter-account) with the following syntax:

    
    
    ALTER ACCOUNT UNSET <param>
    

Copy

For example, to set the [DATE_OUTPUT_FORMAT](../sql-
reference/parameters.html#label-date-output-format) session parameter back to
its default value:

>
>     ALTER ACCOUNT UNSET DATE_OUTPUT_FORMAT;
>  
>
> Copy

