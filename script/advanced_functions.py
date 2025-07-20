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

from script.language_manager import LanguageManager

# Import visualization module
try:
    from .visualization import VisualizationWidget

    VISUALIZATION_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Visualization features disabled: {e}")
    VISUALIZATION_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AdvancedFunctionsWidget(QWidget):
    """Widget containing advanced card data processing functions."""
    
    # Signal to request a card read from the parent
    read_card_requested = pyqtSignal()

    def __init__(
        self, 
        parent: Optional[QWidget] = None, 
        tracks: Optional[List[str]] = None,
        language_manager: Optional[LanguageManager] = None
    ):
        """Initialize the advanced functions widget.

        Args:
            parent: Parent widget
            tracks: List of track data strings [track1, track2, track3]
            language_manager: LanguageManager instance for translations
        """
        super().__init__(parent)
        self.tracks = tracks or ["", "", ""]
        self.decryption_result = None
        self.language_manager = language_manager or LanguageManager()
        
        # Connect language change signal if available
        if hasattr(self.language_manager, 'language_changed'):
            self.language_manager.language_changed.connect(self.retranslate_ui)

        self._setup_ui()
        self.retranslate_ui()

    def _setup_ui(self):
        """Set up the user interface."""
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        # Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # Create tabs
        self.setup_decode_tab()
        self.setup_decrypt_tab()

        # Add visualization tab if available
        if VISUALIZATION_AVAILABLE:
            self.setup_visualization_tab()

        # Add stretch to push everything to the top
        main_layout.addStretch()
        
    def retranslate_ui(self):
        """Update all UI text with current translations."""
        # Tab names
        if hasattr(self, 'tab_widget'):
            for i in range(self.tab_widget.count()):
                tab_text = self.tab_widget.tabText(i)
                # Map tab text to translation keys
                translation_map = {
                    "Decode Card": "adv_tab_decode",
                    "Decrypt Data": "adv_tab_decrypt",
                    "Visualization": "adv_tab_visualization"
                }
                if tab_text in translation_map:
                    translated = self.language_manager.translate(
                        translation_map[tab_text], 
                        default=tab_text
                    )
                    self.tab_widget.setTabText(i, translated)
        
        # Decode tab elements
        if hasattr(self, 'track_label'):
            self.track_label.setText(self.language_manager.translate(
                "lbl_select_tracks", 
                default="Select Tracks to Decode:"
            ))
            
        if hasattr(self, 'track_checks'):
            for i, check in enumerate(self.track_checks, 1):
                check.setText(self.language_manager.translate(
                    f"chk_track_{i}", 
                    default=f"Track {i}"
                ))
        
        if hasattr(self, 'decode_btn'):
            self.decode_btn.setText(self.language_manager.translate(
                "btn_decode_tracks", 
                default="Decode Selected Tracks"
            ))
            
        if hasattr(self, 'result_group'):
            self.result_group.setTitle(self.language_manager.translate(
                "grp_decoded_data", 
                default="Decoded Data"
            ))
        
        # Decrypt tab elements
        if hasattr(self, 'key_group'):
            self.key_group.setTitle(self.language_manager.translate(
                "grp_encryption_key", 
                default="Encryption Key"
            ))
            
        if hasattr(self, 'key_label'):
            self.key_label.setText(self.language_manager.translate(
                "lbl_key_hex", 
                default="Key (hex):"
            ))
            
        if hasattr(self, 'key_entry'):
            self.key_entry.setPlaceholderText(self.language_manager.translate(
                "placeholder_enter_key", 
                default="Enter encryption key..."
            ))
            
        if hasattr(self, 'algo_group_ui'):
            self.algo_group_ui.setTitle(self.language_manager.translate(
                "grp_algorithm", 
                default="Algorithm"
            ))
            
        if hasattr(self, 'algorithm_buttons'):
            for btn in self.algorithm_buttons:
                algo_name = btn.property("algorithm_name")
                if algo_name:
                    btn.setText(self.language_manager.translate(
                        f"algo_{algo_name.lower().replace('-', '')}", 
                        default=algo_name
                    ))
            
        if hasattr(self, 'data_group') and isinstance(self.data_group, QGroupBox):
            self.data_group.setTitle(self.language_manager.translate(
                "grp_data_decrypt", 
                default="Data to Decrypt"
            ))
            
        if hasattr(self, 'data_text'):
            self.data_text.setPlaceholderText(self.language_manager.translate(
                "placeholder_enter_data", 
                default="Enter data to decrypt or use 'Load Track Data'..."
            ))
            
        if hasattr(self, 'load_btn'):
            self.load_btn.setText(self.language_manager.translate(
                "btn_load_track", 
                default="Load Track Data"
            ))
            
        if hasattr(self, 'decrypt_btn'):
            self.decrypt_btn.setText(self.language_manager.translate(
                "btn_decrypt", 
                default="Decrypt"
            ))
            
        if hasattr(self, 'results_label'):
            self.results_label.setText(
                f"<b>{self.language_manager.translate('lbl_decryption_results', default='Decryption Results:')}</b>"
            )

    def setup_decode_tab(self):
        """Set up the decode tab."""
        # Create decode tab widget
        decode_tab = QWidget()
        decode_layout = QVBoxLayout(decode_tab)

        # Track selection
        self.track_label = QLabel()
        self.track_label.setStyleSheet("font-weight: bold;")
        decode_layout.addWidget(self.track_label)

        # Track checkboxes
        self.track_checks = []
        track_frame = QWidget()
        track_frame_layout = QHBoxLayout(track_frame)
        track_frame_layout.setContentsMargins(0, 0, 0, 0)

        for i in range(3):
            check = QCheckBox()
            check.setChecked(True)
            self.track_checks.append(check)
            track_frame_layout.addWidget(check)

        track_frame_layout.addStretch()
        decode_layout.addWidget(track_frame)

        # Decode button
        self.decode_btn = QPushButton()
        self.decode_btn.clicked.connect(self.decode_selected_tracks)
        self.decode_btn.setStyleSheet(
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
        decode_layout.addWidget(self.decode_btn)

        # Results area
        self.result_group = QGroupBox()
        result_layout = QVBoxLayout(self.result_group)

        self.decode_text = QTextEdit()
        result_layout.addWidget(self.decode_text)

        decode_layout.addWidget(self.result_group)
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
        self.key_group = QGroupBox()
        key_layout = QHBoxLayout()

        self.key_label = QLabel()
        self.key_entry = QLineEdit()
        self.key_entry.setPlaceholderText(
            self.language_manager.translate("placeholder_enter_key", default="Enter encryption key...")
        )

        key_layout.addWidget(self.key_label)
        key_layout.addWidget(self.key_entry)
        self.key_group.setLayout(key_layout)
        decrypt_layout.addWidget(self.key_group)

        # Algorithm selection
        self.algo_group_ui = QGroupBox()
        algo_layout = QHBoxLayout()

        self.algo_group = QButtonGroup(self)
        self.algorithms = ["DES", "3DES", "AES-128", "AES-192", "AES-256"]
        self.algorithm_buttons = []

        for i, algo in enumerate(self.algorithms):
            radio = QRadioButton()
            radio.setProperty("algorithm_name", algo)  # Store the algorithm name
            self.algorithm_buttons.append(radio)
            if i == 0:  # Default to DES
                radio.setChecked(True)
            self.algo_group.addButton(radio, i)
            algo_layout.addWidget(radio)

        self.algo_group_ui.setLayout(algo_layout)
        decrypt_layout.addWidget(self.algo_group_ui)

        # Data to decrypt
        self.data_group = QGroupBox()
        data_layout = QVBoxLayout()

        self.data_text = QTextEdit()
        self.data_text.setPlaceholderText(self.language_manager.translate(
            "placeholder_enter_data", 
            default="Enter data to decrypt or use 'Load Track Data'..."
        ))
        data_layout.addWidget(self.data_text)

        self.data_group.setLayout(data_layout)
        decrypt_layout.addWidget(self.data_group)

        # Buttons
        btn_frame = QWidget()
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setContentsMargins(0, 0, 0, 0)

        self.load_btn = QPushButton()
        self.load_btn.clicked.connect(self.load_track_data)

        self.decrypt_btn = QPushButton()
        self.decrypt_btn.clicked.connect(self.decrypt_data)
        self.decrypt_btn.setStyleSheet(
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

        btn_layout.addWidget(self.load_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.decrypt_btn)

        decrypt_layout.addWidget(btn_frame)

        # Results area
        self.results_label = QLabel()
        self.results_label.setTextFormat(Qt.TextFormat.RichText)
        decrypt_layout.addWidget(self.results_label)

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

        # Create visualization widget
        self.visualization_widget = VisualizationWidget()
        visualization_layout.addWidget(self.visualization_widget)
        
        # Connect the read card signal from visualization widget to our signal
        self.visualization_widget.read_card_requested.connect(self._on_read_card_requested)

        # Add tab
        self.tab_widget.addTab(visualization_tab, "Visualization")

    def update_tracks(self, tracks: List[str]):
        """Update the track data in the widget and refresh visualizations.

        Args:
            tracks: List of track data strings [track1, track2, track3]
        """
        self.tracks = tracks or ["", "", ""]
        
        # Update visualization if available
        if hasattr(self, 'visualization_widget') and self.visualization_widget is not None:
            self.visualization_widget.update_visualizations(self.tracks)
    
    def _on_read_card_requested(self):
        """Handle read card request from visualization widget."""
        self.read_card_requested.emit()

    def load_track_data(self):
        """Load track data into the decrypt text area."""
        selected_tracks = []
        for i, check in enumerate(self.track_checks):
            if check.isChecked() and i < len(self.tracks) and self.tracks[i]:
                track_label = self.language_manager.translate(
                    f"track_{i+1}", 
                    default=f"Track {i+1}"
                )
                selected_tracks.append(f"{track_label}: {self.tracks[i]}")

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
            no_data_msg = self.language_manager.translate(
                "msg_no_track_data", 
                default="No valid track data found in selected tracks."
            )
            self.decode_text.setPlainText(no_data_msg)

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

        # Get translated labels
        track_label = self.language_manager.translate(f"track_{track_num}", default=f"Track {track_num}")
        card_number_label = self.language_manager.translate("lbl_card_number", default="Card Number")
        cardholder_label = self.language_manager.translate("lbl_cardholder", default="Cardholder")
        last_name_label = self.language_manager.translate("lbl_last_name", default="Last Name")
        expiration_label = self.language_manager.translate("lbl_expiration", default="Expiration")
        service_code_label = self.language_manager.translate("lbl_service_code", default="Service Code")
        raw_data_label = self.language_manager.translate("lbl_raw_data", default="Raw Data")

        result = [f"=== {track_label} ==="]

        # Try to parse track data based on format
        if track_num == 1 and "^" in track_data:
            # Track 1 format: %B1234567890123456^CARDHOLDER/NAME^YYMM...
            parts = track_data[2:].split("^")
            if len(parts) >= 3:
                result.append(f"{card_number_label}: {parts[0]}")
                result.append(f"{cardholder_label}: {parts[1].split('/')[0].strip()}")
                if len(parts[1].split("/")) > 1:
                    result.append(f"{last_name_label}: {parts[1].split('/')[1].strip()}")
                if len(parts[2]) >= 4:
                    exp_month = parts[2][2:4]
                    exp_year = parts[2][:2]
                    result.append(f"{expiration_label}: {exp_month}/{exp_year}")
                if len(parts[2]) >= 7:
                    result.append(f"{service_code_label}: {parts[2][4:7]}")
        elif track_num in (2, 3) and "=" in track_data:
            # Track 2/3 format: ;1234567890123456=YYMM...
            parts = track_data[1:].split("=")
            if len(parts) >= 2:
                result.append(f"{card_number_label}: {parts[0][:16]}")
                if len(parts[1]) >= 4:
                    exp_month = parts[1][2:4]
                    exp_year = parts[1][:2]
                    result.append(f"{expiration_label}: {exp_month}/{exp_year}")
                if len(parts[1]) >= 7:
                    result.append(f"{service_code_label}: {parts[1][4:7]}")

        # Add raw data
        result.append(f"\n{raw_data_label}: {track_data}")
        return "\n".join(result)

    def decrypt_data(self):
        """Decrypt the provided data using the specified key and algorithm."""
        key = self.key_entry.text().strip()
        algorithm = self.algo_group.checkedButton().text()
        data = self.data_text.toPlainText().strip()

        if not key or not data:
            error_title = self.language_manager.translate("error_title", default="Error")
            error_msg = self.language_manager.translate(
                "error_key_and_data_required", 
                default="Both key and data are required"
            )
            QMessageBox.critical(self, error_title, error_msg)
            return

        try:
            # TODO: Implement actual decryption using the decrypt.py module
            # For now, just show a placeholder
            decrypted_with = self.language_manager.translate(
                "msg_decrypted_with", 
                default="Decrypted with {algorithm} and key {key}"
            ).format(algorithm=algorithm, key=key)
            
            result = f"{decrypted_with}\n\n{data}"
            self.result_text.setPlainText(result)

        except Exception as e:
            error_title = self.language_manager.translate("error_decryption_failed", default="Decryption Error")
            error_msg = self.language_manager.translate(
                "error_decryption_failed_msg", 
                default="Failed to decrypt data: {error}"
            ).format(error=str(e))
            QMessageBox.critical(self, error_title, error_msg)


# Example usage
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Apply a stylesheet for consistent look
    app.setStyle("Fusion")

    # Initialize language manager
    language_manager = LanguageManager()
    
    # Sample track data for testing
    sample_tracks = [
        "%B1234567890123456^CARDHOLDER/NAME^24051010000000000000?",
        ";1234567890123456=24051010000000000?",
        ";1234567890123456=24051010000000000?",
    ]

    window = QWidget()
    window.setWindowTitle("Advanced Card Functions")

    layout = QVBoxLayout(window)

    # Initialize with language manager
    frame = AdvancedFunctionsWidget(window, tracks=sample_tracks, language_manager=language_manager)
    layout.addWidget(frame)

    window.resize(800, 700)
    window.show()

    sys.exit(app.exec())
