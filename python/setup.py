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
        python_lib = sysconfig.get_config_var('LIBDIR')
        
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
        print(f"Python library directory: {python_lib}")
        print(f"Sysroot: {sysroot}")

        # Get Python API version
        python_api_version = sysconfig.get_config_var('PYTHON_API_VERSION')
        if not python_api_version:
            python_api_version = f"{sys.version_info[0]}0{sys.version_info[1]}"

        # Common defines for Python compatibility
        python_defines = [
            '-DPy_BUILD_CORE',
            '-DNDEBUG',
            f'-DPYTHON_API_VERSION="{python_api_version}"',
            '-DPy_LONG_BIT=64',
            '-DPLATFORM_ANDROID',
            f'-DPYTHON_VERSION="{python_version}"',
        ]

        # Compile command
        cmd = [
            cc,
            '-shared',
            '-fPIC',
            '-O3',
            f'-I{python_include}',
            f'-L{python_lib}',
            f'-lpython{python_version}',
            f'--sysroot={sysroot}',
            *python_defines,
            'flutter_onnx_ffi/bridge.c',
            '-o',
            os.path.join(output_dir, 'libocr_bridge.so')
        ]

        print(f"Running command: {' '.join(cmd)}")
        
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            print(f"Build output: {output.decode()}")
            print(f"Successfully built for {abi}")

            # Copy Python shared library
            src_lib = os.path.join(python_lib, f'libpython{python_version}.so')
            dst_lib = os.path.join(output_dir, f'libpython{python_version}.so')
            if os.path.exists(src_lib):
                import shutil
                shutil.copy2(src_lib, dst_lib)
                print(f"Copied Python library to {dst_lib}")

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