[![Snowflake logo in black \(no text\)](../../../../_images/logo-snowflake-
black.png)](../../../../_images/logo-snowflake-black.png) Preview Feature —
Open

Available to accounts in all regions in all cloud providers (including
government regions). For details, contact your Snowflake representative.

# Tutorial: Native SDK for Connectors Java Template¶

## Introduction¶

Welcome to our tutorial on using a connector template utilizing Snowflake
Native SDK for Connectors. This guide will help you setup a simple Connector
Native Application.

In this tutorial you will learn how to:

  * Deploy a Connector Native Application

  * Configure a template connector to ingest data

  * Customize a template connector to your own needs

The template contains various helpful comments in the code to make it easier
for you to find specific files that need to be modified. Look for the comments
with the following keywords, they will guide you and help implement your own
connector:

  * `TODO`

  * `TODO: HINT`

  * `TODO: IMPLEMENT ME`

Before you begin this tutorial, you should prepare yourself by reviewing the
following recommended content:

  * [Snowflake Native SDK for Connectors](../about-connector-sdk)

  * [The Snowflake Labs quickstart for building and deploying a connector using Native Apps framework in Snowflake and Native Connectors SDK Java](https://quickstarts.snowflake.com/guide/connectors_native_sdk_java_example).

### Prerequisites¶

Before getting started please make sure that you meet the following
requirements:

  * Java 11 installed

  * access to Snowflake account with `ACCOUNTADMIN` role

  * [SnowSQL (CLI client)](../../../../user-guide/snowsql) tool with `variable_substitution` and `exit_on_error` configured in your local machine

  * Review this documentation page: [Snowflake Native SDK for Connectors](../about-connector-sdk) and keep it opened online or printed from your browser Review this quickstart: [Connector Native Java SDK](https://quickstarts.snowflake.com/guide/connectors_native_sdk_java_example) (optional, but recommended) The quickstart uses an example connector based on a template and it can be referenced to check out example implementations of various components.

## Initialization and deployment¶

To initialize a project, clone the [Native SDK for Connectors repository from
GitHub](https://github.com/snowflakedb/connectors-native-sdk) and copy the
`/templates/native-sdk-connectors-java-template` directory to the desired
project location. This template contains all the code required to deploy a
working Connector Native Application. Once this is done the template is ready
to be deployed.

### Deployment¶

The template is ready to be deployed out of the box and provides a convenience
script that handles the whole process for you. Before deploying the Connector,
a `snowsql` connection must be specified. To do so, open the `Makefile` and
put the name of the connection into the `CONNECTION` environmental variable.

To quickly deploy the application go into the main directory of the template
and execute the following command:

    
    
    make reinstall_application_from_version_dir
    

Copy

This command does the following things:

  * Removes previously existing `APPLICATION` and `APPLICATION PACKAGE` from the Snowflake account.

  * Copies the SDK jar and sql files extracted from the jar to the target `sf_build` directory.

  * Copies the custom streamlit and java components of the application to `sf_build` directory.

  * Creates a new `APPLICATION PACKAGE` from the files in `sf_build` directory inside a Snowflake account.

  * Creates a new `APPLICATION` instance inside a Snowflake account.

This process takes around 2-3 minutes to complete. After it is finished,
navigate to the `Data Products` -> `Apps` tab inside Snowflake, your Connector
should be visible there. If you have a lot of applications and have trouble
finding it, try typing `NATIVE_SDK_CONNECTOR_TEMPLATE` in the search bar, or
in the case of a custom `APPLICATION` name use the custom name instead. This
Connector is ready to be configured. The following steps guide you through the
process and explain how to customize each of the steps along the way.

If you need to redeploy your connector during any steps of this tutorial, for
example to test your changes, then just rerun the above command.

## Prerequisites step¶

Right after deployment the Connector is in its Wizard phase. This phase
consists of a few steps that guide the end user through all the necessary
configurations. The first step is the Prerequisites step. It is optional and
might not be necessary for every connector. Prerequisites are usually actions
required from the user outside of the application, for example running queries
through the worksheet, doing some configurations on the source system side,
etc.

Read more about prerequisites:

  * [Prerequisites](../flow/prerequisites)

The contents of each prerequisite are retrieved directly from the internal
table (`STATE.PREREQUISITES`) inside the connector. They can be customized
through the `setup.sql` script. However, keep in mind that the `setup.sql`
script is executed on every installation, upgrade and downgrade of the
application. The inserts must be idempotent, because of this it is recommended
to use merge query as in the example below:

    
    
    MERGE INTO STATE.PREREQUISITES AS dest
    USING (SELECT * FROM VALUES
               ('1',
                'Sample prerequisite',
                'Prerequisites can be used to notice the end user of the connector about external configurations. Read more in the SDK documentation below. This content can be modified inside `setup.sql` script',
                'https://docs.snowflake.com/developer-guide/native-apps/connector-sdk/flow/prerequisites',
                NULL,
                NULL,
                1
               )
    ) AS src (id, title, description, documentation_url, learnmore_url, guide_url, position)
    ON dest.id = src.id
    WHEN NOT MATCHED THEN
        INSERT (id, title, description, documentation_url, learnmore_url, guide_url, position)
        VALUES (src.id, src.title, src.description, src.documentation_url, src.learnmore_url, src.guide_url, src.position);
    

Copy

## Connector configuration step¶

The next step of the Wizard Phase is the connector configuration step. During
this step you can configure database objects and permissions required by the
connector. This step allows for the following configuration properties to be
specified:

  * `warehouse`

  * `destination_database`

  * `destination_schema`

  * `operational_warehouse`

  * `global_schedule`

  * `data_owner_role`

  * `agent_username`

  * `agent_role`

If you need any other custom properties, they can be configured in one of the
next steps of the Wizard phase. For more information on each of the properties
see:

  * [Connector configuration](../flow/connector_configuration)

Additionally, the streamlit component (`streamlit/wizard/connector_config.py`)
provided in the template shows how to trigger `permissions-sdk` and requests
some grants from the end-user. As long as the available properties satisfy the
needs of the connector then there is no need to overwrite any of the backend
classes, although this is still possible the same way as for the components in
the further steps of the configuration.

For more information on internal procedures and Java objects see:

  * [Connector configuration reference](../reference/connector_configuration_reference)

The provided streamlit example allows for requesting account level grants like
`create database` and `execute tasks`. It also allows the user to specify a
warehouse reference through the `permissions-sdk` popup.

In the template, the user is asked to only provide the `destination_database`
and `destination_schema`. However, a `TODO` comment in
`streamlit/wizard/connector_configuration.py` contains commented code that can
be reused to display more input boxes in the streamlit UI.

    
    
    # TODO: Here you can add additional fields in connector configuration. Supported values are the following: warehouse, operational_warehouse, data_owner_role, agent_role, agent_username
    # For example:
    st.subheader("Operational warehouse")
    input_col, _ = st.columns([2, 1])
    with input_col:
        st.text_input("", key="operational_warehouse", label_visibility="collapsed")
    st.caption("Name of the operational warehouse to be used")
    

Copy

## Connection configuration step¶

The next step of the Wizard Phase is the connection configuration step. This
step allows the end-user to configure external connectivity parameters for the
connector. This configuration may include identifiers of objects like secrets,
integrations, etc. Because this varies depending on the source system for the
data ingested by the connector, this is the first place where bigger
customizations have to be made in the source code.

For more information on connection configuration see:

  * [Connection configuration](../flow/connection_configuration)

  * [Connection configuration reference](../reference/connection_configuration_reference)

Starting with the streamlit UI side (`streamlit/wizard/connection_config.py`
file) you need to add text boxes for all needed parameters. An example text
box is implemented for you and if you search the code in this file, you can
find a `TODO` with commented code for a new field.

    
    
    # TODO: Additional configuration properties can be added to the UI like this:
    st.subheader("Additional connection parameter")
    input_col, _ = st.columns([2, 1])
    with input_col:
        st.text_input("", key="additional_connection_property", label_visibility="collapsed")
    st.caption("Some description of the additional property")
    

Copy

After the properties are added to the form, they need to be passed to the
backend layer of the connector. To do so, two additional places must be
modified in the streamlit files. The first one is the `finish_config` function
in the `streamlit/wizard/connection_config.py` file. The state of the newly
added text boxes must be read here. Additionally, it can be validated if
needed, and then passed to the `set_connection_configuration` function. For
example if `additional_connection_property` was added it would look like this
after the edits:

    
    
    def finish_config():
    try:
        # TODO: If some additional properties were specified they need to be passed to the set_connection_configuration function.
        # The properties can also be validated, for example, check whether they are not blank strings etc.
        response = set_connection_configuration(
            custom_connection_property=st.session_state["custom_connection_property"],
            additional_connection_property=st.session_state["additional_connection_property"],
        )
    
    # rest of the method without changes
    

Copy

Then the `set_connection_configuration` function must be edited, it can be
found in the `streamlit/native_sdk_api/connection_config.py` file. This
function is a proxy between streamlit UI and the underlying SQL procedure,
which is an entry points to the backend of the connector.

    
    
    def set_connection_configuration(custom_connection_property: str, additional_connection_property: str):
        # TODO: this part of the code sends the config to the backend so all custom properties need to be added here
        config = {
            "custom_connection_property": escape_identifier(custom_connection_property),
            "additional_connection_property": escape_identifier(additional_connection_property),
        }
    
        return call_procedure(
            "PUBLIC.SET_CONNECTION_CONFIGURATION",
            [variant_argument(config)]
        )
    

Copy

After doing this the new property is saved in the internal connector table,
which contains configuration. However, this is not the end of the possible
customisations. Some backend components can be customized too, look for the
following comments in the code to find them:

  * `TODO: IMPLEMENT ME connection configuration validate`

  * `TODO: IMPLEMENT ME connection callback`

  * `TODO: IMPLEMENT ME test connection`

The validate part allows for any additional validation on the data received
from the UI. It can also transform the data for example like making them lower
case, trimming or checking that objects with provided names actually exist
inside Snowflake.

Connection callback is a part that lets you perform any additional operation
based on the config, for example alter procedures that need to use external
access integrations.

Test connection is a final component of the connection configuration, it
checks whether the connection can be established between the connector and the
source system.

For more information on those internal components see:

  * [Connection configuration](../flow/connection_configuration)

  * [Connection configuration reference](../reference/connection_configuration_reference)

Example implementations might look like this:

    
    
    public class TemplateConfigurationInputValidator implements ConnectionConfigurationInputValidator {
    
        private static final String ERROR_CODE = "INVALID_CONNECTION_CONFIGURATION";
    
        @Override
        public ConnectorResponse validate(Variant config) {
          // TODO: IMPLEMENT ME connection configuration validate: If the connection configuration input
          // requires some additional validation this is the place to implement this logic.
          // See more in docs:
          // https://docs.snowflake.com/developer-guide/native-apps/connector-sdk/reference/connection_configuration_reference
          // https://docs.snowflake.com/developer-guide/native-apps/connector-sdk/flow/connection_configuration
          var integrationCheck = checkParameter(config, INTEGRATION_PARAM, false);
          if (!integrationCheck.isOk()) {
            return integrationCheck;
          }
    
          var secretCheck = checkParameter(config, SECRET_PARAM, true);
          if (!secretCheck.isOk()) {
            return ConnectorResponse.error(ERROR_CODE);
          }
    
          return ConnectorResponse.success();
        }
    }
    

Copy

    
    
    public class TemplateConnectionConfigurationCallback implements ConnectionConfigurationCallback {
    
        private final Session session;
    
        public TemplateConnectionConfigurationCallback(Session session) {
          this.session = session;
        }
    
        @Override
        public ConnectorResponse execute(Variant config) {
          // TODO: If you need to alter some procedures with external access you can use
          // configureProcedure method or implement a similar method on your own.
          // TODO: IMPLEMENT ME connection callback: Implement the custom logic of changes in application
          // to be done after connection configuration, like altering procedures with external access.
          // See more in docs:
          // https://docs.snowflake.com/developer-guide/native-apps/connector-sdk/reference/connection_configuration_reference
          // https://docs.snowflake.com/developer-guide/native-apps/connector-sdk/flow/connection_configuration
          configureProcedure(format("PUBLIC.TEST_CONNECTION()"), config);
    
          return ConnectorResponse.success();
        }
    }
    

Copy

    
    
    public class TemplateConnectionValidator {
    
        private static final String ERROR_CODE = "TEST_CONNECTION_FAILED";
    
        public static Variant testConnection(Session session) {
          // TODO: IMPLEMENT ME test connection: Implement the custom logic of testing the connection to
          // the source system here. This usually requires connection to some webservice or other external
          // system. It is suggested to perform only the basic connectivity validation here.
          // If that's the case then this procedure must be altered in TemplateConnectionConfigurationCallback first.
          // See more in docs:
          // https://docs.snowflake.com/developer-guide/native-apps/connector-sdk/reference/connection_configuration_reference
          // https://docs.snowflake.com/developer-guide/native-apps/connector-sdk/flow/connection_configuration
          return test().toVariant();
        }
    
        private static ConnectorResponse test() {
          try {
            var response = SourceSystemHttpHelper.testEndpoint();
    
            if (isSuccessful(response.statusCode())) {
              return ConnectorResponse.success();
            } else {
              return ConnectorResponse.error(ERROR_CODE, "Connection to source system failed");
            }
          } catch (Exception exception) {
            return ConnectorResponse.error(ERROR_CODE, "Test connection failed");
          }
        }
    }
    

Copy

## Finalize configuration step¶

Thr finalize connector configuration step is the final step of the Wizard
Phase. This step has multiple responsibilities. First, it allows user to
specify any additional configuration needed by the connector. Second, it
creates sink database, schema and if needed some tables and views for the
ingested data. Lastly, it initializes internal components such as scheduler
and task reactor.

For more information on configuration finalization please see:

  * [Finalize configuration](../flow/finalize_configuration)

  * [Finalize configuration reference](../reference/finalize_configuration_reference)

For more information on task reactor and scheduling please see:

  * [Task reactor](../using/task_reactor)

  * [Task reactor SQL reference](../reference/task_reactor_reference)

  * [Ingestion scheduler](../using/scheduler)

  * [Ingestion scheduler reference](../reference/scheduler_reference)

Similarly to the connection configuration step, customisation can be started
with the streamlit UI. `streamlit/wizard/finalize_config.py` contains a form
with an example property. More properties can be added according to the
connector needs. To add another property look for a `TODO` comment, that
contains example code of adding a new property in the mentioned file.

    
    
    # TODO: Here you can add additional fields in finalize connector configuration.
    # For example:
    st.subheader("Some additional property")
    input_col, _ = st.columns([2, 1])
    with input_col:
        st.text_input("", key="some_additional_property", label_visibility="collapsed")
    st.caption("Description of some new additional property")
    

Copy

After adding the text box for a new property it needs to be passed to the
backend. To do so, modify the `finalize_configuration` function in the same
file:

    
    
    def finalize_configuration():
        try:
            st.session_state["show_main_error"] = False
            # TODO: If some additional properties were introduced, they need to be passed to the finalize_connector_configuration function.
            response = finalize_connector_configuration(
                st.session_state.get("custom_property"),
                st.session_state.get("some_additional_property")
            )
    

Copy

Next, open `streamlit/native_sdk_api/finalize_config.py` and add it to the
following function:

    
    
    def finalize_connector_configuration(custom_property: str, some_additional_property: str):
        # TODO: If some custom properties were configured, then they need to be specified here and passed to the FINALIZE_CONNECTOR_CONFIGURATION procedure.
        config = {
            "custom_property": custom_property,
            "some_additional_property": some_additional_property,
        }
        return call_procedure(
            "PUBLIC.FINALIZE_CONNECTOR_CONFIGURATION",
            [variant_argument(config)]
        )
    

Copy

Again, similarly to the connection configuration step, this step also allows
for the customisation of various backend components, they can be found using
the following phrases in code:

  * `TODO: IMPLEMENT ME validate source`

  * `TODO: IMPLEMENT ME finalize internal`

The validate source part is responsible for performing more sophisticated
validations on the source systems. If the previous test connection only
checked that a connection can be established, then validate source could check
access to specific data in the system, for example, extracting a single record
of data.

Finalize internal is an internal procedure responsible for initializing task
reactor and scheduler, creating a sink database and necessary nested objects.
It can also be used to save the configuration provided during the finalize
step (this configuration is not saved by default).

More information on the internal components can be found in:

  * [Finalize configuration](../flow/finalize_configuration)

  * [Finalize configuration reference](../reference/finalize_configuration_reference)

Additionally, input can be validated using `FinalizeConnectorInputValidator`
interface and providing it to the finalize handler (check the
`TemplateFinalizeConnectorConfigurationCustomHandler`). More information on
using builders can be found in:

  * [Stored procedures and handlers customization](../using/sproc_and_handlers_customization)

Example implementation of the validate source might look like this:

    
    
    public class SourceSystemAccessValidator implements SourceValidator {
    
        @Override
        public ConnectorResponse validate(Variant variant) {
          // TODO: IMPLEMENT ME validate source: Implement the custom logic of validating the source
          // system. In some cases this can be the same validation that happened in
          // TemplateConnectionValidator.
          // However, it is suggested to perform more complex validations, like specific access rights to
          // some specific resources here.
          // See more in docs:
          // https://docs.snowflake.com/developer-guide/native-apps/connector-sdk/reference/finalize_configuration_reference
          // https://docs.snowflake.com/developer-guide/native-apps/connector-sdk/flow/finalize_configuration
          var finalizeProperties = Configuration.fromCustomConfig(variant);
    
          var httpResponse = SourceSystemHttpHelper.validateSource(finalizeProperties.get("custom_property"));
          return prepareConnectorResponse(httpResponse.statusCode());
        }
    
        private ConnectorResponse prepareConnectorResponse(int statusCode) {
          switch (statusCode) {
            case 200:
              return ConnectorResponse.success();
            case 401:
              return ConnectorResponse.error("Unauthorized error");
            case 404:
              return ConnectorResponse.error("Not found error");
            default:
              return ConnectorResponse.error("Unknown error");
          }
        }
    }
    

Copy

## Create resources¶

After the Wizard Phase is completed, the connector is ready to start ingesting
data. But first, resources must be implemented and configured. A resource is
an abstraction describing a specific set of data in the source system, for
example a table, an endpoint, a file, etc.

Various source systems might need various information about a resource, for
that reason, a resource definition needs to be customized according to the
specific needs. To do so, go to the `streamlit/daily_use/data_sync_page.py`
file. There you can find a `TODO` about adding text boxes for resource
parameters. The resource parameters should allow for the identification and
retrieval of data from the source system. Those parameters can be then
extracted during the ingestion:

    
    
    # TODO: specify all the properties needed to define a resource in the source system. A subset of those properties should allow for a identification of a single resource, be it a table, endpoint, repository or some other data storage abstraction
    st.text_input(
        "Resource name",
        key="resource_name",
    )
    st.text_input(
        "Some resource parameter",
        key="some_resource_parameter"
    )
    

Copy

Once all necessary properties are added to the form, they can be passed to the
backend. First, the state of the text fields has to be extracted and passed to
the API level `queue_resource` method in
`streamlit/daily_use/data_sync_page.py`:

    
    
    def queue_resource():
        # TODO: add additional properties here and pass them to create_resource function
        resource_name = st.session_state.get("resource_name")
        some_resource_parameter = st.session_state.get("some_resource_parameter)
    
        if not resource_name:
            st.error("Resource name cannot be empty")
            return
    
        result = create_resource(resource_name, some_resource_parameter)
        if result.is_ok():
            st.success("Resource created")
        else:
            st.error(result.get_message())
    

Copy

Then `create_resource` function from the
`streamlit/native_sdk_api/resource_management.py` needs to be updated:

    
    
    def create_resource(resource_name, some_resource_parameter):
        ingestion_config = [{
            "id": "ingestionConfig",
            "ingestionStrategy": "INCREMENTAL",
            # TODO: HINT: scheduleType and scheduleDefinition are currently not supported out of the box, due to globalSchedule being used. However, a custom implementation of the scheduler can use those fields. They need to be provided becuase they are mandatory in the resourceDefinition.
            "scheduleType": "INTERVAL",
            "scheduleDefinition": "60m"
        }]
        # TODO: HINT: resource_id should allow identification of a table, endpoint etc. in the source system. It should be unique.
        resource_id = {
            "resource_name": resource_name,
        }
        id = f"{resource_name}_{random_suffix()}"
    
        # TODO: if you specified some additional resource parameters then you need to put them inside resource metadata:
        resource_metadata = {
            "some_resource_parameter": some_resource_parameter
        }
    
        return call_procedure("PUBLIC.CREATE_RESOURCE",
                              [
                                  varchar_argument(id),
                                  variant_argument(resource_id),
                                  variant_list_argument(ingestion_config),
                                  varchar_argument(id),
                                  "true",
                                  variant_argument(resource_metadata)
                              ])
    

Copy

### Customizing CREATE_RESOURCE() procedure logic¶

The `PUBLIC.CREATE_RESOURCE()` procedure allows the developer to customize
its’ execution by implementing an own logic that is plugged in to several
places of the main execution flow. The SDK allows the developer to:

  1. Validate the resource before it’s created. The logic should be implemented in `PUBLIC.CREATE_RESOURCE_VALIDATE()` procedure.

  2. Do some custom operations before the resource is created. The logic should be implemented in `PUBLIC.PRE_CREATE_RESOURCE()` procedure.

  3. Do some custom operations after the resource is created. The logic should be implemented in `PUBLIC.POST_CREATE_RESOURCE()` procedure.

More information about `PUBLIC.CREATE_RESOURCE()` procedure customization can
be found here:

  * [Create resource](../flow/ingestion-management/create_resource)

  * [Create resource reference](../reference/create_resource_reference)

#### TemplateCreateResourceHandler.java¶

This class is a handler for the `PUBLIC.CREATE_RESOURCE()` procedure. Here,
you can inject the Java implementations of handlers for callback procedures
mentioned before. By default, the Template provides mocked Java
implementations of callback handlers in order to get rid of calling SQL
procedures that extend whole procedure execution time. Java implementations
make the execution faster. These mocked implementations do nothing apart from
returning a success response. You can either provide the custom implementation
to the callback classes prepared by the template or create these callbacks
from scratch and inject them to the main procedure execution flow in the
handler builder.

In order to implement the custom logic to callback methods that are called by
default, look for the following phrases in the code:

  * `TODO: IMPLEMENT ME create resource validate`

  * `TODO: IMPLEMENT ME pre create resource callback`

  * `TODO: IMPLEMENT ME post create resource callback`

## Ingestion¶

To perform ingestion of data you need to implement a class that will handle
the connection with the source system and retrieve data, based on the resource
configuration. Scheduler and Task Reactor modules will take care of triggering
and queueing of ingestion tasks.

Ingestion logic is invoked from the `TemplateIngestion` class, look for `TODO:
IMPLEMENT ME ingestion` in the code and replace the random data generation
with the data retrieval from the source system. If you added some custom
properties to the resource definition, they can be fetched from the internal
connectors tables using `ResourceIngestionDefinitionRepository` and properties
available in the `TemplateWorkItem`:

  * `resourceIngestionDefinitionId`

  * `ingestionConfigurationId`

For example retrieving data from some webservice MIGHT look like this:

    
    
    public final class SourceSystemHttpHelper {
    
      private static final String DATA_URL = "https://source_system.com/data/%s";
      private static final SourceSystemHttpClient sourceSystemClient = new SourceSystemHttpClient();
      private static final ObjectMapper objectMapper = new ObjectMapper();
    
      private static List<Variant> fetchData(String resourceId) {
        var response = sourceSystemClient.get(String.format(url, resourceId));
        var body = response.body();
    
        try {
            return Arrays.stream(objectMapper.readValue(body, Map[].class))
                  .map(Variant::new)
                  .collect(Collectors.toList());
        } catch (JsonProcessingException e) {
          throw new RuntimeException("Cannot parse json", e);
        }
      }
    }
    

Copy

    
    
    public class SourceSystemHttpClient {
    
      private static final Duration REQUEST_TIMEOUT = Duration.ofSeconds(15);
    
      private final HttpClient client;
      private final String secret;
    
      public SourceSystemHttpClient() {
        this.client = HttpClient.newHttpClient();
        this.secret =
            SnowflakeSecrets.newInstance()
                .getGenericSecretString(ConnectionConfiguration.TOKEN_NAME);
      }
    
      public HttpResponse<String> get(String url) {
        var request =
            HttpRequest.newBuilder()
                .uri(URI.create(url))
                .GET()
                .header("Authorization", format("Bearer %s", secret))
                .header("Content-Type", "application/json")
                .timeout(REQUEST_TIMEOUT)
                .build();
    
        try {
          return client.send(request, HttpResponse.BodyHandlers.ofString());
        } catch (IOException | InterruptedException ex) {
          throw new RuntimeException(format("HttpRequest failed: %s", ex.getMessage()), ex);
        }
      }
    }
    

Copy

## Manage resources lifecycle¶

Once the logic of creating resources and the their ingestion is implemented,
you can manage their lifecycle by the following procedures:

  1. `PUBLIC.ENABLE_RESOURCE()` \- this procedure enables a particular resource, meaning that it will be scheduled for ingestion

  2. `PUBLIC.DISABLE_RESOURCE()` \- this procedure disables a particular resource, meaning that its’ ingestion scheduling will be stopped

  3. `PUBLIC.UPDATE_RESOURCE()` \- this procedure allows to update the ingestion configurations of a particular resource. It isn’t implemented in the Streamlit UI by default because sometimes it may be undesirable by the developer to allow the connector user to customize the ingestion configuration (revoke grants on this procedure to application role `ACCOUNTADMIN` in order to disallow its’ usage completly).

All these procedures have Java handlers and are extended with callbacks that
allow to customize their execution. You can inject custom implementations of
callbacks using builder of these handlers. By default, the Template provides
mocked Java implementations of callback handlers in order to get rid of
calling SQL procedures that extend whole execution time of mentioned
procedures. These mocked implementations do nothing apart from returning a
success response. You can either provide the custom implementation to the
callback classes prepared by the template or create these callbacks from
scratch and inject them to the main procedure execution flow in the handler
builders.

### TemplateEnableResourceHandler.java¶

This class is a handler for the `PUBLIC.ENABLE_RESOURCE()` procedure, which
can be extended with the callbacks that are dedicated to:

  1. Validate the resource before it’s enabled. Look for `TODO: IMPLEMENT ME enable resource validate` phrase in the code in order to provide the custom implementation.

  2. Do some custom operations before the resource is enabled. Look for `TODO: IMPLEMENT ME pre enable resource` phrase in the code in order to provide the custom implementation.

  3. Do some custom operations after the resource is enabled. Look for `TODO: IMPLEMENT ME post enable resource` phrase in the code in order to provide the custom implementation.

Learn more from the `PUBLIC.ENABLE_RESOURCE()` procedure detailed
documentations:

  * [Enable resource](../flow/ingestion-management/enable_resource)

  * [Enable resource reference](../reference/enable_resource_reference)

### TemplateDisableResourceHandler.java¶

This class is a handler for the `PUBLIC.DISABLE_RESOURCE()` procedure, which
can be extended with the callbacks that are dedicated to:

  1. Validate the resource before it’s disabled. Look for `TODO: IMPLEMENT ME disable resource validate` phrase in the code in order to provide the custom implementation.

  2. Do some custom operations before the resource is disabled. Look for `TODO: IMPLEMENT ME pre disable resource` phrase in the code in order to provide the custom implementation.

Learn more from the `PUBLIC.DISABLE_RESOURCE()` procedure detailed
documentations:

  * [Disable resource](../flow/ingestion-management/disable_resource)

  * [Disable resource reference](../reference/disable_resource_reference)

### TemplateUpdateResourceHandler.java¶

This class is a handler for the `PUBLIC.UPDATE_RESOURCE()` procedure, which
can be extended with the callbacks that are dedicated to:

  1. Validate the resource before it’s updated. Look for `TODO: IMPLEMENT ME update resource validate` phrase in the code in order to provide the custom implementation.

  2. Do some custom operations before the resource is updated. Look for `TODO: IMPLEMENT ME pre update resource` phrase in the code in order to provide the custom implementation.

  3. Do some custom operations after the resource is updated. Look for `TODO: IMPLEMENT ME post update resource` phrase in the code in order to provide the custom implementation.

Learn more from the `PUBLIC.UPDATE_RESOURCE()` procedure detailed
documentations:

  * [Update resource](../flow/ingestion-management/update_resource)

  * [Update resource reference](../reference/update_resource_reference)

## Settings¶

The template contains a settings tab that lets you view all the configuration
made before. However, if configuration properties were customized, then this
view also needs some customisations. Settings tab code can be found in the
`streamlit/daily_use/settings_page.py` file. To customize it, simply extract
the values from the configuration for the keys that were added in the
respective configurations.

For example, if earlier `additional_connection_property` was added in the
connection configuration step, then it could be added like this:

    
    
    def connection_config_page():
        current_config = get_connection_configuration()
    
        # TODO: implement the display for all the custom properties defined in the connection configuration step
        custom_property = current_config.get("custom_connection_property", "")
        additional_connection_property = current_config.get("additional_connection_property", "")
    
    
        st.header("Connector configuration")
        st.caption("Here you can see the connector connection configuration saved during the connection configuration step "
                   "of the Wizard. If some new property was introduced it has to be added here to display.")
        st.divider()
    
        st.text_input(
            "Custom connection property:",
            value=custom_property,
            disabled=True
        )
        st.text_input(
            "Additional connection property:",
            value=additional_connection_property,
            disabled=True
        )
        st.divider()
    

Copy

