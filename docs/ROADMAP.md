# Project Roadmap

This document outlines the development roadmap for the MSR605 Card Reader/Writer project. It provides a high-level overview of the planned features, improvements, and milestones.

## 🚀 Upcoming Features (Planned)

### v2.5.0 - PIN Block Decoding & Serial Reliability (Nov 2026) ✅ Released
- [x] **PIN Block Decoding**
  - [x] ISO 9564 formats 0/1/3, VISA-1/3/4, ECI-4 support
  - [x] DES/3DES key support with automatic PAN extraction
  - [x] PIN block extraction from Track 2 discretionary data
- [x] **Serial Communication Reliability**
  - [x] Dedicated swipe timeout for card operations
  - [x] Input buffer flushing before commands
  - [x] Configurable serial timeout in Connection Settings
- [ ] **Security Enhancements** (moved to v3.0.0)
  - [ ] Implement hardware security module (HSM) integration
  - [ ] Add support for FIDO2 authentication
  - [ ] Enhanced encryption key management
- [ ] **User Experience** (moved to v3.0.0)
  - [ ] Redesigned settings interface
  - [ ] Customizable keyboard shortcuts
  - [ ] Improved dark/light theme support

### v3.0.0 - Next Generation (Q1 2027)
- [ ] **Architecture**
  - [ ] Plugin system for extending functionality
  - [ ] Microservices architecture
  - [ ] Cloud synchronization
- [ ] **New Features**
  - [ ] Mobile companion app
  - [ ] Advanced analytics dashboard
  - [ ] AI-powered data validation

## 📅 Release Schedule

| Version | Target Date       | Status      | Key Features |
|---------|-------------------|-------------|--------------|
| v2.0.1  | April 2025        | ✅ Released | Initial release with basic functionality |
| v2.1.0  | June 2025         | ✅ Released | UI improvements and bug fixes |
| v2.3.0  | July 2025         | ✅ Released | Advanced card data visualization |
| v2.4.0  | July 2025         | ✅ Released | Multiple card format support |
| v2.4.1  | August 2025       | ✅ Released | Bug fixes and performance improvements |
| v2.4.2  | Sept. 2025        | ✅ Released | Build system improvements |
| v2.4.5  | Nov. 2025         | ✅ Released | CI/CD pipeline implementation |
| v2.5.0  | Nov. 2026         | ✅ Released | PIN block decoding, serial reliability |
| v3.0.0  | Q1 2027           | ⏳ Planned  | Next Generation Release |

## 🏗️ In Development (v3.0.0)

### Current Focus
- Security enhancements
- Performance optimization
- User experience improvements

### Next Steps
1. Complete security audit
2. Performance benchmarking
3. UI/UX refinement

## 🤝 How to Contribute

We welcome contributions from the community! If you're interested in helping with any of these features:

1. Check out our [Contributing Guidelines](CONTRIBUTING.md)
2. Look for issues labeled "help wanted" or "good first issue"
3. Fork the repository and submit a pull request

## 📝 Notes

- This roadmap is subject to change based on community feedback and priorities
- Feature priorities may be adjusted to address critical bug fixes or security issues
- Suggestions and feature requests are welcome through GitHub Issues
