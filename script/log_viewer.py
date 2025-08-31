"""
Log viewer dialog for MSR605 Card Reader.
"""

import os
import re
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List

# Import logger first
from .logger import logger

try:
    from send2trash import send2trash
    SEND2TRASH_AVAILABLE = True
except ImportError:
    SEND2TRASH_AVAILABLE = False
    logger.warning("send2trash module not available. Log files will be permanently deleted.")

from PyQt6.QtCore import Qt, QSize, QTimer, QFile, QTextStream, pyqtSignal
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QFileDialog,
    QMessageBox,
    QApplication,
    QSizePolicy,
    QComboBox,
    QLabel,
    QCheckBox,
    QGroupBox,
    QWidget,
    QStyle,
)

# Import logger and language manager
from .logger import logger
from script.language_manager import LanguageManager


class LogViewer(QDialog):
    """A dialog for viewing application logs."""

    def __init__(self, parent=None, language_manager: Optional[LanguageManager] = None):
        super().__init__(parent)

        # Initialize language manager
        self.lang_manager = language_manager or LanguageManager()

        # Connect language changed signal
        if self.lang_manager:
            self.lang_manager.language_changed.connect(self.on_language_changed)

        self.setup_ui()
        self.setup_connections()
        self.refresh_log_list()

        # Set up auto-refresh timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_log_list)
        self.timer.start(5000)  # Refresh every 5 seconds

    def translate(self, key: str, **kwargs) -> str:
        """Helper method to get translated text."""
        if hasattr(self, "lang_manager") and self.lang_manager:
            return self.lang_manager.translate(key, **kwargs)
        return key

    def on_language_changed(self, lang_code: str) -> None:
        """Handle language change."""
        self.retranslate_ui()

    def retranslate_ui(self) -> None:
        """Retranslate the UI elements."""
        self.setWindowTitle(self.translate("log_viewer"))
        self.filter_group.setTitle(self.translate("log_level_filters"))
        self.file_label.setText(f"{self.translate('select_log_file')}:")

        # Update filter checkboxes
        for level, checkbox in self.filters.items():
            checkbox.setText(level.upper())
            
        # Update filter type combo box
        current_index = self.filter_type_combo.currentIndex()
        self.filter_type_combo.blockSignals(True)
        self.filter_type_combo.clear()
        self.filter_type_combo.addItem(self.translate("ALL"), "all")
        self.filter_type_combo.addItem(self.translate("DEBUG"), "debug")
        self.filter_type_combo.addItem(self.translate("INFO"), "info")
        self.filter_type_combo.addItem(self.translate("WARNING"), "warning")
        self.filter_type_combo.addItem(self.translate("ERROR"), "error")
        self.filter_type_combo.addItem(self.translate("CRITICAL"), "critical")
        self.filter_type_combo.addItem(self.translate("CUSTOM"), "custom")
        
        # Restore the previous selection if possible
        if 0 <= current_index < self.filter_type_combo.count():
            self.filter_type_combo.setCurrentIndex(current_index)
        self.filter_type_combo.blockSignals(False)

        # Update buttons
        self.refresh_btn.setText(self.translate("refresh"))
        self.delete_btn.setText(self.translate("delete_log"))
        self.clear_btn.setText(self.translate("clear_log"))
        self.save_btn.setText(self.translate("save_as"))
        self.close_btn.setText(self.translate("close"))
        
        # Update tooltips
        self.delete_btn.setToolTip(self.translate("delete_log_tooltip"))

    def setup_ui(self):
        """Set up the user interface."""
        self.setMinimumSize(1000, 700)

        # Create widgets
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

        # Log file selection
        self.log_selector = QComboBox()
        self.log_selector.setMinimumWidth(200)

        # Log level filters with dropdown
        self.filter_group = QGroupBox()
        self.filter_layout = QVBoxLayout()
        self.filter_group.setLayout(self.filter_layout)
        
        # Create a horizontal layout for the filter controls
        filter_controls = QHBoxLayout()
        
        # Add filter type label
        filter_label = QLabel(self.translate("filter_by") + ":")
        filter_controls.addWidget(filter_label)
        
        # Create filter type dropdown
        self.filter_type_combo = QComboBox()
        self.filter_type_combo.addItem(self.translate("all_levels"), "all")
        self.filter_type_combo.addItem(self.translate("debug_only"), "debug")
        self.filter_type_combo.addItem(self.translate("info_only"), "info")
        self.filter_type_combo.addItem(self.translate("warnings_only"), "warning")
        self.filter_type_combo.addItem(self.translate("errors_only"), "error")
        self.filter_type_combo.addItem(self.translate("critical_only"), "critical")
        self.filter_type_combo.addItem(self.translate("custom"), "custom")
        
        # Set default to "all levels"
        self.filter_type_combo.setCurrentIndex(0)
        
        # Add to layout
        filter_controls.addWidget(self.filter_type_combo, 1)  # Add stretch to push to left
        filter_controls.addStretch()
        
        # Add to main filter layout
        self.filter_layout.addLayout(filter_controls)
        
        # Create a container for the custom filter checkboxes
        self.custom_filter_container = QWidget()
        custom_filter_layout = QHBoxLayout()
        custom_filter_layout.setContentsMargins(0, 10, 0, 0)  # Add some top margin
        self.custom_filter_container.setLayout(custom_filter_layout)
        
        # Create checkboxes for custom filtering
        self.filters = {
            "debug": QCheckBox("DEBUG"),
            "info": QCheckBox("INFO"),
            "warning": QCheckBox("WARNING"),
            "error": QCheckBox("ERROR"),
            "critical": QCheckBox("CRITICAL"),
        }

        # Set all filters to checked by default and connect signals
        for level, checkbox in self.filters.items():
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(self.on_custom_filter_changed)
            custom_filter_layout.addWidget(checkbox)
        
        custom_filter_layout.addStretch()
        
        # Add the custom filter container to the main layout
        self.filter_layout.addWidget(self.custom_filter_container)
        
        # Initially hide the custom filters
        self.custom_filter_container.setVisible(False)
        
        # Connect filter type change signal
        self.filter_type_combo.currentIndexChanged.connect(self.on_filter_type_changed)

        # Buttons with translations
        self.refresh_btn = QPushButton()
        self.delete_btn = QPushButton()
        self.delete_btn.setToolTip(self.translate("delete_log_tooltip"))
        self.delete_btn.setEnabled(False)  # Disabled until a log is selected
        self.clear_btn = QPushButton()
        self.save_btn = QPushButton()
        self.close_btn = QPushButton()

        # Setup layout
        top_layout = QHBoxLayout()
        self.file_label = QLabel()
        top_layout.addWidget(self.file_label)
        top_layout.addWidget(self.log_selector, 1)
        
        # Add delete button to top right
        top_buttons = QHBoxLayout()
        self.delete_btn.setIcon(self.style().standardIcon(
            getattr(QStyle.StandardPixmap, 'SP_TrashIcon', None) or 
            getattr(QStyle.StandardPixmap, 'SP_DialogDiscardButton', None) or
            getattr(QStyle.StandardPixmap, 'SP_DialogCloseButton', None)
        ))
        top_buttons.addWidget(self.delete_btn)
        top_buttons.addStretch()
        top_layout.addLayout(top_buttons)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.close_btn)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.filter_group)
        main_layout.addWidget(self.text_edit, 1)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # Set initial translations
        self.retranslate_ui()

    def setup_connections(self):
        """Set up signal connections."""
        self.refresh_btn.clicked.connect(self.refresh_log_list)
        self.delete_btn.clicked.connect(self.delete_log)
        self.clear_btn.clicked.connect(self.clear_log)
        self.save_btn.clicked.connect(self.save_log)
        self.close_btn.clicked.connect(self.accept)
        self.log_selector.currentIndexChanged.connect(self.on_log_selected)

    def get_log_dir(self) -> Path:
        """Get the directory containing log files."""
        # First try the application's logs directory
        app_log_dir = Path(__file__).parent.parent / "logs"
        if app_log_dir.exists():
            return app_log_dir

        # Fall back to user's home directory if app directory not found
        home_log_dir = Path.home() / ".config" / "MSR605" / "logs"
        home_log_dir.mkdir(parents=True, exist_ok=True)
        return home_log_dir

    def refresh_log_list(self):
        """Refresh the list of available log files."""
        log_dir = self.get_log_dir()
        current_file = self.log_selector.currentText()

        self.log_selector.clear()

        # Get all log files
        log_files = sorted(log_dir.glob("*.log"), key=os.path.getmtime, reverse=True)

        if not log_files:
            self.log_selector.addItem(self.translate("no_logs_found"))
            self.text_edit.setPlainText(self.translate("no_logs_available"))
            return

        # Add log files to the combo box
        for log_file in log_files:
            self.log_selector.addItem(log_file.name)

        # Restore the previous selection if it still exists
        if current_file in [log.name for log in log_files]:
            index = self.log_selector.findText(current_file)
            if index >= 0:
                self.log_selector.setCurrentIndex(index)

        # Load the first log file by default
        if log_files and not current_file:
            self.load_log_file(log_files[0])

    def on_log_selected(self, index: int):
        """Handle log selection change."""
        if (
            self.log_selector.count() == 0
            or self.log_selector.currentText() == self.translate("no_logs_found")
        ):
            self.delete_btn.setEnabled(False)
            return

        log_file = self.get_log_dir() / self.log_selector.currentText()
        self.delete_btn.setEnabled(log_file.exists())
        
        if log_file.exists():
            self.load_log_file(log_file)
    
    # Keep the old method for compatibility
    def load_selected_log(self, index: int):
        """Load the selected log file. (Legacy method, use on_log_selected instead)"""
        self.on_log_selected(index)

    def load_log_file(self, log_file: Path):
        """Load the content of a log file."""
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                self.current_log_content = f.read()
            self.apply_filters()
        except Exception as e:
            logger.error(f"Error loading log file {log_file}: {e}")
            self.text_edit.setPlainText(
                self.translate("error_loading_log", error=str(e))
            )

    def on_filter_type_changed(self, index: int):
        """Handle changes in the filter type dropdown."""
        filter_type = self.filter_type_combo.currentData()
        
        # Show/hide custom filters based on selection
        if filter_type == "custom":
            self.custom_filter_container.setVisible(True)
        else:
            self.custom_filter_container.setVisible(False)
            
            # Update checkboxes based on selection
            for level, checkbox in self.filters.items():
                checkbox.setChecked(level == filter_type or filter_type == "all")
        
        # Apply the new filters
        self.apply_filters()
    
    def on_custom_filter_changed(self):
        """Handle changes to custom filter checkboxes."""
        # If custom filters are being used, update the dropdown to show "Custom"
        if self.filter_type_combo.currentData() != "custom":
            # Only update if not already on custom
            self.filter_type_combo.blockSignals(True)
            self.filter_type_combo.setCurrentText(self.translate("custom"))
            self.filter_type_combo.blockSignals(False)
        
        self.apply_filters()
    
    def apply_filters(self):
        """Apply the selected log level filters."""
        if not hasattr(self, "current_log_content"):
            return

        # Get selected filter type
        filter_type = self.filter_type_combo.currentData()
        
        # Determine which levels to show
        if filter_type == "all":
            selected_levels = [level.upper() for level in self.filters.keys()]
        elif filter_type == "custom":
            selected_levels = [
                level.upper()
                for level, checkbox in self.filters.items()
                if checkbox.isChecked()
            ]
        else:
            # Single level selected
            selected_levels = [filter_type.upper()]

        if not selected_levels:
            self.text_edit.setPlainText(self.translate("no_filters_selected"))
            return

        # Filter log lines by selected levels
        filtered_lines = []
        for line in self.current_log_content.split("\n"):
            if not line.strip():
                continue

            # Check if line contains any of the selected levels
            if any(f" {level} " in f" {line} " for level in selected_levels):
                filtered_lines.append(line)

        self.text_edit.setPlainText("\n".join(filtered_lines) or self.translate("no_matching_entries"))

        # Scroll to bottom
        cursor = self.text_edit.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.text_edit.setTextCursor(cursor)

    def clear_log(self):
        """Clear the current log display."""
        self.text_edit.clear()

    def delete_log(self):
        """Delete the currently selected log file using send2trash if available."""
        if self.log_selector.count() == 0 or not self.log_selector.currentText():
            return
            
        log_file = self.get_log_dir() / self.log_selector.currentText()
        if not log_file.exists():
            return
            
        # Ask for confirmation
        reply = QMessageBox.question(
            self,
            self.translate("confirm_delete"),
            self.translate("confirm_delete_log").format(file=log_file.name),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                if SEND2TRASH_AVAILABLE:
                    send2trash(str(log_file))
                    message = self.translate("log_moved_to_trash").format(file=log_file.name)
                else:
                    os.remove(log_file)
                    message = self.translate("log_permanently_deleted").format(file=log_file.name)
                
                # Refresh the log list
                self.refresh_log_list()
                
                # Show success message
                QMessageBox.information(
                    self,
                    self.translate("log_deleted"),
                    message
                )
                
            except Exception as e:
                logger.error(f"Error deleting log file: {e}")
                QMessageBox.critical(
                    self,
                    self.translate("error"),
                    self.translate("error_deleting_log", error=str(e)),
                )
    
    def save_log(self):
        """Save the current log display to a file."""
        if not self.text_edit.toPlainText():
            QMessageBox.information(
                self, self.translate("save_log"), self.translate("no_log_to_save")
            )
            return

        file_name, _ = QFileDialog.getSaveFileName(
            self, 
            self.translate("save_log_as"), 
            "", 
            "Log Files (*.log);;Text Files (*.txt);;All Files (*)"
        )

        if not file_name:
            return

        try:
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(self.text_edit.toPlainText())

            QMessageBox.information(
                self,
                self.translate("save_log"),
                self.translate("log_saved_successfully"),
            )
        except Exception as e:
            logger.error(f"Error saving log file: {e}")
            QMessageBox.critical(
                self,
                self.translate("error"),
                self.translate("error_saving_log", error=str(e)),
            )


if __name__ == "__main__":
    # Example usage
    app = QApplication(sys.argv)

    # Create a default language manager for testing
    from script.language_manager import LanguageManager

    lang_manager = LanguageManager()

    # Create and show the log viewer
    viewer = LogViewer(language_manager=lang_manager)
    viewer.show()

    sys.exit(app.exec())
