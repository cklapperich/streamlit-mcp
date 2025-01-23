# Git operations in Snowflake¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) Feature — Generally
Available

Using a Git repository in Snowflake is not supported in the Gov region.

This topic describes how to perform common repository operations.

## Integrate a Git repository with your Snowflake account¶

For information about setting up an integration with a Git repository, see
[Setting up Snowflake to use Git](git-setting-up).

## Refresh a repository stage from the repository¶

You can refresh the repository stage with a full clone that fetches all
branches, tags, and commits from the remote repository. When you do so, you
also prune branches and commits that were fetched earlier but no longer exist
in the remote repository.

To perform the operations described in this section, you’ll need the Snowflake
access described in [Access control for ALTER GIT REPOSITORY](../../sql-
reference/sql/alter-git-repository.html#label-alter-git-repository-access-
control).

You can refresh your repository stage using either Snowsight or SQL.

SQLSnowsight

When you want to refresh your repository stage, you can fetch contents of the
integrated Git repository to the repository stage by using the [ALTER GIT
REPOSITORY](../../sql-reference/sql/alter-git-repository) command.

Code in the following example updates the repository stage with the contents
of the repository:

    
    
    ALTER GIT REPOSITORY snowflake_extensions FETCH;
    

Copy

You can use Snowsight to refresh the repository stage (which contains a clone
of the remote repository) from the remote repository.

  1. Sign in to Snowsight.

  2. In the navigation menu, select Data » Databases.

  3. In the object explorer, select the database and schema that contain the Git repository stage you want to refresh.

  4. Inside the schema, open Git Repositories.

  5. In Git Repositories, select the repository to view the details page.

  6. In the repository details, on the Files Explorer tab, select the Fetch button to refresh the repository stage.

## View a list of repository branches or tags¶

You can view a list of branches and tags available in the repository stage
that represents a clone of your Git repository.

