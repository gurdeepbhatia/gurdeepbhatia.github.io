"""
Build script for Chart Preparation Utility
Automates the PyInstaller build process
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def clean_build_directories():
    """Remove old build directories"""
    print("Cleaning old build directories...")
    
    dirs_to_remove = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  - Removed {dir_name}/")
    
    # Remove spec pycache
    spec_cache = Path('services/__pycache__')
    if spec_cache.exists():
        shutil.rmtree(spec_cache)
        print(f"  - Removed {spec_cache}/")
    
    print("Clean complete.\n")


def build_executable():
    """Run PyInstaller with the spec file"""
    print("Building executable with PyInstaller...")
    print("This may take a few minutes...\n")
    
    try:
        # Run PyInstaller with the spec file
        result = subprocess.run(
            ['pyinstaller', 'ChartPreparation.spec', '--clean'],
            check=True,
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        
        if result.returncode == 0:
            print("\n" + "=" * 60)
            print("BUILD SUCCESSFUL!")
            print("=" * 60)
            
            exe_path = Path('dist/ChartPreparation.exe')
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"\nExecutable created: {exe_path}")
                print(f"File size: {size_mb:.2f} MB")
                print("\nYou can now distribute ChartPreparation.exe to users.")
            else:
                print("\nWarning: Executable not found at expected location.")
            
            return True
        else:
            print("\n" + "=" * 60)
            print("BUILD FAILED")
            print("=" * 60)
            print(result.stderr)
            return False
            
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 60)
        print("BUILD FAILED")
        print("=" * 60)
        print(f"Error: {e}")
        print(e.stderr)
        return False
    except FileNotFoundError:
        print("\n" + "=" * 60)
        print("ERROR: PyInstaller not found")
        print("=" * 60)
        print("Please install PyInstaller first:")
        print("  pip install pyinstaller")
        return False


def main():
    print("=" * 60)
    print("Chart Preparation Utility - Build Script")
    print("=" * 60)
    print()
    
    # Check if we're on Windows (recommended)
    if sys.platform != 'win32':
        print("WARNING: You are not on Windows!")
        print("Building a Windows exe on a non-Windows platform may not work correctly.")
        print("It's recommended to build on Windows or use a Windows VM.")
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Build cancelled.")
            return
        print()
    
    # Clean old builds
    clean_build_directories()
    
    # Build the executable
    success = build_executable()
    
    if success:
        print("\nNext steps:")
        print("1. Test the executable: dist/ChartPreparation.exe")
        print("2. Verify the version info in the UI")
        print("3. Test with both Daily and Index CSV files")
        print("4. Distribute the exe to users")
    else:
        print("\nPlease fix the errors and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
