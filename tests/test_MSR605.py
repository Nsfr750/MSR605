#!/usr/bin/env python3

import sys
import os
import time

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from script.cardReader import CardReader
from script.cardReaderExceptions import (
    MSR605ConnectError,
    CommunicationTestError,
    SensorTestError,
    RamTestError,
    GetDeviceModelError,
    GetFirmwareVersionError,
    SetCoercivityError,
    GetCoercivityError
)

# Create an alias for the exceptions module for easier access
import script.cardReaderExceptions as cardReaderExceptions
import serial.tools.list_ports

def list_serial_ports():
    """Lists all available serial ports"""
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("No serial ports found!")
        return []
    print("\nAvailable COM ports:")
    for i, port in enumerate(ports, 1):
        print(f"{i}. {port.device} - {port.description}")
    return [port.device for port in ports]

# List available ports and let the user choose
print("\nSCANNING FOR AVAILABLE PORTS...")
ports = list_serial_ports()

if not ports:
    print("\nNo COM ports found. Please connect your MSR605 and try again.")
    sys.exit(1)

# If only one port, use it automatically
if len(ports) == 1:
    port = ports[0]
    print(f"\nAutomatically connecting to {port}...")
else:
    # Let the user choose a port
    while True:
        try:
            choice = input(f"\nEnter the number of the port to use (1-{len(ports)}), or 'q' to quit: ")
            if choice.lower() == 'q':
                print("Exiting...")
                sys.exit(0)
            choice = int(choice)
            if 1 <= choice <= len(ports):
                port = ports[choice - 1]
                break
            print(f"Please enter a number between 1 and {len(ports)}")
        except ValueError:
            print("Please enter a valid number")

# INITIALIZE MSR605
try:
    print(f"\nINITIALIZING MSR605 on {port}...")
    msr = CardReader(port=port)
    print("MSR605 initialized successfully")
    
    # Connect to the MSR605
    print("\nCONNECTING TO MSR605...")
    msr.connect()
    print("Successfully connected to MSR605")
    
except MSR605ConnectError as e:
    print(f"\nConnection Error: {e}")
    print("Please check the following:")
    print("1. Is the MSR605 connected to your computer?")
    print("2. Is the correct port selected?")
    print("3. Is the MSR605 powered on?")
    print("4. Is another program using the port?")
    sys.exit(1)
except CommunicationTestError as e:
    print(f"\nCommunication Test Error: {e}")
    print("The device might not be responding correctly.")
    sys.exit(1)
