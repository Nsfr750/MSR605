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
        self._autofill_pin_block_from_tracks()

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
        self.setup_pin_decode_tab()
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

    def setup_pin_decode_tab(self):
        """Set up the PIN block decode tab."""
        # Create PIN decode tab widget
        pin_tab = QWidget()
        pin_layout = QVBoxLayout(pin_tab)

        # PIN block input
        block_group = QGroupBox("PIN Block")
        block_layout = QVBoxLayout()

        # Encrypted PIN block (hex)
        block_row = QWidget()
        block_row_layout = QHBoxLayout(block_row)
        block_row_layout.setContentsMargins(0, 0, 0, 0)

        block_row_layout.addWidget(QLabel("Encrypted PIN block (hex):"))
        self.pin_block_entry = QLineEdit()
        self.pin_block_entry.setPlaceholderText("16 hex digits, e.g. BAFB0C0F6A2C7DEE")
        block_row_layout.addWidget(self.pin_block_entry)
        block_layout.addWidget(block_row)

        # PAN input with auto-fill from track data
        pan_row = QWidget()
        pan_row_layout = QHBoxLayout(pan_row)
        pan_row_layout.setContentsMargins(0, 0, 0, 0)

        pan_row_layout.addWidget(QLabel("PAN (card number):"))
        self.pin_pan_entry = QLineEdit()
        self.pin_pan_entry.setPlaceholderText("Primary Account Number from track data")
        pan_row_layout.addWidget(self.pin_pan_entry)

        self.pin_pan_btn = QPushButton("Use Track PAN")
        self.pin_pan_btn.clicked.connect(self.fill_pan_from_tracks)
        pan_row_layout.addWidget(self.pin_pan_btn)
        block_layout.addWidget(pan_row)

        block_group.setLayout(block_layout)
        pin_layout.addWidget(block_group)

        # Key and format parameters
        params_group = QGroupBox("Decryption Parameters")
        params_layout = QVBoxLayout()

        key_row = QWidget()
        key_row_layout = QHBoxLayout(key_row)
        key_row_layout.setContentsMargins(0, 0, 0, 0)

        key_row_layout.addWidget(QLabel("PIN key (hex):"))
        self.pin_key_entry = QLineEdit()
        self.pin_key_entry.setPlaceholderText("8/16/24 bytes (DES/3DES)")
        key_row_layout.addWidget(self.pin_key_entry)
        params_layout.addWidget(key_row)

        fmt_row = QWidget()
        fmt_row_layout = QHBoxLayout(fmt_row)
        fmt_row_layout.setContentsMargins(0, 0, 0, 0)

        fmt_row_layout.addWidget(QLabel("Key type:"))
        self.pin_key_type_combo = QComboBox()
        self.pin_key_type_combo.addItems(
            [
                "Single DES (8 bytes)",
                "3DES double-length (16 bytes)",
                "3DES triple-length (24 bytes)",
            ]
        )
        self.pin_key_type_combo.setCurrentIndex(1)
        fmt_row_layout.addWidget(self.pin_key_type_combo)

        fmt_row_layout.addWidget(QLabel("PIN block format:"))
        self.pin_format_combo = QComboBox()
        self.pin_format_combo.addItems(
            [
                "ISO 9564 format 0 (ISO-0)",
                "ISO 9564 format 1 (ISO-1 / ECI-4)",
                "ISO 9564 format 3 (ISO-3)",
                "VISA-1",
                "VISA-3",
                "VISA-4",
            ]
        )
        self.pin_format_combo.currentIndexChanged.connect(self._on_pin_format_changed)
        fmt_row_layout.addWidget(self.pin_format_combo)
        fmt_row_layout.addStretch()
        params_layout.addWidget(fmt_row)

        params_group.setLayout(params_layout)
        pin_layout.addWidget(params_group)

        # Decode button
        decode_pin_btn = QPushButton("Decode PIN")
        decode_pin_btn.clicked.connect(self.decode_pin)
        decode_pin_btn.setStyleSheet(
            """
            QPushButton {
                padding: 8px;
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
        pin_layout.addWidget(decode_pin_btn)

        # Results area
        pin_layout.addWidget(QLabel("<b>PIN Decode Result:</b>"))

        self.pin_result_text = QTextEdit()
        self.pin_result_text.setReadOnly(True)
        self.pin_result_text.setStyleSheet(
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
        pin_layout.addWidget(self.pin_result_text)

        # Add to tab widget
        self.tab_widget.addTab(pin_tab, "PIN Decode")

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

        self._autofill_pin_block_from_tracks()

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

    def set_encrypted_pin_block(self, pin_block_hex: str) -> None:
        """Fill the encrypted PIN block field, e.g. after a card read.

        Args:
            pin_block_hex: The 16-hex-digit encrypted PIN block
        """
        self.pin_block_entry.setText(pin_block_hex)

    def _autofill_pin_block_from_tracks(self):
        """Auto-fill the PIN block field from Track 2 discretionary data."""
        try:
            from .decrypt import extract_pin_block_from_track2

            pin_block = extract_pin_block_from_track2(self.tracks[1])
            if pin_block:
                self.set_encrypted_pin_block(pin_block)
        except Exception as e:
            logger.warning(f"Could not auto-fill PIN block: {e}")

    def fill_pan_from_tracks(self):
        """Fill the PAN field using the card number decoded from track data."""
        pan = self._extract_pan_from_tracks()
        if pan:
            self.pin_pan_entry.setText(pan)
        else:
            QMessageBox.information(
                self,
                "No PAN Found",
                "No card number could be decoded from the loaded track data.",
            )

    def _extract_pan_from_tracks(self) -> str:
        """Extract the PAN from the loaded track data.

        Prefers Track 2 (;PAN=...) and falls back to Track 1 (%BPAN^...).

        Returns:
            The card number as a string of digits, or an empty string
        """
        if len(self.tracks) > 1 and "=" in self.tracks[1]:
            return self.tracks[1].lstrip(";").split("=")[0].strip()
        if (
            len(self.tracks) > 0
            and self.tracks[0].startswith("%B")
            and "^" in self.tracks[0]
        ):
            return self.tracks[0][2:].split("^")[0].strip()
        return ""

    def _on_pin_format_changed(self, index: int):
        """Enable the PAN field only for PIN block formats that use it.

        Args:
            index: Selected index in the PIN block format combo
        """
        # ECI-4 (ISO-1) at index 1 and VISA-3 at index 4 don't use the PAN
        pan_needed = index not in (1, 4)
        self.pin_pan_entry.setEnabled(pan_needed)
        self.pin_pan_btn.setEnabled(pan_needed)

    def decode_pin(self):
        """Decode the encrypted PIN block using the provided key and PAN."""
        pin_block_hex = self.pin_block_entry.text().strip().replace(" ", "")
        pan = self.pin_pan_entry.text().strip()
        key_hex = self.pin_key_entry.text().strip().replace(" ", "")

        try:
            from .decrypt import CardDataDecryptor, KeyType, PinBlockFormat
        except ImportError as e:
            QMessageBox.critical(
                self,
                "Decryption Unavailable",
                f"The decryption module could not be loaded:\n{str(e)}",
            )
            return

        pin_formats = [
            PinBlockFormat.ISO9564_1,
            PinBlockFormat.ECI4,
            PinBlockFormat.ISO9564_3,
            PinBlockFormat.VISA1,
            PinBlockFormat.VISA3,
            PinBlockFormat.VISA4,
        ]
        pin_block_format = pin_formats[self.pin_format_combo.currentIndex()]

        # ECI-4 (ISO-1) and VISA-3 don't use the PAN
        pan_needed = pin_block_format not in (
            PinBlockFormat.ECI4,
            PinBlockFormat.VISA3,
        )

        if not pin_block_hex or not key_hex or (pan_needed and not pan):
            QMessageBox.warning(
                self,
                "Missing Input",
                "Encrypted PIN block, key"
                + (" and PAN" if pan_needed else "")
                + " are required.",
            )
            return

        try:
            pin_block = bytes.fromhex(pin_block_hex)
        except ValueError:
            QMessageBox.critical(
                self,
                "Invalid Input",
                "The encrypted PIN block must be a hexadecimal string "
                "(16 hex digits).",
            )
            return

        try:
            key = bytes.fromhex(key_hex)
        except ValueError:
            QMessageBox.critical(
                self,
                "Invalid Input",
                "The key must be a hexadecimal string.",
            )
            return

        key_type = [
            KeyType.SINGLE_DES,
            KeyType.DOUBLE_DES,
            KeyType.TRIPLE_DES,
        ][self.pin_key_type_combo.currentIndex()]

        try:
            decryptor = CardDataDecryptor(key, key_type=key_type)
        except ValueError as e:
            QMessageBox.critical(self, "Invalid Key", str(e))
            return

        result = decryptor.decrypt_pin_block(pin_block, pan, pin_block_format)

        if result.success:
            self.pin_result_text.setPlainText(
                f"Decoded PIN : {result.data}\n\n"
                f"PIN length  : {result.metadata.get('pin_length', '')}\n"
                f"Format      : {result.metadata.get('pin_block_format', '')}\n"
                f"Algorithm   : {result.algorithm}\n"
                f"Key type    : {result.key_type}\n"
                f"Timestamp   : {result.timestamp}"
            )
        else:
            self.pin_result_text.setPlainText(f"PIN decoding failed:\n{result.error}")

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
