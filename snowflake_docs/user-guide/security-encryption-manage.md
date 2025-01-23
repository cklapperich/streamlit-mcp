# Understanding Encryption Key Management in Snowflake¶

This topic provides concepts related to Snowflake-managed keys and customer-
managed keys.

## Overview¶

Snowflake manages data encryption keys to protect customer data. This
management occurs automatically without any need for customer intervention.

Customers can use the key management service in the cloud platform that hosts
their Snowflake account to maintain their own additional encryption key.

When enabled, the combination of a Snowflake-maintained key and a customer-
managed key creates a composite [master
key](https://csrc.nist.gov/glossary/term/master_key) to protect the Snowflake
data. This is called [Tri-Secret Secure](security-encryption-tss).

## Snowflake-managed keys¶

All Snowflake customer data is encrypted by default using the latest security
standards and best practices. Snowflake uses strong AES 256-bit encryption
with a hierarchical key model rooted in a hardware security module.

Keys are automatically rotated on a regular basis by the Snowflake service,
and data can be automatically re-encrypted (“rekeyed”) on a regular basis.
Data encryption and key management is entirely transparent and requires no
configuration or management.

### Hierarchical key model¶

A hierarchical key model provides a framework for Snowflake’s encryption key
management. The hierarchy is composed of several layers of keys in which each
higher layer of keys (parent keys) encrypts the layer below (child keys). In
security terminology, a parent key encrypting all child keys is known as
“wrapping”.

Snowflake’s hierarchical key model consists of four levels of keys:

  * The root key

  * Account master keys

  * Table master keys

  * File keys

Each customer account has a separate key hierarchy of account-level, table-
level, and file-level keys, as shown in the following image:

![Snowflake's hierarchical key model](../_images/hierarchical-key-model.png)

In a multi-tenant cloud service like Snowflake, the hierarchical key model
isolates every account with the use of separate account master keys. In
addition to the [access control model](security-access-control-overview),
which separates storage of customer data, the hierarchical key model provides
another layer of account isolation.

A hierarchical key model reduces the scope of each layer of keys. For example,
a table master key encrypts a single table. A file key encrypts a single file.
A hierarchical key model constrains the amount of data each key protects and
the duration of time for which it is usable.

### Encryption key rotation¶

All Snowflake-managed keys are automatically rotated by Snowflake when they
are more than 30 days old. Active keys are retired, and new keys are created.
When Snowflake determines the retired key is no longer needed, the key is
automatically destroyed. When active, a key is used to encrypt data and is
available for usage by the customer. When retired, the key is used solely to
decrypt data and is only available for accessing the data.

When wrapping child keys in the key hierarchy, or when inserting data into a
table, only the current, active key is used to encrypt data. When a key is
destroyed, it is not used for either encryption or decryption. Regular key
rotation limits the life cycle for the keys to a limited period of time.

The following image illustrates key rotation for one table master key (TMK)
over a period of three months:

![Key rotation of one table master key \(TMK\) over a time period of three
months.](../_images/key-rotation.png)

The TMK rotation works as follows:

  * Version 1 of the TMK is active in April. Data inserted into this table in April is protected with TMK v1.

  * In May, this TMK is rotated: TMK v1 is retired and a new, completely random key, TMK v2, is created. TMK v1 is now used only to decrypt data from April. New data inserted into the table is encrypted using TMK v2.

  * In June, the TMK is rotated again: TMK v2 is retired and a new TMK, v3, is created. TMK v1 is used to decrypt data from April, TMK v2 is used to decrypt data from May, and TMK v3 is used to encrypt and decrypt new data inserted into the table in June.

As stated previously, key rotation limits the duration of time in which a key
is actively used to encrypt data. In conjunction with the hierarchical key
model, key rotation further constrains the amount of data a key version
protects. Limiting the lifetime of a key is
[recommended](http://csrc.nist.gov/publications/nistpubs/800-57/sp800-57_part1_rev3_general.pdf)
by the National Institute of Standards and Technology (NIST) to enhance
security.

### Periodic rekeying¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Enterprise Edition
Feature](intro-editions)

Periodic rekeying requires Enterprise Edition (or higher). To inquire about
upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-
guide/contacting-support).

This section continues the explanation of the account and table master key
lifecycle. Encryption Key Rotation described key rotation, which replaces
active keys with new keys on a periodic basis and retires the old keys.
Periodic data rekeying completes the life cycle.

While key rotation ensures that a key is transferred from its active state to
a retired state, rekeying ensures that a key is transferred from its retired
state to being destroyed.

If periodic rekeying is enabled, then when the retired encryption key for a
table is older than one year, Snowflake automatically creates a new encryption
key and re-encrypts all data previously protected by the retired key using the
new key. The new key is used to decrypt the table data going forward.

Note

For Enterprise Edition accounts, users with the ACCOUNTADMIN role (i.e. your
account administrators) can enable rekeying using [ALTER ACCOUNT](../sql-
reference/sql/alter-account) and the [PERIODIC_DATA_REKEYING](../sql-
reference/parameters.html#label-periodic-data-rekeying) parameter:

>
>     ALTER ACCOUNT SET PERIODIC_DATA_REKEYING = true;
>  
>
> Copy

The following image shows periodic rekeying for a TMK for a single table:

![Rekeying one table master key \(TMK\) after one
year](../_images/rekeying.png)

Periodic rekeying works as follows:

  * In April of the following year, after TMK v1 has been retired for an entire year, it is rekeyed (generation 2) using a fully new random key.

The data files protected by TMK v1 generation 1 are decrypted and re-encrypted
using TMK v1 generation 2. Having no further purpose, TMK v1 generation 1 is
destroyed.

  * In May, Snowflake performs the same rekeying process on the table data protected by TMK v2.

  * And so on.

In this example, the lifecycle of a key is limited to a total duration of one
year.

Rekeying constrains the total duration in which a key is used for recipient
usage, following NIST recommendations. Furthermore, when rekeying data,
Snowflake can increase encryption key sizes and utilize better encryption
algorithms that may be standardized since the previous key generation was
created.

Rekeying, therefore, ensures that all customer data, new and old, is encrypted
with the latest security technology.

Snowflake rekeys data files online, in the background, without any impact to
currently running customer workloads. Data that is being rekeyed is always
available to you. No service downtime is necessary to rekey data, and you
encounter no performance impact on your workload. This benefit is a direct
result of Snowflake’s architecture of separating storage and compute
resources.

Note

You cannot use [hybrid tables](tables-hybrid) if your Snowflake account is
enabled to use periodic rekeying. If periodic rekeying is enabled in your
account and you want to use hybrid tables, you must use an [ALTER
ACCOUNT](../sql-reference/sql/alter-account) command to set the
[PERIODIC_DATA_REKEYING](../sql-reference/parameters.html#label-periodic-data-
rekeying) parameter to `FALSE`.

#### Impact of rekeying on Time Travel and Fail-safe¶

[Time Travel](data-time-travel) and [Fail-safe](data-failsafe) retention
periods are not affected by rekeying. Rekeying is transparent to both
features. However, some additional storage charges are associated with
rekeying of data in Fail-safe (see next section).

#### Impact of rekeying on storage utilization¶

Snowflake customers are charged with additional storage for Fail-safe
protection of data files that were rekeyed. For these files, 7 days of Fail-
safe protection is charged.

That is, for example, the data files with the old key on Amazon S3 are already
protected by Fail-safe, and the data files with the new key on Amazon S3 are
also added to Fail-safe, leading to a second charge, but only for the 7-day
period.

### Hardware security module¶

Snowflake relies on cloud-hosted hardware security modules (HSMs) to ensure
that key storage and usage is secure. Each cloud platform has different HSM
services and that affects how Snowflake uses the HSM service on each platform:

  * On AWS and Azure, Snowflake uses the HSM to create and store the root key.

  * On Google Cloud, the HSM service is made available through the Google Cloud KMS (key management service) API. Snowflake uses Google Cloud KMS to create and store the root key in multi-tenant HSM partitions.

For all cloud platforms and all keys in the key hierarchy, a key that is
stored in the HSM is used to unwrap a key in the hierarchy. For example, to
decrypt the table master key, the key in the HSM unwraps the account master
key. This process occurs in the HSM. After this process completes, a software
operation decrypts the table master key with the account master key.

The following image shows the relationship between the HSM, the account master
keys, table master keys, and the file keys:

![Key hierarchy rooted in Hardware Security Module](../_images/hardware-
security-module.png)

## Customer-managed keys¶

A customer-managed key is a master encryption key that the customer maintains
in the key management service for the cloud provider that hosts your Snowflake
account. The key management services for each platform are:

  * **AWS:** [AWS Key Management Service (KMS)](https://aws.amazon.com/kms/)

  * **Google Cloud:** [Cloud Key Management Service (Cloud KMS)](https://cloud.google.com/kms)

  * **Microsoft Azure:** [Azure Key Vault](https://azure.microsoft.com/en-us/services/key-vault/)

The customer-managed key can then be combined with a Snowflake-managed key to
create a composite master key. When this occurs, Snowflake refers to this as
Tri-Secret Secure.

You can call these system functions in your Snowflake account to obtain
information about your keys:

  * AWS: [SYSTEM$GET_CMK_KMS_KEY_POLICY](../sql-reference/functions/system_get_cmk_kms_key_policy)

  * Microsoft Azure: [SYSTEM$GET_CMK_AKV_CONSENT_URL](../sql-reference/functions/system_get_cmk_akv_consent_url)

  * Google Cloud: [SYSTEM$GET_GCP_KMS_CMK_GRANT_ACCESS_CMD](../sql-reference/functions/system_get_gcp_kms_cmk_grant_access_cmd)

Important

Snowflake does not support key rotation for customer-managed keys and does not
recommend implementing an automatic key rotation policy on the customer-
managed key.

The reason for this recommendation is that the key rotation can lead to a loss
of data if the rotated key is deleted because Snowflake will not be able to
decrypt the data. For more information, see [Tri-Secret Secure](security-
encryption-tss).

### Benefits of customer-managed keys¶

Benefits of customer-managed keys include:

Control over data access:

    

You have complete control over your master key in the key management service
and, therefore, your data in Snowflake. It is impossible to decrypt data
stored in your Snowflake account without you releasing this key.

Disable access due to a data breach:

    

If you experience a security breach, you can disable access to your key and
halt all data operations running in your Snowflake account.

Ownership of the data lifecycle:

    

Using customer-managed keys, you can align your data protection requirements
with your business processes. Explicit control over your key provides
safeguards throughout the entire data lifecycle, from creation to deletion.

### Important requirements for customer-managed keys¶

Customer-managed keys provide significant security benefits, but they also
have crucial, fundamental requirements that you must continuously follow to
safeguard your master key:

Confidentiality:

    

You must keep your key secure and confidential at all times.

Integrity:

    

You must ensure your key is protected against improper modification or
deletion.

Availability:

    

To execute queries and access your data, you must ensure your key is
continuously available to Snowflake.

By design, an invalid or unavailable key will result in a disruption to your
Snowflake data operations until a valid key is made available again to
Snowflake.

However, Snowflake is designed to handle temporary availability issues (up to
10 minutes) caused by common issues, such as network communication failures.
After 10 minutes, if the key remains unavailable, all data operations in your
Snowflake account will cease completely. Once access to the key is restored,
data operations can be started again.

Failure to comply with these requirements can significantly jeopardize the
integrity of your data, ranging from your data being temporarily inaccessible
to it being permanently disabled. In addition, Snowflake cannot be responsible
for 3rd-party issues that occur or administrative mishaps caused by your
organization in the course of maintaining your key.

For example, if an issue with the key management service results in your key
becoming unavailable, your data operations will be impacted. These issues must
be resolved between you and the Support team for the key management service.
Similarly, if your key is tampered with or destroyed, all existing data in
your Snowflake account will become unreadable until the key is restored.

