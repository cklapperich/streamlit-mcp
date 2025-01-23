# Sensitive data classification¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Enterprise Edition
Feature](intro-editions)

This feature requires Enterprise Edition or higher. To inquire about
upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-
guide/contacting-support).

This topic provides information on how sensitive data classification works.

For information on how to use custom classifiers, see [Custom sensitive data
classification](classify-custom).

## Overview¶

Sensitive data classification is a multi-step process that associates
Snowflake-defined system tags to columns by analyzing the fields and metadata
for personal data; this data can be tracked by a data engineer using SQL and
Snowsight. A data engineer can classify columns in a table to determine
whether the column contains certain kinds of data that need to be tracked or
protected, such a unique identifier (passport or bank account data), a quasi-
identifier (the city in which the individual lives), or a sensitive value (the
salary of an individual).

By tracking the data with a system tag and protecting the data by using a
masking or row access policy, the data engineer can improve the governance
posture associated with the data. The overall result of the classification and
data protection steps is to facilitate compliance with data privacy
regulations.

You can classify a single table or tables in a schema. Snowflake provides
predefined system tags to enable you to classify and tag columns, or you can
use custom classifiers to define your own semantic category based on your
knowledge of your data. You can also choose an approach the uses Snowflake
system tags and custom classifiers depending on the governance posture that
you wish to adopt.

Classification provides the following benefits to data privacy and data
governance administrators:

Data access:

    

The results of classifying column data can inform identity and access
management administrators to evaluate and maintain their Snowflake [role
hierarchies](security-access-control-overview) to ensure the Snowflake roles
have the appropriate access to sensitive or PII data.

Data sharing:

    

The classification process can help to identify and confirm the storage
location of PII data. Subsequently, a data sharing provider can use the
classification results to determine whether to share data and how to make the
PII data available to a data sharing consumer.

Policy application:

    

The usage of columns containing PII data, such as referencing columns in base
tables to create a view or materialized view, can help to determine the best
approach to protect the data with either a masking policy or a row access
policy.

## System tags and categories¶

System tags are tags that Snowflake creates, maintains, and makes available in
the shared [SNOWFLAKE database](../sql-reference/snowflake-db). There are two
Classification system tags, both of which exist in the `SNOWFLAKE.CORE`
schema:

  * `SNOWFLAKE.CORE.SEMANTIC_CATEGORY`

  * `SNOWFLAKE.CORE.PRIVACY_CATEGORY`

The data engineer assigns these tags to a column containing personal or
sensitive data.

String values:

    

Snowflake stores the assignment of a system tag on a column as a key-value
pair, where the value is a string. Snowflake defines the allowed string values
for each classification system tag because Snowflake maintains each of these
system tags.

The tag names, `SEMANTIC_CATEGORY` and `PRIVACY_CATEGORY`, correspond to the
Classification categories that Snowflake assigns to the column data during the
column sampling process (i.e. the tag names and category names use the same
words):

Semantic category:

    

The semantic category identifies personal attributes.

A non-exhaustive list of personal attributes Classification supports include
name, age, and gender. These three attributes are possible string values when
assigning the `SEMANTIC_CATEGORY` tag to a column.

Classification can detect information from different countries, such as
Australia, Canada, and the United Kingdom. For example, if your table column
contains phone number information, the analysis process can differentiate the
different phone number values from each of these countries.

Privacy category:

    

If the analysis determines that the column data corresponds to a semantic
category, Snowflake further classifies the column to a privacy category. The
privacy category has three values: identifier, quasi-identifier, or sensitive.
These three values are the string values that can be specified when assigning
the `PRIVACY_CATEGORY` Classification system tag to a column.

  * Identifier: These attributes uniquely identify an individual. Example attributes include name, social security number, and phone number.

Identifier attributes are synonymous with _direct identifiers_.

  * Quasi-identifier: These attributes can uniquely identify an individual when two or more or these attributes are in combination. Example attributes include age and gender.

Quasi-identifiers are synonymous with _indirect identifiers_.

  * Sensitive: These attributes are not considered enough to identify an individual but are information that the individual would rather not disclose for privacy reasons.

Currently, the only attribute that Snowflake evaluates as sensitive is salary.

  * Insensitive: These attributes do not contain personal or sensitive information.

