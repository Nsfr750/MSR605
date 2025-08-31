#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nuitka Build Script for MSR605 Card Reader/Writer

This script compiles the MSR605 application into a standalone executable using Nuitka.
It handles all necessary dependencies, data files, and platform-specific configurations.

Usage:
    python build_nuitka.py [--clean] [--onefile] [--windows-disable-console] [--include-qt-plugins]

Options:
    --clean                Clean build directory before building
    --onefile              Create a single executable file
    --windows-disable-console  Disable console window (Windows only)
    --include-qt-plugins   Include additional Qt plugins (may increase size)
"""

import os
import sys
import shutil
import subprocess
import platform
import argparse
from pathlib import Path
from script.version import __version__

# Project information
PROJECT_NAME = "MSR605"
MAIN_SCRIPT = "main.py"
VERSION_FILE = "script/version.py"
ASSETS_DIR = "assets"
CONFIG_DIR = "config"
LANG_DIR = "lang"
DOCS_DIR = "docs"

# Get version from version.py and ensure it's in Windows version format (X.Y.Z.W)
try:
    version = {}
    with open(VERSION_FILE, "r") as f:
        exec(f.read(), version)
    # Convert version to Windows format (X.Y.Z.W)
    version_parts = version["__version__"].replace('-', '.').split('.')
    while len(version_parts) < 4:
        version_parts.append('0')
    VERSION = '.'.join(version_parts[:4])  # Take first 4 parts
except Exception as e:
    print(f"Error reading version from {VERSION_FILE}: {e}")
    VERSION = "2.4.0.0"

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=f"Build {PROJECT_NAME} with Nuitka")
    parser.add_argument("--clean", action="store_true", help="Clean build directory before building")
    parser.add_argument("--windows-disable-console", action="store_true", 
                        help="Disable console window (Windows only)")
    return parser.parse_args()

def clean_build():
    """Clean build and dist directories."""
    print("Cleaning build directories...")
    for dir_name in ['build', 'dist', f'{PROJECT_NAME}.spec']:
        if os.path.exists(dir_name):
            try:
                if os.path.isdir(dir_name):
                    shutil.rmtree(dir_name)
                else:
                    os.remove(dir_name)
                print(f"Removed {dir_name}")
            except Exception as e:
                print(f"Error removing {dir_name}: {e}")

def get_nuitka_command(args):
    """Build the Nuitka command based on arguments."""
    # Base command
    # Base command with minimal required options
    cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",
        "--assume-yes-for-downloads",
        "--output-dir=dist",
        "---output-filename=MSR605-2.4.0.exe",
        "--windows-icon-from-ico=assets/icon.ico",
        "--follow-imports",
        "--remove-output",
        "--company-name=Tuxxle",
        "--product-name=MSR605",
        "--product-version=2.4.0.stable",
        "--file-version=2.4.0.stable",
        "--file-description=MSR605 - Card Reader/Writer",
        "--windows-disable-console",
        "--windows-company-name=Tuxxle",
        "--windows-file-version=2.4.0.0",
        "--windows-product-version=2.4.0.0",
        "--windows-product-name=MSR605",
        "--windows-file-description=MSR605 - Card Reader/Writer",
        "--copyright=© 2025 Nsfr750",
        "--enable-plugin=pyqt6",
        "--include-package=script",
        "--include-package=config",
        "--include-data-dir=assets=assets"
    ]

    # Add Windows-specific options
    if platform.system() == "Windows" and args.windows_disable_console:
        cmd.append("--windows-disable-console")
      
    # Add main script
    cmd.append(MAIN_SCRIPT)
    
    return [x for x in cmd if x]  # Remove empty strings

def build():
    """Build the application with Nuitka."""
    args = parse_arguments()
    
    if args.clean:
        clean_build()
    
    # Create necessary directories
    os.makedirs("build", exist_ok=True)
    
    # Build the command
    cmd = get_nuitka_command(args)
    
    print("Starting build with command:")
    print(" ".join(cmd))
    
    # Run the build
    try:
        subprocess.run(cmd, check=True)
        print("\nBuild completed successfully!")
        
        # Copy additional files for non-onefile builds
        if not args.onefile:
            print("Copying additional files...")
            build_dir = os.path.join("build", f"{PROJECT_NAME}.dist")
            if os.path.exists(build_dir):
                # Copy config directory
                if os.path.exists(CONFIG_DIR):
                    shutil.copytree(CONFIG_DIR, os.path.join(build_dir, CONFIG_DIR), dirs_exist_ok=True)
                # Copy language files
                if os.path.exists(LANG_DIR):
                    shutil.copytree(LANG_DIR, os.path.join(build_dir, LANG_DIR), dirs_exist_ok=True)
                # Copy documentation
                if os.path.exists(DOCS_DIR):
                    shutil.copytree(DOCS_DIR, os.path.join(build_dir, DOCS_DIR), dirs_exist_ok=True)
                
                print(f"\nBuild is ready in: {os.path.abspath(build_dir)}")
            
            print("\nTo create a distributable package, you can create a zip archive of the build directory.")
        else:
            print(f"\nStandalone executable created in: {os.path.abspath('build')}")
        
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed with error code {e.returncode}")
        sys.exit(1)
    except Exception as e:
        print(f"\nAn error occurred during build: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build()
