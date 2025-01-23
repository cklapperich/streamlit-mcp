# About Data Exchange¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) Data exchange is not enabled
for all accounts

To inquire about enabling a data exchange, please contact [Snowflake
Support](https://docs.snowflake.com/user-guide/contacting-support).

Data Exchange provides a data hub for securely collaborating around data with
a selected group of members that you invite. It lets you, as a provider,
publish data which can then be discovered by the consumers participating in
your exchange.

With a Data Exchange, you can easily provide data to a specific group of
consistent business partners taking part in the Data Exchange, such as
internal departments in your company or vendors, suppliers, and partners
external to your company. If you want to share data with a variety of
consumers inside and outside your organization, you can also use listings
offered to specific consumers or publicly on the Snowflake Marketplace.

[![Diagram depicting a data exchange featuring a listing published by your
account, accessible by Company A with a reader/writer account in your
organization. Company A also publishes a listing to the data exchange which is
then accessed by Company B in a separate organization, also participating in
the data exchange. Company B shares a listing which is then accessed by your
account. Each company account is creating a listing from a share, which is in
turn created from a database in their account.](../_images/private-data-
exchange-govern.png)](../_images/private-data-exchange-govern.png)

You can manage membership, access to data, and audit data usage, as well as
apply security controls to the data shared in the Data Exchange. see [Manage
data listings](data-exchange-managing-data-listings).

To set up a data exchange, see [Request a new Data Exchange](data-exchange-
requesting).

  * To access a data exchange, see [Access a Data Exchange](data-exchange-accessing).

  * To create and manage data exchange provider profiles, see [Manage provider profiles](data-exchange-becoming-a-provider).

  * If you’re a consumer of a data exchange, see [Configure and use a Data Exchange](data-exchange-using).

## Data Exchange Admin responsibilities¶

The Snowflake account that hosts the Data Exchange is the Data Exchange Admin.
The Data Exchange Admin is responsible for configuring the Data Exchange and
managing members (data providers and data consumers).

A user with the ACCOUNTADMIN role in the account designated as the Data
Exchange Admin can:

  * Add or remove members

  * Designate members as providers, or consumers, or both

A Data Exchange Admin can delegate these privileges to other roles. For more
information, see [Granting administrator privileges in a Data Exchange](data-
exchange-marketplace-privileges.html#label-granting-admin-privileges-to-other-
roles).

## Data Exchange membership¶

Members are Snowflake accounts that are added by the Data Exchange Admin and
designated as providers, consumers, or both.

After joining the Data Exchange, providers can:

  * Create a listing.

  * Define listing access personalized or [free](https://other-docs.snowflake.com/en/collaboration/collaboration-listings-about.html#label-free-listing)).

  * Publish the listing.

  * Grant access to personalized listings or datasets that reside in a different region from the consumer.

After joining the Data Exchange, consumers can:

  * Discover by browsing the exchange listings.

  * Switch between the Snowflake Marketplace and the Data Exchange.

  * Consume datasets (instantly or by request).

