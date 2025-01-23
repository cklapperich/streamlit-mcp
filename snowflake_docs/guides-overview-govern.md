# Data Governance in Snowflake¶

Snowflake provides industry-leading features that ensure the highest levels of
governance for your account and users, as well as all the data you store and
access in Snowflake.

[Data Quality Monitoring and data metric functions](user-guide/data-quality-
intro)

    

Allows the monitoring of the state and integrity of your data using system
data metric functions and user-defined data metric functions.

[Column-level Security](user-guide/security-column-intro)

    

Allows the application of a masking policy to a column within a table or view.

[Row-level Security](user-guide/security-row-intro)

    

Allows the application of a row access policy to a table or view to determine
which rows are visible in the query result.

[Object Tagging](user-guide/object-tagging)

    

Allows the tracking of sensitive data for compliance, discovery, protection,
and resource usage.

[Tag-based masking policies](user-guide/tag-based-masking-policies)

    

Allows protecting column data by assigning a masking policy to a tag and then
setting the tag on a database object or the Snowflake account.

[Sensitive data classification](user-guide/classify-intro)

    

Allows categorizing potentially personal and/or sensitive data to support
compliance and privacy regulations.

[Access History](user-guide/access-history)

    

Allows the auditing of the user access history through the Account Usage
[ACCESS_HISTORY view](sql-reference/account-usage/access_history).

[Object Dependencies](user-guide/object-dependencies)

    

Allows the auditing of how one object references another object by its
metadata (e.g. creating a view depends on a table name and column names)
through the Account Usage [OBJECT_DEPENDENCIES](sql-reference/account-
usage/object_dependencies) view.

Data Governance area in Snowsight

    

Allows using the Monitoring » Governance area to monitor and report on the
usage of policies and tags with tables, views, and columns using two different
interfaces: Dashboard and Tagged Objects. For details, see:

  * [Create and assign tags](user-guide/object-tagging.html#label-object-tagging-create-assign)

  * [Monitor tags with Snowsight](user-guide/object-tagging.html#label-object-tagging-snowsight)

  * [Monitor masking policies with Snowsight](user-guide/security-column-intro.html#label-security-column-intro-snowsight)

  * [Monitor row access policies with Snowsight](user-guide/security-row-intro.html#label-security-row-intro-snowsight)

