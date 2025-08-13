from dataclasses import dataclass, field
from typing import List
from .detected_label import DetectedLabel

@dataclass
class AnalysisResult:
    labels: List[DetectedLabel] = field(default_factory=list)
    s3_key: str | None = None
    image_url: str | None = None

