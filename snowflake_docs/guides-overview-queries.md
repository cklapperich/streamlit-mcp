# Query Data in Snowflake¶

Snowflake supports standard SQL, including a subset of ANSI SQL:1999 and the
SQL:2003 analytic extensions. Snowflake also supports common variations for a
number of commands where those variations do not conflict with each other.

Tip

You can use the search optimization service to improve query performance. For
details, see [Search Optimization Service](user-guide/search-optimization-
service).

[Working with Joins](user-guide/querying-joins)

    

A join combines rows from two tables to create a new combined row that can be
used in the query.

Learn join concepts, types of joins, and how to work with joins.

[Analyzing time-series data](user-guide/querying-time-series-data)

    

Analyze time-series data, using SQL functionality designed for this purpose,
such as the ASOF JOIN feature, date and time helper functions, aggregate
functions for downsampling, and functions that support sliding window frames.

Using ASOF JOIN, learn how to join tables on timestamp columns when their
values closely follow each other, precede each other, or match exactly.

[Eliminate Redundant Joins](user-guide/join-elimination)

    

A join on a key column can refer to tables that are not needed for the join.
Such a join is referred to as a _redundant join_.

Learn about redundant joins, and how to eliminate them to improve query
performance.

[Working with Subqueries](user-guide/querying-subqueries)

    

A subquery is a query within another query.

Learn about subqueries and how to use them.

[Querying Hierarchical Data](user-guide/queries-hierarchical)

    

Relational databases often store hierarchical data by using different tables.

Learn about querying hierarchical data using joins, Common Table
Expressions(CTEs) and CONNECT BY.

[Working with CTEs (Common Table Expressions)](user-guide/queries-cte)

    

A CTE (common table expression) is a named subquery defined in a WITH clause,
the result of which is effectively a table.

Learn how to write and work with CTE expressions.

[Querying Semi-structured Data](user-guide/querying-semistructured)

    

Semi-structured data represents arbitrary hierarchical data structures, which
can be used to load and operate on data in semi-structured formats (e.g. JSON,
Avro, ORC, Parquet, or XML).

Learn how to use special operators and functions to query complex hierarchical
data stored in a VARIANT.

[Using full-text search](user-guide/querying-with-search-functions)

    

You can use full-text search to find character data (text) in specified
columns from one or more tables, including fields in VARIANT, OBJECT, and
ARRAY columns.

Learn how to run queries that use full-text search.

[Constructing SQL at runtime](user-guide/querying-construct-at-runtime)

    

You can create programs that construct SQL statements dynamically at runtime.

Learn about different options for constructing SQL at runtime.

[Analyzing data with window functions](user-guide/functions-window-using)

    

Window functions operate on windows, which are groups of rows that are related
in some way.

Learn about windows, window functions, and how to use window functions to
examine data.

[Identifying Sequences of Rows That Match a Pattern](user-guide/match-
recognize-introduction)

    

In some cases, you might need to identify sequences of table rows that match a
pattern.

Learn about pattern matching, and how to use MATCH_RECOGNIZE to work with
table rows matching patterns.

[Using Sequences](user-guide/querying-sequences)

    

Sequences are used to generate unique numbers across sessions and statements,
including concurrent statements.

Learn what are sequences, and how to use them.

[Using Persisted Query Results](user-guide/querying-persisted-results)

    

When a query is executed, the result is persisted for a period of time.

Learn how query results are persisted, how long persisted results are
available, and how to use persisted query results to improve performance.

[Computing the Number of Distinct Values](user-guide/querying-distinct-counts)

    

Various methods exist to determine the count of distinct elements within a
column.

Learn methods to identify and report distinct elements in data.

[Estimating Similarity of Two or More Sets](user-guide/querying-approximate-
similarity)

    

Snowflake provides mechanisms to compare data sets for similarity.

Learn how Snowflake determines similarity and how to compare multiple data
sets for similarity.

[Estimating Frequent Values](user-guide/querying-approximate-frequent-values)

    

Snowflake can examine data to determine how frequent values are within the
data.

Learn how frequency is determined and how to query data to determine data
frequency using the through the APPROX_TOP_K family of functions.

[Estimating Percentile Values](user-guide/querying-approximate-percentile-
values)

    

Snowflake can estimate percentages of values using an improved version of the
t-Digest algorithm.

Learn how to estimate percentages using the APPROX_PERCENTILE family of
functions

[Querying data using worksheets](user-guide/ui-snowsight-query)

    

Query Profiles provide execution details for a query.

Learn how examine queries, using query profiles, to understand and improve
performance.

[Using the Query Hash to Identify Patterns and Trends in Queries](user-
guide/query-hash)

    

To identify patterns and trends in queries, you can use the hash of the query
text, which is included in the `query_hash` and `query_parameterized_hash`
columns in selected Account Usage view and in the output of selected
Information Schema table functions.

Learn how to use the query hash in these columns to identify repeated queries
and detect patterns and trends in queries.

[Top-K pruning for improved query performance](user-guide/querying-top-k-
pruning-optimization)

    

Instead of scanning all eligible rows in SELECT statements that contain LIMIT
and ORDER BY clauses, SELECT statements that use top-K pruning scan a subset
of rows, which can improve performance.

Learn how to use top-K pruning to improve the performance of SELECT statements
that contain LIMIT and ORDER BY clauses.

[Canceling Statements](user-guide/querying-cancel-statements)

    

Executing statements are typically cancelled using the interface used to start
the query.

Learn how to use system functions to cancel a specific query or all currently
executing queries.

