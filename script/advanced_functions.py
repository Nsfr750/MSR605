import sys
import re
import logging
from typing import List, Optional, Dict, Union, Tuple
from datetime import datetime

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTabWidget,
    QCheckBox,
    QPushButton,
    QTextEdit,
    QLabel,
    QLineEdit,
    QRadioButton,
    QButtonGroup,
    QMessageBox,
    QGroupBox,
    QSizePolicy,
    QApplication,
    QFrame,
    QScrollArea,
    QComboBox,
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QObject
from PyQt6.QtGui import QFont, QTextCursor, QIcon

# Import visualization module
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from .visualization import VisualizationWidget

    VISUALIZATION_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Visualization features disabled: {e}")
    VISUALIZATION_AVAILABLE = False


class AdvancedFunctionsWidget(QWidget):
    """Widget containing advanced card data processing functions."""

    def __init__(
        self, parent: Optional[QWidget] = None, tracks: Optional[List[str]] = None
    ):
        """Initialize the advanced functions widget.

        Args:
            parent: Parent widget
            tracks: List of track data strings [track1, track2, track3]
        """
        super().__init__(parent)
        self.tracks = tracks or ["", "", ""]
        self.decryption_result = None

        self._setup_ui()

    def _setup_ui(self):
        """Set up the user interface."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)

        # Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # Create tabs
        self.setup_decode_tab()
        self.setup_decrypt_tab()

        # Add visualization tab if available
        if VISUALIZATION_AVAILABLE:
            self.setup_visualization_tab()

    def setup_decode_tab(self):
        """Set up the decode tab."""
        # Create decode tab widget
        decode_tab = QWidget()
        decode_layout = QVBoxLayout(decode_tab)

        # Track selection
        track_label = QLabel("Select Tracks to Decode:")
        track_label.setStyleSheet("font-weight: bold;")
        decode_layout.addWidget(track_label)

        # Track checkboxes
        self.track_checks = []
        track_frame = QWidget()
        track_frame_layout = QHBoxLayout(track_frame)
        track_frame_layout.setContentsMargins(0, 0, 0, 0)

        for i in range(3):
            check = QCheckBox(f"Track {i+1}")
            check.setChecked(True)
            self.track_checks.append(check)
            track_frame_layout.addWidget(check)

        track_frame_layout.addStretch()
        decode_layout.addWidget(track_frame)

        # Decode button
        decode_btn = QPushButton("Decode Selected Tracks")
        decode_btn.clicked.connect(self.decode_selected_tracks)
        decode_btn.setStyleSheet(
            """
            QPushButton {
                padding: 8px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003d7a;
            }
        """
        )
        decode_layout.addWidget(decode_btn)

        # Results area
        result_group = QGroupBox("Decoded Data")
        result_layout = QVBoxLayout(result_group)

        self.decode_text = QTextEdit()
        result_layout.addWidget(self.decode_text)

        decode_layout.addWidget(result_group)
        self.decode_text.setReadOnly(True)
        self.decode_text.setStyleSheet(
            """
            QTextEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
                font-family: monospace;
            }
        """
        )
        decode_layout.addWidget(self.decode_text)

        # Add tab
        self.tab_widget.addTab(decode_tab, "Decode Card")

    def setup_decrypt_tab(self):
        """Set up the decrypt tab."""
        # Create decrypt tab widget
        decrypt_tab = QWidget()
        decrypt_layout = QVBoxLayout(decrypt_tab)

        # Key input
        key_group = QGroupBox("Encryption Key")
        key_layout = QHBoxLayout()

        key_label = QLabel("Key (hex):")
        self.key_entry = QLineEdit()
        self.key_entry.setPlaceholderText("Enter encryption key...")

        key_layout.addWidget(key_label)
        key_layout.addWidget(self.key_entry)
        key_group.setLayout(key_layout)
        decrypt_layout.addWidget(key_group)

        # Algorithm selection
        algo_group = QGroupBox("Algorithm")
        algo_layout = QHBoxLayout()

        self.algo_group = QButtonGroup(self)
        algorithms = ["DES", "3DES", "AES-128", "AES-192", "AES-256"]

        for i, algo in enumerate(algorithms):
            radio = QRadioButton(algo)
            if i == 0:  # Default to DES
                radio.setChecked(True)
            self.algo_group.addButton(radio, i)
            algo_layout.addWidget(radio)

        algo_group.setLayout(algo_layout)
        decrypt_layout.addWidget(algo_group)

        # Data to decrypt
        data_group = QGroupBox("Data to Decrypt")
        data_layout = QVBoxLayout()

        self.data_text = QTextEdit()
        self.data_text.setPlaceholderText(
            "Enter data to decrypt or use 'Load Track Data'..."
        )
        data_layout.addWidget(self.data_text)

        data_group.setLayout(data_layout)
        decrypt_layout.addWidget(data_group)

        # Buttons
        btn_frame = QWidget()
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setContentsMargins(0, 0, 0, 0)

        load_btn = QPushButton("Load Track Data")
        load_btn.clicked.connect(self.load_track_data)

        decrypt_btn = QPushButton("Decrypt")
        decrypt_btn.clicked.connect(self.decrypt_data)
        decrypt_btn.setStyleSheet(
            """
            QPushButton {
                padding: 8px 16px;
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """
        )

        btn_layout.addWidget(load_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(decrypt_btn)

        decrypt_layout.addWidget(btn_frame)

        # Results area
        decrypt_layout.addWidget(QLabel("<b>Decryption Results:</b>"))

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setStyleSheet(
            """
            QTextEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
                font-family: monospace;
                background-color: #f8f9fa;
            }
        """
        )
        decrypt_layout.addWidget(self.result_text)

        # Add to tab widget
        self.tab_widget.addTab(decrypt_tab, "Decrypt Data")

    def setup_visualization_tab(self):
        """Set up the visualization tab."""
        # Create visualization tab widget
        visualization_tab = QWidget()
        visualization_layout = QVBoxLayout(visualization_tab)

        # Create visualization widget with current track data
        self.visualization_widget = VisualizationWidget(tracks=self.tracks)
        visualization_layout.addWidget(self.visualization_widget)

        # Add tab
        self.tab_widget.addTab(visualization_tab, "Visualization")

    def update_tracks(self, tracks: List[str]):
        """Update the track data in the widget.

        Args:
            tracks: List of track data strings [track1, track2, track3]
        """
        self.tracks = tracks or ["", "", ""]

        # Update visualization tab if available
        if hasattr(self, "visualization_widget"):
            self.visualization_widget.update_visualizations(self.tracks)

    def load_track_data(self):
        """Load track data into the decrypt text area."""
        selected_tracks = []
        for i, check in enumerate(self.track_checks):
            if check.isChecked() and i < len(self.tracks):
                selected_tracks.append(f"Track {i+1}: {self.tracks[i]}")

        self.data_text.clear()
        if selected_tracks:
            self.data_text.setPlainText("\n".join(selected_tracks))

    def decode_selected_tracks(self):
        """Decode the selected tracks and display results."""
        results = []
        for i, check in enumerate(self.track_checks):
            if check.isChecked() and i < len(self.tracks):
                track_data = self.tracks[i]
                if not track_data:
                    continue

                decoded = self._decode_track(track_data, i + 1)
                if decoded:
                    results.append(decoded)

        self.decode_text.clear()
        if results:
            self.decode_text.setPlainText("\n\n".join(results))
        else:
            self.decode_text.setPlainText(
                "No valid track data found in selected tracks."
            )

    def _decode_track(self, track_data: str, track_num: int) -> str:
        """Decode a single track's data.

        Args:
            track_data: Raw track data string
            track_num: Track number (1, 2, or 3)

        Returns:
            Formatted string with decoded track information
        """
        if not track_data:
            return ""

        result = [f"=== Track {track_num} ==="]

        # Try to parse track data based on format
        if track_num == 1 and "^" in track_data:
            # Track 1 format: %B1234567890123456^CARDHOLDER/NAME^YYMM...
            parts = track_data[2:].split("^")
            if len(parts) >= 3:
                result.append(f"Card Number: {parts[0]}")
                result.append(f"Cardholder: {parts[1].split('/')[0].strip()}")
                if len(parts[1].split("/")) > 1:
                    result.append(f"Last Name: {parts[1].split('/')[1].strip()}")
                if len(parts[2]) >= 4:
                    result.append(f"Expiration: {parts[2][2:4]}/{parts[2][:2]}")
                if len(parts[2]) >= 7:
                    result.append(f"Service Code: {parts[2][4:7]}")
        elif track_num in (2, 3) and "=" in track_data:
            # Track 2/3 format: ;1234567890123456=YYMM...
            parts = track_data[1:].split("=")
            if len(parts) >= 2:
                result.append(f"Card Number: {parts[0][:16]}")
                if len(parts[1]) >= 4:
                    result.append(f"Expiration: {parts[1][2:4]}/{parts[1][:2]}")
                if len(parts[1]) >= 7:
                    result.append(f"Service Code: {parts[1][4:7]}")

        # Add raw data
        result.append(f"\nRaw Data: {track_data}")
        return "\n".join(result)

    def decrypt_data(self):
        """Decrypt the provided data using the specified key and algorithm."""
        key = self.key_entry.text().strip()
        algorithm = self.algo_group.checkedButton().text()
        data = self.data_text.toPlainText().strip()

        if not key or not data:
            QMessageBox.critical(self, "Error", "Both key and data are required")
            return

        try:
            # TODO: Implement actual decryption using the decrypt.py module
            # For now, just show a placeholder
            result = f"Decrypted with {algorithm} and key {key}\n\n{data}"

            self.result_text.setPlainText(result)

        except Exception as e:
            QMessageBox.critical(
                self, "Decryption Error", f"Failed to decrypt data: {str(e)}"
            )


# Example usage
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Apply a stylesheet for consistent look
    app.setStyle("Fusion")

    # Sample track data for testing
    sample_tracks = [
        "%B1234567890123456^CARDHOLDER/NAME^24051010000000000000?",
        ";1234567890123456=24051010000000000000?",
        ";1234567890123456=24051010000000000000?",
    ]

    window = QWidget()
    window.setWindowTitle("Advanced Card Functions")

    layout = QVBoxLayout(window)

    frame = AdvancedFunctionsWidget(window, tracks=sample_tracks)
    layout.addWidget(frame)

    window.resize(800, 700)
    window.show()

    sys.exit(app.exec())
