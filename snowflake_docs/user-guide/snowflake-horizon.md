# Snowflake Horizon Catalog¶

Snowflake Horizon Catalog lets organizations discover and govern data, apps,
and models through a built-in set of compliance, security, privacy, discovery,
and collaboration capabilities. It’s a unified solution addressing enterprise-
wide challenges while meeting the diverse needs of users working with the
organization’s content.

## Who benefits from Snowflake Horizon Catalog?¶

Snowflake Horizon Catalog provides a solution for everyone with a stake in
governing, discovering, or taking action on an organization’s content. These
stakeholders include the following:

Data stewards:

    

Data stewards want to provide access to data, apps, and models while still
ensuring that the right people have access to the content. They want to
identify sensitive data and appropriately protect it. It’s their job to
determine who’s using what data and understand the quality of the data.

Horizon Catalog lets data stewards effectively govern the organization’s
content with a built-in solution. They can protect content on a granular level
to safely make it available to a wider audience; use tools that monitor
security, quality of data, and flow of sensitive data; and continually audit
who has accessed data and whether that access was done securely.

Data teams:

    

Data teams of analysts, data scientists, and data engineers often struggle
with finding the right data, app, or model for their task. After they find an
object, it’s hard to tell if the data is up-to-date and trustworthy, what the
columns mean, and who owns it. Even when they’ve determined it’s the right
data, getting access to it can take days or weeks.

Horizon Catalog helps data teams find and collaborate on relevant content
faster. Horizon Catalog helps these teams extract more value from content by
making it easier to find the right data, understand the data so they can trust
that it meets requirements, and take action on that data. Data teams can
enhance collaboration and data-driven decisions by leveraging organizational
listings to discover and include relevant and up-to-date data products shared
by their coworkers and auto-fulfilled through the Internal Marketplace.

## Scope of an organization’s content¶

