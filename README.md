# MSR605 Card Reader/Writer

## 🌟 Overview

**MSR605 Card Reader/Writer** is a sophisticated, open-source GUI application designed for reading, writing, and managing magnetic stripe cards using the MSR605 hardware. This powerful tool provides comprehensive card data management with advanced decoding and analysis capabilities.

## 🚀 Features

### 1. Card Operations
- 🔍 Read magnetic stripe cards
- ✍️ Write data to cards
- 🧹 Erase card data
- 🔬 Advanced card data decoding
- 🛠️ Granular track-level controls

### 2. Advanced Track Tools
- Set/Clear/Check Leading Zero
- Select Bits Per Inch (BPI)
- Configure Bits Per Character (BPC)
- Raw data read/write capabilities

### 3. Database Management
- 💾 Automatic card data storage
- 📋 Comprehensive card data viewer
- 🚫 Duplicate card detection
- 📊 Export to CSV

### 4. Card Data Decoding
Detailed parsing for all three tracks:
- Track 1: Card number, name, expiration
- Track 2: Card number, service code
- Track 3: Raw data analysis

## 🔧 Prerequisites

### System Requirements
- **Operating System**: Windows 10/11, Linux
- **Python**: 3.12 or higher
- **Hardware**: MSR605 Card Reader

### Dependencies
- PySerial
- Tkinter
- SQLite3
- binascii

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Nsfr750/MSR605.git
cd MSR605
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

## 🖥️ Usage

### Starting the Application
```bash
python GUI.py
```

### Basic Workflow
1. Connect MSR605 hardware
2. Select card coercivity (HI-CO/LOW-CO)
3. Read, write, or decode cards
4. Optionally save to database

## 📋 Configuration

- Adjust settings in `config.ini`
- Customize database location
- Set default card preferences

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

Distributed under the GNU General Public License v3.0. See `LICENSE` for more information.

## 💬 Support

- 📧 Email: support@nsfr750.com
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
- [Payapal](https://paypal.me/3dmega)
