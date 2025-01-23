# Using a Git repository in Snowflake¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) Feature — Generally
Available

Using a Git repository in Snowflake is not supported in the Gov region.

You can integrate your remote Git repository with Snowflake so that files from
the repository are synchronized to a special kind of stage called a repository
stage. The repository stage acts as a local Git repository with a full clone
of the remote repository, including branches, tags, and commits.

After you’ve created the repository stage, you can refer in Snowflake code to
repository files on the repository stage. For example, when creating a stored
procedure, you can import a file from the repository stage and use it as the
procedure’s handler.

With an integrated Git repository, you can do the following:

  * Fetch files from your remote Git repository to a Snowflake repository stage for use in Snowflake applications.

The files in the repository stage represent a full clone of the repository
that you can refresh as the repository changes.

  * Interact with the repository stage, viewing information about branches and tags.

  * From a repository stage synchronized from your remote repository, import files into code you execute in Snowflake.

For example, you can write procedures and user-defined functions (UDFs) whose
handler code is held by the repository stage synchronized from the repository.

  * In Snowflake, use files from any branch, tag, or commit.

## How Snowflake works with a Git repository¶

With a remote Git repository integrated with your Snowflake account, you
synchronize files from the remote repository to a repository stage in
Snowflake. To access a file in Snowflake, you refer to it on the repository
stage. For more information about using repository files, see [Use a Git
repository file as a stored procedure handler](git-examples.html#label-
integrating-git-repository-using-procedure).

![Diagram showing Git repository exchanging files with development tools and
Snowflake.](../../_images/git-architecture.png)

### Snowflake repository stage¶

A repository stage is the Snowflake representation of a repository. Like a
local Git repository, it is a full clone with all branches, tags, and commits
from the remote repository.

After repository contents are on the repository stage, you can reference files
there as you would any other file on a stage. Note that while you can execute
GET commands against a repository stage, most other ordinary stage commands
aren’t applicable to a repository stage.

You can perform operations similar to those you perform with Git commands in a
local repository, including:

  * [Fetching the repository](git-operations.html#label-git-integration-refreshing-stage) to refresh the repository stage as the repository changes.

  * [Viewing repository branches or tags](git-operations.html#label-git-integration-viewing-repositories) contained by the repository stage.

A repository stage is a special kind of stage with additional properties
specific to the repository’s integration with Snowflake. These properties
include:

  * Location of Git repository origin.

  * A secret (if needed) that contains credentials for authenticating.

  * A Snowflake API integration that specifies how Snowflake should interact with the Git API.

For more information, see [View repository stage properties](git-
operations.html#label-git-integration-viewing-repo-stage-properties).

### Git repository and development tools¶

After you integrate your repository with Snowflake, you can continue using
your development tools and local repository as before. In other words,
Snowflake becomes another client of your repository separate from your local
repository.

## Supported platforms¶

You can currently integrate Git repositories on the following Git platforms:

  * GitHub

  * GitLab

  * BitBucket

  * Azure DevOps

  * AWS CodeCommit

## References¶

  * [CREATE GIT REPOSITORY](../../sql-reference/sql/create-git-repository)

  * [ALTER GIT REPOSITORY](../../sql-reference/sql/alter-git-repository)

  * [DESCRIBE GIT REPOSITORY](../../sql-reference/sql/desc-git-repository)

  * [DROP GIT REPOSITORY](../../sql-reference/sql/drop-git-repository)

  * [SHOW GIT REPOSITORIES](../../sql-reference/sql/show-git-repositories)

  * [SHOW GIT BRANCHES](../../sql-reference/sql/show-git-branches)

  * [SHOW GIT TAGS](../../sql-reference/sql/show-git-tags)

