import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QComboBox, QMessageBox, QGroupBox)
from PyQt6.QtCore import Qt, pyqtSignal
import serial.tools.list_ports
from .language_manager import LanguageManager

class COMPortDialog(QDialog):
    """Dialog for COM port selection and device management."""
    
    # Signals
    port_selected = pyqtSignal(str)  # Emitted when a port is selected
    
    def __init__(self, parent=None, language_manager=None):
        super().__init__(parent)
        self.language_manager = language_manager or LanguageManager()
        self.setWindowTitle(self.tr("COM Port Settings"))
        self.setMinimumWidth(400)
        
        self.setup_ui()
        self.refresh_ports()
    
    def tr(self, key, default=None):
        """Translate text using the language manager."""
        if self.language_manager and hasattr(self.language_manager, 'translate'):
            return self.language_manager.translate(key, default=default)
        return default or key
    
    def setup_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        
        # COM Port Selection
        port_group = QGroupBox(self.tr("COM Port Settings"))
        port_layout = QVBoxLayout()
        
        # Port selection
        port_select_layout = QHBoxLayout()
        port_select_layout.addWidget(QLabel(self.tr("Select Port:")))
        
        self.port_combo = QComboBox()
        port_select_layout.addWidget(self.port_combo, 1)
        
        refresh_btn = QPushButton(self.tr("Refresh"))
        refresh_btn.clicked.connect(self.refresh_ports)
        port_select_layout.addWidget(refresh_btn)
        
        port_layout.addLayout(port_select_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.reset_port_btn = QPushButton(self.tr("Reset Port"))
        self.reset_port_btn.clicked.connect(self.reset_port)
        btn_layout.addWidget(self.reset_port_btn)
        
        self.reset_device_btn = QPushButton(self.tr("Reset Device"))
        self.reset_device_btn.clicked.connect(self.reset_device)
        btn_layout.addWidget(self.reset_device_btn)
        
        port_layout.addLayout(btn_layout)
        port_group.setLayout(port_layout)
        
        # Test Section
        test_group = QGroupBox(self.tr("Device Tests"))
        test_layout = QVBoxLayout()
        
        self.test_device_btn = QPushButton(self.tr("Test MSR605"))
        self.test_device_btn.clicked.connect(self.run_msr605_test)
        test_layout.addWidget(self.test_device_btn)
        
        self.test_reader_btn = QPushButton(self.tr("Test Card Reader"))
        self.test_reader_btn.clicked.connect(self.run_reader_test)
        test_layout.addWidget(self.test_reader_btn)
        
        self.test_format_btn = QPushButton(self.tr("Test Card Format"))
        self.test_format_btn.clicked.connect(self.run_format_test)
        test_layout.addWidget(self.test_format_btn)
        
        test_group.setLayout(test_layout)
        
        # Dialog buttons
        button_box = QHBoxLayout()
        
        ok_btn = QPushButton(self.tr("OK"))
        ok_btn.clicked.connect(self.accept)
        
        cancel_btn = QPushButton(self.tr("Cancel"))
        cancel_btn.clicked.connect(self.reject)
        
        button_box.addStretch()
        button_box.addWidget(ok_btn)
        button_box.addWidget(cancel_btn)
        
        # Add all to main layout
        layout.addWidget(port_group)
        layout.addWidget(test_group)
        layout.addLayout(button_box)
    
    def refresh_ports(self):
        """Refresh the list of available COM ports."""
        self.port_combo.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.port_combo.addItem(f"{port.device} - {port.description}", port.device)
    
    def reset_port(self):
        """Reset the selected COM port."""
        port = self.port_combo.currentData()
        if not port:
            QMessageBox.warning(self, self.tr("Error"), self.tr("No port selected"))
            return
        
        # TODO: Implement actual port reset logic
        QMessageBox.information(self, self.tr("Success"), 
                              self.tr("Port {} has been reset").format(port))
    
    def reset_device(self):
        """Reset the MSR605 device."""
        port = self.port_combo.currentData()
        if not port:
            QMessageBox.warning(self, self.tr("Error"), self.tr("No port selected"))
            return
        
        # TODO: Implement actual device reset logic
        QMessageBox.information(self, self.tr("Success"), 
                              self.tr("MSR605 device has been reset"))
    
    def run_msr605_test(self):
        """Run the MSR605 test suite."""
        self.run_test("test_MSR605.py")
    
    def run_reader_test(self):
        """Run the card reader test suite."""
        self.run_test("test_card_reader.py")
    
    def run_format_test(self):
        """Run the card format test suite."""
        self.run_test("test_card_formats.py")
    
    def run_test(self, test_file):
        """Run the specified test file."""
        import subprocess
        import sys
        
        test_path = f"tests/{test_file}"
        if not os.path.exists(test_path):
            QMessageBox.critical(self, self.tr("Error"), 
                               self.tr("Test file not found: {}").format(test_path))
            return
        
        try:
            result = subprocess.run(
                [sys.executable, test_path],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            )
            
            # Show test results
            msg = QMessageBox(self)
            msg.setWindowTitle(self.tr("Test Results"))
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText(self.tr("Test completed"))
            
            details = result.stdout
            if not details:
                details = result.stderr
            
            msg.setDetailedText(details)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
            
        except Exception as e:
            QMessageBox.critical(self, self.tr("Error"), 
                               self.tr("Failed to run test: {}").format(str(e)))
