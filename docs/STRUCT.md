# MSR605 Project Structure

## 📁 Root Directory

- [main.py](cci:7://file:///x:/GitHub/MSR605/main.py:0:0-0:0) - Main application entry point
- [README.md](cci:7://file:///x:/GitHub/MSR605/README.md:0:0-0:0) - Project overview and documentation
- [CHANGELOG.md](cci:7://file:///x:/GitHub/MSR605/CHANGELOG.md:0:0-0:0) - Version history and changes
- [LICENSE](cci:7://file:///x:/GitHub/MSR605/LICENSE:0:0-0:0) - GPLv3 License
- [pyproject.toml](cci:7://file:///x:/GitHub/MSR605/pyproject.toml:0:0-0:0) - Python project configuration
- [requirements.txt](cci:7://file:///x:/GitHub/MSR605/requirements.txt:0:0-0:0) - Python dependencies
- [setup.py](cci:7://file:///x:/GitHub/MSR605/setup.py:0:0-0:0) - Installation script

## 📁 Directories

### 📁 assets/

- Icons, images, and other static resources
- `gallery/` - Screenshots and demo images

### 📁 config/

- Application configuration files
- Settings and preferences

### 📁 data/

- Application data storage
- Database files and user data

### 📁 docs/

- Project documentation
- [API_REFERENCE.md](cci:7://file:///x:/GitHub/MSR605/docs/API_REFERENCE.md:0:0-0:0) - API documentation
- [CHANGELOG.md](cci:7://file:///x:/GitHub/MSR605/CHANGELOG.md:0:0-0:0) - Version history
- [CI_CD.md](cci:7://file:///x:/GitHub/MSR605/docs/CI_CD.md:0:0-0:0) - CI/CD pipeline documentation
- [CONTRIBUTING.md](cci:7://file:///x:/GitHub/MSR605/docs/CONTRIBUTING.md:0:0-0:0) - Contribution guidelines
- [FAQ.md](cci:7://file:///x:/GitHub/MSR605/docs/FAQ.md:0:0-0:0) - Frequently Asked Questions
- [INSTALLATION.md](cci:7://file:///x:/GitHub/MSR605/docs/INSTALLATION.md:0:0-0:0) - Installation instructions
- [ROADMAP.md](cci:7://file:///x:/GitHub/MSR605/docs/ROADMAP.md:0:0-0:0) - Development roadmap
- [SECURITY.md](cci:7://file:///x:/GitHub/MSR605/docs/SECURITY.md:0:0-0:0) - Security policies
- `STRUCT.md` - This file
- `TROUBLESHOOTING.md` - Troubleshooting guide
- [user_guide.md](cci:7://file:///x:/GitHub/MSR605/docs/user_guide.md:0:0-0:0) - User manual
- `PDF/` - Generated PDF documentation

### 📁 script/

- Core application code
- [UI.py](cci:7://file:///x:/GitHub/MSR605/script/UI.py:0:0-0:0) - Main user interface
- [cardReader.py](cci:7://file:///x:/GitHub/MSR605/script/cardReader.py:0:0-0:0) - Card reading/writing logic
- [logger.py](cci:7://file:///x:/GitHub/MSR605/script/logger.py:0:0-0:0) - Logging functionality
- [language_manager.py](cci:7://file:///x:/GitHub/MSR605/script/language_manager.py:0:0-0:0) - Internationalization
- [updates.py](cci:7://file:///x:/GitHub/MSR605/script/updates.py:0:0-0:0) - Auto-update functionality
- [settings_manager.py](cci:7://file:///x:/GitHub/MSR605/script/settings_manager.py:0:0-0:0) - Application settings
- [help.py](cci:7://file:///x:/GitHub/MSR605/script/help.py:0:0-0:0) - Help system
- [api/](cci:7://file:///x:/GitHub/MSR605/script/api:0:0-0:0) - API implementation
- (various other modules for different functionalities)

### 📁 tests/

- Unit and integration tests
- Test data and fixtures

## 🛠️ Build and Development

- [build_debug.py](cci:7://file:///x:/GitHub/MSR605/build_debug.py:0:0-0:0) - Debug build script
- [build_linux.py](cci:7://file:///x:/GitHub/MSR605/build_linux.py:0:0-0:0) - Linux build script
- [build_nuitka.py](cci:7://file:///x:/GitHub/MSR605/build_nuitka.py:0:0-0:0) - Nuitka compilation script
- [clean_pycache.py](cci:7://file:///x:/GitHub/MSR605/clean_pycache.py:0:0-0:0) - Cache cleaning utility
- [clear_cache.py](cci:7://file:///x:/GitHub/MSR605/clear_cache.py:0:0-0:0) - Cache clearing script
- [installer.nsi](cci:7://file:///x:/GitHub/MSR605/installer.nsi:0:0-0:0) - NSIS installer script
- [pypi.py](cci:7://file:///x:/GitHub/MSR605/pypi.py:0:0-0:0) - PyPI packaging script

## 🔄 Version Control

- [.git/](cci:7://file:///x:/GitHub/MSR605/.git:0:0-0:0) - Git repository
- [.github/](cci:7://file:///x:/GitHub/MSR605/.github:0:0-0:0) - GitHub configurations
  - `workflows/` - GitHub Actions workflows
- [.gitignore](cci:7://file:///x:/GitHub/MSR605/.gitignore:0:0-0:0) - Git ignore rules

## 🐍 Virtual Environment

- [venv312/](cci:7://file:///x:/GitHub/MSR605/venv312:0:0-0:0) - Python virtual environment (Python 3.12)

## 📊 Project Information

- **Language**: Python 3.8+
- **Dependencies**: See [requirements.txt](cci:7://file:///x:/GitHub/MSR605/requirements.txt:0:0-0:0)
- **License**: GPLv3
- **Maintainer**: Nsfr750
- **Repository**: [GitHub](https://github.com/Nsfr750/MSR605)

## 🏗️ Build System

- Uses PyInstaller for standalone executables
- Nuitka for compilation to C
- NSIS for Windows installer creation
- GitHub Actions for CI/CD

## 📦 Distribution

- Windows: `.exe` installer
- Linux: Package and AppImage
- Source: Python package on PyPI

## 🔒 Security

- Secure coding practices
- Dependency scanning
- Automated security testing

## 🌐 Internationalization

- Multi-language support
- Easy translation system
- Built-in language packs

## 📈 Monitoring

- Application logging
- Error tracking
- Performance monitoring
