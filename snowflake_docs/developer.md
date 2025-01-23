# Develop Apps and Extensions

Write applications that extend Snowflake, act as a client, or act as an
integrating component.

SNOWPARK API

## Run Python, Java, and Scala Code in Snowpark

Using Snowpark libraries and code execution environments, you can run Python
and other programming languages next to your data in Snowflake.

#### Build

Enable all data users to bring their work to a single platform with native
support for Python, Java, Scala, and more.

#### Secure

Apply consistent controls trusted by over 500 of the Forbes Global 2000 across
all workloads.

#### Optimize

Benefit from the Snowflake Data Cloud with super price/performance and near-
zero maintenance.

Get to know Snowpark API

Snowpark is the set of libraries and code execution environments that run
Python and other programming languages next to your data in Snowflake.
Snowpark can be used to build data pipelines, ML models, apps, and other data
processing tasks.

[Learn more](/en/developer-guide/snowpark/index)

![Snowpark example code](/images/snowpark-code-example-banner.svg)

### Code in Snowpark with multiple languages

Run custom Python, Java, or Scala code directly in Snowflake with Snowpark
user-defined functions (UDFs) and stored procedures. There are no separate
clusters to manage, scale, or operate.

PythonJavaScala

    
    
    from snowflake.snowpark import Session  
    from snowflake.snowpark.functions import col  
      
    # Create a new session, using the connection properties specified in a file.  
    new_session = Session.builder.configs(connection_parameters).create()  
      
    # Create a DataFrame that contains the id, name, and serial_number  
    # columns in the “sample_product_data” table.  
    df = session.table("sample_product_data").select(  
    col("id"), col("name"), col("name"), col("serial_number")  
    )  
      
    # Show the results   
    df.show()

[Developer Guide](/developer-guide/snowpark/python/index)[API
Reference](/developer-guide/snowpark/reference/python/index.html)

### Try Snowpark

Use the following quickstart tutorials to get a hands-on introduction to
Snowpark

