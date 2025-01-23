# Understanding Snowflake Table Structures¶

All data in Snowflake is stored in database tables, logically structured as
collections of columns and rows. To best utilize Snowflake tables,
particularly large tables, it is helpful to have an understanding of the
physical structure behind the logical structure.

These topics describe _micro-partitions_ and _data clustering_ , two of the
principal concepts utilized in Snowflake physical table structures. They also
provides guidance for explicitly defining _clustering keys_ for very large
tables (in the multi-terabyte range) to help optimize table maintenance and
query performance.

**Next Topics:**

  * [Micro-partitions & Data Clustering](tables-clustering-micropartitions)
  * [Clustering Keys & Clustered Tables](tables-clustering-keys)
  * [Automatic Clustering](tables-auto-reclustering)
  * [Manual Reclustering — _Deprecated_](tables-clustering-manual)

