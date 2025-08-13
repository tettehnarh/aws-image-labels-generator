"""Utilities to create an authenticated boto3 session.

This module centralizes AWS authentication and region configuration. It uses
standard credential providers (env vars, shared config, instance profile).
"""
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

class AWSAuthenticator:
    """Create and validate a boto3 Session for a given region."""

    def __init__(self, region_name: str):
        self.region_name = region_name

    def create_session(self):
        """Return a boto3 Session configured for the app's AWS region.

        Raises:
            RuntimeError: if no valid AWS credentials are available. This is
                caught by callers and surfaced as a friendly HTTP error.
        """
        try:
            session = boto3.Session(region_name=self.region_name)
            # Validate by getting credentials (does not make a network call)
            creds = session.get_credentials()
            if not creds:
                raise NoCredentialsError()
            return session
        except (NoCredentialsError, PartialCredentialsError) as e:
            raise RuntimeError("AWS credentials not configured") from e

