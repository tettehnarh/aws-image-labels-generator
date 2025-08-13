"""Wrapper for Amazon Rekognition calls used by the app."""

class RekognitionManager:
    def __init__(self, session):
        self.client = session.client('rekognition')

    def detect_labels(self, bucket: str, key: str, max_labels: int, min_confidence: float):
        """Call Rekognition DetectLabels for an S3 object.

        Args:
            bucket: S3 bucket name
            key: S3 object key
            max_labels: Max labels to return
            min_confidence: Minimum confidence percentage to include
        """
        resp = self.client.detect_labels(
            Image={'S3Object': {'Bucket': bucket, 'Name': key}},
            MaxLabels=max_labels,
            MinConfidence=min_confidence
        )
        return resp

