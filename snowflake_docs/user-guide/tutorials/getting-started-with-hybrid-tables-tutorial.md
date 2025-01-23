# Getting started with hybrid tables¶

## Introduction¶

A [hybrid table](../tables-hybrid) is a Snowflake table type that is optimized
for hybrid transactional and analytic workloads. These workloads require low
latency and high throughput on small but random reads and writes, which often
access a single row in a table. Hybrid tables enforce unique and referential
integrity constraints, which are critical for transactional workloads.

You can use a hybrid table along with other Snowflake tables and features to
power [Unistore workloads](https://www.snowflake.com/en/data-
cloud/workloads/unistore/), which unite transactional and analytic data in a
single platform.

Hybrid tables are integrated seamlessly into the existing Snowflake
architecture. Customers connect to the same Snowflake database service.
Queries are compiled and optimized in the cloud services layer and executed in
the same query engine in virtual warehouses. This architecture provides
several key benefits:

  * Snowflake platform features, such as data governance, work with hybrid tables out of the box.

  * You can run hybrid workloads that mix operational and analytic queries.

  * You can join hybrid tables with other Snowflake tables, and the query executes natively and efficiently in the same query engine. No federation is required.

  * You can execute an atomic transaction across hybrid tables and other Snowflake tables. There is no need to orchestrate your own two-phase commit.

![Unistore architecture](../../_images/unistore-arch.png)

Hybrid tables leverage a row store as the primary data store to provide
excellent operational query performance. When you write to a hybrid table, the
data is written directly into the row store. Data is asynchronously copied
into object storage in order to provide better performance and workload
isolation for large scans without affecting ongoing operational workloads.
Some data may also be cached in columnar format on your warehouse in order to
provide better performance on analytical queries. You simply execute SQL
statements against the logical hybrid table, and the query optimizer decides
where to read data from to provide the best performance. You get one
consistent view of your data without worrying about the underlying
infrastructure.

### What you will learn¶

In this tutorial you will learn how to:

  * Create and bulk load hybrid tables.

  * Create and check the enforcement of UNIQUE, PRIMARY KEY, and FOREIGN KEY constraints.

  * Run concurrent updates that depend on row-level locks.

  * Run a multi-statement operation in a consistent atomic transaction (across hybrid and standard tables).

  * Query hybrid tables and join them to standard tables.

  * Verify that security and governance principles apply to both hybrid and standard tables.

## Prerequisites¶

