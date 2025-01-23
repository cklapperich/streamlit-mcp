# Snowflake Terraform provider¶

Note

The following content is not supported by Snowflake. All code is provided “AS
IS” and without warranty.

[HashiCorp Terraform](https://developer.hashicorp.com/terraform) is an open
source Infrastructure as Code (IaC) tool that allows you to dynamically build,
change, and version infrastructure resources. You use the [Terraform
language](https://developer.hashicorp.com/terraform/language) to create
configuration files that describe the configuration you want. Terraform
compares your configuration to the current state and then generates a plan to
create new resources or update and delete existing resources. The plan runs as
a directed acyclic graph (DAG), which allows Terraform to understand and
handle dependencies between resources.

The [Snowflake Terraform
provider](https://registry.terraform.io/providers/Snowflake-
Labs/snowflake/latest) allows you to establish a consistent workflow to manage
Snowflake resources like warehouses, databases, schemas, tables, roles,
grants, and more. For more information about other features and building
blocks that support Snowflake DevOps workflows, see [Snowflake
DevOps](../developer-guide/builders/devops).

After you [install
Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-
started/install-cli#install-terraform), see the following resources to get
started using the Snowflake provider.

Resource | Description  
---|---  
[Snowflake provider documentation](https://registry.terraform.io/providers/Snowflake-Labs/snowflake/latest/docs) | Guides and reference documentation in the [Terraform Registry](https://registry.terraform.io/) for the Snowflake provider. Documentation includes the [resource blocks](https://developer.hashicorp.com/terraform/language/resources/syntax) that describe objects in Snowflake (for example, [snowflake_database](https://registry.terraform.io/providers/Snowflake-Labs/snowflake/latest/docs/resources/database)) and the [data sources](https://developer.hashicorp.com/terraform/language/data-sources) that you can use to name and dynamically fetch configuration state from Snowflake objects (for example, [snowflake_users](https://registry.terraform.io/providers/Snowflake-Labs/snowflake/latest/docs/data-sources/users)).  
[terraform-provider-snowflake](https://github.com/Snowflake-Labs/terraform-provider-snowflake) | The open-source project on GitHub from Snowflake Labs where you can do the following:

  * Stay up to date on feature developments and status, including the [project roadmap](https://github.com/Snowflake-Labs/terraform-provider-snowflake/blob/main/ROADMAP.md) and [issues](https://github.com/Snowflake-Labs/terraform-provider-snowflake/issues).
  * Get support from the community in [discussion forums](https://github.com/Snowflake-Labs/terraform-provider-snowflake/discussions). (Snowflake does not provide support for the Snowflake provider.)
  * Review supplementary documentation and source code.

  
[Terraforming Snowflake](https://quickstarts.snowflake.com/guide/terraforming_snowflake/#0) | This Quickstart tutorial from Snowflake Labs guides you through creating a Terraform project in GitHub that uses the Snowflake provider to create a demo database and warehouse.

