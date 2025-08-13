from typing import List
from botocore.exceptions import ClientError

class RekognitionManager:
    def __init__(self, session):
        self.client = session.client('rekognition')

    def detect_labels(self, bucket: str, key: str, max_labels: int, min_confidence: float):
        resp = self.client.detect_labels(
            Image={
                'S3Object': {'Bucket': bucket, 'Name': key}
            },
            MaxLabels=max_labels,
            MinConfidence=min_confidence
        )
        return resp

