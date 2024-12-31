from setuptools import setup, find_packages

setup(
    name='flutter_onnx_ffi',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.21.0',
        'onnxruntime>=1.8.0',
        'Pillow>=8.0.0',
        'onnxtr>=0.6.0'
    ],
    python_requires='>=3.7',
    author='ro7m',
    author_email='',
    description='Python bridge for Flutter DocTR FFI integration',
    long_description='Python bridge for flutter FFI ',
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)