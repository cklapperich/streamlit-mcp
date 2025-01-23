# Snowflake Connector for Spark¶

The Snowflake Connector for Spark (“Spark connector”) brings Snowflake into
the Apache Spark ecosystem, enabling Spark to read data from, and write data
to, Snowflake. From Spark’s perspective, Snowflake looks similar to other
Spark data sources (PostgreSQL, HDFS, S3, etc.).

Note

As an alternative to using Spark, consider writing your code to use [Snowpark
API](../developer-guide/snowpark/index) instead. Snowpark allows you to
perform all of your work within Snowflake (rather than in a separate Spark
compute cluster). Snowpark also supports pushdown of all operations, including
Snowflake UDFs.

Snowflake supports three versions of Spark: Spark 3.2, Spark 3.3, and Spark
3.4. There is a separate version of the Snowflake connector for each version
of Spark. Use the correct version of the connector for your version of Spark.

The connector runs as a Spark plugin and is provided as a Spark package
(`spark-snowflake`).

**Next Topics:**

  * [Overview of the Spark Connector](spark-connector-overview)
  * [Installing and Configuring the Spark Connector](spark-connector-install)
  * [Configuring Snowflake for Spark in Databricks](spark-connector-databricks)
  * [Configuring Snowflake for Spark in Qubole](spark-connector-qubole)
  * [Using the Spark Connector](spark-connector-use)

