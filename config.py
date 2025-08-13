import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
    AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
    S3_BUCKET = os.environ.get("S3_BUCKET", "")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB upload limit
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "bmp", "webp"}
    DEFAULT_CONFIDENCE_THRESHOLD = float(os.environ.get("DEFAULT_CONFIDENCE_THRESHOLD", 50))
    DEFAULT_MAX_LABELS = int(os.environ.get("DEFAULT_MAX_LABELS", 10))

