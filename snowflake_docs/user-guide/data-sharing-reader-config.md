# Configure a reader account¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) Provider sharing not enabled
for all accounts

Provider sharing is enabled by default for most, but not all accounts.

If you encounter errors when attempting to share data with consumers, the
feature may not be enabled for your account. To inquire about enabling it,
please contact [Snowflake Support](https://docs.snowflake.com/user-
guide/contacting-support).

A newly-created reader account contains only a single user, who serves as the
administrator for the entire account.

To “bootstrap” (i.e. configure) the account, the account administrator must
create a minimum set of additional objects in the account, including users,
custom roles (if desired), virtual warehouses, and one or more shared
databases (for the data shared by the provider account).

This topic provides an overview of all these configuration tasks, both
required and optional.

Note

Tasks 2 to 4 must be completed as the account administrator. All remaining
tasks can be delegated to other users.

Also, all of these tasks must be performed in the reader account, as opposed
to the provider account.

## Task 1: Log into the reader account as the account administrator¶

Log into the reader account using any of the supported interfaces (e.g.
SnowSQL or the web interface).

The instructions in this topic assume you are using SQL to perform these
tasks, either in SnowSQL or using a worksheet (in the web interface ).
However, the tasks can be performed in any supported Snowflake interface.

Tip

Remember to set ACCOUNTADMIN as the role to use. You can set this role either
during login or afterwards in the active session.

If you are using a worksheet (in the web interface) to perform these tasks,
set the role in the context for the worksheet.

## Task 2: Create custom roles (optional)¶

Roles enable fine-grained control over the tasks that users in the reader
account can perform. You can use roles to:

  * Specify the users who can query the data shared with the account.

  * Grant control over virtual warehouses to selected users.

  * Delegate some administrator tasks and responsibilities to selected users (if desired).

Each reader account comes with the standard, system-defined roles (SYSADMIN,
SECURITYADMIN, PUBLIC). If these roles do not meet the access requirements for
the users you will create in the account, you can create additional custom
roles.

For more details, see [Overview of Access Control](security-access-control-
overview).

## Task 3: Create users¶

Create the users who will log into the reader account and query data shared
with the account, as well as perform any other tasks you choose to allow.

As part of the user creation process, remember to grant roles, system-defined
or custom (if you created any), to the users. The roles you assign to the
users determine what they can do in the account.

For more details, see [CREATE USER](../sql-reference/sql/create-user) and
[GRANT ROLE](../sql-reference/sql/grant-role).

Tip

All remaining tasks in this topic can be completed by the account
administrator or can be delegated (through privileges and roles) to other
users in the account.

At a minimum, we recommend:

  * Grant the SECURITYADMIN role to at least one other user so that they can help create and manage other users and object access in the account.

  * Grant the SYSADMIN role to at least one other user so that they can help create and manage other objects in the account (e.g. virtual warehouses).

## Task 4: Create resource monitors (optional)¶

Virtual warehouses are required for querying data shared with the reader
account. When running, virtual warehouses consume credits, which will be
charged to your provider account.

If you wish to control the amount of credits consumed monthly by the virtual
warehouses in the reader account, create one or more resource monitors and
specify whether they control:

  * All warehouses in the account.

  * Individual warehouses.

For more details, see [CREATE RESOURCE MONITOR](../sql-reference/sql/create-
resource-monitor).

Attention

If you choose to skip this task, the warehouses in the reader account can
consume an unlimited number of credits each month, which will be charged to
your provider account.

## Task 5: Create virtual warehouses¶

To enable querying the objects in the shared database, you must create at
least one virtual warehouse. You can create as many warehouses as you like or
need; however, remember that your provider account is responsible for all
credits consumed by the warehouses in the reader account and consider the
following:

  * Set the warehouse size appropriately, weighing desired query performance against desired credit consumption.

  * Ensure the warehouse is set to auto-suspend when not in use.

For more details, see [CREATE WAREHOUSE](../sql-reference/sql/create-
warehouse).

## Task 6: Create a database from each share shared with the account¶

A reader account does not contain any data by default. To consume data shared
from your provider account, you must use the [CREATE DATABASE](../sql-
reference/sql/create-database) command to create a database from each share
shared with the account. When you create the database(s), you specify the name
that other users in the reader account will reference when querying the shared
data.

For example, if your provider account is named `ab12345` and you shared two
shares named `share1` and `share2` with this reader account:

>
>     CREATE DATABASE shared_db1 FROM SHARE ab12345.share1;
>  
>     CREATE DATABASE shared_db2 FROM SHARE ab12345.share2;
>  
>
> Copy

## Task 7: Grant privileges on virtual warehouses and databases to roles¶

Data providers can choose to add objects to a share by either granting
privileges on the objects to a share via a database role, and then granting
the database role to a share (Option 1) or granting privileges on the objects
directly to the share (Option 2). The instructions in this section differ
depending on the option a database provider chose:

Option 1:

    

To enable querying data shared with the reader account, grant a database role
in the share that aligns with a business function in your account with the
appropriate role in your account. For example, suppose the share includes a
database role named `shared_db1.dr1` that you want to share with every user in
your account. In this case, you would grant the database role to the PUBLIC
system role:

    
    
    GRANT DATABASE ROLE shared_db1.dr1 TO ROLE PUBLIC;
    

Copy

Option 2:

    

To enable querying data shared with the reader account, grant the following
privileges to the other roles, system-defined or custom (if any), in the
account:

  * IMPORTED PRIVILEGES on each database created from the share(s) in Task 6: Create a database from each share shared with the account (in this topic).

For example, the following commands grant the necessary privileges for two
databases named `shared_db1` and `shared_db2`, and a warehouse named
`testing_vw`, to the PUBLIC role. Because all users in the account
automatically have the PUBLIC role, this enables any user in the account to
use the warehouse and query the databases:

    
    
    GRANT IMPORTED PRIVILEGES ON DATABASE shared_db1 TO ROLE PUBLIC;
    
    GRANT IMPORTED PRIVILEGES ON DATABASE shared_db2 TO ROLE PUBLIC;
    

Copy

In addition, grant the USAGE privilege on a virtual warehouse you created for
executing queries:

    
    
    GRANT USAGE ON WAREHOUSE testing_vw TO ROLE PUBLIC;
    

Copy

You can grant additional privileges if desired; however, the privileges listed
above are the minimum privileges required to query the shared databases in the
account.

In addition, you could grant full privileges on the `testing_vw` warehouse to
the SYSADMIN role, enabling users with the role to start, stop, and resize the
warehouse:

    
    
    GRANT ALL ON WAREHOUSE testing_vs TO ROLE SYSADMIN;
    

Copy

For more details, see [GRANT <privileges>](../sql-reference/sql/grant-
privilege).

## Task 8: Invite users to log in and reset their passwords¶

As the last configuration task, notify all the users you created that the
account is available to use.

The fastest/easiest way to do this is to use the [ALTER USER](../sql-
reference/sql/alter-user) command to reset the password for each user. This
generates a unique URL for each user, which you then send/give to them. They
use the URL to change their password and log into the account.

For example:

>
>     ALTER USER ra_user1 RESET PASSWORD;
>  
>     ALTER USER ra_user2 RESET PASSWORD;
>  
>
> Copy

Important

Each URL can be used only once and expires after 4 hours. However, you can
reset the password for a user as often as needed.

For more details, see [ALTER USER](../sql-reference/sql/alter-user).

