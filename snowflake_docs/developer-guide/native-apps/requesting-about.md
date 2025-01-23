# Request access to objects in a consumer account¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) Feature — Generally
Available

The Snowflake Native App Framework is generally available on supported cloud
platforms. For additional information, see [Support for private connectivity,
VPS, and government regions](limitations.html#label-native-apps-supported-
clouds).

This topic provides general information about how a provider can request
privileges or access to objects in the consumer account after a Snowflake
Native App is installed.

## About privileges and references in a Snowflake Native App¶

In a simple Snowflake Native App, all of the required objects are created
inside the APPLICATION object when the setup script runs during installation.
In this context, all of the objects required by the app are created and
accessible within the APPLICATION object. The consumer is not required to
perform any actions. All of the necessary privileges required are managed by
the app using application roles.

However, a more complex Snowflake Native App may need to create new objects or
access objects in the consumer account that are outside the APPLICATION
object. In this case, the consumer must grant the necessary privileges or
authorize access to allow the Snowflake Native App to create or access these
objects.

The Snowflake Native App Framework allows providers to do the following:

  * Check for account-level privileges in the consumer account.

  * Request account-level privileges to perform tasks, for example creating a database.

  * Use [references](../../sql-reference/references) to access existing objects in the consumer account.

Providers request access to a consumer account by requesting the following:

Global privileges

    

Global privileges allow the Snowflake Native App to perform actions in the
consumer account. Refer to [Privileges the provider can request from the
consumer](requesting-privs.html#label-native-apps-privs-supported) for
details.

References

    

[References](../../sql-reference/references) allow the app to access existing
objects in the consumer account. A provider defines the references that the
app requests in the `manifest.yml` file.

After installation, the consumer allows access to the object by providing a
reference that is created with the [fully qualified name](../../sql-
reference/name-resolution) of the object.

References allow the app to access objects using a logical name. A reference
allows a provider to create the app without having to know the specific name
of the object or its parent database and schema.

See [references](../../sql-reference/references) for more information.

## How a consumer allows access to a Snowflake Native App¶

For each request for access that provider defines in the app, the consumer
must allow access to the app. How a consumer allows access is different for
global privileges and references.

### Grant global privileges to a Snowflake Native App¶

When a provider configures an app to request specific privileges or access to
specific objects, there are two ways a consumer can grant these privileges to
the app:

  * If a provider implements a user interface using the Python Permission SDK, the consumer uses Snowsight to grant the permissions that are requested by the app. The Python Permission SDK automatically runs the required GRANT statements in the consumer account.

  * If a provider does not implement a user interface, the provider must communicate to the consumer what privileges the app requires. For example, the provide must communicate to the consumer information about the SQL statements that the consumer must run to grant the necessary privileges to the app.

Snowflake recommends including this information in the README file of the app,
which the consumer can view as part of listing for the Snowflake Native App.

### Authorize access on objects¶

When a provider defines a reference to an object in the consumer account that
is outside of the APPLICATION object, there are two ways a consumer can create
references on these objects and associate them to the application.

  * If a provider implements a user interface with the Python Permission SDK, the consumer uses Snowsight to associate the references to the objects required by the app. See [Managing Access Requests using Snowsight](https://other-docs.snowflake.com/en/native-apps/consumer-granting-privs#managing-access-requests-using-snowsight)

  * If a provider does not implement a user interface, the consumer must manually create the reference, then associate it with the Snowflake Native App.

