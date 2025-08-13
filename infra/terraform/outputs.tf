output "bucket_name" {
  value = aws_s3_bucket.uploads.bucket
}

output "region" {
  value = var.aws_region
}

output "iam_user_name" {
  value = var.create_iam_user ? aws_iam_user.app_user[0].name : null
}

output "iam_access_key_id" {
  value     = var.create_iam_user ? aws_iam_access_key.app_key[0].id : null
  sensitive = true
}

output "iam_secret_access_key" {
  value     = var.create_iam_user ? aws_iam_access_key.app_key[0].secret : null
  sensitive = true
}

