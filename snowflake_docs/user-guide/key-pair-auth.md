# Key-pair authentication and key-pair rotation¶  
  
This topic describes using key pair authentication and key pair rotation in
Snowflake.

## Overview¶

Snowflake supports using key pair authentication for enhanced authentication
security as an alternative to basic authentication, such as username and
password.

This authentication method requires, as a minimum, a 2048-bit RSA key pair.
You can generate the Privacy Enhanced Mail (PEM) private-public key pair using
OpenSSL. Some of the Supported Snowflake Clients allow using encrypted private
keys to connect to Snowflake. The public key is assigned to the Snowflake user
who uses the Snowflake client to connect and authenticate to Snowflake.

Snowflake also supports rotating public keys in an effort to allow compliance
with more robust security and governance postures.

## Supported Snowflake clients¶

The following table summarizes support for key pair authentication among
Snowflake Clients. A checkmark (✔) indicates full support. A missing checkmark
indicates key pair authentication is not supported.

Client | Key Pair Authentication | Key Pair Rotation | Unencrypted Private Keys | Encrypted Private Keys  
---|---|---|---|---  
[Snowflake CLI](../developer-guide/snowflake-cli/index) | ✔ | ✔ | ✔ | ✔  
[SnowSQL (CLI client)](snowsql) | ✔ | ✔ | ✔ |   
[Snowflake Connector for Python](../developer-guide/python-connector/python-connector) | ✔ | ✔ | ✔ | ✔  
[Snowflake Connector for Spark](spark-connector) | ✔ | ✔ | ✔ |   
[Snowflake Connector for Kafka](kafka-connector) | ✔ | ✔ | ✔ |   
[Go driver](https://godoc.org/github.com/snowflakedb/gosnowflake) | ✔ | ✔ | ✔ |   
[JDBC Driver](../developer-guide/jdbc/jdbc) | ✔ | ✔ | ✔ | ✔  
[ODBC Driver](../developer-guide/odbc/odbc) | ✔ | ✔ | ✔ | ✔  
[Node.js Driver](../developer-guide/node-js/nodejs-driver) | ✔ | ✔ | ✔ | ✔  
[.NET Driver](../developer-guide/dotnet/dotnet-driver) | ✔ | ✔ | ✔ | ✔  
[PHP PDO Driver for Snowflake](../developer-guide/php-pdo/php-pdo-driver) | ✔ | ✔ | ✔ | ✔  
  
## Configuring key-pair authentication¶

Complete the following steps to configure key pair authentication for all
supported Snowflake clients.

### Generate the private key¶

Depending on which one of the Supported Snowflake Clients you use to connect
to Snowflake, you have the option to generate encrypted or unencrypted private
keys. Generally, it is safer to generate encrypted keys. Snowflake recommends
communicating with your internal security and governance officers to determine
which key type to generate prior to completing this step.

Tip

The command to generate an encrypted key prompts for a passphrase to regulate
access to the key. Snowflake recommends using a passphrase that complies with
PCI DSS standards to protect the locally generated private key. Additionally,
Snowflake recommends storing the passphrase in a secure location. If you are
using an encrypted key to connect to Snowflake, enter the passphrase during
the initial connection. The passphrase is only used for protecting the private
key and will never be sent to Snowflake.

To generate a long and complex passphrase based on PCI DSS standards:

>   1. Access the [PCI Security Standards Document
> Library](https://www.pcisecuritystandards.org/document_library).
>
>   2. For PCI DSS, select the most recent version and your desired language.
>
>   3. Complete the form to access the document.
>
>   4. Search for `Passwords/passphrases must meet the following:` and follow
> the recommendations for password/passphrase requirements, testing, and
> guidance. Depending on the document version, the phrase is likely located in
> a section called `Requirement 8: Identify and authenticate access to system
> components` or a similar name.
>
>

To start, open a terminal window and generate a private key.

You can generate either an encrypted version of the private key or an
unencrypted version of the private key.

To generate an unencrypted version, use the following command:

    
    
    openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out rsa_key.p8 -nocrypt
    

Copy

To generate an encrypted version, use the following command, which omits
`-nocrypt`:

    
    
    openssl genrsa 2048 | openssl pkcs8 -topk8 -v2 des3 -inform PEM -out rsa_key.p8
    

Copy

The commands generate a private key in PEM format.

    
    
    -----BEGIN ENCRYPTED PRIVATE KEY-----
    MIIE6T...
    -----END ENCRYPTED PRIVATE KEY-----
    

Copy

### Generate a public key¶

From the command line, generate the public key by referencing the private key.
The following command assumes the private key is encrypted and contained in
the file named `rsa_key.p8`.

    
    
    openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
    

Copy

The command generates the public key in PEM format.

    
    
    -----BEGIN PUBLIC KEY-----
    MIIBIj...
    -----END PUBLIC KEY-----
    

Copy

### Store the private and public keys securely¶

Copy the public and private key files to a local directory for storage. Record
the path to the files. Note that the private key is stored using the PKCS#8
(Public Key Cryptography Standards) format and is encrypted using the
passphrase you specified in the previous step.

However, the file should still be protected from unauthorized access using the
file permission mechanism provided by your operating system. It is your
responsibility to secure the file when it is not being used.

### Assign the public key to a Snowflake user¶

Execute an [ALTER USER](../sql-reference/sql/alter-user) command to assign the
public key to a Snowflake user.

    
    
    ALTER USER example_user SET RSA_PUBLIC_KEY='MIIBIjANBgkqh...';
    

Copy

Note

  * Only owners of a user, or users with the SECURITYADMIN role or higher can alter a user. For more information, see [Overview of Access Control](security-access-control-overview) and [GRANT OWNERSHIP](../sql-reference/sql/grant-ownership)

  * Exclude the public key delimiters in the SQL statement.

### Verify the user’s public key fingerprint¶

  1. Execute the following command to retrieve the user’s public key fingerprint:
    
        DESC USER example_user;
    SELECT SUBSTR((SELECT "value" FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
      WHERE "property" = 'RSA_PUBLIC_KEY_FP'), LEN('SHA256:') + 1);
    

Copy

Output:

    
        Azk1Pq...
    

  2. Copy the output.

  3. Run the following command on the command line:
    
        openssl rsa -pubin -in rsa_key.pub -outform DER | openssl dgst -sha256 -binary | openssl enc -base64
    

Copy

Output:

    
        writing RSA key
    Azk1Pq...
    

  4. Compare both outputs. If both outputs match, the user correctly configured their public key.

### Configure the Snowflake client to use key-pair authentication¶

Update the client to use key pair authentication to connect to Snowflake.

  * [Snowflake CLI](../developer-guide/snowflake-cli/connecting/configure-connections.html#label-snowcli-private-key)

  * [SnowSQL](snowsql-start.html#label-snowsql-key-pair-authn-rotation)

  * [Python connector](../developer-guide/python-connector/python-connector-connect.html#label-python-key-pair-authn-rotation)

  * [Spark connector](spark-connector-use.html#label-spark-key-pair-authn-rotation)

  * [Kafka connector](kafka-connector-install.html#label-kafka-key-pair-authn-rotation)

  * [Go driver](https://godoc.org/github.com/snowflakedb/gosnowflake)

  * [JDBC driver](../developer-guide/jdbc/jdbc-configure.html#label-jdbc-using-key-pair-authentication)

  * [ODBC driver](../developer-guide/odbc/odbc-parameters.html#label-odbc-key-pair-authentication)

  * [.NET driver](https://github.com/snowflakedb/snowflake-connector-net/blob/master/README.md)

  * [Node.js Driver](../developer-guide/node-js/nodejs-driver-authenticate.html#label-nodejs-key-pair-authentication)

## Configuring key-pair rotation¶

Snowflake supports multiple active keys to allow for uninterrupted rotation.
Rotate and replace your public and private keys based on the expiration
schedule you follow internally.

Currently, you can use the `RSA_PUBLIC_KEY` and `RSA_PUBLIC_KEY_2` parameters
for [ALTER USER](../sql-reference/sql/alter-user) to associate up to 2 public
keys with a single user.

Complete the following steps to configure key pair rotation and rotate your
keys.

  1. Complete all steps in Configuring key-pair authentication with the following updates:

     * Generate a new private and public key set.

     * Assign the public key to the user. Set the public key value to either `RSA_PUBLIC_KEY` or `RSA_PUBLIC_KEY_2`, whichever key value is not currently in use. For example:
        
                ALTER USER example_user SET RSA_PUBLIC_KEY_2='JERUEHtcve...';
        

Copy

  2. Update the code to connect to Snowflake. Specify the new private key.

Snowflake verifies the correct active public key for authentication based on
the private key submitted with your connection information.

  3. Remove the old public key from the user profile using an [ALTER USER](../sql-reference/sql/alter-user) command.
    
        ALTER USER example_user UNSET RSA_PUBLIC_KEY;
    

Copy