Horizon Catalog governs and makes discoverable more than just Snowflake tables
and views in the internal storage of an account. It covers a range of content,
including the following:

  * Data, apps, and models in accounts across your entire organization, including data shared using organizational listings and the [Internal Marketplace](collaboration/listings/organizational/org-listing-about).

  * Data from [Apache Iceberg™ tables](tables-iceberg) and [external tables](tables-external-intro).

  * Data shared through [private listings](https://other-docs.snowflake.com/en/collaboration/collaboration-listings-about#listing-availability-options) by trusted partners.

  * Publicly available data and every Snowflake Native App from the [Snowflake Marketplace](https://other-docs.snowflake.com/en/collaboration/collaboration-marketplace-about).

  * Data from third-party applications and data systems brought into Snowflake using [connectors](https://other-docs.snowflake.com/en/connectors).

## Governing content¶

Horizon Catalog provides the tools a data steward needs to govern an
organization’s data, apps, and models.

Compliance:

    

Horizon Catalog lets you do the following:

  * Audit the [access history](access-history) and [object dependencies](object-dependencies) of content.

  * Monitor data quality using built-in and custom [data metric functions](data-quality-intro), which lets you troubleshoot and visualize. You can configure an alert based on the centralized table to enable near-real-time data quality notifications.

  * View [data lineage](ui-snowsight-lineage) in Snowsight to understand the table and column lineage from a source table to a target table, and set tags on columns that appear in either a downstream or upstream table.

  * View object insights [1] using a user interface that lets you learn information about tables and views without writing SQL. You can determine who is accessing the data, the queries that access the data most frequently, whether someone has been modifying the governance posture of the data, whether there are downstream or upstream dependencies on the data, and whether the data has been classified as sensitive.

  * Track data by monitoring tags, which can be user-defined tags implemented with [object tagging](object-tagging) or classification tags ([system-defined](classify-intro.html#label-classification-system-tags) or [custom](classify-custom)) that have been automatically assigned to columns based on the content of the column.

[1] Currently in private preview.

Security:

    

Horizon Catalog lets you do the following:

  * Use the [Trust Center](trust-center/overview) to determine the current security posture of an account, including whether it meets the benchmarks established by the Center for Internet Security (CIS).

  * Use [end-to-end encryption](security-encryption-end-to-end) to prevent third parties from reading data while at-rest or in transit to and from Snowflake while minimizing the attack surface.

  * Choose your preferred authentication method such as [OAuth](oauth-intro) or [federated authentication](admin-security-fed-auth-overview).

  * Use granular [authorization controls](security-access-control-overview) to control access to objects.

  * Define and apply data access policies to provide [column-level](security-column-intro) and [row-level](security-row-intro) protections.

Privacy:

    

Horizon Catalog lets you do the following:

  * Define and assign [aggregation policies](aggregation-policies) and [projection policies](projection-policies) to control what type of queries can be run against shared data. Aggregation policies require analysts to run queries that aggregate data rather than retrieving individual rows. Projection policies control whether an analyst can use a SELECT statement to project a particular column.

  * Open up highly sensitive data to analysts while protecting the identity of individuals. [Differential privacy](diff-privacy/differential-privacy-overview) uses rigorous mathematics to protect against sophisticated privacy attacks on your data.

  * Facilitate collaboration while preserving privacy using a [Snowflake Data Clean Room](cleanrooms/introduction).

  * Expand who can learn insights from sensitive data by synthetically generating data with similar characteristics that they can work with directly.

## Discovering and taking action on content¶

Data teams rely on an organization’s data, apps, and models to do their job.
Horizon Catalog provides these teams with the tools they need to discover
content for their task, evaluate that content to ensure it’s relevant and
trustworthy, and take action on the content.

Discovery:

    

Horizon Catalog lets you do the following:

  * Use the [Internal Marketplace](collaboration/listings/organizational/org-listing-about) to discover and take action on data within your organization. The Internal Marketplace is a company-exclusive site that lets you discover organizational listings. The wiki-like listing pages, complete with data dictionaries and validated SQL examples, simplify the identification of data products curated by internal teams. No extra setup is needed — just copy the listing name, and the data is ready for immediate use.

  * Search for data, apps, and models using [Universal Search](ui-snowsight-universal-search), which is a user interface that lets you find content inside and outside your organization using natural language.

  * Quickly understand the contents of a table and its columns by reading AI-generated descriptions. Object owners can click a single button in Snowsight to [generate these descriptions](ui-snowsight-cortex-descriptions), which increases the likelihood that objects and columns have useful comments. These useful comments improve the discoverability of the objects through Universal Search.

  * [Browse publicly available data](https://other-docs.snowflake.com/en/collaboration/consumer-listings-exploring) on the Snowflake Marketplace.

  * Evaluate the relevancy of data by using object insights in Snowsight [3] to look at the popularity, access, quality, and dependencies of content.

[3] Currently in private preview.

Collaboration:

    

Horizon Catalog lets you do the following:

  * Share data within your organization in the [Internal Marketplace](collaboration/listings/organizational/org-listing-about) and privately with external business partners using [private listings](https://other-docs.snowflake.com/en/collaboration/provider-listings-creating-publishing#label-listings-create).

  * Buy and sell data products on the [Snowflake Marketplace](https://other-docs.snowflake.com/en/collaboration/collaboration-marketplace-about).

  * Manage your listings with a user interface or [programmatically using SQL commands](https://other-docs.snowflake.com/en/progaccess/listing-progaccess-about).

## Use case: Seeing Horizon Catalog in action¶

Suppose BazFin, a large financial services firm, needs to ensure the
compliance, data quality, and usability of its content, which consists of 10
PB of data. BazFin uses Horizon Catalog to govern and discover content.

Govern content

    

The chief data officer (CDO) of BazFin needs to assure company stakeholders
that business decisions are based on high-quality data. The CDO instructs the
data steward to leverage [system-defined and custom data metric
functions](data-quality-intro) to continually monitor data quality on a
regular schedule. On any given day, the CDO can view a dashboard built on the
events table to report on data quality.

Returning to her work for the day, the data steward opens the [Trust
Center](trust-center/overview) to check the overall security posture of a
Snowflake account that was recently created for a new division. From a built-
in interface, she identifies that someone forgot to define a network policy to
protect the account from unknown network traffic.

Discover and take action on content

    

A BazFin analyst wants to build a new dashboard to show top-performing
products. The analyst goes to the Internal Marketplace and finds just the
right organizational listing with performance data published by the finance
team. The analyst browses through a Data Dictionary to preview the data, then
starts querying the data right away using the listing’s Unified Listing
Locator.

The analyst also wants to enrich BazFin data with third-party data. Turning to
[Universal Search](ui-snowsight-universal-search), the analyst uses the
natural language search term `income bands for zipcodes`, which returns a data
product from the Snowflake Marketplace that they can join with the BazFin
product performance data.

