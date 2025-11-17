# Frequently Asked Questions (FAQ) - v2.4.5+

## Version 2.4.5 Updates

### What's new in version 2.4.5?

- **CI/CD Integration**: Automated testing and deployment pipeline
- **Improved Stability**: Better error handling and recovery
- **Enhanced Security**: Updated dependencies and security patches
- **Better Performance**: Optimized card reading/writing operations
- **Automatic Updates**: Notifications for new versions

### How do I update to version 2.4.5?

1. Download the latest version from the [Releases](https://github.com/Nsfr750/MSR605/releases) page
2. Run the installer (it will automatically detect and update existing installations)
3. Restart the application

### Where can I find the changelog?

The complete changelog is available in the [CHANGELOG.md](CHANGELOG.md) file.

## General Questions

### What is the MSR605 Card Reader/Writer?

The MSR605 is a software application that allows you to read from and write to magnetic stripe cards using compatible card reader/writer devices. It provides a user-friendly interface for managing card data.

### What operating systems are supported?

The application is designed to work on:

- Windows 10/11 (64-bit)
- Linux (most distributions)
- macOS (Intel and Apple Silicon)

### Where can I download the latest version?

You can download the latest release from our [GitHub Releases](https://github.com/Nsfr750/MSR605/releases) page.

## Installation

### What are the system requirements?

- **Operating System**:
  - Windows 10/11 (64-bit)
  - Linux (Ubuntu 20.04+ recommended)
  - macOS 10.15+
- **Python**: 3.8, 3.9, 3.10, or 3.12 (3.10+ recommended)
- **Hardware**:
  - USB 2.0+ port
  - 2GB RAM minimum (4GB recommended)
  - 200MB free disk space
  - MSR605-compatible card reader/writer

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

## CI/CD and Updates

### How does the CI/CD pipeline benefit me?

- More frequent and reliable updates
- Automated testing ensures higher quality releases
- Faster bug fixes and security updates
- Better tracking of changes and issues

### How do I know when updates are available?

The application will notify you in the status bar when a new version is available. You can also check manually in **Help** > **Check for Updates**.

### How do I report an issue with the new version?

Please include the following information when reporting issues:
- Version number (2.4.5+)
- Operating system and version
- Steps to reproduce the issue
- Any error messages from the log file

## Security

### Is my card data secure?

The application processes all data locally on your computer. No card data is transmitted over the internet unless you explicitly choose to export or share it.

### Can I encrypt the card data?

Yes, the application supports encrypting card data before writing to the card. Enable this option in the settings.

### What security features are available in 2.4.5?

- **Enhanced Data Encryption**: Stronger encryption algorithms
- **Secure Settings Storage**: Protected storage for connection settings
- **Audit Logging**: Detailed operation logging
- **Secure Data Wiping**: Multiple pass secure erase
- **Dependency Updates**: All dependencies updated to their latest secure versions
- **Automatic Security Patches**: Through the new update system

## Development and Contribution

### How has the development process changed in 2.4.5?

The project now uses GitHub Actions for continuous integration and deployment, which means:

- Automated testing on multiple platforms
- Automatic builds for each commit
- Streamlined release process
- Better code quality control

### How can I contribute to the project?

We welcome contributions! Please see our updated [Contributing Guidelines](CONTRIBUTING.md) for information on:

- Setting up a development environment
- Submitting pull requests
- Reporting issues
- Code style and standards


### Is there an API available?

Yes, the application provides a Python API for integration with other applications. See the [API Documentation](API.md) for details.

### How do I report a bug?

Please open an issue on our [GitHub Issues](https://github.com/Nsfr750/MSR605/issues) page with the following information:

- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- System information

## Support and Troubleshooting

### Where can I get help with version 2.4.5?

- Check the updated [User Guide](USER_GUIDE.md)
- Review the [Troubleshooting Guide](TROUBLESHOOTING.md)
- Search or post on [GitHub Discussions](https://github.com/Nsfr750/MSR605/discussions)
- Check the [CI/CD Status](https://github.com/Nsfr750/MSR605/actions) for known issues

### How do I enable debug logging?

1. Go to **Settings** > **Advanced**
2. Enable "Debug Mode"
3. Restart the application
4. Logs will be saved to the application data directory


## Legal

### What are the licensing terms?

This software is licensed under the GPLv3 License. See the [LICENSE](LICENSE) file for details.

### Can I use this for commercial purposes?

Yes, the GPLv3 license allows for commercial use, but be aware of the license requirements regarding distribution of source code for any modifications you make.

### Where can I find the source code?

The complete source code is available on [GitHub](https://github.com/Nsfr750/MSR605).
