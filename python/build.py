import os
import sys
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

def build_shared_library():
    """Build shared library for FFI."""
    
    # Determine library name based on platform
    if sys.platform == 'win32':
        lib_name = 'ocr_bridge.dll'
    elif sys.platform == 'darwin':
        lib_name = 'libocr_bridge.dylib'
    else:
        lib_name = 'libocr_bridge.so'

    # Source files
    sources = ['flutter_onnx_ffi/bridge.py']

    # Platform-specific compile arguments
    extra_compile_args = []
    extra_link_args = []

    if sys.platform == 'darwin':
        extra_compile_args.extend(['-arch', 'x86_64', '-arch', 'arm64'])
        extra_link_args.extend(['-arch', 'x86_64', '-arch', 'arm64'])
    
    # Define extension
    extension = Extension(
        'ocr_bridge',
        sources=sources,
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    )

    # Build
    setup(
        name='ocr_bridge',
        version='1.0.0',
        ext_modules=[extension],
        cmdclass={'build_ext': build_ext},
        install_requires=[
            'onnxtr',
            'numpy',
            'Pillow',
        ],
    )

if __name__ == '__main__':
    build_shared_library()