# Share data content in a Snowflake Native App¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) Feature — Generally
Available

The Snowflake Native App Framework is generally available on supported cloud
platforms. For additional information, see [Support for private connectivity,
VPS, and government regions](limitations.html#label-native-apps-supported-
clouds).

This topic describes how providers can add shared data content to a Snowflake
Native App.

Note

Providers can publish a Snowflake Native App to the Snowflake Marketplace as a
limited trial listing. To publish an app as a trial listing, see [Preparing to
offer a limited trial listing](https://other-
docs.snowflake.com/collaboration/provider-listings-preparing#label-prepare-
limited-trial-listing).

## About shared data in a Snowflake Native App¶

The Snowflake Native App Framework allows providers to add shared data content
to an app. This data content is shared with the consumers when they install
and use the app. To share data content, providers must grant privileges on the
shared data to the application package. Data content that providers share with
an application package is shared across all installed instances of the app.

Caution

Shared data content is not versioned, which means that all versions of an app
use the same data.

Consumers cannot access shared content directly. Instead, a provider creates a
secure view in the setup script of an application package and grants the
consumer access to the secure view. For details, see Allow consumers to access
shared objects in an app.

### Database objects that can be shared¶

The Snowflake Native App Framework allows providers to add the following
database objects to an application package:

  * Schemas

  * Tables, including external and Apache Iceberg™ tables

  * Views

Note

When sharing database objects such as tables and views, you must also share
the schema that contains them.

The following restrictions apply to tables and views shared in an application
package:

  * Tables cannot have virtual columns, including policies containing Java, Python, or JavaScript code.

  * View definitions or virtual columns associated with them such as policies cannot contain calls to Java, Python, or JavaScript.

  * Shared tables cannot be temporary, volatile, or transient tables.

  * Cross-Cloud Auto-Fulfillment is not supported for apps that contain external or Apache Iceberg™ tables.

### Restrictions on sharing data content that contains policies¶

Some functions that are commonly referenced by policies, such as CURRENT_USER,
behave differently in the context of an app installed in a consumer account.
Although a policy defined by a provider might work correctly in the provider
account, it might not work correctly in the consumer account after the
consumer installs the app.

Snowflake recommends that providers define policies on the proxy views that
are specified in the setup script. Defining policies on the proxy views
ensures that the definition of the policies cannot be changed after an app is
installed. Defining policies on proxy views also ensures that during upgrades
running code continues to use the policies that were applied when the version
was created.

## Grant privileges on shared content to an application package¶

To include shared data content in an app, providers must grant privileges on
the object to be shared with the application package. When providers add an
object to an application package, by default, the object is private to the
application package and not visible when the app is installed.

To make objects visible to an app installed from the application package, use
the GRANT … TO SHARE IN APPLICATION PACKAGE command as shown in the following
example:

    
    
    CREATE APPLICATION PACKAGE app_package;
    
    GRANT USAGE ON SCHEMA app_package.shared_schema
      TO SHARE IN APPLICATION PACKAGE app_package;
    GRANT SELECT ON TABLE app_package.shared_schema.shared_table
      TO SHARE IN APPLICATION PACKAGE app_package;
    

Copy

In this example, the first command grants the USAGE privilege on the
`shared_schema` schema to the application package. This command allows the
schema to be shared with consumers. The second command grants the SELECT
privilege on the `shared_table` table within `shared_schema` to the
application package. This command allows consumers to query the table.

After a consumer installs an app from the application package `app_package`,
they can access the `shared_schema` and query the `shared_table`.

Note

When adding a shared object to an application package, you must also share the
schema that contains the object.

You can also share views with an app by using similar SQL commands.

## Grant privileges on objects outside the application package¶

To share a database object that exists outside the application package,
providers must create views in the application package that allow access the
object. You cannot share objects outside the application package directly with
app installed in the consumer account.

For example, to share a database that is outside the application package,
grant the REFERENCE_USAGE privilege on the database to the application package
as shown in the following example:

    
    
    GRANT REFERENCE_USAGE ON DATABASE other_db
      TO SHARE IN APPLICATION PACKAGE app_pkg;
    

Copy

After granting the REFERENCE_USAGE on the external database, a provider must
create a view within the application to references the shared objects as shown
in the following example:

    
    
    CREATE VIEW app_pkg.shared_schema.shared_view
      AS SELECT c1, c2, c3, c4
      FROM other_db.other_schema.other_table;
    

Copy

This command creates a view in the application package that references the
database, table, and schema that are outside the application package.

After creating the view, you must grant privileges on the schema and view to
the application as shown in the following example:

    
    
    GRANT USAGE ON SCHEMA app_pkg.shared_schema
      TO SHARE IN APPLICATION PACKAGE app_pkg;
    GRANT SELECT ON VIEW app_pkg.shared_schema.shared_view
      TO SHARE IN APPLICATION PACKAGE app_pkg;
    

Copy

## Allow consumers to access shared objects in an app¶

Database objects that are created in the setup script are directly accessible
to the app after installation. These include tables, functions, procedures,
and new view definitions,

