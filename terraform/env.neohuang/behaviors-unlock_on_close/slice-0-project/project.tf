variable "project" {
  type = string
}

resource "null_resource" "project" {
  triggers = {
    project = var.project
  }
}

resource "null_resource" "project2" {
  triggers = {
    project = var.project
  }
}
