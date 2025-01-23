# Setting up Snowflake to use Git¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) Feature — Generally
Available

Using a Git repository in Snowflake is not supported in the Gov region.

When you integrate a Git repository and clone the repository, Snowflake
creates a Git repository stage that specifies the location of the repository,
credentials (if needed), and details about how Snowflake should interact with
the Git repository API.

To use a Git repository with Snowflake, follow these steps:

  1. Create a secret, if needed, to contain credentials for authenticating with the repository.

  2. Create an API integration to specify details about Snowflake interaction with the Git repository API.

  3. Create a Snowflake Git repository stage to which you can synchronize files from the repository.

## Create a secret with credentials for authenticating¶

If your Git repository requires authentication, you’ll need to [create a
secret](../../sql-reference/sql/create-secret) that contains credentials that
Snowflake can use to authenticate with the repository.

You’ll use the secret in multiple ways. Someone creating an API integration
that specifies Snowflake interaction with the Git repository API must specify
this secret as a value of the ALLOWED_AUTHENTICATION_SECRETS parameter. In
addition, someone setting up Snowflake to use Git specifies the secret.

To create a secret, you must use a role that has been granted the following
privileges:

  * CREATE SECRET on the schema where you’ll store the secret

For more information, see [CREATE SECRET access control
requirements](../../sql-reference/sql/create-secret.html#label-create-secret-
access-control).

  * USAGE on the database and schema that will contain the integration

As a best practice, use a personal access token for the secret’s PASSWORD
value. For information about creating a personal access token in GitHub, see
[Managing your personal access
tokens](https://docs.github.com/en/authentication/keeping-your-account-and-
data-secure/managing-your-personal-access-tokens) in the GitHub documentation.

SQL:

    

You can use the [CREATE SECRET](../../sql-reference/sql/create-secret) command
to create a secret that contains Git repository credentials.

Code in the following example creates a secret called `myco_git_secret` with a
username and the user’s personal access token to use as credentials:

    
    
    USE ROLE securityadmin;
    CREATE ROLE myco_secrets_admin;
    GRANT CREATE SECRET ON SCHEMA myco_db.integrations TO ROLE myco_secrets_admin;
    
    USE ROLE myco_db_owner;
    GRANT USAGE ON DATABASE myco_db TO ROLE myco_secrets_admin;
    GRANT USAGE ON SCHEMA myco_db.integrations TO ROLE myco_secrets_admin;
    
    USE ROLE myco_secrets_admin;
    USE DATABASE myco_db;
    USE SCHEMA myco_db.integrations;
    
    CREATE OR REPLACE SECRET myco_git_secret
      TYPE = password
      USERNAME = 'gladyskravitz'
      PASSWORD = 'ghp_token';
    

Copy

## Create an API integration for interacting with the repository API¶

To specify details about how Snowflake interacts with the Git repository API,
you’ll need to create an API integration.

Someone setting up a Snowflake account to use Git will specify the API
integration to use.

To create an API integration, you must use a role that has been granted the
following privileges:

  * CREATE INTEGRATION on the account

For more information, see [CREATE API INTEGRATION access control
requirements](../../sql-reference/sql/create-api-integration.html#label-
create-api-integration-access-control).

  * USAGE on the database and schema that contain the secret

  * USAGE on the secret that the integration references

When creating an API integration for a Git repository API, you must:

  * Specify `git_https_api` as the value of the API_PROVIDER parameter.

  * Specify, if authentication is required, a secret that contains the repository’s credentials as a value of the ALLOWED_AUTHENTICATION_SECRETS parameter. You can specify one of the following:

    * One or more Snowflake secrets (in a comma-separated list) that Snowflake can use when authenticating with the repository

    * The string `'all'` (case insensitive) to specify that any secret may be used

    * The string `'none'` (case insensitive) to specify that no secrets may be used

SQL:

    

You can use the [CREATE API INTEGRATION](../../sql-reference/sql/create-api-
integration) command to create an API integration that specifies details for
the Snowflake interaction with the Git repository API.

