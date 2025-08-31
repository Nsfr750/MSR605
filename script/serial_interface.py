import serial
import serial.tools.list_ports
from typing import Optional, List, Dict, Any
from .logger import logger


class MSR605Serial:
    """
    A class to handle serial communication with the MSR605 magnetic card reader/writer.
    """
    
    # Default serial settings for MSR605
    DEFAULT_BAUDRATE = 9600
    DEFAULT_BYTESIZE = serial.EIGHTBITS
    DEFAULT_PARITY = serial.PARITY_NONE
    DEFAULT_STOPBITS = serial.STOPBITS_ONE
    DEFAULT_TIMEOUT = 1  # seconds
    
    def __init__(self):
        """Initialize the MSR605 serial interface."""
        self.serial_port: Optional[serial.Serial] = None
        self.connected = False
    
    def list_available_ports(self) -> List[Dict[str, Any]]:
        """
        List all available serial ports.
        
        Returns:
            List of dictionaries containing port information
        """
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append({
                'device': port.device,
                'name': port.name,
                'description': port.description,
                'hwid': port.hwid,
                'vid': port.vid,
                'pid': port.pid,
                'serial_number': port.serial_number,
                'manufacturer': port.manufacturer,
                'product': port.product,
                'interface': port.interface
            })
        return ports
    
    def connect(self, port: str, baudrate: int = DEFAULT_BAUDRATE, 
                bytesize: int = DEFAULT_BYTESIZE, 
                parity: str = DEFAULT_PARITY, 
                stopbits: float = DEFAULT_STOPBITS,
                timeout: float = DEFAULT_TIMEOUT) -> bool:
        """
        Connect to the MSR605 device.
        
        Args:
            port: The serial port to connect to (e.g., 'COM3' on Windows)
            baudrate: Baud rate (default: 9600)
            bytesize: Number of data bits (default: 8)
            parity: Parity setting (default: 'N' for no parity)
            stopbits: Number of stop bits (default: 1)
            timeout: Read timeout in seconds (default: 1)
            
        Returns:
            bool: True if connection was successful, False otherwise
        """
        if self.connected and self.serial_port and self.serial_port.is_open:
            self.disconnect()
        
        try:
            self.serial_port = serial.Serial(
                port=port,
                baudrate=baudrate,
                bytesize=bytesize,
                parity=parity,
                stopbits=stopbits,
                timeout=timeout,
                xonxoff=False,
                rtscts=False,
                dsrdtr=False
            )
            self.connected = True
            logger.info(f"Successfully connected to {port} at {baudrate} baud")
            return True
            
        except serial.SerialException as e:
            logger.error(f"Failed to connect to {port}: {str(e)}")
            self.connected = False
            return False
    
    def disconnect(self) -> None:
        """Close the serial connection if it's open."""
        if self.serial_port and self.serial_port.is_open:
            try:
                self.serial_port.close()
                logger.info("Serial connection closed")
            except Exception as e:
                logger.error(f"Error closing serial port: {str(e)}")
            finally:
                self.connected = False
    
    def send_command(self, command: bytes) -> bool:
        """
        Send a command to the MSR605 device.
        
        Args:
            command: The command bytes to send
            
        Returns:
            bool: True if the command was sent successfully, False otherwise
        """
        if not self.connected or not self.serial_port or not self.serial_port.is_open:
            logger.error("Cannot send command: Not connected to a serial port")
            return False
            
        try:
            self.serial_port.write(command)
            self.serial_port.flush()
            logger.debug(f"Sent command: {command.hex()}")
            return True
            
        except serial.SerialException as e:
            logger.error(f"Error sending command: {str(e)}")
            self.connected = False
            return False
    
    def read_response(self, size: int = 1024, timeout: Optional[float] = None) -> bytes:
        """
        Read a response from the MSR605 device.
        
        Args:
            size: Maximum number of bytes to read (default: 1024)
            timeout: Optional timeout in seconds (overrides default timeout)
            
        Returns:
            bytes: The response data, or empty bytes if an error occurred
        """
        if not self.connected or not self.serial_port or not self.serial_port.is_open:
            logger.error("Cannot read response: Not connected to a serial port")
            return b''
            
        try:
            if timeout is not None:
                original_timeout = self.serial_port.timeout
                self.serial_port.timeout = timeout
                
            response = self.serial_port.read(size)
            
            if timeout is not None:
                self.serial_port.timeout = original_timeout
                
            if response:
                logger.debug(f"Received response: {response.hex()}")
            return response
            
        except serial.SerialException as e:
            logger.error(f"Error reading response: {str(e)}")
            self.connected = False
            return b''
    
    def is_connected(self) -> bool:
        """Check if the serial connection is active."""
        return self.connected and self.serial_port is not None and self.serial_port.is_open
    
    def __del__(self):
        """Ensure the serial connection is closed when the object is destroyed."""
        self.disconnect()
