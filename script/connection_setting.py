#!/usr/bin/env python3

"""
Connection Settings Module for MSR605 Card Reader/Writer.
This module contains the connection settings UI components including COM port configuration.
"""

import serial
import serial.tools.list_ports
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QFormLayout, QComboBox, 
    QPushButton, QLabel, QHBoxLayout
)
from PyQt6.QtCore import pyqtSignal


class ConnectionSettingsWidget(QWidget):
    """
    Widget for connection settings including COM port and serial communication parameters.
    """
    
    # Signals to notify parent of changes
    connect_requested = pyqtSignal()
    disconnect_requested = pyqtSignal()
    settings_changed = pyqtSignal(dict)
    save_requested = pyqtSignal(dict)  # New signal for save button
    
    def __init__(self, parent=None):
        """
        Initialize the connection settings widget.
        
        Args:
            parent: The parent widget
        """
        super().__init__(parent)
        self.parent = parent
        self.is_connected = False
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
        
        # Connection settings group
        self.conn_group = QGroupBox("Connection Settings")
        conn_layout = QFormLayout()
        
        # Port selection
        self.port_combo = QComboBox()
        self.refresh_ports_button = QPushButton("Refresh")
        self.refresh_ports_button.clicked.connect(self.refresh_ports)
        
        port_layout = QHBoxLayout()
        port_layout.addWidget(self.port_combo)
        port_layout.addWidget(self.refresh_ports_button)
        conn_layout.addRow("Port:", port_layout)
        
        # Baud rate
        self.baudrate_combo = QComboBox()
        baudrates = ['9600', '19200', '38400', '57600', '115200']
        self.baudrate_combo.addItems(baudrates)
        self.baudrate_combo.setCurrentText('9600')  # Default baud rate
        self.baudrate_combo.currentTextChanged.connect(self.on_settings_changed)
        conn_layout.addRow("Baud Rate:", self.baudrate_combo)
        
        # Data bits
        self.databits_combo = QComboBox()
        databits = ['5', '6', '7', '8']
        self.databits_combo.addItems(databits)
        self.databits_combo.setCurrentText('8')  # Default data bits
        self.databits_combo.currentTextChanged.connect(self.on_settings_changed)
        conn_layout.addRow("Data Bits:", self.databits_combo)
        
        # Stop bits
        self.stopbits_combo = QComboBox()
        stopbits = ['1', '1.5', '2']
        self.stopbits_combo.addItems(stopbits)
        self.stopbits_combo.setCurrentText('1')  # Default stop bits
        self.stopbits_combo.currentTextChanged.connect(self.on_settings_changed)
        conn_layout.addRow("Stop Bits:", self.stopbits_combo)
        
        # Parity
        self.parity_combo = QComboBox()
        parity_options = ['None', 'Even', 'Odd', 'Mark', 'Space']
        self.parity_combo.addItems(parity_options)
        self.parity_combo.setCurrentText('None')  # Default parity
        self.parity_combo.currentTextChanged.connect(self.on_settings_changed)
        conn_layout.addRow("Parity:", self.parity_combo)
        
        # Flow control
        self.flowcontrol_combo = QComboBox()
        flowcontrol_options = ['None', 'XON/XOFF', 'RTS/CTS', 'DTR/DSR']
        self.flowcontrol_combo.addItems(flowcontrol_options)
        self.flowcontrol_combo.setCurrentText('None')  # Default flow control
        self.flowcontrol_combo.currentTextChanged.connect(self.on_settings_changed)
        conn_layout.addRow("Flow Control:", self.flowcontrol_combo)
        
        # Timeout
        self.timeout_combo = QComboBox()
        timeouts = ['0.1', '0.5', '1.0', '2.0', '5.0', '10.0']
        self.timeout_combo.addItems(timeouts)
        self.timeout_combo.setCurrentText('1.0')  # Default timeout in seconds
        self.timeout_combo.currentTextChanged.connect(self.on_settings_changed)
        conn_layout.addRow("Timeout (s):", self.timeout_combo)
        
        self.conn_group.setLayout(conn_layout)
        
        # Create horizontal layout for buttons
        buttons_layout = QHBoxLayout()
        
        # Connect/Disconnect button
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.on_connect_button_clicked)
        
        # Save button (green background, white text)
        self.save_button = QPushButton("Save")
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
        """)
        self.save_button.clicked.connect(self.on_save_button_clicked)
        
        # Add buttons to layout with stretch
        buttons_layout.addWidget(self.connect_button)
        buttons_layout.addStretch()  # This pushes the save button to the right
        buttons_layout.addWidget(self.save_button)
        
        # Status label
        self.status_label = QLabel("Not connected")
        
        # Add widgets to layout
        layout.addWidget(self.conn_group)
        layout.addLayout(buttons_layout)  # Add the buttons layout
        layout.addWidget(self.status_label)
        layout.addStretch()
        
        # Initial port refresh
        self.refresh_ports()
        
    def retranslate_ui(self):
        """Retranslate UI elements based on current language."""
        if not self.language_manager:
            return
            
        t = self.language_manager.translate
        
        self.conn_group.setTitle(t("grp_connection"))
        self.refresh_ports_button.setText(t("btn_refresh"))
        self.connect_button.setText(t("btn_connect") if not self.is_connected else t("btn_disconnect"))
        self.save_button.setText(t("btn_save"))
        self.status_label.setText(t("msg_not_connected") if not self.is_connected else t("msg_connection_success").format(port=self.port_combo.currentText()))
        
    def refresh_ports(self):
        """Refresh the list of available COM ports."""
        current_port = self.port_combo.currentText()
        self.port_combo.clear()
        
        try:
            ports = self.get_available_ports()
            if ports:
                self.port_combo.addItems(ports)
                # Restore previous selection if available
                if current_port and current_port in ports:
                    self.port_combo.setCurrentText(current_port)
            else:
                if self.language_manager:
                    self.port_combo.addItem(self.language_manager.translate("msg_no_ports"))
                else:
                    self.port_combo.addItem("No ports found")
        except Exception as e:
            if self.language_manager:
                self.port_combo.addItem(self.language_manager.translate("msg_port_error"))
            else:
                self.port_combo.addItem("Error detecting ports")
            print(f"Error refreshing ports: {e}")
            
    def get_available_ports(self):
        """
        Get a list of available COM ports.
        
        Returns:
            list: List of available COM port names
        """
        try:
            return [port.device for port in serial.tools.list_ports.comports()]
        except Exception as e:
            print(f"Error getting available ports: {e}")
            return []
            
    def on_connect_button_clicked(self):
        """Handle connect/disconnect button click."""
        if self.is_connected:
            self.disconnect_requested.emit()
        else:
            self.connect_requested.emit()
            
    def on_save_button_clicked(self):
        """Handle save button click."""
        settings = self.get_serial_settings()
        self.save_requested.emit(settings)
        
    def on_settings_changed(self):
        """Handle settings changes."""
        settings = self.get_serial_settings()
        self.settings_changed.emit(settings)
        
    def get_serial_settings(self):
        """
        Get the current serial communication settings.
        
        Returns:
            dict: Dictionary containing serial settings
        """
        # Map string values to serial constants
        parity_map = {
            'None': serial.PARITY_NONE,
            'Even': serial.PARITY_EVEN,
            'Odd': serial.PARITY_ODD,
            'Mark': serial.PARITY_MARK,
            'Space': serial.PARITY_SPACE
        }
        
        stopbits_map = {
            '1': serial.STOPBITS_ONE,
            '1.5': serial.STOPBITS_ONE_POINT_FIVE,
            '2': serial.STOPBITS_TWO
        }
        
        flowcontrol_map = {
            'None': 0,  # No flow control
            'XON/XOFF': 1,  # Software flow control (XON/XOFF)
            'RTS/CTS': 2,  # Hardware flow control (RTS/CTS)
            'DTR/DSR': 3   # Hardware flow control (DTR/DSR)
        }
        
        return {
            'port': self.port_combo.currentText(),
            'baudrate': int(self.baudrate_combo.currentText()),
            'bytesize': int(self.databits_combo.currentText()),
            'parity': parity_map.get(self.parity_combo.currentText(), serial.PARITY_NONE),
            'stopbits': stopbits_map.get(self.stopbits_combo.currentText(), serial.STOPBITS_ONE),
            'flowcontrol': flowcontrol_map.get(self.flowcontrol_combo.currentText(), 0),
            'timeout': float(self.timeout_combo.currentText())
        }
        
    def set_connected_state(self, connected):
        """
        Set the connection state and update UI accordingly.
        
        Args:
            connected (bool): Whether the device is connected
        """
        self.is_connected = connected
        
        if connected:
            self.connect_button.setText("Disconnect")
            self.status_label.setText(f"Connected to {self.port_combo.currentText()}")
        else:
            self.connect_button.setText("Connect")
            self.status_label.setText("Not connected")
            
        # Update translations if language manager is available
        if self.language_manager:
            self.retranslate_ui()
        
    def set_connection_state(self, connected):
        """
        Set the connection state (alias for set_connected_state).
        
        Args:
            connected (bool): Whether the device is connected
        """
        self.set_connected_state(connected)
        
    def get_selected_port(self):
        """
        Get the currently selected port.
        
        Returns:
            str: The selected COM port name
        """
        return self.port_combo.currentText()
        
    def get_port(self):
        """
        Get the currently selected port (alias for get_selected_port).
        
        Returns:
            str: The selected COM port name
        """
        return self.get_selected_port()
        
    def get_baudrate(self):
        """
        Get the currently selected baud rate.
        
        Returns:
            str: The selected baud rate
        """
        return self.baudrate_combo.currentText()
        
    def set_port(self, port):
        """
        Set the selected port.
        
        Args:
            port (str): The COM port name to select
        """
        index = self.port_combo.findText(port)
        if index >= 0:
            self.port_combo.setCurrentIndex(index)
            
    def set_settings(self, settings):
        """
        Set the serial communication settings.
        
        Args:
            settings (dict): Dictionary containing serial settings
        """
        if 'port' in settings:
            self.set_port(settings['port'])
        if 'baudrate' in settings:
            self.baudrate_combo.setCurrentText(str(settings['baudrate']))
        if 'bytesize' in settings:
            self.databits_combo.setCurrentText(str(settings['bytesize']))
        if 'timeout' in settings:
            self.timeout_combo.setCurrentText(str(settings['timeout']))
