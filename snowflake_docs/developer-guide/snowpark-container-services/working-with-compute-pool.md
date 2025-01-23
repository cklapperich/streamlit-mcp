# Snowpark Container Services: Working with compute pools¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) Feature — Generally
Available

Available to accounts in [AWS and Microsoft Azure commercial
regions](../../user-guide/intro-regions.html#label-na-general-regions), with
some exceptions. For more information, see [Available
regions](overview.html#label-snowpark-containers-overview-available-regions).

A compute pool is a collection of one or more virtual machine (VM) nodes on
which Snowflake runs your Snowpark Container Services services (including job
services). You create a compute pool using the [CREATE COMPUTE
POOL](../../sql-reference/sql/create-compute-pool) command. You then specify
it when [creating a service](../../sql-reference/sql/create-service) or
[executing a job service](../../sql-reference/sql/execute-job-service).

## Creating a compute pool¶

A compute pool is an account-level construct, analogous to a Snowflake virtual
warehouse. The naming scope of the compute pool is your account. That is, you
cannot have multiple compute pools with the same name in your account.

The minimum information required to create a compute pool includes the
following:

  * The machine type (referred to as the _instance family_) to provision for the compute pool nodes

  * The minimum nodes to launch the compute pool with

  * The maximum number of nodes the compute pool can scale to (Snowflake manages the scaling.)

If you expect a substantial load or sudden bursts of activity on the services
you intend to run within your compute pool, you can set a minimum node count
greater than 1. This approach ensures that additional nodes are readily
available when needed, instead of waiting for autoscaling to start.

Setting a maximum node limit prevents an unexpectedly large number of nodes
from being added to your compute pool by Snowflake autoscaling. This can be
crucial in scenarios such as unexpected load spikes or issues in your code
that might cause Snowflake to allocate a larger number of compute pool nodes
than originally planned.

To create a compute pool using [Snowsight](../../user-guide/ui-snowsight), or
SQL:

Snowsight:

    

  1. Select Admin » Compute pools.

  2. Select your username at the bottom of the navigation bar and switch to the ACCOUNTADMIN role, or any role that is allowed to create a compute pool.

  3. Select \+ Compute Pool.

  4. In the New compute pool UI, specify the required information (the compute pool name, the instance family, and the node limit).

  5. Select Create Compute Pool.

SQL:

    

Execute the [CREATE COMPUTE POOL](../../sql-reference/sql/create-compute-pool)
command.

For example, the following command creates a one-node compute pool:

    
    
    CREATE COMPUTE POOL tutorial_compute_pool
      MIN_NODES = 1
      MAX_NODES = 1
      INSTANCE_FAMILY = CPU_X64_XS;
    

Copy

The instance family identifies the type of machine you want to provision for
computer nodes in the compute pool. Specifying instance family in creating a
compute pool is similar to specifying warehouse size (XSMALL, SMALL, MEDIUM,
LARGE and so on) when creating a warehouse. The following table lists the
available machine types.

> INSTANCE_FAMILY, [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf) Mapping | vCPU | Memory (GiB) | Storage (GiB) | Bandwidth limit (Gbps) | GPU | GPU Memory per GPU (GiB) | Node limit | Description  
> ---|---|---|---|---|---|---|---|---  
> CPU_X64_XS, . CPU | XS | 1 | 6 | 100 | Up to 12.5 | n/a | n/a | 50 | Smallest instance available for Snowpark Containers. Ideal for cost-savings and getting started.  
> CPU_X64_S, . CPU | S | 3 | 13 | 100 | Up to 12.5 | n/a | n/a | 50 | Ideal for hosting multiple services/jobs while saving cost.  
> CPU_X64_M, . CPU | M | 6 | 28 | 100 | Up to 12.5 | n/a | n/a | 50 | Ideal for having a full stack application or multiple services  
> CPU_X64_L, . CPU | L | 28 | 116 | 100 | 12.5 | n/a | n/a | 50 | For applications which need an unusually large number of CPUs, memory and Storage.  
> HIGHMEM_X64_S, . High-Memory CPU | S | 6 | 58 | 100 | AWS: Up to 12.5, Azure: 8 | n/a | n/a | 50 | For memory intensive applications.  
> HIGHMEM_X64_M, . High-Memory CPU | M . (AWS only) | 28 | 240 | 100 | 12.5 | n/a | n/a | 50 | For hosting multiple memory intensive applications on a single machine.  
> HIGHMEM_X64_M, . High-Memory CPU | M . (Azure only) | 28 | 244 | 100 | 16 | n/a | n/a | 50 | For hosting multiple memory intensive applications on a single machine.  
> HIGHMEM_X64_L, . High-Memory CPU | L . (AWS only) | 124 | 984 | 100 | 50 | n/a | n/a | 20 | Largest AWS high-memory machine available for processing large in-memory data.  
> HIGHMEM_X64_SL, . High-Memory CPU | L . (Azure only) | 92 | 654 | 100 | 32 | n/a | n/a | 20 | Largest Azure high-memory machine available for processing large in-memory data.  
> GPU_NV_S, . GPU | S . (AWS only, except Paris and Osaka regions) | 6 | 27 | 100 | Up to 10 | 1 NVIDIA A10G | 24 | 10 | Our smallest NVIDIA GPU size available for Snowpark Containers to get started.  
> GPU_NV_M, . GPU | M . (AWS only, except not Paris and Osaka regions) | 44 | 178 | 100 | 40 | 4 NVIDIA A10G | 24 | 10 | Optimized for intensive GPU usage scenarios like Computer Vision or LLMs/VLMs.  
> GPU_NV_L, . GPU | L . (AWS only, available only in AWS US West and US East regions by request; limited availability might be possible in other regions upon request) | 92 | 1112 | 100 | 400 | 8 NVIDIA A100 | 40 | On request | Largest GPU instance for specialized and advanced GPU cases like LLMs and Clustering, etc.  
> GPU_NV_XS, . GPU | XS . (Azure only, except not Switzerland North and UAE North regions) | 3 | 26 | 100 | 8 | 1 NVIDIA T4 | 16 | 10 | Our smallest Azure NVIDIA GPU size available for Snowpark Containers to get started.  
> GPU_NV_SM, . GPU | SM . (Azure only, except not Central US region) | 32 | 424 | 100 | 40 | 1 NVIDIA A10 | 24 | 10 | A smaller Azure NVIDIA GPU size available for Snowpark Containers to get started.  
> GPU_NV_2M, . GPU | 2M . (Azure only, except not Central US region) | 68 | 858 | 100 | 80 | 2 NVIDIA A10 | 24 | 5 | Optimized for intensive GPU usage scenarios like Computer Vision or LLMs/VLMs.  
> GPU_NV_3M, . GPU | 3M . (Azure only, except not North Europe and UAE North regions) | 44 | 424 | 100 | 40 | 2 NVIDIA A100 | 80 | On request | Optimized for memory-intensive GPU usage scenarios like Computer Vision or LLMs/VLMs.  
> GPU_NV_SL, . GPU | SL . (Azure only, except not North Europe and UAE North regions) | 92 | 858 | 100 | 80 | 4 NVIDIA A100 | 80 | On request | Largest GPU instance for specialized and advanced GPU cases like LLMs and Clustering, etc.  
  
For information about available instance families, see [CREATE COMPUTE
POOL](../../sql-reference/sql/create-compute-pool).

### Autoscaling of compute pool nodes¶

After you create a compute pool, Snowflake launches the minimum number of
nodes and automatically creates additional nodes up to the maximum allowed.
This is called _autoscaling_. New nodes are allocated when the running nodes
cannot take any additional workload. For example, suppose that two service
instances are running on two nodes within your compute pool. If you execute
another service within the same compute pool, the additional resource
requirements might cause Snowflake to start an additional node.

However, if no services run on a node for a specific duration, Snowflake
automatically removes the node, ensuring that the compute pool maintains the
minimum required nodes even after the removal.

## Managing a compute pool¶

You can manage a compute pool using [Snowsight](../../user-guide/ui-
snowsight), or SQL.

In [Snowsight](../../user-guide/ui-snowsight), you choose the more option (…)
next to the compute pool name, and choose the desired operation from the menu.
The section explains SQL commands you can use to manage a compute pool.

Snowpark Container Services provides the following commands to manage compute
pools:

  * **Monitoring:** Use the [SHOW COMPUTE POOLS](../../sql-reference/sql/show-compute-pools) command to get information about compute pools.

  * **Operating:** Use the [ALTER COMPUTE POOL](../../sql-reference/sql/alter-compute-pool) command to change the state of a compute pool.
    
        ALTER COMPUTE POOL <name> { SUSPEND | RESUME | STOP ALL }
    

Copy

When you suspend a compute pool, Snowflake suspends all services except the
job services. The job services continue to run until they reach a terminal
state (DONE or FAILED), after which the compute pool nodes are released.

A suspended compute pool must be resumed before you can start a new service.
If the compute pool is configured to auto-resume (with the AUTO_RESUME
property set to TRUE), Snowflake automatically resumes the pool when a service
is submitted to it. Otherwise, you need to run the ALTER COMPUTE POOL command
to manually resume the compute pool.

  * **Modifying:** Use the [ALTER COMPUTE POOL](../../sql-reference/sql/alter-compute-pool) command to change compute pool properties.
    
        ALTER COMPUTE POOL <name> SET propertiesToAlter = <value>
    propertiesToAlter := { MIN_NODES | MAX_NODES | AUTO_RESUME | AUTO_SUSPEND_SECS | COMMENT }
    

Copy

When you decrease MAX_NODES, note the following potential effects:

    * Snowflake might need to terminate one or more service instances and restart them on other available nodes in the compute pool. If MAX_NODES is set too low, Snowflake might be unable to schedule certain service instances.

    * If the node terminated had a job service execution in progress, the job execution will fail. Snowflake will not restart the job service.

**Example:**

> >         ALTER COMPUTE POOL MYPOOL SET MIN_NODES = 2  MAX_NODES = 2;
>  
>
> Copy

  * **Removing:** Use the [DROP COMPUTE POOL](../../sql-reference/sql/drop-compute-pool) command to remove a compute pool.

> **Example:**
>

>> >>     DROP COMPUTE POOL <name>

>>  
>>

>> Copy

>>

>> You must stop all running services before you can drop a compute pool.

  * **Listing compute pools and viewing properties:** Use SHOW COMPUTE POOLS and DESCRIBE COMPUTE POOL commands. For examples, see [Show Compute Pools](../../sql-reference/sql/show-compute-pools).

## Compute pool lifecycle¶

A compute pool can be in any of the following states:

  * **IDLE:** The compute pool has the desired number of virtual machine (VM) nodes, but no services are scheduled. In this state, autoscaling can shrink the compute pool to the minimum size due to lack of activity.

  * **ACTIVE:** The compute pool has at least one service running or scheduled to run on it. The pool can grow (up to the maximum nodes) or shrink (down to the minimum nodes) in response to load or user actions.

  * **SUSPENDED:** The pool currently contains no running virtual machine nodes, but if the AUTO_RESUME compute pool property is set to TRUE, the pool will automatically resume when a service is scheduled.

The following states are transient:

  * **STARTING:** When you create or resume a compute pool, the compute pool enters the STARTING state until at least one node is provisioned.

  * **STOPPING:** When you suspend a compute pool (using ALTER COMPUTE POOL), the compute pool enters the STOPPING state until Snowflake has released all nodes in the compute pool. When you suspend a compute pool, Snowflake suspends all services except the job services. The job services continue to run until they reach a terminal state (DONE or FAILED), after which the compute pool nodes are released.

  * **RESIZING:** When you create a compute pool, initially it enters the STARTING state. After it has one node provisioned, it enters the RESIZING state until the minimum number of nodes (as specified in CREATE COMPUTE POOL) are provisioned. When you change a compute pool (ALTER COMPUTE POOL) and update the minimum and maximum node values, the pool enters the RESIZING state until the minimum nodes are provisioned. Note that autoscaling of a compute pool also puts the compute pool in the RESIZING state.

## Compute pool privileges¶

When you work with compute pools, the following privilege model applies:

  * To create a compute pool in an account, the current role needs the CREATE COMPUTE POOL privilege on the account. If you create a pool, as an owner you have OWNERSHIP permission, which grants full control over that compute pool. Having OWNERSHIP of one compute pool doesn’t imply any permissions on other compute pools.

  * For compute pool management, the following privileges (capabilities) are supported:

Privilege | Usage  
---|---  
MODIFY | Enables altering any compute pool properties, including changing the size.  
MONITOR | Enables viewing compute pool usage, including describing compute pool properties.  
OPERATE | Enables changing the state of the compute pool (suspend, resume). In addition, enables stopping any scheduled services (including job services).  
USAGE | Enables creating services in the compute pool. Note that when a compute pool is in a suspended state and has its AUTO_RESUME property set to true, a role with USAGE permission on the compute pool can implicitly trigger the compute pool’s resumption when they start or resume a service, even if the role lacks the OPERATE permission.  
OWNERSHIP | Grants full control over the compute pool. Only a single role can hold this privilege on a specific object at a time.  
ALL [ PRIVILEGES ] | Grants all privileges, except OWNERSHIP, on the compute pool.  

## Compute pool maintenance¶

As part of routine internal infrastructure maintenance, Snowflake regularly
updates older compute pool nodes to ensure optimal performance and security.
This includes operating system upgrades, driver enhancements, and security
fixes. Maintenance involves replacing outdated nodes with updated ones every
few weeks, with each node active for up to a month.

### Maintenance window¶

Scheduled maintenance occurs every Monday to Thursday, from 11 PM to 5 AM
local time in the deployment region, with an expected window of 6 hours.

### Service disruption¶

During maintenance, all service instances in compute pools requiring upgrades
will be automatically recreated on new nodes. Ongoing job services will be
disrupted and must be restarted by customers after maintenance is complete.

Attention

Service disruptions during a maintenance window or critical updates are not
covered by the Service Level set forth in [Snowflake’s Support Policy and
Service Level Agreement](https://www.snowflake.com/legal/support-policy-and-
service-level-agreement/).

### Best practices to minimize downtime¶

  * Use high availability techniques including ensuring that each service has multiple instances that can be spread across [multiple](working-with-services.html#label-spcs-working-with-services-multiple-services-autoscaling) compute nodes to avoid single points of failure.

  * Monitor maintenance schedules and plan critical tasks outside maintenance windows.

  * Implement automated restart procedures for job services.

  * Perform regular backups or checkpoints.

## How services are scheduled on a compute pool¶

At the time of [creating a service](../../sql-reference/sql/create-service),
you might choose to run multiple instances to manage incoming load. Snowflake
uses the following general guidelines when scheduling your service instances
on compute pool nodes:

  * All containers in a service instance always run on a single compute pool node. That is, a service instance never spans across multiple nodes.

  * When you run multiple service instances, Snowflake may run these service instances on the same node or different nodes within the compute pool. When making this decision, Snowflake considers any specified hard resource requirements (such as memory and GPU) as outlined in the service specification file (see [containers.resources field](specification-reference.html#label-spcs-spec-reference-containers-resources-field)).

For example, suppose each node in your compute pool provides 8 GB of memory.
If your service specification includes a 6-GB memory requirement, and you
choose to run two instances when creating a service, Snowflake cannot run both
instances on the same node. In this case, Snowflake schedules each instance on
a separate node within the compute pool to fulfill the memory requirements.

Note

Snowflake supports stage mounts for use by application containers. Snowflake
internal stage is one of the supported storage volume types.

For optimal performance, Snowflake now limits the total number of [stage
volume](snowflake-stage-volume) mounts to eight per compute pool node,
regardless of whether these volumes belong to the same service instance, the
same service, or different services.

When the limit on a node is reached, Snowflake doesn’t use that node to start
new service instances that use a stage volume. If the limit is reached on all
nodes in the compute pool, Snowflake will be unable to start your service
instance. In this scenario, when you execute the SHOW SERVICE CONTAINERS IN
SERVICE command, Snowflake returns PENDING status with the “Unschedulable due
to insufficient resources” message.

To accommodate this stage mount allotment limit on a node, in some cases, you
can increase the maximum number of nodes that you request for a compute pool.
This ensures that additional nodes are available for Snowflake to start your
service instances.

## Default compute pools for Notebooks¶

Starting release 8.46, Snowflake automatically provisions two compute pools in
each Snowflake account (except the trial accounts) for running Notebook apps.
These compute pools are exclusively for running Notebooks and cannot be used
to create a Snowpark Container Services service.

  * **Compute pool name (as it appears in the Snowsight UI):** SYSTEM_COMPUTE_POOL_GPU

    * **Instance family:** GPU_NV_S (see Instance family table)

    * **Default configuration:**

      * MIN_NODES=1

      * MAX_NODES=25

      * INITIALLY_SUSPENDED=true

      * AUTO_SUSPEND_SECS=600

  * **Compute pool name (as it appears in the Snowsight UI):** SYSTEM_COMPUTE_POOL_CPU

    * **Instance family:** CPU_X64_S

    * **Default configuration:**

      * MIN_NODES=1

      * MAX_NODES=5

      * INITIALLY_SUSPENDED=true

      * AUTO_SUSPEND_SECS=600

The default configuration properties mean the following:

  * Compute pools are initially in a suspended state and only begin incurring costs when Notebooks are started within them.

  * If no Notebooks are running, these compute pools are automatically suspended after 10 minutes. Note the following:

    * By default, Notebooks are suspended automatically after 30 minutes of inactivity. After all Notebooks stop running on a default compute pool, Snowflake suspends the pool after 10 minutes.

    * To modify the auto-suspension policy for default compute pools, use the [ALTER COMPUTE POOL SET AUTO_SUSPEND_SECS](../../sql-reference/sql/alter-compute-pool) command. You can also adjust the Notebook auto-suspension policy. For more information, see [Idle time and reconnection](../../user-guide/ui-snowsight/notebooks-setup.html#label-notebooks-idle-time-property).

Default compute pools are provided for convenience. While any role in a
Snowflake account can create a Notebook, only the ACCOUNTADMIN role is
authorized to create compute pools. By using default compute pools, users can
create Notebooks without needing an account administrator to configure a
compute pool.

These compute pools are dedicated to Notebook workloads, and you can associate
[budgets](../../user-guide/budgets) with default compute pools to manage
Notebook costs.

Note the following about the default compute pool permission:

  * In a Snowflake account, the ACCOUNTADMIN role owns these compute pools. Administrators have full control over the compute pools, including modifying their properties, suspending operations, and monitoring consumption. If the default compute pools created by Snowflake are not needed, the ACCOUNTADMIN role can delete them. For example:
    
        USE ROLE ACCOUNTADMIN;
    ALTER COMPUTE POOL SYSTEM_COMPUTE_POOL_CPU STOP ALL;
    DROP COMPUTE POOL SYSTEM_COMPUTE_POOL_CPU;
    

Copy

  * By default, the USAGE permission on default compute pools is granted to the PUBLIC role, allowing all roles in the account to use them. However, the ACCOUNTADMIN can modify these privileges to restrict access if necessary.

To restrict access to default compute pools to specific roles in your account,
use the ACCOUNTADMIN role to revoke the USAGE permission from the PUBLIC role
and grant it to the desired role(s). For example:

    
        USE ROLE ACCOUNTADMIN;
    REVOKE USAGE ON COMPUTE POOL SYSTEM_COMPUTE_POOL_CPU FROM ROLE PUBLIC;
    GRANT USAGE ON COMPUTE POOL SYSTEM_COMPUTE_POOL_CPU TO ROLE <role-name>;
    

Copy

## Guidelines and limitations¶

  * **CREATE COMPUTE POOL permission:** If you cannot create a compute pool under the current role, consult your account administrator to grant permission. For example:
    
        GRANT CREATE COMPUTE POOL ON ACCOUNT TO ROLE <role_name> [WITH GRANT OPTION];
    

Copy

For more information, see [GRANT <privileges>](../../sql-reference/sql/grant-
privilege).

  * **Per account limit on compute pool nodes**. The number of nodes you can create in your account (regardless of the number of compute pools) is limited to 120. In addition, there is a limit on the number of nodes allowed for each instance family (see the **Node limit** column in the instance family table). If you see an error message like `Requested number of nodes <#> exceeds the node limit for the account`, you have encountered these limits. For more information, contact your account representation.

