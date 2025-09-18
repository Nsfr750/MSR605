#!/usr/bin/env python3
"""
Test script to scan and test all available COM ports
"""

import serial
import sys
import time

def test_com_port(port):
    """Test if we can open a COM port"""
    try:
        print(f"Testing access to {port}...")
        ser = serial.Serial(port, timeout=1)  # Add timeout to prevent hanging
        print(f"  ✓ Successfully opened {port}")
        ser.close()
        print(f"  ✓ Successfully closed {port}")
        return True, "Success"
    except serial.SerialException as e:
        error_msg = str(e)
        if "could not open port" in error_msg:
            return False, "Port not available or doesn't exist"
        elif "PermissionError" in error_msg or "Access is denied" in error_msg:
            return False, "Permission denied (try running as Administrator)"
        else:
            return False, f"Serial Exception: {error_msg}"
    except PermissionError as e:
        return False, f"Permission Error: {e} (try running as Administrator)"
    except Exception as e:
        return False, f"Unexpected Error: {e}"

def scan_com_ports():
    """Scan all possible COM ports and test them"""
    print(f"COM Port Scanner")
    print(f"=" * 60)
    print(f"Scanning all available COM ports...\n")
    
    # List available ports
    available_ports = []
    try:
        import serial.tools.list_ports
        print(f"Detected COM ports:")
        ports = serial.tools.list_ports.comports()
        if ports:
            for p in ports:
                print(f"  {p.device} - {p.description}")
                available_ports.append(p.device)
        else:
            print(f"  No COM ports detected by system")
        print()
    except ImportError:
        print(f"Could not list available ports using serial.tools.list_ports")
        print()
    
    # Also scan common COM port range
    print(f"Scanning COM ports COM1 to COM20...")
    print(f"-" * 60)
    
    successful_ports = []
    failed_ports = []
    
    # Test both detected ports and common range
    ports_to_test = list(set(available_ports + [f"COM{i}" for i in range(1, 21)]))
    ports_to_test.sort()
    
    for port in ports_to_test:
        success, message = test_com_port(port)
        
        if success:
            successful_ports.append(port)
            print(f"  ✓ {port}: {message}")
        else:
            failed_ports.append((port, message))
            print(f"  ✗ {port}: {message}")
        
        # Small delay between tests to prevent port conflicts
        time.sleep(0.1)
    
    print(f"\n" + "=" * 60)
    print(f"SCAN RESULTS:")
    print(f"=" * 60)
    
    if successful_ports:
        print(f"\n✓ SUCCESSFUL PORTS ({len(successful_ports)}):")
        for port in successful_ports:
            print(f"  • {port} - Accessible and ready to use")
    else:
        print(f"\n✗ No accessible COM ports found")
    
    if failed_ports:
        print(f"\n✗ FAILED PORTS ({len(failed_ports)}):")
        for port, error in failed_ports:
            print(f"  • {port}: {error}")
    
    print(f"\n" + "-" * 60)
    
    # Provide recommendations
    if successful_ports:
        print(f"\n🎯 RECOMMENDATIONS:")
        print(f"• Use one of the successful ports for your MSR605 device")
        print(f"• If multiple ports work, try the one with 'Prolific' in the description")
        print(f"• Recommended port: {successful_ports[0]}")
    else:
        print(f"\n⚠️  TROUBLESHOOTING STEPS:")
        print(f"1. Run this script as Administrator (right-click → Run as administrator)")
        print(f"2. Ensure your MSR605 device is connected and powered on")
        print(f"3. Check USB cable and try a different USB port")
        print(f"4. Install or update Prolific USB-to-Serial drivers")
        print(f"5. Check Windows Device Manager for port conflicts")
        print(f"6. Close any other applications that might be using COM ports")
        print(f"7. Try unplugging and replugging the MSR605 device")
    
    return successful_ports, failed_ports

if __name__ == "__main__":
    # Check if a specific port was provided as argument
    if len(sys.argv) > 1:
        port = sys.argv[1]
        print(f"COM Port Access Test - Single Port Mode")
        print(f"=" * 50)
        print(f"Testing specific port: {port}\n")
        
        success, message = test_com_port(port)
        
        if success:
            print(f"\n✓ COM port {port} access is working!")
        else:
            print(f"\n✗ COM port {port} access failed!")
            print(f"Error: {message}")
            print(f"\nTroubleshooting steps:")
            print(f"1. Run this script as Administrator")
            print(f"2. Check if another application is using the COM port")
            print(f"3. Update USB-to-Serial drivers")
            print(f"4. Try a different COM port number")
            print(f"5. Check USB cable and connection")
    else:
        # Default mode: scan all ports
        successful_ports, failed_ports = scan_com_ports()
