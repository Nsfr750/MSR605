#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script for Linux using Nuitka
"""

import os
import shutil
import sys
import subprocess
from pathlib import Path

def run_command(cmd):
    """Run a shell command and check for errors"""
    print(f"Running: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        return False
    except FileNotFoundError as e:
        print(f"Command not found: {e}")
        return False

def clean_build():
    """Clean build directory"""
    build_dir = Path("build")
    dist_dir = Path("dist" if not hasattr(sys, "_MEIPASS") else sys._MEIPASS)
    
    print("Cleaning build directories...")
    for directory in [build_dir, dist_dir]:
        if directory.exists():
            print(f"Removing {directory}")
            shutil.rmtree(directory)

def build():
    """Build the application using Nuitka"""
    # Configuration
    main_script = "main.py"  # Change this to your main script
    app_name = "MSR605"
    # Set the path to your logo file (update this to your actual logo path)
    logo_path = os.path.join("assets", "about_icon.png")  # Update this path
    output_name = "MSR605.bin"  # The name you want for the output executable
    icon_path = os.path.join("assets", "icon.ico")  # Update this path
    # Use the Python interpreter from the virtual environment
    script_dir = os.path.dirname(os.path.abspath(__file__))
    python_executable = os.path.join(script_dir, '.venv', 'bin', 'python3')
    
    # Basic Nuitka command with minimal options
    cmd = [
        python_executable, "-m", "nuitka",
        "--standalone",
        "--follow-imports",
        "--output-dir=build",
        "--show-progress",
        "--show-memory",
        "--enable-plugin=pyqt6",
        "--include-qt-plugins=platforms",
        "--python-flag=no_site",
        "--static-libpython=no"
    ]
    
    # Add icon if specified
    if icon_path and os.path.exists(icon_path):
        cmd.append(f"--windows-icon-from-ico={icon_path}")
    
    # Add output name and main script
    cmd.extend([
        f"--output-filename={output_name}",
        main_script
    ])
    
    # If logo exists, include it in the build
    if os.path.exists(logo_path):
        cmd.append(f"--include-data-files={logo_path}=icon.png")
    
    # Run the build
    if not run_command(cmd):
        print("Build failed!")
        return False
    
    print("\nBuild completed successfully!")
    print(f"Executable is in: build/{app_name}.dist/{output_name}")
    return True

def main():
    print("=== MSR605 Linux Build Script ===\n")
    
    # Clean previous builds
    clean_build()
    
    # Run the build
    if not build():
        sys.exit(1)
    
    print("\nDone!")

if __name__ == "__main__":
    main()
