# Sync Snowflake Notebooks with a Git repository¶

Feature — Generally Available

Generally available in Amazon Web Services (AWS), Microsoft Azure, and Google
Cloud Platform (GCP) commercial regions.

To use version control with your Snowflake Notebooks, you can sync your
notebook development with a branch in a Git repository.

You must have already set up your Snowflake account to be connected to a Git
repository and have created a branch in that repository to use for your
notebook development. See [Setting up Snowflake to use Git](../../developer-
guide/git/git-setting-up).

## Create a notebook from a file in a Git repository¶

Note

The file must be an `.ipynb` formatted file and it must use notebook format
(nbformat) 4.0 or higher.

To create a Snowflake Notebook from a file in a Git repository, do the
following:

  1. Sign in to [Snowsight](../ui-snowsight).

  2. Select Projects » Notebooks.

  3. Next to \+ Notebook, open the drop-down menu and select Create from repository.

  4. For File location in repository, select the repository and branch in the repository that contain the notebook file, then select the specific `.ipynb` file. For details on connecting Snowflake to your Git repository, see [Setting up Snowflake to use Git](../../developer-guide/git/git-setting-up).

  5. For Notebook location, select a database and schema to contain the notebook. These cannot be changed after you create the notebook.

  6. For Notebook warehouse, select a warehouse.

  7. Select Create to create a Snowflake Notebook from the `.ipynb` file in your Git repository.

## Connect an existing notebook with a Git repository¶

To connect an existing Snowflake notebook to a Git repository, do the
following:

Note

You must use a role with the following privileges at a minimum:

  * OWNERSHIP or READ privilege on the Git repository.

  * USAGE privilege on the schema that contains the Git repository.

To learn how to connect to your Git repository, see [Setting up Snowflake to
use Git](../../developer-guide/git/git-setting-up).

> For more details, see [Access control requirements](../../sql-
> reference/sql/show-git-repositories.html#label-show-git-repositories-access-
> control).

  1. Sign in to [Snowsight](../ui-snowsight).

  2. Select Projects » Notebooks and open or create a Snowflake Notebook.

  3. In the Files tab, next to the database object explorer, select Connect Git Repository.

  4. For File location in repository, select the repository and branch in the repository with which you want to sync the notebook.

  5. Select Select Folder.

  6. When you are prompted to commit and push your notebook to the Git repository, complete the Push to Git steps outlined in Push changes to a branch in a Git repository.

When your notebook is successfully pushed to the Git repository, a new folder
is created for your notebook in the selected location in the Git repository
branch, and all the files and folders in that location are synced back to your
notebook. You can select the branch name and open the repository details in
Snowflake or on Git.

## Push changes to a branch in a Git repository¶

If a Snowflake Notebook is connected to a branch in a Git repository, after
you make changes to the notebook you can push your changes to the branch.

You must use a role with the OWNERSHIP or WRITE privilege on the Git
repository to push your changes. For more details, see [Access control
requirements](../../sql-reference/sql/alter-git-repository.html#label-alter-
git-repository-access-control).

  1. Sign in to [Snowsight](../ui-snowsight).

  2. Select Projects » Notebooks and open a Snowflake Notebook.

  3. Make any relevant changes to the notebook.

  4. Select Push to Git.

  5. In the Push to Git dialog that appears, you can review the username and email address that are used to commit the changes to the specified branch and repository. If you need to update the username and email address, expand the Credentials section and update the Author name and Author email.

  6. For Commit message, enter a message to include with your commit.

  7. Expand the Credentials section to configure credentials. Enter your personal access token for the Git repository in the Personal access token field. This access token comes from the remote Git provider, such as GitHub.

     * This token is required to authenticate to the Git repository.

     * The token must have read and write access to the content of the repository for the commit to work.

     * Once entered, the token will be saved for future commits. You can update it during any future commits.

  8. Select Push.

A confirmation message states that your changes were pushed successfully to
your branch.

## Sync a notebook with a remote branch in a Git repository¶

After you connect your notebook to a branch in a Git repository, you can sync
any changes in the remote branch with your Snowflake Notebook.

  1. Sign in to [Snowsight](../ui-snowsight).

  2. Select Projects » Notebooks and open or create a Snowflake Notebook.

  3. In the database object explorer, in the Files tab, select Pull.

Snowflake fetches any changes present on the remote repository branch and
merges the notebook contents with those changes.

### Merge conflicts¶

Snowflake attempts to resolve merge conflicts that occur during a sync. If
there are merge conflicts that Snowflake isn’t able to resolve, you will get a
message to either discard your changes or commit them to a new branch. When
they are committed to a new branch, use your Git provider to manually merge
your changes from the new branch to the original branch. Then you should pull
the latest updates into your Snowflake notebook.

