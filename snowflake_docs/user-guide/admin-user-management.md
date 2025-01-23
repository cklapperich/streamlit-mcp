# User management¶

User administrators can create and manage Snowflake users through SQL or the
web interface:

  * Using SQL, administrators can perform all user-related tasks, including changing login credentials and defaults for users.

  * Snowsight supports most user-related tasks.

  * Classic Console doesn’t support all user-related tasks, but provides a wizard for creating users and performing most common activities, such as resetting a user’s password.

## Privileges required to create and modify users¶

The following roles or privileges are required to manage users in your
account:

Create users:

    

The USERADMIN system role can create users using SQL ([CREATE USER](../sql-
reference/sql/create-user)).

If you prefer to use a custom role for this purpose, grant the CREATE USER
privilege on the account to this role.

Modify users:

    

Only the role with the OWNERSHIP privilege on a user can modify most user
properties using SQL ([ALTER USER](../sql-reference/sql/alter-user)).

## Password policies¶

A password policy specifies the requirements that must be met to create and
reset a password to authenticate to Snowflake.

Snowflake provides two options for password policies:

  * A built-in password policy to facilitate the initial user provisioning process.

  * A schema-level password policy object that can be set at the level of the Snowflake account, an individual user, or both depending on the use cases and needs of the user administrator.

For details on best practices and each of the password policy options, see:

  * Best practices for password policies and passwords

  * Snowflake-provided password policy

  * Custom password policy for the account and users

### Best practices for password policies and passwords¶

Snowflake recommends the following best practices regarding passwords and
password policies:

Create and enforce the custom password policy

    

The password policy object is enforced once the password policy is set on an
account or user.

Set these properties to values that meet your internal security needs. For
details, see Step 4: Create a password policy (in this topic):

  * `PASSWORD_HISTORY` to ensure users cannot reuse passwords too frequently and to help prevent brute force attacks to determine the password for a user.

  * `PASSWORD_MIN_AGE_DAYS` to require the user to use the new password. A value of 0 is not recommended because the user can change the password to exhaust the password history and reuse the original password value too soon.

To require the user to change their password to meet the password policy on
their initial or next login to Snowflake, set the `MUST_CHANGE_PASSWORD`
property on the user to `TRUE` using an [ALTER USER](../sql-
reference/sql/alter-user) command.

For details, see Step 6: Require a password change (in this topic).

Require strong passwords

    

Define an account-level password policy to require strong passwords.

A strong password has at least 8 characters and includes a combination of
uppercase and lowercase letters, special characters (e.g. `!` and `*`), and
numbers.

MFA

    

Use [Multi-factor authentication (MFA)](security-mfa) for additional security.

Using SCIM

    

You can set a password for the user to access Snowflake in a SCIM API request.
SCIM administrators and user administrators should choose to manage the user
password to access Snowflake in either your identity provider or using a
password policy in Snowflake.

Currently, users provisioned to Snowflake with SCIM are required to have their
password meet the default Snowflake password policy. This requirement can be
bypassed if you choose to use this password policy feature.

To bypass the default password policy requirement, follow the instructions in
the Using Password Policies section (in this topic).

Monitoring passwords

    

To monitor passwords:

  * Query the Snowflake Account Usage [USERS](../sql-reference/account-usage/users) view to determine whether the `HAS_PASSWORD` column value returns `TRUE` for a given user.

  * Query the Snowflake Account Usage [LOGIN_HISTORY](../sql-reference/account-usage/login_history) view and evaluate the `FIRST_AUTHENTICATION_FACTOR` column. If a user does not require a password to access Snowflake, execute an [ALTER USER](../sql-reference/sql/alter-user) command to set the `password` property to NULL.

### Snowflake-provided password policy¶

A password can be any case-sensitive string up to 256 characters, including
blank spaces and special (i.e. non-alphanumeric) characters, such as
exclamation points (`!`), percent signs (`%`), and asterisks (`*`).

During the initial user creation, it is possible to set a weak password for
the user that does not meet the minimum requirements described below (e.g.
`'test12345'`). This feature allows administrators the option to use generic
passwords for the user during the creation process. If this pathway is chosen,
Snowflake strongly recommends setting the `MUST_CHANGE_PASSWORD` property to
`TRUE` to require users to change their password on their next login,
including the initial login, to Snowflake.

