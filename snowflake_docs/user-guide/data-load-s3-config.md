# Configuring secure access to Amazon S3¶

To read data from and write to an S3 bucket, the security and access
management policies on the bucket must allow Snowflake to access the bucket.

The following options for configuring secure access to a private S3 bucket are
supported:

Option 1:

    

Configure a storage integration object to delegate authentication
responsibility for external cloud storage to a Snowflake identity and access
management (IAM) entity.

Note

We highly recommend this option, which avoids the need to supply AWS IAM
credentials when creating stages or loading data.

Option 2:

    

Configure an AWS IAM role with the required policies and permissions to access
your external S3 bucket. This approach allows individual users to avoid
providing and managing security credentials and access keys.

Note that implementing this feature requires a named external stage. Support
for accessing an S3 bucket URL directly in a COPY statement is not supported.

Important

The ability to use an AWS IAM role to access a private S3 bucket to load or
unload data is now deprecated (i.e. support will be removed in a future
release, TBD). We highly recommend modifying any existing S3 stages that use
this feature to instead reference storage integration objects (**Option 1** in
this topic).

Option 3:

    

Configure an AWS IAM user with the required permissions to access your S3
bucket. This one-time setup involves establishing access permissions on a
bucket and associating the required permissions with an IAM user. You can then
access an external (i.e. S3) stage that points to the bucket with the AWS key
and secret key.

This topic describes how to perform the required tasks in S3.

Note

Completing the instructions in this topic requires administrative access to
AWS. If you are not an AWS administrator, ask your AWS administrator to
perform these tasks.

**Next Topics:**

  * [Option 1: Configuring a Snowflake storage integration to access Amazon S3](data-load-s3-config-storage-integration)
  * [Option 2: Configuring an AWS IAM role to access Amazon S3 — _Deprecated_](data-load-s3-config-aws-iam-role)
  * [Option 3: Configuring AWS IAM user credentials to access Amazon S3](data-load-s3-config-aws-iam-user)

