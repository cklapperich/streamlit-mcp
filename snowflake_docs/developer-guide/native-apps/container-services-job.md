# Add job services to an app¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) Feature — Generally
Available

The Snowflake Native App Framework is generally available on supported cloud
platforms. For additional information, see [Support for private connectivity,
VPS, and government regions](limitations.html#label-native-apps-supported-
clouds).

This topic describes how to create and manage job services within a Snowflake
Native App with Snowpark Container Services. For information on using services
in an app, see Add job services to an app.

A Snowflake Native App with Snowpark Container Services can run a Snowpark
Container Services job service.

A service created using [CREATE SERVICE](../../sql-reference/sql/create-
service) is long-running. An app must explicitly stop the service when it is
no longer needed. In contrast, a job service created using [EXECUTE JOB
SERVICE](../../sql-reference/sql/execute-job-service) is a service that
terminates when the code of the service exits, similar to a stored procedure.
When all containers exit, the job is done.

Job services run synchronously. The [EXECUTE JOB SERVICE](../../sql-
reference/sql/execute-job-service) command completes after all containers
exit.

## Execute a job service in an app¶

To execute a job service in an app, add the [EXECUTE JOB SERVICE](../../sql-
reference/sql/execute-job-service) command to the setup script.

The following example shows how to execute a job service in the context of a
Snowflake Native App with Snowpark Container Services:

    
    
    EXECUTE JOB SERVICE
      IN COMPUTE POOL consumer_compute_pool
      FROM SPECIFICATION_FILE = 'job_service.yml'
      NAME = 'services_schema.job_service'
    
    GRANT MONITOR ON SERVICE services.job_service TO APPLICATION ROLE app_public;
    

Copy

Note

Note that the command parameters must be specified in the order shown in this
example.

When called from the setup script, the [EXECUTE JOB SERVICE](../../sql-
reference/sql/execute-job-service) command creates a job in a compute pool in
the consumer account.

If the consumer creates the compute pool manually, they must grant the USAGE
privilege on the compute pool to the app before this command will succeed.
Therefore, providers must include logic in a stored procedure that tests if
the correct privileges have been granted before running the [EXECUTE JOB
SERVICE](../../sql-reference/sql/execute-job-service).

The `FROM SPECIFICATION_FILE =` clause specifies the relative path to the
service specification file on a stage. See [Create the service specification
file](container-containers.html#label-native-apps-cont-service-spec) for more
information.

The `NAME =` clause specifies the identifier for the job service. The name of
this job service must be unique within the schema where it is located.

Note

Job services cannot be executed within a version schema.

The `NAME =` clause should use the schema and name of the job within the
application. For , `services_schema.job_service` If the schema name is not
specified the job service is created in the schema of the stored procedure or
function that is executing the job service.

## Monitor a job service in an app¶

To monitor the status of a job service within an app, use the
[SYSTEM$GET_SERVICE_STATUS — Deprecated](../../sql-
reference/functions/system_get_service_status) command as shown in the
following example:

    
    
    CALL SYSTEM$GET_SERVICE_STATUS('schema.job_name')
    

Copy

This system function returns a JSON object that contains information about the
specified job service within the app. Providers can call this system function
from within the app to determine if the services has started or failed.

Consumers can also call this system function to determine the status of a
service. This requires that providers grant the MONITOR privilege on the
service an application role. See Execute a job service in an app for more
information.

## Accessing local container logs¶

To obtain the system logs for a job service within an app, use the
[SYSTEM$GET_SERVICE_LOGS](../../sql-
reference/functions/system_get_service_logs) system function as shown in the
following example:

    
    
    CALL SYSTEM$GET_SERVICE_LOGS('schema.job_name', 'instance_id', 'container_name'[, 10])
    

Copy

Providers can call this system function from within an app. In this context,
the provider does not have to specify the `app_name` as part of the fully
qualified job name.

Consumers can also run this system command. This requires that providers grant
the MONITOR privilege on the service to an application role. See Execute a job
service in an app for more information.

