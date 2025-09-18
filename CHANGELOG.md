# Changelog

All notable changes to the MSR605 Card Reader/Writer project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.4.1] - 2025-08-31

### Fixed

- Fixed menu item duplication when changing languages

## [2.4.0] - 2025-07-20

### Added

- **Advanced Card Data Visualization**: New visualization features for analyzing card data
  - Character distribution charts showing frequency of each character in track data
  - Bit pattern visualization displaying binary representation of track data
  - Data density metrics including length, unique characters, and character density
  - Field analysis with automatic detection of field separators and visualization of field lengths
  - Interactive visualizations with tooltips and zooming
  - Integration with the main UI in the Advanced Functions tab

## [2.3.2] - 2025-07-20

### Added

- **Multiple Card Format Support**: Added support for both ISO 7811 and ISO 7813 standards
  - ISO 7811: General purpose magnetic stripe cards
  - ISO 7813: Financial transaction cards with enhanced validation
  - Automatic format detection based on track data
  - Format-specific validation and parsing
  - Detailed error reporting for invalid card data

## [2.3.1] - 2025-07-20

### Added

- Comprehensive project documentation including user guide, API reference, and FAQ
- Enhanced CODEOWNERS file with detailed ownership rules
- Updated dependency specifications with version bounds for better reproducibility
- Added PyPI classifiers for better package discovery
- Included development environment setup instructions in PREREQUISITES.md

### Changed

- Updated all dependencies to their latest stable versions
- Improved requirements.txt organization with clear section comments
- Enhanced error messages for better debugging
- Optimized build process for better cross-platform compatibility
- Updated development tooling configurations

### Fixed

- Resolved cryptography Rust binary inclusion in PyInstaller builds
- Fixed path resolution issues in build scripts
- Corrected menu translations and UI text
- Addressed various linting and type checking issues
- Fixed documentation build process

## [2.3.0] - 2025-07-19

### Added

- Daily log file rotation with automatic cleanup
- Application icon support
- Improved menu organization and translations
- New update checking system with GitHub integration
- Dark mode support throughout the application
- Sponsor information in Help menu

### Changed

- Replaced Pillow with Wand for image processing
- Updated menu structure for better usability
- Improved error handling and logging
- Enhanced translation support for all UI elements
- Optimized application startup time
- Updated dependencies to latest stable versions

### Fixed

- Fixed menu translation issues
- Resolved initialization order in menu system
- Fixed update checker timestamp parsing
- Improved cross-platform compatibility
- Fixed various UI layout issues

## [2.2.0] - 2025-06-15

### Added

- Support for Python 3.12 and 3.13
- Enhanced error handling for hardware communication
- Additional test cases for better code coverage
- Comprehensive documentation in CONTRIBUTING.md and PREREQUISITES.md
- GitHub CODEOWNERS file for better code review workflow
- Pre-commit hooks for code quality
- Sphinx documentation with ReadTheDocs theme

### Changed

- Updated all dependencies to their latest stable versions
- Improved documentation and code comments
- Optimized database operations
- Restructured project documentation
- Enhanced development tooling with pre-commit hooks
- Improved test coverage reporting

### Fixed
- Minor UI layout issues
- Fixed potential memory leaks in card reading operations
- Resolved issues with special character handling
- Fixed compatibility issues with latest PyQt6 and Qt6.6
- Addressed security vulnerabilities in dependencies

## [2.1.0] - 2025-05-22

### Added
- New Advanced Functions window with dedicated tabs for decoding and decryption
- Support for multiple encryption algorithms (DES, 3DES, AES)
- Enhanced track data parsing with detailed field extraction
- Improved error handling and user feedback
- Better organization of decryption and decoding functionality

### Changed
- Moved decode/decrypt functionality to a dedicated module
- Updated UI for better usability and organization
- Improved error messages and logging
- More robust card data parsing

### Fixed
- Fixed issues with card reading error handling
- Improved stability during track data processing
- Better handling of invalid card data formats

## [2.0.2] - 2025-05-22

### Added
- Enhanced error handling for card reading operations
- Improved connection management with better status feedback
- Added support for individual track reading when full card read fails
- More detailed error messages for troubleshooting

### Changed
- Updated UI to show more detailed connection status
- Improved card reading reliability with retry mechanisms
- Optimized database operations for better performance
- Enhanced error recovery during card operations

### Fixed
- Fixed issue with connection status not updating properly
- Resolved problems with track data parsing
- Fixed potential memory leaks in card reading operations
- Addressed UI responsiveness issues during long operations

## [2.0.1] - 2025-05-15

### Added
- Comprehensive README with detailed project information
- Modular code structure with separate modules for sponsor, about, and version
- Enhanced error handling in database management
- Improved GUI layout with better button organization

### Changed
- Refactored card data decoding logic
- Optimized database storage and retrieval
- Updated project documentation

### Fixed
- Minor UI responsiveness issues
- Potential memory leaks in track data processing

## [2.0.0] - 2025-02-28

### Added
- Advanced track-level controls
  - Set/Clear/Check Leading Zero
  - Configurable Bits Per Inch (BPI)
  - Configurable Bits Per Character (BPC)
- Detailed card data decoding for all three tracks
- Comprehensive database management system
- Export functionality for card data (CSV)

### Changed
- Complete UI redesign
- Improved hardware communication protocol
- Enhanced error reporting mechanism

### Removed
- Legacy track parsing methods
- Outdated hardware communication routines

## [1.5.0] - 2024-11-15

### Added
- Initial database storage functionality
- Basic track data parsing
- Hardware connection diagnostics
- Coercivity selection (HI-CO/LOW-CO)

### Changed
- Improved serial communication reliability
- Enhanced error handling

## [1.0.0] - 2024-07-01

### Added
- Initial release of MSR605 Card Reader/Writer
- Basic card reading and writing capabilities
- Simple GUI interface
- Support for MSR605 hardware

## Version Roadmap

### Planned Features
- [ ] Multi-language support
- [ ] Advanced card data validation
- [ ] Cloud synchronization for card databases
- [ ] Machine learning-based card data analysis
- [ ] Support for additional magnetic card readers

## Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to propose features, report bugs, and submit pull requests.

## License

This project is licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE) for more details.