This tutorial assumes that you are:

  * Familiar with the Snowsight interface

  * Familiar with SQL

  * Using a non-trial Snowflake account in [select AWS regions](../tables-hybrid-limitations.html#label-hybrid-table-limitations-regions)

  * Able to run as a user who has been granted the ACCOUNTADMIN role

  * Aware of [unsupported features and limitations on hybrid tables](../tables-hybrid-limitations)

## Step 1. Set up your account¶

To get started, set up your Snowflake account by creating a new worksheet, a
role, database objects, and a virtual warehouse. Then you will be able to
create two hybrid tables and one standard table. Follow these steps:

  1. Under Worksheets, click the + button in the top-right corner of Snowsight and select SQL Worksheet.

  2. Rename the worksheet by selecting its auto-generated timestamp name and typing `Hybrid Tables - QuickStart`.

  3. Complete the following steps by copying the block of SQL commands into your worksheet and running them all.

    1. Use the ACCOUNTADMIN role to create the `hybrid_quickstart_role` custom role, then grant this role to the current user.

    2. Create the `hybrid_quickstart_wh` warehouse and the `hybrid_quickstart_db` database. Grant ownership on these objects to the new role.

    3. Use the new role to create the `data` schema.

    4. Use the new warehouse. (The database and schema you created are already in use, by default.)
    
        USE ROLE ACCOUNTADMIN;
    CREATE OR REPLACE ROLE hybrid_quickstart_role;
    SET my_user = CURRENT_USER();
    GRANT ROLE hybrid_quickstart_role TO USER IDENTIFIER($my_user);
    
    CREATE OR REPLACE WAREHOUSE hybrid_quickstart_wh WAREHOUSE_SIZE = XSMALL, AUTO_SUSPEND = 300, AUTO_RESUME = TRUE;
    GRANT OWNERSHIP ON WAREHOUSE hybrid_quickstart_wh TO ROLE hybrid_quickstart_role;
    CREATE OR REPLACE DATABASE hybrid_quickstart_db;
    GRANT OWNERSHIP ON DATABASE hybrid_quickstart_db TO ROLE hybrid_quickstart_role;
    
    USE ROLE hybrid_quickstart_role;
    CREATE OR REPLACE SCHEMA data;
    
    USE WAREHOUSE hybrid_quickstart_wh;
    

Copy

## Step 2. Create and bulk load three tables¶

This tutorial uses the Tasty Bytes Snowflake fictional food truck business to
simulate a use case where you can serve data to an application.

You will create three tables:

  * `order_header` hybrid table - This table stores order metadata such as `truck_id`, `customer_id`, `order_amount`, and so on.

  * `truck` hybrid table - This table stores truck metadata such as `truck_id`, `franchise_id`, `menu_type_id`, and so on.

  * `truck_history` standard table - This table stores historical information about food trucks, enabling you to track changes over time.

You are creating hybrid and standard tables to demonstrate how well they work
together. Nonetheless, hybrid tables have some fundamental differences in
their definition and behavior:

  * Hybrid tables require a primary key on one or more columns (which implies the creation of a primary key index).

  * Hybrid tables allow the creation of [secondary indexes](../tables-hybrid-create.html#label-add-secondary-indexes) on any column.

  * PRIMARY KEY, FOREIGN KEY, and UNIQUE [constraints](../../sql-reference/constraints-overview) are all enforced on hybrid tables.

  * Locks on hybrid tables are [row-level](../../sql-reference/transactions.html#label-txn-locking), not table-level.

  * Hybrid table data resides in a row store, but is also copied to columnar object storage.

These differences result in:

  * Support for referential integrity when table data is loaded, updated, or deleted.

  * Faster DML operations (especially those that update single rows).

  * Faster lookup queries.

You may bulk load data into hybrid tables by copying data from a stage or from
other tables (that is, by using [CTAS](../../sql-reference/sql/create-
table.html#label-ctas-syntax), [COPY INTO <table>](../../sql-
reference/sql/copy-into-table), or [INSERT INTO … SELECT](../../sql-
reference/sql/insert)). Bulk loading data into a hybrid table using a CTAS
statement is strongly recommended because there are several optimizations that
can only be applied when data is loaded as part of the creation of the table.

Create a [file format](../../sql-reference/sql/create-file-format), which
describes a staged data set that you can access or load into Snowflake tables,
and a [stage](../data-load-overview), which is a Snowflake object that points
to a cloud storage location that Snowflake can access to both ingest and query
data. The data is stored in a publicly accessible AWS S3 bucket that you
reference when you create the stage.

    
    
    CREATE OR REPLACE FILE FORMAT csv_format TYPE = CSV FIELD_DELIMITER = ',' SKIP_HEADER = 1 NULL_IF = ('NULL', 'null') EMPTY_FIELD_AS_NULL = true;
    CREATE OR REPLACE STAGE frostbyte_tasty_bytes_stage URL = 's3://sfquickstarts/hybrid_table_guide' FILE_FORMAT = csv_format;
    

Copy

Now use the [LIST](../../sql-reference/sql/list) statement to return all the
files in the FROSTBYTE_TASTY_BYTES_STAGE:

    
    
    LIST @frostbyte_tasty_bytes_stage;
    

Copy

The statement should return two records: one for the `TRUCK.csv` file and one
for the `ORDER_HEADER.csv` file.

![Output of LIST command, with names and sizes of two
files.](../../_images/list_tasty_bytes_stage.png)

After you have created the stage, which points to the location of the data in
cloud storage, you can create and load the data into the `truck` by using a
[CTAS command](../../sql-reference/sql/create-hybrid-table) that selects data
from the `TRUCK.csv` file. Note the PRIMARY KEY constraint on the `truck_id`
column.

The second DDL statement creates a standard table named `truck_history`, also
by using a CTAS statement.

    
    
    SET CURRENT_TIMESTAMP = CURRENT_TIMESTAMP();
    
    CREATE OR REPLACE HYBRID TABLE truck (
      truck_id NUMBER(38,0) NOT NULL,
      menu_type_id NUMBER(38,0),
      primary_city VARCHAR(16777216),
      region VARCHAR(16777216),
      iso_region VARCHAR(16777216),
      country VARCHAR(16777216),
      iso_country_code VARCHAR(16777216),
      franchise_flag NUMBER(38,0),
      year NUMBER(38,0),
      make VARCHAR(16777216),
      model VARCHAR(16777216),
      ev_flag NUMBER(38,0),
      franchise_id NUMBER(38,0),
      truck_opening_date DATE,
      truck_email VARCHAR NOT NULL UNIQUE,
      record_start_time TIMESTAMP,
      PRIMARY KEY (truck_id)
      )
      AS
      SELECT
          t.$1 AS truck_id,
          t.$2 AS menu_type_id,
          t.$3 AS primary_city,
          t.$4 AS region,
          t.$5 AS iso_region,
          t.$6 AS country,
          t.$7 AS iso_country_code,
          t.$8 AS franchise_flag,
          t.$9 AS year,
          t.$10 AS make,
          t.$11 AS model,
          t.$12 AS ev_flag,
          t.$13 AS franchise_id,
          t.$14 AS truck_opening_date,
          CONCAT(truck_id, '_truck@email.com') truck_email,
          $CURRENT_TIMESTAMP AS record_start_time
        FROM @FROSTBYTE_TASTY_BYTES_STAGE (PATTERN=>'.*TRUCK.csv') t;
    
    CREATE OR REPLACE TABLE truck_history (
      truck_id NUMBER(38,0) NOT NULL,
      menu_type_id NUMBER(38,0),
      primary_city VARCHAR(16777216),
      region VARCHAR(16777216),
      iso_region VARCHAR(16777216),
      country VARCHAR(16777216),
      iso_country_code VARCHAR(16777216),
      franchise_flag NUMBER(38,0),
      year NUMBER(38,0),
      make VARCHAR(16777216),
      model VARCHAR(16777216),
      ev_flag NUMBER(38,0),
      franchise_id NUMBER(38,0),
      truck_opening_date DATE,
      truck_email VARCHAR NOT NULL UNIQUE,
      record_start_time TIMESTAMP,
      record_end_time TIMESTAMP,
      PRIMARY KEY (truck_id)
      )
      AS
      SELECT
          t.$1 AS truck_id,
          t.$2 AS menu_type_id,
          t.$3 AS primary_city,
          t.$4 AS region,
          t.$5 AS iso_region,
          t.$6 AS country,
          t.$7 AS iso_country_code,
          t.$8 AS franchise_flag,
          t.$9 AS year,
          t.$10 AS make,
          t.$11 AS model,
          t.$12 AS ev_flag,
          t.$13 AS franchise_id,
          t.$14 AS truck_opening_date,
          CONCAT(truck_id, '_truck@email.com') truck_email,
          $CURRENT_TIMESTAMP AS record_start_time,
          NULL AS record_end_time
       FROM @frostbyte_tasty_bytes_stage (PATTERN=>'.*TRUCK.csv') t;
    

Copy

The following DDL statement creates the structure for the `order_header`
hybrid table. Note the PRIMARY KEY constraint on the `order_id` column, the
FOREIGN KEY constraint on the `truck_id` column from the `truck` table, and
the secondary index on the `order_ts` column.

    
    
    CREATE OR REPLACE HYBRID TABLE order_header (
      order_id NUMBER(38,0) NOT NULL,
      truck_id NUMBER(38,0),
      location_id NUMBER(19,0),
      customer_id NUMBER(38,0),
      discount_id FLOAT,
      shift_id NUMBER(38,0),
      shift_start_time TIME(9),
      shift_end_time TIME(9),
      order_channel VARCHAR(16777216),
      order_ts TIMESTAMP_NTZ(9),
      served_ts VARCHAR(16777216),
      order_currency VARCHAR(3),
      order_amount NUMBER(38,4),
      order_tax_amount VARCHAR(16777216),
      order_discount_amount VARCHAR(16777216),
      order_total NUMBER(38,4),
      order_status VARCHAR(16777216) DEFAULT 'INQUEUE',
      PRIMARY KEY (order_id),
      FOREIGN KEY (truck_id) REFERENCES TRUCK(truck_id),
      INDEX IDX01_ORDER_TS(order_ts)
    );
    

Copy

The following DML statement inserts data into the `order_header` table, using
an INSERT INTO … SELECT statement.

    
    
    INSERT INTO order_header (
      order_id,
      truck_id,
      location_id,
      customer_id,
      discount_id,
      shift_id,
      shift_start_time,
      shift_end_time,
      order_channel,
      order_ts,
      served_ts,
      order_currency,
      order_amount,
      order_tax_amount,
      order_discount_amount,
      order_total,
      order_status)
      SELECT
          t.$1 AS order_id,
          t.$2 AS truck_id,
          t.$3 AS location_id,
          t.$4 AS customer_id,
          t.$5 AS discount_id,
          t.$6 AS shift_id,
          t.$7 AS shift_start_time,
          t.$8 AS shift_end_time,
          t.$9 AS order_channel,
          t.$10 AS order_ts,
          t.$11 AS served_ts,
          t.$12 AS order_currency,
          t.$13 AS order_amount,
          t.$14 AS order_tax_amount,
          t.$15 AS order_discount_amount,
          t.$16 AS order_total,
          '' as order_status
        FROM @frostbyte_tasty_bytes_stage (PATTERN=>'.*ORDER_HEADER.csv') t;
    

Copy

## Step 3. Explore your data¶

Earlier you created the `hybrid_quickstart_role` role, `hybrid_quickstart_wh`
warehouse, `hybrid_quickstart_db` database, and `data` schema. Continue to use
those objects.

You also created and loaded the `truck`, `truck_history`, and `order_header`
tables. Now you can run a few queries and become familiar with both the data
in these tables and their metadata.

Use the [SHOW TABLES](../../sql-reference/sql/show-tables) command to view
properties and metadata for both standard tables and hybrid tables. Use the
[SHOW HYBRID TABLES](../../sql-reference/sql/show-hybrid-tables) command to
view information about hybrid tables only.

    
    
    SHOW TABLES LIKE '%truck%';
    

Copy

![Output of SHOW TABLES command for the truck
table](../../_images/show_tables_like_truck.png)

    
    
    SHOW HYBRID TABLES LIKE '%order_header%';
    

Copy

![Output of SHOW HYBRID TABLES command for the order_header
table](../../_images/show_hybrid_tables_like_order_header.png)

Display information about the columns in the table by using [DESCRIBE
<object>](../../sql-reference/sql/desc) commands. Note the columns with
PRIMARY KEY and UNIQUE constraints.

    
    
    DESCRIBE TABLE truck;
    

Copy

![Output of DESCRIBE command for the truck
table](../../_images/describe_table_truck.png)

    
    
    DESCRIBE TABLE order_header;
    

Copy

![Output of DESCRIBE command for the order_header
table](../../_images/describe_table_order_header.png)

List the [hybrid tables](../../sql-reference/sql/show-hybrid-tables) for which
you have access privileges.

    
    
    SHOW HYBRID TABLES;
    

Copy

![Output of SHOW HYBRID TABLES command](../../_images/show_hybrid_tables.png)

List all the [indexes](../../sql-reference/sql/show-indexes) for which you
have access privileges. Note the value in the `is_unique` column for each
index.

    
    
    SHOW INDEXES;
    

Copy

![Output of SHOW INDEXES command](../../_images/show_indexes.png)

Look at sample data from the tables by running these simple queries.

    
    
    SELECT * FROM truck LIMIT 10;
    SELECT * FROM truck_history LIMIT 10;
    SELECT * FROM order_header LIMIT 10;
    

Copy

The output for the first query looks similar to the following:

![Output of SELECT query against truck
table](../../_images/select_from_truck.png)

## Step 4. Test the behavior of UNIQUE and FOREIGN KEY constraints¶

In this step, you will test UNIQUE and FOREIGN KEY [constraints](../../sql-
reference/constraints-overview). These constraints are enforced when they are
defined on hybrid tables.

UNIQUE constraints preserve data integrity by preventing duplicate values from
being inserted into a column. FOREIGN KEY constraints work in tandem with
PRIMARY KEY constraints to preserve referential integrity. A value cannot be
inserted into a primary key column if no matching foreign key value exists in
the referenced table. For example, a sale of a product with ID `100` cannot be
recorded in a sales fact table if no such product ID already exists in a
referenced product dimension table.

Both types of constraints support data accuracy and consistency for
applications that rely heavily on reliable but fast transaction processing.

### Step 4.1. Test a UNIQUE constraint¶

A UNIQUE constraint ensures that all values in a column are different. In the
`truck` table, you defined the `truck_email` column as NOT NULL and UNIQUE.

Given the UNIQUE constraint, if you attempt to insert two records with the
same email address, the statement will fail. To test this behavior, run the
following commands.

Start by selecting an existing email address and setting a variable
`truck_email` to that string. Then select the maximum value of `truck_id` from
the table and set another variable `max_truck_id` to that value. Next, set a
third variable, `new_truck_id` that increments `max_truck_id` by 1. This
process ensures that you do not run into a “Primary key already exists” error
when you insert a new row.

Finally, insert the new row.

    
    
    SET truck_email = (SELECT truck_email FROM truck LIMIT 1);
    SET max_truck_id = (SELECT MAX(truck_id) FROM truck);
    SET new_truck_id = $max_truck_id+1;
    INSERT INTO truck VALUES
      ($new_truck_id,2,'Stockholm','Stockholm län','Stockholm','Sweden','SE',1,2001,'Freightliner','MT45 Utilimaster',0,276,'2020-10-01',$truck_email,CURRENT_TIMESTAMP());
    

Copy

The INSERT statement fails and you receive the following error message:

    
    
    Duplicate key value violates unique constraint SYS_INDEX_TRUCK_UNIQUE_TRUCK_EMAIL
    

Now create a new unique email address and insert a new record into the `truck`
table:

    
    
    SET new_unique_email = CONCAT($new_truck_id, '_truck@email.com');
    INSERT INTO truck VALUES ($new_truck_id,2,'Stockholm','Stockholm län','Stockholm','Sweden','SE',1,2001,'Freightliner','MT45 Utilimaster',0,276,'2020-10-01',$new_unique_email,CURRENT_TIMESTAMP());
    

Copy

The INSERT statement should run successfully this time.

### Step 4.2. Test a FOREIGN KEY constraint¶

In this step you will test a FOREIGN KEY constraint.

First, show the DDL that you used to create the `order_header` table by
executing the [GET_DDL](../../sql-reference/functions/get_ddl) function. Note
the FOREIGN KEY constraint for the `truck_id` column in the output.

    
    
    SELECT GET_DDL('table', 'order_header');
    

Copy

The output of this command looks similar to the following partial result:

![Output of get_ddl on order_header
table](../../_images/select_getddl_order_header.png)

Now try to insert a new record into the `order_header` table, using a non-
existent truck ID.

    
    
    SET max_order_id = (SELECT MAX(order_id) FROM order_header);
    SET new_order_id = ($max_order_id +1);
    SET no_such_truck_id = -1;
    INSERT INTO order_header VALUES
      ($new_order_id,$no_such_truck_id,6090,0,0,0,'16:00:00','23:00:00','','2022-02-18 21:38:46.000','','USD',17.0000,'','',17.0000,'');
    

Copy

The INSERT statement should fail because it violates the FOREIGN KEY
constraint on the `truck` table. You should receive the following error
message:

    
    
    Foreign key constraint SYS_INDEX_ORDER_HEADER_FOREIGN_KEY_TRUCK_ID_TRUCK_TRUCK_ID was violated.
    

Now use the new `new_truck_id` variable that you used earlier and insert a new
record into the `order_header` table:

    
    
    INSERT INTO order_header VALUES
      ($new_order_id,$new_truck_id,6090,0,0,0,'16:00:00','23:00:00','','2022-02-18 21:38:46.000','','USD',17.0000,'','',17.0000,'');
    

Copy

The INSERT statement should run successfully this time.

### Step 4.3. Attempt to truncate a table referenced by a FOREIGN KEY
constraint¶

Next, you can verify that a table referenced by a FOREIGN KEY constraint
cannot be truncated as long as the foreign-key relationship exists. Run the
following [TRUNCATE TABLE](../../sql-reference/sql/truncate-table) statement:

    
    
    TRUNCATE TABLE truck;
    

Copy

The statement should fail, and you should receive the following error message:

    
    
    91458 (0A000): Hybrid table 'TRUCK' cannot be truncated as it is involved in active foreign key constraints.
    

### Step 4.4. Delete a row referenced by a FOREIGN KEY constraint¶

Next, you can verify that a record referenced by a FOREIGN KEY constraint
cannot be deleted as long as the foreign-key relationship exists. Run the
following [DELETE](../../sql-reference/sql/delete) statement.

    
    
    DELETE FROM truck WHERE truck_id = $new_truck_id;
    

Copy

The statement should fail, and you should receive the following error message:

    
    
    Foreign keys that reference key values still exist.
    

To delete a record referenced by a FOREIGN KEY constraint, you must first
delete the corresponding record from the `order_header` table. Then you can
delete the referenced record from the `truck` table. Run the following DELETE
statements:

    
    
    DELETE FROM order_header WHERE order_id = $new_order_id;
    DELETE FROM truck WHERE truck_id = $new_truck_id;
    

Copy

Both statements should run successfully.

## Step 5. Use row-level locking to run concurrent updates¶

Unlike standard tables, which use partition or table-level locking, hybrid
tables employ [row-level locking](../../sql-reference/transactions.html#label-
txn-locking) for update operations. Row-level locking allows concurrent
updates on independent records so that transactions don’t wait on full table
locks. For applications that rely on heavy transactional workloads, wait times
for locks must be kept to a minimum, allowing concurrent operations to access
the same table very frequently.

In this step, you can test concurrent updates to different records in the
`order_header` hybrid table.

You will use the main `Hybrid Tables - QuickStart` worksheet that you created
earlier, and you will create a new worksheet named `Hybrid Tables - QuickStart
Session 2` to simulate a new session. From the `Hybrid Tables - QuickStart`
worksheet, you will start a new transaction by using the [BEGIN](../../sql-
reference/sql/begin) statement, then run an UPDATE statement (a DML
operation). Before running the [COMMIT](../../sql-reference/sql/commit)
transaction statement, you will open the `Hybrid Tables - QuickStart Session
2` worksheet and run another UPDATE statement. Finally, you will commit the
open transaction.

### Step 5.1. Create a new worksheet¶

Under Worksheets, click the + button in the top-right corner of Snowsight,
then select SQL Worksheet.

Rename the worksheet by selecting its auto-generated timestamp name and typing
`Hybrid Tables - QuickStart Session 2`. This new worksheet will only be used
in the current step.

### Step 5.2. Run concurrent updates¶

First, open the `Hybrid Tables - QuickStart` worksheet. Make sure you are
using the right role, warehouse, database, and schema, then set and select the
`max_order_id` variable.

    
    
    USE ROLE hybrid_quickstart_role;
    USE WAREHOUSE hybrid_quickstart_wh;
    USE DATABASE hybrid_quickstart_db;
    USE SCHEMA data;
    
    SET max_order_id = (SELECT MAX(order_id) FROM order_header);
    SELECT $max_order_id;
    

Copy

Note the value of the `max_order_id` variable.

Start a new transaction and run the first UPDATE statement.

    
    
    BEGIN;
    UPDATE order_header
      SET order_status = 'COMPLETED'
      WHERE order_id = $max_order_id;
    

Copy

Note that you did not commit the transaction, so now there is an open lock on
the row that matches this condition:

    
    
    WHERE order_id = $max_order_id
    

Copy

Run the [SHOW TRANSACTIONS](../../sql-reference/sql/show-transactions)
command, which should return a single open transaction.

    
    
    SHOW TRANSACTIONS;
    

Copy

The output of this command looks similar to the following partial result:

![Output of SHOW TRANSACTIONS command, showing one open
transaction](../../_images/show_one_open_transaction.png)

Open the `Hybrid Tables - QuickStart Session 2` worksheet. Make sure you are
using the right role, warehouse, database, and schema, then set and select the
`min_order_id` variable.

    
    
    USE ROLE hybrid_quickstart_role;
    USE WAREHOUSE hybrid_quickstart_wh;
    USE DATABASE hybrid_quickstart_db;
    USE SCHEMA data;
    

Copy

    
    
    SET min_order_id = (SELECT MIN(order_id) FROM order_header);
    SELECT $min_order_id;
    

Copy

Note that the `min_order_id` value is different from the `max_order_id` value
that you used in the first UPDATE statement. Run the second UPDATE statement.

    
    
    UPDATE order_header
      SET order_status = 'COMPLETED'
      WHERE order_id = $min_order_id;
    

Copy

Because hybrid tables use row-level locking and the open transaction locks the
row `WHERE order_id = $MAX_ORDER_ID`, the UPDATE statement runs successfully.

Open the `Hybrid Tables - QuickStart` worksheet and commit the open
transaction.

    
    
    COMMIT;
    

Copy

Run the following query to view the updated records:

    
    
    SELECT * FROM order_header WHERE order_status = 'COMPLETED';
    

Copy

The output of this command looks similar to the following partial result:

![SELECT result from order_header table where order_status is
completed](../../_images/select_order_header_where_completed.png)

## Step 6. Demonstrate consistency¶

In this step, you will learn about a unique hybrid tables feature: the ability
to run multi-statement operations natively, easily, and effectively in one
consistent atomic transaction, with access to both hybrid tables and standard
tables. Snowflake [transactions](../../sql-reference/transactions) guarantee
the “ACID” properties of atomicity, consistency, isolation, and durability.
Any given transaction is treated as an atomic unit; preserves a consistent
database state when writes occur; is isolated from other concurrent
transactions (as if they were being run sequentially); and is committed
durably (remains committed, once committed).

In this example, the company acquires a new truck of the same model as an
existing truck. Consequently, you must update the `year` column for the
relevant record in the `truck` hybrid table to reflect the change. After this
update, you need to promptly update a row and insert a new row in the
`truck_history` table. This standard table will track and preserve all the
changes to the truck fleet over time. You complete all of these steps as part
of one explicitly committed transaction.

### Step 6.1. Run a single transaction that contains multiple DML statements¶

Open the original `Hybrid Tables - QuickStart` worksheet.

Start a new transaction to ensure that a subsequent series of operations is
treated as a single, atomic unit. Then execute multiple DML statements:

  * Update the relevant truck record in the `truck` hybrid table.

  * Update the corresponding record in the `truck_history` table by setting the `record_end_time` to mark the end of its validity.

  * Insert a new record in the `truck_history` table, capturing the updated information.

Finally, commit the transaction.

    
    
    BEGIN;
    SET CURRENT_TIMESTAMP = CURRENT_TIMESTAMP();
    UPDATE truck SET year = '2024', record_start_time=$CURRENT_TIMESTAMP WHERE truck_id = 1;
    UPDATE truck_history SET record_end_time=$CURRENT_TIMESTAMP WHERE truck_id = 1 AND record_end_time IS NULL;
    INSERT INTO truck_history SELECT *, NULL AS record_end_time FROM truck WHERE truck_id = 1;
    COMMIT;
    

Copy

### Step 6.2. Check the results¶

Now run the following SELECT queries to review the results of the UPDATE and
INSERT statements.

The first query should return two rows, and the second query should return
one.

    
    
    SELECT * FROM truck_history WHERE truck_id = 1;
    

Copy

The output of this command looks similar to the following partial result:

![Output of truck_history query that returns two
rows](../../_images/select_where_truck_history_id.png)

    
    
    SELECT * FROM truck WHERE truck_id = 1;
    

Copy

The output of this command looks similar to the following partial result:

![Output of truck query that returns one
row](../../_images/select_where_truck_id.png)

## Step 7. Join a hybrid table to a standard table¶

In this step, you run a [join](../../sql-reference/constructs/join) query that
combines data from a hybrid table (`order_header`) and a standard table
(`truck_history`). This query demonstrates the interoperability of the two
table types.

### Step 7.1. Explore the data in the tables¶

Earlier you created and loaded the `order_header` table. Now you can run a few
queries and review some information to get familiar with the table. First,
list the tables in the database with the SHOW TABLES command, then select two
columns from the output of that list.

    
    
    SHOW TABLES IN DATABASE hybrid_quickstart_db;
    SELECT "name", "is_hybrid" FROM TABLE(RESULT_SCAN(last_query_id()));
    

Copy

The output of this command looks similar to the following partial result:

![Query that shows whether tables are
hybrid](../../_images/show_tables_is_hybrid.png)

Now run two simple queries:

    
    
    SELECT * FROM truck_history LIMIT 10;
    SELECT * FROM order_header LIMIT 10;
    

Copy

The output of the second query looks similar to the following partial result:

![Query that returns 10 rows from the order_header
table](../../_images/select_from_order_header_limit.png)

### Step 7.2. Join a hybrid table to a standard table¶

To join the `order_header` hybrid table to the `truck_history` standard table,
run the following SET statement and query. Joining hybrid tables to standard
tables does not require any special syntax.

    
    
    SET order_id = (SELECT order_id FROM order_header LIMIT 1);
    
    SELECT hy.*,st.*
      FROM order_header AS hy JOIN truck_history AS st ON hy.truck_id = st.truck_id
      WHERE hy.order_id = $order_id
        AND st.record_end_time IS NULL;
    

Copy

The join result looks similar to the following partial result:

![Query that returns the results of a join between a hybrid table and a
standard table](../../_images/hybrid_table_join_query.png)

## Step 8. Demonstrate security and governance¶

In this step, you will run two security-related examples to demonstrate that
Snowflake [security and governance](../ecosystem-security) functionality
applies equally to standard tables and hybrid tables.

Roles and grants of privileges to those roles are standard mechanisms for
enforcing security when large numbers of database users have access to the
same system, whether the workload is transactional, analytic, or hybrid.

### Step 8.1. Set up hybrid table access control and user management¶

[Role-based access control (RBAC)](../security-access-control-overview) works
the same for hybrid tables and standard tables. You can manage access to
hybrid table data in Snowflake by granting privileges to some roles.

First, create a new `hybrid_quickstart_bi_user_role` role. Use the
ACCOUNTADMIN role to create the new role.

    
    
    USE ROLE ACCOUNTADMIN;
    CREATE ROLE hybrid_quickstart_bi_user_role;
    SET my_user = CURRENT_USER();
    GRANT ROLE hybrid_quickstart_bi_user_role TO USER IDENTIFIER($my_user);
    

Copy

Now you can grant USAGE privileges for the `hybrid_quickstart_wh` warehouse,
`hybrid_quickstart_db` database, and all of its schemas to the new role. Use
`hybrid_quickstart_role` to run the GRANT statements.

    
    
    USE ROLE hybrid_quickstart_role;
    GRANT USAGE ON WAREHOUSE hybrid_quickstart_wh TO ROLE hybrid_quickstart_bi_user_role;
    GRANT USAGE ON DATABASE hybrid_quickstart_db TO ROLE hybrid_quickstart_bi_user_role;
    GRANT USAGE ON ALL SCHEMAS IN DATABASE hybrid_quickstart_db TO hybrid_quickstart_bi_user_role;
    

Copy

Using the new role (`hybrid_quickstart_bi_user_role`), try to select some data
from the `order_header` table.

    
    
    USE ROLE hybrid_quickstart_bi_user_role;
    USE DATABASE hybrid_quickstart_db;
    USE SCHEMA data;
    
    SELECT * FROM order_header LIMIT 10;
    

Copy

You cannot select any data because the role `hybrid_quickstart_bi_user_role`
has not been granted the necessary SELECT privilege on the tables. You receive
the following error message:

    
    
    Object 'ORDER_HEADER' does not exist or not authorized.
    

To solve this problem, use the role `hybrid_quickstart_role` to grant SELECT
privileges on all the tables in the `data` schema to
`hybrid_quickstart_bi_user_role`.

    
    
    USE ROLE hybrid_quickstart_role;
    GRANT SELECT ON ALL TABLES IN SCHEMA DATA TO ROLE hybrid_quickstart_bi_user_role;
    

Copy

Try again to select data from the `order_header` hybrid table.

    
    
    USE ROLE hybrid_quickstart_bi_user_role;
    SELECT * FROM order_header LIMIT 10;
    

Copy

This time the query succeeds because HYBRID_QUICKSTART_BI_USER_ROLE has the
appropriate privileges at all levels of the hierarchy. The output looks
similar to the following partial result:

![Query that now allows access to order_header after SELECT is granted on the
DATA schema](../../_images/query_succeeds_after_grant_select_on_schema.png)

### Step 8.2. Create and implement a masking policy¶

In this step, you create a [masking policy](../security-column-intro) and
apply it to the `truck_email` column in the `truck` hybrid table by using an
ALTER TABLE … ALTER COLUMN statement. A masking policy is a standard way of
controlling the column-level visibility of data to users with different roles
and privileges.

Note

To create masking policies, you must use an Enterprise Edition account (or a
higher-level account). If you are using a Standard Edition account, skip this
step. For more information, see [Snowflake Editions](../intro-editions).

Use the `hybrid_quickstart_role` role, then create the new masking policy,
which is intended to mask entire column values from unauthorized roles.

    
    
    USE ROLE hybrid_quickstart_role;
    
    CREATE MASKING POLICY hide_column_values AS
      (col_value VARCHAR) RETURNS VARCHAR ->
        CASE WHEN CURRENT_ROLE() IN ('HYBRID_QUICKSTART_ROLE') THEN col_value
          ELSE '***MASKED***'
          END;
    

Copy

Now apply this policy to the hybrid table.

    
    
    ALTER TABLE truck MODIFY COLUMN truck_email
      SET MASKING POLICY hide_column_values USING (truck_email);
    

Copy

Because you are currently using the `hybrid_quickstart_role`, the
`truck_email` column should _not_ be masked. Run the following query:

    
    
    SELECT * FROM truck LIMIT 10;
    

Copy

![Query that does not mask the truck_email
column](../../_images/truck_email_column_not_masked.png)

Switch to `HYBRID_QUICKSTART_BI_USER_ROLE` and run the query again. The
`TRUCK_EMAIL` column should be masked now.

    
    
    USE ROLE hybrid_quickstart_bi_user_role;
    SELECT * FROM truck LIMIT 10;
    

Copy

![Query that masks the truck_email
column](../../_images/truck_email_column_masked.png)

## Step 9. Cleanup, conclusion, and further reading¶

### Cleanup¶

To clean up your Snowflake environment, run the following SQL statements:

    
    
    USE ROLE hybrid_quickstart_role;
    USE WAREHOUSE hybrid_quickstart_wh;
    USE DATABASE hybrid_quickstart_db;
    USE SCHEMA data;
    

Copy

    
    
    DROP DATABASE hybrid_quickstart_db;
    DROP WAREHOUSE hybrid_quickstart_wh;
    USE ROLE ACCOUNTADMIN;
    DROP ROLE hybrid_quickstart_role;
    DROP ROLE hybrid_quickstart_bi_user_role;
    

Copy

Finally, manually delete the `Hybrid Tables - QuickStart` and `Hybrid Tables -
QuickStart Session 2` worksheets.

### What you learned¶

In this tutorial, you learned how to:

  * Create and bulk load hybrid tables.

  * Create and check the enforcement of UNIQUE, PRIMARY KEY, and FOREIGN KEY constraints.

  * Run concurrent updates that depend on row-level locks.

  * Run a multi-statement operation in a consistent atomic transaction (across hybrid and standard tables).

  * Query hybrid tables and join them to standard tables.

  * Verify that security and governance principles apply to both hybrid and standard tables.

### Related resources¶

  * [Snowflake Unistore Landing Page](https://www.snowflake.com/en/data-cloud/workloads/unistore/)

  * [Snowflake Documentation for Hybrid Tables](https://docs.snowflake.com/en/user-guide/tables-hybrid)

  * [Blog: Simplify Application Development with Hybrid Tables](https://www.snowflake.com/blog/simplify-application-development-hybrid-tables)

