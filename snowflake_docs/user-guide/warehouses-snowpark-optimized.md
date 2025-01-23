# Snowpark-optimized warehouses¶

Snowpark-optimized warehouses let you configure the available memory resources
and CPU architecture on a single-node instance for your workloads.

## When to use a Snowpark-optimized warehouse¶

While Snowpark workloads can be run on both standard and Snowpark-optimized
warehouses, Snowpark-optimized warehouses are recommended for running code,
and recommended workloads that have large memory requirements or dependencies
on a specific CPU architecture. Example workloads include ML training use
cases using a [stored procedure](../developer-guide/stored-procedure/stored-
procedures-overview) on a single virtual warehouse node. Snowpark workloads,
utilizing [UDF](../developer-guide/udf/udf-overview) or [UDTF](../developer-
guide/udf/python/udf-python-tabular-functions), might also benefit from
Snowpark-optimized warehouses.

Note

Initial creation and resumption of a Snowpark-optimized virtual warehouse
might take longer than standard warehouses.

## Configuration options for Snowpark-optimized warehouses¶

The default configuration for a Snowpark-optimized warehouse provides 16x
memory per node compared to a standard warehouse. You can optionally configure
additional memory per node and specify CPU architecture using the
`resource_constraint` property. The following options are available:

Memory (up to) | CPU architecture | Minimum warehouse size required  
---|---|---  
16GB | Default or x86 | XSMALL  
256GB | Default or x86 | M  
1TB [1] | Default or x86 | L  
[1] (1,2)

1 TB memory options are not currently available for the Microsoft Azure and
Google Cloud Platform (GCP) [regions](intro-regions).

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Preview Feature](../release-
notes/preview-features) — Open

Resource constraints are available to all accounts.

## Creating a Snowpark-optimized warehouse¶

To create a new Snowpark-optimized warehouse, you can set the warehouse type
property in the following interfaces.

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Preview Feature](../release-
notes/preview-features) — Open

Resource constraints are available to all accounts.

SQLPython

Set the WAREHOUSE_TYPE property to `'SNOWPARK-OPTIMIZED'` when running the
[CREATE WAREHOUSE](../sql-reference/sql/create-warehouse) command. For
example:

    
    
    CREATE OR REPLACE WAREHOUSE snowpark_opt_wh WITH
      WAREHOUSE_SIZE = 'MEDIUM'
      WAREHOUSE_TYPE = 'SNOWPARK-OPTIMIZED';
    

Copy

Create a large Snowpark-optimized warehouse `so_warehouse` with 256 GB of
memory by specifying the resource constraint `MEMORY_16X_X86`:

    
    
    CREATE WAREHOUSE so_warehouse WITH
      WAREHOUSE_SIZE = 'LARGE'
      WAREHOUSE_TYPE = 'SNOWPARK-OPTIMIZED'
      RESOURCE_CONSTRAINT = 'MEMORY_16X_X86';
    

Copy

Note

The default resource constraint is `MEMORY_16X`.

Set the `warehouse_type` property to `'SNOWPARK-OPTIMIZED'` when constructing
a [Warehouse](/developer-guide/snowflake-python-
api/reference/latest/_autosummary/snowflake.core.warehouse.Warehouse) object.

Then, pass this `Warehouse` object to the
[WarehouseCollection.create](/developer-guide/snowflake-python-
api/reference/latest/_autosummary/snowflake.core.warehouse.WarehouseCollection#snowflake.core.warehouse.WarehouseCollection.create)
method to create the warehouse in Snowflake. For example:

    
    
    from snowflake.core import CreateMode
    from snowflake.core.warehouse import Warehouse
    
    my_wh = Warehouse(
      name="snowpark_opt_wh",
      warehouse_size="MEDIUM",
      warehouse_type="SNOWPARK-OPTIMIZED"
    )
    root.warehouses.create(my_wh, mode=CreateMode.or_replace)
    

Copy

Note

Resource constraints are currently not supported in the Snowflake Python APIs.

## Modifying Snowpark-optimized warehouse properties¶

To modify warehouse properties including the warehouse type, you can use the
following interfaces.

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Preview Feature](../release-
notes/preview-features) — Open

Resource constraints are available to all accounts.

Note

Changing the warehouse type is only supported for a warehouse in the
`SUSPENDED` state. To suspend a warehouse before changing the `warehouse_type`
property, execute the following operation:

SQLPython

    
    
    ALTER WAREHOUSE snowpark_opt_wh SUSPEND;
    

Copy

    
    
    root.warehouses["snowpark_opt_wh"].suspend()
    

Copy

SQLPython

Use the [ALTER WAREHOUSE](../sql-reference/sql/alter-warehouse) command to
modify the memory resources and CPU architecture for Snowpark-optimized
warehouse `so_warehouse`:

    
    
    ALTER WAREHOUSE so_warehouse SET
      RESOURCE_CONSTRAINT = 'MEMORY_1X_x86';
    

Copy

Resource constraints are currently not supported in the Snowflake Python APIs.

## Using Snowpark Python Stored Procedures to run ML training workloads¶

For information on Machine Learning Models and Snowpark Python, see [Training
Machine Learning Models with Snowpark Python](../developer-
guide/snowpark/python/python-snowpark-training-ml).

## Billing for Snowpark-optimized warehouses¶

For information on Snowpark-optimized warehouse credit consumption see `Table
1(a): Snowflake Credit Table for Virtual Warehouse Services` in the [Snowflake
Service Consumption Table](https://www.snowflake.com/legal-
files/CreditConsumptionTable.pdf).

## Region availability¶

Snowpark-optimized warehouses are available in all regions across AWS, Azure,
and Google Cloud [1].

