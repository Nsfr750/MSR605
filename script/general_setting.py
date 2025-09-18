#!/usr/bin/env python3

"""
General Settings Module for MSR605 Card Reader/Writer.
This module contains the general settings UI components including coercivity and database settings.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QRadioButton, QCheckBox, QLabel
)
from PyQt6.QtCore import pyqtSignal


class GeneralSettingsWidget(QWidget):
    """
    Widget for general application settings including coercivity and database options.
    """
    
    # Signals to notify parent of changes
    coercivity_changed = pyqtSignal(str)
    auto_save_changed = pyqtSignal(bool)
    allow_duplicates_changed = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        """
        Initialize the general settings widget.
        
        Args:
            parent: The parent widget
        """
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        
        # Coercivity settings
        coercivity_group = QGroupBox("Coercivity")
        coercivity_layout = QVBoxLayout()
        
        self.hi_coercivity = QRadioButton("High Coercivity (300 Oe)")
        self.lo_coercivity = QRadioButton("Low Coercivity (300 Oe)")
        
        # Default to high coercivity
        self.hi_coercivity.setChecked(True)
        
        # Connect signals
        self.hi_coercivity.toggled.connect(self.on_coercivity_changed)
        
        coercivity_layout.addWidget(self.hi_coercivity)
        coercivity_layout.addWidget(self.lo_coercivity)
        coercivity_group.setLayout(coercivity_layout)
        
        # Database settings
        db_group = QGroupBox("Database Settings")
        db_layout = QVBoxLayout()
        
        self.auto_save = QCheckBox("Auto-save read cards to database")
        self.allow_duplicates = QCheckBox("Allow duplicate cards in database")
        
        # Connect signals
        self.auto_save.toggled.connect(self.on_auto_save_changed)
        self.allow_duplicates.toggled.connect(self.on_allow_duplicates_changed)
        
        db_layout.addWidget(self.auto_save)
        db_layout.addWidget(self.allow_duplicates)
        db_group.setLayout(db_layout)
        
        # Add groups to layout
        layout.addWidget(coercivity_group)
        layout.addWidget(db_group)
        layout.addStretch()
        
    def on_coercivity_changed(self):
        """Handle coercivity radio button changes."""
        coercivity = "hi" if self.hi_coercivity.isChecked() else "lo"
        self.coercivity_changed.emit(coercivity)
        
    def on_auto_save_changed(self, checked):
        """Handle auto-save checkbox changes."""
        self.auto_save_changed.emit(checked)
        
    def on_allow_duplicates_changed(self, checked):
        """Handle allow duplicates checkbox changes."""
        self.allow_duplicates_changed.emit(checked)
        
    def set_coercivity(self, coercivity):
        """
        Set the coercivity value.
        
        Args:
            coercivity (str): 'hi' or 'lo'
        """
        if coercivity == "hi":
            self.hi_coercivity.setChecked(True)
        else:
            self.lo_coercivity.setChecked(True)
            
    def set_auto_save(self, enabled):
        """
        Set the auto-save checkbox state.
        
        Args:
            enabled (bool): Whether auto-save is enabled
        """
        self.auto_save.setChecked(enabled)
        
    def set_allow_duplicates(self, enabled):
        """
        Set the allow duplicates checkbox state.
        
        Args:
            enabled (bool): Whether duplicates are allowed
        """
        self.allow_duplicates.setChecked(enabled)
        
    def get_coercivity(self):
        """
        Get the current coercivity setting.
        
        Returns:
            str: 'hi' or 'lo'
        """
        return "hi" if self.hi_coercivity.isChecked() else "lo"
        
    def get_auto_save(self):
        """
        Get the current auto-save setting.
        
        Returns:
            bool: Whether auto-save is enabled
        """
        return self.auto_save.isChecked()
        
    def get_allow_duplicates(self):
        """
        Get the current allow duplicates setting.
        
        Returns:
            bool: Whether duplicates are allowed
        """
        return self.allow_duplicates.isChecked()
