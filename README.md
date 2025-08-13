# AWS Image Labels Generator

A Flask web app that uploads images to S3 and uses Amazon Rekognition to generate labels with confidence scores.

## Setup
1. Create and activate a virtualenv
2. Install requirements: `pip install -r requirements.txt`
3. Configure AWS credentials (via AWS CLI or environment)
4. Set env vars: `export S3_BUCKET=your-bucket AWS_REGION=us-east-1`
5. Run: `python app.py`

Note: specs/ and steering/ are development docs and intentionally excluded from git.

