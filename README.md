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

## Hardware Description
The MSR605 is a versatile magnetic stripe card reader/writer compatible with standard magstripe cards (credit cards, debit cards, ID cards, etc.). It supports reading and writing on all three tracks of magnetic stripe cards.

## Technical Details
- Follows ISO standards for magnetic stripe encoding
- Supports all three tracks (Track 1, 2, and 3)
- Includes comprehensive error handling
- Built-in hardware diagnostic tools

## File Structure
- `GUI.py`: Main graphical interface and application entry point
- `cardReader.py`: MSR605 interface implementation for serial communication
- `cardReaderExceptions.py`: Custom exception handling for device operations

## Installation
1. Install Python 3.8 or higher
2. Install required packages: `pip install -r requirements.txt`
3. Clone the repository
4. Run `GUI.py`

## Usage
1. Connect MSR605 to your computer via USB
2. Launch the application
3. Click "Connect to MSR605"
4. Set appropriate coercivity (HI-CO/LOW-CO)
5. Use the application features:
   - **Main Actions:**
     - Read cards: Reads all tracks from a card
     - Write cards: Write data to any track
     - Erase cards: Securely erase card data
   - **Advanced Track Tools:**
     - Set/Clear/Check Leading Zero for any track
     - Select BPI (75 or 210) and set BPC (5, 7, or 8)
     - Read and write raw data to any track
   - **Database:** View stored cards and export to CSV
   - **Settings:** Configure auto-save and duplicates handling
   - **GUI Layout:** All button groups are organized in two columns for easier access

## Database Features
- Automatic card data storage (optional)
- View stored cards in a sortable table
- Export database to CSV
- Duplicate card detection
- Timestamps for all entries
- Data stored in user's Documents folder

## Contributing
Contributions are welcome! Please feel free to submit pull requests or report issues on GitHub.

## Known Issues
- Please report any bugs or issues on the GitHub issue tracker
- For hardware-specific issues, consult the MSR605 manual

## License
GNU General Public License v3

## Social Links

- [Patreon](https://www.patreon.com/Nsfr750)
- [GitHub](https://github.com/Nsfr750)
- [Discord](https://discord.gg/BvvkUEP9)
- [Payapal](https://paypal.me/3dmega)

## ToDo

- Add better decode of data