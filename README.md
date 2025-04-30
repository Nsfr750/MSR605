# MSR605 Card Reader/Writer v2.0.1

## Overview
A powerful GUI application for reading, writing, and managing magnetic stripe cards using the MSR605 hardware.

## Latest Updates
- Added card data decoding functionality
- Improved GUI with Help and Support menus
- Enhanced database management
- Modern user interface with better error handling

## Project Information
- Version: 2.0.1
- Last Updated: April 30, 2025
- Author: Nsfr750
- Platform: Windows/Linux
- Python Version: 3.12 or higher
- License: GNU General Public License v3

## Required Libraries
- PySerial: For MSR605 communication (https://github.com/pyserial/pyserial)
- Tkinter: For the graphical user interface
- SQLite3: For database management

## Features
1. Card Operations:
   - Read magnetic stripe cards
   - Write data to cards
   - Erase card data
   - Decode card data according to ISO standards

2. Database Management:
   - Automatic card data storage
   - View saved card data
   - Duplicate detection

3. Hardware Controls:
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
   - Read cards: Reads all tracks from a card
   - Write cards: Write data to any track
   - Erase cards: Securely erase card data
   - Database: View stored cards and export to CSV
   - Settings: Configure auto-save and duplicates handling

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
