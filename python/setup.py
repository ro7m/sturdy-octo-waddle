from setuptools import setup, Extension
import sys
import os
import subprocess
from distutils.core import Command
from distutils.command.build_ext import build_ext
import sysconfig

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

        # Only build for arm64-v8a
        abi = 'arm64-v8a'
        config = {
            'cc': 'aarch64-linux-android21-clang',
            'target': 'aarch64-linux-android21',
        }

        # Get Python paths and version info
        python_version = f"{sys.version_info[0]}.{sys.version_info[1]}"
        python_include = sysconfig.get_path('include')
        
        print(f"\nBuilding for {abi}...")
        
        # Set up compiler and paths
        toolchain = os.path.join(android_ndk, 'toolchains', 'llvm', 'prebuilt', 'linux-x86_64', 'bin')
        cc = os.path.join(toolchain, config['cc'])
        sysroot = os.path.join(android_ndk, 'toolchains', 'llvm', 'prebuilt', 'linux-x86_64', 'sysroot')
        
        # Create output directory
        output_dir = f'build/lib.android-{abi}'
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"Using compiler: {cc}")
        print(f"Python include directory: {python_include}")
        print(f"Sysroot: {sysroot}")

        # Common defines for Python compatibility
        python_defines = [
            '-DPy_LIMITED_API=0x03070000',  # Use Python 3.7+ stable ABI
            '-DPY_SSIZE_T_CLEAN',
            '-DANDROID',
            '-DPy_BUILD_CORE',
            '-DNDEBUG',
            '-DPy_LONG_BIT=64',
        ]

        # Compile command
        cmd = [
            cc,
            '-shared',
            '-fPIC',
            '-O3',
            f'-I{python_include}',
            f'--sysroot={sysroot}',
            *python_defines,
            '-fvisibility=hidden',
            'flutter_onnx_ffi/bridge.c',
            '-o',
            os.path.join(output_dir, 'libocr_bridge.so')
        ]

        print(f"Running command: {' '.join(cmd)}")
        
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            print(f"Build output: {output.decode()}")
            print(f"Successfully built for {abi}")

        except subprocess.CalledProcessError as e:
            print(f"Error building for {abi}:")
            print(f"Command output: {e.output.decode()}")
            raise

class CustomBuildExt(build_ext):
    def build_extensions(self):
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