# Getting started with Streamlit in Snowflake¶  
  
This topic describes how to begin using Streamlit in Snowflake.

## Prerequisites for using Streamlit in Snowflake¶

To use Streamlit in Snowflake, ensure that you meet the following
prerequisites:

  * Have privileges required to create and use a Streamlit app.

  * To use Mapbox in Streamlit in Snowflake and the packages provided by Anaconda, you must acknowledge the [External Offerings Terms](https://www.snowflake.com/legal/external-offering-terms/).

For information about using these packages, see [Using Third-Party Packages
from Anaconda](../udf/python/udf-python-packages.html#label-python-udfs-
anaconda-terms).

  * Ensure that `*.snowflake.app` is allowlisted in your network and that the app can connect to Snowflake.

For more information, see [You cannot load the Streamlit
app](troubleshooting.html#label-streamlit-troubleshooting-allowlist).

## Privileges required to create and use a Streamlit app¶

Within Streamlit in Snowflake, a Streamlit app is a securable object that
adheres to the [Snowflake access control framework](../../user-guide/security-
access-control-overview). Streamlit apps use a permission model that is based
on owner’s rights. For more information, see [Understanding owner’s rights and
Streamlit in Snowflake apps](owners-rights).

An app editor and the owner of the schema containing the Streamlit app can
determine which roles have permission to use the app. Users can interact with
the app and can see anything displayed by the Streamlit app. Users have the
same view of the app as the owner does.

For more information, see [Share a Streamlit app](create-streamlit-
ui.html#label-streamlit-sharing).

### Privileges required to create a Streamlit app¶

Streamlit apps are schema-level objects.

To create and edit a Streamlit app by using Streamlit in Snowflake, you must
use a role that has either the OWNERSHIP privilege on the schema, or both of
the following privileges:

  * Granted on the database that contains the Streamlit app:

    * USAGE

  * Granted on the schema that contains the Streamlit app:

    * USAGE

    * CREATE STREAMLIT

    * CREATE STAGE

You must also have the USAGE privilege on the warehouse used to run the
Streamlit app.

Use the [GRANT <privileges>](../../sql-reference/sql/grant-privilege) command
to grant these privileges to a role, as shown in this example:

>
>     GRANT USAGE ON SCHEMA streamlit_db.streamlit_schema TO ROLE
> streamlit_creator;
>     GRANT USAGE ON DATABASE streamlit_db TO ROLE streamlit_creator;
>     GRANT USAGE ON WAREHOUSE streamlit_wh TO ROLE streamlit_creator;
>     GRANT CREATE STREAMLIT ON SCHEMA streamlit_db.streamlit_schema TO ROLE
> streamlit_creator;
>     GRANT CREATE STAGE ON SCHEMA streamlit_db.streamlit_schema TO ROLE
> streamlit_creator;
>  
>
> Copy

If a future grant is defined on the database or schema, ensure that the user
creates the Streamlit app using the role defined in the future grant.

### Privileges required to view a Streamlit app¶

To view a Streamlit app, you must have a Snowflake account and be signed in.
Additionally, you must use a role that is granted the USAGE privilege on the
following objects:

  * The database that contains the Streamlit app

  * The schema that contains the Streamlit app

  * The Streamlit app

In most cases, when the app owner shares a Streamlit app with another role,
the USAGE privilege is automatically granted to the new role. However, if a
Streamlit app is created in a schema with MANAGED ACCESS, the USAGE privilege
must be manually granted to the new role.

The schema owner or a user with the role with the MANAGE GRANTS privilege must
grant the USAGE privilege using the [GRANT <privileges>](../../sql-
reference/sql/grant-privilege) command as shown in this example:

    
    
    GRANT USAGE ON DATABASE streamlit_db TO ROLE streamlit_role;
    GRANT USAGE ON SCHEMA streamlit_db.streamlit_schema TO ROLE streamlit_role;
    GRANT USAGE ON STREAMLIT streamlit_db.streamlit_schema.streamlit_app TO ROLE streamlit_role;
    

Copy

## Supported versions of the Streamlit library¶

Streamlit in Snowflake supports the following versions of the Streamlit open-
source library:

  * 1.39.0 (currently in preview)

  * 1.35.0

  * 1.31.1

  * 1.29.0

  * 1.26.0

  * 1.22.0

To view release notes for each version, see [Streamlit library
changelog](https://docs.streamlit.io/library/changelog). Note that some
features of the open-source Streamlit library are unsupported in Streamlit in
Snowflake. See [Unsupported Streamlit features](limitations.html#label-
streamlit-unsupported-features).

### Select the Streamlit library version¶

For each Streamlit in Snowflake app, you can [select the Streamlit library
version](create-streamlit-ui.html#label-streamlit-install-packages-ui) in
Snowsight or [pin the version](create-streamlit-sql.html#label-streamlit-pin-
version) in the app’s `environment.yml` file. If you do not pin the version,
the latest available version is used.

Snowflake recommends pinning a version of Streamlit to prevent the app from
being upgraded when a new version of Streamlit becomes available in the
Snowflake Anaconda Channel.

## Supported external packages¶

By default, Streamlit in Snowflake includes the `python`, `streamlit`, and
`snowflake-snowpark-python` packages pre-installed in your environment. The
environment also has access to the dependencies required by these packages.

Streamlit in Snowflake apps run in Python 3.8.

You can install additional packages in your Streamlit app. For a list of
supported packages, see the [Snowflake Anaconda
Channel](https://repo.anaconda.com/pkgs/snowflake/).

See the following topics for information about including a supported package
in your Streamlit app:

  * [Manage packages for a Streamlit app](create-streamlit-ui.html#label-streamlit-install-packages-ui)

  * [Manage packages by using the environment.yml file](create-streamlit-sql.html#label-streamlit-install-packages-manual)

## Guidelines for selecting a warehouse in Streamlit in Snowflake¶

When you run a Streamlit app in Streamlit in Snowflake, multiple factors may
affect performance, including the complexity of the Streamlit app,
availability of warehouses, latency, and cost. The following sections provide
general guidelines for using virtual warehouses in Streamlit in Snowflake.

### Use smaller warehouses¶

When you run a Streamlit app in Streamlit in Snowflake, you should select the
smallest warehouse possible.

When running, a warehouse maintains a cache of the Python packages used by a
Streamlit app. Caching Python packages improves the performance for later app
loads by using the cached version of a package instead of downloading the
packages again. The cache is removed when the warehouse is suspended, which
may result in a slower loading of the app initially after the warehouse is
resumed. As the resumed warehouse runs more apps, the package cache is
rebuilt, and apps that can take advantage of the cache will experience
improved app loading performance.

Note that per-second credit billing and auto-suspend give you the flexibility
to start with smaller warehouses and then adjust the size of the warehouse to
match the workload of the Streamlit app. You can increase the size of a
warehouse at any time. For more information, see [Change the warehouse of a
Streamlit app](create-streamlit-ui.html#label-streamlit-ui-change-warehouse).

### Use dedicated warehouses¶

When you use Streamlit in Snowflake, Snowflake recommends using a dedicated
warehouse for running Streamlit apps. This enables you to isolate the costs of
running a Streamlit app. A dedicated warehouse may also improve the load time
of the app because the warehouse does not have to manage other workloads.

For more information, see [Warehouse considerations](../../user-
guide/warehouses-considerations).

Tip

To avoid warehouse suspension during initialization, consider setting auto-
suspend to a minimum of 30 seconds.

### Use a separate warehouse to run queries¶

Streamlit apps use a virtual warehouse to run the app and its queries. More
advanced apps and use cases might involve running a complex query, which
requires a larger warehouse.

Streamlit in Snowflake supports the [USE WAREHOUSE](../../sql-
reference/sql/use-warehouse) command, which specifies a current warehouse for
the session. With this command, you can run the app using an X-Small warehouse
and run complex queries using a larger warehouse.

You can use a separate warehouse to run queries in a Streamlit app with this
code:

    
    
    import streamlit as st
    from snowflake.snowpark.context import get_active_session
    
    # Get the current credentials
    session = get_active_session()
    
    warehouse_sql = f"USE WAREHOUSE LARGE_WH"
    session.sql(warehouse_sql).collect()
    
    # Execute the SQL using a different warehouse
    sql = """SELECT * from MY_DB.INFORMATION_SCHEMA.PACKAGES limit 100"""
    session.sql(sql).collect()
    

Copy

Note

The warehouse is used only for the duration of the query.

## Build your first Streamlit in Snowflake app¶

  1. Sign in to Snowsight.

  2. In the navigation menu, select Projects » Streamlit.

  3. Select \+ Streamlit App.

  4. Enter a title for the app, and choose a database, schema, and warehouse.

  5. Select Create.

### Access Snowflake data in your Streamlit in Snowflake app¶

In this section, you edit the new Streamlit app to access data from a
Snowflake table.

  1. Create a `BUG_REPORT_DATA` table in your database and schema:
    
        CREATE OR REPLACE TABLE <your_database>.<your_schema>.BUG_REPORT_DATA (
      AUTHOR VARCHAR(25),
      BUG_TYPE VARCHAR(25),
      COMMENT VARCHAR(100),
      DATE DATE,
      BUG_SEVERITY NUMBER(38,0)
    );
    

Copy

  2. Add sample data into the `BUG_REPORT_DATA` table:
    
        INSERT INTO <your_database>.<your_schema>.BUG_REPORT_DATA (AUTHOR, BUG_TYPE, COMMENT, DATE, BUG_SEVERITY)
    VALUES
    ('John Doe', 'UI', 'The button is not aligned properly', '2024-03-01', 3),
    ('Aisha Patel', 'Performance', 'Page load time is too long', '2024-03-02', 5),
    ('Bob Johnson', 'Functionality', 'Unable to submit the form', '2024-03-03', 4),
    ('Sophia Kim', 'Security', 'SQL injection vulnerability found', '2024-03-04', 8),
    ('Michael Lee', 'Compatibility', 'Does not work on Internet Explorer', '2024-03-05', 2),
    ('Tyrone Johnson', 'UI', 'Font size is too small', '2024-03-06', 3),
    ('David Martinez', 'Performance', 'Search feature is slow', '2024-03-07', 4),
    ('Fatima Abadi', 'Functionality', 'Logout button not working', '2024-03-08', 3),
    ('William Taylor', 'Security', 'Sensitive data exposed in logs', '2024-03-09', 7),
    ('Nikolai Petrov', 'Compatibility', 'Not compatible with Safari', '2024-03-10', 2);
    

Copy

  3. Edit the Streamlit app code:
    
        import streamlit as st
    
    session = st.connection('snowflake').session()
    
    # Change the query to point to your table
    def get_data(_session):
        query = """
        select * from <your_database>.<your_schema>.BUG_REPORT_DATA
        order by date desc
        limit 100
        """
        data = _session.sql(query).collect()
        return data
    
    # Change the query to point to your table
    def add_row_to_db(session, row):
        sql = f"""INSERT INTO <your_database>.<your_schema>.BUG_REPORT_DATA VALUES
        ('{row['author']}',
        '{row['bug_type']}',
        '{row['comment']}',
        '{row['date']}',
        '{row['bug_severity']}')"""
    
        session.sql(sql).collect()
    
    st.set_page_config(page_title="Bug report", layout="centered")
    
    st.title("Bug report demo!")
    
    st.sidebar.write(
        f"This app demos how to read and write data from a Snowflake Table"
    )
    
    form = st.form(key="annotation", clear_on_submit=True)
    
    with form:
        cols = st.columns((1, 1))
        author = cols[0].text_input("Report author:")
        bug_type = cols[1].selectbox(
            "Bug type:", ["Front-end", "Back-end", "Data related", "404"], index=2
        )
        comment = st.text_area("Comment:")
        cols = st.columns(2)
        date = cols[0].date_input("Bug date occurrence:")
        bug_severity = cols[1].slider("Bug priority :", 1, 5, 2)
        submitted = st.form_submit_button(label="Submit")
    
    if submitted:
        try:
            add_row_to_db(
                session,
                {'author':author,
                'bug_type': bug_type,
                'comment':comment,
                'date':str(date),
                'bug_severity':bug_severity
            })
            st.success("Thanks! Your bug was recorded in the database.")
            st.balloons()
        except Exception as e:
            st.error(f"An error occurred: {e}")
    
    expander = st.expander("See 100 most recent records")
    with expander:
        st.dataframe(get_data(session))
    

Copy

  4. To run the Streamlit app, select Run.

