#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup script for MSR605 Card Reader/Writer application.

This script handles the packaging and distribution of the MSR605 application.
"""

import os
import sys
from pathlib import Path
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop

# Read the long description from README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Project metadata
NAME = "msr605-tool"
VERSION = "2.4.0"
DESCRIPTION = "Cross-platform tool for reading, writing, and analyzing magnetic stripe cards using the MSR605 reader/writer"
LONG_DESCRIPTION = long_description
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
