locals {
  env_vars = read_terragrunt_config(find_in_parent_folders("project.hcl"))
}


inputs = merge(
  local.env_vars.inputs
)
