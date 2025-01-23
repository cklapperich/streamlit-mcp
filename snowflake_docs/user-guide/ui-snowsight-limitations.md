# Snowsight Limitations¶

This topic provides information about the limitations of Snowsight.

## Database role privileges¶

Currently, Snowsight does not recognize inherited privileges from database
roles or application roles. As a result, even if a user has the correct
privileges through a database role, they might still be unable to perform
certain actions, such as loading files into a stage, running a task, or
monitoring a Dynamic Table in Snowsight.

In addition, existing database roles are not displayed in Snowsight under
Admin » Users & Roles » Roles.

You can use the [SHOW ROLES IN DATABASE](../sql-reference/sql/show-roles)
command to ensure that you have correctly granted privileges using the
appropriate roles.

Note

This limitation does not impact user written queries executed in worksheets or
notebooks.

**Related topics**

  * [Database privileges](security-access-control-privileges.html#label-database-privileges)

  * [Role hierarchy and privilege inheritance](security-access-control-overview.html#label-role-hierarchy-and-privilege-inheritance)

  * [Grant the role to users](security-access-control-configure.html#label-grant-role-to-users)

