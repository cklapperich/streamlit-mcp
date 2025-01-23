# Overview of federated authentication and SSO¶

This topic describes the components that comprise a federated environment for
authenticating users, and the SSO (single sign-on) workflows supported by
Snowflake.

## What is a federated environment?¶

In a federated environment, user authentication is separated from user access
through the use of one or more external entities that provide independent
authentication of user credentials. The authentication is then passed to one
or more services, enabling users to access the services through SSO. A
federated environment consists of the following components:

  * Service provider (SP):
    

In a Snowflake federated environment, Snowflake serves as the SP.

  * Identity provider (IdP):
    

The external, independent entity responsible for providing the following
services to the SP:

    * Creating and maintaining user credentials and other profile information.

    * Authenticating users for SSO access to the SP.

Snowflake supports most SAML 2.0-compliant vendors as an IdP; however, certain
vendors include native support for Snowflake (see below for details).

## Supported identity providers¶

The following vendors provide native Snowflake support for federated
authentication and SSO:

  * [Okta](http://www.okta.com) — hosted service

  * [Microsoft AD FS](https://msdn.microsoft.com/en-us/library/bb897402.aspx) (Active Directory Federation Services) — on-premises software (installed on Windows Server)

In addition to the native Snowflake support provided by Okta and AD FS,
Snowflake supports using most SAML 2.0-compliant vendors as an IdP, including:

  * [Google G Suite](https://gsuite.google.com/)

  * [Microsoft Entra ID](https://www.microsoft.com/en-us/security/business/identity-access/microsoft-entra-id)

  * [OneLogin](https://www.onelogin.com/product/sso)

  * [Ping Identity PingOne](https://www.pingidentity.com/en/products/pingone.html)

Note

To use an IdP other than Okta or AD FS, you must define a custom application
for Snowflake in the IdP.

For details about configuring Okta, AD FS, or another SAML 2.0-compliant
vendor as the IdP for Snowflake, see [Configuring an identity provider (IdP)
for Snowflake](admin-security-fed-auth-configure-idp).

## Using multiple identity providers¶

You can configure Snowflake so different users authenticate using different
identity providers.

Once you have [configured all of the identity providers](admin-security-fed-
auth-configure-idp), follow the guidance in [Using multiple identity providers
for federated authentication](admin-security-fed-auth-security-integration-
multiple).

Note

Currently, only a subset of Snowflake drivers support the use of multiple
identity providers. These drivers include JDBC, ODBC, and Python.

## Supported SSO workflows¶

Federated authentication enables the following SSO workflows:

  * Logging into Snowflake.

  * Logging out of Snowflake.

  * System timeout due to inactivity.

The behavior for each workflow is determined by whether the action is
initiated within Snowflake or your IdP.

### Login workflow¶

When a user logs in, the behavior of the system is determined by whether the
login is initiated through Snowflake or the IdP:

  * Snowflake-initiated login:
    

To log in through Snowflake:

    1. User goes to the Snowflake web interface.

    2. User chooses to log in using the IdP configured for your account (Okta, AD FS, or a custom IdP).

    3. User authenticates with the IdP using their IdP credentials (e.g. email address and password).

    4. If authentication is successful, the IdP sends a SAML response to Snowflake to initiate a session and displays the Snowflake web interface.

Note

For Snowflake-initiated login, the Snowflake login page provides two options
for authentication (IdP or Snowflake). To use federated authentication, users
must choose the IdP option and then enter their credentials when prompted.
Choosing the Snowflake option bypasses federated authentication and logs the
user in using Snowflake’s native authentication.

  * IdP-initiated login:
    

To log in through the IdP for your account:

    1. User goes to the IdP site/application and authenticates using their IdP credentials (e.g. email address and password).

    2. In the IdP, user clicks on the Snowflake application (if using Okta or AD FS) or the custom application that has been defined in the IdP (if using another IdP).

    3. The IdP sends a SAML response to Snowflake to initiate a session and then displays the Snowflake web interface.

### Logout workflow¶

When a user logs out, the available options are dictated by whether the IdP
supports _global_ logout or only _standard_ logout:

> Standard:
>  
>
> Requires users to explicitly log out of both the IdP and Snowflake to
> completely disconnect. All IdPs support standard logout.
>
> Global:
>  
>
> Enables a user to log out of the IdP and subsequently all their Snowflake
> sessions. Support for global logout is IdP-dependent.

In addition, the behavior of the system is determined by whether the logout is
initiated through Snowflake or the IdP:

  * Snowflake-initiated logout:
    

Global logout is not supported from within Snowflake, regardless of whether
the IdP supports it. When a user logs out of a Snowflake session, they are
logged out of that session only. All their other current Snowflake sessions
stay open, as does their IdP session. As a result, they can continue working
in their other sessions or they can initiate additional sessions without
having to re-authenticate through the IdP.

To completely disconnect, users must explicitly log out of both Snowflake and
the IdP.

  * IdP-initiated logout:
    

When a user logs out through an IdP, the behavior depends on whether the IdP
supports standard logout only or also global logout:

    * AD FS supports both standard and global logout. If global logout is enabled, the AD FS IdP login page provides an option for signing out from all sites that the user has accessed. Selecting this option and clicking Sign Out logs the user out of AD FS and all their Snowflake sessions. To access Snowflake again, they must re-authenticate using AD FS.

    * Okta supports standard logout only. When a user logs out of Okta, they are not automatically logged out of any of their active Snowflake sessions and they can continue working. However, to initiate any new Snowflake sessions, they must authenticate again through Okta.

    * All custom providers support standard logout; support for global logout varies by provider.

Note

For a web-based IdP (e.g. Okta), closing the browser tab/window does not
necessarily end the IdP session. If a user’s IdP session is still active, they
can still access Snowflake until the IdP session times out.

### Timeout workflow¶

When a user’s session times out, the behavior is determined by whether it is
their Snowflake session or IdP session that timed out:

  * Snowflake timeout:
    

If a users logs into Snowflake using SSO and their Snowflake session expires
due to inactivity, the Snowflake web interface is disabled and the prompt for
IdP authentication is displayed:

    * To continue using their expired Snowflake session, the user must authenticate again through the IdP.

    * The user can exit the session by clicking the Cancel button.

    * The user can also go to the IdP site/application directly and relaunch Snowflake, but this initiates a new Snowflake session.

  * IdP timeout:
    

After a specified period of time (defined by the IdP), a user’s session in the
IdP automatically times out, but this does not affect their Snowflake
sessions. Any Snowflake sessions that are active at the time remain open and
do not require re-authentication. However, to initiate any new Snowflake
sessions, the user must log into the IdP again.

## SSO with private connectivity¶

Snowflake supports SSO with private connectivity to the Snowflake service for
Snowflake accounts on Amazon Web Services (AWS), Microsoft Azure, and Google
Cloud Platform (GCP).

Currently, for any given Snowflake account, SSO works with only one account
URL at a time: either the public account URL or the URL associated with the
private connectivity service on AWS, Microsoft Azure, or Google Cloud
Platform.

Snowflake supports using SSO with [organizations](organizations), and you can
use the corresponding URL in the SAML2 security integration. For more
information, see [Configuring Snowflake to use federated
authentication](admin-security-fed-auth-security-integration).

To use SSO with private connectivity to Snowflake, configure private
connectivity before configuring SSO:

  * If your Snowflake account is on AWS or Azure, follow the self-service instructions as listed in [AWS PrivateLink and Snowflake](admin-security-privatelink) and [Azure Private Link and Snowflake](privatelink-azure).

  * If your Snowflake account is on GCP, you must contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) and provide the Snowflake account URL to use with [Google Cloud Private Service Connect and Snowflake](private-service-connect-google).

To determine the correct URL to use, call the
[SYSTEM$GET_PRIVATELINK_CONFIG](../sql-
reference/functions/system_get_privatelink_config) function in your Snowflake
account on GCP.

## Replicate the SSO Configuration¶

Snowflake supports replication and failover/failback of the [SAML2 security
integration](admin-security-fed-auth-security-integration) from a source
account to a target account.

For details, see [Replication of security integrations & network policies
across multiple accounts](account-replication-security-integrations).

