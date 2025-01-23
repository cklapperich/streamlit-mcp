# Using Persisted Query Results¶

When a query is executed, the result is persisted (i.e. cached) for a period
of time. At the end of the time period, the result is purged from the system.

Snowflake uses persisted query results to avoid re-generating results when
nothing has changed (i.e. “retrieval optimization”). In addition, you can use
persisted query results to post-process the results (e.g. layering a new query
on top of the results already calculated).

For persisted query results of all sizes, the cache expires after 24 hours.

Note that the security token used to access large persisted query results
(i.e. greater than 100 KB in size) expires after 6 hours. A new token can be
retrieved to access results while they are still in cache. Smaller persisted
query results do not use an access token.

Note

The token provided to the Snowflake Connector for Spark (“Spark connector”)
expires after 24 hours regardless of the size of the persisted query results.
The Spark connector leverages the longer cache expiration time to avoid
timeouts in some use cases.

See also [Optimizing the warehouse cache](performance-query-warehouse-cache),
which discusses how table data may be cached and reused by an active
warehouse.

## Retrieval Optimization¶

If a user repeats a query that has already been run, and the data in the
table(s) hasn’t changed since the last time that the query was run, then the
result of the query is the same. Instead of running the query again, Snowflake
simply returns the same result that it returned previously. This can
substantially reduce query time because Snowflake bypasses query execution
and, instead, retrieves the result directly from the cache.

Typically, query results are reused if all of the following conditions are
met:

  * The new query matches the previously executed query exactly. Any difference in syntax, including lowercase versus uppercase, or the use of table aliases, will inhibit 100% cache reuse. For example, consider the following queries, run in succession:

> >     SELECT DISTINCT(severity) FROM weather_events;
>     SELECT DISTINCT(severity) FROM weather_events;
>     SELECT DISTINCT(severity) FROM weather_events we;
>     select distinct(severity) from weather_events;
>  
>
> Copy

The first query will populate the cache, and the identical second query will
benefit from 100% cache reuse. However, the third and fourth queries will not
trigger cache reuse, simply because the third query introduces a table alias
and the fourth query uses lowercase keywords.

  * The query does not include non-reusable functions, which return different results for successive runs of the same query. [UUID_STRING](../sql-reference/functions/uuid_string), [RANDOM](../sql-reference/functions/random), and [RANDSTR](../sql-reference/functions/randstr) are good examples of non-reusable functions.

  * The query does not include [external functions](../sql-reference/external-functions).

  * The query does not select from [hybrid tables](tables-hybrid).

  * The table data contributing to the query result has not changed.

  * The persisted result for the previous query is still available.

  * The role accessing the cached results has the required privileges.

    * If the query was a SELECT query, the role executing the query must have the necessary access privileges for all the tables used in the cached query.

    * If the query was a SHOW query, the role executing the query must match the role that generated the cached results.

  * Any configuration options that affect how the result was produced have not changed.

  * The table’s micro-partitions have not changed (e.g. been reclustered or consolidated) due to changes to other data in the table.

Note

Meeting all these conditions does not guarantee that Snowflake reuses the
query results.

By default, result reuse is enabled, but can be overridden at the account,
user, and session level using the [USE_CACHED_RESULT](../sql-
reference/parameters.html#label-use-cached-result) session parameter.

Note

Each time the persisted result for a query is reused, Snowflake resets the
24-hour retention period for the result, up to a maximum of 31 days from the
date and time that the query was first executed. After 31 days, the result is
purged and the next time the query is submitted, a new result is generated and
persisted.

## Post-processing Query Results¶

In some cases, you might want to perform further processing on the result of a
query that you’ve already run. For example:

  * You are developing a complex query step-by-step and you want to add a new layer on top of the previous query and run the new query without recalculating the partial results from scratch.

  * The previous query was a [SHOW <objects>](../sql-reference/sql/show), [DESCRIBE <object>](../sql-reference/sql/desc), or [CALL](../sql-reference/sql/call) statement, which returns results in a form that are not easy to reuse.

For example, you can’t call a stored procedure inside a more complex SQL
statement the way you can call a function inside a SQL statement, so the only
way to process the output of the stored procedure is to post-process the
stored query results.

Post-processing can be performed using the [RESULT_SCAN](../sql-
reference/functions/result_scan) table function. The function returns the
results of the previous query as a “table” and a new query can then be run on
the tabular data.

### Examples¶

Process the result of a [SHOW TABLES](../sql-reference/sql/show-tables)
command and extract the following columns and rows from the result:

>   * `schema_name`, `table_name`, and `rows` columns.
>
>   * Rows for tables that are empty.
>
>

>  
>  
>     SHOW TABLES;
>  
>
> +-----+-------------------------------+-------------+-------+-------+------+
>     | Row |           created_on          | name        | ...   | ...   | rows |
>
> +-----+-------------------------------+-------------+-------+-------+------+
>     |  1  | 2018-07-02 09:43:49.971 -0700 | employees   | ...   | ...   | 2405 |
>
> +-----+-------------------------------+-------------+-------+-------+------+
>     |  2  | 2018-07-02 09:43:52.483 -0700 | dependents  | ...   | ...   | 5280 |
>
> +-----+-------------------------------+-------------+-------+-------+------+
>     |  3  | 2018-07-03 11:43:52.483 -0700 | injuries    | ...   | ...   |    0 |
>
> +-----+-------------------------------+-------------+-------+-------+------+
>     |  4  | 2018-07-03 11:43:52.483 -0700 | claims      | ...   | ...   |    0 |
>
> +-----+-------------------------------+-------------+-------+-------+------+
>     | ...                                                                      |
>     | ...                                                                      |
>
> +-----+-------------------------------+-------------+-------+-------+------+
>  
>     -- Show the tables that are empty.
>     SELECT  "schema_name", "name" as "table_name", "rows"
>         FROM table(RESULT_SCAN(LAST_QUERY_ID()))
>         WHERE "rows" = 0;
>  
>     +-----+-------------+-------------+------+
>     | Row | schema_name | name        | rows |
>     +-----+-------------+-------------+------+
>     |  1  |  PUBLIC     | injuries    |    0 |
>     +-----+-------------+-------------+------+
>     |  2  |  PUBLIC     | claims      |    0 |
>     +-----+-------------+-------------+------+
>     | ...                                    |
>     | ...                                    |
>     +-----+-------------+-------------+------+
>  
>
> Copy

Additional examples are provided in [RESULT_SCAN](../sql-
reference/functions/result_scan).

