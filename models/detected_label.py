from dataclasses import dataclass, field
from typing import List

@dataclass
class BoundingBox:
    left: float
    top: float
    width: float
    height: float

@dataclass
class LabelInstance:
    confidence: float
    bounding_box: BoundingBox | None = None

@dataclass
class DetectedLabel:
    name: str
    confidence: float
    instances: List[LabelInstance] = field(default_factory=list)

