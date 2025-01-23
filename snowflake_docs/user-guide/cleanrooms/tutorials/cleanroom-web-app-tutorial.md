# Tutorial: Get started with the web app of a Snowflake Data Clean Room¶

## Introduction¶

Feature — Generally Available

Not available in government regions.

A [Snowflake Data Clean Room](../introduction) is a cryptographically secure
environment that allows entities to collaborate on sensitive data. It allows
an entity to share its data with a collaborator while maintaining the privacy
of the data by tightly controlling what can be done with it.

This tutorial leads you through the basic flow of using the web app to work
with a Snowflake Data Clean Room.

### What you will learn¶

In this tutorial, you will learn how to do the following in the web app:

  * Add a collaborator to your clean room environment.

  * Create a clean room, including how to add data, specify join policies, define which type of analysis a collaborator can run on the data, and share the clean room with a collaborator.

  * Install a clean room, including how to add data and define how this data is joined with the collaborator’s data.

  * Run an analysis, including how to create a new analysis based on what is allowed in the clean room and specify relevant parameters for the analysis.

  * Activate the results of the analysis.

### About clean room collaborators¶

Clean room collaborators are either providers or consumers.

A _provider_ is the entity sharing their data with other clean room
collaborators. They create and configure the clean room in order to maintain
the privacy of the data that they are sharing.

A _consumer_ is the entity using the clean room to interact with the shared
data. The consumer can analyze and query the data within the clean room,
including joining and enriching it with their own data.

In this tutorial, you will act as both the provider and the consumer of the
clean room.

### Prerequisites¶

Before completing this tutorial, an administrator must set up the clean room
environment and configure the Snowflake account associated with it. This must
be done for both the provider account and the consumer account. For details on
how to perform these actions, see [Get started with Snowflake Data Clean
Rooms](../getting-started).

To act as a consumer for the purposes of this tutorial, you must have access
to a second Snowflake account associated with a second clean room. This allows
you to mimic how a consumer installs and uses the clean room. If you do not
have a second account, you can still use this tutorial to learn how to create,
configure, and share a clean room.

If you are not the administrator who set up the clean rooms, a clean room
administrator also needs to [add you as an user](../admin-tasks.html#label-
cleanrooms-get-started-add-users) for the web app. You need to be an admin
user in the clean room environment.

## Sign in to the web app as a provider¶

Feature — Generally Available

Not available in government regions.

In this section you will sign in to the clean room where you will create,
configure, and share a clean room as a provider.

