# Dynamic tables¶

Dynamic tables simplify data engineering in Snowflake by providing a reliable,
cost-effective, and automated way to transform data. Instead of managing
transformation steps with tasks and scheduling, you define the end state using
dynamic tables and let Snowflake handle the pipeline management.

Here’s why they’re beneficial:

  * **Declarative programming** : Define your pipeline outcomes using declarative SQL without worrying about the steps to achieve them, reducing complexity.

  * **Transparent orchestration** : Easily create pipelines of various shapes, from linear chains to directed graphs, by chaining dynamic tables together. Snowflake manages the orchestration and scheduling of pipeline refresh based on your data freshness target.

  * **Performance boost with incremental processing** : For [favorable workloads](dynamic-table-performance-guide) that are suited for incremental processing, dynamic tables can provide a significant performance improvement over full refreshes.

  * **Easy switching** : Transition seamlessly from batch to streaming with a single ALTER DYNAMIC TABLE command. You control how often data is refreshed in your pipeline, which helps balance cost and data freshness.

  * **Operationalization** : Dynamic tables are fully observable and manageable through Snowsight, and also offer programmatic access to build your own observability apps.

A dynamic table reflects query results, eliminating the need for a separate
target table and custom code for data transformation. An automated process
updates the results regularly through scheduled [refreshes](dynamic-tables-
refresh). Since a dynamic table’s content is based on the query, you can’t
modify it using DML operations. The automated refresh process materializes
query results into the dynamic table.

The following topics introduce dynamic table concepts and explain how to
transform data in a continuous data pipeline using dynamic tables.

Concept | Description  
---|---  
[How dynamic tables work](dynamic-tables-about) | Learn about the privileges needed to work with dynamic tables, how dynamic table refresh operates, and the distinctions between dynamic tables, streams & tasks, and materialized views.  
[Working with dynamic tables](dynamic-tables-working-with) | Learn about creating, managing, and monitoring dynamic tables.  
[Best practices for dynamic tables](dynamic-tables-best-practices) | Understand the best practices for working with dynamic tables.  
[Understanding cost for dynamic tables](dynamic-tables-cost) | Understand the compute and storage cost for dynamic tables.  
[Known limitations for dynamic tables](dynamic-tables-limitations) | Some actions might be restricted due to limitations on using dynamic tables or if you don’t have the necessary privileges.

