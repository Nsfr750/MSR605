"""
MSR605 Python Interface - Core Package

This package provides the core functionality for interacting with the MSR605 magnetic stripe card reader/writer.
"""

# Import key components to make them available at the package level
from .UI import GUI
from .menu import MenuBar
from .language_manager import LanguageManager
from . import translations

__version__ = '2.3.0'
__author__ = 'Nsfr750'
__license__ = 'GPLv3'
