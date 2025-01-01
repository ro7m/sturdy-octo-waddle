import subprocess
import sys
import os

def install_dependencies():
    """Install required packages."""
    try:
        print("Installing required packages...")
        subprocess.check_call([
            sys.executable, 
            '-m', 
            'pip', 
            'install',
            '--upgrade',
            'numpy',
            'onnxtr',
            'Pillow',
            'setuptools',
            'crossenv'  # Added for cross-compilation
        ])
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def build_bridge_for_android():
    """Build the OCR bridge for Android ARM architectures."""
    try:
        # Build for arm64-v8a
        print("Building for arm64-v8a...")
        env = os.environ.copy()
        env['ANDROID_ABI'] = 'arm64-v8a'
        env['ANDROID_PLATFORM'] = '21'  # Minimum SDK version
        
        subprocess.check_call([
            sys.executable,
            'setup.py',
            'build_ext',
            '--inplace',
            '--target-android'
        ], env=env)
        
        # Build for armeabi-v7a
        print("Building for armeabi-v7a...")
        env['ANDROID_ABI'] = 'armeabi-v7a'
        subprocess.check_call([
            sys.executable,
            'setup.py',
            'build_ext',
            '--inplace',
            '--target-android'
        ], env=env)
        
        print("Android builds completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error building for Android: {e}")
        return False

if __name__ == '__main__':
    if not install_dependencies():
        sys.exit(1)
    success = build_bridge_for_android()
    sys.exit(0 if success else 1)