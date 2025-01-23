# Overview of Views¶

This topic covers concepts for understanding and using views.

## What is a View?¶

A view allows the result of a query to be accessed as if it were a table. The
query is specified in the CREATE VIEW statement.

Views serve a variety of purposes, including combining, segregating, and
protecting data. For example, you can create separate views that meet the
needs of different types of employees, such as doctors and accountants at a
hospital:

>
>     CREATE TABLE hospital_table (patient_id INTEGER,
>                                  patient_name VARCHAR,
>                                  billing_address VARCHAR,
>                                  diagnosis VARCHAR,
>                                  treatment VARCHAR,
>                                  cost NUMBER(10,2));
>     INSERT INTO hospital_table
>             (patient_ID, patient_name, billing_address, diagnosis,
> treatment, cost)
>         VALUES
>             (1, 'Mark Knopfler', '1982 Telegraph Road', 'Industrial
> Disease',
>                 'a week of peace and quiet', 2000.00),
>             (2, 'Guido van Rossum', '37 Florida St.', 'python bite', 'anti-
> venom',
>                 70000.00)
>             ;
>  
>
> Copy
>  
>  
>     CREATE VIEW doctor_view AS
>         SELECT patient_ID, patient_name, diagnosis, treatment FROM
> hospital_table;
>  
>     CREATE VIEW accountant_view AS
>         SELECT patient_ID, patient_name, billing_address, cost FROM
> hospital_table;
>  
>
> Copy

A view can be used almost anywhere that a table can be used (joins,
subqueries, etc.). For example, using the views created above:

  * Show all of the types of medical problems for each patient:

> >     SELECT DISTINCT diagnosis FROM doctor_view;
>     +--------------------+
>     | DIAGNOSIS          |
>     |--------------------|
>     | Industrial Disease |
>     | python bite        |
>     +--------------------+
>  
>
> Copy

  * Show the cost of each treatment (without showing personally identifying information about specific patients):

> >     SELECT treatment, cost
>         FROM doctor_view AS dv, accountant_view AS av
>         WHERE av.patient_ID = dv.patient_ID;
>     +---------------------------+----------+
>     | TREATMENT                 |     COST |
>     |---------------------------+----------|
>     | a week of peace and quiet |  2000.00 |
>     | anti-venom                | 70000.00 |
>     +---------------------------+----------+
>  
>
> Copy

A [CREATE VIEW](../sql-reference/sql/create-view) command can use a fully-
qualified, partly-qualified, or unqualified table name. For example:

>
>     CREATE VIEW v1 AS SELECT ... FROM my_database.my_schema.my_table;
>  
>     CREATE VIEW v1 AS SELECT ... FROM my_schema.my_table;
>  
>     CREATE VIEW v1 AS SELECT ... FROM my_table;
>  
>
> Copy

If the schema is not specified, then Snowflake assumes that the table is in
the same schema as the view. (If the table were assumed to be in the active
schema, then the view could refer to different tables at different times.)

## Types of Views¶

Snowflake supports two types of views:

  * Non-materialized views (usually simply referred to as “views”)

  * Materialized views.

### Non-materialized Views¶

The term “view” generically refers to all types of views; however, the term is
used here to refer specifically to non-materialized views.

A view is basically a named definition of a query. A non-materialized view’s
results are created by executing the query at the time that the view is
referenced in a query. The results are not stored for future use. Performance
is slower than with materialized views. Non-materialized views are the most
common type of view.

Any query expression that returns a valid result can be used to create a non-
materialized view, such as:

  * Selecting some (or all) columns in a table.

  * Selecting a specific range of data in table columns.

  * Joining data from two or more tables.

### Materialized Views¶

Although a materialized view is named as though it were a type of view, in
many ways it behaves more like a table. A materialized view’s results are
stored, almost as though the results were a table. This allows faster access,
but requires storage space and active maintenance, both of which incur
additional costs.

In addition, materialized views have some restrictions that non-materialized
views do not have.

For more details, see [Working with Materialized Views](views-materialized).

## Secure Views¶

Both non-materialized and materialized views can be defined as _secure_.
Secure views have advantages over standard views, including improved data
privacy and data sharing; however, they also have some performance impacts to
take into consideration.

For more details, see [Working with Secure Views](views-secure).

## Recursive Views (Non-materialized Views Only)¶

A non-materialized view can be recursive (i.e. the view can refer to itself).

Use of recursion in views is similar to the use of recursion in [recursive
CTEs](queries-cte.html#label-recursive-common-table-expression). In fact, a
view can be defined with a recursive CTE. For example:

>
>     CREATE VIEW employee_hierarchy (title, employee_ID, manager_ID,
> "MGR_EMP_ID (SHOULD BE SAME)", "MGR TITLE") AS (
>        WITH RECURSIVE employee_hierarchy_cte (title, employee_ID,
> manager_ID, "MGR_EMP_ID (SHOULD BE SAME)", "MGR TITLE") AS (
>           -- Start at the top of the hierarchy ...
>           SELECT title, employee_ID, manager_ID, NULL AS "MGR_EMP_ID (SHOULD
> BE SAME)", 'President' AS "MGR TITLE"
>             FROM employees
>             WHERE title = 'President'
>           UNION ALL
>           -- ... and work our way down one level at a time.
>           SELECT employees.title,
>                  employees.employee_ID,
>                  employees.manager_ID,
>                  employee_hierarchy_cte.employee_id AS "MGR_EMP_ID (SHOULD
> BE SAME)",
>                  employee_hierarchy_cte.title AS "MGR TITLE"
>             FROM employees INNER JOIN employee_hierarchy_cte
>            WHERE employee_hierarchy_cte.employee_ID = employees.manager_ID
>        )
>        SELECT *
>           FROM employee_hierarchy_cte
>     );
>  
>
> Copy

