# Cloning considerations¶

This topic provides important considerations when cloning objects in
Snowflake, particularly databases, schemas, and non-temporary tables. Factors
such as DDL and DML transactions (on the source object), Time Travel, and data
retention periods can affect the object clone.

## Access control privileges for cloned objects¶

If the source object is a database or schema, the clone inherits all granted
privileges on the clones of all child objects contained in the source object:

  * For databases, contained objects include schemas, tables, views, etc.

  * For schemas, contained objects include tables, views, etc.

Note that the clone of the container itself (database or schema) does not
inherit the privileges granted on the source container.

[CREATE <object> … CLONE](../sql-reference/sql/create-clone) statements for
most objects do not copy grants on the source object to the object clone.
However, [CREATE <object>](../sql-reference/sql/create) commands that support
the COPY GRANTS clause (e.g. CREATE TABLE, CREATE VIEW) enable you to
optionally copy grants to object clones. For example, the [CREATE
TABLE](../sql-reference/sql/create-table) … CLONE command syntax supports the
COPY GRANTS parameter. When the COPY GRANTS parameter is specified in a CREATE
TABLE statement, the create operation copies all privileges, except OWNERSHIP,
from the source table to the new table. The same behavior is true for other
CREATE commands that support the COPY GRANTS clause.

In all other cases, you must grant any required privileges to the newly-
created clone (using [GRANT <privileges>](../sql-reference/sql/grant-
privilege)).

## Cloning and Snowflake objects¶

This section describes special cloning considerations with regard to specific
Snowflake objects.

### Cloning and managed access schemas¶

If you clone a schema and specify the WITH MANAGED ACCESS clause, the required
privileges depends on whether the source schema is a managed or unmanaged
schema. For details, see [CREATE SCHEMA privileges](../sql-
reference/sql/create-schema.html#label-create-schema-ac).

### Cloning and object parameters¶

Cloned objects inherit any object parameters that were set on the source
object when that object was cloned. If an object parameter can be set on
object containers (i.e. account, database, schema) and is not explicitly set
on the source object, an object clone inherits the default parameter value or
the value overridden at the lowest level. For more information about object
parameters, see [Parameters](../sql-reference/parameters).

### Cloning and default sequences¶

In a table, a column can reference a [sequence](querying-sequences) that
generates default values. When a table is cloned, the cloned table references
the source or cloned sequence:

  * If the database or schema containing both the table and sequence is cloned, the cloned table references the cloned sequence.

  * Otherwise, the cloned table references the source sequence.

For example, if the sequence is defined in a different database or schema, the
cloned table references the source sequence. Or if you clone just the table
itself, the cloned table references the source sequence.

If you do not want the new table to continue using the source sequence, run
the following command:

    
        ALTER TABLE <table_name> ALTER COLUMN <column_name> SET DEFAULT <new_sequence>.nextval;
    

Copy

### Cloning and foreign key constraints¶

A table can have a foreign key constraint that references a table that
includes the primary key. When a table with a foreign key constraint is
cloned, the cloned table references the source or cloned table that includes
the primary key:

  * If the database or schema containing both tables is cloned, the cloned table with the foreign key references the primary key in the other cloned table.

  * If the tables are in separate databases or schemas, the cloned table references the primary key in the source table.

### Cloning and clustering keys¶

A table can have a subset of columns designated as a [clustering key](tables-
clustering-keys) to co-locate similar rows in the same micro-partition. When a
table with a clustering key is cloned, the new table is created with a
clustering key. By default, [Automatic Clustering](tables-auto-reclustering)
is suspended for the new table. To resume automatic clustering for the new
table, run the following command:

    
    
    ALTER TABLE <name> RESUME RECLUSTER
    

Copy

### Cloning and stages¶

Individual external named stages can be cloned. An external stage references a
bucket or container in external cloud storage; cloning an external stage has
no impact on the referenced cloud storage.

Internal (i.e. Snowflake) named stages cannot be cloned.

When cloning a database or schema:

  * External named stages that were present in the source when the cloning operation started are cloned.

  * Tables are cloned, which means the internal stage associated with each table is also cloned. Any data files that were present in a table stage in the source database or schema are not copied to the clone (i.e. the cloned table stages are empty).

  * Internal named stages are not cloned.

### Cloning and Apache Iceberg™ tables¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Preview Feature](../release-
notes/preview-features) — Open

