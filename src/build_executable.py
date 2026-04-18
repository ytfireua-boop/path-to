#!/usr/bin/env python3
"""
Build script to create standalone executable for path-to
"""

import os
import sys
import subprocess
import shutil

def build_executable():
    """Build standalone executable using PyInstaller"""
    print("Building path-to standalone executable...")
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"PyInstaller found: {PyInstaller.__version__}")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # Clean previous builds
    print("Cleaning previous builds...")
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    for folder in ['build', 'dist']:
        folder_path = os.path.join(parent_dir, folder)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
    
    # Build executable
    print("Building executable...")
    cmd = [sys.executable, "-m", "PyInstaller", "--onefile", "--console", "path_to_final.py"]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Build completed successfully!")
        print(result.stdout)
        
        # Check if executable was created
        exe_path = os.path.join(parent_dir, "dist", "path-to.exe" if os.name == "nt" else "path-to")
        if os.path.exists(exe_path):
            print(f"Executable created: {os.path.abspath(exe_path)}")
            
            # Copy to executable folder for easy access
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            executable_dir = os.path.join(parent_dir, "executable")
            if not os.path.exists(executable_dir):
                os.makedirs(executable_dir)
            dest_path = os.path.join(executable_dir, "path-to.exe" if os.name == "nt" else "path-to")
            shutil.copy2(exe_path, dest_path)
            print(f"Executable copied to: {os.path.abspath(dest_path)}")
            
            print("Build complete! You can now run 'path-to' without Python installed.")
            print(f"   Command: {dest_path} <filename>")
            print(f"   GUI Installer: {dest_path} --installer")
            
        else:
            print("Executable not found in dist folder")
            
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False
    
    return True

if __name__ == "__main__":
    build_executable()
