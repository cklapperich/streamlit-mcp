# Getting started with differential privacy¶

## Introduction¶

This tutorial demonstrates how to protect sensitive data using a differential
privacy policy so that you can share it safely with analysts.

### What you will learn¶

In this tutorial you will learn how to do the following:

  * Create a differential privacy policy.

  * Apply that privacy policy to a table to protect it with differential privacy.

  * Define privacy domains for a table.

  * Run a query on a table protected by differential privacy.

  * Determine the amount of noise present in query results.

This tutorial does not fully explain the key concepts of differential privacy,
such as [noise](../diff-privacy/differential-privacy-overview.html#label-diff-
privacy-noisy-aggregates), [privacy budgets](../diff-privacy/differential-
privacy-admin-privacy-budgets), and [privacy domains](../diff-
privacy/differential-privacy-privacy-domains). This tutorial focuses on how to
apply differential privacy to your data.

### About admins and analysts¶

You’ll be assuming two personas in this tutorial:

  * The admin, who has privileges to the raw data and manages differential privacy policies on a table.

  * The analyst, who runs queries on this protected data.

In real-world use cases these might be two different people or groups of
people, or they could be one person who wants to analyze and share protected
results safely with others.

While this tutorial shows how to run queries on protected data, it is intended
primarily to show how to implement differential privacy rather than how to
consume it.

### Prerequisites¶

  * You must be on an account with **Enterprise edition or above**.

  * You must be able to **use the ACCOUNTADMIN role**.

Important

In this tutorial you will perform all of the admin persona steps using the
ACCOUNTADMIN role. In general practice, though, you should use roles with
privileges specifically defined for the action you’re performing. The
privileges required to create and apply privacy policies are [described
here](../diff-privacy/differential-privacy-overview.html#label-diff-privacy-
noisy-aggregates).

## Create roles, a warehouse, and data¶

In this section, you will perform the following setup steps:

  * Create a role for the analyst.

  * Create the warehouse used to execute the queries against the protected data.

  * Create mock sensitive data that will be protected by the privacy policy.

None of these setup steps are specific to differential privacy policies. If
there already exists a suitable role, warehouse, and/or dataset, you can use
those instead.

### Create the analyst role¶

In a Snowsight worksheet or other environment that is connected to run
Snowflake SQL on your Snowflake account, run the following commands to create
the analyst role and assign it to yourself:

    
    
    USE ROLE ACCOUNTADMIN;
    CREATE ROLE dp_tutorial_analyst;
    
    -- You can find your own user name by running "SELECT CURRENT_USER();"
    GRANT ROLE dp_tutorial_analyst TO USER <user_name>;
    

Copy

### Create a warehouse for the data¶

    
    
    CREATE OR REPLACE WAREHOUSE dp_tutorial_wh;
    GRANT USAGE ON WAREHOUSE dp_tutorial_wh TO ROLE dp_tutorial_analyst;
    

Copy

### Create mock sensitive data¶

The following commands create a database, schema, and table, and fill it with
data. The data simulates a simple diabetes study in which we want to protect
patient identities. Later in the tutorial you’ll use differential privacy to
protect the identity of individuals in the study.

    
    
    -- Create the table
    CREATE OR REPLACE DATABASE dp_db;
    CREATE OR REPLACE SCHEMA dp_db.dp_schema;
    USE SCHEMA dp_db.dp_schema;
    CREATE OR REPLACE TABLE dp_tutorial_diabetes_survey (
      patient_id TEXT,
      is_smoker BOOLEAN,
      has_difficulty_walking BOOLEAN,
      gender TEXT,
      age INT,
      has_diabetes BOOLEAN,
      income_code INT);
    
    -- Populate the table
    INSERT INTO dp_db.dp_schema.dp_tutorial_diabetes_survey
    VALUES
    ('ID-23493', TRUE, FALSE, 'male', 39, TRUE, 2),
    ('ID-00923', FALSE, FALSE, 'female', 82, TRUE, 5),
    ('ID-24020', FALSE, FALSE, 'male', 69, FALSE, 8),
    ('ID-92848', TRUE, TRUE, 'other', 75, FALSE, 3),
    ('ID-62937', FALSE, FALSE, 'male', 46, TRUE, 5);
    

Copy

**Notes:**

Although it might seem that masking the patient ID would be better than using
differential privacy, that would prevent joins against that column.
Additionally, if you added a table where each patient has multiple rows, such
as a medications table or a visits table, simple masking would prevent you
from grouping results by person. This is a case where differential privacy can
be much more powerful than simple masking and row hiding; you can make more of
your data available to analysts and allow more useful queries while still
protecting entity privacy.

## Define a privacy policy¶

Applying a [privacy policy](../diff-privacy/differential-privacy-admin-
privacy-policies) to a table or view protects it with differential privacy and
assigns a [privacy budget](../diff-privacy/differential-privacy-admin-privacy-
budgets) to groups or users so that Snowflake can prevent multiple queries
from revealing too much sensitive information.

