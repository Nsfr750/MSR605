# MSR605 Card Reader/Writer - API Documentation

This document provides detailed information about the MSR605 Card Reader/Writer API for developers who want to extend or integrate with the application.

## Table of Contents
1. [Overview](#overview)
2. [Core Modules](#core-modules)
3. [Device Communication](#device-communication)
4. [Card Operations](#card-operations)
5. [Data Formats](#data-formats)
6. [Error Handling](#error-handling)
7. [Examples](#examples)

## Overview

The MSR605 API provides a Python interface for interacting with magnetic stripe card readers/writers. The API is designed to be easy to use while providing access to all device features.

## Core Modules

### `msr605`
The main module containing the core functionality.

#### `MSR605` Class
```python
class MSR605:
    def __init__(self, port=None, baudrate=9600, timeout=1):
        """Initialize the MSR605 device connection.
        
        Args:
            port (str, optional): Serial port name. If None, auto-detection is attempted.
            baudrate (int, optional): Communication baud rate. Defaults to 9600.
            timeout (int, optional): Read timeout in seconds. Defaults to 1.
        """
        pass
    
    def connect(self):
        """Establish connection to the device."""
        pass
    
    def disconnect(self):
        """Close the connection to the device."""
        pass
    
    def is_connected(self):
        """Check if the device is connected.
        
        Returns:
            bool: True if connected, False otherwise.
        """
        pass
    
    def read_card(self, tracks=[1, 2, 3]):
        """Read data from a magnetic stripe card.
        
        Args:
            tracks (list, optional): List of tracks to read (1, 2, 3). Defaults to all tracks.
            
        Returns:
            dict: Dictionary containing track data with track numbers as keys.
        """
        pass
    
    def write_card(self, track_data, verify=True):
        """Write data to a magnetic stripe card.
        
        Args:
            track_data (dict): Dictionary with track numbers as keys and data as values.
            verify (bool, optional): Whether to verify the written data. Defaults to True.
            
        Returns:
            bool: True if write was successful, False otherwise.
        """
        pass
```

## Device Communication

### Serial Protocol

#### Commands
| Command | Description | Format |
|---------|-------------|--------|
| `ESC e` | Reset device | `\x1be` |
| `ESC s` | Read card | `\x1bs` |
| `ESC w` | Write card | `\x1bw` |
| `ESC x` | Set security level | `\x1bx` |

#### Responses
| Response | Description |
|----------|-------------|
| `\x1b1` | Command successful |
| `\x1b2` | Command failed |
| `\x1b3` | No card present |
| `\x1b4` | Write protect error |

## Card Operations

### Reading Data
```python
from msr605 import MSR605

# Initialize and connect to the device
device = MSR605()
device.connect()

# Read all tracks
data = device.read_card()
print(f"Track 1: {data.get(1, 'No data')}")
print(f"Track 2: {data.get(2, 'No data')}")
print(f"Track 3: {data.get(3, 'No data')}")

# Read specific tracks
data = device.read_card(tracks=[1, 2])

# Disconnect
device.disconnect()
```

### Writing Data
```python
from msr605 import MSR605

# Initialize and connect to the device
device = MSR605()
device.connect()

# Prepare track data
track_data = {
    1: "%B1234567890123456^CARDHOLDER/NAME^25121010000000000000000000000000000?",
    2: ";1234567890123456=25121010000000000000?",
    3: ""  # Empty track 3
}

# Write to card
success = device.write_card(track_data)
print(f"Write {'successful' if success else 'failed'}")

# Disconnect
device.disconnect()
```

## Data Formats

### Track Formats
- **Track 1 (IATA)**: Up to 79 alphanumeric characters
- **Track 2 (ABA)**: Up to 40 numeric characters
- **Track 3 (THRIFT)**: Up to 107 numeric characters

### Special Characters
| Character | Description |
|-----------|-------------|
| `%` | Start sentinel (Track 1) |
| `;` | Start sentinel (Track 2 & 3) |
| `?` | End sentinel |
| `^` | Separator (Track 1) |
| `=` | Separator (Track 2) |
| `\\` | Escape character |

## Error Handling

### Exceptions
| Exception | Description |
|-----------|-------------|
| `MSR605Error` | Base exception for all MSR605 errors |
| `MSR605ConnectionError` | Connection-related errors |
| `MSR605CommandError` | Command execution errors |
| `MSR605CardError` | Card operation errors |

### Example
```python
from msr605 import MSR605, MSR605Error

try:
    device = MSR605()
    device.connect()
    data = device.read_card()
    print(data)
except MSR605Error as e:
    print(f"Error: {e}")
finally:
    if 'device' in locals():
        device.disconnect()
```

## Examples

### Basic Usage
```python
from msr605 import MSR605

def main():
    try:
        # Initialize and connect
        device = MSR605()
        print("Connecting to device...")
        device.connect()
        
        if not device.is_connected():
            print("Failed to connect to device")
            return
            
        print("Connected. Please swipe a card...")
        
        # Read card
        data = device.read_card()
        print("\nCard Data:")
        for track, value in data.items():
            print(f"Track {track}: {value}")
            
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'device' in locals():
            device.disconnect()
            print("\nDisconnected from device")

if __name__ == "__main__":
    main()
```

### Advanced Usage
```python
from msr605 import MSR605
import json
import time

class CardManager:
    def __init__(self):
        self.device = MSR605()
        self.config = self._load_config()
        
    def _load_config(self):
        # Load configuration from file
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'baudrate': 9600, 'timeout': 1}
            
    def start(self):
        try:
            # Connect with config
            self.device = MSR605(
                baudrate=self.config.get('baudrate', 9600),
                timeout=self.config.get('timeout', 1)
            )
            self.device.connect()
            
            print("Card reader ready. Press Ctrl+C to exit.")
            
            while True:
                print("\nSwipe a card or press Ctrl+C to exit...")
                try:
                    data = self.device.read_card()
                    self._process_card(data)
                except Exception as e:
                    print(f"Error reading card: {e}")
                
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("\nExiting...")
        finally:
            if hasattr(self, 'device') and self.device.is_connected():
                self.device.disconnect()
    
    def _process_card(self, data):
        print("\nCard Data:")
        for track, value in data.items():
            print(f"Track {track}: {value}")
        
        # Save to file
        with open('card_data.log', 'a') as f:
            f.write(f"{time.ctime()}: {data}\n")

if __name__ == "__main__":
    manager = CardManager()
    manager.start()
```
