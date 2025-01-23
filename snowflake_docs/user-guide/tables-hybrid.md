# Hybrid tables¶

A hybrid table is a Snowflake table type that is optimized for hybrid
transactional and operational workloads that require low latency and high
throughput on small random point reads and writes. A hybrid table supports
unique and referential integrity constraint enforcement that is critical for
transactional workloads. You can use a hybrid table along with other Snowflake
tables and features to power [Unistore
workloads](https://www.snowflake.com/en/data-cloud/workloads/unistore/) that
bring transactional and analytical data together in a single platform.

Use cases that may benefit from hybrid tables include:

  * Build a cohort for a targeted marketing campaign through an interactive user interface.

  * Maintain a central workflow state to coordinate large parallel data transformation pipelines.

  * Serve a precomputed promotion treatment for users who are visiting your website or mobile app.

## Architecture¶

Hybrid tables are integrated seamlessly into the existing Snowflake
architecture. Customers connect to the same Snowflake database service.
Queries are compiled and optimized in the cloud services layer and executed in
the same query engine in virtual warehouses. This architecture has several key
benefits:

  * Snowflake platform features, such as data governance, work with hybrid tables out of the box.

  * You can run hybrid workloads that mix operational and analytical queries.

  * You can join hybrid tables with other Snowflake tables, and the query executes natively and efficiently in the same query engine. No federation is required.

  * You can execute an atomic transaction across hybrid tables and other Snowflake tables. There is no need to orchestrate your own two-phase commit.

![Unistore architecture](../_images/unistore-arch.png)

Hybrid tables leverage a row store as the primary data store to provide
excellent operational query performance. When you write to a hybrid table, the
data is written directly into the row store. Data is asynchronously copied
into object storage in order to provide better performance and workload
isolation for large scans without affecting your ongoing operational
workloads. Some data may also be cached in columnar format on your warehouse
in order to provide better performance on analytical queries. You simply
execute SQL statements against the logical hybrid table and the Snowflake
query optimizer decides where to read data from in order to provide the best
performance. You get one consistent view of your data without needing to worry
about the underlying infrastructure.

Note

Because the primary storage for hybrid tables is a row store, hybrid tables
typically have a larger storage footprint than standard tables. The main
reason for the difference is that columnar data for standard tables often
achieves higher rates of compression. For details about storage costs, see
[Evaluate cost for hybrid tables](tables-hybrid-cost).

## Features¶

Hybrid tables provide some additional features that are not supported by other
Snowflake table types.

Feature | Hybrid tables | Standard tables  
---|---|---  
Primary data layout | Row-oriented, with secondary columnar storage | Columnar [micro-partitions](tables-clustering-micropartitions.html#label-what-are-micropartitions)  
Locking | Row-level locking | Partition or table locking  
PRIMARY KEY constraints | Required, enforced | Optional, not enforced  
FOREIGN KEY constraints | Optional, enforced (referential integrity) | Optional, not enforced  
UNIQUE constraints | Optional, enforced | Optional, not enforced  
NOT NULL constraints | Optional, enforced | Optional, enforced  
Indexes | Supported for performance; updated synchronously on writes | The search optimization service indexes columns for better point-lookup performance; batch updated/maintained asynchronously  
  
A constraint is _enforced_ when it protects a column from being updated in
certain ways. For example, a column that is declared NOT NULL cannot contain a
NULL value. An attempt to copy or insert a NULL value into a NOT NULL column
always results in an error. For hybrid tables, you cannot set the NOT ENFORCED
property on PRIMARY KEY, FOREIGN KEY, and UNIQUE constraints. Setting this
property results in an “invalid constraint property” error.

A constraint is _required_ when one or more columns in a table must have such
a constraint, which is only true for PRIMARY KEY constraints on hybrid tables.

## Determining when to use a hybrid table¶

While you should expect Snowflake standard tables to offer better performance
on large analytical queries, hybrid tables allow for faster results on short-
running operational queries. The following types of queries are most likely to
benefit from hybrid tables:

>   * High concurrency random point reads versus large range reads.
>
>   * High concurrency random writes versus large sequential writes (for
> example, bulk loading).
>
>   * Retrieval of a small number of entire records (for example, customer
> object) versus narrow projections with analytical functions (for example,
> aggregations or GROUP BY queries).
>
>

If your queries fit in one of these models, hybrid tables may be the preferred
choice for storing your data.

