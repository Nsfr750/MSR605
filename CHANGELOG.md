# Changelog

All notable changes to the MSR605 Card Reader/Writer project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Support for Python 3.12
- Enhanced error handling for hardware communication
- New configuration options in `config.ini`
- Additional test cases for better code coverage

### Changed
- Updated dependencies to their latest versions
- Improved documentation and code comments
- Optimized database operations

### Fixed
- Minor UI layout issues
- Fixed potential memory leaks in card reading operations
- Resolved issues with special character handling

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