You will create the privacy policy in its own database. This is a best
practice for all types of policies in Snowflake. If you create the policy in
the same database, then cloning the database would create unsynchronized
copies of the policy. Putting all policies in a single, separate database, and
applying them to multiple tables lets you manage and update a single copy of
each policy.

You’ll name this new policy `patients_policy`.

    
    
    -- Define a privacy policy. Use default budget, budget window, max budget per aggregate.
    CREATE OR REPLACE DATABASE policy_db;
    CREATE OR REPLACE SCHEMA policy_db.diff_priv_policies;
    CREATE OR REPLACE PRIVACY POLICY policy_db.diff_priv_policies.patients_policy AS () RETURNS privacy_budget ->
      CASE
        WHEN CURRENT_ROLE() = 'ACCOUNTADMIN' THEN no_privacy_policy()
        WHEN CURRENT_ROLE() IN ('DP_TUTORIAL_ANALYST')
          THEN privacy_budget(budget_name => 'clinical_analysts')
        ELSE privacy_budget(budget_name => 'default')
    END;
    

Copy

**Notes:**

  * The privacy policy applied depends on the role of the user, as specified in the CASE statement. Role names are given here in uppercase because CURRENT_ROLE() returns uppercase values.

  * Creating separate privacy budgets per role allows you to separate the budget used for analysts and other users, and also to monitor usage by each group.

  * If the privacy policy resolves to a valid privacy budget when evaluated, the user cannot run non-aggregated SELECT queries, noise is added to the results, and the number of queries is limited by the privacy budget for that policy.

  * The account admin role has no privacy policy applied. This means that queries run as that role have no differential privacy applied. To indicate no privacy policy, you must return `no_privacy_policy()` rather than returning NULL.

  * The DP_TUTORIAL_ANALYST role uses a privacy policy named “clinical_analysts” with default values for privacy budget, budget window, and maximum budget per aggregate.

  * Any other user with SELECT access will get a privacy budget named “default,” also with default privacy policy values. If you want to prevent other users from running queries on this table, you should do so by limiting the SELECT privileges on the table. Table-level policies require an ELSE clause and cannot return NULL.

## Assign the privacy policy¶

Next you’ll assign the privacy policy you just created to the table to protect
it with differential privacy.

    
    
    -- Assign the privacy policy to the table.
    ALTER TABLE dp_db.dp_schema.dp_tutorial_diabetes_survey
    ADD PRIVACY POLICY policy_db.diff_priv_policies.patients_policy ENTITY KEY (patient_id);
    

Copy

**Notes:**

