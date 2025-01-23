# Snowflake DevOps¶  
  
Snowflake DevOps empowers developers to streamline and automate the software
development lifecycle for their Snowflake environments. With an emphasis on
best practices in CI/CD, deployment automation, and infrastructure management,
Snowflake DevOps tools and practices ensure smooth integration between
development and operational tasks.

This guide offers insights into leveraging Snowflake’s capabilities to enhance
collaboration, maintain quality, and achieve efficient software delivery
across your Snowflake projects.

## What is Snowflake DevOps?¶

Snowflake provides an integrated approach to accelerate development lifecycles
and improve overall productivity for data teams. This approach integrates Git
version control, Python APIs, declarative object management, and seamless
CI/CD automation.

Git repository for all of your sources | By keeping your data assets, code, and configurations centrally managed and version-controlled, you can ensure consistency, simplify collaboration, and streamline rollbacks if needed. Using your Git repository from Snowflake lets you do all of this within Snowflake’s secure perimeter, which is crucial for production-ready environments.  
---|---  
Declarative syntax | By embracing a declarative approach to database change management — defining and managing Snowflake objects using Python or SQL — you eliminate the need for complex scripts while promoting readability.  
CI/CD automation | You can integrate with your existing CI/CD tools or Snowflake CLI to automatically execute commands and orchestrate your entire pipeline for efficient and reliable deployments.  
  
## What are the building blocks of Snowflake DevOps?¶

Snowflake offers several features that integrate to make DevOps tasks simpler
and more secure.

