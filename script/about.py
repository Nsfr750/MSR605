from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton, 
                             QHBoxLayout, QTextBrowser, QApplication)
from PyQt6.QtCore import Qt, QSize, QUrl, QT_VERSION_STR, PYQT_VERSION_STR, pyqtSignal
from PyQt6.QtGui import QPixmap, QIcon, QDesktopServices
from .version import get_version
from .language_manager import LanguageManager  # Import LanguageManager
import os
import sys
import platform
from pathlib import Path
import psutil
import subprocess

class AboutDialog(QDialog):
    def __init__(self, parent=None, language_manager=None):
        super().__init__(parent)
        
        # Initialize language manager
        self.lang_manager = language_manager if language_manager else LanguageManager()
        
        # Connect language changed signal
        if self.lang_manager:
            self.lang_manager.language_changed.connect(self.on_language_changed)
        
        self.setWindowTitle(self.translate("about_title"))
        self.setMinimumSize(500, 400)
        
        # Initialize UI
        self.setup_ui()
    
    def translate(self, key, **kwargs):
        """Helper method to get translated text."""
        if hasattr(self, 'lang_manager') and self.lang_manager:
            return self.lang_manager.translate(key, **kwargs)
        return key  # Fallback to key if no translation available
    
    def on_language_changed(self, lang_code):
        """Handle language change."""
        self.retranslate_ui()
    
    def retranslate_ui(self):
        """Retranslate the UI elements."""
        self.setWindowTitle(self.translate("about_title"))
        
        # Update title and version
        if hasattr(self, 'title_label'):
            self.title_label.setText(self.translate("app_name"))
        
        if hasattr(self, 'version_label'):
            self.version_label.setText(
                self.translate("version", version=get_version())
            )
        
        # Update description
        if hasattr(self, 'description_label'):
            self.description_label.setText(
                self.translate("about_description")
            )
        
        # Update system info
        if hasattr(self, 'sys_info'):
            self.sys_info.setHtml(self.get_system_info())
        
        # Update copyright
        if hasattr(self, 'copyright_label'):
            self.copyright_label.setText(
                self.translate(
                    "copyright",
                    year="2025",
                    author="Nsfr750"
                )
            )
        
        # Update buttons
        if hasattr(self, 'github_btn'):
            self.github_btn.setText(self.translate("github"))
        
        if hasattr(self, 'close_btn'):
            self.close_btn.setText(self.translate("close"))
    
    def setup_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # App logo and title
        header = QHBoxLayout()
        
        # Load application logo
        logo_path = Path(__file__).parent.parent / "assets" / "about_icon.png"
        if logo_path.exists():
            logo_label = QLabel()
            pixmap = QPixmap(str(logo_path))
            # Scale logo to a reasonable size while maintaining aspect ratio
            scaled_pixmap = pixmap.scaled(96, 96, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            # Add some spacing
            logo_label.setContentsMargins(0, 0, 20, 0)
            header.addWidget(logo_label)
        else:
            # Add placeholder if logo not found
            print(f"Logo not found at: {logo_path}")
            logo_label = QLabel("LOGO")
            logo_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #666;")
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            logo_label.setFixedSize(96, 96)
            header.addWidget(logo_label)
        
        # App info
        app_info = QVBoxLayout()
        
        self.title_label = QLabel()
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        
        self.version_label = QLabel()
        self.version_label.setStyleSheet("color: #ffffff")
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        app_info.addWidget(self.title_label)
        app_info.addWidget(self.version_label)
        app_info.addStretch()
        
        header.addLayout(app_info)
        header.addStretch()
        
        layout.addLayout(header)
        
        # Description
        self.description_label = QLabel()
        self.description_label.setWordWrap(True)
        layout.addWidget(self.description_label)
        
        # System info
        layout.addWidget(QLabel(f"<b>{self.translate('system_information')}:</b>"))
        self.sys_info = QTextBrowser()
        self.sys_info.setOpenLinks(True)
        self.sys_info.setMaximumHeight(150)
        layout.addWidget(self.sys_info)
        
        # Copyright and license
        self.copyright_label = QLabel()
        self.copyright_label.setStyleSheet("color: #ffffff; font-size: 11px;")
        self.copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.copyright_label)
        
        # Buttons
        buttons = QHBoxLayout()
        
        # GitHub button
        self.github_btn = QPushButton()
        self.github_btn.setStyleSheet("""
            QPushButton {
                background-color: #1976D2;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        self.github_btn.clicked.connect(lambda: QDesktopServices.openUrl(
            QUrl("https://github.com/Nsfr750/Images-Deduplicator")))
        
        # Close button
        self.close_btn = QPushButton()
        self.close_btn.clicked.connect(self.accept)
        
        buttons.addStretch()
        buttons.addWidget(self.github_btn)
        buttons.addWidget(self.close_btn)
        
        layout.addLayout(buttons)
        
        # Set initial translations
        self.retranslate_ui()
    
    def get_system_info(self):
        """Get system information as HTML."""
        try:
            import psutil
            
            system = platform.system()
            release = platform.release()
            machine = platform.machine()
            python_version = platform.python_version()
            
            # Get CPU information
            cpu_info = platform.processor()
            if not cpu_info and system == 'Windows':
                cpu_info = platform.processor() or "Unknown"
            elif not cpu_info and system == 'Darwin':
                cpu_info = subprocess.check_output(['sysctl', '-n', 'machdep.cpu.brand_string']).strip().decode()
            elif not cpu_info and system == 'Linux':
                cpu_info = ""
                with open('/proc/cpuinfo', 'r') as f:
                    for line in f:
                        if 'model name' in line:
                            cpu_info = line.split(':', 1)[1].strip()
                            break
            
            # Get core count
            core_count = psutil.cpu_count(logical=True)
            physical_cores = psutil.cpu_count(logical=False) or core_count
            
            # Get RAM information
            ram = psutil.virtual_memory()
            total_ram = ram.total / (1024 ** 3)  # Convert to GB
            available_ram = ram.available / (1024 ** 3)  # Convert to GB
            
            return (
                f"<table style='width:100%; color:#ffffff;'>"
                f"<tr><td style='width:40%;'>{self.translate('operating_system')}:</td>"
                f"<td>{system} {release} ({machine})</td></tr>"
                f"<tr><td>CPU:</td><td>{cpu_info}</td></tr>"
                f"<tr><td>Cores:</td><td>{physical_cores} physical, {core_count} logical</td></tr>"
                f"<tr><td>RAM:</td><td>{total_ram:.1f} GB total, {available_ram:.1f} GB available</td></tr>"
                f"<tr><td>Python:</td><td>{python_version}</td></tr>"
                f"<tr><td>Qt:</td><td>{QT_VERSION_STR}</td></tr>"
                f"<tr><td>PyQt:</td><td>{PYQT_VERSION_STR}</td></tr>"
                f"</table>"
            )
        except Exception as e:
            import traceback
            print(f"Error getting system info: {e}")
            print(traceback.format_exc())
            return self.translate("error_loading_system_info")