except Exception as e:
    print(f"\nUnexpected error during initialization: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
except Exception as e:
    print(f"Error connecting to MSR605: {e}")
    sys.exit()

# RESET MSR605
try:
    print("\nRESETTING MSR605...")
    msr.reset()
    print("MSR605 reset successfully")
except Exception as e:
    print(f"Error resetting MSR605: {e}")

# Allow time for reset to complete
time.sleep(1)

try:
    print("\nTESTING COMMUNICATION...")
    msr.communication_test()
    print("Communication test passed")
except CommunicationTestError as e:
    print(f"Communication Test Failed: {e}")
    sys.exit()
except Exception as e:
    print(f"Unexpected error during communication test: {e}")
    sys.exit()

time.sleep(1)

# SENSOR TEST, REQUIRES A CARD SWIPE
try:
    print("\nTESTING SENSOR...")
    msr.sensor_test()
    print("Sensor test passed")
except SensorTestError as e:
    print(f"Sensor Test Failed: {e}")
    sys.exit()
except Exception as e:
    print(f"Unexpected error during sensor test: {e}")
    sys.exit()

time.sleep(1)

# RAM TEST
try:
    print("\nTESTING RAM...")
    msr.ram_test()
    print("RAM test passed")
except RamTestError as e:
    print(f"RAM Test Failed: {e}")
    sys.exit()
except Exception as e:
    print(f"Unexpected error during RAM test: {e}")
    sys.exit()

time.sleep(1)

# GETTING DEVICE MODEL
try:
    print("\nGETTING DEVICE MODEL...")
    msr.get_device_model()
    print("Device model retrieved successfully")
except GetDeviceModelError as e:
    print(f"Failed to get device model: {e}")
    sys.exit()
except Exception as e:
    print(f"Unexpected error during device model retrieval: {e}")
    sys.exit()

time.sleep(1)

# GET FIRMWARE VERSION
try:
    print("\nGETTING FIRMWARE VERSION...")
    msr.get_firmware_version()
    print("Firmware version retrieved successfully")
except GetFirmwareVersionError as e:
    print(f"Failed to get firmware version: {e}")
    sys.exit()
except Exception as e:
    print(f"Unexpected error during firmware version retrieval: {e}")
    sys.exit()

time.sleep(1)

# SETTING MSR605 TO LOW-CO, I DID LOW FIRST BECAUSE I'M PRETTY SURE HI IS THE DEFAULT
try:
    print("\nSETTING MSR605 TO LOW-CO...")
    msr.set_low_co()
    print("MSR605 set to low-co successfully")
except SetCoercivityError as e:
    print(f"Failed to set MSR605 to low-co: {e}")
    sys.exit()
except Exception as e:
    print(f"Unexpected error during low-co setting: {e}")
    sys.exit()

time.sleep(1)

# CHECKING IF THE MSR605 IS IN LOW-CO (WAS SET BEFORE)
try:
    print("\nCHECKING MSR605 COERCIVITY...")
    msr.get_hi_or_low_co()
    print("MSR605 coercivity checked successfully")
except GetCoercivityError as e:
    print(f"Failed to check MSR605 coercivity: {e}")
    sys.exit()
except Exception as e:
    print(f"Unexpected error during coercivity check: {e}")
    sys.exit()

time.sleep(1)

# SETTING MSR605 TO HI-CO
try:
    print("\nSETTING MSR605 TO HI-CO...")
    msr.set_hi_co()
    print("MSR605 set to hi-co successfully")
except SetCoercivityError as e:
    print(f"Failed to set MSR605 to hi-co: {e}")
    sys.exit()
except Exception as e:
    print(f"Unexpected error during hi-co setting: {e}")
    sys.exit()

time.sleep(1)

# CHECKING IF THE MSR605 IS IN HI-CO
try:
    print("\nCHECKING MSR605 COERCIVITY...")
    msr.get_hi_or_low_co()
    print("MSR605 coercivity checked successfully")
except GetCoercivityError as e:
    print(f"Failed to check MSR605 coercivity: {e}")
    sys.exit()
except Exception as e:
    print(f"Unexpected error during coercivity check: {e}")
    sys.exit()

time.sleep(2)

tracks = ["", "", ""]

# READING THE MAGNETIC STRIPE CARD
try:
    print("\nREADING MAGNETIC STRIPE CARD...")
    tracks = msr.read_card()
    print("Card read successfully")
except Exception as e:
    print(f"Error reading card: {e}")
    sys.exit()

print("\nTHE DATA THAT WAS READ FROM THE LAST READ (ABOVE) WILL BE USED TO WRITE")

time.sleep(2)

# WRITE THE DATA THAT WAS READ IN BACK TO THE CARD
try:
    print("\nWRITING DATA TO CARD...")
    msr.write_card(tracks, True)
    print("Data written to card successfully")
except Exception as e:
    print(f"Error writing data to card: {e}")
    sys.exit()

time.sleep(2)

# CHECK IF THE DATA WAS WRITTEN PROPERLY
try:
    print("\nREADING CARD AGAIN TO VERIFY DATA...")
    tracks = msr.read_card()
    print("Data verified successfully")
except Exception as e:
    print(f"Error verifying data: {e}")
    sys.exit()

time.sleep(2)

# ERASED THE CARD
try:
    print("\nERASING CARD...")
    msr.erase_card(7)
    print("Card erased successfully")
except Exception as e:
    print(f"Error erasing card: {e}")
    sys.exit()

time.sleep(2)

# CHECK IF THE CARD IS ERASED
# NOTE THAT THE MSR605 WILL NO RESPOND TO EMPTY CARDS, SO YOU WILL NEED TO SWIPE A CARD WITH DATA
try:
    print("\nREADING CARD AGAIN TO VERIFY ERASE...")
    msr.read_card()
    print("Card erased verified successfully")
except Exception as e:
    print(f"Error verifying card erase: {e}")
    sys.exit()

print("TRACKS: ", tracks)


# CLOSE THE SERIAL CONNECTION
try:
    print("\nCLOSING SERIAL CONNECTION...")
    msr.close_serial_connection()
    print("Serial connection closed successfully")
except Exception as e:
    print(f"Error closing serial connection: {e}")
    sys.exit()
