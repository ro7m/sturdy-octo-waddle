#!/bin/bash
set -e

# Build Python package
cd python
python3 -m pip install -r requirements.txt
python3 setup.py build

# Copy library to Android project
cp build/lib*/ocr_bridge*.so ../android/app/src/main/jniLibs/