[TUTORIALGetting Started with Data Engineering and ML using Snowpark for
PythonFollow this step-by-step guide to transform raw data into an interactive
application using Python with Snowpark and
Streamlit.](https://quickstarts.snowflake.com/guide/getting_started_with_dataengineering_ml_using_snowpark_python/index.html)

[TUTORIALData Engineering Pipelines with Snowpark PythonLearn how to build
end-to-end data engineering pipelines using Snowpark with
Python.](https://quickstarts.snowflake.com/guide/data_engineering_pipelines_with_snowpark_python)

[TUTORIALIntro to Machine Learning with Snowpark MLBuild an end-to-end ML
workflow from feature engineering to model training and batch inference using
Snowpark
ML.](https://quickstarts.snowflake.com/guide/intro_to_machine_learning_with_snowpark_ml_for_python/index.html)

Snowflake ML

## End-to-End Machine Learning in Snowflake

Pre-process data and train, manage, and deploy machine learning models all
within Snowflake.

[Developer GuideModel developmentTransform data and train models. Run your ML
pipeline within security and governance frameworks.](/en/developer-
guide/snowflake-ml/modeling)

[Developer GuideModel RegistrySecurely manage models and their metadata in
Snowflake regardless of origin.](/en/developer-guide/snowflake-ml/model-
registry/overview)

[Developer GuideFeature StoreMake creating, storing, and managing features for
machine learning workloads easier and more efficient.](/en/developer-
guide/snowflake-ml/feature-store/overview)

[Developer GuideDatasetsImmutable, versioned snapshots of data ready to be fed
to popular machine learning frameworks.](/en/developer-guide/snowflake-
ml/dataset)

[Developer GuideFramework ConnectorsProvide Snowflake data to PyTorch and
Tensorflow in their own formats.](/en/developer-guide/snowflake-ml/framework-
connectors)

[API ReferenceSnowpark MLThe Python API for Snowflake ML modeling and ML Ops
features.](/en/developer-guide/snowflake-ml/snowpark-ml)

Snowflake Python APIs

## Manage Snowflake resources, apps, and data pipelines

Create and manage Snowflake resources across data engineering, Snowpark,
Snowpark ML, and application workloads using a unified, first-class Python
API.

[Developer GuideSnowflake Python APIs overviewLearn about the Snowflake Python
APIs and how to get started.](/en/developer-guide/snowflake-python-
api/snowflake-python-overview)

[TutorialGetting started with the Snowflake Python APIsLearn the fundamentals
for creating and managing Snowflake resources using the Snowflake Python
APIs.](/en/developer-guide/snowflake-python-api/overview-tutorials)

[API ReferenceSnowflake Python APIs referenceReference for the Snowflake
Python APIs.](/en/developer-guide/snowflake-python-api/reference/latest/index)

NATIVE APPS FRAMEWORK

## Build secure data applications

Expand the capabilities of other Snowflake features by sharing data and
related business logic with other Snowflake accounts.

[TutorialDeveloping an Application with the Native Apps FrameworkFollow this
step-by-step tutorial to create a secure data application using the Native
Apps Framework.](/en/developer-guide/native-apps/tutorials/getting-started-
tutorial)

[Developer GuideAbout the Native Apps FrameworkLearn about the building blocks
of the Native Apps Framework, including key terms and
components.](/en/developer-guide/native-apps/native-apps-about)

[Developer GuideNative Apps Framework WorkflowsUnderstand the end-to-end
workflows for developing, publishing, and using applications.](/en/developer-
guide/native-apps/native-apps-workflow)

[SQL ReferenceNative Apps Framework CommandsView the SQL commands used to
create and use database objects supported by the Native Apps
Framework.](/en/sql-reference/commands-native-apps)

SNOWPARK CONTAINER SERVICES

## Deploy, manage, and scale containerized applications

Build atop a fully-managed service that comes with Snowflake security,
configuration, and operational best practices built in.

[Developer GuideSnowpark Container Services OverviewLearn about Snowpark
Container Services, including how it works and how to get
started.](/en/developer-guide/snowpark-container-services/overview)

[TutorialIntroductory tutorialsLearn the basics of creating a Snowpark
Container Services service.](/en/developer-guide/snowpark-container-
services/overview-tutorials)

[TutorialAdvanced tutorialsLearn advanced concepts such as service-to-service
communications.](/en/developer-guide/snowpark-container-services/overview-
advanced-tutorials)

STREAMLIT IN SNOWFLAKE

## Develop custom web apps for machine learning and data science

Securely build, deploy, and share Streamlit apps on Snowflake’s data cloud.

[Developer GuideAbout Streamlit in SnowflakeLearn about deploying Streamlit
apps by using Streamlit in Snowflake.](/en/developer-guide/streamlit/about-
streamlit)

[Developer GuideExample - Accessing Snowflake data from Streamlit in Snowflake
Learn how to securely access Snowflake data from a Streamlit
app.](/en/developer-guide/streamlit/example-access-snowflake)

[Developer GuideDeveloping a Streamlit app by using SnowsightLearn how to
quickly create, use, and share a Streamlit app in Snowsight.](/en/developer-
guide/streamlit/create-streamlit-ui)

FUNCTIONS AND PROCEDURES

## Extend Snowflake Capabilities

Enhance and extend Snowflake by writing procedures and user-defined functions.
In both cases, you write the logic in one of the supported programming
languages.

[Developer GuideStored Procedures or UDFsUnderstand key differences between
procedures and UDFs.](/en/developer-guide/stored-procedures-vs-udfs)

[Developer GuideStored ProceduresPerform scheduled or on-demand operations by
executing code or SQL statements.](/en/developer-guide/stored-
procedure/stored-procedures-overview)

[Developer GuideUser-Defined Functions (UDFs)Run logic to calculate and return
data for batch processing and integrating custom logic into
SQL.](/en/developer-guide/udf/udf-overview)

[Developer GuideDesign GuidelinesGeneral guidelines on security, conventions,
and more.](/en/developer-guide/udf-stored-procedure-guidelines)

[Developer GuidePackaging Handler CodeBuild a JAR file that contains the
handler and its dependencies. Reference the handler JAR on a
stage.](/en/developer-guide/udf-stored-procedure-building)

[Developer GuideWriting External FunctionsWriting external functions you can
use to invoke code on other systems.](/en/sql-reference/external-functions)

[Developer GuideLogging and TracingCapture log and trace messages in an event
table that you can query for analysis later.](/en/developer-guide/logging-
tracing/logging-tracing-overview)

[Developer GuideExternal Network AccessA guide for accessing network locations
external to Snowflake.](/en/developer-guide/external-network-access/external-
network-access-overview)

KAFKA AND SPARK CONNECTORS

## Integrate with Other Systems

Snowflake includes connectors with APIs for integrating with systems outside
Snowflake.

[User GuideSnowflake EcosystemIntegrate Snowflake with many other systems for
exchanging data, performing analysis, and more.](/en/user-guide/ecosystem)

[User GuideApache KafkaSend events from the Kafka event streaming platform to
Snowflake.](/en/user-guide/kafka-connector-overview)

[User GuideApache SparkIntegrate the Apache Spark analytics engine in Spark
workloads for data processing directly on Snowflake.](/en/user-guide/spark-
connector-overview)

DRIVERS

## Build a Client App with Drivers and APIs

Integrate Snowflake operations into a client app. In addition to the Snowpark
API, you can also use language and platform specific drivers.

### Drivers

Drivers allow you to connect from your code or apps to Snowflake. Using
languages such as C#, Go, and Python, you can write applications that perform
operations on Snowflake.

[Go Snowflake Driver](/developer-guide/golang/go-driver)[JDBC
Driver](/developer-guide/jdbc/jdbc)[.NET Driver](/developer-
guide/dotnet/dotnet-driver)[Node.js Driver](/developer-guide/node-js/nodejs-
driver)[ODBC Driver](/developer-guide/odbc/odbc)[PHP PDO Driver](/developer-
guide/php-pdo/php-pdo-driver)[Python Connector](/developer-guide/python-
connector/python-connector)

### RESTful API

Using the Snowflake RESTful SQL API, you can access and update data over HTTPS
and REST. For example, you can submit SQL statements, create and execute
stored procedures, provision users, and so on.

In the SQL REST API, you submit a SQL statement for execution in the body of a
POST request. You then check execution status and fetch results with GET
requests.

[DEVELOPER GUIDESnowflake SQL REST APIGet started with the Snowflake SQL REST
API.](/en/developer-guide/sql-api/index)

TOOLS

## Develop more efficiently

Work with Snowflake using tools that integrate well with your existing
workflow.

### Work with Snowflake from the command line

Use the command line to create, manage, update, and view apps running on
Snowflake across workloads.

[DEVELOPER GUIDEIntroducing Snowflake CLILearn about Snowflake CLI benefits
and how it differs from SnowSQL.](/en/developer-guide/snowflake-
cli-v2/introduction/introduction)

[DEVELOPER GUIDEInstalling Snowflake CLIInstall Snowflake CLI using common
package managers.](/en/developer-guide/snowflake-
cli-v2/installation/installation)

[REFERENCESnowflake CLI command referenceExplore commands for connecting,
managing apps, objects, and other Snowflake features.](/en/developer-
guide/snowflake-cli-v2/command-reference/overview)

### Use Git from Snowflake

Execute and use Git repository code directly from Snowflake.

[DEVELOPER GUIDEUsing a Git repository in SnowflakeIntegrate your Git
repository with Snowflake and fetch repository files to a repository stage
that is a Git client with a full clone of the repository.](/en/developer-
guide/git/git-overview)

[DEVELOPER GUIDESetting up Snowflake to use GitSet up Snowflake to securely
interact with your Git repository.](/en/developer-guide/git/git-setting-up)

[DEVELOPER GUIDEGit operations in SnowflakePerform common Git operations from
within Snowflake, including fetching files, viewing branches or tags, and
executing repository code.](/en/developer-guide/git/git-operations)

