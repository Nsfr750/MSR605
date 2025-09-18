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
    
    def __init__(self, parent=None):
        """
        Initialize the connection settings widget.
        
        Args:
            parent: The parent widget
        """
        super().__init__(parent)
        self.parent = parent
        self.is_connected = False
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        
        # Connection settings group
        conn_group = QGroupBox("Connection Settings")
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
        
        conn_group.setLayout(conn_layout)
        
        # Connect/Disconnect button
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.on_connect_button_clicked)
        
        # Status label
        self.status_label = QLabel("Not connected")
        
        # Add widgets to layout
        layout.addWidget(conn_group)
        layout.addWidget(self.connect_button)
        layout.addWidget(self.status_label)
        layout.addStretch()
        
        # Initial port refresh
        self.refresh_ports()
        
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
                self.port_combo.addItem("No ports found")
        except Exception as e:
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
            'XON/XOFF': serial.XONXOFF,
            'RTS/CTS': serial.RTSCTS,
            'DTR/DSR': serial.DTRDSR
        }
        
        return {
            'port': self.port_combo.currentText(),
            'baudrate': int(self.baudrate_combo.currentText()),
            'bytesize': int(self.databits_combo.currentText()),
            'parity': parity_map.get(self.parity_combo.currentText(), serial.PARITY_NONE),
            'stopbits': stopbits_map.get(self.stopbits_combo.currentText(), serial.STOPBITS_ONE),
            'timeout': float(self.timeout_combo.currentText()),
            'xonxoff': flowcontrol_map.get(self.flowcontrol_combo.currentText(), 0) == serial.XONXOFF,
            'rtscts': flowcontrol_map.get(self.flowcontrol_combo.currentText(), 0) == serial.RTSCTS,
            'dsrdtr': flowcontrol_map.get(self.flowcontrol_combo.currentText(), 0) == serial.DTRDSR
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
            # Disable settings when connected
            self.port_combo.setEnabled(False)
            self.refresh_ports_button.setEnabled(False)
            self.baudrate_combo.setEnabled(False)
            self.databits_combo.setEnabled(False)
            self.stopbits_combo.setEnabled(False)
            self.parity_combo.setEnabled(False)
            self.flowcontrol_combo.setEnabled(False)
            self.timeout_combo.setEnabled(False)
        else:
            self.connect_button.setText("Connect")
            self.status_label.setText("Not connected")
            # Enable settings when disconnected
            self.port_combo.setEnabled(True)
            self.refresh_ports_button.setEnabled(True)
            self.baudrate_combo.setEnabled(True)
            self.databits_combo.setEnabled(True)
            self.stopbits_combo.setEnabled(True)
            self.parity_combo.setEnabled(True)
            self.flowcontrol_combo.setEnabled(True)
            self.timeout_combo.setEnabled(True)
            
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
        if 'baudrate' in settings:
            self.baudrate_combo.setCurrentText(str(settings['baudrate']))
        if 'bytesize' in settings:
            self.databits_combo.setCurrentText(str(settings['bytesize']))
        if 'stopbits' in settings:
            # Map back from serial constants to strings
            stopbits_map = {
                serial.STOPBITS_ONE: '1',
                serial.STOPBITS_ONE_POINT_FIVE: '1.5',
                serial.STOPBITS_TWO: '2'
            }
            stopbits_str = stopbits_map.get(settings['stopbits'], '1')
            self.stopbits_combo.setCurrentText(stopbits_str)
        if 'parity' in settings:
            # Map back from serial constants to strings
            parity_map = {
                serial.PARITY_NONE: 'None',
                serial.PARITY_EVEN: 'Even',
                serial.PARITY_ODD: 'Odd',
                serial.PARITY_MARK: 'Mark',
                serial.PARITY_SPACE: 'Space'
            }
            parity_str = parity_map.get(settings['parity'], 'None')
            self.parity_combo.setCurrentText(parity_str)
        if 'timeout' in settings:
            self.timeout_combo.setCurrentText(str(settings['timeout']))
