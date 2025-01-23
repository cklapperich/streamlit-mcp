# Search Optimization Service¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Enterprise Edition
Feature](intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about
upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-
guide/contacting-support).

The search optimization service can significantly improve the performance of
certain types of lookup and analytical queries. An extensive set of filtering
predicates are supported (see [Identifying queries that can benefit from
search optimization](search-optimization/queries-that-benefit)).

Note

To start with a tutorial that compares execution time with and without search
optimization, see [Getting Started with Search
Optimization](https://quickstarts.snowflake.com/guide/getting_started_with_search_optimization/index.html).

The search optimization service aims to significantly improve the performance
of certain types of queries on tables, including:

  * Selective point lookup queries on tables. A point lookup query returns only one or a small number of distinct rows. Use case examples include:

    * Business users who need fast response times for critical dashboards with highly selective filters.

    * Data scientists who are exploring large data volumes and looking for specific subsets of data.

    * Data applications retrieving a small set of results based on an extensive set of filtering predicates.

For more information, see [Speeding up point lookup queries with search
optimization](search-optimization/point-lookup-queries).

  * Character data (text) and IPv4 address searches executed with the [SEARCH](../sql-reference/functions/search) and [SEARCH_IP](../sql-reference/functions/search_ip) functions. For more information, see [Speeding up text queries with search optimization](search-optimization/text-queries).

  * Substring and regular expression searches (e.g. [[ NOT ] LIKE](../sql-reference/functions/like), [[ NOT ] ILIKE](../sql-reference/functions/ilike), [[ NOT ] RLIKE](../sql-reference/functions/rlike), etc.). For more information, see [Speeding up substring and regular expression queries with search optimization](search-optimization/substring-queries).

  * Queries on elements in [VARIANT, OBJECT, and ARRAY](../sql-reference/data-types-semistructured) (semi-structured) columns that use the following types of predicates:

    * Equality predicates.

    * IN predicates.

    * Predicates that use [ARRAY_CONTAINS](../sql-reference/functions/array_contains).

    * Predicates that use [ARRAYS_OVERLAP](../sql-reference/functions/arrays_overlap).

    * Predicates that use full-text search with [SEARCH](../sql-reference/functions/search).

    * Substring and regular expression predicates.

    * Predicates that check for NULL values.

For more information, see [Speeding up queries of semi-structured data with
search optimization](search-optimization/semi-structured-queries).

  * Queries that use selected geospatial functions with [GEOGRAPHY](../sql-reference/data-types-geospatial) values. For more information, see [Speeding up geospatial queries with search optimization](search-optimization/geospatial-queries).

Once you identify the queries that can benefit from the search optimization
service, you can [enable search optimization](search-optimization/enabling)
for the columns and tables used in those queries.

The search optimization service is generally transparent to users. Queries
work the same as they do without search optimization; some are just faster.
However, search optimization does have effects on certain other table
operations. For more information, see [Working with search-optimized
tables](search-optimization/working-with-tables).

## How the Search Optimization Service Works¶

To improve performance of search queries, the search optimization service
creates and maintains a persistent data structure called a _search access
path_. The search access path keeps track of which values of the table’s
columns might be found in each of its [micro-partitions](tables-clustering-
micropartitions.html#label-what-are-micropartitions), allowing some micro-
partitions to be skipped when scanning the table.

A maintenance service is responsible for creating and maintaining the search
access path:

  * When you enable search optimization, the maintenance service creates and populates the search access path with the data needed to perform the lookups.

Building the search access path can take significant time, depending on the
size of the table. The maintenance service works in the background and does
not block any operations on the table. Queries are not accelerated until the
search access path has been fully built.

  * When data in the table is updated (for example, by loading new data sets or through DML operations), the maintenance service automatically updates the search access path to reflect the changes to the data.

If queries are run while the search access path is still being updated,
queries might run more slowly, but will still return correct results.

The progress of each table’s maintenance service appears in the
`search_optimization_progress` column in the output of [SHOW TABLES](../sql-
reference/sql/show-tables). Before you measure the performance improvement of
search optimization on a newly-optimized table, make sure this column shows
that the table has been fully optimized.

Search access path maintenance is transparent. You don’t need to create a
virtual warehouse for running the maintenance service. However, there is a
cost for the storage and compute resources of maintenance. For more details on
costs, see [Search optimization cost estimation and management](search-
optimization/cost-estimation).

## Other Options for Optimizing Query Performance¶

The search optimization service is one of several ways to optimize query
performance. Other techniques include:

  * Query acceleration.

  * Clustering a table.

  * Creating one or more materialized views (clustered or unclustered).

Each of these has different advantages, as shown in the following table:

Feature | Supported Query Types | Notes  
---|---|---  
Search Optimization Service | 

  * [Equality searches](search-optimization/point-lookup-queries.html#label-search-optimization-service-queries-equality-in).
  * [Substring and regular expression searches](search-optimization/substring-queries.html#label-search-optimization-service-queries-wildcard-regexp).
  * [Character data (text) and IPv4 address searches](search-optimization/text-queries).
  * Searches of [elements in VARIANT](search-optimization/semi-structured-queries.html#label-search-optimization-service-queries-variant).
  * Searches of [GEOGRAPHY columns using geospatial functions](search-optimization/geospatial-queries.html#label-search-optimization-service-queries-geo).

The search optimization service can improve the performance of these types of searches for the [supported data types](search-optimization/queries-that-benefit.html#label-search-optimization-service-supported-data-types). |   
[Query Acceleration Service](query-acceleration-service) |  Queries with filters or aggregation. If the query includes LIMIT, the query must also include ORDER BY. The filters must be highly selective, and the ORDER BY clause must have a low cardinality.   
Query acceleration works well with ad-hoc analytics, queries with unpredictable data volume, and queries with large scans and selective filters. | Query acceleration and search optimization are complementary. Both can accelerate the same query. See Compatibility with Query Acceleration.  
[Materialized View](views-materialized) | 

  * Equality searches.
  * Range searches.
  * Sort operations.

| You can also use materialized views to define different clustering keys on
the same source table (or a subset of that table), or to store flattened JSON
or variant data so it only needs to be flattened once. Materialized views
improve performance only for the subset of rows and columns included in the
materialized view.  
[Clustering the Table](tables-clustering-keys) | 

  * Equality searches.
  * Range searches.

| A table can be clustered only on a single key, which can contain one or more
columns or expressions.  
  
The following table shows which of these optimizations have storage or compute
costs:

| Storage Cost | Compute Cost  
---|---|---  
Search Optimization Service | ✔ | ✔  
Query Acceleration Service |  | ✔  
Materialized View | ✔ | ✔  
Clustering the Table | ✔ [1] | ✔  
[1]

The process of reclustering can increase the size of [fail-safe](data-
failsafe) storage due to the rewriting of existing partitions into new
partitions. (Reclustering does not introduce any new rows, but only
reorganizes existing rows.) For details, see [Credit and Storage Impact of
Reclustering](tables-clustering-keys.html#label-clustering-keys-reclustering-
credit-storage).

### Compatibility with Query Acceleration¶

Search optimization and [query acceleration](query-acceleration-service) can
work together to optimize query performance. First, search optimization can
prune the [micro-partitions](tables-clustering-micropartitions.html#label-
what-are-micropartitions) not needed for a query. Then, for [eligible
queries](query-acceleration-service.html#label-identifying-queries-warehouses-
for-qas), query acceleration can offload portions of the rest of the work to
shared compute resources provided by the service.

Performance of queries accelerated by both services varies depending on
workload and available resources.

## Examples¶

Start by creating a table with data:

    
    
    create or replace table test_table (id int, c1 int, c2 string, c3 date) as
    select * from values
      (1, 3, '4',  '1985-05-11'),
      (2, 4, '3',  '1996-12-20'),
      (3, 2, '1',  '1974-02-03'),
      (4, 1, '2',  '2004-03-09'),
      (5, null, null,  null);
    

Copy

Add the SEARCH OPTIMIZATION property to the table using [ALTER TABLE](../sql-
reference/sql/alter-table.html#label-alter-table-searchoptimizationaction):

    
    
    alter table test_table add search optimization;
    

Copy

The following queries can use the search optimization service:

    
    
    select * from test_table where id = 2;
    

Copy

    
    
    select * from test_table where c2 = '1';
    

Copy

    
    
    select * from test_table where c3 = '1985-05-11';
    

Copy

    
    
    select * from test_table where c1 is null;
    

Copy

    
    
    select * from test_table where c1 = 4 and c3 = '1996-12-20';
    

Copy

The following query can use the search optimization service because the
implicit cast is on the constant, not the column:

    
    
    select * from test_table where c2 = 2;
    

Copy

The following cannot use the search optimization service because the cast is
on the table’s column:

    
    
    select * from test_table where cast(c2 as number) = 2;
    

Copy

An [IN](../sql-reference/functions/in) clause is supported by the search
optimization service:

    
    
    select id, c1, c2, c3
        from test_table
        where id IN (2, 3)
        order by id;
    

Copy

If predicates are individually supported by the search optimization service,
then they can be joined by the conjunction `AND` and still be supported by the
search optimization service:

    
    
    select id, c1, c2, c3
        from test_table
        where c1 = 1
           and
              c3 = TO_DATE('2004-03-09')
        order by id;
    

Copy

DELETE and UPDATE (and MERGE) can also use the search optimization service:

    
    
    delete from test_table where id = 3;
    

Copy

    
    
    update test_table set c1 = 99 where id = 4;
    

Copy

