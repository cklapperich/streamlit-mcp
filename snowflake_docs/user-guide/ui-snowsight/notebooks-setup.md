# Set up Snowflake Notebooks¶

Feature — Generally Available

Generally available in Amazon Web Services (AWS), Microsoft Azure, and Google
Cloud Platform (GCP) commercial regions.

Snowflake Notebooks are first-class objects stored within a schema under a
database. They can run on two compute architectures: warehouses and
containers. This topic provides steps to set up your account as an
administrator and start using Snowflake Notebooks.

## Administrator setup¶

To set up your organization using Snowflake Notebooks, perform these steps:

  * Review account and deployment requirements.

  * Accept the Anaconda terms to import libraries.

  * Create resources and grant privileges to create notebooks.

  * (Optional) Meet the prerequisites for using private notebooks.

### Review account and deployment requirements¶

Ensure that `*.snowflake.app` is on the allowlist in your network, including
content filtering systems, and can connect to Snowflake. When this domain is
on the allowlist, your apps can communicate with Snowflake servers without any
restrictions.

In addition, to prevent any issues connecting to the Snowflake backend, ensure
that WebSockets are not blocked in your network configuration.

### Accept the Anaconda terms to import libraries¶

Before you start using the packages provided by Anaconda inside Snowflake, you
must acknowledge the [External Offerings
Terms](https://www.snowflake.com/legal/external-offering-terms/).

Note

You must use the ORGADMIN role to accept the terms. You only need to accept
the [External Offerings Terms](https://www.snowflake.com/legal/external-
offering-terms/) once for your Snowflake account. If you do not have the
ORGADMIN role, see [Enabling the ORGADMIN role in an
account](../organizations-gs.html#label-enabling-orgadmin-role-for-account).

  1. Sign in to Snowsight.

  2. Select Admin » Billing & Terms.

  3. In the Anaconda section, select Enable.

  4. In the Anaconda Packages dialog, click the link to review the [External Offerings Terms page](https://www.snowflake.com/legal/external-offering-terms/).

  5. If you agree to the terms, select Acknowledge & Continue.

If you encounter an error when attempting to accept the [External Offerings
Terms](https://www.snowflake.com/legal/external-offering-terms/), it may be
due to missing information in your user profile, such as a first name, last
name, or email address.

### Create resources and grant privileges¶

To create a notebook, a role needs privileges on the following resources:

  * [CREATE NOTEBOOK](../../sql-reference/sql/create-notebook) privilege on a location

  * USAGE privilege on compute resources

  * (Optional) USAGE privilege on external access integrations (EAIs)

See Template for Notebooks setup for example scripts of creating and granting
permissions on these resources.

#### Location¶

The location is where a notebook object is stored. The end user can query any
database and schema their role has access to.

  * To change the context to a different database or schema, use the [USE DATABASE](../../sql-reference/sql/use-database) or [USE SCHEMA](../../sql-reference/sql/use-schema) commands in a SQL cell.

In the container runtime, the role creating the notebook also requires the
[CREATE SERVICE](../../sql-reference/sql/create-service) privilege on the
schema.

Privilege | Object  
---|---  
USAGE | Database  
USAGE | Schema  
CREATE NOTEBOOK | Schema  
CREATE SERVICE | Schema  
  
Roles that own a schema automatically have the privilege to create notebooks
within that schema, because owners can create any type of object, including
notebooks.

Privilege | Object  
---|---  
USAGE | Database  
OWNERSHIP | Schema  
  
### Compute resources¶

In the warehouse runtime, both a notebook’s engine and Python processes from
the code authored in the notebook run on the Notebook warehouse, but SQL
queries and Snowpark push down queries run on the Query warehouse. The owner
role of the notebook requires the USAGE privilege on both warehouses.

If a notebook runs on container runtime, the role needs the USAGE privilege on
a compute pool in lieu of the Notebook warehouse. Compute pools are CPU-based
or GPU-based virtual machines managed by Snowflake. When creating a compute
pool, set the MAX_NODES parameter to greater than one because each notebook
will require one full node to run. For information, see [Snowpark Container
Services: Working with compute pools](../../developer-guide/snowpark-
container-services/working-with-compute-pool).

Privilege | Object  
---|---  
USAGE | Notebook warehouse or compute pool  
USAGE | Query warehouse  
  
### External access integrations (optional)¶

If you allow certain roles to access an external network, use the ACCOUNTADMIN
role to set up and grant the USAGE privilege on external access integrations
(EAIs). EAIs allow access to specific external endpoints so your teams can
download data and models, send API requests and responses, log in to other
services, etc. For notebooks running on container runtime, EAIs also allow
your teams to install packages from repositories such as PyPi and Hugging
Face.

For details on how to set up EAI for your notebook, see [Set up external
access for Snowflake Notebooks](notebooks-external-access).

Privilege | Object  
---|---  
USAGE | External access integration  
  
### Template for Notebooks setup¶

Because notebooks are objects with role-based creation and ownership
privileges, you can configure access to the Notebooks feature to align with
your organization and team needs. Here are a few examples:

#### Allow everyone to create notebooks in a specific location¶

The following steps outline how to configure access for creating notebooks in
a specific location by granting usage on a database and schema. Alternatively,
you can enable private notebooks, which do not require these access grants.
For more information about private notebooks, see [Private
notebooks](notebooks-private).

Replace <database> and <database.schema> with the specific database and schema
where you want to create your notebooks:

    
    
    ----------------------------------
    --       Location Setup         --
    ----------------------------------
    GRANT USAGE ON DATABASE <database> TO ROLE PUBLIC;
    GRANT USAGE ON SCHEMA <database.schema> TO ROLE PUBLIC;
    GRANT CREATE NOTEBOOK ON SCHEMA <database.schema> TO ROLE PUBLIC;
    
    -- For Notebooks on Container runtime, run the following:
    GRANT CREATE SERVICE ON SCHEMA <database.schema> TO ROLE PUBLIC;
    
    ----------------------------------
    --    Compute Resource Setup    --
    ----------------------------------
    GRANT USAGE ON WAREHOUSE <warehouse> TO ROLE PUBLIC;
    
    -- For Notebooks on Container runtime:
    CREATE COMPUTE POOL CPU_XS
      MIN_NODES = 1
      MAX_NODES = 15
      INSTANCE_FAMILY = CPU_X64_XS;
    
    CREATE COMPUTE POOL GPU_S
      MIN_NODES = 1
      MAX_NODES = 5
      INSTANCE_FAMILY = GPU_NV_S;
    
    GRANT USAGE ON COMPUTE POOL CPU_XS TO ROLE PUBLIC;
    GRANT USAGE ON COMPUTE POOL GPU_S TO ROLE PUBLIC;
    
    -------------------------------------
    -- Optional: External Access --
    -------------------------------------
    
    -- Example EAI
    CREATE OR REPLACE NETWORK RULE allow_all_rule
    MODE = 'EGRESS'
    TYPE = 'HOST_PORT'
    VALUE_LIST = ('0.0.0.0:443','0.0.0.0:80');
    
    CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION allow_all_integration
    ALLOWED_NETWORK_RULES = (allow_all_rule)
    ENABLED = true;
    
    GRANT USAGE ON INTEGRATION allow_all_integration TO ROLE PUBLIC;
    

Copy

#### Create a dedicated role¶

If you only want specific users to create notebooks (assuming they do not
already OWN any schemas), you can create a dedicated role for controlling
access. For example:

    
    
    CREATE ROLE notebooks_rl;
    

Copy

Grant the ROLE notebook_rl to specific users. Then, use the above script to
create resources and grant permissions to this role (replace ROLE PUBLIC with
ROLE notebook_rl).

#### Notebook engine¶

The notebook engine (“kernel”) and Python processes run on the Notebook
warehouse. Snowflake recommends that you start with an X-Small warehouse to
minimize credit consumption.

While you are using the notebook (for example, editing code, running,
reordering, or deleting cells), or if the notebook remains active within its
idle timeout setting, an [EXECUTE NOTEBOOK](../../sql-reference/sql/execute-
notebook) query will run continuously to indicate that the notebook engine is
active and a notebook session is in use. You can check the status of this
query in Query history. While [EXECUTE NOTEBOOK](../../sql-
reference/sql/execute-notebook) is running, the Notebook warehouse is also
running. When [EXECUTE NOTEBOOK](../../sql-reference/sql/execute-notebook)
finishes, if there are no other queries or jobs running on the warehouse, it
will shut down according to its auto-suspend policy.

To end the [EXECUTE NOTEBOOK](../../sql-reference/sql/execute-notebook) query
(end the notebook session), follow these steps:

  1. Select Active or select End session from the Active drop-down menu.

  2. In Query history, find the corresponding [EXECUTE NOTEBOOK](../../sql-reference/sql/execute-notebook) query and select Cancel query.

  3. Let the notebook time out due to inactivity based on its idle time setting. If the [STATEMENT_TIMEOUT_IN_SECONDS](../../sql-reference/parameters.html#label-statement-timeout-in-seconds) and [STATEMENT_QUEUED_TIMEOUT_IN_SECONDS](../../sql-reference/parameters.html#label-statement-queued-timeout-in-seconds) parameters on the Notebook warehouse are set to a small value, the notebook could shut down quickly or fail to start, regardless of user activity.

#### Queries¶

SQL and Snowpark queries (for example, session.sql) are pushed down to the
Query warehouse, which is used on demand. When the SQL and Snowpark queries
finish running, the Query warehouse suspends if no other jobs are running on
it outside the notebook. Select a warehouse size that best fits your query
performance needs. For example, you might want to run large SQL queries or
perform compute-intensive operations using Snowpark Python that require a
larger warehouse. For operations that require high memory usage, consider
using a [Snowpark-optimized warehouse](../warehouses-snowpark-optimized).

You can change the Query warehouse in Notebook Settings. Alternatively, you
can run the following command in any SQL cell in the notebook to change the
Query warehouse for all subsequent queries in the current notebook session:

    
    
    USE WAREHOUSE <warehouse_name>;
    

Copy

![Notebook compute diagram](../../_images/notebook-compute-diagram1.png)

#### Idle time and reconnection¶

Each notebook has an idle time property called IDLE_AUTO_SHUTDOWN_TIME_SECONDS
with a default value of 30 minutes. You can configure the idle time for each
notebook in Snowsight.

>   1. Sign in to [Snowsight](../ui-snowsight).
>
>   2. Select Projects » Notebooks.
>
>   3. Select the vertical ellipsis [![more actions for
> worksheet](../../_images/snowsight-worksheet-vertical-
> ellipsis.png)](../../_images/snowsight-worksheet-vertical-ellipsis.png) menu
> to configure a new time.
>
>   4. Select Notebook settings.
>
>   5. Manually restart the session for the new idle time to take effect.
>
>

Idle time accumulates whenever there is no user activity, such as editing
code, running cells, reordering cells, or deleting cells. Each time you resume
activity, the idle time resets. Once the idle time reaches the timeout
setting, the notebook session automatically shuts down.

Before idle timeout, your notebook session will remain active until the idle
timeout period is reached, even if you refresh the page, visit other parts of
Snowsight, or shut down or sleep your computer. When you reopen the same
notebook, you reconnect to the same session, with all session states and
variables preserved, allowing you to continue working seamlessly. Note,
however, that the state of your Streamlit widgets will not be retained.

Each individual user running the same notebook has their own independent
session. They do not interfere with one another.

#### Recommendations for optimizing cost¶

As an account administrator, consider the following recommendations to control
the cost of running notebooks:

  * Ask your teams to use the same warehouse (X-Small is recommended) as a dedicated “Notebook warehouse” for running the notebook sessions to increase concurrency. Note that this might lead to slower session starts (queued on warehouse) or out-of-memory errors if too many notebooks are to be executed simultaneously.

  * Allow your teams to use a warehouse with a lower [STATEMENT_TIMEOUT_IN_SECONDS](../../sql-reference/parameters.html#label-statement-timeout-in-seconds) value to run notebooks. This warehouse parameter controls how long any queries can last, including notebook sessions. For example, if the parameter is set to 10 minutes, the notebook session can run for a maximum of 10 minutes, regardless of whether the user is active in the notebook session during that time.

  * Ask your teams to end their notebook sessions when they do not intend to actively work in the session.

  * Ask your teams to minimize the idle timeout setting (for example, to 15 minutes) if they do not need the session to run for an extended period of time.

  * Alternatively, raise a support ticket to set a default value for idle time that applies to your entire account. This value can still be overridden at the notebook level by the notebook owner.

## Prerequisites for using private notebooks¶

In Snowsight, you can create a private, user-owned notebook. Before you create
and use private notebooks, an administrator with the ACCOUNTADMIN role must
complete the following tasks:

  1. Enable the personal database feature either at the account level or for specific users. Personal databases are Snowflake objects that make it possible for notebooks to behave as private notebooks. For information about completing this task, see the following sections:

     * Enabling and disabling private notebooks for the account

     * Enabling and disabling private notebooks for individual users

  2. If necessary, set secondary roles appropriately for users who are going to create private notebooks. For information about completing this task, which might depend on the enablement of recent BCR bundles, see [Activating all secondary roles for private notebook users](notebooks-private.html#label-activate-secondary-roles).

Important

After the administrator has enabled personal databases, affected users must
sign out and sign back in to see the new user interface behavior.

For details about private notebooks, see [Private notebooks](notebooks-
private).

### Enabling and disabling private notebooks for the account¶

To enable private notebooks on a Snowflake account, use an [ALTER
ACCOUNT](../../sql-reference/sql/alter-account) command that sets the
ENABLE_PERSONAL_DATABASE parameter to TRUE. For example:

    
    
    ALTER ACCOUNT SET ENABLE_PERSONAL_DATABASE = TRUE;
    

Copy

You cannot alter a different account; you can only alter the current account.
For more information about this command, see [ALTER ACCOUNT](../../sql-
reference/sql/alter-account).

If you need to disable private notebooks for the account, run the same command
but set the parameter to FALSE. For example:

    
    
    ALTER ACCOUNT SET ENABLE_PERSONAL_DATABASE = FALSE;
    

Copy

To check the current value of the ENABLE_PERSONAL_DATABASE parameter, run the
following [SHOW PARAMETERS](../../sql-reference/sql/show-parameters) command:

    
    
    SHOW PARAMETERS LIKE 'ENABLE_PERSONAL_DATABASE' IN ACCOUNT;
    

Copy

After the administrator enables the parameter for the account, a user must
sign out and sign back in. Then the user can check that the personal database
has been created by running a [USE DATABASE](../../sql-reference/sql/use-
database) command:

    
    
    USE DATABASE USER$;
    

Copy

You can name the current user explicitly by specifying the `USER$` prefix
followed by the login username. For example:

    
    
    USE DATABASE USER$bobr;
    

Copy

These commands succeed when the personal database for the current user exists.
The USE DATABASE command returns an error if the personal database does not
exist (because the prerequisite tasks were not completed) or if it is not the
current user’s personal database. For example, if `jlap` is not the current
user, the following message appears:

    
    
    USE DATABASE USER$jlap;
    

Copy

    
    
    ERROR: Insufficient privileges to operate on database 'USER$JLAP'
    

Note

  * Personal databases do not have a specific owner; they are system-owned objects.

  * You cannot create personal databases yourself:

    * They are “lazily created” in the background for existing users when the account is enabled for private notebooks. The first time a user runs a command with explicit USER$ name resolution, the personal database is created. For example, running the command USE DATABASE USER$ results in lazy creation of the personal database for the current user.

### Enabling and disabling private notebooks for individual users¶

Administrators may want specific users in the account to have personal
database access, rather than all users in the account. To enable access for
given users, use the [ALTER USER](../../sql-reference/sql/alter-user) command
to set the [ENABLE_PERSONAL_DATABASE](../../sql-
reference/parameters.html#label-enable-personal-database) parameter to TRUE
for those users. For example, enable access for three users:

    
    
    ALTER USER bobr SET ENABLE_PERSONAL_DATABASE = TRUE;
    ALTER USER amya SET ENABLE_PERSONAL_DATABASE = TRUE;
    ALTER USER jlap SET ENABLE_PERSONAL_DATABASE = TRUE;
    

Copy

If you enable personal databases at the account level, you can disable
personal databases for individual users, as needed. To disable users, run the
same command but set the parameter to FALSE. For example:

    
    
    ALTER USER jlap SET ENABLE_PERSONAL_DATABASE = FALSE;
    

Copy

If user `jlap` specifies the `USER$` prefix in any command, the command will
fail because the personal database does not exist.

    
    
    NotebookSqlException: Failed to fetch a pandas Dataframe. The error is: 060109 (0A000): Personal Database is not enabled for user JLAP.
    Please contact an account administrator to enable it and try again.
    

Note

If you enable and then disable personal databases for a specific user, the
user loses access to the personal database that was created but the database
continues to exist.

## Get started using notebooks by adding data¶

Before you get started using Snowflake Notebooks, add data to Snowflake.

You can add data to Snowflake in several ways:

  * Add data from a CSV file to a table using the web interface. See [Load data using the web interface](../data-load-web-ui).

  * Add data from external cloud storage:

    * To load data from Amazon S3, see [Bulk loading from Amazon S3](../data-load-s3).

    * To load data from Google Cloud Storage, see [Bulk loading from Google Cloud Storage](../data-load-gcs).

    * To load data from Microsoft Azure, see [Bulk loading from Microsoft Azure](../data-load-azure).

  * Add data in bulk programmatically. See [Bulk loading from a local file system](../data-load-local-file-system).

You can also add data in other ways. See [Overview of data loading](../data-
load-overview) for complete details.

