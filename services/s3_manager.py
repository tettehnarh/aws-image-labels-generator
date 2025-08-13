"""Thin wrapper around S3 operations used by the app.

Keeps key-generation conventions and presign logic in one place.
"""
import uuid

class S3Manager:
    def __init__(self, session, bucket: str):
        self.s3 = session.resource('s3')
        self.client = session.client('s3')
        self.bucket = bucket

    def generate_key(self, filename: str, session_id: str) -> str:
        """Create a unique object key namespaced by session.

        Example: uploads/<session>/<uuid>.ext
        """
        ext = filename.rsplit('.', 1)[-1].lower()
        return f"uploads/{session_id}/{uuid.uuid4().hex}.{ext}"

    def upload_bytes(self, data: bytes, key: str, content_type: str) -> str:
        """Upload raw bytes to S3 under the given key."""
        obj = self.s3.Object(self.bucket, key)
        obj.put(Body=data, ContentType=content_type)
        return key

    def presigned_url(self, key: str, expires_in: int = 3600) -> str:
        """Return a presigned GET URL for the object.

        boto3 expects the client method in snake_case.
        """
        return self.client.generate_presigned_url(
            'get_object', Params={'Bucket': self.bucket, 'Key': key}, ExpiresIn=expires_in
        )

