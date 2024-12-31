from setuptools import setup, find_packages

setup(
    name='flutter_onnxtr_ffi',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.21.0',
        'onnxruntime>=1.8.0',
        'Pillow>=8.0.0',
        'onnxtr @ git+https://github.com/felixdittrich92/OnnxTR.git'
    ],
    python_requires='>=3.7',
    author='Your Name',
    author_email='your.email@example.com',
    description='Python bridge for Flutter OnnxTR FFI integration',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)