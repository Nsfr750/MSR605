# MSR605 Card Reader/Writer - User Guide

Welcome to the MSR605 Card Reader/Writer user guide! This document will help you get started with using the application to read from and write to magnetic stripe cards.

## Table of Contents

1. [Installation](#installation)
2. [Getting Started](#getting-started)
3. [Reading Cards](#reading-cards)
4. [Writing Cards](#writing-cards)
5. [Configuration](#configuration)
6. [Troubleshooting](#troubleshooting)

## Installation

### Windows

1. Download the latest installer from the [Releases](https://github.com/yourusername/MSR605/releases) page
2. Run the installer and follow the on-screen instructions
3. Connect your MSR605 device to an available USB port
4. Launch the application from the Start Menu or desktop shortcut

### Linux/macOS

1. Ensure you have Python 3.8+ installed
2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python main.py
   ```

## Getting Started

### Connecting the Device

1. Connect your MSR605 device to your computer using the USB cable
2. The application should automatically detect the device
3. The status bar will show "Device Connected" when successful

### Main Interface

- **Card Data Display**: Shows the data read from the card
- **Track Selection**: Choose which tracks to read/write (1, 2, and/or 3)
- **Action Buttons**: Read, Write, and Clear functions
- **Status Bar**: Displays connection status and operation results

## Reading Cards

1. Insert a magnetic stripe card into the reader
2. Click the "Read" button
3. The card data will be displayed in the main window
4. To save the data, click "File" > "Save As..."

## Writing Cards

1. Insert a writable magnetic stripe card into the writer
2. Enter or paste the data you want to write in the appropriate track fields
3. Select which tracks you want to write to
4. Click the "Write" button
5. The status bar will show the result of the operation

## Card Format Support

The application supports two major magnetic card standards: ISO 7811 and ISO 7813. Understanding these formats is crucial for proper card reading and writing operations.

### ISO 7811

ISO 7811 is the international standard for identification cards with magnetic stripes. It defines:

- **Track 1**: Alphanumeric data (up to 79 characters)
  - Format: `%[format code][primary account number]^[name]^[expiration date][service code][discretionary data]?`
  - Example: `%B1234567890123456^CARDHOLDER/NAME^24011234567890123456789?`

- **Track 2**: Numeric data (up to 40 characters)
  - Format: `;[primary account number]=[expiration date][service code][discretionary data]?`
  - Example: `;1234567890123456=24011234567890123456?`

- **Track 3**: Read/write capability (not commonly used)
  - Primarily numeric data
  - Used for financial transactions and value updates

### ISO 7813

ISO 7813 is a subset of ISO 7811 specifically for financial transaction cards. Key differences:

- **Track 1**: More strictly formatted
  - Format code must be 'B' (banking)
  - Fixed field lengths for certain data elements
  - Example: `%B1234567890123456^CARDHOLDER/NAME^24011234567890123456789?`

- **Track 2**: Similar to ISO 7811 but with specific validation rules
  - Example: `;1234567890123456=24011234567890123456?`

### Selecting the Correct Format

1. Go to **Settings** > **Card Format**

2. Choose between:

   - **Auto-detect** (default): Automatically detects the card format
   - **ISO 7811**: For general purpose cards
   - **ISO 7813**: For financial transaction cards

3. Click **Apply** to save the settings

## Writing Cards

1. Select the tracks you want to write to
2. Choose the appropriate card format (ISO 7811 or ISO 7813)
3. Enter the data in the appropriate track fields following the selected format
4. Click the "Write" button
5. The application will validate the data and perform the write operation
6. The operation status will be displayed in the status bar

## Configuration

### Device Settings

- **Baud Rate**: Adjust the communication speed (default: 9600)
- **Parity**: Set the parity (None, Even, Odd, Mark, Space)
- **Data Bits**: Set the number of data bits (default: 8)
- **Stop Bits**: Set the number of stop bits (default: 1)

### Application Settings

- **Auto-detect Device**: Enable/disable automatic device detection
- **Start Minimized**: Launch the application minimized to system tray
- **Save Logs**: Enable logging of operations to a file

## Troubleshooting

### Common Issues

#### Device Not Detected

- Ensure the device is properly connected to the USB port
- Try a different USB port
- Check if the device is recognized in your system's Device Manager
- Restart the application

#### Reading/Writing Fails

- Ensure the card is properly inserted
- Clean the card's magnetic stripe
- Verify the card is not write-protected
- Check the track configuration matches the card format

#### Application Crashes

- Ensure you have the latest version installed
- Check the log file for error details
- Try reinstalling the application

## Support

For additional help, please:

- Check the [FAQ](FAQ.md)

- Search or open an issue on [GitHub](https://github.com/yourusername/MSR605/issues)
