#!/usr/bin/env python3

"""
General Settings Module for MSR605 Card Reader/Writer.
This module contains the general settings UI components including coercivity and database settings.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QRadioButton, QCheckBox, QLabel, QComboBox, QPushButton, QMessageBox
)
from PyQt6.QtCore import pyqtSignal
import sys
import os


class GeneralSettingsWidget(QWidget):
    """
    Widget for general application settings including coercivity and database options.
    """
    
    # Signals to notify parent of changes
    coercivity_changed = pyqtSignal(str)
    auto_save_changed = pyqtSignal(bool)
    allow_duplicates_changed = pyqtSignal(bool)
    language_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        """
        Initialize the general settings widget.
        
        Args:
            parent: The parent widget
        """
        super().__init__(parent)
        self.parent = parent
        self.language_manager = None
        self.init_ui()
        
    def set_language_manager(self, language_manager):
        """
        Set the language manager for translations.
        
        Args:
            language_manager: The language manager instance
        """
        self.language_manager = language_manager
        if self.language_manager:
            # Connect to language changes
            self.language_manager.language_changed.connect(self.retranslate_ui)
            self.retranslate_ui()
        
    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        
        # Coercivity settings
        self.coercivity_group = QGroupBox("Coercivity")
        coercivity_layout = QVBoxLayout()
        
        self.hi_coercivity = QRadioButton("High Coercivity (300 Oe)")
        self.lo_coercivity = QRadioButton("Low Coercivity (300 Oe)")
        
        # Default to high coercivity
        self.hi_coercivity.setChecked(True)
        
        # Connect signals
        self.hi_coercivity.toggled.connect(self.on_coercivity_changed)
        
        coercivity_layout.addWidget(self.hi_coercivity)
        coercivity_layout.addWidget(self.lo_coercivity)
        self.coercivity_group.setLayout(coercivity_layout)
        
        # Language settings
        self.language_group = QGroupBox("Language")
        language_layout = QVBoxLayout()
        
        self.language_combo = QComboBox()
        self.language_combo.addItem("English", "en")
        self.language_combo.addItem("Italiano", "it")
        
        # Add restart button
        self.restart_button = QPushButton("Apply Language Changes")
        self.restart_button.clicked.connect(self.on_language_changed)
        
        language_layout.addWidget(QLabel("Select Language:"))
        language_layout.addWidget(self.language_combo)
        language_layout.addWidget(self.restart_button)
        self.language_group.setLayout(language_layout)
        
        # Database settings
        self.db_group = QGroupBox("Database Settings")
        db_layout = QVBoxLayout()
        
        self.auto_save = QCheckBox("Auto-save read cards to database")
        self.allow_duplicates = QCheckBox("Allow duplicate cards in database")
        
        # Connect signals
        self.auto_save.toggled.connect(self.on_auto_save_changed)
        self.allow_duplicates.toggled.connect(self.on_allow_duplicates_changed)
        
        db_layout.addWidget(self.auto_save)
        db_layout.addWidget(self.allow_duplicates)
        self.db_group.setLayout(db_layout)
        
        # Add groups to layout
        layout.addWidget(self.coercivity_group)
        layout.addWidget(self.language_group)
        layout.addWidget(self.db_group)
        layout.addStretch()
        
    def retranslate_ui(self):
        """Retranslate UI elements based on current language."""
        if not self.language_manager:
            return
            
        t = self.language_manager.translate
        
        self.coercivity_group.setTitle(t("settings_coercivity"))
        self.hi_coercivity.setText(t("settings_hi_coercivity"))
        self.lo_coercivity.setText(t("settings_lo_coercivity"))
        
        self.language_group.setTitle(t("settings_language"))
        self.restart_button.setText(t("settings_apply_language"))
        
        self.db_group.setTitle(t("settings_database"))
        self.auto_save.setText(t("settings_auto_save"))
        self.allow_duplicates.setText(t("settings_allow_duplicates"))
        
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
        
    def on_language_changed(self):
        """Handle language change and restart application."""
        if not self.language_manager:
            return
            
        current_lang = self.language_manager.current_language
        selected_lang = self.language_combo.currentData()
        
        if selected_lang != current_lang:
            # Show confirmation dialog
            reply = QMessageBox.question(
                self,
                self.language_manager.translate("msg_language_change_title"),
                self.language_manager.translate("msg_language_change_confirm"),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                # Set the new language
                self.language_manager.set_language(selected_lang)
                
                # Restart the application
                self.restart_application()
        
    def restart_application(self):
        """Restart the application with the new language."""
        import subprocess
        import sys
        
        # Get the current script path
        script_path = os.path.abspath(sys.argv[0])
        
        # Restart the application
        try:
            # Close the current application
            if self.parent:
                self.parent.close()
            
            # Start new instance
            subprocess.Popen([sys.executable, script_path])
            
            # Exit the current process
            sys.exit(0)
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Restart Error",
                f"Failed to restart application: {str(e)}"
            )
        
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
            enabled (bool): True to enable auto-save
        """
        self.auto_save.setChecked(enabled)
        
    def set_allow_duplicates(self, enabled):
        """
        Set the allow duplicates checkbox state.
        
        Args:
            enabled (bool): True to allow duplicates
        """
        self.allow_duplicates.setChecked(enabled)
        
    def set_language(self, lang_code):
        """
        Set the selected language.
        
        Args:
            lang_code (str): Language code ('en', 'it', etc.)
        """
        index = self.language_combo.findData(lang_code)
        if index >= 0:
            self.language_combo.setCurrentIndex(index)
