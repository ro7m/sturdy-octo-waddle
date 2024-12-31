from setuptools import setup, Extension

setup(
    name='ocr_bridge',
    version='1.0.0',
    packages=['flutter_onnx_ffi'],
    ext_modules=[
        Extension(
            'ocr_bridge',
            sources=['flutter_onnx_ffi/bridge.py'],
            language='c',
        )
    ],
)