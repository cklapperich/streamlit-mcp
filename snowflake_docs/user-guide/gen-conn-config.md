# Configuring a client, driver, library, or third-party application to connect
to Snowflake¶

To configure a client, driver, library, or application to connect to
Snowflake, you must specify your Snowflake account identifier. In addition,
you might need to specify the warehouse, database, schema, and role that
should be used.

## Specifying the account to use¶

Clients, connectors, and drivers use a variety of syntaxes to connect to
Snowflake. In general, you should use the variation that includes the
organization name (`_orgname_`) and account name (`_account_name_`), with the
following exception: If you use the [Client Redirect](client-redirect)
feature, replace the name of the account (`_account_name_`) with the name of
the connection (`_connection_name_`). For examples of this syntax, see [Using
a connection URL](client-redirect.html#label-using-a-connection-url).

To configure a private connection to the Snowflake service, add `.privatelink`
to either the account name or the account locator syntax. To determine which
value you should use to connect to Snowflake when using private connectivity,
call the [SYSTEM$GET_PRIVATELINK_CONFIG](../sql-
reference/functions/system_get_privatelink_config) function in your Snowflake
account.

If you need to use the account locator, you might also need to specify the
cloud region ID, the cloud, and the level of government compliance as
additional segments after the account locator. For the format to use, see
[Format 2: Account locator in a region](admin-account-identifier.html#label-
account-locator). In the examples below,
`_account_locator_with_additional_segments_` represents the account location
with any additional segments that are required.

SnowSQL:

    

  * Account name: `snowsql -a _orgname_ -_account_name_`

  * Account locator: `snowsql -a _account_locator_with_additional_segments_`

For additional information, see [Connection syntax](snowsql-start.html#label-
connection-syntax).

JDBC:

    

  * Account name: `jdbc:snowflake://_orgname >-<account_name_.snowflakecomputing.com/?_connection_paramsr_`

  * Account locator: `jdbc:snowflake://_account_locator_with_additional_segments_.snowflakecomputing.com/?_connection_params_`

For additional information, see [JDBC Driver connection string](../developer-
guide/jdbc/jdbc-configure.html#label-jdbc-connection-string).

ODBC:

    

  * Account name:

    * Server: `_orgname_ -_account_name_.snowflakecomputing.com`

  * Account locator:

    * Server: `_account_locator_with_additional_segments_.snowflakecomputing.com}`

For additional information, see [ODBC configuration and connection
parameters](../developer-guide/odbc/odbc-parameters).

Python:

    

  * Account name:

    * Set the `ACCOUNT` parameter value as `_orgname_ -_account_name_`.

  * Account locator:

    * Set the `ACCOUNT` parameter value as `_account_locator_with_additional_segments_`.

For additional information, see [Connecting to Snowflake with the Python
Connector](../developer-guide/python-connector/python-connector-connect).

.Net:

    

  * Account name:

    * Set the `ACCOUNT` parameter value as `_orgname_ -_account_name_`.

    * Set the `HOST` parameter value as the default (`.snowflakecomputing.com`).

  * Account locator:

    * Set the `ACCOUNT` parameter value as `_account_locator_with_additional_segments_`.

    * Set the `HOST` parameter value as the default `.snowflakecomputing.com`. Specify if your Snowflake account is not in the `us-west` region.

For additional information, see
[Connecting](https://github.com/snowflakedb/snowflake-connector-
net/blob/master/doc/Connecting.md).

Golang:

    

  * Account name: `db, err := sql.Open("snowflake", "jsmith:mypassword@_orgname_ -_account_name_ /mydb/testschema?warehouse=mywh")`

  * Account locator: `sql.Open("snowflake", "jsmith:mypassword@_account_locator_with_additional_segments_ /mydb/testschema?warehouse=mywh")`

For additional information, see [Connection
String](https://pkg.go.dev/github.com/snowflakedb/gosnowflake#hdr-
Connection_String).

node.js:

    

  * Account name: Set the `ACCOUNT` parameter value as `_orgname_ -_account_name_`.

  * Account locator: Set the `ACCOUNT` parameter value as `_account_locator_with_additional_segments_`.

For additional information, see [Managing connections](../developer-
guide/node-js/nodejs-driver-connect).

Spark (connector):

    

  * Account name: Same as JDBC

  * Account locator: Same as JDBC

For additional information, see [Setting Configuration Options for the
Connector](spark-connector-use.html#label-spark-options).

Spark (Databricks):

    

  * Account name: `_Account URL for Snowflake account_`

  * Account locator: `_Account Locator URL for Snowflake account_`

For additional information, see [Configuring Snowflake for Spark in
Databricks](spark-connector-databricks).

Spark (Qubole):

    

  * Account name: Set the Host Address field value as `_orgname_ -_account_name_.snowflakecomputing.com`.

  * Account locator: Set the Host Address field value as `_account_locator_with_additional_segments_.snowflakecomputing.com`.

For additional information, see [Configuring Snowflake for Spark in
Qubole](spark-connector-qubole).

PHP:

    

  * Account name:

    * Set the `ACCOUNT` parameter value as `_orgname_ -_account_name_`.

    * Leave the `REGION` parameter value blank for all regions.

  * Account locator:

    * Set the `ACCOUNT` parameter value as `_account_locator_`.

    * Set the `REGION` parameter value if your Snowflake account is not in the `us-west` region.

For additional information, see [Connecting to the Snowflake
database](https://github.com/snowflakedb/pdo_snowflake/blob/master/README.rst#connecting-
to-the-snowflake-database).

SQLAchemy:

    

  * Account name: `snowflake://_user_login_name_ :_password_ @_orgname_ -_account_name_`

  * Account locator: `snowflake://_user_login_name_ :_password_ @_account_locator_with_additional_segments_`

For additional information, see [Using the Snowflake SQLAlchemy toolkit with
the Python Connector](../developer-guide/python-connector/sqlalchemy).

## Using SQL statements to find your account identifier¶

To get the `_organization_name_ -_account_name_` form of your account
identifier, execute the following SQL command:

    
    
    SELECT CURRENT_ORGANIZATION_NAME() || '-' || CURRENT_ACCOUNT_NAME();
    

Copy

To get the [account locator](admin-account-identifier.html#label-account-
locator) form of your account identifier, execute the following SQL command:

    
    
    SELECT CURRENT_ACCOUNT();
    

Copy

## Additional configuration steps¶

The next topics cover specific areas of configuring a connection:

  * [Allowing Hostnames](hostname-allowlist)

  * [OCSP Configuration](ocsp)

