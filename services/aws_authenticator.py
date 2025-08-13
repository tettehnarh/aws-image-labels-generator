import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

class AWSAuthenticator:
    def __init__(self, region_name: str):
        self.region_name = region_name

    def create_session(self):
        try:
            session = boto3.Session(region_name=self.region_name)
            # Validate by getting credentials
            creds = session.get_credentials()
            if not creds:
                raise NoCredentialsError()
            return session
        except (NoCredentialsError, PartialCredentialsError) as e:
            raise RuntimeError("AWS credentials not configured") from e

