"""Raw serial diagnostic for MSR605 card reads.

Opens the port, sends the READ command, then dumps every byte received
for 30 seconds. Swipe a card (both directions) while it waits.

Usage:
    python diag_read.py [COM_PORT]

Close the MSR605 app first - the port is exclusive.
"""

import sys
import time

import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "COM3"
WINDOW = 30

ser = serial.Serial(PORT, 9600, timeout=0.2)
ser.reset_input_buffer()

print(f"Port {PORT} open.")
print("Sending ESC+r (READ)...")
ser.write(b"\x1br")
ser.flush()

print(f"Swipe the card NOW - listening for {WINDOW}s")
print("(the device LED should be on; swipe BOTH directions)\n")

deadline = time.monotonic() + WINDOW
received = bytearray()
while time.monotonic() < deadline:
    chunk = ser.read(ser.in_waiting or 1)
    for b in chunk:
        received.append(b)
        t = time.monotonic()
        printable = chr(b) if 32 <= b < 127 else "."
        print(f"  t={t:7.2f}s  0x{b:02X}  '{printable}'")

print()
if received:
    print(f"RECEIVED {len(received)} bytes: {received.hex()}")
    print(f"As text: {received!r}")
else:
    print("RECEIVED NOTHING - the device never responded to the swipe.")

ser.close()
