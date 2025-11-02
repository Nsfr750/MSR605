"""
Sponsor dialog for the MSR605 application.
"""

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QTextBrowser,
    QWidget,
    QSizePolicy,
    QApplication,
    QGridLayout,
    QInputDialog,
    QMessageBox,
)
from PyQt6.QtCore import Qt, QUrl, QSize, QBuffer, QTimer
from PyQt6.QtGui import QDesktopServices, QPixmap, QPalette, QColor, QIcon, QImage

from script.language_manager import LanguageManager
from typing import Optional

import webbrowser
import os
import io
import qrcode
from wand.image import Image as WandImage


class SponsorDialog(QDialog):
    def __init__(self, parent=None, language_manager: Optional[LanguageManager] = None):
        super().__init__(parent)

        # Initialize language manager
        self.lang_manager = language_manager or LanguageManager()

        # Connect language changed signal
        if self.lang_manager:
            self.lang_manager.language_changed.connect(self.on_language_changed)

        self.setMinimumSize(500, 400)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        # Initialize UI
        self.setup_ui()

        # Set initial translations
        self.retranslate_ui()

    def translate(self, key: str, **kwargs) -> str:
        """Helper method to get translated text."""
        if hasattr(self, "lang_manager") and self.lang_manager:
            return self.lang_manager.translate(key, **kwargs)
        return key  # Fallback to key if no translation available

    def on_language_changed(self, lang_code: str) -> None:
        """Handle language change."""
        self.retranslate_ui()

    def retranslate_ui(self) -> None:
        """Retranslate the UI elements."""
        self.setWindowTitle(self.translate("support_development"))

        if hasattr(self, "title_label"):
            self.title_label.setText(self.translate("support_app_name"))

        if hasattr(self, "message_label"):
            self.message_label.setText(self.translate("support_message"))

        if hasattr(self, "github_btn"):
            self.github_btn.setText(self.translate("github_sponsors"))
            self.github_btn.clicked.connect(
                lambda: QDesktopServices.openUrl(
                    QUrl("https://github.com/sponsors/Nsfr750")
                )
            )

        if hasattr(self, "monero_label"):
            self.monero_label.setText(f"{self.translate('monero')}:")

        if hasattr(self, "close_btn"):
            self.close_btn.setText(self.translate("close"))

        if hasattr(self, "donate_btn"):
            self.donate_btn.setText(self.translate("donate_with_paypal"))

        if hasattr(self, "copy_monero_btn"):
            self.copy_monero_btn.setText(self.translate("copy_monero_address"))

    def setup_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)

        # Title
        self.title_label = QLabel()
        self.title_label.setStyleSheet(
            "font-size: 18px; font-weight: bold; margin-bottom: 20px;"
        )
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)

        # Message
        self.message_label = QLabel()
        self.message_label.setWordWrap(True)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.message_label)

        # Create a container widget for the grid layout
        grid_container = QWidget()
        grid = QGridLayout(grid_container)

        # GitHub button
        self.github_btn = QPushButton()
        self.github_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.github_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #1a73e8;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1557b0;
            }
        """
        )

        # PayPal
        self.paypal_label = QLabel()
        self.paypal_label.setOpenExternalLinks(True)
        self.paypal_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Monero
        monero_address = "47Jc6MC47WJVFhiQFYwHyBNQP5BEsjUPG6tc8R37FwcTY8K5Y3LvFzveSXoGiaDQSxDrnCUBJ5WBj6Fgmsfix8VPD4w3gXF"
        self.monero_label = QLabel()
        monero_address_label = QLabel(monero_address)
        monero_address_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        monero_address_label.setStyleSheet(
            """
            QLabel {
                font-family: monospace;
                background-color: #2a2a2a;
                padding: 5px;
                border-radius: 3px;
                border: 1px solid #444;
                color: #f0f0f0;
            }
        """
        )

        # Generate QR Code
        try:
            # Create QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(f"monero:{monero_address}")
            qr.make(fit=True)

            # Generate QR code image
            qr_img = qr.make_image(
                fill_color="#4a9cff", back_color="#2a2a2a"
            )  # Changed to solid background

            # Convert to QPixmap directly using PIL
            qr_img = qr_img.convert("RGBA")
            data = qr_img.tobytes("raw", "RGBA")
            qimage = QImage(
                data, qr_img.size[0], qr_img.size[1], QImage.Format.Format_RGBA8888
            )
            pixmap = QPixmap.fromImage(qimage)

            # Scale the pixmap
            pixmap = pixmap.scaled(
                200,
                200,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            # Create and configure the QR code label
            self.qr_label = QLabel()
            self.qr_label.setPixmap(pixmap)
            self.qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.qr_label.setToolTip(self.translate("scan_to_donate_xmr"))

            # Add some styling to make it more visible
            self.qr_label.setStyleSheet(
                """
                QLabel {
                    background-color: #2a2a2a;
                    border: 1px solid #444;
                    border-radius: 5px;
                    padding: 10px;
                }
            """
            )

        except Exception as e:
            print(f"Error generating QR code: {e}")
            self.qr_label = QLabel(self.translate("qr_generation_failed"))
            self.qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.qr_label.setStyleSheet("color: #ff4444; font-weight: bold;")

        # Add widgets to grid
        grid.addWidget(
            QLabel(f"<h3>{self.translate('ways_to_support')}</h3>"), 0, 0, 1, 2
        )
        grid.addWidget(self.github_btn, 1, 0, 1, 2)
        grid.addWidget(self.paypal_label, 2, 0, 1, 2)
        grid.addWidget(self.monero_label, 3, 0, 1, 2)
        grid.addWidget(monero_address_label, 4, 0, 1, 2)

        # Add QR code to the grid if it was created
        if hasattr(self, "qr_label") and self.qr_label is not None:
            # Create a container widget for the QR code with proper alignment
            qr_container = QWidget()
            qr_layout = QVBoxLayout(qr_container)
            qr_layout.addWidget(self.qr_label, 0, Qt.AlignmentFlag.AlignCenter)
            qr_layout.setContentsMargins(10, 10, 10, 10)

            # Add the container to the grid, spanning 5 rows (from 0 to 4)
            grid.addWidget(qr_container, 0, 2, 5, 1)

        # Add some spacing
        grid.setSpacing(10)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        # Add grid container to layout
        layout.addWidget(grid_container)

        # Other ways to help
        other_help = QTextBrowser()
        other_help.setOpenExternalLinks(True)
        other_help.setHtml(
            f"<h3>{self.translate('other_ways_to_help')}</h3>"
            f"<ul>"
            f"<li>{self.translate('star_on_github')} <a href=\"https://github.com/Nsfr750/MSR605\">GitHub</a></li>"
            f"<li>{self.translate('report_bugs')}</li>"
            f"<li>{self.translate('share_with_others')}</li>"
            f"</ul>"
        )
        other_help.setMaximumHeight(150)
        other_help.setStyleSheet(
            """
            QTextBrowser {
                background-color: #2a2a2a;
                border: 1px solid #444;
                border-radius: 4px;
                color: #f0f0f0;
            }
            a { color: #4a9cff; }
        """
        )
        layout.addWidget(other_help)

        # Button layout
        button_layout = QHBoxLayout()

        # Close button
        self.close_btn = QPushButton()
        self.close_btn.clicked.connect(self.accept)

        # Donate button
        self.donate_btn = QPushButton()
        self.donate_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #0079C1;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0062A3;
            }
        """
        )
        self.donate_btn.clicked.connect(self.open_paypal_link)

        # Copy Monero address button
        self.copy_monero_btn = QPushButton()
        self.copy_monero_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #F26822;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                margin-right: 10px;
            }
            QPushButton:hover {
                background-color: #D45B1D;
            }
        """
        )
        self.copy_monero_btn.clicked.connect(
            lambda: self.copy_to_clipboard(monero_address)
        )

        button_layout.addWidget(self.close_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.copy_monero_btn)
        button_layout.addWidget(self.donate_btn)

        layout.addLayout(button_layout)

        # Apply dark theme
        self.apply_dark_theme()

    def apply_dark_theme(self):
        """Apply dark theme to the dialog."""
        # Set dark palette
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        dark_palette.setColor(QPalette.ColorRole.Link, QColor(74, 156, 255))
        dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(74, 156, 255))
        dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)

        self.setPalette(dark_palette)

        # Set style sheet
        self.setStyleSheet(
            """
            QDialog {
                background-color: #2d2d2d;
            }
            QLabel {
                color: #f0f0f0;
            }
            QPushButton {
                background-color: #3a3a3a;
                color: #f0f0f0;
                border: 1px solid #555;
                padding: 8px 16px;
                border-radius: 4px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
                border: 1px solid #777;
            }
            QPushButton:pressed {
                background-color: #2a2a2a;
            }
            QTextBrowser {
                background-color: #2a2a2a;
                border: 1px solid #444;
                border-radius: 4px;
                color: #f0f0f0;
            }
            a {
                color: #4a9cff;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        """
        )

    def open_donation_link(self):
        """Open donation link in default web browser."""
        QDesktopServices.openUrl(QUrl("https://github.com/sponsors/Nsfr750"))

    def open_paypal_link(self):
        """Open PayPal link in default web browser."""
        QDesktopServices.openUrl(QUrl("https://paypal.me/3dmega"))

    def copy_to_clipboard(self, text):
        """Copy text to clipboard and show a tooltip."""
        clipboard = QApplication.clipboard()
        clipboard.setText(text)

        # Show a temporary tooltip
        button = self.sender()
        if button:
            original_text = button.text()
            button.setText(self.translate("copied"))
            button.setStyleSheet(button.styleSheet() + "background-color: #4CAF50;")

            # Reset button text after 2 seconds
            QTimer.singleShot(2000, lambda: self.reset_button(button, original_text))

    def reset_button(self, button, text):
        """Reset button text and style."""
        button.setText(text)
        button.setStyleSheet(
            """
            QPushButton {
                background-color: #F26822;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                margin-right: 10px;
            }
            QPushButton:hover {
                background-color: #D45B1D;
            }
        """
        )