Instead of using a recursive CTE, you can create a recursive view with the
keyword `RECURSIVE`, for example:

>
>     CREATE RECURSIVE VIEW employee_hierarchy_02 (title, employee_ID,
> manager_ID, "MGR_EMP_ID (SHOULD BE SAME)", "MGR TITLE") AS (
>           -- Start at the top of the hierarchy ...
>           SELECT title, employee_ID, manager_ID, NULL AS "MGR_EMP_ID (SHOULD
> BE SAME)", 'President' AS "MGR TITLE"
>             FROM employees
>             WHERE title = 'President'
>           UNION ALL
>           -- ... and work our way down one level at a time.
>           SELECT employees.title,
>                  employees.employee_ID,
>                  employees.manager_ID,
>                  employee_hierarchy_02.employee_id AS "MGR_EMP_ID (SHOULD BE
> SAME)",
>                  employee_hierarchy_02.title AS "MGR TITLE"
>             FROM employees INNER JOIN employee_hierarchy_02
>             WHERE employee_hierarchy_02.employee_ID = employees.manager_ID
>     );
>  
>
> Copy

For more details, including examples, see [CREATE VIEW](../sql-
reference/sql/create-view).

## Advantages of Views¶

### Views Enable Writing More Modular Code¶

Views help you to write clearer, more modular SQL code. For example, suppose
that your hospital database has a table listing information about all
employees. You can create views to make it convenient to extract information
about only the medical staff or only the maintenance staff. You can even
create hierarchies of views.

For example, you can create one view for the doctors, and one for the nurses,
and then create the `medical_staff` view by referring to the doctors view and
nurses view:

>
>     CREATE TABLE employees (id INTEGER, title VARCHAR);
>     INSERT INTO employees (id, title) VALUES
>         (1, 'doctor'),
>         (2, 'nurse'),
>         (3, 'janitor')
>         ;
>  
>     CREATE VIEW doctors as SELECT * FROM employees WHERE title = 'doctor';
>     CREATE VIEW nurses as SELECT * FROM employees WHERE title = 'nurse';
>     CREATE VIEW medical_staff AS
>         SELECT * FROM doctors
>         UNION
>         SELECT * FROM nurses
>         ;
>  
>
> Copy
>  
>  
>     SELECT *
>         FROM medical_staff
>         ORDER BY id;
>     +----+--------+
>     | ID | TITLE  |
>     |----+--------|
>     |  1 | doctor |
>     |  2 | nurse  |
>     +----+--------+
>  
>
> Copy

In many cases, rather than writing one large and difficult-to-understand
query, you can decompose the query into smaller pieces, and create a view for
each of those pieces. This not only makes the code easier to understand, but
in many cases it also makes the code easier to debug because you can debug one
view at a time, rather than the entire query.

One view can be referenced by many different queries, so views help increase
code re-use.

### Views Allow Granting Access to a Subset of a Table¶

Views allow you to grant access to just a portion of the data in a table(s).
For example, suppose that you have a table of medical patient records. The
medical staff should have access to all of the medical information (for
example, diagnosis) but not the financial information (for example, the
patient’s credit card number). The accounting staff should have access to the
billing-related information, such as the costs of each of the prescriptions
given to the patient, but not to the private medical data, such as diagnosis
of a mental health condition. You can create two separate views, one for the
medical staff, and one for the billing staff, so that each of those roles sees
only the information needed to perform their jobs. Views allow this because
you can grant privileges on a particular view to a particular role, without
the grantee role having privileges on the table(s) underlying the view.

In the medical example:

  * The medical staff would not have privileges on the data table(s), but would have privileges on the view showing diagnosis and treatment.

  * The accounting staff would not have privileges on the data table(s), but would have privileges on the view showing billing information.

For additional security, Snowflake supports defining a view as secure. For
more details about secure views, see [Working with Secure Views](views-
secure).

### Materialized Views Can Improve Performance¶

Materialized Views are designed to improve performance. Materialized Views
contain a copy of a subset of the data in a table. Depending upon the amount
of data in the table and in the materialized view, scanning the materialized
view can be much faster than scanning the table. Materialized views also
support clustering, and you can create multiple materialized views on the same
data, with each materialized view being clustered on a different column, so
that different queries can each run on the view with the best clustering for
that query.

For more details, see [Working with Materialized Views](views-materialized).

## Limitations on Views¶

  * For limitations and usage notes related to creating views, see [CREATE VIEW](../sql-reference/sql/create-view.html#label-create-view-usage-notes).

  * The definition for a view cannot be updated (i.e. you cannot use [ALTER VIEW](../sql-reference/sql/alter-view) or [ALTER MATERIALIZED VIEW](../sql-reference/sql/alter-materialized-view) to change the definition of a view). To change a view definition, you must recreate the view with the new definition.

  * Views are read-only (i.e. you cannot execute DML commands directly on a view). However, you can use a view in a subquery within a DML statement that updates the underlying base table. For example:
    
        DELETE FROM hospital_table 
        WHERE cost > (SELECT AVG(cost) FROM accountant_view);
    

Copy

  * Changes to a table are not automatically propagated to views created on that table. For example, if you drop a column in a table, the views on that table might become invalid.

