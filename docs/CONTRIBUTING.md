# Contributing to MSR605 Card Reader/Writer

Thank you for your interest in contributing to the MSR605 Card Reader/Writer project! We welcome all contributions, whether they're bug reports, feature requests, documentation improvements, or code contributions.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Feature Requests](#feature-requests)
  - [Code Contributions](#code-contributions)
- [Development Setup](#development-setup)
  - [Prerequisites](#prerequisites)
  - [Environment Setup](#environment-setup)
- [Development Guidelines](#development-guidelines)
  - [Code Style](#code-style)
  - [Testing](#testing)
  - [Documentation](#documentation)
  - [Version Control](#version-control)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)
- [Getting Help](#getting-help)
- [License](#license)

## 👥 Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before making any contributions.

## 🚀 How to Contribute (v2.4.5+)

### CI/CD Integration

The project now uses GitHub Actions for continuous integration and deployment. When you create a pull request, the following checks will run automatically:

- **Test Suite**: Runs unit and integration tests across Python 3.8, 3.9, and 3.10
- **Code Style**: Enforces code formatting with Black and isort
- **Type Checking**: Verifies type hints with mypy
- **Documentation**: Builds documentation to catch any errors
- **Security**: Scans for vulnerabilities with Bandit and safety

### Development Workflow

1. **Create a feature branch** from the latest `develop` branch
2. **Make your changes** following the coding standards
3. **Run tests locally** before pushing:

   ```bash
   # Run all tests
   pytest
   
   # Run tests with coverage
   pytest --cov=msr605 tests/
   
   # Check code style
   black .
   isort .
   flake8
   ```

4. **Commit your changes** with a descriptive message
5. **Push to your fork** and create a pull request
6. **Monitor the CI/CD pipeline** and address any failures

### Branching Strategy

- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: New features
- `bugfix/*`: Bug fixes
- `release/*`: Release preparation

### 🐛 Reporting Bugs

1. **Check Existing Issues**: Before creating a new issue, please search the [issues](https://github.com/Nsfr750/MSR605/issues) to see if a similar issue already exists.
2. **Create a New Issue**: If you've found a bug, please create a new issue with the following details:
   - A clear and descriptive title (e.g., "Error when reading card with special characters")
   - Steps to reproduce the issue
   - Expected vs. actual behavior
   - Screenshots or error messages if applicable
   - Your system information (OS, Python version, hardware details)
   - Any relevant logs from the `logs/` directory
   - MSR605 firmware version (if known)

### 💡 Feature Requests

1. **Check Existing Features**: Before requesting a new feature, check the [ROADMAP.md](../ROADMAP.md) and existing issues to see if it's already planned.
2. **Create a Feature Request**: If you have an idea for a new feature, please create a new issue with the following details:
   - A clear and descriptive title (e.g., "Add support for batch processing")
   - A detailed description of the feature and its benefits
   - Use cases and examples
   - Any potential security implications
   - Screenshots or mockups if applicable
   - References to any relevant standards (e.g., ISO 7811, ISO 7813)

## 💻 Development Setup

### Prerequisites

- **Python**: 3.8, 3.9, 3.10, or 3.12 (3.10+ recommended)
- **Rust Toolchain**: Required for cryptography package
- **Git**: Version control
- **MSR605 Hardware**: For hardware testing (recommended but not required for all contributions)
- **Operating System**: 
  - Windows 10/11 (fully supported)
  - Linux (Ubuntu/Debian recommended)
  - macOS (limited testing)
- **Disk Space**: Minimum 200MB free
- **Memory**: 4GB RAM minimum

### Environment Setup

1. **Fork and Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/MSR605.git
   cd MSR605
   ```

2. **Set Up Development Environment**:

   ```bash
   # Create and activate virtual environment
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   
   # Install development dependencies
   pip install -r requirements-dev.txt
   
   # Install pre-commit hooks
   pre-commit install
   
   # Verify setup
   pytest --version
   black --version
   mypy --version
   ```

3. **Run the Development Server**:

   ```bash
   # Start the application in development mode
   python main.py --dev
   
   # Or run specific test cases
   python -m pytest tests/test_specific_feature.py -v
   
   # For hardware testing
   python -m pytest tests/hardware/ --hardware
   ```

4. **Set Up Pre-commit Hooks**:

   ```bash
   pre-commit install
   ```

## 🛠 Development Guidelines

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code
- Use [Google Style Docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
- Maximum line length: 88 characters (Black's default)
- Use type hints for all functions and methods
- Sort imports using `isort` (configured in `pyproject.toml`)
- Format code using `black` (configured in `pyproject.toml`)
- Keep functions small and focused (preferably < 50 lines)

### Testing

- Write unit tests for all new features and bug fixes
- Use `pytest` for testing
- Aim for at least 80% test coverage
- Place tests in the `tests/` directory
- Test on multiple Python versions (3.10+)
- Run tests locally before pushing:

  ```bash
  # Run all tests
  pytest
  
  # Run tests with coverage
  pytest --cov=script --cov-report=term-missing
  
  # Run a specific test file
  pytest tests/test_card_reader.py -v
  ```

### Documentation

- Update relevant documentation when adding new features
- Follow the existing documentation style
- Add docstrings to all public functions and classes
- Document all public API endpoints
- Update the CHANGELOG.md with significant changes
- Keep the README.md up to date with setup and usage instructions

### Version Control

1. **Create a Feature Branch**:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**:
   - Follow the code style guidelines
   - Add tests for new features
   - Update documentation as needed

3. **Run Checks Before Committing**:

   ```bash
   # Run linters
   black .
   isort .
   flake8
   
   # Run type checking
   mypy script/
   
   # Run tests
   pytest
   ```

4. **Commit Your Changes**:

   ```bash
   git add .
   git commit -m "feat: add your feature"
   ```
   
   Use [conventional commit messages](https://www.conventionalcommits.org/):
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `style:` for formatting changes
   - `refactor:` for code changes that don't fix bugs or add features
   - `test:` for adding or modifying tests
   - `chore:` for maintenance tasks
   - `build:` for build system changes
   - `ci:` for CI configuration changes
   - `perf:` for performance improvements
   - `revert:` for reverting commits

5. **Push Your Changes**:

   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**:
   - Go to the [original repository](https://github.com/Nsfr750/MSR605)
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template
   - Request review from maintainers

## 🛠 Development Guidelines

### 🎨 Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code
- Use [Google Style Docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) for documentation
- Keep lines under 88 characters (Black's default)
- Use type hints for all function signatures and important variables
- Sort imports using `isort` (configured in `pyproject.toml`)
- Format code using `black` (configured in `pyproject.toml`)

### 🧪 Testing

- Write unit tests for all new features and bug fixes
- Use `pytest` for testing
- Aim for at least 80% test coverage
- Place tests in the `tests/` directory
- Test on multiple Python versions (3.10+)
- Run tests before pushing:
  ```bash
  pytest --cov=msr605 --cov-report=term-missing
  ```

### 📚 Documentation

- Update relevant documentation when adding new features or changing behavior
- Follow the existing documentation style
- Add docstrings to all public functions and classes
- Use type hints in docstrings
- Document all public API endpoints
- Update the CHANGELOG.md with significant changes

## 🔄 Pull Request Process

1. **Initial Review**:
   - Ensure your code follows the project's style guidelines
   - Make sure all tests pass
   - Update documentation as needed

2. **Code Review**:
   - Request review from at least one maintainer
   - Address all review comments
   - Update your PR with requested changes

3. **Merge Approval**:
   - At least one maintainer must approve the PR
   - All CI checks must pass
   - Resolve any merge conflicts

4. **Merging**:
   - Use "Squash and merge" for feature branches
   - Use "Rebase and merge" for hotfixes
   - Delete the feature branch after merging

## ❓ Getting Help

If you have any questions or need help:

1. **Check the Documentation**:
   - [User Guide](docs/user_guide.md)
   - [API Reference](docs/api.md)
   - [FAQ](docs/faq.md)

2. **Search Existing Issues**:
   - [Open Issues](https://github.com/Nsfr750/MSR605/issues)
   - [Closed Issues](https://github.com/Nsfr750/MSR605/issues?q=is%3Aissue+is%3Aclosed)

3. **Ask for Help**:
   - Open a [new discussion](https://github.com/Nsfr750/MSR605/discussions)
   - Email: nsfr750@yandex.com

## 🔄 Release Process

1. **Version Bumping**:
   - Update the version in `script/version.py`
   - Update `CHANGELOG.md` with the new version and changes
   - Create a git tag for the release:
   
     ```bash
     git tag -a vX.Y.Z -m "Version X.Y.Z"
     git push origin vX.Y.Z
     ```

2. **Create Release**:
   - Draft a new release on GitHub
   - Attach the built binaries
   - Publish release notes

3. **Update Documentation**:
   - Ensure all new features are documented
   - Update the user guide if needed
   - Verify all links and examples

## 📄 License

By contributing to MSR605 Card Reader/Writer, you agree that your contributions will be licensed under the [GNU General Public License v3.0](../LICENSE).

## 🙏 Acknowledgments

- Thanks to all contributors who have helped improve this project
- Special thanks to our sponsors and backers
- This project follows the [all-contributors](https://allcontributors.org/) specification
