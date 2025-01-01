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
            'setuptools'
        ])
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def build_bridge():
    """Build the OCR bridge."""
    try:
        # First ensure dependencies are installed
        if not install_dependencies():
            return False

        # Build with Android target if NDK is available
        if os.getenv('ANDROID_NDK_HOME'):
            print("Building for Android...")
            subprocess.check_call([
                sys.executable,
                'setup.py',
                'build_android'  # Using our new custom command
            ])
        else:
            # Normal build
            print("Building for host system...")
            subprocess.check_call([
                sys.executable,
                'setup.py',
                'build_ext',
                '--inplace'
            ])
        
        print("Bridge built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error building bridge: {e}")
        return False

if __name__ == '__main__':
    success = build_bridge()
    sys.exit(0 if success else 1)