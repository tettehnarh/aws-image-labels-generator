from dataclasses import dataclass

@dataclass
class DetectionConfig:
    confidence_threshold: float = 50.0
    max_labels: int = 10