Additionally, Snowflake allows creating users without an initial password to
support business processes in which new users are not allowed to log into the
system. If this occurs, the user’s `PASSWORD` property value will be `NULL`.
However, as a general rule, Snowflake expects that users are created with
initial passwords.

In the context of resetting an existing password (e.g. change `'test12345'` to
`'q@-*DaC2yjZoq3Re4JYX'`), Snowflake enforces the following password policy as
a minimum requirement while using the [ALTER USER](../sql-reference/sql/alter-
user) command and the web interface:

  * Must be at least 8 characters long.

  * Must contain at least 1 digit.

  * Must contain at least 1 uppercase letter and 1 lowercase letter.

Snowflake strongly recommends the following guidelines for creating the
strongest passwords possible:

  * Create a unique password for Snowflake (i.e. do not reuse passwords from other systems or accounts).

  * Use more than 8 characters.

  * Include multiple, random mixed-case letters, numbers, and special characters, including blank spaces.

  * Do not use easily-guessed common passwords, names, numbers, or dates.

Finally, to configure the highest level of security for user login, Snowflake
recommends that users [enroll in MFA](ui-preferences).

### Custom password policy for the account and users¶

The custom password policy is a schema-level object that specifies the
requirements that must be met to create and reset a password to authenticate
to Snowflake, including the number of attempts to enter the password
successfully and the number of minutes before a password can be retried (i.e.
the “lockout” time).

The password policy requirements for a password include upper or lowercase
letters, special characters, numbers, and password length to meet security
requirements for users and clients to authenticate to Snowflake. Password
policies that require strong passwords help to meet security guidelines and
regulations.

Snowflake supports setting a password policy for your Snowflake account and
for individual users. Only one password policy can be set at any given time
for your Snowflake account or a user. If a password policy exists for the
Snowflake account and another password policy is set for a user in the same
Snowflake account, the user-level password policy takes precedence over the
account-level password policy.

The password policy applies to new passwords that are set in your Snowflake
account. To ensure that users with existing passwords meet the password policy
requirements, require users to change their password during their next login
to Snowflake as shown in Step 6: Require a password change (in this topic).

Note

Most password policy property changes take effect the next time a user changes
their password. For example, if you change the `PASSWORD_MAX_LENGTH` property
from `10` to `16` to require the user to use a longer password then the user
must comply with the password policy change whenever they change their
password. You can set the user property `MUST_CHANGE_PASSWORD` to `TRUE` with
an [ALTER USER](../sql-reference/sql/alter-user) statement to require the user
to change their password on their next login to Snowflake.

However, some password policy property changes take effect during the next
login because Snowflake does not force the user to change their password in
their current session:

  * `PASSWORD_MAX_AGE_DAYS = _integer_`

  * `PASSWORD_MAX_RETRIES = _integer_`

  * `PASSWORD_LOCKOUT_TIME_MINS = _integer_`

Any changes to these properties do not affect the current session. For
example, a change to the value of the `PASSWORD_MAX_AGE_DAYS` property does
not cause the user’s current password to expire. However, during the next
login to Snowflake, the user must change their password.

