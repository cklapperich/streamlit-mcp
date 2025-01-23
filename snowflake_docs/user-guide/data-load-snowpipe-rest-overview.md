# Overview of the Snowpipe REST endpoints to load data¶

This topic provides an overview of the usage details when calling the public
REST endpoints to load data and retrieve load history reports.

## Authentication¶

Calls to the public Snowpipe REST endpoints use key-based authentication,
rather than the typical username/password authentication, because the
ingestion service does not maintain client sessions.

To follow the general principle of least privilege, we recommend creating a
separate user and role to use for ingesting files using a pipe. The user
should be created with this role as its default role, and the role should have
the minimum set of permissions needed to insert files into the target table
for data loading.

## Process flow¶

Your client application calls a public REST endpoint with a list of data
filenames and a referenced pipe name (Java and Python SDKs are provided for
your convenience). If new data files matching the list are discovered in the
stage, they are queued for loading. Snowflake-provided compute resources load
data from the queue into a Snowflake table based on parameters defined in the
pipe.

The following diagram shows the Snowpipe REST API process flow:

[![Snowpipe Process Flow](../_images/data-load-snowpipe-
flow.png)](../_images/data-load-snowpipe-flow.png)

  1. Data files are copied to an internal (Snowflake) or external (Amazon S3, Google Cloud Storage, or Microsoft Azure) stage.

  2. A client calls the `insertFiles` endpoint with a list of files to ingest and a defined pipe.

The endpoint moves these files to an ingest queue.

  3. A Snowflake-provided virtual warehouse loads data from the queued files into the target table based on parameters defined in the specified pipe.

## Workflow¶

This section provides a high-level overview of the setup and load workflow.

### Configuring Snowpipe¶

  1. Create a named stage object where your data files will be staged. Snowpipe supports both internal (Snowflake) stages and external stages, i.e. S3 buckets.

  2. Create a pipe object using [CREATE PIPE](../sql-reference/sql/create-pipe).

  3. Configure security for the user who will execute the continuous data load. If you plan to restrict Snowpipe data loads to a single user, you only need to configure key pair authentication for the user once. After that, you only need to grant access control privileges on the database objects used for each data load.

  4. Install a client SDK (Java or Python) for calling the Snowpipe public REST endpoints.

### Using the Snowpipe REST API to load data¶

#### Option 1: Using a client to call the REST API¶

Use a client to call the REST API. Java and Python SDK sample code is
provided. For more information, see [Option 1: Loading data using the Snowpipe
REST API](data-load-snowpipe-rest-load).

  1. Call a REST endpoint with a list of files to load when staged.

  2. Retrieve the load history.

#### Option 2: Using AWS Lambda to call the REST API¶

Automate Snowpipe by using an AWS Lambda function to call the REST API. A
Lambda function can call the REST API to load data from files stored in Amazon
S3 only. For more information, see [Option 2: Automating Snowpipe with AWS
Lambda](data-load-snowpipe-rest-lambda).

  1. Create an AWS Lambda function that calls the Snowpipe REST API to load data from your external (i.e. S3) stage .

  2. Retrieve the load history.

