# Tutorial 1: Create a Snowpark Container Services Service¶  
  
[![Snowflake logo in black \(no text\)](../../../_images/logo-snowflake-
black.png)](../../../_images/logo-snowflake-black.png) Feature — Generally
Available

Available to accounts in [AWS and Microsoft Azure commercial
regions](../../../user-guide/intro-regions.html#label-na-general-regions),
with some exceptions. For more information, see [Available
regions](../overview.html#label-snowpark-containers-overview-available-
regions).

## Introduction¶

After completing the [common setup](common-setup), you are ready to create a
service. In this tutorial, you create a service (named `echo_service`) that
simply echoes back text that you provide as input. For example, if the input
string is “Hello World,” the service returns “I said, Hello World.”

There are two parts to this tutorial:

**Part 1: Create and test a service.** You download code provided for this
tutorial and follow step-by-step instructions:

  1. Download the service code for this tutorial.

  2. Build a Docker image for Snowpark Container Services, and upload the image to a repository in your account.

  3. Create a service by providing the service specification file and the compute pool in which to run the service.

  4. Create a service function to communicate with the service.

  5. Use the service. You send echo requests to the service and verify the response.

**Part 2: Understand the service**. This section provides an overview of the
service code and highlights how different components collaborate.

## 1: Download the service code¶

Code (a Python application) is provided to create the Echo service.

  1. Download [`SnowparkContainerServices-Tutorials.zip`](../../../_downloads/c3a8f6109048f2ecca7734c7fd3b0b3b/SnowparkContainerServices-Tutorials.zip).

  2. Unzip the content, which includes one directory for each tutorial. The `Tutorial-1` directory has the following files:

     * `Dockerfile`

     * `echo_service.py`

     * `templates/basic_ui.html`

## 2: Build an image and upload¶

Build an image for the linux/amd64 platform that Snowpark Container Services
supports, and then upload the image to the image repository in your account
(see [Common Setup](common-setup)).

You will need information about the repository (the repository URL and the
registry hostname) before you can build and upload the image. For more
information, see [Registry and Repositories](../working-with-registry-
repository).

**Get information about the repository**

  1. To get the repository URL, execute the [SHOW IMAGE REPOSITORIES](../../../sql-reference/sql/show-image-repositories) SQL command.
    
        SHOW IMAGE REPOSITORIES;
    

Copy

     * The `repository_url` column in the output provides the URL. An example is shown:
        
                <orgname>-<acctname>.registry.snowflakecomputing.com/tutorial_db/data_schema/tutorial_repository
        

     * The host name in the repository URL is the registry host name. An example is shown:
        
                <orgname>-<acctname>.registry.snowflakecomputing.com
        

**Build image and upload it to the repository**

  1. Open a terminal window, and change to the directory containing the files you unzipped.

  2. To build a Docker image, execute the following `docker build` command using the Docker CLI. Note the command specifies current working directory (`.`) as the `PATH` for files to use for building the image.
    
        docker build --rm --platform linux/amd64 -t <repository_url>/<image_name> .
    

Copy

     * For `_image_name_`, use `my_echo_service_image:latest`.

**Example**

    
        docker build --rm --platform linux/amd64 -t myorg-myacct.registry.snowflakecomputing.com/tutorial_db/data_schema/tutorial_repository/my_echo_service_image:latest .
    

Copy

  3. Upload the image to the repository in your Snowflake account. In order for Docker to upload an image on your behalf to your repository, you must first [authenticate Docker with the registry](../working-with-registry-repository.html#label-registry-and-repository-authentication).

    1. To authenticate Docker with the image registry, execute the following command.
        
                docker login <registry_hostname> -u <username>
        

Copy

       * For `_username_`, specify your Snowflake username. Docker will prompt you for your password.

    2. To upload the image execute the following command:
        
                docker push <repository_url>/<image_name>
        

Copy

**Example**

        
                docker push myorg-myacct.registry.snowflakecomputing.com/tutorial_db/data_schema/tutorial_repository/my_echo_service_image:latest
        

Copy

## 3: Create a service¶

In this section you create a service and also create a service function to
communicate with the service.

To create a service, you need the following:

  * A [compute pool](../working-with-compute-pool). Snowflake runs your service in the specified compute pool. You created a compute pool as part of the common setup.

  * A [service specification](../specification-reference). This specification provides Snowflake with the information needed to configure and run your service. For more information, see [Snowpark Container Services: Working with services](../working-with-services). In this tutorial, you provide the specification inline, in CREATE SERVICE command. You can also save the specification to a file in your Snowflake stage and provide file information in the CREATE SERVICE command as shown in Tutorial 2.

A service function is one of the methods available to communicate with your
service. A service function is a user-defined function (UDF) that you
associate with the service endpoint. When the service function is executed, it
sends a request to the service endpoint and receives a response.

  1. Verify that the compute pool is ready and that you are in the right context to create the service.

    1. Previously you set the context in the [Common Setup](common-setup.html#label-snowpark-containers-common-setup-create-objects) step. To ensure you are in the right context for the SQL statements in this step, execute the following:

> >     USE ROLE test_role;
>     USE DATABASE tutorial_db;
>     USE SCHEMA data_schema;
>     USE WAREHOUSE tutorial_warehouse;
>  
>
> Copy

    1. To ensure the compute pool you created in the [common setup](common-setup.html#label-snowpark-containers-common-setup-create-objects) is ready, execute `DESCRIBE COMPUTE POOL`, and verify that the `state` is `ACTIVE` or `IDLE`. If the `state` is `STARTING`, you need to wait until the `state` changes to either `ACTIVE` or `IDLE`.

> >     DESCRIBE COMPUTE POOL tutorial_compute_pool;
>  
>
> Copy

  2. To create the service, execute the following command using `test_role`:
    
        CREATE SERVICE echo_service
      IN COMPUTE POOL tutorial_compute_pool
      FROM SPECIFICATION $$
        spec:
          containers:
          - name: echo
            image: /tutorial_db/data_schema/tutorial_repository/my_echo_service_image:latest
            env:
              SERVER_PORT: 8000
              CHARACTER_NAME: Bob
            readinessProbe:
              port: 8000
              path: /healthcheck
          endpoints:
          - name: echoendpoint
            port: 8000
            public: true
          $$
       MIN_INSTANCES=1
       MAX_INSTANCES=1;
    

Copy

Note

If a service with that name already exists, use the DROP SERVICE command to
delete the previously created service, and then create this service.

  3. Execute the following SQL commands to get detailed information about the service you just created. For more information, see [Snowpark Container Services: Working with services](../working-with-services).

     * To list services in your account, execute the SHOW SERVICES command:
        
                SHOW SERVICES;
        

Copy

     * To get information about your service including the service status, execute the [DESCRIBE SERVICE](../../../sql-reference/sql/desc-service) command.
        
                DESC SERVICE echo_service;
        

Copy

Verify the `status` column shows the service status as RUNNING; if the status
is PENDING, it indicates the service is still starting. To investigate why the
service is not RUNNING, execute the [SHOW SERVICE CONTAINERS IN
SERVICE](../../../sql-reference/sql/show-service-containers-in-service)
command and review the `status` of individual containers:

        
                SHOW SERVICE CONTAINERS IN SERVICE echo_service;
        

Copy

  4. To create a service function, execute the following command:
    
        CREATE FUNCTION my_echo_udf (InputText varchar)
      RETURNS varchar
      SERVICE=echo_service
      ENDPOINT=echoendpoint
      AS '/echo';
    

Copy

Note the following:

     * The SERVICE property associates the UDF with the `echo_service` service.

     * The ENDPOINT property associates the UDF with the `echoendpoint` endpoint within the service.

     * AS ‘/echo’ specifies the HTTP path to the Echo server. You can find this path in the service code (`echo_service.py`).

## 4: Use the service¶

First, setup the context for the SQL statements in this section, execute the
following:

    
    
    USE ROLE test_role;
    USE DATABASE tutorial_db;
    USE SCHEMA data_schema;
    USE WAREHOUSE tutorial_warehouse;
    

Copy

Now you can communicate with the Echo service.

  1. **Using a service function:** You can invoke the service function in a query. The example service function (`my_echo_udf`) can take either a single string or a list of strings as input.

**Example 1.1: Pass a single string**

     * To call the `my_echo_udf` service function, execute the following SELECT statement, passing one input string (`'hello'`):
        
                SELECT my_echo_udf('hello!');
        

Copy

Snowflake sends a POST request to the service endpoint (`echoendpoint`). Upon
receiving the request, the service echos the input string in the response.

        
                +--------------------------+
        | **MY_ECHO_UDF('HELLO!')**|
        |------------------------- |
        | Bob said hello!          |
        +--------------------------+
        

**Example 1.2: Pass a list of strings**

When you pass a list of strings to the service function, Snowflake batches
these input strings and sends a series of POST requests to the service. After
the service processes all the strings, Snowflake combines the results and
returns them.

The following example passes a table column as input to the service function.

    1. Create a table with multiple strings:
        
                CREATE TABLE messages (message_text VARCHAR)
          AS (SELECT * FROM (VALUES ('Thank you'), ('Hello'), ('Hello World')));
        

Copy

    2. Verify that the table was created:
        
                SELECT * FROM messages;
        

Copy

    3. To call the service function, execute the following SELECT statement, passing table rows as input:
        
                SELECT my_echo_udf(message_text) FROM messages;
        

Copy

Output:

        
                +---------------------------+
        | MY_ECHO_UDF(MESSAGE_TEXT) |
        |---------------------------|
        | Bob said Thank you        |
        | Bob said Hello            |
        | Bob said Hello World      |
        +---------------------------+
        

  2. **Using a web browser:** The service exposes the endpoint publicly (see the inline specification provided in the CREATE SERVICE command). Therefore, you can log in to a web UI the service exposes to the internet, and then send requests to the service from a web browser.

    1. Find the URL of the public endpoint the service exposes:
        
                SHOW ENDPOINTS IN SERVICE echo_service;
        

Copy

The `ingress_url` column in the response provides the URL.

**Example**

        
                p6bye-myorg-myacct.snowflakecomputing.app
        

    2. Append `/ui` to the endpoint URL, and paste it in the web browser. This causes the service to execute the `ui()` function (see `echo_service.py`).

Note that the first time you access the endpoint URL, you will be asked to log
in to Snowflake. For this test, use the same user that you used to create the
service to ensure the user has the necessary privileges.

[![Web form to communicate with echo service.](../../../_images/Snowpark-
Containers-T1-web-ui-10.png)](../../../_images/Snowpark-Containers-T1-web-
ui-10.png)

    3. Enter the string “Hello” in the **Input** box, and press **Return**.

[![Web form showing response from the Echo
service.](../../../_images/Snowpark-Containers-T1-web-
ui-20.png)](../../../_images/Snowpark-Containers-T1-web-ui-20.png)

Note

You can access the public endpoint programmatically. For sample code, see
[Public endpoint access from outside Snowflake and authentication](../working-
with-services.html#label-snowpark-containers-service-public-endpoint-access).
Note that you need to append `/ui` to the endpoint URL in the code so that
Snowflake can route the request to the `ui()` function in the service code.

## 5: (Optional) Access the public endpoint programmatically¶

In the preceding section, you tested the Echo service using a web browser. In
the browser, you accessed the public endpoint (ingress endpoint) and sent
requests using the web UI that the service exposed. In this section you test
the same public endpoint programmatically.

The example uses [key pair authentication](../../../user-guide/key-pair-auth).
Using the key pair you provide, the sample code first generates a JSON Web
Token (JWT) and then exchanges the token with Snowflake for an OAuth token.
The code then uses the OAuth token for authentication when communicating with
the Echo service public endpoint.

### Prerequisites¶

Make sure you have the following information:

  * **Ingress URL of the public endpoint.** Execute the SHOW ENDPOINTS IN SERVICE command to get the URL:
    
        SHOW ENDPOINTS IN SERVICE echo_service;
    

Copy

  * **Your Snowflake account name.** For more information, see the [Common Setup: Verify that you are ready to continue](common-setup.html#label-snowpark-containers-common-setup-verify-ready).

  * **Your Snowflake account URL:** It is `<acctname>.snowflakecomputing.com`.

  * **User name in the Snowflake account.** This is the user you chose in [Common Setup: Create Snowflake objects](common-setup.html#label-snowpark-containers-common-setup-create-objects). You login to Snowflake as this user and test the programmatic access.

  * **Role name:** You created a role (`test_role`) as part of the common setup. The user assumes this role to perform actions.

### Setup¶

Follow the steps to communicate with the Echo service programmatically. Using
the Python code provided, you send requests to the public endpoint that the
Echo service exposes.

  1. At a command prompt, create a directory and navigate to it.

  2. Configure key pair authentication for the user.

    1. Generate a [key pair](../../../user-guide/key-pair-auth.html#label-configuring-key-pair-authentication):

      1. Generate a private key. To simplify the exercise steps, you generate an unencrypted private key. You can also use an encrypted private key but it will require you to enter the password.
            
                        openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out rsa_key.p8 -nocrypt
            

Copy

      2. Generate a public key (`rsa_key.pub`) by referencing the private key you created.
            
                        openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
            

Copy

    2. Verify you have the private key and public key generated in the directory.

    3. Assign the public key to the user you are using to test the programmatic access. This lets the user specify the key for authentication.
        
                ALTER USER <user-name> SET RSA_PUBLIC_KEY='MIIBIjANBgkqh...';
        

Copy

  3. Save the provided sample code in Python files.

    1. Save the following code in `generateJWT.py`.
        
                # To run this on the command line, enter:
        #   python3 generateJWT.py --account=<account_identifier> --user=<username> --private_key_file_path=<path_to_private_key_file>
        
        from cryptography.hazmat.primitives.serialization import load_pem_private_key
        from cryptography.hazmat.primitives.serialization import Encoding
        from cryptography.hazmat.primitives.serialization import PublicFormat
        from cryptography.hazmat.backends import default_backend
        from datetime import timedelta, timezone, datetime
        import argparse
        import base64
        from getpass import getpass
        import hashlib
        import logging
        import sys
        
        # This class relies on the PyJWT module (https://pypi.org/project/PyJWT/).
        import jwt
        
        logger = logging.getLogger(__name__)
        
        try:
            from typing import Text
        except ImportError:
            logger.debug('# Python 3.5.0 and 3.5.1 have incompatible typing modules.', exc_info=True)
            from typing_extensions import Text
        
        ISSUER = "iss"
        EXPIRE_TIME = "exp"
        ISSUE_TIME = "iat"
        SUBJECT = "sub"
        
        # If you generated an encrypted private key, implement this method to return
        # the passphrase for decrypting your private key. As an example, this function
        # prompts the user for the passphrase.
        def get_private_key_passphrase():
            return getpass('Passphrase for private key: ')
        
        class JWTGenerator(object):
            """
            Creates and signs a JWT with the specified private key file, username, and account identifier. The JWTGenerator keeps the
            generated token and only regenerates the token if a specified period of time has passed.
            """
            LIFETIME = timedelta(minutes=59)  # The tokens will have a 59-minute lifetime
            RENEWAL_DELTA = timedelta(minutes=54)  # Tokens will be renewed after 54 minutes
            ALGORITHM = "RS256"  # Tokens will be generated using RSA with SHA256
        
            def __init__(self, account: Text, user: Text, private_key_file_path: Text,
                        lifetime: timedelta = LIFETIME, renewal_delay: timedelta = RENEWAL_DELTA):
                """
                __init__ creates an object that generates JWTs for the specified user, account identifier, and private key.
                :param account: Your Snowflake account identifier. See https://docs.snowflake.com/en/user-guide/admin-account-identifier.html. Note that if you are using the account locator, exclude any region information from the account locator.
                :param user: The Snowflake username.
                :param private_key_file_path: Path to the private key file used for signing the JWTs.
                :param lifetime: The number of minutes (as a timedelta) during which the key will be valid.
                :param renewal_delay: The number of minutes (as a timedelta) from now after which the JWT generator should renew the JWT.
                """
        
                logger.info(
                    """Creating JWTGenerator with arguments
                    account : %s, user : %s, lifetime : %s, renewal_delay : %s""",
                    account, user, lifetime, renewal_delay)
        
                # Construct the fully qualified name of the user in uppercase.
                self.account = self.prepare_account_name_for_jwt(account)
                self.user = user.upper()
                self.qualified_username = self.account + "." + self.user
        
                self.lifetime = lifetime
                self.renewal_delay = renewal_delay
                self.private_key_file_path = private_key_file_path
                self.renew_time = datetime.now(timezone.utc)
                self.token = None
        
                # Load the private key from the specified file.
                with open(self.private_key_file_path, 'rb') as pem_in:
                    pemlines = pem_in.read()
                    try:
                        # Try to access the private key without a passphrase.
                        self.private_key = load_pem_private_key(pemlines, None, default_backend())
                    except TypeError:
                        # If that fails, provide the passphrase returned from get_private_key_passphrase().
                        self.private_key = load_pem_private_key(pemlines, get_private_key_passphrase().encode(), default_backend())
        
            def prepare_account_name_for_jwt(self, raw_account: Text) -> Text:
                """
                Prepare the account identifier for use in the JWT.
                For the JWT, the account identifier must not include the subdomain or any region or cloud provider information.
                :param raw_account: The specified account identifier.
                :return: The account identifier in a form that can be used to generate the JWT.
                """
                account = raw_account
                if not '.global' in account:
                    # Handle the general case.
                    idx = account.find('.')
                    if idx > 0:
                        account = account[0:idx]
                else:
                    # Handle the replication case.
                    idx = account.find('-')
                    if idx > 0:
                        account = account[0:idx]
                # Use uppercase for the account identifier.
                return account.upper()
        
            def get_token(self) -> Text:
                """
                Generates a new JWT. If a JWT has already been generated earlier, return the previously generated token unless the
                specified renewal time has passed.
                :return: the new token
                """
                now = datetime.now(timezone.utc)  # Fetch the current time
        
                # If the token has expired or doesn't exist, regenerate the token.
                if self.token is None or self.renew_time <= now:
                    logger.info("Generating a new token because the present time (%s) is later than the renewal time (%s)",
                                now, self.renew_time)
                    # Calculate the next time we need to renew the token.
                    self.renew_time = now + self.renewal_delay
        
                    # Prepare the fields for the payload.
                    # Generate the public key fingerprint for the issuer in the payload.
                    public_key_fp = self.calculate_public_key_fingerprint(self.private_key)
        
                    # Create our payload
                    payload = {
                        # Set the issuer to the fully qualified username concatenated with the public key fingerprint.
                        ISSUER: self.qualified_username + '.' + public_key_fp,
        
                        # Set the subject to the fully qualified username.
                        SUBJECT: self.qualified_username,
        
                        # Set the issue time to now.
                        ISSUE_TIME: now,
        
                        # Set the expiration time, based on the lifetime specified for this object.
                        EXPIRE_TIME: now + self.lifetime
                    }
        
                    # Regenerate the actual token
                    token = jwt.encode(payload, key=self.private_key, algorithm=JWTGenerator.ALGORITHM)
                    # If you are using a version of PyJWT prior to 2.0, jwt.encode returns a byte string instead of a string.
                    # If the token is a byte string, convert it to a string.
                    if isinstance(token, bytes):
                      token = token.decode('utf-8')
                    self.token = token
                    logger.info("Generated a JWT with the following payload: %s", jwt.decode(self.token, key=self.private_key.public_key(), algorithms=[JWTGenerator.ALGORITHM]))
        
                return self.token
        
            def calculate_public_key_fingerprint(self, private_key: Text) -> Text:
                """
                Given a private key in PEM format, return the public key fingerprint.
                :param private_key: private key string
                :return: public key fingerprint
                """
                # Get the raw bytes of public key.
                public_key_raw = private_key.public_key().public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)
        
                # Get the sha256 hash of the raw bytes.
                sha256hash = hashlib.sha256()
                sha256hash.update(public_key_raw)
        
                # Base64-encode the value and prepend the prefix 'SHA256:'.
                public_key_fp = 'SHA256:' + base64.b64encode(sha256hash.digest()).decode('utf-8')
                logger.info("Public key fingerprint is %s", public_key_fp)
        
                return public_key_fp
        
        def main():
            logging.basicConfig(stream=sys.stdout, level=logging.INFO)
            cli_parser = argparse.ArgumentParser()
            cli_parser.add_argument('--account', required=True, help='The account identifier (e.g. "myorganization-myaccount" for "myorganization-myaccount.snowflakecomputing.com").')
            cli_parser.add_argument('--user', required=True, help='The user name.')
            cli_parser.add_argument('--private_key_file_path', required=True, help='Path to the private key file used for signing the JWT.')
            cli_parser.add_argument('--lifetime', type=int, default=59, help='The number of minutes that the JWT should be valid for.')
            cli_parser.add_argument('--renewal_delay', type=int, default=54, help='The number of minutes before the JWT generator should produce a new JWT.')
            args = cli_parser.parse_args()
        
            token = JWTGenerator(args.account, args.user, args.private_key_file_path, timedelta(minutes=args.lifetime), timedelta(minutes=args.renewal_delay)).get_token()
            print('JWT:')
            print(token)
        
        if __name__ == "__main__":
            main()
        

Copy

    2. Save the following code in `access-via-keypair.py`.
        
                from generateJWT import JWTGenerator
        from datetime import timedelta
        import argparse
        import logging
        import sys
        import requests
        logger = logging.getLogger(__name__)
        
        def main():
          args = _parse_args()
          token = _get_token(args)
          snowflake_jwt = token_exchange(token,endpoint=args.endpoint, role=args.role,
                          snowflake_account_url=args.snowflake_account_url,
                          snowflake_account=args.account)
          spcs_url=f'https://{args.endpoint}{args.endpoint_path}'
          connect_to_spcs(snowflake_jwt, spcs_url)
        
        def _get_token(args):
          token = JWTGenerator(args.account, args.user, args.private_key_file_path, timedelta(minutes=args.lifetime),
                    timedelta(minutes=args.renewal_delay)).get_token()
          logger.info("Key Pair JWT: %s" % token)
          return token
        
        def token_exchange(token, role, endpoint, snowflake_account_url, snowflake_account):
          scope_role = f'session:role:{role}' if role is not None else None
          scope = f'{scope_role} {endpoint}' if scope_role is not None else endpoint
          data = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            'scope': scope,
            'assertion': token,
          }
          logger.info(data)
          url = f'https://{snowflake_account}.snowflakecomputing.com/oauth/token'
          if snowflake_account_url:
            url =       f'{snowflake_account_url}/oauth/token'
          logger.info("oauth url: %s" %url)
          response = requests.post(url, data=data)
          logger.info("snowflake jwt : %s" % response.text)
          assert 200 == response.status_code, "unable to get snowflake token"
          return response.text
        
        def connect_to_spcs(token, url):
          # Create a request to the ingress endpoint with authz.
          headers = {'Authorization': f'Snowflake Token="{token}"'}
          response = requests.post(f'{url}', headers=headers)
          logger.info("return code %s" % response.status_code)
          logger.info(response.text)
        
        def _parse_args():
          logging.basicConfig(stream=sys.stdout, level=logging.INFO)
          cli_parser = argparse.ArgumentParser()
          cli_parser.add_argument('--account', required=True,
                      help='The account identifier (for example, "myorganization-myaccount" for '
                        '"myorganization-myaccount.snowflakecomputing.com").')
          cli_parser.add_argument('--user', required=True, help='The user name.')
          cli_parser.add_argument('--private_key_file_path', required=True,
                      help='Path to the private key file used for signing the JWT.')
          cli_parser.add_argument('--lifetime', type=int, default=59,
                      help='The number of minutes that the JWT should be valid for.')
          cli_parser.add_argument('--renewal_delay', type=int, default=54,
                      help='The number of minutes before the JWT generator should produce a new JWT.')
          cli_parser.add_argument('--role',
                      help='The role we want to use to create and maintain a session for. If a role is not provided, '
                        'use the default role.')
          cli_parser.add_argument('--endpoint', required=True,
                      help='The ingress endpoint of the service')
          cli_parser.add_argument('--endpoint-path', default='/',
                      help='The url path for the ingress endpoint of the service')
          cli_parser.add_argument('--snowflake_account_url', default=None,
                      help='The account url of the account for which we want to log in. Type of '
                        'https://myorganization-myaccount.snowflakecomputing.com')
          args = cli_parser.parse_args()
          return args
        
        if __name__ == "__main__":
          main()
        

Copy

### Send requests to the service endpoint programmatically¶

Execute the `access-via-keypair.py` Python code to make the ingress call to
the Echo service public endpoint.

>
>     python3 access-via-keypair.py \
>       --account <account-identifier> \
>       --user <user-name> \
>       --role TEST_ROLE \
>       --private_key_file_path rsa_key.p8 \
>       --endpoint <ingress-hostname> \
>       --endpoint-path /ui
>  
>
> Copy

For more information about `account-identifier`, see [Account
identifiers](../../../user-guide/admin-account-identifier).

### How authentication works¶

The code first converts the provided key pair into a JWT token. It then sends
the JWT token to Snowflake to obtain an OAuth token. Finally, the code uses
the OAuth token to connect to Snowflake and access the public endpoint.
Specifically, the code does the following:

  1. Calls the `_get_token(args)` function to generate a JWT token from the key pair you provide. The function implementation is shown:
    
        def _get_token(args):
        token = JWTGenerator(args.account,
                            args.user,
                            args.private_key_file_path,
                            timedelta(minutes=args.lifetime),
                            timedelta(minutes=args.renewal_delay)).get_token()
        logger.info("Key Pair JWT: %s" % token)
        return token
    

Copy

`JWTGenerator` is a helper class that is provided to you. Note the following
about the parameters you provide when creating this object:

     * `args.account` and the `args.user` parameters: A JWT token has several fields (see [token format](../../sql-api/authenticating.html#label-sql-api-authenticating-key-pair)), `iss` is one of the fields. This field value includes the Snowflake account name and a user name. Therefore, you provide these values as parameters.

     * The two `timedelta` parameters provide the following information:

       * `lifetime` specifies the number of minutes during which the key will be valid (60 minutes).

       * `renewal_delay` specifies the number of minutes from now after which the JWT generator should renew the JWT.

  2. Calls the `token_exchange()` function to connect to Snowflake and exchange the JWT token for an OAuth token.
    
        scope_role = f'session:role:{role}' if role is not None else None
    scope = f'{scope_role} {endpoint}' if scope_role is not None else endpoint
    
    data = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'scope': scope,
        'assertion': token,
    }
    

Copy

The preceding code constructs a JSON setting the scope for the OAuth token,
the public endpoint that can be accessed using the specified role. This code
then makes a POST request to Snowflake passing the JSON to exchange the JWT
token for an OAuth token (see [Token exchange](../../../user-guide/oauth-
custom.html#label-oauth-token-exchange)) as shown:

    
        url = f'{snowflake_account_url}/oauth/token'
    response = requests.post(url, data=data)
    assert 200 == response.status_code, "unable to get Snowflake token"
    return response.text
    

Copy

  3. The code then calls `connect_to_spcs()` function to connect to the public endpoint of the Echo service. It provides the URL (`https://<ingress-URL>/ui`) of the endpoint and the OAuth token for authentication.
    
        headers = {'Authorization': f'Snowflake Token="{token}"'}
    response = requests.post(f'{url}', headers=headers)
    

Copy

The `url` is the `spcs_url` you provided to the program and the `token` is the
OAuth token.

The Echo service in this example serves an HTML page (as explained in the
preceding section). This sample code simply prints the HTML in the response.

## 6: Clean up¶

If you do not plan to continue with [Tutorial 2](tutorial-2) or [Tutorial
3](advanced/tutorial-3), you should remove billable resources you created. For
more information, see Step 5 in [Tutorial 3](advanced/tutorial-3).

## 7: Reviewing the service code¶

This section covers the following topics:

  * Examining the tutorial 1 code: Review the code files that implement the Echo service.

  * Understanding the service function: This section explains how the service function in this tutorial is linked with the service.

  * Building and testing an image locally. The section provides an explanation of how you can locally test the Docker image before uploading it to a repository in your Snowflake account.

### Examining the tutorial 1 code¶

The zip file you downloaded in Step 1 includes the following files:

  * `Dockerfile`

  * `echo_service.py`

  * `templates/basic_ui.html`

You also use service specification when creating the service. The following
section explains how these code components work together to create the
service.

#### echo_service.py file¶

This Python file contains the code that implements a minimal HTTP server that
returns (echoes back) input text. The code primarily performs two tasks:
handling echo requests from Snowflake service functions, and providing a web
user interface (UI) for submitting echo requests.

    
    
    from flask import Flask
    from flask import request
    from flask import make_response
    from flask import render_template
    import logging
    import os
    import sys
    
    SERVICE_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
    SERVER_PORT = os.getenv('SERVER_PORT', 8080)
    CHARACTER_NAME = os.getenv('CHARACTER_NAME', 'I')
    
    
    def get_logger(logger_name):
      logger = logging.getLogger(logger_name)
      logger.setLevel(logging.DEBUG)
      handler = logging.StreamHandler(sys.stdout)
      handler.setLevel(logging.DEBUG)
      handler.setFormatter(
        logging.Formatter(
          '%(name)s [%(asctime)s] [%(levelname)s] %(message)s'))
      logger.addHandler(handler)
      return logger
    
    
    logger = get_logger('echo-service')
    
    app = Flask(__name__)
    
    
    @app.get("/healthcheck")
    def readiness_probe():
      return "I'm ready!"
    
    
    @app.post("/echo")
    def echo():
      '''
      Main handler for input data sent by Snowflake.
      '''
      message = request.json
      logger.debug(f'Received request: {message}')
    
      if message is None or not message['data']:
        logger.info('Received empty message')
        return {}
    
      # input format:
      #   {"data": [
      #     [row_index, column_1_value, column_2_value, ...],
      #     ...
      #   ]}
      input_rows = message['data']
      logger.info(f'Received {len(input_rows)} rows')
    
      # output format:
      #   {"data": [
      #     [row_index, column_1_value, column_2_value, ...}],
      #     ...
      #   ]}
      output_rows = [[row[0], get_echo_response(row[1])] for row in input_rows]
      logger.info(f'Produced {len(output_rows)} rows')
    
      response = make_response({"data": output_rows})
      response.headers['Content-type'] = 'application/json'
      logger.debug(f'Sending response: {response.json}')
      return response
    
    
    @app.route("/ui", methods=["GET", "POST"])
    def ui():
      '''
      Main handler for providing a web UI.
      '''
      if request.method == "POST":
        # getting input in HTML form
        input_text = request.form.get("input")
        # display input and output
        return render_template("basic_ui.html",
          echo_input=input_text,
          echo_reponse=get_echo_response(input_text))
      return render_template("basic_ui.html")
    
    
    def get_echo_response(input):
      return f'{CHARACTER_NAME} said {input}'
    
    if __name__ == '__main__':
      app.run(host=SERVICE_HOST, port=SERVER_PORT)
    

Copy

In the code:

  * The `echo` function enables a Snowflake service function to communicate with the service. This function specifies the `@app.post()` decoration as shown:
    
        @app.post("/echo")
    def echo():
    

Copy

When the echo server receives your HTTP POST request with the `/echo` path,
the server routes the request to this function. The function executes and
echoes back the strings from the request body in the response.

To support communication from a Snowflake service function, this server
implements the external functions. That is, the server implementation follows
a certain input/output data format in order to serve a SQL function, and this
is the same [input/output data format](../../../sql-reference/external-
functions-data-format) used by [External Functions](../../../sql-
reference/external-functions).

  * The `ui` function section of the code displays a web form and handles echo requests submitted from the web form. This function uses the `@app.route()` decorator to specify that requests for `/ui` are handled by this function:
    
        @app.route("/ui", methods=["GET", "POST"])
    def ui():
    

Copy

The Echo service exposes the `echoendpoint` endpoint publicly (see service
specification), enabling communication with the service over the web. When you
load the URL of the public endpoint with /ui appended in your browser, the
browser sends an HTTP GET request for this path, and the server routes the
request to this function. The function executes and returns a simple HTML form
for the user to enter a string in.

After the user enters a string and submits the form, the browser sends an HTTP
post request for this path, and the server routes the request to this same
function. The function executes and returns an HTTP response containing the
original string.

  * The `readiness_probe` function uses the `@app.get()` decorator to specify that requests for `/healthcheck` are handled by this function:
    
        @app.get("/healthcheck")
    def readiness_probe():
    

Copy

This function enables Snowflake to check the readiness of the service. When
the container starts, Snowflake wants to confirm that the application is
working and that the service is ready to serve the requests. Snowflake sends
an HTTP GET request with this path (as a health probe, readiness probe) to
ensure that only healthy containers serve traffic. The function can do
whatever you want.

  * The `get_logger` function helps set up logging.

#### Dockerfile¶

This file contains all the commands to build an image using Docker.

    
    
    ARG BASE_IMAGE=python:3.10-slim-buster
    FROM $BASE_IMAGE
    COPY echo_service.py ./
    COPY templates/ ./templates/
    RUN pip install --upgrade pip && \\
    pip install flask
    CMD ["python", "echo_service.py"]
    

Copy

The Dockerfile contains instructions to install the Flask library in the
Docker container. The code in `echo_service.py` relies on the Flask library to
handle HTTP requests.

#### /template/basic_ui.html¶

The Echo service exposes the `echoendpoint` endpoint publicly (see service
specification), enabling communication with the service over the web. When you
load the public endpoint URL with `/ui` appended in your browser, the Echo
service displays this form. You can enter a string in the form and submit the
form, and the service returns the string in an HTTP response.

    
    
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <title>Welcome to echo service!</title>
      </head>
      <body>
        <h1>Welcome to echo service!</h1>
        <form action="{{ url_for("ui") }}" method="post">
          <label for="input">Input:<label><br>
          <input type="text" id="input" name="input"><br>
        </form>
        <h2>Input:</h2>
        {{ echo_input }}
        <h2>Output:</h2>
        {{ echo_reponse }}
      </body>
    </html>
    

Copy

#### Service specification¶

Snowflake uses information you provide in this specification to configure and
run your service.

    
    
    spec:
      containers:
      - name: echo
        image: /tutorial_db/data_schema/tutorial_repository/my_echo_service_image:latest
        env:
          SERVER_PORT: 8000
          CHARACTER_NAME: Bob
        readinessProbe:
          port: 8000
          path: /healthcheck
      endpoints:
      - name: echoendpoint
        port: 8000
        public: true
    

Copy

In the service specification:

  * The `containers.image` specifies the image for Snowflake to start a container.

  * The optional `endpoints` field specifies the endpoint the service exposes.

    * The `name` specifies a user-friendly name for the TCP network port the container is listening on. You use this user-friendly endpoint name to send requests to the corresponding port. Note that the `env.SERVER_PORT` controls this port number.

    * The endpoint is also configured as `public`. This allows traffic to this endpoint from the public web.

  * The optional `containers.env` field is added to illustrate how you might override environment variables that Snowflake passes to all processes in your container. For example, the service code (`echo_service.py`) reads the environment variables with default values as shown:
    
        CHARACTER_NAME = os.getenv('CHARACTER_NAME', 'I')
    SERVER_PORT = os.getenv('SERVER_PORT', 8080)
    

Copy

It works as follows:

    * When the Echo service receives an HTTP POST request with a string (e.g., “Hello”) in the request body, the service returns “I said Hello” by default. The code uses the `CHARACTER_NAME` environment variable to determine the word before “said.” By default, `CHARACTER_NAME` is set to “I.”

You can overwrite the CHARACTER_NAME default value in the service
specification. For example, if you set the value to “Bob,” the Echo service
returns a “Bob said Hello” response.

    * Similarly, the service specification overrides the port (SERVER_PORT) that the service listens on to 8000, overriding the default port 8080.

  * The `readinessProbe` field identifies the `port` and `path` that Snowflake can use to send an HTTP GET request to the readiness probe to verify that the service is ready to handle traffic.

The service code (`echo_python.py`) implements the readiness probe as follows:

    
        @app.get("/healthcheck")
    def readiness_probe():
    

Copy

Therefore, the specification file includes the `container.readinessProbe`
field accordingly.

For more information about service specifications, see [Service specification
reference](../specification-reference).

### Understanding the service function¶

A service function is one of the methods of communicating with your service
(see [Using a service](../working-with-services.html#label-snowpark-
containers-service-communicating)). A service function is a user-defined
function (UDF) that you associate with a service endpoint. When the service
function is executed, it sends a request to the associated service endpoint
and receives a response.

You create the following service function by executing the CREATE FUNCTION
command with the following parameters:

    
    
    CREATE FUNCTION my_echo_udf (InputText VARCHAR)
      RETURNS VARCHAR
      SERVICE=echo_service
      ENDPOINT=echoendpoint
      AS '/echo';
    

Copy

Note the following:

  * The `my_echo_udf` function takes a string as input and returns a string.

  * The SERVICE property identifies the service (`echo_service`), and the ENDPOINT property identifies the user-friendly endpoint name (`echoendpoint`).

  * The AS ‘/echo’ specifies the path for the service. In `echo_service.py`, the `@app.post` decorator associates this path with the `echo` function.

This function connects with the specific ENDPOINT of the specified SERVICE.
When you invoke this function, Snowflake sends a request to the `/echo` path
inside the service container.

### Building and testing an image locally¶

You can test the Docker image locally before uploading it to a repository in
your Snowflake account. In local testing, your container runs standalone (it
is not a service that Snowflake runs).

To test the Tutorial 1 Docker image:

  1. To create a Docker image, in the Docker CLI, execute the following command:
    
        docker build --rm -t my_service:local .
    

Copy

  2. To launch your code, execute the following command:
    
        docker run --rm -p 8080:8080 my_service:local
    

Copy

  3. Send an echo request to the service using one of the following methods:

     * **Using the cURL command:**

In another terminal window, using cURL, send the following POST request to
port 8080:

        
                curl -X POST http://localhost:8080/echo \
          -H "Content-Type: application/json" \
          -d '{"data":[[0, "Hello friend"], [1, "Hello World"]]}'
        

Copy

Note that the request body includes two strings. This cURL command sends a
POST request to port 8080 on which the service is listening. The 0 in the data
is the index of the input string in the list. The Echo service echoes the
input strings in response as shown:

        
                {"data":[[0,"I said Hello Friend"],[1,"I said Hello World"]]}
        

     * **Using a web browser:**

       1. In your browser, on the same computer, open `http://localhost:8080/ui`.

This sends a GET request to port 8080, which the service is listening on. The
service executes the `ui()` function, which renders a HTML form as shown:

[![Web form to communicate with echo service.](../../../_images/Snowpark-
Containers-T1-web-ui-10.png)](../../../_images/Snowpark-Containers-T1-web-
ui-10.png)

       2. Enter the string “Hello” in the **Input** box, and press **Return**.

[![Web form showing response from the Echo
service.](../../../_images/Snowpark-Containers-T1-web-
ui-20.png)](../../../_images/Snowpark-Containers-T1-web-ui-20.png)

## What’s next?¶

You can now test the [Tutorial 2](tutorial-2) that executes a job.

