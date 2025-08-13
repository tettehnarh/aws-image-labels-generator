# Terraform for AWS Image Labels Generator

This Terraform configuration provisions:
- S3 bucket for uploads (with encryption, private ACL, CORS for app)
- Optional IAM user + policy for programmatic access (off by default)

## Usage

1. Install Terraform (>= 1.3)
2. In this directory:

```
terraform init
terraform plan -var="project_name=aws-image-labels-generator" -var="aws_region=us-east-1"
terraform apply -auto-approve -var="project_name=aws-image-labels-generator" -var="aws_region=us-east-1"
```

Outputs:
- bucket_name: S3 bucket you should set as S3_BUCKET env var in the app

To create an IAM user (optional):
```
terraform apply -var="create_iam_user=true"
```

