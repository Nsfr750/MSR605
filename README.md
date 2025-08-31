# MSR605 Card Reader/Writer

![Version](https://img.shields.io/badge/Version-2.4.1-blue)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue)
![GUI](https://img.shields.io/badge/GUI-PyQt6.6-blue)
![License](https://img.shields.io/badge/License-GPLv3-blue)
[![Issues](https://img.shields.io/github/issues/Nsfr750/MSR605)](https://github.com/Nsfr750/MSR605/issues)
[![Code Coverage](https://codecov.io/gh/Nsfr750/MSR605/branch/main/graph/badge.svg)](https://codecov.io/gh/Nsfr750/MSR605)

## 🌟 Overview

**MSR605 Card Reader/Writer** is a sophisticated, open-source GUI application designed for reading, writing, and managing magnetic stripe cards using the MSR605 hardware. This powerful tool provides comprehensive card data management with advanced decoding and analysis capabilities.

### What's New in v2.4.1

#### UI/UX Improvements
- Added flag emojis (🇬🇧/🇮🇹) to language selection menu
- Fixed menu text visibility and styling
- Resolved menu item duplication on language change

#### What's New in v2.4.0

#### New Features

- **Daily Log Rotation**: Automatic log file management with daily rotation
- **Enhanced Error Handling**: More detailed error messages and recovery options
- **Performance Optimizations**: Faster card reading and writing operations
- **New Card Formats**: Support for additional card formats and standards
- **UI Improvements**: Streamlined interface and better dark mode support

#### Bug Fixes

- Fixed issue with special characters in card data
- Resolved database locking problems
- Fixed memory leaks in long-running sessions
- Addressed UI freezing during card operations
- Corrected error in track data parsing

#### Dependencies

- Upgraded to PyQt6.6
- Updated cryptography library to latest version
- Added new dependencies for enhanced functionality

#### Documentation

- Completely revised user manual
- Added API documentation
- Improved code comments
- New troubleshooting guides

## Features

### Advanced Functions

- Dedicated window for advanced card operations
- Tabbed interface with detachable panels
- Detailed track data parsing and display with syntax highlighting
- Support for multiple encryption standards (AES-256, DES, 3DES)
- **Multiple Card Format Support**: Full support for both ISO 7811 and ISO 7813 standards
- Hardware Security Module (HSM) integration
- Real-time data validation and sanitization
- Comprehensive audit logging
- Plugin system for extending functionality

### Core Features

- Read and write magnetic stripe cards (tracks 1, 2, and 3)
  - **ISO 7811**: Support for alphanumeric track 1 and numeric tracks 2/3
  - **ISO 7813**: Support for financial transaction cards with enhanced validation
- Real-time card data visualization
- Multi-language support
- Cross-platform compatibility (Windows, Linux, macOS)
- Logging system with daily rotation
- **Erase Card Data**: Erase card data (all tracks or selective) with confirmation
- **Advanced Card Data Decoding**: Advanced card data decoding with field extraction and formatting
- **Granular Track-Level Controls**: Granular track-level controls with real-time preview
- **End-to-End Encryption**: End-to-end encryption with hardware acceleration
- **Batch Processing**: Batch processing for multiple cards
- **Data Visualization and Statistics**: Data visualization and statistics

### Track Tools

- Set/Clear/Check Leading Zero with undo/redo support
- Configure Bits Per Inch (BPI) with presets for common standards
- Adjust Bits Per Character (BPC) with validation
- Raw data read/write capabilities with hex editor
- Track simulation and testing with pattern generation
- Checksum calculation and validation
- Data scrambling and descrambling
- Track data comparison and diff tools

### Data Management

- SQLite database with encryption
- Comprehensive card data viewer with advanced filtering
- **Duplicate Card Detection**: Duplicate card detection with fuzzy matching
- **Export to Multiple Formats**: Export to multiple formats (CSV, JSON, XML, Excel)
- Advanced search with regular expressions
- Data import/export with validation
- Database backup and restore functionality
- Data anonymization for testing

### Card Data Decoding

- **Track 1**: Card number, name, expiration, service code with validation
- **Track 2**: Card number, expiration, service restrictions with LRC validation
- **Track 3**: Financial data, encryption data with format validation
- Raw hex, binary, and ASCII data views with syntax highlighting
- Custom parsing rules with regular expressions
- Data validation against industry standards (ISO 7811, ISO 7813)
- Format-preserving encryption for sensitive data

## Prerequisites

### System Requirements

- **OS**: Windows 10/11, Linux (Ubuntu 22.04+, Debian 11+, Fedora 36+)
- **Python**: 3.10, 3.11, or 3.12
- **Hardware**: MSR605 Card Reader (USB or Serial)
- **Dependencies**: See [PREREQUISITES.md](PREREQUISITES.md) for detailed requirements

### Recommended Hardware

- **Processor**: Dual-core 2.0 GHz or better
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 100MB available space
- **Display**: 1366x768 resolution minimum

## Installation

### Prerequisites

- Python 3.10, 3.11, or 3.12
- MSR605 Hardware Reader
- USB connection

### Windows

```bash
# Clone the repository
git clone https://github.com/Nsfr750/MSR605.git
cd MSR605

# Create a virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Linux/macOS

```bash
# Clone the repository
git clone https://github.com/Nsfr750/MSR605.git
cd MSR605

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python3 main.py
```

## Usage

### Basic Operations

1. Connect your MSR605 device
2. Insert a card
3. Click 'Read' to read card data
4. Edit the data if needed
5. Click 'Write' to write to a new card

### Advanced Features

- Use the database tab to manage card records
- Export/import card data in various formats
- Create and run custom scripts for automation
- Configure application settings in the settings menu

## Configuration

### Configuration Files

- `config.ini`: Main application configuration
- `keyring.json`: Secure storage for encryption keys
- `logging.conf`: Logging configuration

### Key Configuration Options

#### Database

- **Type**: SQLite (default), PostgreSQL, or MySQL
- **Encryption**: Enable/disable database encryption
- **Backup**: Automatic backup settings

#### Device

- **Connection**: Auto-detect or manual port selection
- **Baud Rate**: Communication speed (default: 9600)
- **Timeout**: Operation timeout in seconds

#### Security

- **Encryption**: Enable/disable data encryption
- **Key Storage**: File-based or OS keyring
- **Access Control**: User permissions and roles

#### UI

- **Theme**: Light, Dark, or System
- **Layout**: Customize panel positions
- **Fonts**: Customize application fonts

## Troubleshooting

### Common Issues

- **Device Not Detected**: Verify the device is properly connected and powered on
- **Permission Issues (Linux)**: Add user to dialout group and apply changes
- **Dependency Problems**: Update pip and reinstall requirements

### Getting Help

- Check the `logs` directory for detailed error information
- Search the [GitHub Issues](https://github.com/Nsfr750/MSR605/issues) for similar problems
- Create a new issue with detailed reproduction steps

## Development

### Getting Started

1. Fork the repository
2. Clone your fork
3. Set up a development environment

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests with coverage
pytest --cov=msr605 tests/

# Format code (automatically runs on commit)
black .

# Lint code (automatically checks on commit)
flake8

# Type checking
mypy msr605/
```

### Building Documentation

```bash
# Install documentation dependencies
pip install -r docs/requirements.txt

# Build HTML documentation
cd docs
make html

# View documentation
start _build/html/index.html  # Windows
xdg-open _build/html/index.html  # Linux
open _build/html/index.html  # macOS
```

### Contributing

1. Create a feature branch (`git checkout -b feature/AmazingFeature`)
2. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
3. Push to the branch (`git push origin feature/AmazingFeature`)
4. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

## License

MSR605 Card Reader/Writer is licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE) for the full license text.

## Support & Community

### Getting Help

- 📖 [Documentation](https://github.com/Nsfr750/MSR605/wiki)
- 🐛 [Report a Bug](https://github.com/Nsfr750/MSR605/issues/new?template=bug_report.md)
- 💡 [Request a Feature](https://github.com/Nsfr750/MSR605/issues/new?template=feature_request.md)
- ❓ [Ask a Question](https://github.com/Nsfr750/MSR605/discussions)

### Stay Connected

- 🌐 [GitHub Repository](https://github.com/Nsfr750/MSR605)
- 💬 [Discord Community](https://discord.gg/BvvkUEP9)
- 📰 [Project Blog](https://nsfr750.github.io/)

### Support the Project
- 💖 [GitHub Sponsors](https://github.com/sponsors/Nsfr750)
- 💰 [Patreon](https://www.patreon.com/Nsfr750)
- 💳 [PayPal](https://paypal.me/3dmega)

## 🏷️ Version Information

Current Version: 2.4.0 (Stable)
Release Date: July 20, 2025

### What's New in v2.3.0
- Added voice command support
- New plugin system
- Dark/light theme support
- Performance improvements
- Enhanced security features

### System Requirements
- Python 3.10, 3.11, or 3.12
- Windows 10/11 or Linux
- MSR605 Hardware Reader
