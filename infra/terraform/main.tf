terraform {
  required_version = ">= 1.3"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Account/Suffix for unique naming
data "aws_caller_identity" "current" {}

locals {
  bucket_name = var.bucket_name != "" ? var.bucket_name : lower(replace("${var.project_name}-${data.aws_caller_identity.current.account_id}", ":", "-"))
}

resource "aws_s3_bucket" "uploads" {
  bucket = local.bucket_name
  force_destroy = true
}

resource "aws_s3_bucket_ownership_controls" "uploads" {
  bucket = aws_s3_bucket.uploads.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "uploads" {
  bucket = aws_s3_bucket.uploads.id
  acl    = "private"
  depends_on = [aws_s3_bucket_ownership_controls.uploads]
}

resource "aws_s3_bucket_versioning" "uploads" {
  bucket = aws_s3_bucket.uploads.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "uploads" {
  bucket = aws_s3_bucket.uploads.id
  rule {
    apply_server_side_encryption_by_default { sse_algorithm = "AES256" }
  }
}

resource "aws_s3_bucket_cors_configuration" "uploads" {
  bucket = aws_s3_bucket.uploads.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "PUT", "POST"]
    allowed_origins = ["*"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }
}

# IAM Policy for app (S3 + Rekognition)
resource "aws_iam_policy" "app_policy" {
  name        = "${var.project_name}-policy"
  description = "Least-privilege for S3 uploads and Rekognition detect_labels"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["s3:PutObject", "s3:GetObject", "s3:ListBucket"]
        Resource = [aws_s3_bucket.uploads.arn, "${aws_s3_bucket.uploads.arn}/*"]
      },
      {
        Effect = "Allow"
        Action = ["rekognition:DetectLabels"]
        Resource = "*"
      }
    ]
  })
}

# Optional IAM user
resource "aws_iam_user" "app_user" {
  count = var.create_iam_user ? 1 : 0
  name = "${var.project_name}-user"
}

resource "aws_iam_user_policy_attachment" "attach" {
  count      = var.create_iam_user ? 1 : 0
  user       = aws_iam_user.app_user[0].name
  policy_arn = aws_iam_policy.app_policy.arn
}

resource "aws_iam_access_key" "app_key" {
  count = var.create_iam_user ? 1 : 0
  user  = aws_iam_user.app_user[0].name
}

