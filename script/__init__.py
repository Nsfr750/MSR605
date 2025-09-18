"""
MSR605 Python Interface - Core Package

This package provides the core functionality for interacting with the MSR605 magnetic stripe card reader/writer.
"""

# Import key components to make them available at the package level
from .UI import GUI
from .app_menu import AppMenuBar
from .language_manager import LanguageManager
from . import translations
from .version import get_version, get_version_info

__version__ = get_version()
__version_info__ = get_version_info()
__author__ = "Nsfr750"
__license__ = "GPLv3"
