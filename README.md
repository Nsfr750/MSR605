# MSR605 Card Reader/Writer

<div align="center">
  <img src="https://img.shields.io/badge/Version-2.3.0-blue" alt="Version 2.3.0">
  <img src="https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/GUI-PyQt6.6-blue" alt="PyQt6.6">
  <img src="https://img.shields.io/badge/License-GPLv3-blue" alt="GPLv3">
  <a href="https://github.com/Nsfr750/MSR605/actions">
    <img src="https://github.com/Nsfr750/MSR605/actions/workflows/tests.yml/badge.svg" alt="Build Status">
  </a>
  <a href="https://github.com/Nsfr750/MSR605/issues">
    <img src="https://img.shields.io/github/issues/Nsfr750/MSR605" alt="Issues">
  </a>
  <a href="https://codecov.io/gh/Nsfr750/MSR605">
    <img src="https://codecov.io/gh/Nsfr750/MSR605/branch/main/graph/badge.svg" alt="Code Coverage">
  </a>
</div>

## 🌟 Overview

**MSR605 Card Reader/Writer** is a sophisticated, open-source GUI application designed for reading, writing, and managing magnetic stripe cards using the MSR605 hardware. This powerful tool provides comprehensive card data management with advanced decoding and analysis capabilities.

### 🚀 What's New in v2.3.0

#### 🆕 New Features
- **Daily Log Rotation**: Automatic log file management with daily rotation
- **Enhanced UI**: New application icon and improved menu organization
- **Dark Mode**: System-aware theme switching with persistent settings
- **Update Notifications**: Built-in update checker with GitHub integration
- **Voice Control**: Moved to Tools menu for better accessibility
- **Sponsor Section**: Added to Help menu for supporting the project

#### 🛠 Improvements
- **Performance**: Optimized application startup time
- **Accessibility**: Enhanced translation support for all UI elements
- **Dependencies**: Replaced Pillow with Wand for better image processing
- **Code Quality**: Improved error handling and logging
- **Documentation**: Updated documentation and code comments

#### 🐛 Bug Fixes
- Fixed menu translation issues
- Resolved initialization order in menu system
- Fixed update checker timestamp parsing
- Improved cross-platform compatibility
- Fixed various UI layout issues

## 🚀 Features

### 🔍 Advanced Functions
- Dedicated window for advanced card operations
- Tabbed interface with detachable panels
- Detailed track data parsing and display with syntax highlighting
- Support for multiple encryption standards (AES-256, DES, 3DES)
- Hardware Security Module (HSM) integration
- Real-time data validation and sanitization
- Comprehensive audit logging
- Plugin system for extending functionality

### 🛠️ Card Operations
- 🔍 Read magnetic stripe cards with detailed analysis and validation
- ✍️ Write data to cards with verification and checksum validation
- 🧹 Erase card data (all tracks or selective) with confirmation
- 🔬 Advanced card data decoding with field extraction and formatting
- 🎯 Granular track-level controls with real-time preview
- 🔐 End-to-end encryption with hardware acceleration
- 🔄 Batch processing for multiple cards
- 📊 Data visualization and statistics

### 📊 Track Tools
- Set/Clear/Check Leading Zero with undo/redo support
- Configure Bits Per Inch (BPI) with presets for common standards
- Adjust Bits Per Character (BPC) with validation
- Raw data read/write capabilities with hex editor
- Track simulation and testing with pattern generation
- Checksum calculation and validation
- Data scrambling and descrambling
- Track data comparison and diff tools

### 💾 Data Management
- SQLite database with encryption
- Comprehensive card data viewer with advanced filtering
- 🚫 Duplicate card detection with fuzzy matching
- 📊 Export to multiple formats (CSV, JSON, XML, Excel)
- Advanced search with regular expressions
- Data import/export with validation
- Database backup and restore functionality
- Data anonymization for testing

### 🔍 Card Data Decoding
- **Track 1**: Card number, name, expiration, service code with validation
- **Track 2**: Card number, expiration, service restrictions with LRC validation
- **Track 3**: Financial data, encryption data with format validation
- Raw hex, binary, and ASCII data views with syntax highlighting
- Custom parsing rules with regular expressions
- Data validation against industry standards (ISO 7811, ISO 7813)
- Format-preserving encryption for sensitive data

## 🔧 Prerequisites

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

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Nsfr750/MSR605.git
cd MSR605
```

### 2. Set Up Python Environment
#### Using venv (Recommended)
```bash
# Create and activate virtual environment
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

