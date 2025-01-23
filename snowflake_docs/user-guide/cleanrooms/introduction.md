# About Snowflake Data Clean Rooms¶

Feature — Generally Available

Not available in government regions.

A Snowflake Data Clean Room is a native solution that makes it easy to build,
connect, and use data clean rooms in Snowflake.

Data clean rooms offer a secure way to gain valuable insights while protecting
sensitive information. They allow you to combine and analyze data from
different parties without worrying about the privacy concerns that go with
sharing raw data. With data clean rooms, multiple parties can collaborate
without revealing their underlying data.

Benefits of data clean rooms include:

  * **Enhanced privacy** — Protects sensitive data while enabling collaboration.

  * **Deeper insights** — Combines data from multiple sources for richer analysis.

  * **Increased security** — Reduces the risk of unauthorized access.

## How Snowflake Data Clean Rooms work¶

With Snowflake Data Clean Rooms, all analyses are conducted within the secure
environment of the clean room. Collaborators are able to return aggregated
results and insights, but cannot directly query the raw data in the clean
room. The collaborator who is sharing their data can define what analyses are
available to the other collaborators, allowing them to tightly control how
their data is used.

A Snowflake Data Clean Room also uses privacy-enhancing techniques on its data
such as:

  * Using differential privacy to add noise to results in order to prevent someone from identifying whether a particular individual is in the data.

  * Encrypting the data, then running multi-party computations directly on the encrypted data.

## Clean room collaborators¶

Snowflake Data Clean Rooms use the concept of a provider and consumer, similar
to other Snowflake features like Secure Data Sharing. The data owner is a
_provider_ who uses a clean room to safely share data with a _consumer_. The
consumer installs the clean room in their own account and analyzes data in the
clean room, including joining their own data with the data of the provider.

Tasks associated with clean room collaborators include:

Provider:

    

  * Create a clean room.

  * Add data to a clean room.

  * Configure a clean room to control how a consumer can interact with data.

  * Share a clean room with a consumer.

Consumer:

    

  * Install a clean room.

  * Add datasets to the clean room.

  * Analyze data in the clean room, including joining consumer data with the provider’s data.

Within the clean room environment associated with a Snowflake account, a
collaborator can be the provider of one clean room while acting as the
consumer of another.

If you want to collaborate with someone who is not currently a Snowflake
customer, see [Clean room managed accounts](managed-accounts).

For information about adding a collaborator to your clean room environment,
see [Add collaborators](admin-tasks.html#label-cleanrooms-get-started-add-
collaborators).

## Working with a Snowflake Data Clean Room¶

A Snowflake Data Clean Room is designed for both business and technical users.
You have two options for working with a clean room:

  * **Web app** — An easy-to-use interface that makes privacy-enhanced data collaboration accessible to a wide base of users, including non-technical business users. Collaborators can use pre-defined analysis templates including audience overlap, reach and frequency, and last touch attribution. For an overview, see [Snowflake Data Clean Rooms: Web app overview](web-app-introduction).

  * **Developer APIs** — A complete set of APIs that allow a technical audience to work with clean rooms programmatically, including the ability to build custom applications and to customize analysis templates and ML models. For an overview, see [Snowflake Data Clean Rooms: Developer APIs overview](developer-introduction).

## Known limitations¶

Snowflake Data Clean Rooms have some limitations, including:

  * In the web app, the Audience Lookalike Modeling template does not support objects with quoted identifiers.

## Next Step¶

Before users can work with the web app or developer APIs, a clean room
administrator needs to sign up for the clean room environment and configure
the Snowflake account associated with it. For details, see [Get started with
Snowflake Data Clean Rooms](getting-started).