The following table summarizes the relationship between each classification
category and system tag, and the string values for each classification system
tag. Snowflake supports international SEMANTIC_CATEGORY tag values that
pertain to certain countries. The country codes are based on the [ISO-3166-1
alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) standard. Other
semantic categories, such as `EMAIL` and `GENDER`, do not have a country code.
To track international information, the data engineer uses the value in the
SEMANTIC_CATEGORY tag values column when setting a system tag on a column.

PRIVACY_CATEGORY values | SEMANTIC_CATEGORY values | Supported countries  
---|---|---  
`IDENTIFIER` | 

  * `BANK_ACCOUNT`
  * `DRIVERS_LICENSE`
  * `MEDICARE_NUMBER`
  * `NATIONAL_IDENTIFIER`
  * `ORGANIZATION_IDENTIFIER`
  * `PASSPORT`
  * `PHONE_NUMBER`
  * `STREET_ADDRESS`
  * `TAX_IDENTIFIER`
  * `EMAIL`
  * `IBAN`
  * `IMEI`
  * `IP_ADDRESS`
  * `NAME`
  * `PAYMENT_CARD`
  * `URL`
  * `VIN`

|

  * CA, NZ, US
  * AU, CA, NZ, US
  * AU, NZ
  * CA, NZ, SG, UK, US (SSN)
  * AU, NZ, SG
  * AU, CA, NZ, SG, US
  * AU, CA, JP, UK, US
  * CA, US
  * AU, NZ, US (EIN, ITIN)

  
`QUASI_IDENTIFIER` | 

  * `ADMINISTRATIVE_AREA_1`
  * `ADMINISTRATIVE_AREA_2`
  * `CITY`
  * `POSTAL_CODE`
  * `AGE`
  * `COUNTRY`
  * `DATE_OF_BIRTH`
  * `ETHNICITY`
  * `GENDER`
  * `LAT_LONG`
  * `LATITUDE`
  * `LONGITUDE`
  * `MARITAL_STATUS`
  * `OCCUPATION`
  * `YEAR_OF_BIRTH`

|

  * CA, NZ, US
  * US
  * CA, NZ, US
  * AU, CA, CH, JP, NZ, UK, US

  
`SENSITIVE` | 

  * `SALARY`

|  
  
Note

Contains public sector information licensed under the [Open Government Licence
v3.0](https://www.nationalarchives.gov.uk/doc/open-government-
licence/version/3/).

Multiple semantic tag string values from all three privacy categories can be
considered “Sensitive Personal Data”, “Special Categories of Data”, or similar
terms under laws and regulations, and might require additional protections or
controls.

## Supported objects and data types¶

Snowflake supports classifying data stored in all types of tables and views,
including external tables, materialized views, and secure views.

Note that Snowflake does not support classification on [shared tables](data-
sharing-intro) and shared schemas from the consumer’s side. If a table is
created by the provider and placed into the provider’s outbound share, the
classification will work only if it is called from the provider’s side.

You can classify table and view columns for all supported [data types](../sql-
reference-data-types) except for the following data types:

  * ARRAY

  * BINARY

  * GEOGRAPHY

  * OBJECT

  * VARIANT

Note that you can classify a column with the VARIANT data type when the column
data type can be [cast](../sql-reference/functions/cast) to a NUMBER or STRING
data type. Snowflake does not classify the column if the column contains JSON,
XML, or other semi-structured data.

  * VECTOR

If a table contains columns that are not of a supported data type or the
column contains all NULL values, the classification process ignores the
columns and does not include them in the output.

Important

If your data represents NULL values with a value other than NULL, the accuracy
of the classification results may be impacted.

## Recommendations¶

To capitalize on the Classification feature and optimize your PII data
tracking capabilities, do the following:

Validation:

    

Query Account Usage views first:

  * [ACCESS_HISTORY](../sql-reference/account-usage/access_history): determine the table and view objects that are accessed most frequently.

  * [OBJECT_DEPENDENCIES](../sql-reference/account-usage/object_dependencies): determine metadata references between two or more objects.

Use the query results to prioritize schema-level or database-level assignment
of the Classification system tags.

Column names:

    

Use sensible column names in your table objects and train table creators to
adhere to internal table creation guidelines.

Data types:

    

Use sensible data types for columns. For example, an AGE column should have
the NUMBER data type.

