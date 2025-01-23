# Continuous Data Protection¶

Continuous Data Protection (CDP) encompasses a comprehensive set of features
that help protect data stored in Snowflake against human error, malicious
acts, and software failure. At every stage within the data lifecycle,
Snowflake enables your data to be accessible and recoverable in the event of
accidental or intentional modification, removal, or corruption.

The features include:

Feature | Additional Reading  
---|---  
Network policies for granting or restricting users access to the site based on their IP address (i.e. IP allow lists). | [Controlling network traffic with network policies](network-policies)  
Verification/authentication required for any users accessing your account (includes support for MFA and SSO). | [Multi-factor authentication (MFA)](security-mfa) — enabled per user . [Federated authentication](admin-security-fed-auth-overview)  
Security roles for controlling user access to all objects in the system. | [Overview of Access Control](security-access-control-overview)  
All files stored on internal stages for data loading and unloading operations are automatically encrypted using AES-256 strong encryption on the server side. By default, Snowflake provides additional client-side encryption with a 128-bit key (with the option to configure a 256-bit key). | [Understanding end-to-end encryption in Snowflake](security-encryption-end-to-end)  
Maintenance of historical data (i.e. data that has been changed or deleted) through Snowflake Time Travel (for querying and restoring data) and Fail-safe (for disaster recovery; can only be performed by Snowflake). | [Snowflake Time Travel & Fail-safe](data-availability)  
  
Most Continuous Data Protection features are included standard for all
[Snowflake Editions](intro-editions) (i.e. no additional licensing is
required); however, some features are available only for Snowflake Enterprise
Edition (or higher).

In addition, both Time Travel and Fail-safe require additional data storage,
which has associated fees. For more details, see [Data storage
considerations](tables-storage-considerations).

