"""Lightweight image validation utilities.

Uses imghdr + Pillow to quickly verify image content before S3 upload.
"""
from PIL import Image
import imghdr
from io import BytesIO

class ImageProcessor:
    # Formats that Rekognition supports for DetectLabels
    SUPPORTED_FORMATS = {"jpeg", "png", "gif", "bmp", "webp"}

    @staticmethod
    def allowed_file(filename: str, allowed_exts: set[str]) -> bool:
        """Check file extension against app-configured allowed types."""
        return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_exts

    @staticmethod
    def validate_image(file_bytes: bytes, max_size_bytes: int) -> tuple[bool, str | None]:
        """Basic validations: size and decodability.

        Returns (ok, error_message)
        """
        if len(file_bytes) > max_size_bytes:
            return False, "File exceeds 5MB limit"
        kind = imghdr.what(None, h=file_bytes)
        if kind not in ImageProcessor.SUPPORTED_FORMATS:
            return False, f"Unsupported image format: {kind}"
        # Try opening with Pillow
        try:
            Image.open(BytesIO(file_bytes)).verify()
        except Exception:
            return False, "Invalid image file"
        return True, None

