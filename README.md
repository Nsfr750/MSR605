# MSR605 Card Reader/Writer

<div align="center">
  <img src="https://img.shields.io/badge/Version-2.1.0-blue" alt="Version 2.1.0">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/License-GPLv3-blue" alt="GPLv3">
  <a href="https://github.com/Nsfr750/MSR605/issues">
    <img src="https://img.shields.io/github/issues/Nsfr750/MSR605" alt="Issues">
  </a>
</div>

## 🌟 Overview

**MSR605 Card Reader/Writer** is a sophisticated, open-source GUI application designed for reading, writing, and managing magnetic stripe cards using the MSR605 hardware. This powerful tool provides comprehensive card data management with advanced decoding and analysis capabilities.

## 🚀 Features

### 🔍 Advanced Functions
- Dedicated window for advanced card operations
- Tabbed interface for easy navigation
- Detailed track data parsing and display
- Support for multiple encryption standards (AES, DES, 3DES)
- Enhanced error handling and logging
- Real-time data validation

### 🛠️ Card Operations
- 🔍 Read magnetic stripe cards with detailed analysis
- ✍️ Write data to cards with verification
- 🧹 Erase card data (all tracks or selective)
- 🔬 Advanced card data decoding with field extraction
- 🎯 Granular track-level controls
- 🔐 End-to-end encryption support

### 📊 Track Tools
- Set/Clear/Check Leading Zero
- Configure Bits Per Inch (BPI)
- Adjust Bits Per Character (BPC)
- Raw data read/write capabilities
- Track simulation and testing

### 💾 Data Management
- SQLite database integration
- Comprehensive card data viewer
- 🚫 Duplicate card detection
- 📊 Export to multiple formats (CSV, JSON)
- Advanced search and filtering

### 🔍 Card Data Decoding
- **Track 1**: Card number, name, expiration, service code
- **Track 2**: Card number, expiration, service restrictions
- **Track 3**: Financial data, encryption data
- Raw hex and binary data views
- Custom parsing rules

## 🔧 Prerequisites

### System Requirements
- **OS**: Windows 10/11, Linux (tested on Ubuntu 22.04+)
- **Python**: 3.10 or higher
- **Hardware**: MSR605 Card Reader
- **Dependencies**: See `requirements.txt`

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Nsfr750/MSR605.git
cd MSR605
```

### 2. Create and Activate Virtual Environment (Recommended)
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 🖥️ Usage

### Starting the Application
```bash
python GUI.py
```

### Basic Workflow
1. Connect your MSR605 hardware
2. Select card coercivity (HI-CO/LOW-CO)
3. Read, write, or decode cards
4. Save to database or export as needed

## ⚙️ Configuration

Configuration is handled through `config.ini`:
- Database location
- Default card preferences
- UI settings
- Hardware parameters

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Format code
black .

# Lint code
flake8
```

## 📜 License

Distributed under the GNU General Public License v3.0. See `LICENSE` for more information.

## 💬 Support

- 📧 Email: nsfr750@yandex.com
- 🌐 Website: https://github.com/Nsfr750/MSR605
- 💸 Support the project: [Sponsor Link](https://github.com/sponsors/Nsfr750)

## 🏷️ Version

Current Version: 2.0.1 (Beta)
Last Updated: May 15, 2025
   - Hi/Lo coercivity settings
   - LED indicators
   - Device testing utilities

## Social Links

- [Patreon](https://www.patreon.com/Nsfr750)
- [GitHub](https://github.com/Nsfr750)
- [Discord](https://discord.gg/BvvkUEP9)
- [Paypal](https://paypal.me/3dmega)
