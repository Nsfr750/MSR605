# Frequently Asked Questions (FAQ)

## General Questions

### What is the MSR605 Card Reader/Writer?
The MSR605 is a software application that allows you to read from and write to magnetic stripe cards using compatible card reader/writer devices. It provides a user-friendly interface for managing card data.

### What operating systems are supported?
The application is designed to work on:
- Windows 10/11 (64-bit)
- Linux (most distributions)
- macOS (Intel and Apple Silicon)

### Where can I download the latest version?
You can download the latest release from our [GitHub Releases](https://github.com/yourusername/MSR605/releases) page.

## Installation

### What are the system requirements?
- Python 3.8 or higher
- USB port for the card reader
- 100MB free disk space
- 2GB RAM minimum (4GB recommended)

### How do I install the required drivers?
- **Windows**: Drivers should install automatically when you connect the device
- **Linux**: Most distributions include the necessary drivers
- **macOS**: No additional drivers are typically needed

### Why isn't my device being detected?
1. Ensure the device is properly connected to a USB port
2. Try a different USB port
3. Check if the device appears in your system's device manager
4. Restart the application
5. Make sure no other application is using the device

## Usage

### How do I read a card?
1. Insert the card into the reader
2. Click the "Read" button
3. The card data will be displayed in the main window

### How do I write to a card?
1. Insert a writable card
2. Enter the data you want to write
3. Select which tracks to write to
4. Click the "Write" button

### What card formats are supported?
The application supports standard magnetic stripe formats:
- Track 1 (IATA): Up to 79 alphanumeric characters
- Track 2 (ABA): Up to 40 numeric characters
- Track 3 (THRIFT): Up to 107 numeric characters

### Why is my card not being read?
- The card may be damaged or demagnetized
- The card might be inserted incorrectly
- The magnetic stripe might be dirty (clean it with a soft cloth)
- The card format might not be supported

## Troubleshooting

### The application crashes on startup
1. Make sure you have all required dependencies installed
2. Check the log file for error messages
3. Try reinstalling the application
4. Contact support with the error details

### I'm getting "Device not found" errors
1. Disconnect and reconnect the device
2. Try a different USB port
3. Restart your computer
4. Check if the device is recognized by your operating system

### The data written to the card isn't being read correctly
1. Verify the data format matches the track specifications
2. Try writing to a different track
3. Test with a different card
4. Check if the write head needs cleaning

## Security

### Is my card data secure?
The application processes all data locally on your computer. No card data is transmitted over the internet unless you explicitly choose to export or share it.

### Can I encrypt the card data?
Yes, the application supports encrypting card data before writing to the card. Enable this option in the settings.

### What security features are available?
- Data encryption
- Password protection for saved files
- Secure data wiping
- Audit logging

## Development

### How can I contribute to the project?
We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more information.

### Is there an API available?
Yes, the application provides a Python API for integration with other applications. See the [API Documentation](API.md) for details.

### How do I report a bug?
Please open an issue on our [GitHub Issues](https://github.com/yourusername/MSR605/issues) page with the following information:
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- System information

## Support

### Where can I get help?
- Check the [User Guide](user_guide.md) for detailed instructions
- Search or post on our [GitHub Discussions](https://github.com/yourusername/MSR605/discussions)
- Email support@example.com for direct assistance

### Is there a community forum?
Yes, you can join our community forum at [forum.example.com](https://forum.example.com) to ask questions and share experiences with other users.

## Legal

### What are the licensing terms?
This software is licensed under the GPLv3 License. See the [LICENSE](LICENSE) file for details.

### Can I use this for commercial purposes?
Yes, the GPLv3 license allows for commercial use, but be aware of the license requirements regarding distribution of source code for any modifications you make.

### Where can I find the source code?
The complete source code is available on [GitHub](https://github.com/yourusername/MSR605).
