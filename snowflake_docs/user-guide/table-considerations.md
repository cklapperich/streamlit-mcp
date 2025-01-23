# Table Design Considerations¶

This topic provides best practices, general guidelines, and important
considerations when designing and managing tables.

## Date/Time Data Types for Columns¶

When defining columns to contain dates or timestamps, Snowflake recommends
choosing a [date or timestamp data type](../sql-reference/data-types-datetime)
rather than a character data type. Snowflake stores DATE and TIMESTAMP data
more efficiently than VARCHAR, resulting in better query performance. Choose
an appropriate date or timestamp data type, depending on the level of
granularity required.

## Referential Integrity Constraints¶

When they are created on standard tables, referential integrity constraints,
as defined by primary-key/foreign-key relationships, are informational; they
are not enforced. NOT NULL constraints are enforced, but other constraints are
not. However, constraints on [hybrid tables](tables-hybrid) are enforced; see
[Overview of Constraints](../sql-reference/constraints-overview).

In general, constraints provide valuable metadata. Primary and foreign keys
enable your project team to understand the schema design and see the
relationships between the tables and their columns.

Additionally, most business intelligence (BI) and visualization tools import
the foreign key definitions with the tables and build the proper join
conditions. This approach saves time and is potentially less prone to error
than someone having to guess how to join the tables and manually configure the
tool. Basing joins on primary and foreign keys also brings integrity to the
design, because the joins are not left to different developers to interpret.
Some BI and visualization tools also take advantage of constraint information
to rewrite queries more efficiently, for example, by using join elimination.

Specify a constraint when creating or modifying a table using the [CREATE | ALTER TABLE … CONSTRAINT](../sql-reference/sql/create-table-constraint) commands.

In the following example, the CREATE TABLE statement for the second table
(`salesorders`) defines an out-of-line foreign key constraint that references
a column in the first table (`salespeople`):

    
    
    CREATE OR REPLACE TABLE salespeople (
      sp_id INT NOT NULL UNIQUE,
      name VARCHAR DEFAULT NULL,
      region VARCHAR,
      constraint pk_sp_id PRIMARY KEY (sp_id)
    );
    CREATE OR REPLACE TABLE salesorders (
      order_id INT NOT NULL UNIQUE,
      quantity INT DEFAULT NULL,
      description VARCHAR,
      sp_id INT NOT NULL UNIQUE,
      constraint pk_order_id PRIMARY KEY (order_id),
      constraint fk_sp_id FOREIGN KEY (sp_id) REFERENCES salespeople(sp_id)
    );
    

Copy

Query the [GET_DDL](../sql-reference/functions/get_ddl) function to retrieve a
DDL statement that could be executed to recreate the specified table. The
statement includes the constraints currently set on a table.

For example:

    
    
    SELECT GET_DDL('TABLE', 'mydb.public.salesorders');
    

Copy

    
    
    +-----------------------------------------------------------------------------------------------------+
    | GET_DDL('TABLE', 'MYDATABASE.PUBLIC.SALESORDERS')                                                   |
    |-----------------------------------------------------------------------------------------------------|
    | create or replace TABLE SALESORDERS (                                                               |
    |   ORDER_ID NUMBER(38,0) NOT NULL,                                                                   |
    |   QUANTITY NUMBER(38,0),                                                                            |
    |   DESCRIPTION VARCHAR(16777216),                                                                    |
    |   SP_ID NUMBER(38,0) NOT NULL,                                                                      |
    |   unique (SP_ID),                                                                                   |
    |   constraint PK_ORDER_ID primary key (ORDER_ID),                                                    |
    |   constraint FK_SP_ID foreign key (SP_ID) references MYDATABASE.PUBLIC.SALESPEOPLE(SP_ID)           |
    | );                                                                                                  |
    +-----------------------------------------------------------------------------------------------------+
    

Alternatively, retrieve a list of all table constraints by schema (or across
all schemas in a database) by querying the [TABLE_CONSTRAINTS view](../sql-
reference/info-schema/table_constraints) in the Information Schema.

For example:

    
    
    SELECT table_name, constraint_type, constraint_name
      FROM mydb.INFORMATION_SCHEMA.TABLE_CONSTRAINTS
      WHERE constraint_schema = 'PUBLIC'
      ORDER BY table_name;
    

Copy

    
    
    +-------------+-----------------+-----------------------------------------------------+
    | TABLE_NAME  | CONSTRAINT_TYPE | CONSTRAINT_NAME                                     |
    |-------------+-----------------+-----------------------------------------------------|
    | SALESORDERS | UNIQUE          | SYS_CONSTRAINT_fce2257e-c343-4e66-9bea-fc1c041b00a6 |
    | SALESORDERS | FOREIGN KEY     | FK_SP_ID                                            |
    | SALESORDERS | PRIMARY KEY     | PK_ORDER_ID                                         |
    | SALESORDERS | UNIQUE          | SYS_CONSTRAINT_bf90e2b3-fd4a-4764-9576-88fb487fe989 |
    | SALESPEOPLE | PRIMARY KEY     | PK_SP_ID                                            |
    +-------------+-----------------+-----------------------------------------------------+
    