#### Considerations¶

  * [Future grants](../sql-reference/sql/grant-privilege.html#label-grant-privilege-schema-future-grants) of privileges on password policies are not supported.

As a workaround, grant the APPLY PASSWORD POLICY privilege to a custom role to
allow that role to apply password policies on the user or the Snowflake
account.

  * The password policy can be managed with SQL using either [SnowSQL](snowsql) or a supported [driver or connector](../guides-overview-connecting), or in Worksheets using the Classic Console or [Snowsight](ui-snowsight).

  * Resetting or changing a password:

    * Classic Console, SnowSQL, and supported connectors and drivers:

When executing an [ALTER USER](../sql-reference/sql/alter-user) command or
using the Classic Console to reset or change a password, Snowflake evaluates
the password policy to ensure that the newly created password matches the
password policy requirements.

  * Tracking password policy usage:

    * Query the Account Usage [PASSWORD_POLICIES](../sql-reference/account-usage/password_policies) view to return a row for each password policy in your Snowflake account.

    * Use the Information Schema table function [POLICY_REFERENCES](../sql-reference/functions/policy_references) to return a row for each user that is assigned to the specified password policy and a row for the password policy assigned to the Snowflake account.

Currently, only the following syntax is supported for password policies:

> >         POLICY_REFERENCES( POLICY_NAME => '<password_policy_name>' )
>  
>
> Copy

Where `_password_policy_name_` is the fully qualified name of the password
policy.

For example, execute the following query to return a row for each user that is
assigned the password policy named `password_policy_prod_1`, which is stored
in the database named `my_db` and the schema named `my_schema`:

> >         SELECT *
>         FROM TABLE(
>             my_db.information_schema.policy_references(
>               POLICY_NAME => 'my_db.my_schema.password_policy_prod_1'
>           )
>         );
>  
>
> Copy

### Using password policies¶

The following steps are a representative guide to define and set a password
policy in Snowflake.

These steps assume a centralized management approach in which a custom role
named `policy_admin` owns the password policy (i.e. has the OWNERSHIP
privilege on the password policy) and is responsible for setting the password
policy on an account or user (i.e. has the global APPLY PASSWORD POLICY
privilege, as shown in step 2).

Note

To set a policy on an account, the `policy_admin` custom role must also have
the USAGE privilege on the database and schema that contain the password
policy.

For more information, see: [Access control privileges](security-access-
control-privileges)

#### Step 1: Create the custom role¶

Create a custom role that allows creating and managing password policies.
Throughout this topic, the example custom role is named `policy_admin`,
although the role could have any appropriate name.

If the custom role already exists, continue to the next step.

Otherwise, create the `policy_admin` custom role.

>
>     USE ROLE USERADMIN;
>  
>     CREATE ROLE policy_admin;
>  
>
> Copy

#### Step 2: Grant privileges to the custom role¶

If the `policy_admin` custom role does not already have the following
privileges, grant these privileges as shown below:

  * USAGE on the database and schema that will contain the password policy.

  * CREATE PASSWORD POLICY on the schema that will store the password policy.

  * APPLY PASSWORD POLICY on the account.

    
    
    USE ROLE SECURITYADMIN;
    
    GRANT USAGE ON DATABASE security TO ROLE policy_admin;
    
    GRANT USAGE ON SCHEMA security.policies TO ROLE policy_admin;
    
    GRANT CREATE PASSWORD POLICY ON SCHEMA security.policies TO ROLE policy_admin;
    
    GRANT APPLY PASSWORD POLICY ON ACCOUNT TO ROLE policy_admin;
    

Copy

If you decide to set a password policy on a user, grant the APPLY PASSWORD
POLICY privilege on the user. For example, if the username is `JSMITH`,
execute the following command.

>
>     GRANT APPLY PASSWORD POLICY ON USER jsmith TO ROLE policy_admin;
>  
>
> Copy

For more information, see Summary of DDL commands, operations, and privileges.

#### Step 3: Grant the custom role to a user¶

Grant the `policy_admin` custom role to the users responsible for managing
password policies.

    
    
    USE ROLE SECURITYADMIN;
    GRANT ROLE policy_admin TO USER jsmith;
    

Copy

For more information, see [Configuring access control](security-access-
control-configure)

#### Step 4: Create a password policy¶

Using the `policy_admin` custom role, create a password policy named
`password_policy_prod_1`. For more information, see [CREATE PASSWORD
POLICY](../sql-reference/sql/create-password-policy).

>
>     USE ROLE policy_admin;
>  
>     USE SCHEMA security.policies;
>  
>     CREATE PASSWORD POLICY PASSWORD_POLICY_PROD_1
>         PASSWORD_MIN_LENGTH = 12
>         PASSWORD_MAX_LENGTH = 24
>         PASSWORD_MIN_UPPER_CASE_CHARS = 2
>         PASSWORD_MIN_LOWER_CASE_CHARS = 2
>         PASSWORD_MIN_NUMERIC_CHARS = 2
>         PASSWORD_MIN_SPECIAL_CHARS = 2
>         PASSWORD_MIN_AGE_DAYS = 1
>         PASSWORD_MAX_AGE_DAYS = 999
>         PASSWORD_MAX_RETRIES = 3
>         PASSWORD_LOCKOUT_TIME_MINS = 30
>         PASSWORD_HISTORY = 5
>         COMMENT = 'production account password policy';
>  
>
> Copy
>
> Note
>
> The property `PASSWORD_MAX_AGE_DAYS` is set to the largest value, 999.
> Choose a value that aligns with your internal guidelines. For details, see
> [CREATE PASSWORD POLICY](../sql-reference/sql/create-password-policy).

#### Step 5: Set the password policy on the account or an individual user¶

Set the policy on an account with the [ALTER ACCOUNT](../sql-
reference/sql/alter-account) command:

>
>     ALTER ACCOUNT SET PASSWORD POLICY
> security.policies.password_policy_prod_1;
>  
>
> Copy

If you decide to create an additional password policy for one or more users,
set the user-level password policy on a user with an [ALTER USER](../sql-
reference/sql/alter-user) command:

>
>     ALTER USER jsmith SET PASSWORD POLICY
> security.policies.password_policy_user;
>  
>
> Copy

Important

To replace a password policy that is already set for an account or user, unset
the password policy first and then set the new password policy for the account
or user. For example:

>
>     ALTER ACCOUNT UNSET PASSWORD POLICY;
>  
>     ALTER ACCOUNT SET PASSWORD POLICY
> security.policies.password_policy_prod_2;
>  
>
> Copy

#### Step 6: Require a password change¶

Set the `MUST_CHANGE_PASSWORD` property to `TRUE` for individual users using
an [ALTER USER](../sql-reference/sql/alter-user) statement to require the
users to change their password to meet the password policy on their next login
to Snowflake.

>
>     ALTER USER JSMITH SET MUST_CHANGE_PASSWORD = true;
>  
>
> Copy

#### Step 7: Replicate the password policy to a target account¶

A password policy and its references (i.e. assignments to a user or the
account) can be replicated from the source account to the target account using
database replication and account replication. For details, refer to:

  * [Account replication](account-replication-considerations.html#label-account-replication-considerations-security-policies).

  * [Database replication](database-replication-considerations.html#label-database-replication-considerations-masking-row-policies).

### Managing password policies¶

Snowflake provides the following set of privileges and DDL to manage password
policies:

Snowflake provides the following DDL commands to manage password policy
objects:

  * [CREATE PASSWORD POLICY](../sql-reference/sql/create-password-policy)

  * [ALTER PASSWORD POLICY](../sql-reference/sql/alter-password-policy)

  * [DROP PASSWORD POLICY](../sql-reference/sql/drop-password-policy)

  * [SHOW PASSWORD POLICIES](../sql-reference/sql/show-password-policies)

  * [DESCRIBE PASSWORD POLICY](../sql-reference/sql/desc-password-policy)

The USAGE privilege on the parent database and schema are required to perform
operations on any object in a schema.

Privilege | Usage  
---|---  
CREATE PASSWORD POLICY | Enables creating a new password policy.  
APPLY PASSWORD POLICY | Enables applying a password policy at the account or user level.  
OWNERSHIP | Grants full control over the password policy. Required to alter most properties of a password policy.  
  
### Summary of DDL commands, operations, and privileges¶

The following table summarizes the relationship between the password policy
DDL operations and their necessary privileges.

The USAGE privilege on the parent database and schema are required to perform
operations on any object in a schema.

Operation | Privilege required  
---|---  
Create password policy | A role with the CREATE PASSWORD POLICY privilege on the schema to store the password policy.  
Alter password policy | A role with the OWNERSHIP privilege on the password policy.  
Drop password policy | A role with the OWNERSHIP privilege on the password policy.  
Describe password policy | A role with the OWNERSHIP privilege on the password policy or . the APPLY PASSWORD POLICY privilege on the account.  
Show password policies | A role with the OWNERSHIP privilege on the password policy or . the APPLY PASSWORD POLICY privilege on the account.  
Set & unset password policy | A role with the APPLY PASSWORD POLICY privilege on the account or the user.  
  
## User roles¶

Snowflake uses roles to control the objects (virtual warehouses, databases,
tables, etc.) that users can access:

  * Snowflake provides a set of predefined roles, as well as a framework for defining a hierarchy of custom roles.

  * All Snowflake users are automatically assigned the predefined PUBLIC role, which enables login to Snowflake and basic object access.

  * In addition to the PUBLIC role, each user can be assigned additional roles, with one of these roles designated as their _default role_. A user’s default role determines the role used in the Snowflake sessions initiated by the user; however, this is only a default. Users can change roles within a session at any time.

  * Roles can be assigned at user creation or afterwards.

Attention

When deciding the additional roles to assign to a user, as well as designating
their default role, consider the following for the predefined ACCOUNTADMIN
role (required for performing account-level administrative tasks):

  * Snowflake recommends strictly controlling the assignment of ACCOUNTADMIN, but recommends assigning it to at least two users.

  * ACCOUNTADMIN should never be designated as a user’s default role. Instead, designate a lower-level administrative or custom role as their default.

For more details and best practices related to the ACCOUNTADMIN role, see
[Access control considerations](security-access-control-considerations). For
more general information about roles, see [Overview of Access
Control](security-access-control-overview).

## Creating users¶

You can create a user by using the following interfaces.

Note

The web interface, whether you use Classic Console or Snowsight, requires that
you specify a password when you create a user. The [CREATE USER](../sql-
reference/sql/create-user) command and [UserCollection.create](/developer-
guide/snowflake-python-
api/reference/latest/_autosummary/snowflake.core.user.UserCollection#snowflake.core.user.UserCollection.create)
Python API do not.

For more information about passwords in Snowflake, see Password Policies (in
this topic)

### Using Snowsight¶

  1. Sign in to Snowsight.

  2. Select Admin » Users & Roles.

  3. Select \+ User.

  4. In the User Name field, enter a unique identifier for the user. The user uses this identifier to sign in to Snowflake unless you specify a login name.

  5. Optionally specify an email address for the user in the Email field.

  6. In the Password and Confirm Password fields, enter the password for the user.

  7. Optionally add a comment explaining why you created the user.

  8. Leave the Force user to change password on first time login checkbox selected to force the user to change their password when they sign in.

  9. Optionally select Advanced User Options to specify additional details about the user:

     * Login Name to use instead of the User Name when signing in to Snowflake.

     * Display Name that appears after signing in.

     * First Name and Last Name to complete the user profile.

     * Default Role, Default Warehouse, and Default Namespace.

  10. Select Create User.

### Using Classic Console¶

  1. Select Account [![Account tab](../_images/ui-navigation-account-icon.svg)](../_images/ui-navigation-account-icon.svg) » Users.

  2. Select Create.

  3. In the User Name field, enter a unique identifier for the user.

> Note
>
> User name is the unique identifier for the user in Snowflake. It is not the
> user’s login name (i.e. the name the user enters when logging into
> Snowflake). Snowflake allows users to have different user names and login
> names, if desired. You specify a login name for the user on the next screen.

  4. In the Password and Confirm Password fields, enter the password for the user.

  5. Leave the Force Password Change checkbox selected to force the user to change their password on their next login; otherwise, clear the checkbox.

  6. Select Next. The Advanced screen opens.

  7. Optionally enter the Login Name, Display Name, and personal information for the user.

> Note
>
> Users require a login name to log into Snowflake; if you don’t explicitly
> provide a login name, Snowflake uses their user name as the login name.

  8. Select Next. The Preferences screen opens.

  9. Optionally enter defaults for the user:

     * Virtual warehouse

     * Namespace in the form of `_db_name_` or `_db_name_._schema_name_`

     * Role

  10. Select Finish. Snowflake displays a success message.

### Using SQL¶

Use the [CREATE USER](../sql-reference/sql/create-user) command to create a
user.

Important

When creating a user, if you assign a default role to the user, you must then
explicitly grant this role to the user. For example:

>
>     CREATE USER janesmith PASSWORD = 'abc123' DEFAULT_ROLE = myrole
> MUST_CHANGE_PASSWORD = TRUE;
>  
>     GRANT ROLE myrole TO USER janesmith;
>  
>
> Copy

Note that the [GRANT ROLE](../sql-reference/sql/grant-role) command allows you
to assign multiple roles to a single user. The web interface does not
currently support the same capability.

### Using Python¶

Use the [UserCollection.create](/developer-guide/snowflake-python-
api/reference/latest/_autosummary/snowflake.core.user.UserCollection#snowflake.core.user.UserCollection.create)
Python API to create a user.

Important

When creating a user, if you assign a default role to the user, you must then
explicitly grant this role to the user. For example:

>
>     from snowflake.core.user import Securable, User
>  
>     my_user = User(
>       name="janesmith",
>       password="abc123",
>       default_role="myrole",
>       must_change_password=True)
>     root.users.create(my_user)
>  
>     root.users['janesmith'].grant_role(role_type="ROLE",
> role=Securable(name='myrole'))
>  
>
> Copy

## Resetting the password for a user¶

Administrators can change a user’s password through the following interfaces.

### Using Snowsight¶

  1. Sign in to Snowsight.

  2. Select Admin » Users & Roles.

  3. Locate the user whose password you want to change and select [![More options](../_images/snowsight-worksheet-explorer-ellipsis.png)](../_images/snowsight-worksheet-explorer-ellipsis.png) » Reset Password.

  4. Enter a new password for the user and confirm the password.

  5. Select Update.

### Using Classic Console¶

Note

Users can only change their own password through Classic Console. For more
information, see [Changing Your Password / Switching Your (Session) Role /
Logging Out](ui-menu).

  1. Select Account [![Account tab](../_images/ui-navigation-account-icon.svg)](../_images/ui-navigation-account-icon.svg) » Users.

  2. Click a user row to select it, then select Reset Password. The Reset Password dialog opens.

  3. Enter the new password for the user, and confirm the password.

  4. Leave the Force Password Change checkbox selected to force the user to change their password on their next login; otherwise, clear the checkbox.

  5. Select Finish.

### Using SQL¶

Use the [ALTER USER](../sql-reference/sql/alter-user) command to input a
user’s password. For example:

>
>     ALTER USER janesmith SET PASSWORD =
> 'H8MZRqa8gEe/kvHzvJ+Giq94DuCYoQXmfbb$Xnt' MUST_CHANGE_PASSWORD = TRUE;
>  
>
> Copy

Alternatively, use the ALTER USER … RESET PASSWORD syntax to generate a URL to
share with the user. The URL opens a web page on which the user can enter the
new password. For example:

>
>     ALTER USER janesmith RESET PASSWORD;
>  
>
> Copy
>
> Note
>
>   * The generated URL is valid for one use only and expires after 4 hours.
>
>   * Executing the ALTER USER … RESET PASSWORD statement does not invalidate
> the current password. The user can continue to use the old password until
> the new password is set.
>
>

### Using Python¶

The [UserResource.create_or_alter](/developer-guide/snowflake-python-
api/reference/latest/_autosummary/snowflake.core.user.UserResource#snowflake.core.user.UserResource.create_or_alter)
method in the Snowflake Python APIs currently does not support changing the
`password` for an existing user. You can only set the password using this
method when creating a new user.

## Resetting the password for an administrator¶

An account administrator (i.e. a user with the ACCOUNTADMIN role) can reset
their own password using the procedure described in Resetting the Password for
a User.

If an account administrator is locked out of their account, a different user
with the ACCOUNTADMIN role can reset the password for the locked-out
administrator. In the event that the administrator is locked out and there is
no other administrator to change the password, contact [Snowflake
Support](https://docs.snowflake.com/user-guide/contacting-support) to reset
the password.

## Disabling the change password functionality for users¶

Users change their Snowflake password in the web interface by clicking the
dropdown menu in the upper right (next to the login name) » Change Password.
The Select a New Password dialog opens. The dialog accepts the current and new
password.

You can optionally disable the ability for users in your account to change
their own password. Account administrators can continue to change user
passwords using the web interface under Account [![Account tab](../_images/ui-
navigation-account-icon.svg)](../_images/ui-navigation-account-icon.svg) »
Users, or through SQL using the [ALTER USER](../sql-reference/sql/alter-user)
command.

To request this change, please contact [Snowflake
Support](https://docs.snowflake.com/user-guide/contacting-support).

## Disabling or enabling a user¶

Disabling a user prevents the user from logging into Snowflake. You can
disable a user through the following interfaces.

### Using Snowsight¶

  1. Sign in to Snowsight.

  2. Select Admin » Users & Roles.

  3. Locate the user that you want to disable and select [![More options](../_images/snowsight-worksheet-explorer-ellipsis.png)](../_images/snowsight-worksheet-explorer-ellipsis.png) » Disable User.

  4. In the confirmation dialog that opens, select Disable.

To enable a user, follow the same steps, but select Enable User.

### Using Classic Console¶

  1. Click on Account [![Account tab](../_images/ui-navigation-account-icon.svg)](../_images/ui-navigation-account-icon.svg) » Users.

  2. Click on a user row to select it, then click the Disable User button. A confirmation dialog opens.

  3. Click Yes to disable the user.

To enable a user, follow the same steps, but select Enable User.

### Using SQL¶

Use the [ALTER USER](../sql-reference/sql/alter-user) command to disable or
enable a user. For example:

  * Disable a user:

> >     ALTER USER janesmith SET DISABLED = TRUE;
>  
>
> Copy

  * Enable a user:

> >     ALTER USER janesmith SET DISABLED = FALSE;
>  
>
> Copy

### Using Python¶

Use the [UserResource.create_or_alter](/developer-guide/snowflake-python-
api/reference/latest/_autosummary/snowflake.core.user.UserResource#snowflake.core.user.UserResource.create_or_alter)
Python API to disable or enable a user. For example:

  * Disable a user:

> >     user_parameters = root.users["janesmith"].fetch()
>     user_parameters.disabled = True
>     root.users["janesmith"].create_or_alter(user_parameters)
>  
>
> Copy

  * Enable a user:

> >     user_parameters = root.users["janesmith"].fetch()
>     user_parameters.disabled = False
>     root.users["janesmith"].create_or_alter(user_parameters)
>  
>
> Copy

## Unlocking a user¶

If a user login fails after five consecutive attempts, the user is locked out
of their account for a period of time (currently 15 minutes). After the period
of time elapses, the system automatically clears the lock and the user can
attempt to log in again.

To unlock the user before the time has elapsed, you can reset the timer using
the [ALTER USER](../sql-reference/sql/alter-user) command or the
[UserResource.create_or_alter](/developer-guide/snowflake-python-
api/reference/latest/_autosummary/snowflake.core.user.UserResource#snowflake.core.user.UserResource.create_or_alter)
Python API.

The following example resets the timer to 0, which immediately unlocks user
`janesmith`:

SQLPython

    
    
    ALTER USER janesmith SET MINS_TO_UNLOCK= 0;
    

Copy

    
    
    user_parameters = root.users["janesmith"].fetch()
    user_parameters.mins_to_unlock = 0
    root.users["janesmith"].create_or_alter(user_parameters)
    

Copy

Tip

If a single role has the OWNERSHIP privilege on all Snowflake users, we
recommend granting the role to multiple users. That way, if a member of the
role is locked out, another member can unlock that user.

## Altering session parameters for a user¶

  * To show the session parameters for a user, use the following SQL syntax:

> >     SHOW PARAMETERS [ LIKE '<pattern>' ] FOR USER <name>
>  
>
> Copy

  * To alter the session parameters for a user, use the following syntax:

> >     ALTER USER <name> SET <session_param> = <value>
>  
>
> Copy

For example, allow a user to remain connected to Snowflake indefinitely
without timing out:

> >     ALTER USER janesmith SET CLIENT_SESSION_KEEP_ALIVE = TRUE;
>  
>
> Copy

  * To reset a session parameter for a user to the default value, use the following syntax:

> >     ALTER USER <name> UNSET <session_param>
>  
>
> Copy

## Modifying other user properties¶

You can modify all other user properties using the [ALTER USER](../sql-
reference/sql/alter-user) command or the
[UserResource.create_or_alter](/developer-guide/snowflake-python-
api/reference/latest/_autosummary/snowflake.core.user.UserResource#snowflake.core.user.UserResource.create_or_alter)
Python API. You can modify many of the same user properties using Snowsight.

For example:

  * Change the last name for user `janesmith` to `Jones`:

SQL:

    
    
        ALTER USER janesmith SET LAST_NAME = 'Jones';
    

Copy

Python:

    
    
        user_parameters = root.users["janesmith"].fetch()
    user_parameters.last_name = "Jones"
    root.users["janesmith"].create_or_alter(user_parameters)
    

Copy

Snowsight:

    
    1. Sign in to Snowsight.

    2. Select Admin » Users & Roles.

    3. Locate the user that you want to edit and select [![More options](../_images/snowsight-worksheet-explorer-ellipsis.png)](../_images/snowsight-worksheet-explorer-ellipsis.png) » Edit.

    4. For the Last Name field, enter Jones.

    5. Select Save User.

  * Set or change the default warehouse, namespace, primary role, and secondary roles for user `janesmith`:

SQL:

    
    
        ALTER USER janesmith SET DEFAULT_WAREHOUSE = mywarehouse DEFAULT_NAMESPACE = mydatabase.myschema DEFAULT_ROLE = myrole DEFAULT_SECONDARY_ROLES = ('ALL');
    

Copy

Python:

    
    
        user_parameters = root.users["janesmith"].fetch()
    user_parameters.default_warehouse = "mywarehouse"
    user_parameters.default_namespace = "mydatabase.myschema"
    user_parameters.default_role = "myrole"
    user_parameters.default_secondary_roles = "ALL"
    root.users["janesmith"].create_or_alter(user_parameters)
    

Copy

Snowsight:

    

Note

You cannot set default secondary roles for a user using Snowsight.

    1. Sign in to Snowsight.

    2. Select Admin » Users & Roles.

    3. Locate the user that you want to edit and select [![More options](../_images/snowsight-worksheet-explorer-ellipsis.png)](../_images/snowsight-worksheet-explorer-ellipsis.png) » Edit.

    4. Open the Advanced User Options and enter values in the relevant fields.

    5. Select Save User.

## Viewing users¶

You can view information about users using the following interfaces.

### Using SQL¶

Use the [DESCRIBE USER](../sql-reference/sql/desc-user) or [SHOW
USERS](../sql-reference/sql/show-users) command to view information about one
or more users.

For example:

    
    
    DESC USER janeksmith;
    

Copy

### Using Python¶

Use the [UserResource.fetch](/developer-guide/snowflake-python-
api/reference/latest/_autosummary/snowflake.core.user.UserResource#snowflake.core.user.UserResource.fetch)
Python API to get information about a user.

For example:

    
    
    my_user = root.users["janesmith"].fetch()
    print(my_user.to_dict())
    

Copy

Use the [UserCollection.iter](/developer-guide/snowflake-python-
api/reference/latest/_autosummary/snowflake.core.user.UserCollection#snowflake.core.user.UserCollection.iter)
Python API to list users in an account.

For example:

    
    
    users = root.users.iter(like="jane%")
    for user in users:
      print(user.name)
    

Copy

### Using Snowsight¶

  1. Sign in to Snowsight.

  2. Select Admin » Users & Roles.

  3. Locate the user for which you want to view more details.

You can review the display name, status, last login time, owning role, and
whether or not the user has multi-factor authentication (MFA) set up. If the
user has a comment, you can hover over the [![Comment
icon](../_images/snowsight-admin-user-comment.png)](../_images/snowsight-
admin-user-comment.png).

  4. Optionally select the user to see more details, such as their default settings, roles that have privileges granted on the user, and the roles granted to the user.

## Dropping a user¶

Dropping a user removes the user credentials from Snowflake.

Important

When you drop a user, the folders, worksheets, and dashboards owned by that
user become inaccessible and **do not** transfer to another user unless
sharing is enabled.

Share recipients with [View, View + Run, and Edit permissions](ui-snowsight-
worksheets.html#label-sharing-worksheets-and-folders) will retain their
assigned permissions and can still access the shared folders, worksheets, and
dashboards. However, only users with Edit permissions can modify or delete the
shared folders, worksheets, and dashboards. If you don’t give Edit permissions
to at least one other user before you drop the owner, that owner’s folders,
worksheets, and dashboards cannot be deleted.

If a dropped user’s worksheets do not have sharing enabled, an administrator
can [recover up to 500 worksheets owned by the user](ui-snowsight-
worksheets.html#label-snowsight-worksheets-recover).

Caution

Any worksheets in the Classic Console will be permanently deleted, and
dashboards will be inaccessible if they were not previously shared with
another user.

Objects created by the user, such as tables or views, are not dropped because
they are owned by the user’s active role when the objects were created.
Another user assigned the same role or a higher role in the [role
hierarchy](security-access-control-considerations) can manage the objects or
transfer ownership to another role.

### Using Snowsight¶

  1. Sign in to Snowsight.

  2. Select Admin » Users & Roles.

  3. Locate the user that you want to disable and select [![More options](../_images/snowsight-worksheet-explorer-ellipsis.png)](../_images/snowsight-worksheet-explorer-ellipsis.png) » Drop.

  4. In the confirmation dialog that opens, select Drop User.

### Using Classic Console¶

  1. Select Account [![Account tab](../_images/ui-navigation-account-icon.svg)](../_images/ui-navigation-account-icon.svg) » Users.

  2. Click a user row to select it, then select Drop. A confirmation dialog opens.

  3. Select Yes to drop the user.

### Using SQL¶

Use the [DROP USER](../sql-reference/sql/drop-user) command to drop a user.

    
    
    DROP USER janesmith;
    

Copy

### Using Python¶

Use the [UserResource.drop](/developer-guide/snowflake-python-
api/reference/latest/_autosummary/snowflake.core.user.UserResource#snowflake.core.user.UserResource.drop)
Python API to drop a user.

    
    
    root.users["janesmith"].drop()
    

Copy