[CREATE OR ALTER <object>](../../sql-reference/sql/create-or-alter) | You can use the CREATE OR ALTER command to apply updates to your Snowflake objects and keep your account in sync with the infrastructure as code in Git. For more information, see Manage changes with declarative code and versioning.  
---|---  
[EXECUTE IMMEDIATE FROM](../../sql-reference/sql/execute-immediate-from) | With the EXECUTE IMMEDIATE FROM Snowflake command, you can execute SQL from a Git repository in Snowflake. The SQL script can be a Jinja2 template. For more information, see Parameterize scripts with Jinja templates.  
[Snowflake CLI](../snowflake-cli/index) | In scripts to drive your CI/CD pipeline, you can run Snowflake CLI commands to automate deployments, collaborate with version control, and integrate with other CI/CD tools. For more information, see Automate CI/CD jobs with GitHub Actions.  
[Python APIs](https://docs.snowflake.com/en/developer-guide/snowflake-python-api/reference/latest/index) | Using Snowflake’s Python APIs, you can manage Snowflake resources, including databases, schemas, tables, and tasks. For more information, see [Snowflake Python APIs: Managing Snowflake objects with Python](../snowflake-python-api/snowflake-python-overview).  
[Git in Snowflake](../git/git-overview) | You can fetch project config and data pipelines (schema, tables, scripts) from a Git repo to trigger the deployment workflow. For more information, see Streamline workflows by keeping assets in a Git repository connected with Snowflake.  
  
## Using Snowflake features in DevOps workflows¶

Using Snowflake with your existing tools, you can achieve the following DevOps
goals:

  * Streamline workflows by keeping assets in a Git repository connected with Snowflake.

You can take advantage of your existing Git investment by connecting the
repository to your Snowflake account. Once this connection is in place, with
the repository cloned locally in Snowflake itself, you can browse and execute
its code directly in Snowflake.

  * Minimize risk by maintaining separate environments for development, testing, and production.

By using separate Snowflake databases for each environment, you can minimize
the risk of unwanted changes affecting live systems. To more easily manage
deployments, you use scripts that parameterize the deployment process.

  * Manage database changes in a controlled and repeatable way for development, testing, and production by using scripts and declarative code.

  * Automate CI/CD jobs, including deployment of code and data, by using GitHub Actions.

Note

With the [Snowflake Extension for Visual Studio Code](../../user-guide/vscode-
ext), you can write and execute Snowflake SQL statements directly in VS Code.
By connecting VS Code with the same repository you’ve connected to Snowflake,
you can develop code locally in VS Code, keep your work in your Git
repository, and then access your code from within Snowflake.

### Streamline workflows by keeping assets in a Git repository connected with
Snowflake¶

You can ensure consistency, simplify collaboration, and streamline rollbacks
if needed by keeping your data assets, code, and configurations centrally
managed and version-controlled in a Git repository and using the repository
from Snowflake.

You can connect your Snowflake acccount with your Git repository so that
Snowflake can execute code in files cloned from the repository. The result is
a Git repository stage that represents a full clone of your repository. From
within Snowflake, you can access version-controlled files at a certain commit,
branch, or tag.

With the repository stage, you can create a Snowpark function or procedure
from a version controlled file and directly execute versioned SQL scripts with
EXECUTE IMMEDIATE FROM or use the Snowflake CLI to execute Python scripts.
This way, you can declaratively define database objects with SQL or Python and
then deploy those objects with a robust and easy to set up CI/CD pipeline.

![Diagram showing Git repository exchanging files with development tools and
Snowflake.](../../_images/devops-flow.png)

### Maintain separate environments for development, test, and production¶

By maintaining separate environments for development, testing, and production,
your teams can isolate development activities from the production environment,
reducing the likelihood of unintended consequences and data corruption.

When you separate workflows into multiple environments, each gets its own
Snowflake database — typically an identical copy.

#### Parameterize scripts with Jinja templates¶

To support deploying and executing code in essentially identical ways between
development and production environments, you can parameterize references to
environment specifics — such as which database to use during deployment. That
way, you can enable a CI/CD pipeline to choose the deployment target
appropriate to the environment.

To parameterize scripts, you can use Jinja2, a popular templating language
with features ranging from simple script parameterization to extensive and
modular scripting in a language similar to Python. Snowflake supports the
execution of templated SQL scripts with [EXECUTE IMMEDIATE FROM](../../sql-
reference/sql/execute-immediate-from). Alternatively, the Snowflake CLI allows
you to pass environment variables to Python scripts.

For changing a deployment target, for example, you’d replace the name of the
target database with a Jinja variable such as `{{ environment }}` in SQL
scripts, or an environment variable in Python scripts. This technique is shown
in the following SQL and Python code examples:

SQLPython

    
    
    CREATE OR ALTER TASK {{ environment }}.my_schema.my_task
      WAREHOUSE = my_warehouse
      SCHEDULE = '60 minute'
      AS select pi();
    

Copy

    
    
    import os
    from snowflake.core import Root, CreateMode
    from datetime import timedelta
    from snowflake.core.task import Task
    
    my_task = Task(
        name="my_task",
        warehouse="my_warehouse",
        definition="select pi()",
        schedule=timedelta(minutes=60)
    )
    root = Root(Session.builder.getOrCreate())
    tasks = root.databases[os.environ["environment"]].schemas["my_schema"].tasks
    tasks.create(my_task, mode=CreateMode.or_replace)
    

Copy

You can execute the parametrized scripts with the `snow git execute` command
of the Snowflake CLI. The CLI can execute scripts in SQL, Python, or a mix of
both directly from the repository stage within the guardrails and performance
features of your Snowflake account.

    
    
    snow git execute @my_git_repo/branches/main/path/to/my_scripts" \
        -D "environment='preprod'"
    

Copy

With [Snowflake CLI](../snowflake-cli/index), you can create, manage, update,
and view apps running on Snowflake across workloads.

### Manage changes with declarative code and versioning¶

You can more easily manage changes to your database resources with reusable
configuration files in your Git repository.

You can define database objects using the [CREATE OR ALTER
<object>](../../sql-reference/sql/create-or-alter) command, which creates the
object or alters it to match the definition specified by the command. By using
this command from a versioned file in a repository, you can more easily roll
back changes to a previous version: you merely execute a previous version of
the file.

SQLPython

    
    
    CREATE OR ALTER TABLE vacation_spots (
      city VARCHAR,
      airport VARCHAR,
      avg_temperature_air_f FLOAT,
      avg_relative_humidity_pct FLOAT,
      avg_cloud_cover_pct FLOAT,
      precipitation_probability_pct FLOAT
    ) data_retention_time_in_days = 1;
    

Copy

    
    
    from snowflake.core import Root
    from snowflake.core.table import PrimaryKey, Table, TableColumn
    
    my_table = root.databases["my_db"].schemas["my_schema"].tables["vacation_spots"].fetch()
    my_table.columns.append(TableColumn(name="city", datatype="varchar", nullable=False]))
    my_table.columns.append(TableColumn(name="airport", datatype="varchar", nullable=False]))
    my_table.columns.append(TableColumn(name="avg_temperature_air_f", datatype="float", nullable=False]))
    my_table.columns.append(TableColumn(name="avg_relative_humidity_pct", datatype="float", nullable=False]))
    my_table.columns.append(TableColumn(name="avg_cloud_cover_pct", datatype="float", nullable=False]))
    my_table.columns.append(TableColumn(name="precipitation_probability_pct", datatype="float", nullable=False]))
    
    my_table_res = root.databases["my_db"].schemas["my_schema"].tables["vacation_spots"]
    my_table_res.create_or_alter(my_table)
    