Code in the following example creates an API integration called
`git_api_integration`:

    
    
    USE ROLE securityadmin;
    CREATE ROLE myco_git_admin;
    GRANT CREATE INTEGRATION ON ACCOUNT TO ROLE myco_git_admin;
    
    USE ROLE myco_db_owner;
    GRANT USAGE ON DATABASE myco_db TO ROLE myco_git_admin;
    GRANT USAGE ON SCHEMA myco_db.integrations TO ROLE myco_git_admin;
    
    USE ROLE myco_secrets_admin;
    GRANT USAGE ON SECRET myco_git_secret TO ROLE myco_git_admin;
    
    USE ROLE myco_git_admin;
    USE DATABASE myco_db;
    USE SCHEMA myco_db.integrations;
    
    CREATE OR REPLACE API INTEGRATION git_api_integration
      API_PROVIDER = git_https_api
      API_ALLOWED_PREFIXES = ('https://github.com/my-account')
      ALLOWED_AUTHENTICATION_SECRETS = (myco_git_secret)
      ENABLED = TRUE;
    

Copy

## Create a Git repository stage and clone the repository¶

To set up Snowflake to work with a Git repository, create a Git repository
stage to contain files fetched from the repository.

Note

Before beginning the steps in this section, consider first creating a secret
(if the remote repository requires authentication) and an API integration. You
might need both of these.

The Git repository stage specifies the following:

  * The repository’s origin

In Git, `origin` is shorthand for the remote repository’s URL. Use that URL
when setting up Snowflake to use a Git repository. The URL must use HTTPS. You
can retrieve the origin URL in the following ways:

    * In the GitHub user interface, to get the origin URL from the repository home page, select the Code button, and then copy the HTTPS URL from the box displayed beneath the button.

    * From the command line, use the `git config` command from within your local repository, as in the following example:
        
                $ git config --get remote.origin.url
        https://github.com/my-account/snowflake-extensions.git
        

Copy

For reference information about `git config`, see the [git
documentation](https://git-scm.com/docs/git-config).

  * Credentials, if needed, for Snowflake to use when authenticating with the repository

  * An API integration specifying details for Snowflake interaction with the repository API

To create a Git repository stage, you must use a role that has been granted
the following privileges:

  * CREATE GIT REPOSITORY on the schema that contains the repository

For more information, see [CREATE GIT REPOSITORY access control
requirements](../../sql-reference/sql/create-git-repository.html#label-create-
git-repository-access-control).

  * USAGE on the secret that contains credentials for authenticating with Git

  * USAGE on the API integration that the Git repository stage references

You can create a Git repository stage by using either Snowsight or SQL.

SQLSnowsight

You can use the [CREATE GIT REPOSITORY](../../sql-reference/sql/create-git-
repository) command to create a Git repository stage.

Note

Before creating a local repository, you’ll need to create a secret (if the
remote repository requires authentication) and an API integration.

Code in the following example creates a Git repository stage called
`snowflake_extensions`. The stage specifies the `git_api_integration` API
integration and the `myco_git_secret` secret with credentials for
authenticating.

    
    
    USE ROLE securityadmin;
    GRANT CREATE GIT REPOSITORY ON SCHEMA myco_db.integrations TO ROLE myco_git_admin;
    
    USE ROLE myco_git_admin;
    
    CREATE OR REPLACE GIT REPOSITORY snowflake_extensions
      API_INTEGRATION = git_api_integration
      GIT_CREDENTIALS = myco_git_secret
      ORIGIN = 'https://github.com/my-account/snowflake-extensions.git';
    

Copy

You can use Snowsight to integrate a Git repository with Snowflake.

  1. Sign in to Snowsight.

  2. In the navigation menu, select Data » Databases.

  3. In the object explorer, select the database and schema that you want to contain the Git repository stage you’re creating.

  4. Select Create » Git Repository.

  5. In the Create Git Repository dialog, for Repository Name, enter a name that will uniquely identify this repository in the schema.

For naming guidelines, see [Identifier requirements](../../sql-
reference/identifiers-syntax).

  6. For Origin, enter the remote repository’s origin URL.

  7. From the API Integration drop-down menu, select the API integration to reference when creating the repository stage.

If you don’t have an API integration to use, select Create new API integration
in Worksheets to use SQL to create one. For more information, see Create an
API integration for interacting with the repository API and [CREATE API
INTEGRATION](../../sql-reference/sql/create-api-integration).

  8. Optional: For the Comment, enter text describing this integration for others.

  9. For Authentication, if the remote repository requires authentication, turn on the toggle.

     * If you turn on the toggle, from the Secret drop-down, select the secret that should be referenced by the Git integration to authenticate with the remote repository.

If you don’t have a secret to use, select Create new secret in Worksheets to
use SQL to create one. For more information, see Create a secret with
credentials for authenticating and [CREATE SECRET](../../sql-
reference/sql/create-secret).

  10. Select Create.

When you successfully create the integration, the repository appears beneath
the schema, in a Git Repositories directory. You’ll also see a page that lists
repository directories, branches, and tags.