To perform the operations described in this section, you’ll need the Snowflake
access described in the following topics:

  * For listing branches: [Access control for SHOW GIT BRANCHES](../../sql-reference/sql/show-git-branches.html#label-show-git-branches-access-control)

  * For listing tags: [Access control for SHOW GIT TAGS](../../sql-reference/sql/show-git-tags.html#label-show-git-tags-access-control)

You can view a list of branches or tags using either Snowsight or SQL.

SQLSnowsight

You can view branches and tags by using the [SHOW GIT BRANCHES](../../sql-
reference/sql/show-git-branches) and [SHOW GIT TAGS](../../sql-
reference/sql/show-git-tags) commands.

The following example generates output that lists branches in the Git
repository `snowflake_extensions`:

    
    
    SHOW GIT BRANCHES IN snowflake_extensions;
    

Copy

The preceding command generates output similar to the following:

    
    
    --------------------------------------------------------------------------------
    | name | path           | checkouts | commit_hash                              |
    --------------------------------------------------------------------------------
    | main | /branches/main |           | 0f81b1487dfc822df9f73ac6b3096b9ea9e42d69 |
    --------------------------------------------------------------------------------
    

You can use Snowsight to view a list of the files in your Git repository.

  1. Sign in to Snowsight.

  2. In the navigation menu, select Data » Databases.

  3. In the object explorer, select the database and schema that contain the Git repository stage you want to view.

  4. Inside the schema, open Git Repositories.

  5. Locate and select the repository to view its details page.

  6. In the repository’s details page, on the Files Explorer tab, select the Branch button.

  7. From the Branch drop-down menu, do one of the following:

     * To view a list of branches cloned from the repository, select Branches .

     * To view a list of the tags cloned from the repository, select Tags.

## View a list of repository files¶

You can view a list of files in a branch, tag, or commit using either
Snowsight or SQL.

SQLSnowsight

You can view a list of files in the repository by using the [LIST](../../sql-
reference/sql/list) command in the following forms (you can abbreviate LIST to
LS):

  * List by branch name:
    
        LS @repository_stage_name/branches/branch_name;
    

Copy

  * List by tag name:
    
        LS @repository_stage_name/tags/tag_name;
    

Copy

  * List by commit hash:
    
        LS @repository_stage_name/commits/commit_hash;
    

Copy

The following example generates output that lists files in the main branch of
the Git repository `snowflake_extensions`:

    
    
    LS @snowflake_extensions/branches/main;
    

Copy

The preceding command generates output similar to the following:

    
    
    -------------------------------------------------------------------------------------------------------------------------------------------------------
    | name                                                         | size | md5 | sha1                                     | last_modified                |
    -------------------------------------------------------------------------------------------------------------------------------------------------------
    | snowflake_extensions/branches/main/.gitignore                | 10   |     | e43b0f988953ae3a84b00331d0ccf5f7d51cb3cf | Wed, 5 Jul 2023 22:42:34 GMT |
    -------------------------------------------------------------------------------------------------------------------------------------------------------
    | snowflake_extensions/branches/main/python-handlers/filter.py | 169  |     | c717137b18d7b75005849d76d89037fafc7b5223 | Wed, 5 Jul 2023 22:42:34 GMT |
    -------------------------------------------------------------------------------------------------------------------------------------------------------
    

You can use Snowsight to view a list of the branches and tags in your Git
repository.

  1. Sign in to Snowsight.

  2. In the navigation menu, select Data » Databases.

  3. In the object explorer, select the database and schema that contain the Git repository stage you want to view.

  4. Inside the schema, open Git Repositories.

  5. Inside Git Repositories, select a repository to view its details page.

  6. In the repository’s details page, on the Files Explorer tab, select the Branch button.

  7. From the Branch drop-down menu, select one of the following:

     * To view a list of branches cloned from the repository, select Branches.

     * To view a list of the tags cloned from the repository, select Tags.

  8. Select the branch or tag whose files you want to list.

  9. Below the repository name, view the list of folders and files corresponding to the selection you made.

## View repository stage properties¶

You can view the properties associated with a repository stage.

To perform the operations described in this section, you’ll need the Snowflake
access described in [Access control for DESC GIT REPOSITORY](../../sql-
reference/sql/desc-git-repository.html#label-desc-git-repository-access-
control).

You can view repository stage properties by using either Snowsight or SQL.

SQLSnowsight

You can view repository stage properties by using the SQL commands [SHOW GIT
REPOSITORIES](../../sql-reference/sql/show-git-repositories) and [DESCRIBE GIT
REPOSITORY](../../sql-reference/sql/desc-git-repository).

The properties information includes the Git origin URL, name of the API
integration and credentials (specified as a [secret](../../sql-
reference/sql/create-secret)) used to connect with the remote repository, and
so on.

    
    
    DESCRIBE GIT REPOSITORY snowflake_extensions;
    

Copy

The preceding command generates output similar to the following:

    
    
    --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    | CREATED_ON                    | NAME                 | DATABASE_NAME | SCHEMA_NAME | ORIGIN                                                 | API_INTEGRATION     | GIT_CREDENTIALS           | OWNER        | OWNER_ROLE_TYPE | COMMENT |
    --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    | 2023-06-28 08:46:10.886 -0700 | SNOWFLAKE_EXTENSIONS | MY_DB         | MAIN        | https://github.com/my-account/snowflake-extensions.git | GIT_API_INTEGRATION | MY_DB.MAIN.GIT_SECRET     | ACCOUNTADMIN | ROLE            |         |
    --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    

You can use Snowsight to view repository properties.

  1. Sign in to Snowsight.

  2. In the navigation menu, select Data » Databases.

  3. In the object explorer, select the database and schema that contain the Git repository stage you want to view.

  4. Inside the schema, open Git Repositories.

  5. Inside Git Repositories, select a repository to view its details page.

  6. In the repository’s details page, select the Git Repository Details tab to view information that includes the following:

     * The repository’s origin

     * The [API integration](git-setting-up.html#label-integrating-git-repository-api-integration) and credentials (specified as a [secret](../../sql-reference/sql/create-secret)) used by Snowflake to interact with the remote repository

     * Privileges granted on the repository stage

## Execute code from a repository¶

You can execute the code contained by a file from the repository.

To perform the operations described in this section, you’ll need the Snowflake
access described in [Access control for EXECUTE IMMEDIATE FROM](../../sql-
reference/sql/execute-immediate-from.html#label-execute-immediate-from-
privilege-errors).

You can execute code by using either Snowsight or SQL.

SQLSnowsight

You can use [EXECUTE IMMEDIATE FROM](../../sql-reference/sql/execute-
immediate-from) to execute code in a repository stage.

Code in the following example executes code in `create-database.sql` from the
repository stage `snowflake_extensions`:

    
    
    EXECUTE IMMEDIATE FROM @snowflake_extensions/branches/main/sql/create-database.sql;
    

Copy

You can use Snowsight to execute SQL code from a Git repository.

Note that when you execute code this way, you won’t see output generated by
the code’s execution.

  1. Sign in to Snowsight.

  2. In the navigation menu, select Data » Databases.

  3. In the object explorer, select the database and schema that contain the Git repository stage you want to view.

  4. Inside the schema, open Git Repositories.

  5. Inside Git Repositories, select a repository to view its details page.

  6. In the repository’s details page, on the Files Explorer tab, select the Branch button.

  7. From the Branch drop-down menu, select one of the following:

     * Branches to view a list of branches cloned from the repository.

     * Tags to view a list of the tags cloned from the repository.

  8. Select the branch or tag containing the file whose code you want to execute.

  9. Beneath the repository name, select the folder containing the file you want to execute.

  10. Locate the file whose code you want to execute, and select [![More options](../../_images/snowsight-worksheet-explorer-ellipsis.png)](../../_images/snowsight-worksheet-explorer-ellipsis.png) » Execute immediate.

  11. In the box that appears, review the code contained by the file.

This is the code that Snowflake will execute.

  12. To execute the displayed code, select Execute Immediate.

The details page displays a notification that the code’s execution was
started. It later indicates whether the execution succeeded or failed.

## Copy repository-based code into a worksheet¶

You can quickly copy code from a repository file into a worksheet. You can
edit and run the copied code or use it as a read-only template for other
users.

You can copy the content of the following types of files: `.sql` and `.py`.

To save your changes in your repository, you need to copy the edited code from
the worksheet into a file (such as the file corresponding to the one you
copied from) in your local Git repository and commit the changes from there.

Snowsight:

    

You can use Snowsight to copy content from a file in your repository into a
worksheet.

  1. Sign in to Snowsight.

  2. In the navigation menu, select Data » Databases.

  3. In the object explorer, select the database and schema that contain the Git repository stage you want to view.

  4. Inside the schema, open Git Repositories.

  5. Inside Git Repositories, select a repository to view its details page.

  6. In the repository’s details page, on the Files Explorer tab, select the Branch button.

  7. From the Branch drop-down menu, do one of the following:

     * To view a list of branches cloned from the repository, select Branches.

     * To view a list of the tags cloned from the repository, select Tags.

  8. Select the branch or tag containing the file whose code you want to copy.

  9. Beneath the repository name, select the folder containing the file you want to execute.

  10. Locate the file whose code you want to execute, and select [![More options](../../_images/snowsight-worksheet-explorer-ellipsis.png)](../../_images/snowsight-worksheet-explorer-ellipsis.png) » Copy into worksheet.

Snowflake copies code from the file you selected into a new worksheet.

