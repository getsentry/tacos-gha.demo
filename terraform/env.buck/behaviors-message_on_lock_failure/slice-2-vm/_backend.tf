# Generated by Terragrunt. Sig: nIlQXj57tbuaRZEa
terraform {
  backend "gcs" {
    bucket   = "sac-dev-tf--tacos-gha"
    prefix   = "tacos-demo/env.buck/behaviors-message_on_lock_failure/slice-2-vm"
  }
}
