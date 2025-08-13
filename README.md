# AWS Image Labels Generator

A Flask web app that uploads images to S3 and uses Amazon Rekognition to generate labels with confidence scores.

## Prerequisites
- Python 3.9+
- AWS credentials configured (aws configure or environment variables)
- An S3 bucket and AWS region

## Environment configuration
Create a .env file in the project root with:

```
# .env
SECRET_KEY=dev-secret
AWS_REGION=us-east-1
S3_BUCKET=your-bucket-name
DEFAULT_CONFIDENCE_THRESHOLD=50
DEFAULT_MAX_LABELS=10
```

The app loads .env automatically via python-dotenv. Do not commit .env.

## Install and run
1. python -m venv venv && source venv/bin/activate
2. pip install -r requirements.txt
3. python app.py
4. Open http://localhost:5000

## Terraform (optional)
Infrastructure as code for the S3 bucket and IAM policy is available under infra/terraform.

Quick start:
```
cd infra/terraform
terraform init -upgrade
terraform apply -auto-approve -var="project_name=aws-image-labels-generator" -var="aws_region=us-east-1"
```
Then manually copy the outputs into your .env as AWS_REGION and S3_BUCKET.

## Notes
- specs/ and steering/ are internal docs and intentionally excluded from git.
- This project uses in-memory stores for demo purposes. Replace with a persistent store for production.

## Further improvements
- Security and auth
  - Add user authentication and per-user isolation
  - Use signed sessions or Redis/DB to store session state instead of in-memory dicts
  - Restrict S3 CORS allowed_origins to your frontend host
- Reliability and UX
  - Stream uploads directly to S3 with presigned POST to avoid large payloads to the server
  - Add client-side preview and progress indicators
  - Graceful error pages and i18n-friendly messages
- Features
  - Overlay labels on the image with position-aware markers and tooltips
  - Toggleable confidence threshold and max labels in the results view
  - Additional Rekognition features (Text, Moderation, Celebrity, Faces)
- DevOps
  - CI: run pytest, flake8, mypy, terraform validate/plan on PRs
  - IaC: Parameter Store/Secrets Manager for configuration, per-env workspaces
  - Observability: structured logging and metrics (e.g., CloudWatch)
- Testing
  - Unit tests with moto/Stubber for boto3
  - Integration tests for Flask routes with pytest and requests