VARIANT:

    

If a column has a VARIANT data type, use the [FLATTEN](../sql-
reference/functions/flatten) command on the column prior to classifying the
table.

## Classify tables and schemas¶

After you’ve defined any [custom classifiers](classify-custom) that you want
to use, you’re ready to classify your sensitive data. You can use the
following approaches:

  * Manually classify a specific table. You can start the classification process using [Snowsight](classify-using.html#label-classification-snowsight) or by [executing a SQL command](classify-using.html#label-classification-sql-table).

  * [Manually classify all the tables in a schema](classify-using.html#label-classification-sql-schema).

  * Set up a classification profile for a schema so the tables in the schema are [automatically classified](classify-auto).

## Manage sensitive data classification¶

### Privilege reference¶

The privilege model for Data Classification enables the data privacy
administrator to determine which personas can classify tables and tag columns.
For example, a single role can have all of the necessary privileges, or the
data privacy administrator can delegate grants to different roles to satisfy
separation of duties (SoD) requirements. One example of a viable grant
combination is shown in the [Get started classifying data](classify-
using.html#label-classification-getting-started) section of [Classify
sensitive data manually](classify-using).

As an administrator, you have different options depending on how you want to
manage which roles or personas are involved. The options provide flexibility
in the governance posture that you wish to adopt. For example:

  * The table owner (the role with the OWNERSHIP privilege on the table) can classify the table and set system tags on the columns.

  * A custom role that has the SELECT privilege on the table and the APPLY TAG privilege on the account can classify the table and set system tags on the columns.

  * If you want different roles or personas to be involved with classifying and tagging columns, you could grant the SELECT privilege on the table to one role and the APPLY TAG privilege on the account to a different role.

This following table summarizes the different grant options to classify a
table, set the Data Classification system tags on columns, and do both of
these tasks:

Privilege or role | Classify table(s) | Set system tags on columns  
---|---|---  
SELECT on the table or view. | ✔ |   
OWNERSHIP on the table. | ✔ | ✔  
APPLY TAG on the account. |  | ✔  
ACCOUNTADMIN role. |  | ✔  
OWNERSHIP on the database or schema. |  |   
  
Important

  * Classifying tables requires a running warehouse. The role that is used to classify a table must have the USAGE privilege on a warehouse at a minimum.

  * You can grant the SNOWFLAKE.GOVERNANCE_VIEWER database role to an account role to enable users with that account role to query the [DATA_CLASSIFICATION_LATEST](../sql-reference/account-usage/data_classification_latest) view to see the most recent results of a classified table.

### Tracking system tags¶

Snowflake provides built-in views and functions to track Classification system
tag usage:

  * To find the columns with a system tag in your account, query the Account Usage [TAG_REFERENCES](../sql-reference/account-usage/tag_references) view:

> >     SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.TAG_REFERENCES
>         WHERE TAG_NAME = 'PRIVACY_CATEGORY'
>         ORDER BY OBJECT_DATABASE, OBJECT_SCHEMA, OBJECT_NAME, COLUMN_NAME;
>  
>
> Copy

  * To find the columns with a system tag for a table or view in a specific database, call the [TAG_REFERENCES](../sql-reference/functions/tag_references) Information Schema table function:

> >     SELECT * FROM
>       TABLE(
>         MY_DB.INFORMATION_SCHEMA.TAG_REFERENCES(
>           'my_db.my_schema.hr_data.fname',
>           'COLUMN'
>         ));
>  
>
> Copy

  * To find every tag set on every column in a table or view within a specific database, call the Information Schema [TAG_REFERENCES_ALL_COLUMNS](../sql-reference/functions/tag_references_all_columns) table function:

> >     SELECT * from
>       TABLE(
>         MY_DB.INFORMATION_SCHEMA.TAG_REFERENCES_ALL_COLUMNS(
>           'my_db.my_schema.hr_data',
>           'table'
>         ));
>  
>
> Copy

  * To find a specific tag value for a column, call the [SYSTEM$GET_TAG](../sql-reference/functions/system_get_tag) system function:

> >     SELECT SYSTEM$GET_TAG(
>       'SNOWFLAKE.CORE.PRIVACY_CATEGORY',
>       'hr_data.fname',
>       'COLUMN'
>       );
>  
>
> Copy

