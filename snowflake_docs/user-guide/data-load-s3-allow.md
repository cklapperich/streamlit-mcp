# Allowing the Virtual Private Cloud IDs¶

This topic describes how an AWS administrator in your organization can
explicitly grant Snowflake access to your AWS S3 storage account (i.e. your
buckets and the objects in those buckets). The process involves allowing the
Amazon Virtual Private Cloud (Amazon VPC) IDs for your Snowflake account.

Important

This security feature currently requires that your S3 bucket is located in the
same AWS [region](intro-regions) as your Snowflake account.

To allow the Amazon VPC IDs for your Snowflake account:

  1. Log into your Snowflake account using any supported client.

  2. Execute [USE ROLE](../sql-reference/sql/use-role) to set ACCOUNTADMIN as the active role for the user session.
    
        USE ROLE ACCOUNTADMIN;
    

Copy

  3. Query the [SYSTEM$GET_SNOWFLAKE_PLATFORM_INFO](../sql-reference/functions/system_get_snowflake_platform_info) function to retrieve the IDs of the AWS Virtual Network (VNet) in which your Snowflake account is located:
    
        SELECT SYSTEM$GET_SNOWFLAKE_PLATFORM_INFO();
    

Copy

Record the VPC IDs returned by the query.

  4. Allow the VPC IDs by creating an [Amazon S3 policy for a specific VPC](https://docs.aws.amazon.com/AmazonS3/latest/dev/example-bucket-policies-vpc-endpoint.html?shortFooter=true#example-bucket-policies-restrict-access-vpc).

  5. Provide an AWS Identity and Access Management (IAM) role to Snowflake to access the allowed Amazon S3 bucket instead of the AWS key and secret.

For help with this configuration process or any of the other AWS configuration
steps, please contact your organization’s AWS administrator.

**Next:** [Configuring secure access to Amazon S3](data-load-s3-config)

