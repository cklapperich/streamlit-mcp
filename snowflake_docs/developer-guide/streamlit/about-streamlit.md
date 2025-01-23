# About Streamlit in Snowflake¶

This topic describes key features of Streamlit in Snowflake.

## What is Streamlit?¶

[Streamlit](https://streamlit.io/) is an open-source Python library that makes
it easy to create and share custom web apps for machine learning and data
science. By using Streamlit you can quickly build and deploy powerful data
applications. For more information about the open-source library, see the
[Streamlit Library documentation](https://docs.streamlit.io/).

[![../../_images/streamlit-visual.png](../../_images/streamlit-
visual.png)](../../_images/streamlit-visual.png)

## Deploy Streamlit apps in Snowflake¶

Streamlit in Snowflake helps developers securely build, deploy, and share
Streamlit apps on Snowflake’s data cloud. Using Streamlit in Snowflake, you
can build applications that process and use data in Snowflake without moving
data or application code to an external system.

[![../../_images/sis-example-app.png](../../_images/sis-example-
app.png)](../../_images/sis-example-app.png)

### Key features of Streamlit in Snowflake¶

  * Snowflake manages the underlying compute and storage for Streamlit apps.

  * Streamlit apps are Snowflake objects and use [Role-based Access Control (RBAC)](../../user-guide/security-access-control-overview) to manage access to Streamlit apps.

  * Streamlit apps run on Snowflake warehouses and use internal stages to store files and data.

  * Streamlit in Snowflake works seamlessly with Snowpark, user-defined functions (UDFs), stored procedures, and Snowflake Native App Framework.

  * When working with Snowsight, you use the side-by-side editor and app preview screen to quickly add, adjust, or remove components. In this way, you can modify your code and see changes in the app right away.

## Use cases¶

For additional use cases on building dashboards, data tools, and ML/AI, see
[Streamlit in Snowflake demos](https://github.com/Snowflake-Labs/snowflake-
demo-streamlit).

Note

These quickstarts are only shown as examples. Following along with the example
may require additional rights to third-party data, products, or services that
are not owned or provided by Snowflake. Snowflake does not guarantee the
accuracy of these examples.

## Billing considerations for Streamlit in Snowflake¶

Streamlit in Snowflake requires a [virtual warehouse](../../user-
guide/warehouses-overview) to run a Streamlit app and to perform SQL queries.
To run a Streamlit app, you must select a single virtual warehouse to run both
the app itself and its queries. This warehouse remains active while the app’s
WebSocket connection is active. The WebSocket connection, which keeps the
Streamlit app’s virtual warehouse active, expires approximately 15 minutes
after the app’s last use.

To conserve credits, you can suspend the virtual warehouse. Alternatively, you
can close the webpage running the app, which allows the virtual warehouse that
is running to auto-suspend.

For guidelines on selecting a warehouse, see [Guidelines for selecting a
warehouse in Streamlit in Snowflake](getting-started.html#label-streamlit-
guidelines-wh).

## Developer guides¶

The following guides explain working with Streamlit in Snowflake.

Guide | Description  
---|---  
[Getting started with Streamlit in Snowflake](getting-started) | Learn about the prerequisites and privileges required to work with Streamlit in Snowflake, and build your first app.  
[Create and deploy Streamlit apps using SQL](create-streamlit-sql) | Learn how to create and deploy Streamlit apps using SQL.  
[Create and deploy Streamlit apps using Snowsight](create-streamlit-ui) | Learn how to create and deploy Streamlit apps using Snowsight.  
[Create and deploy Streamlit apps using Snowflake CLI](create-streamlit-snowflake-cli) | Learn how to create and deploy Streamlit apps using Snowflake CLI.

