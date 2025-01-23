# Automating continuous data loading using cloud messaging¶

Automated data loads leverage event notifications for cloud storage to inform
Snowpipe of the arrival of new data files to load. Snowpipe copies the files
into a queue, from which they are loaded into the target table in a
continuous, serverless fashion based on parameters defined in a specified pipe
object.

Note

  * Automated Snowpipe uses event notifications to determine when new files arrive in monitored cloud storage and are ready to load. Notifications identify the cloud storage event and include a list of the file names. They do not include the actual data in the files.

  * When a pipe is paused, event messages received for the pipe enter a limited retention period. The period is 14 days by default. If a pipe is paused for longer than 14 days, it is considered stale.

Event notifications received while a pipe is paused are retained for only a
limited period of time (14 days). As each notification reaches the end of this
period, Snowflake schedules it to be dropped from the internal metadata. If
the pipe is later resumed, Snowpipe may process notifications older than 14
days on a best effort basis. Snowflake cannot guarantee that these older
notifications are processed.

For information about resuming stale pipes, see [Managing Snowpipe](data-load-
snowpipe-manage).

The following table indicates which cloud storage services are supported for
automatically loading data into your Snowflake account using cloud storage
event notifications, based on the [cloud platform](intro-cloud-platforms) that
hosts your account:

Snowflake Account Host | Amazon S3 | Google Cloud Storage | Microsoft Azure Blob storage | Microsoft Data Lake Storage Gen2 | Microsoft Azure General-purpose v2  
---|---|---|---|---|---  
Amazon Web Services | ✔ | ✔ | ✔ | ✔ | ✔  
Google Cloud | ✔ | ✔ | ✔ | ✔ | ✔  
Microsoft Azure | ✔ | ✔ | ✔ | ✔ | ✔  
  
Important

Snowflake recommends that you enable cloud event filtering for Snowpipe to
reduce costs, event noise, and latency. For more information about configuring
event filtering for each cloud provider, see the following pages:

  * [Configuring event notifications using object key name filtering - Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-how-to-filtering.html#notification-how-to-filtering-examples-invalid)

  * [Understand event filtering for Event Grid subscriptions - Azure](https://docs.microsoft.com/en-us/azure/event-grid/event-filtering)

  * [Filtering messages - Google Pub/Sub](https://cloud.google.com/pubsub/docs/filtering)

**Next Topics:**

  * [Automating Snowpipe for Amazon S3](data-load-snowpipe-auto-s3)
  * [Automating Snowpipe for Google Cloud Storage](data-load-snowpipe-auto-gcs)
  * [Automating Snowpipe for Microsoft Azure Blob Storage](data-load-snowpipe-auto-azure)

