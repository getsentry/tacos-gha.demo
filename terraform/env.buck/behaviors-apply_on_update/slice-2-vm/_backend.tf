# Generated by Terragrunt. Sig: nIlQXj57tbuaRZEa
terraform {
  backend "gcs" {
    bucket   = "sac-dev-tf--tacos-gha"
    prefix   = "tacos-demo/env.buck/behaviors-apply_on_update/slice-2-vm"
  }
}