Available to all accounts.

#### Storage¶

Storage for cloned Iceberg tables works the same as storage for other cloned
Snowflake objects; clones share the same underlying storage as the source
table.

For information about how storage works for cloned objects, see [Cloned table,
schema, and database storage](tables-storage-considerations.html#label-
cloning-tables).

For information about Iceberg table storage, see [Storage for Apache Iceberg™
tables](tables-iceberg-storage).

#### Data manipulation language (DML) commands¶

You can use DML commands on cloned Iceberg tables just as you do on regular
Snowflake-managed tables. For instructions and examples, see [Use DML commands
with Snowflake-managed tables](tables-iceberg-manage.html#label-tables-
iceberg-manage-dml).

For DML operations on cloned tables, Snowflake generates new data files and
stores them in the base location of the source table. The diverging data files
don’t affect the source table; DML operations on the source table are
reflected only in the source table’s data files.

#### Iceberg metadata¶

For cloned tables, Snowflake generates Iceberg metadata files that are
distinct from those of the source table. For example, a cloned Iceberg table
has its own `metadata.json` file with a unique `table-uuid`, `last-sequence-
number`, and other properties. Cloned table snapshots don’t include any
snapshot information from the source table.

### Cloning and event tables¶

When cloning an event table, you can clone to and from only event tables. In
other words, you can not clone from a regular table to an event table, nor
from an event table to a regular table.

### Cloning and pipes¶

When a database or schema is cloned, any pipes in the source container that
reference an internal (i.e. Snowflake) stage are not cloned.

However, any pipes that reference an external stage are cloned. This includes
any pipe objects where the INTEGRATION parameter is set. This parameter points
to a notification integration to enable auto-ingest Snowpipe when loading data
from files in Google Cloud Storage or Microsoft Azure blob storage.

When a data file is created in a stage location (e.g. blob storage container),
a copy of the notification is sent to every pipe that matches the stage
location. This results in the following behavior:

>   * If a table is fully qualified in the COPY statement in the pipe
> definition (in the form of `_db_name_._schema_name_._table_name_` or
> `_schema_name_._table_name_`), then Snowpipe loads duplicate data into the
> source table (i.e. the `_database_._schema_._table_` in the COPY statement)
> for each pipe.
>
>   * If a table is not fully qualified in the pipe definition, then Snowpipe
> loads the data into the table (e.g. `mytable`) in the source and cloned
> databases/schemas.
>
>

The default state of a pipe clone is as follows:

>   * When `AUTO_INGEST = FALSE`, a cloned pipe is paused by default.
>
>   * When `AUTO_INGEST = TRUE`, a cloned pipe is set to the `STOPPED_CLONED`
> state. In this state, pipes do not accumulate event notifications as a
> result of newly staged files. When a pipe is explicitly resumed, it only
> processes data files triggered as a result of new event notifications.
>
>

A pipe clone in either state can be resumed by executing an [ALTER
PIPE](../sql-reference/sql/alter-pipe) … RESUME statement.

### Cloning and search optimization¶

