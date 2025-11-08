# MSR605 Troubleshooting Guide

This guide provides solutions to common issues you might encounter while using the MSR605 card reader/writer.

## Table of Contents
- [Permission Denied Errors](#permission-denied-errors)
- [Device Not Detected](#device-not-detected)
- [Card Read/Write Failures](#card-readwrite-failures)
- [Communication Errors](#communication-errors)
- [LED Indicators](#led-indicators)
- [Common Error Messages](#common-error-messages)

## Permission Denied Errors

### Error: `[Errno 13] could not open port /dev/ttyUSB0: [Errno 13] Permesso negato: '/dev/ttyUSB0'`

**Solution:**
1. Add your user to the `dialout` group:

   ```bash
   sudo usermod -a -G dialout $USER
   newgrp dialout  # Or log out and back in
   ls -l /dev/ttyUSB0
   ```

   If you still have problems, try:

   ```bash
   sudo chmod 666 /dev/ttyUSB0
   ```

2. For a permanent solution, create a udev rule:

   ```bash
   echo 'KERNEL=="ttyUSB[0-9]*", MODE="0666", GROUP="dialout"' | sudo tee /etc/udev/rules.d/99-msr605.rules
   sudo udevadm control --reload-rules
   sudo udevadm trigger
   ```

3. Alternative permanent solution: Add the following line to `/etc/udev/rules.d/99-usb-serial.rules`:

   ```bash
   ATTRS{idVendor}=="067b", ATTRS{idProduct}=="2303", MODE="0666"
   ```

   Then reload the udev rules:

   ```bash
   sudo udevadm control --reload-rules && sudo udevadm trigger
   ```

## Device Not Detected

### MSR605 not showing up as /dev/ttyUSB0

**Solution:**
1. Check if the device is detected by the system:

   ```bash
   dmesg | grep -i usb
   lsusb
   ```

2. Look for the Prolific USB-to-Serial adapter in the output. If not found:
   - Try a different USB port
   - Try a different USB cable
   - Check if the device is powered on (LED should be on)

3. If using a VM, ensure USB passthrough is properly configured

## Card Read/Write Failures

### Card swipe not detected

**Solution:**
1. Ensure the card is swiped in the correct direction (magnetic stripe down, stripe facing the device)
2. Try different swipe speeds (not too fast, not too slow)
3. Clean the card's magnetic stripe with a soft, dry cloth
4. Check if the card is demagnetized by trying a different card

### Write operation fails

**Solution:**
1. Ensure the card is a writable magnetic stripe card
2. Check if the card is write-protected (some cards have a write-protect notch)
3. Verify the card format matches the expected format (ISO 7811 or ISO 7813)
4. Try setting the correct coercivity mode:

   ```python
   # For high-coercivity (Hi-Co) cards (most common)
   reader.set_hi_co()
   
   # For low-coercivity (Lo-Co) cards
   # reader.set_low_co()
   ```

## Communication Errors

### Timeout or No Response

**Solution:**
1. Check the baud rate (default is 9600)
2. Verify the correct port is being used
3. Try resetting the device:

   ```python
   reader.reset()
   ```
4. Test communication:

   ```python
   reader.communication_test()
   ```

## LED Indicators

| LED Color | State | Meaning |
|-----------|-------|---------|
| Red       | On    | Error or write mode |
| Yellow    | On    | Ready for card swipe |
| Green     | On    | Operation successful |
| All LEDs  | Blink | Device initializing |

## Common Error Messages

### `MSR605ConnectError: Could not find MSR605 on any COM port`
- Check USB connection
- Verify the device is powered on
- Try a different USB port
- Check if the device is recognized by the system with `lsusb`

### `CardReadError: Failed to read card data`
- Clean the card's magnetic stripe
- Try a different card
- Check if the card is properly aligned during swipe
- Verify the track data format matches expectations

### `StatusError: Device reported error status`
- Reset the device
- Check the card format
- Verify the track specifications match the card type

## Additional Help

If you're still experiencing issues:
1. Check the project's [GitHub Issues](https://github.com/Nsfr750/MSR605/issues) for similar problems
2. Ensure you're using the latest version of the software
3. Try the `examples/` directory for working code samples
4. Check the device's documentation for specific requirements

## Hardware Troubleshooting

1. **Device not powering on**
   - Check USB cable and port
   - Try a different power source
   - Check for physical damage

2. **Intermittent connections**
   - Try a different USB cable
   - Avoid using USB hubs if possible
   - Check for loose connections

3. **Card jamming**
   - Remove any stuck cards carefully
   - Check for debris in the card slot
   - Do not force cards into the reader

# Common Issues

## Device Not Detected

    Ensure the device is properly connected to the USB port
    Try a different USB port
    Check if the device is recognized in your system's Device Manager
    Restart the application

## Reading/Writing Fails

    Ensure the card is properly inserted
    Clean the card's magnetic stripe
    Verify the card is not write-protected
    Check the track configuration matches the card format

## Application Crashes

    Ensure you have the latest version installed
    Check the log file for error details
    Try reinstalling the application
