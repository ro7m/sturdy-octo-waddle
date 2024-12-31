from onnxtr.io import DocumentFile
from onnxtr.models import ocr_predictor

class OCREngine:
    def __init__(self):
        self.predictor = ocr_predictor(
            det_arch='db_mobilenet_v3_large',
            reco_arch='crnn_mobilenet_v3_small'
        )

    def process_image(self, image_path: str, min_confidence: float = 0.5):
        try:
            # Load and process image
            img = DocumentFile.from_images([image_path])
            result = self.predictor(img)
            
            return {
                'status': 'success',
                'text': result.text,
                'boxes': result.boxes,
                'confidence': float(result.confidence) if hasattr(result, 'confidence') else 1.0
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }