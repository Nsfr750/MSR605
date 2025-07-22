#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyPI Publisher Script for MSR605 Tool

This script automates the process of building and uploading the MSR605 Tool package to PyPI.
It handles package building, version checking, and secure API token authentication.

Usage:
    python publish_to_pypi.py [--test] [--token YOUR_API_TOKEN] [--save-token]

Environment Variables:
    PYPI_API_TOKEN: Your PyPI API token (can be set instead of using --token)
"""

import os
import sys
import shutil
import subprocess
import getpass
from pathlib import Path
import argparse
import json
import keyring
import keyring.errors
from typing import Optional, List, Tuple

# Project configuration
PROJECT_NAME = "msr605-tool"
PYPI_TEST_URL = "https://test.pypi.org/legacy/"
PYPI_PROD_URL = "https://upload.pypi.org/legacy/"
PROJECT_ROOT = Path(__file__).parent
DIST_DIR = PROJECT_ROOT / "dist"
KEYRING_SERVICE = f"pypi-{PROJECT_NAME}"


def get_saved_token() -> Optional[str]:
    """Retrieve the saved PyPI API token from the system keyring."""
    try:
        return keyring.get_password(KEYRING_SERVICE, "pypi-token")
    except (keyring.errors.NoKeyringError, keyring.errors.InitError):
        print("Warning: No system keyring available. Cannot securely store API token.")
        return None


def save_token(token: str) -> bool:
    """Save the PyPI API token to the system keyring."""
    try:
        keyring.set_password(KEYRING_SERVICE, "pypi-token", token)
        print("API token saved securely in system keyring.")
        return True
    except (keyring.errors.NoKeyringError, keyring.errors.InitError) as e:
        print(f"Warning: Could not save token to keyring: {e}")
        return False


def delete_token() -> bool:
    """Delete the saved PyPI API token."""
    try:
        keyring.delete_password(KEYRING_SERVICE, "pypi-token")
        print("Saved API token has been deleted.")
        return True
    except keyring.errors.PasswordDeleteError:
        print("No saved API token found to delete.")
        return False
    except (keyring.errors.NoKeyringError, keyring.errors.InitError) as e:
        print(f"Warning: Could not access keyring: {e}")
        return False


def run_command(cmd: List[str], cwd: Optional[Path] = None) -> bool:
    """Run a shell command and return True if successful."""
    try:
        print(f"\nRunning: {' '.join(cmd)}")
        result = subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(e.cmd)}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False


def check_installed(package: str) -> bool:
    """Check if a Python package is installed."""
    try:
        __import__(package)
        return True
    except ImportError:
        return False


def install_package(package: str) -> bool:
    """Install a Python package using pip."""
    print(f"Installing {package}...")
    return run_command([sys.executable, "-m", "pip", "install", "--upgrade", package])


def clean_directory(directory: Path) -> bool:
    """Remove all files in the specified directory."""
    if not directory.exists():
        return True
    
    print(f"Cleaning {directory}...")
    try:
        for item in directory.glob("*"):
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
        return True
    except Exception as e:
        print(f"Error cleaning {directory}: {e}")
        return False


def build_package() -> bool:
    """Build the Python package."""
    print("\n" + "="*50)
    print("Building package...")
    print("="*50)
    
    # Clean the dist directory
    if not clean_directory(DIST_DIR):
        return False
    
    # Ensure build is installed
    if not check_installed("build"):
        if not install_package("build"):
            return False
    
    # Build the package
    if not run_command([sys.executable, "-m", "build", "--no-isolation"], PROJECT_ROOT):
        return False
    
    # Verify the distribution files were created
    dist_files = list(DIST_DIR.glob("*.whl")) + list(DIST_DIR.glob("*.tar.gz"))
    if not dist_files:
        print("Error: No distribution files were created.")
        return False
    
    print("\nCreated distribution files:")
    for f in dist_files:
        print(f"  - {f.name}")
    
    return True


def upload_to_pypi(test: bool = False, token: Optional[str] = None) -> bool:
    """Upload the package to PyPI using twine with API token authentication."""
    print("\n" + "="*50)
    print(f"Uploading to {'TestPyPI' if test else 'PyPI'}...")
    print("="*50)
    
    # Ensure twine is installed
    if not check_installed("twine"):
        if not install_package("twine"):
            return False
    
    # Get API token
    if not token:
        token = os.getenv("PYPI_API_TOKEN")
        if not token:
            token = getpass.getpass("Enter your PyPI API token (input will be hidden): ")
    
    if not token:
        print("Error: No API token provided. Set PYPI_API_TOKEN environment variable or use --token")
        return False
    
    # Set the repository URL
    repository_url = PYPI_TEST_URL if test else PYPI_PROD_URL
    
    # Upload using twine with the API token
    cmd = [
        sys.executable, "-m", "twine", "upload", "--non-interactive",
        "--repository-url", repository_url,
        "--username", "__token__",
        "--password", token,
        str(DIST_DIR / "*")
    ]
    
    if not run_command(cmd, PROJECT_ROOT):
        print(f"\nError uploading to {'TestPyPI' if test else 'PyPI'}")
        return False
    
    print(f"\nSuccessfully uploaded to {'TestPyPI' if test else 'PyPI'}!")
    return True


def main():
    """Main function to handle command line arguments and execute the publishing process."""
    parser = argparse.ArgumentParser(description=f"Publish {PROJECT_NAME} to PyPI")
    parser.add_argument(
        "--test", 
        action="store_true", 
        help="Upload to TestPyPI instead of PyPI"
    )
    parser.add_argument(
        "--token", 
        type=str, 
        help="PyPI API token (can also be set via PYPI_API_TOKEN environment variable)",
        default=None
    )
    parser.add_argument(
        "--save-token",
        action="store_true",
        help="Save the provided or entered API token for future use"
    )
    parser.add_argument(
        "--delete-token",
        action="store_true",
        help="Delete any saved API token"
    )
    
    args = parser.parse_args()
    
    print(f"\n{'='*50}")
    print(f"{PROJECT_NAME} Publisher")
    print("="*50)
    
    # Handle token management
    if args.delete_token:
        delete_token()
        return
    
    # If token is provided and --save-token is set, save it
    if args.save_token and args.token:
        save_token(args.token)
    
    # Build the package
    if not build_package():
        sys.exit(1)
    
    # Upload to PyPI
    if not upload_to_pypi(test=args.test, token=args.token):
        sys.exit(1)
    
    # If --save-token was used without --token, save the token from environment or prompt
    if args.save_token and not args.token:
        token = os.getenv("PYPI_API_TOKEN") or getpass.getpass("\nEnter your PyPI API token to save for future use (input will be hidden): ")
        if token:
            save_token(token)
    
    print("\n" + "="*50)
    print("Publishing completed successfully!")
    print("="*50)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)
