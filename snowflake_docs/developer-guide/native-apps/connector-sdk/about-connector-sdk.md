# Snowflake Native SDK for Connectors¶

[![Snowflake logo in black \(no text\)](../../../_images/logo-snowflake-
black.png)](../../../_images/logo-snowflake-black.png) Preview Feature — Open

Available to accounts in all regions in all cloud providers (including
government regions). For details, contact your Snowflake representative.

The Snowflake Native SDK for Connectors is a library that provides a skeleton
of the Snowflake native app whose purpose is to ingest data from external data
source into Snowflake. We call such an app a native connector.

The Snowflake Native SDK for Connectors is a set of application templates and
quickstarts that show how to build a Snowflake Native App that ingests data
from an external data source into Snowflake. These templates cover pull-based
and push-based data integration patterns.

These templates do not restrict or limit developers. Instead, the templates
provide examples of how to use core Snowflake features to ingest data and
encapsulate application code within a Snowflake Native App.

The Snowflake Native App Framework allows providers to publish and monetize a
Snowflake Native App on the Snowflake Marketplace. Snowflake Native App
developers can clone the template repository, modify the boilerplate code, and
create their own Snowflake Connectors.

## What is a native connector?¶

A connector is an application that allows data flow from an external source
system into Snowflake. A native connector is a connector application built and
deployed using the Snowflake Native App Framework. There are different types
of connectors:

  * pull-based connectors

  * push-based connectors

The Snowflake Native SDK for Connectors currently supports only the pull-based
pattern.

### Pull-based connectors¶

Pull-based patterns are effective when the source data provider does not
manage customer data in Snowflake and is not willing to incur COGS for a
continuous data share in Snowflake. These patterns are also effective when a
source data provider has well-documented APIs that customers can use to
replicate and consume data.

### How to use a pull-based pattern¶

By using a pull-based connector pattern, providers (Snowflake, or a third-
party ETL provider) can publish and distribute a native connector based on a
Snowflake Native App using the Snowflake Marketplace. A native connector uses
direct external access to connect with the source application. It performs
outbound authentication, fetches data from the source directly into a
customer’s Snowflake account, processes and persists the data based on a user-
specified configuration.

![Pull-based
architecture](../../../_images/connector_sdk_pull_based_architecture.png)

### Push-based connectors¶

Using a push-based pattern is effective when inbound access to the source
application through a customer firewall is not feasible because of security,
performance or governance limitations. This pattern uses an agent and a
Snowflake Native App to allow customers to ingest data changes into Snowflake
from behind a firewall .

### How to use a push-based pattern¶

An agent is a standalone application, distributed as a Docker image, that is
deployed in a customer environment and is responsible for sending initial and
incremental loads to Snowflake by reading data changes from a source CDC
stream.

A Snowflake Native App runs within Snowflake and coordinates the integration.
It is primarily responsible for managing the replication process, controlling
the agent state and creating required objects, including the target databases.

![Push-based
architecture](../../../_images/connector_sdk_push_based_architecture.png)

## What is the native SDK for connectors?¶

The Snowflake Native SDK for Connectors is a library that provides universal
components that can be used to build a custom Snowflake native app that
ingests the data from an external data source into Snowflake. The provided
components define the recommended flow

of the connector application and allow for customization and exclusion of some
features. As of now the Snowflake Native SDK for Connectors is provided as
code to be built locally and only in Java. Additionally, a second library
containing useful helper and utility classes for writing unit tests is
provided. Those libraries can be found in the maven central repository:

  * [Native SDK for Connectors library](https://central.sonatype.com/artifact/com.snowflake/connectors-native-sdk)

  * [Native SDK for Connectors Test library](https://central.sonatype.com/artifact/com.snowflake/connectors-native-sdk-test/overview)

The provided examples using those libraries also include example scripts that
can be used to deploy and create instance of the application inside Snowflake.

The Snowflake Native SDK for Connectors is designed to be used when building
applications based on the Snowflake Native App Framework and then publish and
monetize them using Snowflake Marketplace. To use the Snowflake Native SDK for
Connectors, clone it from a template or example application.

The Snowflake Native SDK for Connectors leverages the following features of
Snowflake:

  * [Native App Framework](../native-apps-about)

  * [External network access overview](../../external-network-access/external-network-access-overview)

  * [Stored procedures](../../stored-procedure/stored-procedures-overview) and [UDFs](../../udf/udf-overview)

  * [Streamlit in Snowflake](../../streamlit/about-streamlit)

### Additional information¶

For more information about the templates and quickstarts, see:

  * [Example repository](https://github.com/snowflakedb/connectors-native-sdk)

  * [Quickstart: Native GitHub Connector (Python)](https://quickstarts.snowflake.com/guide/connectors_github_python)

  * [Quickstart: Native Github Connector (Java)](https://quickstarts.snowflake.com/guide/connectors_github_java)

## Learn more¶

For more information about implementing connectors, see [Getting started with
the Snowflake Native SDK for Connectors](getting_started)

