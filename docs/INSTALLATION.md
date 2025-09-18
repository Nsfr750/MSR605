# Installation Guide for MSR605 Card Reader/Writer

## Prerequisites

### System Requirements

- **Operating System**:

  - Windows 10/11 (64-bit)
  - Linux (Ubuntu 20.04 or later)
  - macOS 10.15 or later
- **Python**: 3.12 or higher
- **Hardware**: MSR605 Card Reader

### Required Hardware

- MSR605 Magnetic Card Reader/Writer
- USB-to-Serial Adapter (if not included with MSR605)
- Compatible magnetic stripe cards (ISO 7813)

## Installation Steps

### 1. Python Installation

1. Download Python 3.12+ from [official Python website](https://www.python.org/downloads/)
2. During installation, ensure "Add Python to PATH" is checked
3. Verify installation:

   ```bash
   python --version
   pip --version
   ```

### 2. Clone Repository

```bash
git clone https://github.com/Nsfr750/MSR605.git
cd MSR605
```

### 3. Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Hardware Setup

1. Connect MSR605 to computer via USB/Serial
2. Install any necessary device drivers
3. Verify device recognition:

   ```bash
   python -m serial.tools.list_ports
   ```

### 6. Run Application

```bash
python GUI.py
```

## Troubleshooting

- Ensure all dependencies are installed
- Check serial port connections
- Verify Python version compatibility
- Consult [GitHub Issues](https://github.com/Nsfr750/MSR605/issues) for known problems

## Uninstallation

```bash
# Deactivate virtual environment
deactivate

# Remove project directory
rm -rf MSR605
```