#### Using conda (Alternative)
```bash
conda create -n msr605 python=3.10
conda activate msr605
```

### 3. Install Dependencies
```bash
# Install core requirements
pip install -r requirements.txt

# For development
pip install -r requirements-dev.txt
```

### 4. Run the Application
```bash
python -m msr605

# Or for development
python -m msr605 --debug
```

### 5. (Optional) Install as Package
```bash
pip install -e .
```

## 🖥️ Usage

### 🚀 Getting Started
1. Connect your MSR605 device
2. Launch the application
3. The application will auto-detect and connect to your device
4. Use the intuitive interface to read, write, and manage cards

### 🔄 Basic Workflow

#### Reading a Card
1. Insert a magnetic stripe card into the reader
2. Click `Read` or press `Ctrl+R`
3. View the decoded card data in the interface
4. Save to database or export as needed

#### Writing to a Card
1. Select the `Write` tab
2. Enter or load the data for each track
3. Insert a blank/erasable card
4. Click `Write` or press `Ctrl+W`
5. Verify the written data with the `Verify` option

### 🎛 Advanced Features

#### Batch Processing
1. Create a batch job with multiple card operations
2. Queue multiple read/write operations
3. Process the entire batch automatically

#### Plugin System
1. Install additional plugins from the `Plugins` menu
2. Enable/disable plugins as needed
3. Configure plugin settings

#### Voice Commands (Experimental)
1. Enable voice control in settings
2. Use voice commands like "read card" or "write track 1"
3. See `Help > Voice Commands` for available commands

### ⚙️ Configuration
- Customize the interface in `Settings > Appearance`
- Configure device parameters in `Settings > Device`
- Set up keyboard shortcuts in `Settings > Shortcuts`
- Manage database settings in `Settings > Database`

## ⚙️ Configuration

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

## 🐛 Troubleshooting

### Common Issues

#### Device Not Detected
- Verify the device is properly connected and powered on
- Check if the device appears in your system's device manager
- Try a different USB cable or port

#### Permission Issues (Linux)
```bash
# Add user to dialout group
sudo usermod -a -G dialout $USER

# Apply changes (log out and back in or run)
newgrp dialout

# Check device permissions
ls -l /dev/ttyUSB*
```

#### Dependency Problems
```bash
# Update pip
python -m pip install --upgrade pip

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Getting Help
- Check the `logs` directory for detailed error information
- Search the [GitHub Issues](https://github.com/Nsfr750/MSR605/issues) for similar problems
- Create a new issue with detailed reproduction steps

## 🛠️ Development

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

## 📜 License

MSR605 Card Reader/Writer is licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE) for the full license text.

## 💬 Support & Community

### Getting Help
- 📖 [Documentation](https://nsfr750.github.io/MSR605/)
- 🐛 [Report a Bug](https://github.com/Nsfr750/MSR605/issues/new?template=bug_report.md)
- 💡 [Request a Feature](https://github.com/Nsfr750/MSR605/issues/new?template=feature_request.md)
- ❓ [Ask a Question](https://github.com/Nsfr750/MSR605/discussions)

### Stay Connected
- 🌐 [GitHub Repository](https://github.com/Nsfr750/MSR605)
- 💬 [Discord Community](https://discord.gg/BvvkUEP9)
- 📰 [Project Blog](https://github.com/Nsfr750/MSR605/discussions/categories/announcements)

### Support the Project
- 💖 [GitHub Sponsors](https://github.com/sponsors/Nsfr750)
- 💰 [Patreon](https://www.patreon.com/Nsfr750)
- 💳 [PayPal](https://paypal.me/3dmega)

## 🏷️ Version Information

Current Version: 2.3.0 (Stable)
Release Date: July 19, 2025

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

## 📚 Resources

### Documentation
- [User Guide](https://nsfr750.github.io/MSR605/user-guide/)
- [Developer Documentation](https://nsfr750.github.io/MSR605/developer/)
- [API Reference](https://nsfr750.github.io/MSR605/api/)
- [FAQ](https://nsfr750.github.io/MSR605/faq/)

### Community
- [GitHub Discussions](https://github.com/Nsfr750/MSR605/discussions)
- [Issue Tracker](https://github.com/Nsfr750/MSR605/issues)
- [Contributing Guide](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)

## 🙏 Acknowledgments

Special thanks to all contributors and the open source community for their valuable feedback and contributions.