However, by default, database objects shared with an application package are
not visible to consumers. To allow consumers to view and access data content,
the application package must create a secure view and grant the appropriate
privileges.

This approach offers the following advantages:

  * Creating the view in the setup script ensures that changes made directly to the shared objects, such as new columns, are not visible to the version of the Snowflake Native App being installed by the setup script. To allow access to changes to the object, providers must create a new version or patch for the app.

  * Creating the view in a versioned schema ensures that each version of the Snowflake Native App contains only the definition of the view for that version. This is important for upgrade scenarios.

To expose shared objects to a consumer, the setup script must include commands
to:

  * Install views within a versioned schema in the application package.

  * Grant access to those views to the consumer using an application role.

The following example describes how to use application roles to grant access
to shared objects within the setup script of the application package:

    
    
    CREATE APPLICATION ROLE app_user;
    
    CREATE OR ALTER VERSIONED SCHEMA inst_schema;
    GRANT USAGE ON SCHEMA inst_schema
      TO APPLICATION ROLE app_user;
    
    CREATE VIEW IF NOT EXISTS inst_schema.shared_view
      AS SELECT c1, c2, c3, c4
      FROM shared_schema.shared_table;
    
    GRANT SELECT ON VIEW inst_schema.shared_view
      TO APPLICATION ROLE app_user;
    

Copy

In this example, the view accesses content in the `shared_schema.shared_view`
and shares it with the application package.

Note

If a provider attempts to define a view that directly accesses shared data
content, such as a database object external to the application package,
Snowflake returns an error.

## Define policies on proxy views¶

Snowflake recommends that you create proxy views and define policies to
protect them within the setup script. Defining policies to protect the proxy
view ensures that the definition of policies cannot be changed after the
Snowflake Native App is installed. Defining policies on proxy views also
ensures that during upgrades running code continues to use the policies that
are applied when the upgraded version is created.

## Support for external and Apache Iceberg™ tables¶

The Snowflake Native App Framework allows providers to share [external
tables](../../user-guide/tables-external-intro) and [Apache Iceberg™
tables](../../user-guide/tables-iceberg) with consumers. The method for
sharing these types of tables is similar to normal tables in that providers
add views to the setup script and grant privileges on these views to an
application role.

Caution

External and Apache Iceberg™ tables might incur additional egress or ingress
costs to the provider or consumer if the backing object store is not in the
same region as the app listing.

The following restrictions and requirements apply when sharing an external or
Iceberg table:

  * External and Iceberg tables and views that access them are read-only for the app.

  * Cross-Cloud Auto-Fulfillment is not supported for apps that share external or Iceberg tables.

  * Consumers must allow the app to use an external or Iceberg table in the provider account before it is available to the app.

### Cross-Cloud Auto-Fulfillment is not supported¶

External and Iceberg tables are not supported for apps that have listings that
enable [Cross-Cloud Auto-Fulfillment](https://other-
docs.snowflake.com/collaboration/provider-listings-auto-fulfillment).

Note

To publish an app that uses external or Iceberg tables to multiple Snowflake
regions, providers must publish the listing to each region.

If a provider creates a listing for an app that includes an external or
Iceberg table, the ability to configure Cross-Cloud Auto-Fulfillment is
disabled in Snowight.

If a provider attempts to add a version or patch to an application package
that is the data product of a listing that has Cross-Cloud Auto-Fulfillment
configured, Snowflake returns an error.

### Add an external or Iceberg table to an app¶

In addition to adding an external or Iceberg table to the application package,
providers must perform the following:

  * Add an entry to the manifest file to enable external and Iceberg tables. See [Add an entry for external and Iceberg tables to the manifest](requesting-external-tables.html#label-native-apps-ext-table-manifest) for more information.

  * Providers can use the Python Permission SDK to allow consumers to use Snowsight to enable the app to access an external or Iceberg table. Alternately, providers can ask consumers to enable the external or Iceberg table manually. See [Request permissions to access external and Iceberg tables](requesting-external-tables.html#label-native-apps-ext-table-sdk) for more information.

## Use caution when revoking privileges on or dropping shared objects¶

Use caution when revoking privileges from shared objects in an application
package or when dropping shared objects. If an installed version of a
Snowflake Native App still requires access to those objects, the Snowflake
Native App might become unstable or fail.

## Considerations when granting the MONITOR or OPERATE privilege on dynamic
tables¶

Providers should use caution when granting the MONITOR or OPERATE privilege on
dynamic tables to an application role. These privileges allow the consumer to
view a dynamic table’s metadata, which might expose the implementation details
of the app. See [Privileges to view a dynamic table’s metadata](../../user-
guide/dynamic-tables-privileges.html#label-dynamic-tables-privileges-view-
metadata) for more information on what actions the consumer can perform.

## Revoke and drop permissions on shared objects¶

Use caution when revoking permissions on shared objects from an application
package or when dropping shared objects. If an installed version of the
Snowflake Native App still requires access to those objects, the Snowflake
Native App might become unstable or fail.