To sign in to the web app as a provider:

  1. Navigate to the [Snowflake Data Clean Rooms login page](https://cleanroom.c1.us-east-1.aws.app.snowflake.com).

For this tutorial, you must be a user with the Admin role.

  2. Enter your email address, and select Continue.

  3. Enter your password.

  4. If you are associated with multiple clean room environments, select the Snowflake account you want to use as the provider account.

## Add the consumer as a collaborator¶

Feature — Generally Available

Not available in government regions.

In this section you will add the consumer account you are using for this
tutorial as a collaborator. Administrators must define someone as a
collaborator _before_ other users can share a clean room with that
collaborator.

To add the consumer as a collaborator:

  1. In the left navigation, select Collaborators.

  2. Select the Snowflake Partners tab.

  3. Select \+ Snowflake Partner.

  4. In the Company Name field, enter `Tutorial Consumer`.

  5. In the Email Address field, enter the email associated with your clean room user.

  6. In the Account Locator field, enter the [account locator](../../admin-account-identifier.html#label-account-locator) of the Snowflake account you are using to simulate the consumer experience.

  7. Select the cloud and region of the account you are using to simulate the consumer experience.

  8. Select Add.

## Create and share a clean room¶

Feature — Generally Available

Not available in government regions.

In this section, you will do the following:

  * Create a clean room.

  * Add data to the clean room that is being shared with collaborators.

  * Define a join policy, which controls the columns on which a collaborator can join their own data.

  * Define which type of analysis a collaborator can run in the clean room.

  * Share the clean room with the consumer.

### Start the creation process¶

To begin the process of creating a clean room:

  1. In the left navigation, select Clean Rooms.

  2. On the Clean Rooms page, select \+ Clean Room.

  3. Name your clean room `Tutorial`. You will be allowing collaborators to run an audience overlap analysis in the clean room.

### Add data to your clean room¶

To add data to your clean room:

  1. In the Datasource section, select `Snowflake`.

  2. From the Tables drop-down list, select the `DEMO.CUSTOMERS` table. This table is located under the `SAMOOHA_SAMPLE_DATABASE` database.

  3. Select Next.

### Specify a join policy¶

A join policy controls which columns of a shared table that a collaborator can
join on.

To specify a join policy:

  1. From the Join Columns drop-down list, select the following columns:

     * `HASHED_EMAIL`

     * `HASHED_FIRST_NAME`

     * `HASHED_LAST_NAME`

     * `HASHED_PHONE`

A collaborator can join their data with these columns only.

  2. Select Next.

### Configure an analysis template¶

Analysis templates control how a collaborator can access the shared data in a
clean room. Collaborators can only run analyses and queries that conform to
the template.

To select which analysis template is available to collaborators in the clean
room and configure the template:

  1. Select the `Audience Overlap & Segmentation` template. Collaborators will be limited to running audience overlap & segmentation analyses.

  2. From the Tables drop-down list, select `DEMO.CUSTOMERS`. Collaborators can only analyze data in the `DEMO.CUSTOMERS` table.

  3. From the Segmentation & Activation Columns drop-down list, select the following columns:

     * `AGE_BAND`

     * `DEVICE_TYPE`

     * `EDUCATION_LEVEL`

     * `STATUS`

As the consumer, you will be able to filter and create segments using these
columns.

  4. Toggle on Allow categorical value previews during filtering.

  5. Select Next.

### Share clean room with consumer¶

Now that you have created and configured the clean room, you can share it with
a collaborator so they can use it to run analyses.

To share a clean room:

  1. Use the Select Collaborator drop-down list to select `Tutorial Consumer`.

  2. Select Finish.

  3. You need to wait until the clean room is created before continuing with this tutorial. Periodically select Refresh until the `Tutorial` tile changes from Processing to Edit.

Congratulations! You have created and shared a Snowflake Data Clean Room.

### What you learned¶

In this section, you learned how to install, configure, and share a clean room
as a provider.

In the next part of this tutorial, you will switch to the consumer who joins
the clean room and uses it to analyze data.

## Sign in to the web app as a consumer¶

Feature — Generally Available

Not available in government regions.

In this section, you are switching from being the provider who created and
shared the clean room to the consumer who is installing the clean room. You
are installing the clean room in a different account to mimic how a consumer
would install and use the clean room in their own account.

To sign in to the web app as a consumer:

  1. Navigate to the [Snowflake Data Clean Rooms login page](https://cleanroom.c1.us-east-1.aws.app.snowflake.com).

  2. Enter your email address, and select Continue.

  3. Enter your password.

  4. If you are associated with multiple clean room environments, select the Snowflake account you want to use as the consumer account.

## Install and configure the clean room¶

Feature — Generally Available

Not available in government regions.

In this section you will:

  * Install the clean room that was shared with you from the provider account.

  * Add data to the clean room so it can be joined with the provider’s data.

  * Add a join policy to define how the consumer data and the provider data are related.

  * Define the columns that analysts can use to create segments, filter results, and enrich activation data.

### Start the installation process¶

To start installing a clean room that has been shared by the provider account:

  1. In the left navigation, select Clean Rooms.

  2. Select the Invited tab.

  3. Find the `Tutorial` tile, and select Join.

### Add consumer data to the clean room¶

To add data to the clean room:

  1. In the Datasource section, select `Snowflake`.

  2. From the Tables drop-down list, select the `DEMO.CUSTOMERS` table. This table is located under the `SAMOOHA_SAMPLE_DATABASE` database.

  3. Select Next.

### Define a join policy¶

Consumers use a join policy to specify which columns are joined in an analysis
or query, thereby defining the relationship between provider tables and
consumer tables.

To define a join policy:

  1. Ensure that the columns from the consumer’s table (My Columns) and the columns from the provider’s table (Collaborator Columns ) match. For example, the consumer’s `HASHED_EMAIL` column should be joined with the provider’s `HASHED_EMAIL` column. You specified that collaborators are only allowed to join on these columns when you created the clean room.

  2. Select Next.

### Define the segmentation and activation columns¶

When you select segmentation and activation columns during the clean room
installation process, you are defining which columns are available to users
running analyses in the clean room. Analysts can only create a segment based
on these columns. When sending activation data back to the provider, analysts
cannot enrich the results of the analysis with data unless it comes from one
of these columns.

To define the segmentation and activation columns:

  1. From the Tables drop-down list, select the `DEMO.CUSTOMERS` table.

  2. From the Segmentation & Activation Columns drop-down list, select the following columns:

     * `INCOME_BRACKET`

     * `REGION_CODE`

     * `STATUS`

  3. Select Finish.

  4. You need to wait until the clean room is installed before continuing with this tutorial. Periodically select Refresh until the `Tutorial` tile changes from Processing to Run.

## Run an analysis¶

Feature — Generally Available

Not available in government regions.

In this section you will run an audience overlap and segmentation analysis in
the clean room.

To run an analysis:

  1. In the left navigation, select Clean Rooms.

  2. Select the Joined tab.

  3. Find the `Tutorial` tile, and select Run.

  4. Select the `Audience Overlap & Segmentation` tile, then select Proceed.

  5. In My Tables, select `Customers`.

  6. In Collaborator Table, select `Customers`.

  7. In My Join Columns, define the following joins:

    1. From the drop-down list, select `HASHED_EMAIL`.

    2. Select \+ Join Column, then select `HASHED_FIRST_NAME` and `HASHED_LAST_NAME`.

    3. Select \+ Join Column, then select `HASHED_PHONE`.

When you run an analysis in the clean room, results will include records where
any of the following is true:

     * The `HASHED_EMAIL` in the consumer’s table matches the `HASHED_EMAIL` in the provider’s table.

     * The consumer’s `HASHED_FIRST_NAME` matches the provider’s `HASHED_FIRST_NAME` and the consumer’s `HASHED_LAST_NAME` matches the provider’s `HASHED_LAST_NAME`.

     * The consumer’s `HASHED_PHONE` matches the provider’s `HASHED_PHONE`.

  8. In the User Segmentation section, do the following:

    1. From the My Columns drop-down list, select `INCOME_BRACKET`.

    2. From the Collaborator Columns drop-down list, select `AGE_BAND`.

The results of the analysis will be grouped into these segments.

  9. In the Filters section, use the drop-down lists to define `DEMO.CUSTOMERS.STATUS = GOLD`. Be sure to use the color coding to select the column in the consumer account (`My Columns`).

The `STATUS` of a record in the consumer table must be `GOLD` in order to be
included in the analysis results.

  10. Select Run.

  11. Use the Results section to see your results. You can toggle your results metric between match rate and overlap count.

  12. To see the segmentation groups of your analysis, select Download and open the comma-delimited file.

  13. Continue to the next step in the tutorial to send enriched results back to the provider for activation.

## Activate the results¶

Feature — Generally Available

Not available in government regions.

In this section you will activate the results of your analysis by pushing them
back to the provider’s Snowflake account. These results will be enriched with
data from the consumer and provider tables.

To activate the results of the analysis:

  1. Within the Results section, select Activate.

  2. Select the name of the provider account you used to share the clean room.

  3. In the Segment Name field, specify `Provider Snowflake Account`.

  4. From the ID Columns drop-down list, select `HASHED_EMAIL`.

  5. From the Attribute Columns drop-down list, select Select All. When the provider looks at the results of the analysis, the matched records will be enriched with the additional data found in these columns.

You’ll notice that the available columns are the same as the segmentation and
activation columns that you selected as the provider when configuring the
clean room along with the segmentation and activation columns that you
selected as the consumer when installing the clean room.

  6. Select Push Data.

Congratulations! You have now installed and configured a clean room in a
consumer account, run an analysis, and pushed the results back to the provider
account for activation.

## View the activation data as the provider¶

Feature — Generally Available

Not available in government regions.

In this section, you are switching back to the role of the provider to view
the results of the consumer’s activation. Consumer activation data is stored
in the `SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.PUBLIC.PROVIDER_ACTIVATION_SUMMARY`
table of the provider’s Snowflake account.

Before using Snowsight to query this table, you must sign in to the clean room
environment to create the pipeline between the consumer account and the
provider account.

To sign in to the clean room environment as a provider:

  1. Navigate to the [Snowflake Data Clean Rooms login page](https://cleanroom.c1.us-east-1.aws.app.snowflake.com).

  2. Enter your email address, and select Continue.

  3. Enter your password.

  4. If you are associated with multiple clean room environments, select the Snowflake account you used as the provider account for this tutorial.

After the pipeline is built successfully, you can view the activation data
using a SQL query or using the database object explorer in Snowsight:

SnowsightSQL

  1. Sign in to Snowsight for the provider account. You are signing in to the Snowflake account, not the clean room environment.

  2. In the left navigation, select Data » Database.

  3. Navigate to `SAMOOHA_BY_SNOWFLAKE_LOCAL_DB` » `PUBLIC` » `Tables` » `PROVIDER_ACTIVATION_SUMMARY`.

  4. Select Data Preview to view the activation data.

  1. Sign in to Snowsight for the provider account. You are signing in to the Snowflake account, not the clean room environment.

  2. Open Projects » Worksheets.

  3. Select + » SQL Worksheet.

  4. In the new worksheet, paste and run the following statement to list the activation data that was pushed from the consumer’s clean room environment.
    
        SELECT *
       FROM samooha_by_snowflake_local_db.public.provider_activation_summary
       WHERE segment = 'Provider Snowflake Account';
    

Copy

## Clean up¶

Feature — Generally Available

Not available in government regions.

You can delete the clean room and activation data that you created for this
tutorial to clean up your production environment.

### Delete the activation data¶

To delete the activation data from the provider’s Snowflake account:

  1. Sign in to Snowsight for the provider account. You are signing in to the Snowflake account, not the clean room environment.

  2. Open Projects » Worksheets.

  3. Select + » SQL Worksheet.

  4. In the new worksheet, paste and run the following statement to delete the activation data created for this tutorial:
    
        DELETE FROM samooha_by_snowflake_local_db.public.provider_activation_summary
       WHERE segment = 'Provider Snowflake Account';
    

Copy

### Delete the clean room¶

Deleting a clean room in the provider account removes it from both the
provider account and the consumer account.

To delete a clean room:

  1. Navigate to the [Snowflake Data Clean Rooms login page](https://cleanroom.c1.us-east-1.aws.app.snowflake.com).

  2. Enter your email address, and select Continue.

  3. Enter your password.

  4. Select the Snowflake account that you used as the provider account.

  5. In the left navigation, select Clean Rooms.

  6. On the Created tab, find the `Tutorial` tile and select the More icon ([![Three vertical dots indicating more options](../../../_images/vertical-more-icon.png)](../../../_images/vertical-more-icon.png)).

  7. Select Delete.

  8. Select Proceed.

## Learn more¶

Feature — Generally Available

Not available in government regions.

Congratulations! You have now used the web app to create and share a clean
room as a provider. You have also acted as the consumer who is using the clean
room to analyze data within a privacy-preserving environment.

You can use the following resources to learn more:

  * For general information, see [About Snowflake Data Clean Rooms](../introduction).

  * For more information about the web app, see [Snowflake Data Clean Rooms: Web app overview](../web-app-introduction).

  * For information about using the developer APIs to work with a Snowflake Data Clean Room programmatically, see [Snowflake Data Clean Rooms: Developer APIs overview](../developer-introduction).

