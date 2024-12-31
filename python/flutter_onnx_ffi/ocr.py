from onnxtr.io import DocumentFile
from onnxtr.models import ocr_predictor
import json

class OCREngine:
    def __init__(self):
        self.predictor = ocr_predictor(
            det_arch='db_mobilenet_v3_large',
            reco_arch='crnn_mobilenet_v3_small'
        )

    def process_image(self, image_path: str, min_confidence: float = 0.5):
        try:
            img = DocumentFile.from_images([image_path])
            result = self.predictor(img)
            return json.dumps({
                'status': 'success',
                'text': result.text,
                'confidence': float(min_confidence),
            }).encode('utf-8')
        except Exception as e:
            return json.dumps({
                'status': 'error',
                'message': str(e)
            }).encode('utf-8')