# Prerequisites

Before you can use this project, make sure you have the following installed on your system:

## System Requirements

- Python 3.8 or higher
- pip (Python package installer)
- Git

## Python Dependencies

Install the required Python packages by running:

```bash
pip install -r requirements.txt
```

## Hardware Requirements (if applicable)

- MSR605 Magnetic Stripe Card Reader/Encoder
- USB port for device connection
- Prolific USB to Serial Driver (can be find on releases page)

## Environment Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Nsfr750/MSR605.git
   cd MSR605
   ```

2. (Optional) Create and activate a virtual environment:

   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On Unix or MacOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install development dependencies:

   ```bash
   pip install -r requirements-dev.txt
   ```

## Configuration

1. Copy the example configuration file and update it with your settings:

   ```bash
   cp config.example.ini config.ini
   ```

2. Edit the `config.ini` file with your preferred settings.

## Testing the Setup

Run the test suite to verify everything is working correctly:

```bash
pytest tests/
```

## Troubleshooting

- If you encounter permission issues, try running the command with `sudo` (Unix/Linux/MacOS) or as Administrator (Windows)
- Make sure all required USB drivers are installed for your MSR605 device
- Check the [Troubleshooting](Docs/TROUBLESHOOTING.md) guide for common issues and solutions
