# Set up external access for Snowflake Notebooks¶

Feature — Generally Available

Generally available in Amazon Web Services (AWS), Microsoft Azure, and Google
Cloud Platform (GCP) commercial regions.

By default, Snowflake restricts network traffic requests from external
endpoints. In order to access external endpoints, you need to create an
[external network access integration](../../developer-guide/external-network-
access/external-network-access-overview). This topic describes how you can set
up external network access for your notebook.

External access integrations and their underlying network rules must be
created by an organization administrator.

## Create external access integrations (EAI)¶

To create an external access integration for notebooks, do the following:

  1. Create a network rule that defines a set of IP addresses or domains using the [CREATE NETWORK RULE](../../sql-reference/sql/create-network-rule) command.

  2. Create an external access integration that specifies the list of allowed network rules using the [CREATE EXTERNAL ACCESS INTEGRATION](../../sql-reference/sql/create-external-access-integration) command.

Note

Only an ACCOUNTADMIN or a role with the privilege to create EAIs can set them
up for specific external endpoints. For information on the required
privileges, see [Access control requirements](../../sql-reference/sql/create-
external-access-integration.html#label-create-external-access-integration-
privileges).

The following examples show how to set up external access for common data
science and machine learning sites.

Create an external access integration for PyPI:

    
    
    CREATE OR REPLACE NETWORK RULE pypi_network_rule
    MODE = EGRESS
    TYPE = HOST_PORT
    VALUE_LIST = ('pypi.org', 'pypi.python.org', 'pythonhosted.org',  'files.pythonhosted.org');
    
    CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION pypi_access_integration
    ALLOWED_NETWORK_RULES = (pypi_network_rule)
    ENABLED = true;
    

Copy

Create an external access integration for HuggingFace:

    
    
    CREATE OR REPLACE NETWORK RULE hf_network_rule
    MODE = EGRESS
    TYPE = HOST_PORT
    VALUE_LIST = ('huggingface.co', 'cdn-lfs.huggingface.co');
    
    CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION hf_access_integration
    ALLOWED_NETWORK_RULES = (hf_network_rule)
    ENABLED = true;
    

Copy

Allow all network access with one external access integration:

    
    
    CREATE OR REPLACE NETWORK RULE allow_all_rule
    MODE= 'EGRESS'
    TYPE = 'HOST_PORT'
    VALUE_LIST = ('0.0.0.0:443','0.0.0.0:80');
    
    CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION allow_all_integration
    ALLOWED_NETWORK_RULES = (allow_all_rule)
    ENABLED = true;
    

Copy

## Grant the privileges required to create external access integrations¶

After you create the EAIs, you must grant the USAGE privilege on the
integration to an account role.

The role used to create an EAI becomes the owner. As the owner, the role is
required to grant the USAGE privilege to other roles. To grant USAGE
privileges on the integrations, use the following commands:

    
    
    GRANT USAGE ON INTEGRATION pypi_access_integration TO ROLE my_notebook_role;
    GRANT USAGE ON INTEGRATION hf_access_integration TO ROLE my_notebook_role;
    GRANT USAGE ON INTEGRATION allow_all_integration TO ROLE my_notebook_role;
    

Copy

Note

It is important to grant the USAGE privilege on the integration to the role
that creates the notebooks. USAGE granted to the PUBLIC role will not work.
For detailed syntax, see [external network access](../../sql-
reference/sql/create-external-access-integration).

## Enable external access integrations (EAI)¶

After you create and provision EAIs, make sure to restart the notebook session
in order to see the access integrations you created in the external access
pane.

  1. Sign in to [Snowsight](../ui-snowsight).

  2. Select Projects » Notebooks.

  3. To access the external access configuration, select the [![more actions for worksheet](../../_images/snowsight-worksheet-vertical-ellipsis.png)](../../_images/snowsight-worksheet-vertical-ellipsis.png) on the top right of your notebook.

  4. Select Notebook settings, and then select the External access pane.

  5. In the list of external access integrations that are available, select the toggles next to each integration to enable or disable them.

To enable the new integrations, see Enable external access integrations (EAI).

## Use secrets with external access integrations¶

In most cases, APIs require an API key. To allow external access, use SQL to
associate a secret (such as the API key) with your notebook. To manually
associate a secret with a notebook, use the [ALTER NOTEBOOK … SET
SECRETS](../../sql-reference/sql/alter-notebook) command:

    
    
    ALTER NOTEBOOK <name>
     SET SECRETS = ('<secret_variable_name>' = <secret_name>);
    

Copy

To retrieve a secret after associating it with a notebook, see [Python API for
Secret Access](../../developer-guide/external-network-access/secret-api-
reference.html#label-python-api-secret-access).

## Additional resources¶

  * For detailed syntax, see [External network access overview](../../developer-guide/external-network-access/external-network-access-overview).

  * For additional examples of EAIs, see [External network access examples](../../developer-guide/external-network-access/external-network-access-examples) or [Setting up External Access for Snowflake Notebooks on Github](https://github.com/Snowflake-Labs/snowflake-demo-notebooks/blob/main/Access%20External%20Endpoints/Access%20External%20Endpoints.ipynb).

