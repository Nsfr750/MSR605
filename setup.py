#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup script for MSR605 Card Reader/Writer application.

This script handles the packaging and distribution of the MSR605 application,
"""

import os
import sys
import subprocess
from pathlib import Path
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop

# Import version information
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "script"))
from version import (
    get_version,
    get_version_info,
    VERSION_MAJOR,
    VERSION_MINOR,
    VERSION_PATCH,
    VERSION_QUALIFIER,
)

# Create a PEP 440 compliant version string
VERSION = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"
if VERSION_QUALIFIER and VERSION_QUALIFIER != "stable":
    VERSION += (
        f"{VERSION_QUALIFIER[0]}{VERSION_QUALIFIER[1:]}"
        if VERSION_QUALIFIER[0].isdigit()
        else f".{VERSION_QUALIFIER}"
    )

# Read the long description from README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Project metadata
NAME = "msr605-tool"
VERSION = VERSION  # Use the PEP 440 compliant version string
DESCRIPTION = "Cross-platform tool for reading, writing, and analyzing magnetic stripe cards using the MSR605 reader/writer"
LONG_DESCRIPTION = """
MSR605 Tool is a comprehensive application for working with magnetic stripe cards using the MSR605 reader/writer device.

Features:
- Read, write, and erase magnetic stripe cards
- Support for all three tracks (1, 2, and 3)
- Encryption and decryption of card data
- Support for multiple card formats and standards
- User-friendly GUI built with PyQt6
- Command-line interface for automation
- Cross-platform support (Windows, macOS, Linux)
"""

AUTHOR = "Nsfr750"
AUTHOR_EMAIL = "nsfr750@yandex.com"


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        install.run(self)
        print("\n" + "=" * 50)
        print("MSR605 Tool has been successfully installed!")
        print("=" * 50)
        print("\nTo run the application, use one of these commands:")
        print("  - Command line: msr605-tool")
        print("  - GUI: msr605-tool-gui")
        print("\nFor more information, visit: https://github.com/Nsfr750/MSR605")
        print("=" * 50 + "\n")


class PostDevelopCommand(develop):
    """Post-installation for development mode."""

    def run(self):
        develop.run(self)
        print("\n" + "=" * 50)
        print("MSR605 Tool has been installed in development mode!")
        print("=" * 50)
        print("\nTo run the application in development mode, use:")
        print("  - Command line: python -m script.main")
        print("  - GUI: python -m script.main --gui")
        print("\nFor more information, visit: https://github.com/Nsfr750/MSR605")
        print("=" * 50 + "\n")


if __name__ == "__main__":
    setup(
        # This is intentionally minimal as most configuration is in pyproject.toml
        # We only specify cmdclass here
        cmdclass={
            "install": PostInstallCommand,
            "develop": PostDevelopCommand,
        },
    )
