# Understand limitations in the Snowflake Native App Framework¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) Feature — Generally
Available

The Snowflake Native App Framework is generally available on supported cloud
platforms. For additional information, see Support for private connectivity,
VPS, and government regions.

This topic provides information about the limitations of the Snowflake Native
App Framework.

## Known Limitations¶

The Snowflake Native App Framework has limitations, including:

  * Temporary tables or stages are not supported.

  * Some Streamlit features are not supported. See [Unsupported Streamlit Features](adding-streamlit.html#label-streamlit-unsupported-features-na) for details.

  * The Snowflake Native App Framework does not support failover for business continuity. For example, adding an application package to a replication group or failover group is not supported.

## Known limitations in Snowflake Native Apps with Snowpark Container
Services¶

Snowflake Native Apps with Snowpark Container Services have the following
limitations:

  * Apps with containers are only supported on specific AWS and Azure commercial regions. See Support for private connectivity, VPS, and government regions for information on support for private connectivity, VPS, and government regions.

  * Sessions used in connections from containers, for example using the Python connector, are limited to the application owner role. See [Snowpark Container Services: Additional considerations for services and jobs](../snowpark-container-services/additional-considerations-services-jobs) for additional information.

  * A maximum of 15 compute pools per application is allowed.

  * [Cross-Cloud Auto-Fulfillment](https://other-docs.snowflake.com/en/collaboration/provider-listings-auto-fulfillment) is only supported on Amazon Web Services and Microsoft Azure (preview) with the following limitation:

    * There is a 100GB limit for each file within the image repository.

  * Using the LOG_LEVEL and TRACE_LEVEL properties in the `manifest.yml` file to set the logging and trace level for a container is not supported. Instead, use the `spec.logExporters` property in the service specification file.

See [spec.logExporters field (optional)](../snowpark-container-
services/specification-reference.html#label-snowpark-containers-spec-
reference-spec-logexporters) for more information.

## Support for private connectivity, VPS, and government regions¶

The following tables list Snowflake Native App Framework support for private
connectivity, Virtual Private Snowflake (VPS), and government regions on the
[cloud platform](../../user-guide/intro-cloud-platforms) that Snowflake
supports:

**Amazon Web Services**

> | Amazon Web Services | AWS PrivateLink | Virtual Private Snowflake | Government regions  
> ---|---|---|---|---  
> Snowflake Native App Framework (without containers) | Generally available | Generally available | Generally available | Generally available  
> Snowflake Native App Framework (with containers) | Generally available | Not yet supported | Not yet supported | Not yet supported  
  
**Microsoft Azure**

> | Microsoft Azure | Microsoft Azure Private Link | Virtual Private Snowflake | Government regions  
> ---|---|---|---|---  
> Snowflake Native App Framework (without containers) | Generally available | Preview | Not yet supported | Generally available  
> Snowflake Native App Framework (with containers) | Preview | Not yet supported | Not yet supported | Generally available  
  
**Google Cloud**

> | Google Cloud | Google Cloud Private Service Connect | Virtual Private Snowflake  
> ---|---|---|---  
> Snowflake Native App Framework (without containers) | Generally available | Not yet supported | Not yet supported  
> Snowflake Native App Framework (with containers) | Not yet supported | Not yet supported | Not yet supported  
  
## Known issue with AWS and Azure PrivateLink¶

Links in email notifications from apps do not correctly link into a private
link accounts.

## Limitations on government regions¶

The following limitations apply to Snowflake Native App Framework support for
government regions:

  * AWS GovCloud is supported in only the following regions:

    * US Gov West 1 (FedRAMP High Plus)

    * US Gov East 1 (FedRAMP High Plus)

  * AWS Commercial Gov is supported in only the following regions:

    * US East (N. Virginia)

  * Only Azure GovCloud is supported in only the following regions:

    * US East (N. Virginia)

  * Providers publishing apps from government regions can only share listings within the same organization.

## Limitations on Virtual Private Snowflake (VPS)¶

The following limitations apply to Snowflake Native App Framework support for
Virtual Private Snowflake (VPS):

  * The Snowflake Native App Framework and Streamlit are not enabled by default in Virtual Private Snowflake. To use the Snowflake Native App Framework or Streamlit in VPS, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

  * If Streamlit is not enabled in the VPS deployment, consumers cannot use the Python Permission SDK to manage privileges and references.

  * Sharing an app from a VPS account to an account outside the VPS is only supported within the same organization. To share an app outside the current organization, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

  * Only private listings are supported for applications published inside the VPS.

  * Consumers in the VPS can [enable event sharing](https://other-docs.snowflake.com/en/native-apps/consumer-enable-logging#enable-event-sharing-for-an-app) for an app. However, log messages and trace events are not shared unless the provider has an event table within the VPS.

  * Because the Snowflake Marketplace interface is not available in VPS, providers and consumers must manage listings by using SQL. For additional information, see [About managing listings using SQL](https://other-docs.snowflake.com/en/progaccess/listing-progaccess-about).

