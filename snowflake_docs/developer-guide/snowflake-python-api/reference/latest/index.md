# Snowflake API Reference (Python)¶

Snowflake API (Python) allows you to manage Snowflake resources by using
Python APIs. For more information, see the [Snowflake API Developer Guide for
Python](https://docs.snowflake.com/developer-guide/snowflake-python-
api/snowflake-python-overview).

## Overview¶

The Snowflake platform has a rich [SQL command
API](https://docs.snowflake.com/en/sql-reference-commands) which lets you
interact with Snowflake entities, creating, deleting, modifying them, and
more. The library described here, called the “Snowflake Python API” (or
“SnowAPI” for short) provides the same functionality using the Python
language.

Here is a quick overview of the concepts, classes, and functionality for using
Python to interact with the Snowflake platform, in most cases eliminating the
need to write SQL, or use the [Python SQL
connector](https://docs.snowflake.com/developer-guide/python-connector/python-
connector).

### Connecting to Snowflake¶

Before you begin, you must define your connection to Snowflake.

Note

Snowflake is actively evolving the connection definition mechanism, to make it
easier and safer to define your connections. These instructions will change
before the public release of SnowAPI.

You can define your connection information in a dictionary in your code [1]
like so:

    
    
    >>> connection_parameters = dict(
    ...    account = 'your account name',
    ...    user = 'your user name',
    ...    password = 'your password',
    ...    database = 'database name',
    ...    schema = 'schema name',
    ...    role = 'role if needed',
    ...    warehouse = 'warehouse name',
    ... )
    

Copy

You then use this connection information to create a session:

    
    
    >>> session = Session.builder.configs(connection_parameters).create()
    

Copy

### The root resource¶

The SnowAPI is organized as a tree of resources, modeling the resources
available in the Snowflake REST API [2]. You’ll need to first instantiate
_root_ of this resource tree in order to interact with other Snowflake
objects:

    
    
    >>> from snowflake.core import Root
    >>> root = Root(session)
    

Copy

When instantiating the root object, you need to either pass in a session, as
shown here, or a
[SnowflakeConnection](https://docs.snowflake.com/en/developer-guide/python-
connector/python-connector-api#object-connection) object.

### Local references vs Snowflake snapshots¶

There are two important concepts that help you understand how the SnowAPI
library functions. Python objects that you create and interact with are either
local references (a.k.a. handles), or snapshots of state stored on Snowflake.
This separation is made because communicating with Snowflake incurs costs -
network activity and performance costs, but also usage credit costs. For this
reason SnowAPI exposes explicit operations when it talks to Snowflake.

In general, if you act on or retrieve information from Snowflake, you do so
through a local, in-memory reference object. These references do not
synchronize with Snowflake until you call a given method. Calling a method is
a good indication of communication with Snowflake, which incurs some or all of
the costs outlined above. Other operations on in-memory references incur no
such costs.

We’ll call out these differences as we explore more examples.

## Example: create a task in Snowflake¶

In this example, we’ll step through creating a
[task](https://docs.snowflake.com/en/sql-reference/commands-stream) in
Snowflake, providing its definition, naming it, pushing it to Snowflake, as
well as suspending, resuming, and deleting the task.

In order to create a task, we first create a task object describing the task.
We’ll give it a name, a definition, and a schedule to run. Because this is a
local reference, this task definition lives only on the client side; it has
not been pushed to Snowflake.

    
    
    >>> from snowflake.core.task import Task
    >>> from datetime import timedelta
    >>> task_definition = Task(
    ...     'task1', definition='select 1', schedule=timedelta(hours=1))
    ... )
    

Copy

This `task_definition` object isn’t a local reference per se, it’s simply a
Python object that holds a description of the task which can be pushed to
Snowflake in order to create the task.

This task definition must be pushed into Snowflake before it can execute. As
you can see from the SQL [CREATE TASK](https://docs.snowflake.com/en/sql-
reference/sql/create-task) documentation, task creation requires a schema. In
Python terms, this means that creating a new task must happen relative to an
existing schema object. Schemas in turn are relative to a database.

Before we can create the task in Snowflake, we need to build a local path to
the database and schema where the task will be created. This is done by using
mapping-like syntax in various collections, rooted at the `root` object.
Here’s how we build a path to a schema named “public” in the database named
“my_db”. Note most importantly that this is purely local; no communication
with Snowflake occurs.

    
    
    >>> schema = root.databases['my_db'].schemas['public']
    >>> print(schema.name)
    public
    >>> print(schema.database.name)
    my_db
    

Copy

As you can see, these are just the local reference objects for the database
and schema, and accessing their attributes just parrots the `name` attributes
back to you as you gave them. Now we’re ready to push this task definition
into Snowflake:

    
    
    >>> task_reference = schema.tasks.create(task_definition)
    

Copy

This method call communicates with Snowflake.

This object actually _is_ the local reference object, and it holds a handle to
the task object created in Snowflake. But its properties haven’t been
retrieved from Snowflake yet. In order to do that, we have to make a call on
the reference object, returning a “snapshot” object which _does_ contain the
properties of the newly created task. You’ll see this pattern often, where
_fetching_ the snapshot communicates with Snowflake, retrieving the properties
of the referenced object.

    
    
    >>> task_reference.name
    'task1'
    

Copy

    
    
    >>> task = task_reference.fetch()
    >>> task.name
    'TASK1'
    

Copy

Notice that the name on the reference object is lower case while the name on
the task snapshot object is upper case. That’s because Snowflake stores the
task name in upper case and the `.fetch()` call sync’d this value to the local
snapshot object.

Note

Be aware that this snapshot is only guaranteed to be current as of the moment
the `.fetch()` executes. After that, changes to underlying Snowflake objects
are not reflected in the local snapshot objects. You must call `.fetch()`
again to re-sync the data locally.

The snapshot task object has additional attributes on it, such as the task
schedule:

    
    
    >>> task.schedule
    datetime.timedelta(seconds=3600)
    

Copy

and the task’s schema name (notice the upper case again here):

    
    
    >>> task.schema_name
    'PUBLIC'
    

Copy

The task reference object has some additional attributes and methods too. You
can get the task’s fully qualified name:

    
    
    >>> task_reference.fully_qualified_name
    'my_db.public.task1'
    

Copy

You can also execute, resume, and suspend the task by using methods on the
task reference object:

    
    
    >>> task_reference.resume()
    >>> task_reference.suspend()
    >>> task_reference.execute()
    

Copy

You can also delete the task by using the task reference object.

    
    
    >>> task_reference.delete()
    

Copy

Of course, once you’ve done this, you can’t resume, suspend, or execute the
task, because it no longer exists. You also can’t call `.fetch()` to get the
latest snapshop object. All of these operations return `404 Not Found`
exceptions (note that the full traceback is omitted here):

    
    
    >>> task_reference.execute()
    ...
    snowflake.core.exceptions.NotFoundError: (404)
    Reason: None
    HTTP response headers: HTTPHeaderDict({'Content-Type': 'application/json'})
    HTTP response body: {"error_code": "404", ... }
    

Copy

  * [snowflake.core](_autosummary/snowflake.core)
    * [snowflake.core.simple_file_logging](_autosummary/snowflake.core.simple_file_logging)
    * [snowflake.core.Clone](_autosummary/snowflake.core.Clone)
    * [snowflake.core.CreateMode](_autosummary/snowflake.core.CreateMode)
    * [snowflake.core.DeleteMode](_autosummary/snowflake.core.DeleteMode)
    * [snowflake.core.PointOfTime](_autosummary/snowflake.core.PointOfTime)
    * [snowflake.core.PointOfTimeOffset](_autosummary/snowflake.core.PointOfTimeOffset)
    * [snowflake.core.PointOfTimeStatement](_autosummary/snowflake.core.PointOfTimeStatement)
    * [snowflake.core.PointOfTimeTimestamp](_autosummary/snowflake.core.PointOfTimeTimestamp)
    * [snowflake.core.Root](_autosummary/snowflake.core.Root)
  * [snowflake.core.exceptions](_autosummary/snowflake.core.exceptions)
    * [snowflake.core.exceptions.APIError](_autosummary/snowflake.core.exceptions.APIError)
    * [snowflake.core.exceptions.NotFoundError](_autosummary/snowflake.core.exceptions.NotFoundError)
    * [snowflake.core.exceptions.UnauthorizedError](_autosummary/snowflake.core.exceptions.UnauthorizedError)
    * [snowflake.core.exceptions.ForbiddenError](_autosummary/snowflake.core.exceptions.ForbiddenError)
    * [snowflake.core.exceptions.ServerError](_autosummary/snowflake.core.exceptions.ServerError)
    * [snowflake.core.exceptions.ConflictError](_autosummary/snowflake.core.exceptions.ConflictError)
    * [snowflake.core.exceptions.InvalidActionError](_autosummary/snowflake.core.exceptions.InvalidActionError)
    * [snowflake.core.exceptions.InvalidResponseError](_autosummary/snowflake.core.exceptions.InvalidResponseError)
    * [snowflake.core.exceptions.InvalidArgumentsError](_autosummary/snowflake.core.exceptions.InvalidArgumentsError)
    * [snowflake.core.exceptions.InvalidResultError](_autosummary/snowflake.core.exceptions.InvalidResultError)
    * [snowflake.core.exceptions.InvalidOperationError](_autosummary/snowflake.core.exceptions.InvalidOperationError)
    * [snowflake.core.exceptions.RetryTimeoutError](_autosummary/snowflake.core.exceptions.RetryTimeoutError)
    * [snowflake.core.exceptions.MissingModuleError](_autosummary/snowflake.core.exceptions.MissingModuleError)
    * [snowflake.core.exceptions.FileOperationError](_autosummary/snowflake.core.exceptions.FileOperationError)
    * [snowflake.core.exceptions.FilePutError](_autosummary/snowflake.core.exceptions.FilePutError)
    * [snowflake.core.exceptions.FileGetError](_autosummary/snowflake.core.exceptions.FileGetError)
  * [snowflake.core.database](_autosummary/snowflake.core.database)
    * [snowflake.core.database.Database](_autosummary/snowflake.core.database.Database)
    * [snowflake.core.database.DatabaseCollection](_autosummary/snowflake.core.database.DatabaseCollection)
    * [snowflake.core.database.DatabaseResource](_autosummary/snowflake.core.database.DatabaseResource)
  * [snowflake.core.schema](_autosummary/snowflake.core.schema)
    * [snowflake.core.schema.Schema](_autosummary/snowflake.core.schema.Schema)
    * [snowflake.core.schema.SchemaCollection](_autosummary/snowflake.core.schema.SchemaCollection)
    * [snowflake.core.schema.SchemaResource](_autosummary/snowflake.core.schema.SchemaResource)
  * [snowflake.core.task](_autosummary/snowflake.core.task)
    * [snowflake.core.task.Cron](_autosummary/snowflake.core.task.Cron)
    * [snowflake.core.task.StoredProcedureCall](_autosummary/snowflake.core.task.StoredProcedureCall)
    * [snowflake.core.task.Task](_autosummary/snowflake.core.task.Task)
    * [snowflake.core.task.TaskCollection](_autosummary/snowflake.core.task.TaskCollection)
    * [snowflake.core.task.TaskResource](_autosummary/snowflake.core.task.TaskResource)
    * [snowflake.core.task.TaskRun](_autosummary/snowflake.core.task.TaskRun)
  * [snowflake.core.task.context](_autosummary/snowflake.core.task.context)
    * [snowflake.core.task.context.TaskContext](_autosummary/snowflake.core.task.context.TaskContext)
  * [snowflake.core.task.dagv1](_autosummary/snowflake.core.task.dagv1)
    * [snowflake.core.task.dagv1.DAG](_autosummary/snowflake.core.task.dagv1.DAG)
    * [snowflake.core.task.dagv1.DAGTask](_autosummary/snowflake.core.task.dagv1.DAGTask)
    * [snowflake.core.task.dagv1.DAGRun](_autosummary/snowflake.core.task.dagv1.DAGRun)
    * [snowflake.core.task.dagv1.DAGOperation](_autosummary/snowflake.core.task.dagv1.DAGOperation)
  * [snowflake.core.compute_pool](_autosummary/snowflake.core.compute_pool)
    * [snowflake.core.compute_pool.ComputePool](_autosummary/snowflake.core.compute_pool.ComputePool)
    * [snowflake.core.compute_pool.ComputePoolCollection](_autosummary/snowflake.core.compute_pool.ComputePoolCollection)
    * [snowflake.core.compute_pool.ComputePoolResource](_autosummary/snowflake.core.compute_pool.ComputePoolResource)
  * [snowflake.core.account](_autosummary/snowflake.core.account)
    * [snowflake.core.account.Account](_autosummary/snowflake.core.account.Account)
    * [snowflake.core.account.AccountCollection](_autosummary/snowflake.core.account.AccountCollection)
    * [snowflake.core.account.AccountResource](_autosummary/snowflake.core.account.AccountResource)
  * [snowflake.core.managed_account](_autosummary/snowflake.core.managed_account)
    * [snowflake.core.managed_account.ManagedAccount](_autosummary/snowflake.core.managed_account.ManagedAccount)
    * [snowflake.core.managed_account.ManagedAccountCollection](_autosummary/snowflake.core.managed_account.ManagedAccountCollection)
    * [snowflake.core.managed_account.ManagedAccountResource](_autosummary/snowflake.core.managed_account.ManagedAccountResource)
  * [snowflake.core.image_repository](_autosummary/snowflake.core.image_repository)
    * [snowflake.core.image_repository.ImageRepository](_autosummary/snowflake.core.image_repository.ImageRepository)
    * [snowflake.core.image_repository.ImageRepositoryCollection](_autosummary/snowflake.core.image_repository.ImageRepositoryCollection)
    * [snowflake.core.image_repository.ImageRepositoryResource](_autosummary/snowflake.core.image_repository.ImageRepositoryResource)
  * [snowflake.core.service](_autosummary/snowflake.core.service)
    * [snowflake.core.service.ServiceSpec](_autosummary/snowflake.core.service.ServiceSpec)
    * [snowflake.core.service.GrantOf](_autosummary/snowflake.core.service.GrantOf)
    * [snowflake.core.service.Service](_autosummary/snowflake.core.service.Service)
    * [snowflake.core.service.ServiceCollection](_autosummary/snowflake.core.service.ServiceCollection)
    * [snowflake.core.service.ServiceResource](_autosummary/snowflake.core.service.ServiceResource)
    * [snowflake.core.service.ServiceSpecification](_autosummary/snowflake.core.service.ServiceSpecification)
    * [snowflake.core.service.ServiceSpecInlineText](_autosummary/snowflake.core.service.ServiceSpecInlineText)
    * [snowflake.core.service.ServiceSpecStageFile](_autosummary/snowflake.core.service.ServiceSpecStageFile)
    * [snowflake.core.service.JobService](_autosummary/snowflake.core.service.JobService)
    * [snowflake.core.service.ServiceContainer](_autosummary/snowflake.core.service.ServiceContainer)
    * [snowflake.core.service.ServiceEndpoint](_autosummary/snowflake.core.service.ServiceEndpoint)
    * [snowflake.core.service.ServiceInstance](_autosummary/snowflake.core.service.ServiceInstance)
    * [snowflake.core.service.ServiceRole](_autosummary/snowflake.core.service.ServiceRole)
    * [snowflake.core.service.ServiceRoleGrantTo](_autosummary/snowflake.core.service.ServiceRoleGrantTo)
  * [snowflake.core.pipe](_autosummary/snowflake.core.pipe)
    * [snowflake.core.pipe.Pipe](_autosummary/snowflake.core.pipe.Pipe)
    * [snowflake.core.pipe.PipeCollection](_autosummary/snowflake.core.pipe.PipeCollection)
    * [snowflake.core.pipe.PipeResource](_autosummary/snowflake.core.pipe.PipeResource)
  * [snowflake.core.external_volume](_autosummary/snowflake.core.external_volume)
    * [snowflake.core.external_volume.ExternalVolume](_autosummary/snowflake.core.external_volume.ExternalVolume)
    * [snowflake.core.external_volume.ExternalVolumeCollection](_autosummary/snowflake.core.external_volume.ExternalVolumeCollection)
    * [snowflake.core.external_volume.ExternalVolumeResource](_autosummary/snowflake.core.external_volume.ExternalVolumeResource)
    * [snowflake.core.external_volume.StorageLocationS3](_autosummary/snowflake.core.external_volume.StorageLocationS3)
    * [snowflake.core.external_volume.StorageLocationAzure](_autosummary/snowflake.core.external_volume.StorageLocationAzure)
    * [snowflake.core.external_volume.StorageLocationGcs](_autosummary/snowflake.core.external_volume.StorageLocationGcs)
    * [snowflake.core.external_volume.Encryption](_autosummary/snowflake.core.external_volume.Encryption)
    * [snowflake.core.external_volume.StorageLocationS3Gov](_autosummary/snowflake.core.external_volume.StorageLocationS3Gov)
  * [snowflake.core.table](_autosummary/snowflake.core.table)
    * [snowflake.core.table.Table](_autosummary/snowflake.core.table.Table)
    * [snowflake.core.table.TableResource](_autosummary/snowflake.core.table.TableResource)
    * [snowflake.core.table.TableCollection](_autosummary/snowflake.core.table.TableCollection)
    * [snowflake.core.table.TableColumn](_autosummary/snowflake.core.table.TableColumn)
    * [snowflake.core.table.ForeignKey](_autosummary/snowflake.core.table.ForeignKey)
    * [snowflake.core.table.PrimaryKey](_autosummary/snowflake.core.table.PrimaryKey)
    * [snowflake.core.table.UniqueKey](_autosummary/snowflake.core.table.UniqueKey)
    * [snowflake.core.table.Constraint](_autosummary/snowflake.core.table.Constraint)
  * [snowflake.core.warehouse](_autosummary/snowflake.core.warehouse)
    * [snowflake.core.warehouse.Warehouse](_autosummary/snowflake.core.warehouse.Warehouse)
    * [snowflake.core.warehouse.WarehouseCollection](_autosummary/snowflake.core.warehouse.WarehouseCollection)
    * [snowflake.core.warehouse.WarehouseResource](_autosummary/snowflake.core.warehouse.WarehouseResource)
  * [snowflake.core.database_role](_autosummary/snowflake.core.database_role)
    * [snowflake.core.database_role.DatabaseRole](_autosummary/snowflake.core.database_role.DatabaseRole)
    * [snowflake.core.database_role.DatabaseRoleCollection](_autosummary/snowflake.core.database_role.DatabaseRoleCollection)
    * [snowflake.core.database_role.DatabaseRoleResource](_autosummary/snowflake.core.database_role.DatabaseRoleResource)
    * [snowflake.core.database_role.ContainingScope](_autosummary/snowflake.core.database_role.ContainingScope)
    * [snowflake.core.database_role.Securable](_autosummary/snowflake.core.database_role.Securable)
    * [snowflake.core.database_role.Grant](_autosummary/snowflake.core.database_role.Grant)
  * [snowflake.core.cortex](_autosummary/snowflake.core.cortex)
  * [snowflake.core.cortex.search_service](_autosummary/snowflake.core.cortex.search_service)
    * [snowflake.core.cortex.search_service.CortexSearchServiceCollection](_autosummary/snowflake.core.cortex.search_service.CortexSearchServiceCollection)
    * [snowflake.core.cortex.search_service.QueryResponse](_autosummary/snowflake.core.cortex.search_service.QueryResponse)
    * [snowflake.core.cortex.search_service.QueryRequest](_autosummary/snowflake.core.cortex.search_service.QueryRequest)
    * [snowflake.core.cortex.search_service.CortexSearchServiceApi](_autosummary/snowflake.core.cortex.search_service.CortexSearchServiceApi)
    * [snowflake.core.cortex.search_service.CortexSearchServiceApiClient](_autosummary/snowflake.core.cortex.search_service.CortexSearchServiceApiClient)
    * [snowflake.core.cortex.search_service.CortexSearchServiceResource](_autosummary/snowflake.core.cortex.search_service.CortexSearchServiceResource)
  * [snowflake.core.dynamic_table](_autosummary/snowflake.core.dynamic_table)
    * [snowflake.core.dynamic_table.DownstreamLag](_autosummary/snowflake.core.dynamic_table.DownstreamLag)
    * [snowflake.core.dynamic_table.DynamicTable](_autosummary/snowflake.core.dynamic_table.DynamicTable)
    * [snowflake.core.dynamic_table.DynamicTableClone](_autosummary/snowflake.core.dynamic_table.DynamicTableClone)
    * [snowflake.core.dynamic_table.DynamicTableResource](_autosummary/snowflake.core.dynamic_table.DynamicTableResource)
    * [snowflake.core.dynamic_table.DynamicTableCollection](_autosummary/snowflake.core.dynamic_table.DynamicTableCollection)
    * [snowflake.core.dynamic_table.DynamicTableColumn](_autosummary/snowflake.core.dynamic_table.DynamicTableColumn)
    * [snowflake.core.dynamic_table.TargetLag](_autosummary/snowflake.core.dynamic_table.TargetLag)
    * [snowflake.core.dynamic_table.UserDefinedLag](_autosummary/snowflake.core.dynamic_table.UserDefinedLag)
  * [snowflake.core.function](_autosummary/snowflake.core.function)
    * [snowflake.core.function.Function](_autosummary/snowflake.core.function.Function)
    * [snowflake.core.function.FunctionArgument](_autosummary/snowflake.core.function.FunctionArgument)
    * [snowflake.core.function.FunctionCollection](_autosummary/snowflake.core.function.FunctionCollection)
    * [snowflake.core.function.FunctionResource](_autosummary/snowflake.core.function.FunctionResource)
    * [snowflake.core.function.ServiceFunction](_autosummary/snowflake.core.function.ServiceFunction)
  * [snowflake.core.grant](_autosummary/snowflake.core.grant)
    * [snowflake.core.grant.Grant](_autosummary/snowflake.core.grant.Grant)
    * [snowflake.core.grant.Grants](_autosummary/snowflake.core.grant.Grants)
    * [snowflake.core.grant.Grantee](_autosummary/snowflake.core.grant.Grantee)
    * [snowflake.core.grant.Grantees](_autosummary/snowflake.core.grant.Grantees)
    * [snowflake.core.grant.Privileges](_autosummary/snowflake.core.grant.Privileges)
    * [snowflake.core.grant.Securable](_autosummary/snowflake.core.grant.Securable)
    * [snowflake.core.grant.Securables](_autosummary/snowflake.core.grant.Securables)
  * [snowflake.core.notification_integration](_autosummary/snowflake.core.notification_integration)
    * [snowflake.core.notification_integration.NotificationHook](_autosummary/snowflake.core.notification_integration.NotificationHook)
    * [snowflake.core.notification_integration.NotificationEmail](_autosummary/snowflake.core.notification_integration.NotificationEmail)
    * [snowflake.core.notification_integration.NotificationWebhook](_autosummary/snowflake.core.notification_integration.NotificationWebhook)
    * [snowflake.core.notification_integration.NotificationQueueAwsSnsOutbound](_autosummary/snowflake.core.notification_integration.NotificationQueueAwsSnsOutbound)
    * [snowflake.core.notification_integration.NotificationQueueAzureEventGridOutbound](_autosummary/snowflake.core.notification_integration.NotificationQueueAzureEventGridOutbound)
    * [snowflake.core.notification_integration.NotificationQueueGcpPubsubOutbound](_autosummary/snowflake.core.notification_integration.NotificationQueueGcpPubsubOutbound)
    * [snowflake.core.notification_integration.NotificationQueueAzureEventGridInbound](_autosummary/snowflake.core.notification_integration.NotificationQueueAzureEventGridInbound)
    * [snowflake.core.notification_integration.NotificationQueueGcpPubsubInbound](_autosummary/snowflake.core.notification_integration.NotificationQueueGcpPubsubInbound)
    * [snowflake.core.notification_integration.NotificationIntegration](_autosummary/snowflake.core.notification_integration.NotificationIntegration)
    * [snowflake.core.notification_integration.NotificationIntegrationCollection](_autosummary/snowflake.core.notification_integration.NotificationIntegrationCollection)
    * [snowflake.core.notification_integration.NotificationIntegrationResource](_autosummary/snowflake.core.notification_integration.NotificationIntegrationResource)
    * [snowflake.core.notification_integration.WebhookSecret](_autosummary/snowflake.core.notification_integration.WebhookSecret)
  * [snowflake.core.role](_autosummary/snowflake.core.role)
    * [snowflake.core.role.Role](_autosummary/snowflake.core.role.Role)
    * [snowflake.core.role.RoleCollection](_autosummary/snowflake.core.role.RoleCollection)
    * [snowflake.core.role.RoleResource](_autosummary/snowflake.core.role.RoleResource)
    * [snowflake.core.role.Securable](_autosummary/snowflake.core.role.Securable)
    * [snowflake.core.role.ContainingScope](_autosummary/snowflake.core.role.ContainingScope)
    * [snowflake.core.role.Grant](_autosummary/snowflake.core.role.Grant)
  * [snowflake.core.user](_autosummary/snowflake.core.user)
    * [snowflake.core.user.User](_autosummary/snowflake.core.user.User)
    * [snowflake.core.user.UserCollection](_autosummary/snowflake.core.user.UserCollection)
    * [snowflake.core.user.UserResource](_autosummary/snowflake.core.user.UserResource)
    * [snowflake.core.user.Securable](_autosummary/snowflake.core.user.Securable)
    * [snowflake.core.user.Grant](_autosummary/snowflake.core.user.Grant)
    * [snowflake.core.user.ContainingScope](_autosummary/snowflake.core.user.ContainingScope)
  * [snowflake.core.stage](_autosummary/snowflake.core.stage)
    * [snowflake.core.stage.Stage](_autosummary/snowflake.core.stage.Stage)
    * [snowflake.core.stage.StageResource](_autosummary/snowflake.core.stage.StageResource)
    * [snowflake.core.stage.StageCollection](_autosummary/snowflake.core.stage.StageCollection)
    * [snowflake.core.stage.AwsCredentials](_autosummary/snowflake.core.stage.AwsCredentials)
    * [snowflake.core.stage.AzureCredentials](_autosummary/snowflake.core.stage.AzureCredentials)
    * [snowflake.core.stage.Credentials](_autosummary/snowflake.core.stage.Credentials)
    * [snowflake.core.stage.FileTransferMaterial](_autosummary/snowflake.core.stage.FileTransferMaterial)
    * [snowflake.core.stage.PresignedUrlRequest](_autosummary/snowflake.core.stage.PresignedUrlRequest)
    * [snowflake.core.stage.StageDirectoryTable](_autosummary/snowflake.core.stage.StageDirectoryTable)
    * [snowflake.core.stage.StageEncryption](_autosummary/snowflake.core.stage.StageEncryption)
    * [snowflake.core.stage.StageFile](_autosummary/snowflake.core.stage.StageFile)
  * [snowflake.core.view](_autosummary/snowflake.core.view)
    * [snowflake.core.view.View](_autosummary/snowflake.core.view.View)
    * [snowflake.core.view.ViewResource](_autosummary/snowflake.core.view.ViewResource)
    * [snowflake.core.view.ViewCollection](_autosummary/snowflake.core.view.ViewCollection)
    * [snowflake.core.view.ViewColumn](_autosummary/snowflake.core.view.ViewColumn)
  * [snowflake.core.event_table](_autosummary/snowflake.core.event_table)
    * [snowflake.core.event_table.EventTable](_autosummary/snowflake.core.event_table.EventTable)
    * [snowflake.core.event_table.EventTableResource](_autosummary/snowflake.core.event_table.EventTableResource)
    * [snowflake.core.event_table.EventTableCollection](_autosummary/snowflake.core.event_table.EventTableCollection)
    * [snowflake.core.event_table.EventTableColumn](_autosummary/snowflake.core.event_table.EventTableColumn)
  * [snowflake.core.network_policy](_autosummary/snowflake.core.network_policy)
    * [snowflake.core.network_policy.NetworkPolicy](_autosummary/snowflake.core.network_policy.NetworkPolicy)
    * [snowflake.core.network_policy.NetworkPolicyResource](_autosummary/snowflake.core.network_policy.NetworkPolicyResource)
    * [snowflake.core.network_policy.NetworkPolicyCollection](_autosummary/snowflake.core.network_policy.NetworkPolicyCollection)
  * [snowflake.core.stream](_autosummary/snowflake.core.stream)
    * [snowflake.core.stream.PointOfTimeOffset](_autosummary/snowflake.core.stream.PointOfTimeOffset)
    * [snowflake.core.stream.Stream](_autosummary/snowflake.core.stream.Stream)
    * [snowflake.core.stream.StreamClone](_autosummary/snowflake.core.stream.StreamClone)
    * [snowflake.core.stream.StreamSource](_autosummary/snowflake.core.stream.StreamSource)
    * [snowflake.core.stream.StreamSourceStage](_autosummary/snowflake.core.stream.StreamSourceStage)
    * [snowflake.core.stream.StreamSourceTable](_autosummary/snowflake.core.stream.StreamSourceTable)
    * [snowflake.core.stream.StreamSourceView](_autosummary/snowflake.core.stream.StreamSourceView)
    * [snowflake.core.stream.StreamResource](_autosummary/snowflake.core.stream.StreamResource)
    * [snowflake.core.stream.StreamCollection](_autosummary/snowflake.core.stream.StreamCollection)
  * [snowflake.core.alert](_autosummary/snowflake.core.alert)
    * [snowflake.core.alert.Alert](_autosummary/snowflake.core.alert.Alert)
    * [snowflake.core.alert.AlertResource](_autosummary/snowflake.core.alert.AlertResource)
    * [snowflake.core.alert.AlertCollection](_autosummary/snowflake.core.alert.AlertCollection)
    * [snowflake.core.alert.AlertClone](_autosummary/snowflake.core.alert.AlertClone)
    * [snowflake.core.alert.CronSchedule](_autosummary/snowflake.core.alert.CronSchedule)
    * [snowflake.core.alert.MinutesSchedule](_autosummary/snowflake.core.alert.MinutesSchedule)
  * [snowflake.core.catalog_integration](_autosummary/snowflake.core.catalog_integration)
    * [snowflake.core.catalog_integration.CatalogIntegration](_autosummary/snowflake.core.catalog_integration.CatalogIntegration)
    * [snowflake.core.catalog_integration.CatalogIntegrationResource](_autosummary/snowflake.core.catalog_integration.CatalogIntegrationResource)
    * [snowflake.core.catalog_integration.CatalogIntegrationCollection](_autosummary/snowflake.core.catalog_integration.CatalogIntegrationCollection)
    * [snowflake.core.catalog_integration.Glue](_autosummary/snowflake.core.catalog_integration.Glue)
    * [snowflake.core.catalog_integration.OAuth](_autosummary/snowflake.core.catalog_integration.OAuth)
    * [snowflake.core.catalog_integration.ObjectStore](_autosummary/snowflake.core.catalog_integration.ObjectStore)
    * [snowflake.core.catalog_integration.Polaris](_autosummary/snowflake.core.catalog_integration.Polaris)
    * [snowflake.core.catalog_integration.RestConfig](_autosummary/snowflake.core.catalog_integration.RestConfig)
  * [snowflake.core.notebook](_autosummary/snowflake.core.notebook)
    * [snowflake.core.notebook.Notebook](_autosummary/snowflake.core.notebook.Notebook)
    * [snowflake.core.notebook.NotebookCollection](_autosummary/snowflake.core.notebook.NotebookCollection)
    * [snowflake.core.notebook.NotebookResource](_autosummary/snowflake.core.notebook.NotebookResource)
    * [snowflake.core.notebook.VersionDetails](_autosummary/snowflake.core.notebook.VersionDetails)
  * [snowflake.core.user_defined_function](_autosummary/snowflake.core.user_defined_function)
    * [snowflake.core.user_defined_function.Argument](_autosummary/snowflake.core.user_defined_function.Argument)
    * [snowflake.core.user_defined_function.BaseLanguage](_autosummary/snowflake.core.user_defined_function.BaseLanguage)
    * [snowflake.core.user_defined_function.ColumnType](_autosummary/snowflake.core.user_defined_function.ColumnType)
    * [snowflake.core.user_defined_function.FunctionLanguage](_autosummary/snowflake.core.user_defined_function.FunctionLanguage)
    * [snowflake.core.user_defined_function.JavaFunction](_autosummary/snowflake.core.user_defined_function.JavaFunction)
    * [snowflake.core.user_defined_function.JavaScriptFunction](_autosummary/snowflake.core.user_defined_function.JavaScriptFunction)
    * [snowflake.core.user_defined_function.PythonFunction](_autosummary/snowflake.core.user_defined_function.PythonFunction)
    * [snowflake.core.user_defined_function.ReturnDataType](_autosummary/snowflake.core.user_defined_function.ReturnDataType)
    * [snowflake.core.user_defined_function.ReturnTable](_autosummary/snowflake.core.user_defined_function.ReturnTable)
    * [snowflake.core.user_defined_function.ReturnType](_autosummary/snowflake.core.user_defined_function.ReturnType)
    * [snowflake.core.user_defined_function.SQLFunction](_autosummary/snowflake.core.user_defined_function.SQLFunction)
    * [snowflake.core.user_defined_function.ScalaFunction](_autosummary/snowflake.core.user_defined_function.ScalaFunction)
    * [snowflake.core.user_defined_function.UserDefinedFunction](_autosummary/snowflake.core.user_defined_function.UserDefinedFunction)
    * [snowflake.core.user_defined_function.UserDefinedFunctionResource](_autosummary/snowflake.core.user_defined_function.UserDefinedFunctionResource)
    * [snowflake.core.user_defined_function.UserDefinedFunctionCollection](_autosummary/snowflake.core.user_defined_function.UserDefinedFunctionCollection)
  * [snowflake.core.procedure](_autosummary/snowflake.core.procedure)
    * [snowflake.core.procedure.Argument](_autosummary/snowflake.core.procedure.Argument)
    * [snowflake.core.procedure.CallArgument](_autosummary/snowflake.core.procedure.CallArgument)
    * [snowflake.core.procedure.CallArgumentList](_autosummary/snowflake.core.procedure.CallArgumentList)
    * [snowflake.core.procedure.ColumnType](_autosummary/snowflake.core.procedure.ColumnType)
    * [snowflake.core.procedure.ErrorResponse](_autosummary/snowflake.core.procedure.ErrorResponse)
    * [snowflake.core.procedure.JavaFunction](_autosummary/snowflake.core.procedure.JavaFunction)
    * [snowflake.core.procedure.JavaScriptFunction](_autosummary/snowflake.core.procedure.JavaScriptFunction)
    * [snowflake.core.procedure.Procedure](_autosummary/snowflake.core.procedure.Procedure)
    * [snowflake.core.procedure.ProcedureCollection](_autosummary/snowflake.core.procedure.ProcedureCollection)
    * [snowflake.core.procedure.ProcedureResource](_autosummary/snowflake.core.procedure.ProcedureResource)
    * [snowflake.core.procedure.PythonFunction](_autosummary/snowflake.core.procedure.PythonFunction)
    * [snowflake.core.procedure.ReturnDataType](_autosummary/snowflake.core.procedure.ReturnDataType)
    * [snowflake.core.procedure.ReturnTable](_autosummary/snowflake.core.procedure.ReturnTable)
    * [snowflake.core.procedure.ReturnType](_autosummary/snowflake.core.procedure.ReturnType)
    * [snowflake.core.procedure.ScalaFunction](_autosummary/snowflake.core.procedure.ScalaFunction)
    * [snowflake.core.procedure.SQLFunction](_autosummary/snowflake.core.procedure.SQLFunction)

[1]

The example given here does require you to include connection information in
your Python source code. **Take care not to leak sensitive information such as
your password!**

[2]

<https://docs.snowflake.com/en/developer-guide/snowflake-rest-api/snowflake-
rest-api>

