"""
Log viewer for MSR605 Card Reader.
"""

import os
import re
import sys
from pathlib import Path
from typing import Optional, Dict, Any

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

        # Update buttons
        self.refresh_btn.setText(self.translate("refresh"))
        self.clear_btn.setText(self.translate("clear_log"))
        self.save_btn.setText(self.translate("save_as"))
        self.close_btn.setText(self.translate("close"))

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

        # Log level filters
        self.filter_group = QGroupBox()
        self.filter_layout = QHBoxLayout()
        self.filter_group.setLayout(self.filter_layout)

        self.filters = {
            "debug": QCheckBox("DEBUG"),
            "info": QCheckBox("INFO"),
            "warning": QCheckBox("WARNING"),
            "error": QCheckBox("ERROR"),
            "critical": QCheckBox("CRITICAL"),
        }

        # Set all filters to checked by default
        for level, checkbox in self.filters.items():
            checkbox.setChecked(True)
            self.filter_layout.addWidget(checkbox)
            checkbox.stateChanged.connect(self.apply_filters)

        self.filter_layout.addStretch()

        # Buttons with translations
        self.refresh_btn = QPushButton()
        self.clear_btn = QPushButton()
        self.save_btn = QPushButton()
        self.close_btn = QPushButton()

        # Setup layout
        top_layout = QHBoxLayout()
        self.file_label = QLabel()
        top_layout.addWidget(self.file_label)
        top_layout.addWidget(self.log_selector, 1)
        top_layout.addStretch()

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
        self.clear_btn.clicked.connect(self.clear_log)
        self.save_btn.clicked.connect(self.save_log)
        self.close_btn.clicked.connect(self.accept)
        self.log_selector.currentIndexChanged.connect(self.load_selected_log)

    def get_log_dir(self) -> Path:
        """Get the directory containing log files."""
        # First try the application's logs directory
        app_log_dir = Path(__file__).parent.parent / "logs"
        if app_log_dir.exists():
            return app_log_dir

        # Fall back to user's home directory if app directory not found
        home_log_dir = Path.home() / ".config" / "image-deduplicator" / "logs"
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

    def load_selected_log(self, index: int):
        """Load the selected log file."""
        if (
            self.log_selector.count() == 0
            or self.log_selector.currentText() == self.translate("no_logs_found")
        ):
            return

        log_file = self.get_log_dir() / self.log_selector.currentText()
        if log_file.exists():
            self.load_log_file(log_file)

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

    def apply_filters(self):
        """Apply the selected log level filters."""
        if not hasattr(self, "current_log_content"):
            return

        selected_levels = [
            level.upper()
            for level, checkbox in self.filters.items()
            if checkbox.isChecked()
        ]

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

        self.text_edit.setPlainText("\n".join(filtered_lines))

        # Scroll to bottom
        cursor = self.text_edit.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.text_edit.setTextCursor(cursor)

    def clear_log(self):
        """Clear the current log display."""
        self.text_edit.clear()

    def save_log(self):
        """Save the current log display to a file."""
        if not self.text_edit.toPlainText():
            QMessageBox.information(
                self, self.translate("save_log"), self.translate("no_log_to_save")
            )
            return

        file_name, _ = QFileDialog.getSaveFileName(
            self, self.translate("save_log_as"), "", "Log Files (*.log);;All Files (*)"
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
