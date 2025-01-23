# Guidelines for publishing an app to the Snowflake Marketplace¶  
  
[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) Feature — Generally
Available

The Snowflake Native App Framework is generally available on supported cloud
platforms. For additional information, see [Support for private connectivity,
VPS, and government regions](limitations.html#label-native-apps-supported-
clouds).

This topic describes the criteria for publishing a Snowflake Native App to the
Snowflake Marketplace.

## Publish an app in the Snowflake Marketplace¶

When your application package is ready to be published on the Snowflake
Marketplace, you must submit it to Snowflake for approval.

Note

The approval process required to publish an app on the Snowflake Marketplace
is in addition to the [automated security scan](security-overview) that is run
when the DISTRIBUTION property of an application package is set to EXTERNAL.

Before creating a listing, verify that you understand the enforced
requirements and ensure that your application package follows each
requirement. If an application package does not follow these requirements,
your submission may be rejected.

If you receive a rejection notification for the application package you
submitted, make the recommended changes and resubmit your application package
for approval.

## Standards for Snowflake Native Apps on the Snowflake Marketplace¶

Snowflake provides a platform that allows providers to build, distribute, and
monetize apps.

The Snowflake review process ensures the quality of the apps that are
published to the Snowflake Marketplace. To ensure a streamlined review
process, Snowflake provides the following requirements and guidelines for apps
that are published to the Snowflake Marketplace.

Immediate utility

    

All app functionality must be provided within the consumer account when the
app is installed. For example, when a consumer installs an app in their
account all app functionality must be available without requiring that the
consumer install additional components.

Standalone

    

Apps must deliver product experience on Snowflake and facilitate external
requirements through Snowflake functionality.

Data-centric

    

Apps should be based on data-centric use cases that leverage data stored in
Snowflake.

Transparent and simple

    

Apps must use Snowflake features to disclose the app’s resource and access
requirements and simplify the configuration process for the consumer.

## Enforced requirements¶

Snowflake uses the following guidelines to determine if a Snowflake Native App
meets the requirements for publication on the Snowflake Marketplace. These
requirements are verified when you submit a listing with an attached
application package to the Snowflake Marketplace.

  1. Immediate utility

    1. Apps must not be shell apps that advertise functionality.

    2. Apps must include a clear framework and instruction for utilizing app functionality.

    3. Apps should not crash, freeze, or otherwise function abnormally.

    4. Apps must list all required credentials and providers must share required credentials with Snowflake at submission for testing.

    5. Apps must be immediately actionable, allowing consumers to fully install and configure the app without needing to contact the provider.

  2. Standalone

    1. Apps must not redirect consumers to an external service to enable application functionality.

    2. App interfaces must be accessible after installation directly from Snowflake.

    3. Apps cannot require consumers to create users or roles that provide access to an external service in the Snowflake consumer’s account.

    4. Apps cannot use the Snowflake Marketplace as a distribution platform for cross-selling external applications or services.

  3. Data-centric

    1. Apps must leverage Snowflake data in one of the following ways:

      1. Share data from the app provider’s account.

      2. Use datasets from the Snowflake Marketplace.

      3. Access data in the consumer account.

  4. Transparent

    1. All account-level privileges and references that the app requires must be listed in the application package manifest file.

    2. All resource requirements for the Snowflake Native App must be listed in the [marketplace.yml](marketplace-file) file of the app. The app must create these resources as part of installation and setup.

    3. All account-level privileges and references listed in the application package manifest file must be requested from the consumer through Snowsight or the Python Permission SDK.

    4. Apps must provide a readme file. Apps that do not include a Streamlit or custom user interface must include the following information in the readme file:

      1. A description of what the app does.

      2. The steps the consumer must perform to configure the app after it is installed.

      3. The stored procedures and user-defined functions the app uses.

      4. The privileges the app requires.

      5. Example SQL commands that show consumers how to use the app.

    5. All required SQL commands must be delivered using Snowflake and formatted as code blocks.

    6. If the app provides sample data, you must include procedures on how to use the sample data.

## Best practices when publishing a Snowflake Native App¶

In addition to the requirements for submitting an application package to the
Snowflake Marketplace, Snowflake also recommends the following best practices
when publishing a Snowflake Native App:

  * Ensure that all required files are uploaded to the named stage for the version of the app you are submitting, including:

    * The `manifest.yml` file.

    * The setup script.

    * The `readme.md` file.

    * Any external stored procedures or user-defined functions required by the application package.

    * Any Streamlit files required by the application package.

    * Any external source code, including Python, Java, etc.

  * Ensure that the version of the app you are developing passes the [automated security scan](security-overview).

  * Test the new version of your application package by creating the application object locally by using the [CREATE APPLICATION](../../sql-reference/sql/create-application) command.

    * Do not add a new version to your application package or set the DISTRIBUTION property to EXTERNAL while you are developing and testing an app. These actions trigger the [automated security scan](security-overview) which delays the development cycle.

Instead, create the application object using [files on a named
stage](installing-testing-application.html#label-native-apps-application-
creating-stage).

    * If your app includes a Streamlit app, test the application in Snowsight to ensure the Streamlit app works as expected.

    * Verify that interactions between the Streamlit app and Snowflake Worksheets are seamless and that the consumer does not have to navigate excessively between the two.

  * Review all parts of a listing before submitting it for approval.

  * Ensure that there are no typos or other textual errors in the listing, `readme` file, and Streamlit app.

### Recommendations for trial listings¶

When an app trial listing expires, Snowflake automatically suspends the app to
avoid consumers incurring extra compute costs to the consumer. Snowflake only
suspends the objects owned by the app that are currently active. Snowflake
does not modify the status of objects that are already suspended.

When a trial listing is converted to a full or paid listing, Snowflake
attempts to re-enable the app by resuming tasks, containers, and compute
pools. Snowflake only resumes services and compute pools that have the
`auto_resume` property set to false.

### Recommendations for apps with containers¶

  * Compute pools should be set to automatically suspend in combination with Snowpark Container Services jobs to avoid idle compute nodes.

  * For higher availability during upgrades and to reduce cold start latency, Snowflake recommends that you set the `MIN_NODES` parameter greater than 1.

  * If connections across different services are required in the same app, use the DNS name of the service instead of configuring an external access integration.

### Recommendations for event sharing¶

  * Providers should configure an app to emit log messages and trace events that conform to [supported event definitions](https://other-docs.snowflake.com/en/native-apps/consumer-enable-logging#about-event-sharing) to ensure that consumers understand what information is collected.

  * Mandatory event definitions should be limited to the log messages and trace events required by the app. Excessive or unnecessary mandatory event definitions should be avoided.

  * Adding new mandatory event definitions in a version upgrade must require the consumer re-enable event definitions for the app.

  * Use the Python Permission SDK to allow consumers to share optional events.

