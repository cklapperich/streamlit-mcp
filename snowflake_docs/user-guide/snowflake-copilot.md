# Using Snowflake Copilot¶

This topic provides an introduction to what Snowflake Copilot is and how to
use it in your data analysis workflow. The examples in this topic uses
worksheets but the same steps apply to using Snowflake Copilot in Snowflake
Notebooks.

Note

Support for this feature is available to accounts in the following regions:

  * AWS us-east-1

  * AWS us-west-2

  * AWS eu-central-1

  * Azure eastus2

## Introduction¶

Snowflake Copilot is an LLM-powered assistant that simplifies data analysis
while maintaining robust data governance, and seamlessly integrates into your
existing Snowflake workflow.

Snowflake Copilot is powered by a model fine-tuned by Snowflake that runs
securely inside [Snowflake Cortex](../guides-overview-ai-features),
Snowflake’s intelligent, fully managed AI service. This approach means that
your enterprise data and metadata always stay securely inside Snowflake.
Snowflake Copilot also fully respects RBAC and provides suggestions based only
on the datasets that you can access.

Snowflake Copilot uses natural language requests to enable data analysis from
start to finish. To start, Copilot can help answer questions about how your
data is structured and guide you in exploring a new dataset. You can then ask
Copilot to generate and refine SQL queries to extract useful information from
your data. Snowflake Copilot can even help improve your SQL query by
recommending optimizations or suggesting fixes for possible issues.

Snowflake Copilot can also help improve your SQL fluency or understanding of
Snowflake features. Ask questions about how to perform a task in Snowflake and
Copilot will return answers based on the Snowflake documentation.

You can interact with Copilot in SQL Worksheets and Snowflake Notebooks in
Snowsight. Using the Copilot panel, you can enter a question, and Snowflake
Copilot will reply with an answer. You can run suggested SQL queries in your
worksheet or notebook.

## Access control requirements¶

The COPILOT_USER database role in the SNOWFLAKE database includes the
privileges that allow users to use Snowflake Copilot features. By default, the
COPILOT_USER role is granted to the PUBLIC role. The PUBLIC role is
automatically granted to all users and roles, so this allows all users in your
account to use Snowflake Copilot features.

Users with this privilege will see Ask Copilot in the lower-right corner of
their worksheet or notebook and can use the panel to interact with Snowflake
Copilot.

## Limit access to Copilot¶

If you don’t want all users to have this privilege, you can revoke access to
the PUBLIC role and grant access to specific roles.

To revoke the COPILOT_USER database role from the PUBLIC role, run the
following command using the ACCOUNTADMIN role:

    
    
    USE ROLE ACCOUNTADMIN;
    
    REVOKE DATABASE ROLE SNOWFLAKE.COPILOT_USER
      FROM ROLE PUBLIC;
    

Copy

