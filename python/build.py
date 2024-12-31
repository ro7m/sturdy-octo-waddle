import subprocess
import sys
import os

def build_bridge():
    try:
        # Run pip install if requirements.txt exists
        if os.path.exists('requirements.txt'):
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

        # Install the package in development mode
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-e', '.'])
        
        print("Bridge built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error building bridge: {e}")
        return False

if __name__ == '__main__':
    success = build_bridge()
    sys.exit(0 if success else 1)