You can clone tables that have the [Search Optimization Service](search-
optimization-service) enabled. When you do, the corresponding search access
path is a [zero-copy clone](tables-storage-considerations.html#label-cloning-
tables). However, if the cloned search access path isn’t up-to-date, it might
incur maintenance costs, even if the cloned table doesn’t change, because the
search access path must catch up with the current state of the cloned table.
For more information about cloning and search optimization, see [Cloning the
table, schema, or database](search-optimization/working-with-
tables.html#label-search-optimization-and-cloning).

### Cloning and streams¶

Currently, when a database or schema that contains source tables and streams
is cloned, any unconsumed records in the streams (in the clone) are
inaccessible. This behavior is consistent with [Time Travel](data-time-travel)
for tables. If a table is cloned, historical data for the table clone begins
at the time/point when the clone was created.

### Cloning and tasks¶

When a database or schema that contains tasks is cloned, the tasks in the
clone are suspended by default. The tasks can be resumed individually (using
[ALTER TASK](../sql-reference/sql/alter-task) … RESUME).

### Cloning and alerts¶

When a database or schema that contains alerts is cloned, the alerts in the
clone are [suspended](alerts.html#label-alerts-suspend-resume) by default.

To resume a suspended alert, you can use the [ALTER ALERT](../sql-
reference/sql/alter-alert) … RESUME command.

### Cloning and governance objects¶

Masking & row access policies:

> The following approach helps to safeguard data from users with the SELECT
> privilege on the table or view when accessing a cloned object:
>
>   * Cloning an individual policy object is not supported.
>
>   * Cloning a schema results in the cloning of all policies within the
> schema.
>
>   * A cloned table maps to the same policies as the source table. In other
> words, if a policy is set on the base table or its columns, the policy is
> attached to the cloned table or its columns.
>
>     * If a table or view exists in the source schema/database and has
> references to policies in the same schema/database, the cloned table or view
> is mapped to the corresponding cloned policy (in the target schema/database)
> instead of the policy in the source schema/database.
>
>     * If the source table refers to a policy in a different schema (i.e. a
> foreign reference), then the cloned table retains the foreign reference.
>
>

>
> For more information, see [CREATE <object> … CLONE](../sql-
> reference/sql/create-clone).
>
> Also see:
>
>   * Cloning external tables and [masking policies](security-column-
> intro.html#label-security-column-intro-ext-table).
>
>   * Cloning external tables and [row access policies](security-row-
> intro.html#label-security-row-intro-ext-table).
>
>

Tags:

>   * Tag associations in the source object (e.g. table) are maintained in the
> cloned objects.
>
>   * For a database or a schema:
>
> The tags stored in that database or schema are also cloned.
>
> When a database or schema is cloned, tags that reside in that schema or
> database are also cloned.
>
> If a table or view exists in the source schema/database and has references
> to tags in the same schema or database, the cloned table or view is mapped
> to the corresponding cloned tag (in the target schema/database) instead of
> the tag in the source schema or database.
>
>

Tag-based masking policies:

> For a tag-based masking policy where the tag is stored in a different schema
> than the masking policy and table, cloning the schema containing the masking
> policy and table results in the cloned table being protected by the masking
> policy in the source schema not the cloned schema.
>
> However, for a tag-based masking policy where the tag, masking policy, and
> table all exist in the schema, cloning the schema results in the table being
> protected by the masking policy in the cloned schema, not the source schema.
>
> If the table is cloned or moved to a different schema or database and was
> originally protected by a tag-based masking policy set on the schema or
> database, the table is not protected by the tag-based masking policy set on
> the source schema or database. The table is protected by the tag-based
> masking policy set on the target schema or database, if there is a tag-based
> masking policy set on the target schema or database.

### Cloning and differential privacy¶

Cloning a table or view that is protected by [differential privacy](diff-
privacy/differential-privacy-overview) results in the following behavior.

#### Privacy policies¶

When you clone a privacy-protected table or view, the object is also privacy-
protected. Whether the privacy policy is cloned depends on what you are
cloning:

  * If you clone the privacy-protected table only, the privacy policy is not cloned.

  * If you clone a schema that contains both the table and the privacy policy, the privacy policy is cloned.

  * If you clone a database that contains a schema that contains both the table and the privacy policy, the privacy policy is cloned.

If the privacy policy and the table are in different schemas, cloning the
database or schema of the table does not clone the privacy policy. In this
case, the privacy policy is automatically associated with the cloned objects.

#### Privacy domains¶

When you clone a privacy-protected table or view, the privacy domains set on
the columns are also cloned.

Keep the following in mind when cloning a privacy-protected table or view with
a REFERENCE privacy domain:

  * If you clone a privacy-protected table but not the referenced table, the new table continues to reference the same table.

  * If you clone both the privacy-protected table and the referenced table, the new privacy-protected table references the new cloned version of the referenced table.

  * If the REFERENCE privacy domain references itself, the newly cloned table references itself, not the original table.

### Cloning and database roles¶

You can clone a database role using the CREATE DATABASE ROLE … CLONE command
if the database role does not already exist in the target database. For
details, see [CREATE <object> … CLONE](../sql-reference/sql/create-clone).

### Cloning and Java UDFs¶

A Java UDF can be cloned when the database or schema containing the Java UDF
is cloned. To be cloned, the Java UDF must meet certain conditions. For more
information, see [Limitations on cloning](../developer-guide/udf/java/udf-
java-limitations.html#label-limitations-on-cloning-java-udfs).

### Cloning and instances of Snowflake classes¶

An instance of the [CUSTOM_CLASSIFIER](../sql-
reference/classes/custom_classifier) is cloned when the schema that contains
the instance is cloned. Cloning of instances of other Snowflake
[classes](../sql-reference-classes.html#label-available-classes) is _not_
supported.

## Impact of DDL on cloning¶

Cloning is fast, but not instantaneous, particularly for large objects (e.g.
tables). As such, if DDL statements are executed on source objects (e.g.
renaming tables in a schema) while the cloning operation is in progress, the
changes may not be represented in the clone. This is because DDL statements
are atomic and not part of multi-statement transactions.

Furthermore, Snowflake does not record which object names were present when
the cloning operation started and which names changed. As such, DDL statements
that rename (or drop and recreate) source child objects compete with any in-
progress cloning operations and can cause name conflicts.

In the following example, the `t_sales` table is dropped and another table is
altered and given the same name as the dropped table while the parent database
is being cloned, producing an error:

>
>     CREATE OR REPLACE DATABASE staging_sales CLONE sales;
>  
>     DROP TABLE sales.public.t_sales;
>  
>     ALTER TABLE sales.public.t_sales_20170522 RENAME TO
> sales.public.t_sales;
>  
>
> Copy
>  
>  
>     002002 (42710): None: SQL compilation error: Object 'T_SALES' already
> exists.
>  

Tip

To avoid conflicts in name resolution during a cloning operation, we suggest
refraining from renaming objects to a name previously used by a dropped object
until cloning is completed.

## Impact of DML and data retention on cloning¶

The [data retention period](data-time-travel.html#label-data-retention-
specifying) specifies the number of days for which Snowflake retains
historical data for performing Time Travel actions on an object. Because the
data retained for Time Travel incurs storage costs at the table-level, some
users set this parameter to `0` for some tables, effectively disabling data
retention for these tables (i.e. when the value is set to `0`, Time Travel
data retained for DML transactions is purged, incurring negligible additional
storage costs).

Cloning operations require time to complete, particularly for large tables.
During this period, DML transactions can alter the data in a source table.
Subsequently, Snowflake attempts to clone the table data as it existed when
the operation began. However, if data is purged for DML transactions that
occur during cloning (because the retention time for the table is `0`), the
data is unavailable to complete the operation, producing an error similar to
the following:

>
>     ProgrammingError occurred: "000707 (02000): None: Data is not
> available." with query id None
>  

Tip

As a workaround, we recommend either of the following best practices when
cloning an object:

  * Refrain, if possible, from executing DML transactions on the source object (or any of its children) until after the cloning operation completes.

  * If this is not possible, prior to starting cloning, set `DATA_RETENTION_TIME_IN_DAYS=1` for all tables in the schema (or database if you are cloning an entire database). Once the operation completes, remember to reset the parameter value back to `0` for those tables in the source, if desired.

You might also want to set the value to `0` for the cloned tables (if you plan
to make DML changes to the cloned tables and do not wish to incur additional
storage costs for Time Travel on the tables).

## Cloning using Time Travel (databases, schemas, tables, dynamic tables,
event tables, and streams only)¶

This section provides information to consider when using [Time Travel](data-
time-travel) to clone objects at a specific time/point in the past.

### Cloning of historical objects¶

If the source object did not exist at the time/point set in the [AT | BEFORE](../sql-reference/constructs/at-before) clause, an error is returned.

In the following example, a CREATE TABLE … CLONE statement attempts to clone
the source table at a point in the past (30 minutes prior) when it didn’t
exist:

>
>     CREATE TABLE t_sales (numeric integer) data_retention_time_in_days=1;
>  
>     CREATE OR REPLACE TABLE sales.public.t_sales_20170522 CLONE
> sales.public.t_sales at(offset => -60*30);
>  
>
> Copy
>  
>  
>     002003 (02000): SQL compilation error:
>     Object 'SALES.PUBLIC.T_SALES' does not exist.
>  

Any child object in a cloned database or schema that did not exist at the
specified time/point is not cloned.

The cloning operation fails in the following scenarios:

>   * If the specified Time Travel time is beyond the retention time of any
> current child of the cloned database or schema.
>
> As a workaround for child objects that have been purged from Time Travel,
> use the [IGNORE TABLES WITH INSUFFICIENT DATA RETENTION](../sql-
> reference/sql/create-clone.html#label-ignore-tables-with-insufficient-data-
> retention) parameter of the CREATE <object> … CLONE command. For more
> information, see Child objects and data retention time.
>
>   * If a pipe object with `AUTO-INGEST = TRUE` set was recreated (using the CREATE OR REPLACE PIPE syntax) or dropped since the point in time specified in the AT | BEFORE clause. This limitation does not apply to pipe objects created for manual Snowpipe ingest using the REST API (i.e. with `AUTO-INGEST = FALSE`).
>
>

#### Child objects and data retention time¶

If a child object (for example, a table) has a shorter [data retention
period](data-time-travel.html#label-time-travel-data-retention-period) than
the data retention period for its parent object (for example, a database or
schema), the child object’s historical data is moved out of Time Travel before
the historical data of its parent object is moved out of Time Travel.

For example, the [data retention period](data-time-travel.html#label-data-
retention-specifying) for database `db1` is seven days and the data retention
period for table `t1` in `db1` is one day. If you clone `db1` using Time
Travel at a point 12 hours in the past, the cloning operation successfully
creates a clone of `db1` and it contains the cloned table `t1`.

However, if you try to clone `db1` at a point two days in the past, the
historical data for table `t1` at that point is no longer available in Time
Travel and the cloning operation fails.

As a workaround, use the [IGNORE TABLES WITH INSUFFICIENT DATA
RETENTION](../sql-reference/sql/create-clone.html#label-ignore-tables-with-
insufficient-data-retention) parameter of the [CREATE <object> …
CLONE](../sql-reference/sql/create-clone) command to clone a database or
schema. The parameter skips tables that no longer have historical data
available in Time Travel at the time specified for the cloning operation.

### Cloning of historical object metadata¶

An object clone inherits the name and structure of the source object current
at the time the [CREATE <object> … CLONE](../sql-reference/sql/create-clone)
statement is executed or at a specified time/point in the past using [Time
Travel](data-time-travel). An object clone inherits any other metadata, such
as comments or table clustering keys, that is current in the source object at
the time the statement is executed, regardless of whether Time Travel is used.

Note

To ensure consistent behavior in long cloning operations, when an AT or BEFORE
clause is not specified for a CREATE _< object>_ … CLONE statement, the
cloning operation internally sets the AT clause value as the timestamp when
the statement was initiated.

## Cloning and replication¶

For more information, see [Replication and cloning](account-replication-
considerations.html#label-replication-and-cloning).

