# Overview of the Data Lifecycle¶

Snowflake provides support for all standard SELECT, DDL, and DML operations
across the lifecycle of data in the system, from organizing and storing data
to querying and working with data, as well as removing data from the system.

## Lifecycle Diagram¶

All user data in Snowflake is logically represented as tables that can be
queried and modified through standard SQL interfaces. Each table belongs to a
schema which in turn belongs to a database.

![Snowflake Data Lifecycle](../_images/data-lifecycle.png)

## Organizing Data¶

You can organize your data into databases, schemas, and tables. Snowflake does
not limit the number of databases you can create or the number of schemas you
can create within a database. Snowflake also does not limit the number of
tables you can create in a schema.

For more information, see:

  * [CREATE DATABASE](../sql-reference/sql/create-database)

  * [ALTER DATABASE](../sql-reference/sql/alter-database)

  * [CREATE SCHEMA](../sql-reference/sql/create-schema)

  * [ALTER SCHEMA](../sql-reference/sql/alter-schema)

  * [CREATE TABLE](../sql-reference/sql/create-table)

  * [ALTER TABLE](../sql-reference/sql/alter-table)

## Storing Data¶

You can insert data directly into tables. In addition, Snowflake provides DML
for loading data into Snowflake tables from external, formatted files.

For more information, see:

  * [INSERT](../sql-reference/sql/insert)

  * [COPY INTO <table>](../sql-reference/sql/copy-into-table)

## Querying Data¶

Once data is stored in a table, you can issue SELECT statements to query the
data.

For more information, see [SELECT](../sql-reference/sql/select).

## Working with Data¶

Once data is stored in a table, all standard DML operations can be performed
on the data. In addition, Snowflake supports DDL actions such as cloning
entire databases, schemas, and tables.

For more information, see:

  * [UPDATE](../sql-reference/sql/update)

  * [MERGE](../sql-reference/sql/merge)

  * [DELETE](../sql-reference/sql/delete)

  * [CREATE <object> … CLONE](../sql-reference/sql/create-clone)

## Removing Data¶

In addition to using the DML command, [DELETE](../sql-reference/sql/delete),
to remove data from a table, you can truncate or drop an entire table. You can
also drop entire schemas and databases.

For more information, see:

  * [TRUNCATE TABLE](../sql-reference/sql/truncate-table)

  * [DROP TABLE](../sql-reference/sql/drop-table)

  * [DROP SCHEMA](../sql-reference/sql/drop-schema)

  * [DROP DATABASE](../sql-reference/sql/drop-database)

