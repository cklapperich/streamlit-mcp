# Working with Amazon S3-compatible storage¶

This topic provides information about accessing Amazon S3-compatible storage
from Snowflake.

A storage application or device is Amazon S3-compatible if it provides an
application programming interface (API) that is compliant with the industry-
standard [Amazon Simple Storage Service (S3) REST
API](https://docs.aws.amazon.com/AmazonS3/latest/API/Welcome.html). The Amazon
S3 REST API enables CRUD operations and administrative actions on storage
buckets and objects.

With Snowflake, you can use an external stage to connect to a growing number
of S3-compatible storage solutions, including on-premises storage and devices
that exist outside of the public cloud. The external stage stores an
S3-compliant API endpoint, bucket name and path, and credentials. To let users
load and unload data from and to your storage locations, you grant privileges
on the stage to roles.

You can use Snowflake support for Amazon S3-compatible storage to perform
tasks such as:

  * Querying data from an external stage without loading the data into Snowflake. For more information, see Extending your data lake using external tables.

  * Reading and processing unstructured data. To learn more, see [Downloading from an internal stage](unstructured-intro.html#label-data-load-processing-unstructured-data).

  * Copying files in S3-compatible storage from one location to another using the [COPY FILES](../sql-reference/sql/copy-files) command.

Note

You can also create an external volume for S3-compatible storage to query an
externally managed Apache Iceberg™ table. For more information, see [Configure
an external volume for S3-compatible storage](tables-iceberg-s3-compatible).

## Cloud platform support¶

This feature is available to Snowflake accounts hosted on the following
supported [cloud platforms](intro-cloud-platforms):

  * Amazon Web Services

  * Google Cloud

  * Microsoft Azure

## Requirements for S3-compatible storage¶

An S3-compatible API endpoint for Snowflake must meet the following
requirements:

  * Highly compliant with the S3 API and able to pass our [public test suite](https://github.com/snowflakedb/snowflake-s3compat-api-test-suite) (in GitHub). If the endpoint does not behave like S3, it cannot work with Snowflake.

  * Supported by your third-party storage provider as a Snowflake S3-compatible tested and compliant service. For a list of vendors that have tested at least some of their products and found them to work with Snowflake, see Vendor support for S3-compatible storage.

  * Accessible from the public cloud where your Snowflake account is hosted.

  * Highly available and performant to serve analytics needs.

  * Configured to use virtual-hosted-style requests. For more information, see [Virtual hosting of buckets](https://docs.aws.amazon.com/AmazonS3/latest/userguide/VirtualHosting.html) in the Amazon S3 documentation.

  * Configured to use HTTPS communication with a valid TLS certificate.

  * Configured to use direct credentials.

  * Does not contain a port number. For example, the endpoint mystorage.com:3000 is not supported.

Important

Amazon S3-compatible endpoints are not automatically enabled for all accounts.
To enable endpoints, contact the Snowflake account team or [Snowflake
Support](https://docs.snowflake.com/user-guide/contacting-support). Before you
send a request, verify the endpoints by using our [public test
suite](https://github.com/snowflakedb/snowflake-s3compat-api-test-suite) (in
GitHub).

Provide the following information with your request:

  * Your Snowflake account name and cloud region deployment.

  * The endpoint URL (for example, `my-s3-endpoint.company.com`).

  * The software or hardware vendor that provides the endpoint.

## Creating an external stage for S3-compatible storage¶

To create an external stage for S3-compatible storage, create a named
[external stage](data-load-overview.html#label-data-load-overview-external-
stages) by using the [CREATE STAGE](../sql-reference/sql/create-stage)
command. You can use an external stage to perform actions such as listing
files, loading data, and unloading files.

Optionally, add a [directory table](data-load-dirtables) to the external
stage. You can query a directory table to retrieve file URLs to access files
in the referenced storage, as well as other metadata.

Note

When you add a directory table, you must set the AUTO_REFRESH parameter to
FALSE. The metadata for S3-compatible external stages cannot be refreshed
automatically.

The following example creates an external stage named `my_s3_compat_stage`
that points to the bucket and path named `my_bucket/files/` at the endpoint
`mystorage.com`. The AWS_KEY_ID and AWS_SECRET_KEY values used in this example
are for illustration purposes only.

    
    
    CREATE STAGE my_s3compat_stage
      URL = 's3compat://my_bucket/files/'
      ENDPOINT = 'mystorage.com'
      CREDENTIALS = (AWS_KEY_ID = '1a2b3c...' AWS_SECRET_KEY = '4x5y6z...')
    

Copy

## Loading and unloading data¶

You can load and unload data using an external stage configured for
S3-compatible storage. The following features work with S3-compatible storage:

  * Bulk data loading using the [COPY INTO <table>](../sql-reference/sql/copy-into-table) command.

For example, load data into table `t1` from all files located in the `load`
subpath in the bucket and path defined in a stage named `my_s3compat_stage`:

    
        COPY INTO t1
      FROM @my_s3compat_stage/load/;
    

Copy

  * [Calling Snowpipe REST endpoints to continuously load data](data-load-snowpipe-rest-overview).

For sample programs, see [Option 1: Loading data using the Snowpipe REST
API](data-load-snowpipe-rest-load).

  * Data unloading using the [COPY INTO <location>](../sql-reference/sql/copy-into-location) command.

For example, unload data from table `t2` into files in the `unload` subpath in
the bucket and path defined in a stage named `my_s3compat_stage`:

    
        COPY INTO @my_s3compat_stage/unload/
      FROM t2;
    

Copy

## Extending your data lake using external tables¶

You can use external tables with S3-compatible storage to query data without
first loading it into Snowflake. This section briefly covers how to create and
query an external table that references a location on an external stage
configured for S3-compatible storage.

Start by creating an external table using [CREATE EXTERNAL TABLE](../sql-
reference/sql/create-external-table) that reference an S3-compatible external
stage.

Note

The metadata for these external tables cannot be refreshed automatically. The
`AUTO_REFRESH = TRUE` parameter setting is not supported. You must manually
refresh the metadata by executing an [ALTER EXTERNAL TABLE … REFRESH](../sql-
reference/sql/alter-external-table) command to register any added or removed
files.

The following example creates an external table named `et` that references
subpath `path1` in a stage named `my_s3compat_stage`. The files in the `path1`
subpath are in the Apache Parquet format.

    
    
    CREATE EXTERNAL TABLE et
     LOCATION=@my_s3compat_stage/path1/
     AUTO_REFRESH = FALSE
     REFRESH_ON_CREATE = TRUE
     FILE_FORMAT = (TYPE = PARQUET);
    

Copy

After you create an external table for S3-compatible storage, you can query
it. For example, query the `value` column in the external table created
previously:

    
    
    SELECT value FROM et;
    

Copy

Query performance varies depending on network and application or device
performance. If performance is critical, create a [materialized view](views-
materialized) on the external table. Materialized views are pre-computed, so
querying a materialized view is faster than executing a query against the base
table of the view.

## Vendor support for S3-compatible storage¶

You can use devices or applications that have an S3-compliant API with
Snowflake. However, your storage service provider is responsible for ensuring
compliance.

The following vendors have indicated to Snowflake that they have tested at
least some of their products and found them to work with Snowflake:

  * Backblaze

  * Cloudflare

  * Cloudian

  * Cohesity

  * Dell

  * Hitachi Content Platform

  * IBM Storage Ceph

  * IDrive e2

  * MinIO

  * NetApp (StorageGRID)

  * Nutanix

  * PureStorage

  * Scality

  * Wasabi

This list is provided for convenience only. Snowflake does not test external
products to validate compatibility and cannot fix issues in products sold by
third-party vendors. If you have questions about whether or how your hardware
or software with an S3 API works with Snowflake, contact the vendor directly.

## Testing your S3-compatible API¶

If you are a hardware or software developer who has created an S3-compatible
API, you can use our [public test
suite](https://github.com/snowflakedb/snowflake-s3compat-api-test-suite) (in
GitHub) to test whether your S3 API works with Snowflake. The test suite looks
for obvious mismatches between your implementation and what Snowflake expects
from S3. However, there might be cases where the tests don’t identify
incompatibility.

If you’re a customer and you want to test your own devices, contact your
vendor to run these tests. You can also run these public tests on your devices
to assess compatibility.