The ENTITY KEY clause specifies a column that uniquely identifies the entity
that should be protected by differential privacy. In this tutorial, which has
a single table where each entity is listed in one and only one row, defining
the entity key is less important. But if each patient could appear in multiple
rows (for example, if it captured patient visits or patient medications), then
defining the key would be important. It’s still a good practice to define the
key here in case a second such table is added to the database later. Learn
more about [entity-level privacy](../diff-privacy/differential-privacy-
admin.html#label-diff-privacy-admin-entity-privacy).

## Define a privacy domain¶

Next you’ll set [privacy domains](../diff-privacy/differential-privacy-
privacy-domains) on select columns in the table.

A privacy domain tells the system the range of values that can be shown in the
results for that column. The system uses this information in two ways:

  * Values outside this range will be omitted or pegged to the boundaries, depending on whether the column is a string or numeric/date value.

  * The system uses this “valid range” as a way to determine the range of results in order to determine the noise applied to each measure value.

An analyst can further restrict a domain, for example by using a WHERE clause,
to potentially reduce the amount of noise generated by differential privacy
(the smaller the domain, the less the noise). If you don’t set a privacy
domain on a column, the analyst must add a privacy domain with a WHERE clause
to see values for that column (columns without a privacy domain cannot be
shown or used in the query).

For the diabetes survey data, you will set privacy domains on three columns:
`gender`, `age`, and `income_code`. You won’t set privacy domains on any
boolean columns (with only two possible values, a privacy domain doesn’t make
sense and isn’t required), and you should not set a privacy domain on the
`patient_id` column because the user can see the values you set in the privacy
domain, which would tell them which patient IDs are in the data. If you need
to specify a privacy domain for a limited number of string values, such as ZIP
codes, you should [pad the domain definition](../diff-privacy/differential-
privacy-privacy-domains-admin.html#label-diff-privacy-admin-privacy-domains-
choosing) with additional, non-present values to obscure possible values.

    
    
    -- Define privacy domains.
    ALTER TABLE dp_db.dp_schema.dp_tutorial_diabetes_survey ALTER (
    COLUMN gender SET PRIVACY DOMAIN IN ('female', 'male', 'other'),
    COLUMN age SET PRIVACY DOMAIN BETWEEN (0, 90),
    COLUMN income_code SET PRIVACY DOMAIN BETWEEN (1, 8)
    );
    

Copy

## Grant analyst access to the table¶

Grant access to the table only after you’ve assigned privacy policies to the
data. Otherwise, users could see the data before you apply privacy policies.

    
    
    GRANT USAGE ON DATABASE dp_db TO ROLE dp_tutorial_analyst;
    GRANT USAGE ON SCHEMA dp_schema TO ROLE dp_tutorial_analyst;
    GRANT SELECT
      ON TABLE dp_db.dp_schema.dp_tutorial_diabetes_survey
      TO ROLE dp_tutorial_analyst;
    

Copy

## Run some queries¶

Finally, you can start running queries against your data!

You will switch roles between admin and analyst to compare the behavior and
output for each role.

### Check that differential privacy is working¶

Use the administrator role to run a query that returns individual rows. This
query succeeds because the privacy policy resolves to no_privacy_policy() for
the ACCOUNTADMIN role:

    
    
    USE ROLE ACCOUNTADMIN;
    SELECT * FROM dp_db.dp_schema.dp_tutorial_diabetes_survey;
    

Copy

Now run the same query using the analyst role. The query fails because
differential privacy does not allow SELECT * queries.

    
    
    USE ROLE dp_tutorial_analyst;
    SELECT * FROM dp_db.dp_schema.dp_tutorial_diabetes_survey;
    

Copy

Try with a third role to ensure that the default result is the same. (Don’t
forget to grant SELECT on the table to the person or role!)

### See what noise looks like¶

First, run a simple query as the administrator, without differential privcy
applied. You will see the exact table values.

    
    
    -- Run a basic query without DP.
    USE ROLE ACCOUNTADMIN;
    SELECT COUNT(DISTINCT patient_id)
      FROM dp_db.dp_schema.dp_tutorial_diabetes_survey
      WHERE income_code = 5;
    

Copy

Now run the same query as an analyst, and you’ll see that noise has been
applied to the results. Note that the query takes a little longer because
differential privacy is being applied.

    
    
    USE ROLE dp_tutorial_analyst;
    SELECT COUNT(DISTINCT patient_id)
      FROM dp_db.dp_schema.dp_tutorial_diabetes_survey
      WHERE income_code = 5;
    

Copy

The results are typically different from the admin results because
differential privacy has introduced noise into the results to obscure the
presence of an individual in the dataset. However, the results can sometimes
be identical because in any given query the randomly generated noise was small
enough to round down to 0. But the analyst cannot know whether or not there is
noise applied to any given query. You can try running this query again to see
if you get a different result.

### Analyze the amount of noise¶

Although analysts cannot see results without noise, they do need a way to
understand how noisy the result is, in general, to determine whether the data
is usable for their needs. In order to provide this information, we expose the
noise interval of each query parameter to the analyst. The noise interval is
retrieved using the functions [DP_INTERVAL_LOW](../../sql-
reference/functions/dp_interval_low) and [DP_INTERVAL_HIGH](../../sql-
reference/functions/dp_interval_high).

    
    
    -- Retrieve noise interval for the previous query.
    USE ROLE dp_tutorial_analyst;
    SELECT COUNT(DISTINCT patient_id) as c,
      DP_INTERVAL_LOW(c) as LOW,
      DP_INTERVAL_HIGH(c) as HIGH
      FROM dp_db.dp_schema.dp_tutorial_diabetes_survey
      WHERE income_code = 5;
    

Copy

There is a minimum 95% confidence that the true value of the aggregation is
between LOW and HIGH.

Note that the interval for this query on this data is wide compared to the
magnitude of the result because of the artificially small dataset. This wide
noise interval essentially means that there are too few patients here for
Snowflake to be able to give an accurate answer while protecting their
privacy.

### See your budget and estimated remaining queries¶

Users running queries on differential privacy protected tables can see their
differential privacy budget used, and an estimate of the number of remaining
queries, by calling the [ESTIMATE_REMAINING_DP_AGGREGATES](../../sql-
reference/functions/estimate_remaining_dp_aggregates) table function. Assume
the role for which you want to see the budget, then call the function as shown
here:

    
    
    USE ROLE <role_name>;
    SELECT * FROM TABLE(SNOWFLAKE.DATA_PRIVACY.ESTIMATE_REMAINING_DP_AGGREGATES(dp_db.dp_schema.dp_tutorial_diabetes_survey));
    

Copy

## Clean up¶

Clean up your resources so that you, or someone else in your org, can run the
tutorial again later.

    
    
    USE ROLE ACCOUNTADMIN;
    DROP ROLE dp_tutorial_analyst;
    DROP WAREHOUSE dp_tutorial_wh;
    ALTER TABLE dp_tutorial_diabetes_survey
      DROP PRIVACY POLICY policy_db.diff_priv_policies.patients_policy;
    DROP DATABASE dp_db;
    DROP DATABASE policies_db;
    

Copy

