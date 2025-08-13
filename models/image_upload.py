from dataclasses import dataclass
from datetime import datetime

@dataclass
class ImageUpload:
    filename: str
    file_size: int
    content_type: str
    s3_key: str | None
    upload_timestamp: datetime
    session_id: str

