from setuptools import setup, Extension
import numpy

# Define the extension module
extension = Extension(
    'ocr_bridge',
    sources=['flutter_onnx_ffi/bridge.c'],
    include_dirs=[numpy.get_include()],
    extra_compile_args=['-fPIC'],
)

setup(
    name='ocr_bridge',
    version='1.0.0',
    packages=['flutter_onnx_ffi'],
    ext_modules=[extension],
    install_requires=[
        'onnxtr',
        'numpy',
        'Pillow',
    ],
)