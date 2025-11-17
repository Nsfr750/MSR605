# Installation Guide for MSR605 Card Reader/Writer (v2.4.5+)

## Prerequisites

### System Requirements

- **Operating System**:
  - Windows 10/11 (64-bit)
  - Linux (Ubuntu 20.04 or later)
  - macOS 10.15 or later
- **Python**: 3.8, 3.9, 3.10, or 3.12 (3.11+ recommended)
- **Hardware**: MSR605 Card Reader
- **Disk Space**: Minimum 100MB free space
- **Memory**: 2GB RAM minimum (4GB recommended)

### Required Hardware

- MSR605 Magnetic Card Reader/Writer
- USB-to-Serial Adapter (if not included with MSR605)
- Compatible magnetic stripe cards (ISO 7813)

## Installation Methods

### Method 1: Using Pre-built Executable (Recommended for End Users)

1. **Download the latest release** from [GitHub Releases](https://github.com/Nsfr750/MSR605/releases)
2. **Run the installer** (Windows) or extract the package (Linux/macOS)
3. **Launch the application**
   - Windows: Double-click `MSR605.exe`
   - Linux/macOS: Run `./MSR605` from terminal

### Method 2: From Source (For Developers)

#### Prerequisites
- Git
- Python 3.8+
- pip (Python package manager)
- Build tools (for compiling dependencies)

## Source Installation Steps

### 1. Install Python

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
# Development mode
python main.py

# Or build and run the executable
python -m PyInstaller --onefile --name MSR605 --icon=assets/icon.ico main.py
./dist/MSR605
```

## CI/CD Integration (v2.4.5+)

The project includes a GitHub Actions workflow for automated testing and deployment:

### Automated Builds
- Triggered on every push to `main` or `develop` branches
- Builds Windows executables automatically
- Runs tests across multiple Python versions

### Release Process
1. Create a version tag (e.g., `v2.4.5`)
2. Push the tag to trigger the release workflow
3. GitHub Actions will:
   - Run all tests
   - Build the Windows executable
   - Create a GitHub release
   - Upload the built artifacts

### Local Development Workflow

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Check code coverage
pytest --cov=msr605 tests/

# Build the application
python -m PyInstaller --onefile --name MSR605 main.py
```

### Monitoring Builds
- View build status at: [GitHub Actions](https://github.com/Nsfr750/MSR605/actions)
- Check code coverage at: [Codecov](https://codecov.io/gh/Nsfr750/MSR605)
- Download releases from: [GitHub Releases](https://github.com/Nsfr750/MSR605/releases)

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
