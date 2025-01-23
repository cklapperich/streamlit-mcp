# Views, materialized views, and dynamic tables¶

Snowflake provides a variety of structures to view, materialize, and otherwise
transform data. Three of the most common mechanisms are:

  * [Views](views-introduction): Snowflake provides what would be considered a traditional database view. In general, a view allows the result of a query to be accessed as if it were a table, including linking (or in database parlance, joining) two or more tables or other views into a single logical view. Once defined, views can be queried like any other table.

  * [Materialized views](views-materialized): Materialized views differ from traditional views by providing the ability to pre-compute the dataset based on materialized view query. Because the result is pre-computed, querying a materialized view is faster than executing a query against the base table of the view. This performance difference can be significant when a query is run frequently or is sufficiently complex. As a result, materialized views can speed up expensive aggregation, projection, and selection operations, especially those that run frequently and that run on large data sets.

  * [Dynamic Tables](dynamic-tables-intro): Dynamic tables materialize the results of a specified query. Instead of creating a separate target table and writing code to transform and update the data in that table, you can define the target table as a dynamic table, and you can specify the SQL statement that performs the transformation. Background automation then keeps the dynamic table up to date based on the refresh criteria that you specify.

## Comparison of Views, materialized views, and dynamic tables¶

Object type | Pros | Cons | Limitations and More information  
---|---|---|---  
View | Simple, easily defined, consumes no storage. | Inflexible, slow, requires compute to generate results. | See [Limitations on Views](views-introduction.html#label-views-introduction-limitations).  
Materialized View | Fast results retrieval. Relatively simple definition. Somewhat flexible. Always up to date. | Incurs compute to keep up to date. Consumes storage. | For more information, including limitations in materialized views, see [Working with Materialized Views](views-materialized).  
Dynamic Tables | Extremely fast results retrieval. Relatively simple definition. Very flexible. Fine control on refresh. Can provide complex transformations. | Incurs compute cost to be kept up to date. Consumes storage. Requires careful consideration as to how often to refresh, and when and how to refresh. | For more information, see [Dynamic tables](dynamic-tables-intro).

