#!/bin/bash

# Check for required environment variables
if [ -z "$ANDROID_NDK_HOME" ]; then
    echo "Error: ANDROID_NDK_HOME environment variable not set"
    exit 1
fi

# Install python-for-android if not already installed
pip install python-for-android

# Create build directory
BUILD_DIR="build_android"
mkdir -p $BUILD_DIR
cd $BUILD_DIR

# Build Python for Android
p4a create --requirements=python3 --arch=arm64-v8a --android-api=21 --bootstrap=sdl2 --dist_name=myapp

# Create the jniLibs directory
JNILIBS_DIR="../android/app/src/main/jniLibs/arm64-v8a"
mkdir -p $JNILIBS_DIR

# Copy the library
cp .p4a-build/artifacts/python3_arm64-v8a/lib/libpython3.10.so $JNILIBS_DIR/

echo "Build complete. Python library installed at: $JNILIBS_DIR"