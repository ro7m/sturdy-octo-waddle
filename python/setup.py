from setuptools import setup, Extension
import sys
import os
import subprocess
from distutils.core import Command
from distutils.command.build_ext import build_ext

class BuildAndroidExt(Command):
    description = 'build Android extensions'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        android_ndk = os.getenv('ANDROID_NDK_HOME')
        if not android_ndk:
            raise EnvironmentError("ANDROID_NDK_HOME environment variable not set")

        # Build for different Android architectures
        architectures = {
            'arm64-v8a': {
                'cc': 'aarch64-linux-android21-clang',
                'target': 'aarch64-linux-android21',
            },
            'armeabi-v7a': {
                'cc': 'armv7a-linux-androideabi21-clang',
                'target': 'armv7a-linux-androideabi21',
            }
        }

        for abi, config in architectures.items():
            print(f"Building for {abi}...")
            
            # Set up compiler and flags
            toolchain = os.path.join(android_ndk, 'toolchains', 'llvm', 'prebuilt', 'linux-x86_64', 'bin')
            cc = os.path.join(toolchain, config['cc'])
            
            # Create output directory
            output_dir = f'build/lib.android-{abi}'
            os.makedirs(output_dir, exist_ok=True)
            
            # Get Python include directory
            python_include = os.path.join(sys.prefix, 'include', f'python{sys.version_info[0]}.{sys.version_info[1]}')
            
            print(f"Using compiler: {cc}")
            print(f"Python include directory: {python_include}")
            
            # Compile
            try:
                subprocess.check_call([
                    cc,
                    '-shared',
                    '-fPIC',
                    '-O3',
                    f'-I{python_include}',
                    'flutter_onnx_ffi/bridge.c',
                    '-o',
                    os.path.join(output_dir, 'libocr_bridge.so')
                ], stderr=subprocess.PIPE)
                
                print(f"Successfully built for {abi}")
            except subprocess.CalledProcessError as e:
                print(f"Error building for {abi}: {e.stderr.decode()}")
                raise

class CustomBuildExt(build_ext):
    def build_extensions(self):
        # Normal build process
        super().build_extensions()

setup(
    name='flutter_onnx_ffi',
    version='1.0',
    description='OCR Bridge for Flutter',
    ext_modules=[
        Extension(
            'ocr_bridge',
            sources=['flutter_onnx_ffi/bridge.c'],
        )
    ],
    cmdclass={
        'build_ext': CustomBuildExt,
        'build_android': BuildAndroidExt,
    },
    packages=['flutter_onnx_ffi'],
)