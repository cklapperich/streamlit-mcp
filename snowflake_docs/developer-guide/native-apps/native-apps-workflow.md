# Snowflake Native App Framework workflow¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) Feature — Generally
Available

The Snowflake Native App Framework is generally available on supported cloud
platforms. For additional information, see [Support for private connectivity,
VPS, and government regions](limitations.html#label-native-apps-supported-
clouds).

This topic describes the workflows for developing, publishing, and installing
an application created using the Native Apps Framework.

## Development workflow¶

The following workflow outlines the general tasks for developing and testing
an application using the Native Apps Framework:

Note

Developing an application is an iterative process. You might perform many of
these tasks multiple times or in a different order depending on the
requirements of your application and environment.

  1. [Create the setup script](creating-setup-script) for your application.

The setup script contains the SQL statements that define the components
created when a consumer installs your application.

  2. [Create the manifest file](creating-manifest) for your application.

The manifest file defines the configuration and setup properties required by
the application, including the location of the setup script and versions.

  3. Upload the application files to a named stage.

The setup script, the manifest file, and other resources that your application
requires must be uploaded to a named stage so that these files are available
as you develop your application.

  4. [Create an application package](creating-app-package).

An application package is a container that encapsulates the data content,
application logic, metadata, and setup script required by an application.

  5. [Add versions and patch levels to your application](update-app-versions).

Adding versions and patches to your application allows you to add features to
your application or fix problems.

  6. [Add shared data content to your application](preparing-data-content).

The Native Apps Framework allows you to securely share your data content with
consumers.

  7. [Add application logic](adding-application-logic).

You can include business logic as part of your application. An application can
contain:

     * [User-defined functions (UDFs) and stored procedures](../extensibility).

     * [Snowpark functions and procedures written in Python, Java, and Scala](../snowpark/index).

     * [External functions](../../sql-reference/external-functions-introduction).

  8. [Set up logging and event handling to troubleshoot your application.](event-about)

To troubleshoot an application, the Native Apps Framework provides logging and
event handling. Consumers can set up logging and event handling in their
account and share them with providers.

  9. [Set the release directive for your application](update-app-release-directive.html#label-native-apps-release-dir).

A release directive determines which version and patch level are available to
consumers.

  10. [Test your application](installing-testing-application).

You can test an application in your account before publishing it to consumers.
The Native Apps Framework provides [development mode](installing-testing-
application.html#label-native-apps-dev-mode) and [debug mode](installing-
testing-application.html#label-native-apps-testing-debug-mode) to test
different aspects of your application.

  11. [Run the automated security scan](security-overview).

Before you can share an application with consumers outside your organization,
the application must pass an automated security scan to ensure that it is
secure and stable.

## Publishing workflow¶

After developing and testing the application, providers can publish the
application to share it with consumers. See [Sharing an Application with
Consumers](https://other-docs.snowflake.com/en/native-apps/provider-
publishing-app-package) for details.

  1. [Become a provider](https://other-docs.snowflake.com/en/collaboration/provider-becoming).

Becoming a provider allows you to create and manage listings to share your
application with consumers.

  2. [Create a listing](https://other-docs.snowflake.com/en/native-apps/provider-publishing-app-package#creating-a-listing-for-an-application-package).

You can create a private listing or a Snowflake Marketplace listing to share
your application with consumers.

  3. [Submit your listing for approval](https://other-docs.snowflake.com/en/native-apps/provider-publishing-app-package#label-nativeapps-provider-listings-submit-approval).

Before you can publish a listing to the Snowflake Marketplace, you must submit
the listing to Snowflake for approval.

  4. [Publish your listing](https://other-docs.snowflake.com/en/native-apps/provider-publishing-app-package#publishing-a-listing-for-an-application-package).

After your listing is approved, you can publish the listing to make it
available to consumers.

## Consumer workflow¶

Consumers can discover the application and install it from a listing. After
installing the application, consumers can configure, use, and monitor the
application. See [Working with Applications as a Consumer](https://other-
docs.snowflake.com/en/native-apps/consumer-about).

  1. [Become a Snowflake consumer](https://other-docs.snowflake.com/en/collaboration/consumer-becoming).

Becoming a Snowflake consumer allows you to access listings shared privately
or on the Snowflake Marketplace. You can also access data shared as part of
direct shares or data exchanges, which offer more limited data sharing
capabilities.

  2. [Install the application](https://other-docs.snowflake.com/en/native-apps/consumer-installing).

Consumers can install an application from a listing.

  3. [Grant the privileges required by the application](https://other-docs.snowflake.com/en/native-apps/consumer-granting-privs).

Some applications might ask the consumer to grant global and object-level
privileges to the application.

  4. [Enable logging and event sharing to troubleshoot the application](https://other-docs.snowflake.com/en/native-apps/consumer-enable-logging).

A provider can set up an application to emit logging and event data. A
consumer can set up an events table to share this data with providers. Logs
and event data are useful when troubleshooting an application.

  5. [Manage the application](https://other-docs.snowflake.com/en/native-apps/consumer-managing-applications).

After installing and configuring the application, a consumer can perform
additional tasks to use and monitor the application.

