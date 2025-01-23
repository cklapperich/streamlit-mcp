# About the Snowflake Native App Framework¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) Feature — Generally
Available

The Snowflake Native App Framework is generally available on supported cloud
platforms. For additional information, see [Support for private connectivity,
VPS, and government regions](limitations.html#label-native-apps-supported-
clouds).

This topic provides general information about the Snowflake Native App
Framework.

## Introduction to the Snowflake Native App Framework¶

The Snowflake Native App Framework allows you to create data applications that
leverage core Snowflake functionality. The Snowflake Native App Framework
allows you to:

  * Expand the capabilities of other Snowflake features by sharing data and related business logic with other Snowflake accounts. The business logic of an application can include a Streamlit app, stored procedures, and functions written using [Snowpark API](../snowpark/index), JavaScript, and SQL.

  * Share an application with consumers through listings. A listing can be either free or paid. You can distribute and monetize your apps in the Snowflake Marketplace or distribute them to specific consumers using private listings.

  * Include rich visualizations in your application using Streamlit.

The Snowflake Native App Framework also supports an enhanced development
experience that provides:

  * A streamlined testing environment where you can test your applications from a single account.

  * A robust developer workflow. While your data and related database objects remain within Snowflake, you can manage supporting code files and resources within source control using your preferred developer tools.

  * The ability to release versions and patches for your application that allows you, as a provider, to change and evolve the logic of your applications and release them incrementally to consumers.

  * Support for logging of structured and unstructured events so that you can troubleshoot and monitor your applications.

## Components of the Snowflake Native App Framework¶

The following diagram shows a high-level view of the Snowflake Native App
Framework.

![../../_images/native-apps-overview.png](../../_images/native-apps-
overview.png)

The Snowflake Native App Framework is built around the concept of provider and
consumer used by other Snowflake features, including [Snowflake
Collaboration](https://other-
docs.snowflake.com/en/collaboration/collaboration-about.html) and [Secure Data
Sharing](../../user-guide/data-sharing-gs)

Provider

    

A Snowflake user who wants to share data content and application logic with
other Snowflake users.

Consumer

    

A Snowflake user who wants to access the data content and application logic
shared by providers.

### Develop and Test an Application Package¶

To share data content and application logic with a consumer, providers create
an application package.

Application package

    

An application package encapsulates the data content, application logic,
metadata, and setup script required by an application. An application package
also contains information about versions and patch levels defined for the
application. See [Create an application package](creating-app-package) for
details.

An application package can include references to data content and external
code files that a provider wants to include in the application. An application
package requires a manifest file and a setup script.

Manifest file

    

Defines the configuration and setup properties required by the application,
including the location of the setup script, versions, etc. See [Create the
manifest file for an application package](creating-manifest) for details.

Setup script

    

Contains SQL statements that are run when the consumer installs or upgrades an
application or when a provider installs or upgrades an application for
testing. The location of the setup script is specified in the `manifest.yml`
file. See [Create a setup script](creating-setup-script) for details.

### Publish an Application Package¶

After developing and testing an application package, a provider can share an
application with consumers by publishing a listing containing the application
package as the data product of a listing. The listing can be a Snowflake
Marketplace listing or a private listing.

Snowflake Marketplace listing

    

Allows providers to market applications across the Snowflake Data Cloud.
Offering a listing on the Snowflake Marketplace lets providers share
applications with many consumers simultaneously, rather than maintain sharing
relationships with each individual consumer.

Private listing

    

Allows providers to take advantage of the capabilities of listings to share
applications directly with another Snowflake account in any [Snowflake region
supported](limitations.html#label-native-apps-framework-limitations) by the
Snowflake Native App Framework.

See [About Listings](https://other-
docs.snowflake.com/en/collaboration/collaboration-listings-about) for details.

### Install and Manage an Application¶

After a provider publishes a listing containing an application package,
consumers can discover the listing and install the application.

Snowflake Native App

    

A Snowflake Native App is the database object installed in the consumer
account. When a consumer installs the Snowflake Native App, Snowflake creates
the application and runs the setup script to create the required objects
within the application. See [Install and test an app locally](installing-
testing-application) for details.

After installing the application, consumers can perform additional tasks,
including:

  * [Enable logging and event sharing](https://other-docs.snowflake.com/en/native-apps/consumer-enable-logging) to help providers troubleshoot the application.

  * [Grant privileges required by the application](https://other-docs.snowflake.com/en/native-apps/consumer-granting-privs).

See [Working with Applications as a Consumer](https://other-
docs.snowflake.com/en/native-apps/consumer-about) for details on how consumers
install and manage an application.

## About Snowflake Native Apps with Snowpark Container Services¶

A Snowflake Native App with Snowpark Container Services (app with containers)
is a Snowflake Native App that runs container workloads in Snowflake.
Container apps can run any containerized service supported by Snowpark
Container Services.

Apps with containers leverage all of the features of the Snowflake Native App
Framework, including provider IP protection, security and governance, data
sharing, monetization, and integration with compute resources.

Like any Snowflake Native App, an app with containers is comprised of an
application package and application object. However, there are some
differences as shown in the following image:

![../../_images/na-spcs-overview.png](../../_images/na-spcs-overview.png)

Application package:

    

To manage containers, the application package must have access to a services
specification file on a stage. Within this file, there are references to the
container images required by the app. These images must be stored in an image
repository in the provider account.

Application object:

    

When a consumer installs an app with containers, the application object that
is created contains a compute pool that stores the containers required by the
app.

Compute pool:

    

A compute pool is a collection of one or more virtual machine (VM) nodes on
which Snowflake runs your Snowpark Container Services jobs and services. When
a consumer installs an app with containers, they can grant the CREATE COMPUTE
POOL privilege to the app or they can create the compute pools manually.

## Protect provider intellectual property in an app with containers¶

When an app with containers is installed in the consumer account, the query
history of the services is available in the consumer account. To protect a
provider’s confidential information, the Snowflake Native App Framework
redacts the following information:

  * The query text is hidden from the [QUERY_HISTORY view](../../sql-reference/account-usage/query_history).

  * All information in the [ACCESS_HISTORY view](../../sql-reference/account-usage/access_history) is hidden.

  * The [Query Profile](../../user-guide/ui-snowsight-activity) graph for the service’s query is collapsed into a single empty node instead of displaying the full query profile tree.

## Multi-factor requirements for users in a provider account¶

Depending on the type of user, Snowflake requires different types of
authentication for users in the provider account.

### Non-service users¶

Snowflake recommends that users in a provider account enroll in [multi-factor
authentication (MFA)](../../user-guide/security-mfa) if they do not have the
[TYPE](../../sql-reference/sql/create-user.html#label-user-type-property)
property set to SERVICE. In a future update, multi-factor authentication will
be mandatory for these types of users. Non-service users who use [federated
authentication](../../user-guide/admin-security-fed-auth-overview) and single
sign-on (SSO) must have MFA enabled as part of their authentication process.

### Service users¶

Users who have the TYPE parameter set to SERVICE must use [key-pair
authentication](../../user-guide/key-pair-auth) or [OAuth](../../user-
guide/oauth-intro).

