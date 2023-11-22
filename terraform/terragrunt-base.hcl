locals {
  env_vars = read_terragrunt_config(find_in_parent_folders("project.hcl"))
}


inputs = merge(
  local.env_vars.inputs
)


generate "_backend.tf" {
  path = "_backend.tf"
  if_exists = "overwrite"
  contents = <<EOF
terraform {
  backend "gcs" {
    bucket   = "sac-dev-tf--tacos-gha"
    prefix   = "tacos-demo/${path_relative_to_include()}"
  }
}
EOF
}