A user without this role will not see Ask Copilot in the lower-right corner of
their worksheet or notebook. You can switch your active role in the navigation
menu on the left to switch to a role that has access to Copilot to see the Ask
Copilot menu again. For details, see [Switch your active role](ui-snowsight-
gs.html#label-switching-your-active-role).

You can then selectively provide access to specific roles. The
SNOWFLAKE.COPILOT_USER database role cannot be granted directly to a user. For
more information, see [Using SNOWFLAKE database roles](../sql-
reference/snowflake-db-roles.html#label-using-snowflake-db-roles). A user with
the ACCOUNTADMIN role can grant this role to a custom role in order to allow
users to access Snowflake Copilot features. In the following example, use the
ACCOUNTADMIN role and grant the user `some_user` the COPILOT_USER database
role via the account role `copilot_access_role`, which you create for this
purpose.

    
    
    USE ROLE ACCOUNTADMIN;
    
    CREATE ROLE copilot_access_role;
    GRANT DATABASE ROLE SNOWFLAKE.COPILOT_USER TO ROLE copilot_access_role;
    
    GRANT ROLE copilot_access_role TO USER some_user;
    

Copy

You can also grant access to Snowflake Copilot through existing roles commonly
used by specific groups of users. (See [User roles](admin-user-
management.html#label-user-management-user-roles).) For example, if you have
created an `analyst` role that is used as a default role by analysts in your
organization, you can easily grant these users access to Snowflake Copilot
with a single GRANT statement.

    
    
    GRANT DATABASE ROLE SNOWFLAKE.COPILOT_USER TO ROLE analyst;
    

Copy

## Supported use cases¶

  * **Explore your data** by asking open-ended questions to learn about the structure and nuances of a new dataset.

  * **Generate SQL queries** with questions in plain English.

  * **Try out the SQL query** suggested by Snowflake Copilot with the click of a button. You can also edit the query before running it.

  * **Build complex queries** through a conversation with Snowflake Copilot by asking follow-up questions to refine the suggested SQL query and dig deeper into the analysis.

  * **Learn about Snowflake** by asking questions about Snowflake concepts, capabilities, and features.

  * **Improve your queries** by asking Snowflake Copilot to help you assess query efficiency, find optimizations, or explain what the query does.

  * **Provide feedback** (thumbs up or thumbs down) on each response from Snowflake Copilot, which will be used to improve the product.

  * **Add custom instructions** such as a set of preferences or specific business knowledge for Snowflake Copilot to consider when generating responses.

## Limitations¶

  * **Limited language support:** Today, only English and SQL are supported.

  * **No access to your data:** Snowflake Copilot does not have access to the data inside your tables. If you want to filter on a particular value of a column, you should provide that value. For example, if you ask Snowflake Copilot to return all rows with a column A value equal to “X”, you should provide the value “X” in your request. See the Construct and run a SQL Statement example.

  * **Cross database or schema queries are not supported:** You can work around this by creating and using views that join data from different schemas and databases.

  * **Delayed response:** Snowflake Copilot might take a second to complete a response, depending on the length of the response provided.

  * **SQL suggestions may not always work:** Snowflake Copilot may sometimes suggest queries that contain invalid SQL syntax or non-existent tables or columns. Please provide feedback using the thumbs up or thumbs down buttons for the particular response. This feedback helps us improve this feature.

  * **Delay in detecting new databases, schemas, and tables:** It may take up to 3-4 hours for Snowflake Copilot to recognize newly created databases, schemas, and tables.

  * **Limited number of tables and columns considered:** To generate a response, Snowflake Copilot first searches for tables and columns most relevant for your request. The search results are then ranked by relevancy and only the top 10 tables and top 10 columns from each of those tables in the results are considered when generating a response.

## How to use Snowflake Copilot¶

Snowflake Copilot is ready to use with no additional setup. Remember the
following points when using Snowflake Copilot:

  * Each chat session with Snowflake Copilot is associated with a particular worksheet or notebook. Opening a new worksheet or notebook opens a new chat session.

  * You must have a database and schema in use during your session to use Snowflake Copilot. Copilot uses them to generate relevant responses.

  * Snowflake Copilot uses the names of your databases, schemas, tables, and columns and also the data types of your columns to determine what data is available to query.

  * If Snowflake Copilot cannot answer your question based on the selected database and schema, it may try to use other ways to answer, such as the Snowflake documentation or general SQL knowledge. If you get an unexpected response, you can leave feedback using the thumbs up and thumbs down buttons.

  * If you need to refer to a table name or a column name in your question, prefix the name with `@`. Referring to specific tables and columns can help Snowflake Copilot provide more accurate responses.

  * For optimal performance, use meaningful names for databases, schemas, tables, and columns, and ensure that columns are assigned the appropriate data type.

Follow these steps to start using Snowflake Copilot:

  1. Create a new worksheet or open an existing worksheet.

  2. Select Ask Copilot in the lower-right corner of the worksheet. The Snowflake Copilot panel opens on the right side of the worksheet.

  3. Make sure a database and a schema are selected for the current worksheet. If not, you can select them by using either the selector on the top of the worksheet or the selector below the Snowflake Copilot message box.

  4. In the message box, type in your question and then select the send icon or press `Enter` to submit it. Snowflake Copilot provides a response in the panel.

  5. If the response from Snowflake Copilot includes SQL statements:

     * Select Run to run the query. This adds the query to your worksheet and runs it.

     * Select Add to edit the query before running it. This adds the query to your worksheet.

## Add custom instructions¶

Snowflake Copilot accepts custom instructions that let you customize how it
responds. When enabled, these instructions are used to enhance the prompt
that’s sent to the model behind Snowflake Copilot and are considered by
Copilot when it’s generating new responses. Custom instructions can include
directions to use a specific tone or respond in a certain way, preferences on
how to write SQL, or additional information about the data to consider.

Remember the following when adding custom instructions:

  * There is a 2,000 character limit for custom instructions.

  * Snowflake recommends specifying custom instructions in plain English.

  * The instructions are specific to the user that entered them and used for all their conversations with Snowflake Copilot.

Follow these steps to add custom instructions for Snowflake Copilot:

  1. Create a new worksheet or open an existing worksheet.

  2. Select Ask Copilot in the lower-right corner of the worksheet. The Snowflake Copilot panel opens on the right side of the worksheet.

  3. Select the Copilot menu at the top of the Snowflake Copilot panel.

  4. Select Custom instructions from the drop-down menu.

  5. To enable the custom instructions text box, select the Enable for new chats toggle on the bottom left of the custom instructions window.

  6. Enter your instructions in plain text English.

  7. Select Save when finished.

  8. Continue your conversation with Snowflake Copilot in the Copilot panel.

## Examples¶

The following sections provide examples that demonstrate how to:

  * Explore your data

  * Construct and run SQL statements

  * Get an explanation of a SQL statement

  * Ask questions about SQL and Snowflake concepts

These examples use a sample dataset from the Snowflake Marketplace.

### Prerequisites¶

The examples in this section use the [Cybersyn Github Archive
dataset](https://app.snowflake.com/marketplace/listing/GZTSZAS2KJ3/cybersyn-
inc-cybersyn-github-archive) from the Snowflake Marketplace:

  1. Install the [Cybersyn Github Archive dataset](https://app.snowflake.com/marketplace/listing/GZTSZAS2KJ3/cybersyn-inc-cybersyn-github-archive) in your account.

  2. Create a new worksheet or open an existing worksheet.

  3. Select Ask Copilot in the lower-right corner of the worksheet.

  4. Select the Cybersyn Github Archive database and schema.

### Explore your data¶

The following example demonstrates how to use Snowflake Copilot to explore a
dataset.

  1. Enter an open-ended question such as “What types of questions can I ask about this dataset?”

  2. Press `Enter` and Snowflake Copilot will generate a response based on the database and schema you’ve selected.

  3. Ask further clarifying questions about the data, such as “What type of events can I filter by?” or “Are any of these tables joinable?”

  4. If the response from Snowflake Copilot includes a SQL statement, you can select Add to add the query to the end of your worksheet and edit it before running or select Run to add the query and run it automatically.

### Construct and run a SQL Statement¶

The following example demonstrates how to use Snowflake Copilot to generate
SQL queries.

  1. Enter the question “How many stars were given in the past year?” in the Snowflake Copilot message box, and press `Enter`. Snowflake Copilot responds with a SQL query that answers your question.

  2. Select Add to add the query to the end of your worksheet.

  3. Enter the question “Show me this for each month,” and press `Enter`. Snowflake Copilot responds with a SQL query that answers your question.

  4. Select Run to add the query to your worksheet and run the query.

Snowflake Copilot does not have access to the data inside your tables. If you
want Snowflake Copilot to construct a SQL statement that filters based on a
specific value of a column, you must provide the value to filter on.

  1. Enter the question “what are all the repo names that start with ‘snowflake’?” in the message box and press `Enter`. Snowflake Copilot responds with a SQL query that uses the filter value you provided.

  2. Select Add to edit the query before running or select Run to add the query to your worksheet and run it.

### Explain a SQL statement¶

The following example demonstrates how to use Snowflake Copilot to explain a
SQL statement you’re working on.

  * In the Snowflake Copilot message box, type the following question and SQL query:
    
        Can you explain this query to me step-by-step?
    

Copy

    
        SELECT
      github_repos.repo_name,
      COUNT(github_stars.repo_id) AS total_stars
    FROM
      github_repos
      JOIN github_stars ON github_repos.repo_id = github_stars.repo_id
    GROUP BY
      github_repos.repo_name
    ORDER BY
      total_stars DESC;
    

Copy

Snowflake Copilot responds with a step-by-step explanation of the provided
query.

### Ask questions about SQL and Snowflake¶

Snowflake Copilot has access to Snowflake documentation and can answer general
questions about Snowflake or SQL. Here are some example questions you can try:

  * How do I write a SQL join?

  * What is Snowpark Cortex?

  * How do I ingest data into Snowflake?

## Tips for using Snowflake Copilot¶

  * Creating curated [views](views-introduction) can significantly improve the performance of Snowflake Copilot.

Follow these guidelines when creating the views:

Guideline | Example  
---|---  
Use descriptive and easy-to-understand names for the views and their columns. When choosing the names, use the business and data taxonomy you are likely to use while using Snowflake Copilot. | If a column contains the date for a specific sale, name the column `sale_date`.  
Make sure all columns have the appropriate data type. | If a column contains the date for a specific sale, make sure it has the [DATE](../sql-reference/data-types-datetime.html#label-datatypes-date) type.  
Define commonly used metrics/expressions as new columns. | If profit is defined as `revenue - cost`, create a column `(revenue - cost) AS profit` in your view.  
If possible, capture common and complex joins. | If two tables `products` and `sales` are often joined, make sure that your view joins these tables. If there are multiple join paths between commonly joined tables, use the preferred join path in your view.  
  * Be as specific as possible when you ask a question. Imagine that you are asking a question to a human who may have limited knowledge of your data.

  * If you want to filter on specific values inside columns, you might need to actively guide Snowflake Copilot. You can ask Snowflake Copilot for a query that returns all the distinct values in a column.

## Costs¶

Snowflake Copilot is currently free to use. Details on pricing and billing are
planned but you will be notified before any charges are applied for this
feature.

## Legal notices¶

Snowflake Copilot is powered by machine learning technology, including Meta’s
Code Llama and Llama Guard. The foundation Code LLama and Llama Guard models
are licensed under the [LLaMA 2 Community
License](https://github.com/facebookresearch/llama/blob/main/LICENSE) and
Copyright (c) Meta Platforms, Inc. All Rights Reserved. Your use of this
feature is subject to Meta’s [Acceptable Use
Policy](https://ai.meta.com/llama/use-policy/).

For additional information, refer to [Snowflake AI and ML](../guides-overview-
ai-features).

The data classification of inputs and outputs are as set forth in the
following table.

Input data classification | Output data classification | Designation  
---|---|---  
Usage Data | Usage Data | Covered AI Features [1]  
[1]

Represents the defined term used in the AI Terms and Acceptable Use Policy.

For additional information, refer to [Snowflake AI and ML](../guides-overview-
ai-features).

