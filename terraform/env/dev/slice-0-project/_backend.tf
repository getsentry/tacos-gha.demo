# Generated by Terragrunt. Sig: nIlQXj57tbuaRZEa
terraform {
  backend "gcs" {
    bucket   = "sac-dev-tf--tacos-gha"
    prefix   = "tacos-demo/env/dev/slice-0-project"
  }
}
