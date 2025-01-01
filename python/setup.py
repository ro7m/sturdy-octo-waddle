from setuptools import setup, Extension
import sys
import os

def get_android_compile_args():
    android_ndk = os.getenv('ANDROID_NDK_HOME')
    if not android_ndk:
        raise EnvironmentError("ANDROID_NDK_HOME environment variable not set")
    
    abi = os.getenv('ANDROID_ABI')
    if not abi:
        raise EnvironmentError("ANDROID_ABI environment variable not set")
    
    platform_level = os.getenv('ANDROID_PLATFORM', '21')
    
    if abi == 'arm64-v8a':
        arch = 'aarch64-linux-android'
    elif abi == 'armeabi-v7a':
        arch = 'armv7a-linux-androideabi'
    else:
        raise ValueError(f"Unsupported ABI: {abi}")
    
    toolchain = os.path.join(android_ndk, 'toolchains', 'llvm', 'prebuilt', 'linux-x86_64')
    
    return {
        'compiler': os.path.join(toolchain, 'bin', f'{arch}{platform_level}-clang'),
        'extra_compile_args': [
            f'-target {arch}',
            '-fPIC',
            f'-D__ANDROID_API__={platform_level}'
        ],
        'extra_link_args': [
            f'-target {arch}',
            '-shared',
            f'-D__ANDROID_API__={platform_level}'
        ]
    }

def build_extension():
    sources = ['flutter_onnx_ffi/bridge.c']
    
    if '--target-android' in sys.argv:
        sys.argv.remove('--target-android')
        android_args = get_android_compile_args()
        
        return Extension(
            'ocr_bridge',
            sources=sources,
            extra_compile_args=android_args['extra_compile_args'],
            extra_link_args=android_args['extra_link_args']
        )
    else:
        return Extension(
            'ocr_bridge',
            sources=sources
        )

setup(
    name='flutter_onnx_ffi',
    version='1.0',
    description='OCR Bridge for Flutter',
    ext_modules=[build_extension()],
    packages=['flutter_onnx_ffi'],
)