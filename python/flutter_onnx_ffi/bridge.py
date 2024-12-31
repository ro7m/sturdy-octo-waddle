import os
import sys
import ctypes
from typing import Optional
from .ocr import OCREngine
from .utils import serialize_result

class OCRBridge:
    _instance: Optional['OCRBridge'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OCRBridge, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize OCR engine."""
        try:
            self.engine = OCREngine()
            self._register_functions()
        except Exception as e:
            print(f"Failed to initialize OCR Bridge: {e}", file=sys.stderr)
            raise

    def _register_functions(self):
        """Register FFI functions."""
        # Process image function
        @ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.c_char_p, ctypes.c_float)
        def process_image(image_path_bytes: bytes, min_confidence: float) -> bytes:
            try:
                image_path = image_path_bytes.decode('utf-8')
                result = self.engine.process_image(
                    image_path,
                    min_confidence=min_confidence
                )
                return serialize_result(result).encode('utf-8')
            except Exception as e:
                error_result = {
                    'status': 'error',
                    'message': f'Bridge error: {str(e)}'
                }
                return serialize_result(error_result).encode('utf-8')

        # Store function references
        self._process_image = process_image

        # Make functions available globally
        lib = ctypes.CDLL(None)
        lib.process_image = self._process_image

# Create global instance
bridge = OCRBridge()