Copy

Note

You can also use the [Snowflake Python APIs](../snowflake-python-
api/snowflake-python-overview) and [Snowflake CLI](../snowflake-cli/index) to
manage Snowflake resources. If you prefer to do your data engineering work in
Python, Snowflake’s first-class Python API enables you do the same resource
management in the language you are most productive in.

### Automate CI/CD jobs with GitHub Actions¶

You can use [GitHub Actions](https://docs.github.com/en/actions) to automate
the jobs that constitute a CI/CD pipeline. With GitHub Actions or similar
CI/CD runners, you can define workflows that automate build, test, and
deployment tasks.

In these workflows, you can use other features of Snowflake and GitHub to put
the pieces together. You can do the following tasks:

  * Store your Snowflake credentials in a [GitHub secret](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions) so that GitHub Actions can connect to Snowflake.

  * Easily install the [Snowflake CLI](../snowflake-cli/index) and connect to Snowflake with the help of the native [Snowflake CLI GitHub action](https://github.com/Snowflake-Labs/snowflake-cli-action).

  * Execute commands in Snowflake, by using the Snowflake CLI. First, fetch the most recent changes from your Git repository to Snowflake. Next, execute your declarative and parametrized scripts to deploy your changes to an environment of your choice.

The GitHub Actions workflow excerpt in the following example deploys a
pipeline. The workflow authenticates with Snowflake by retrieving the needed
values from previously configured secrets.

To deploy the pipeline, the workflow executes the following `snow git`
commands:

  * `snow git fetch` pulls the latest from the GitHub repository to the cloned `my_git_repo` Git repository stage in Snowflake.

  * `snow git execute` runs Python and SQL scripts in the `/scripts` directory from the `main` branch of the repository.

    
    
    name: Deploy scripts to preprod
    
    on:
      push:
        branches:
          - main
    
    jobs:
      deploy:
        runs-on: ubuntu-latest
    
        env:
          SNOWFLAKE_CONNECTIONS_DEFAULT_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
          SNOWFLAKE_CONNECTIONS_DEFAULT_USER: ${{ secrets.SNOWFLAKE_USER }}
          SNOWFLAKE_CONNECTIONS_DEFAULT_PASSWORD: ${{ secrets.SNOWFLAKE_PASSWORD }}
    
        steps:
          - name: Checkout repository
            uses: actions/checkout@v4
    
          - name: Install snowflake-cli
            uses: Snowflake-Labs/snowflake-cli-action@v1.5
            with:
              cli-version: "latest"
              default-config-file-path: ".snowflake/config.toml"
    
          - name: Fetch repository changes
            run: snow git fetch my_git_repo
    
          - name: Deploy scripts to preprod environment
            run: snow git execute @my_git_repo/branches/main/scripts/* \
                -D "environment='preprod'"
    

Copy

## Getting started with Snowflake DevOps¶

For an interactive walk-through of using Snowflake DevOps, see the [Getting
Started with Snowflake
DevOps](https://quickstarts.snowflake.com/guide/getting_started_with_snowflake_devops/index.html#0)
Quickstart.