## When to Set a Clustering Key¶

Specifying a [clustering key](tables-clustering-keys.html#label-clustering-
keys) is not necessary for most tables. Snowflake performs automatic tuning
via the optimization engine and micro-partitioning. In many cases, data is
loaded and organized into micro-partitions by date or timestamp, and is
queried along the same dimension.

When should you specify a clustering key for a table? First, note that
clustering a small table typically doesn’t improve query performance
significantly.

For larger data sets, you might consider specifying a clustering key for a
table when:

  * The order in which the data is loaded does not match the dimension by which it is most commonly queried (e.g. the data is loaded by date, but reports filter the data by ID). If your existing scripts or reports query the data by both date and ID (and potentially a third or fourth column), you may see some performance improvement by creating a multi-column clustering key.

  * [Query Profile](ui-snowsight-activity) indicates that a significant percentage of the total duration time for typical queries against the table is spent scanning. This applies to queries that filter on one or more specific columns.

Note that reclustering rewrites existing data with a different order. The
previous ordering is stored for 7 days to provide Fail-safe protection.
Reclustering a table incurs compute costs that correlate to the size of the
data that is reordered.

For more information, see [Automatic Clustering](tables-auto-reclustering).

## When to Specify Column Lengths¶

Snowflake compresses column data effectively; therefore, creating columns
larger than necessary has minimal impact on the size of data tables. Likewise,
there is no query performance difference between a column with a maximum
length declaration (e.g. `VARCHAR(16777216)`), and a smaller precision.

However, when the size of your column data is predictable, Snowflake
recommends defining an appropriate column length, for the following reasons:

  * Data loading operations are more likely to detect issues such as columns loaded out of order, e.g. a 50-character string loaded erroneously into a VARCHAR(10) column. Such issues produce errors.

  * When the column length is unspecified, some third-party tools may anticipate consuming the maximum size value, which can translate into increased client-side memory usage or unusual behavior.

## Storing Semi-structured Data in a VARIANT Column vs. Flattening the Nested
Structure¶

If you are not sure yet what types of operations you want perform on your
semi-structured data, Snowflake recommends storing the data in a VARIANT
column for now. For data that is mostly regular and uses only native types
(strings and integers), the storage requirements and query performance for
operations on relational data and data in a VARIANT column is very similar.

For better pruning and less storage consumption, Snowflake recommends
flattening your object and key data into separate relational columns if your
semi-structured data includes:

  * Dates and timestamps, especially non-ISO 8601 dates and timestamps, as string values

  * Numbers within strings

  * Arrays

Non-native values such as dates and timestamps are stored as strings when
loaded into a VARIANT column, so operations on these values could be slower
and also consume more space than when stored in a relational column with the
corresponding data type.

If you know your use cases for the data, perform tests on a typical data set.
Load the data set into a VARIANT column in a table. Use the FLATTEN function
to extract the objects and keys you plan to query into a separate table. Run a
typical set of queries against both tables to see which structure provides the
best performance.

## Converting a Permanent Table to a Transient Table or Vice-Versa¶

Currently, it is not possible to change a permanent table to a
[transient](tables-temp-transient) table using the [ALTER TABLE](../sql-
reference/sql/alter-table) command. The TRANSIENT property is set at table
creation and cannot be modified.

Similarly, it is not possible to directly change a transient table to a
permanent table.

To convert an existing permanent table to a transient table (or vice versa)
while preserving data and other characteristics such as column defaults and
granted privileges, you can create a new table and use the `COPY GRANTS`
clause, then copy the data:

    
    
    CREATE TRANSIENT TABLE my_new_table LIKE my_old_table COPY GRANTS;
    INSERT INTO my_new_table SELECT * FROM my_old_table;
    

Copy

If you want to preserve all of the data, but not the granted privileges and
other characteristics, you can use a [CREATE TABLE AS SELECT (CTAS)](../sql-
reference/sql/create-table), for example:

    
    
    CREATE TRANSIENT TABLE my_transient_table AS SELECT * FROM mytable;
    

Copy

Another way to make a copy of a table (but change the lifecycle from permanent
to transient) is to `CLONE` the table, for example:

    
    
    CREATE TRANSIENT TABLE foo CLONE bar COPY GRANTS;
    

Copy

Old partitions are _not_ affected (they do not become transient), but new
partitions added to the clone will follow the transient lifecycle.

You cannot clone a transient table to a permanent table.

