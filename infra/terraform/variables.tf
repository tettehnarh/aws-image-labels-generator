variable "project_name" {
  type = string
}

variable "aws_region" {
  type = string
}

variable "create_iam_user" {
  type    = bool
  default = false
}

# Optional custom bucket name; if empty, name is derived from project + account id
variable "bucket_name" {
  type    = string
  default = ""
}

