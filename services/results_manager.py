"""Transform Rekognition responses into internal models for rendering/export."""
from models.detected_label import DetectedLabel, LabelInstance, BoundingBox
from models.analysis_result import AnalysisResult

class ResultsManager:
    @staticmethod
    def parse_rekognition_response(resp) -> AnalysisResult:
        """Parse Rekognition DetectLabels response to AnalysisResult.

        Sorts labels by confidence and preserves instances + bounding boxes.
        """
        labels = []
        for item in resp.get('Labels', []):
            instances = []
            for inst in item.get('Instances', []) or []:
                bbox = inst.get('BoundingBox')
                bbox_obj = None
                if bbox:
                    bbox_obj = BoundingBox(
                        left=bbox.get('Left', 0.0),
                        top=bbox.get('Top', 0.0),
                        width=bbox.get('Width', 0.0),
                        height=bbox.get('Height', 0.0),
                    )
                instances.append(LabelInstance(confidence=inst.get('Confidence', 0.0), bounding_box=bbox_obj))
            labels.append(DetectedLabel(name=item.get('Name', ''), confidence=item.get('Confidence', 0.0), instances=instances))
        return AnalysisResult(labels=sorted(labels, key=lambda l: l.confidence, reverse=True))

