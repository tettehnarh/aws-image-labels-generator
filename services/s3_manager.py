import uuid
from typing import Optional

from botocore.exceptions import ClientError

class S3Manager:
    def __init__(self, session, bucket: str):
        self.s3 = session.resource('s3')
        self.client = session.client('s3')
        self.bucket = bucket

    def generate_key(self, filename: str, session_id: str) -> str:
        ext = filename.rsplit('.', 1)[-1].lower()
        return f"uploads/{session_id}/{uuid.uuid4().hex}.{ext}"

    def upload_bytes(self, data: bytes, key: str, content_type: str) -> str:
        obj = self.s3.Object(self.bucket, key)
        obj.put(Body=data, ContentType=content_type)
        return key

    def presigned_url(self, key: str, expires_in: int = 3600) -> str:
        return self.client.generate_presigned_url(
            'getObject', Params={'Bucket': self.bucket, 'Key': key}, ExpiresIn=expires_in
        )

