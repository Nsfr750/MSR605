# CI/CD Pipeline Documentation (v2.4.5+)

## Table of Contents

- [Overview](#overview)
- [Workflow Configuration](#workflow-configuration)
- [Build Process](#build-process)
- [Testing Strategy](#testing-strategy)
- [Release Process](#release-process)
- [Monitoring and Notifications](#monitoring-and-notifications)
- [Local Development](#local-development)
- [Troubleshooting](#troubleshooting)
- [Security Considerations](#security-considerations)

## Overview

The MSR605 project uses GitHub Actions for continuous integration and deployment. The CI/CD pipeline automates testing, building, and releasing the application, ensuring code quality and reliability.

## Workflow Configuration

The main workflow file is located at `.github/workflows/ci-cd.yml` and includes three primary jobs:

1. **Test Job**: Runs on every push and pull request
2. **Build Job**: Creates distributable artifacts
3. **Release Job**: Handles versioned releases

### Trigger Conditions

- **Test Job**: Runs on all pushes and pull requests to `main` and `develop` branches
- **Build Job**: Runs after successful test completion on `main` and `develop` branches
- **Release Job**: Triggers when a new version tag is pushed (e.g., `v2.4.5`)

## Build Process

### Windows Build

- Uses PyInstaller to create a standalone executable
- Includes all required dependencies
- Embeds version information and icons
- Generates a single executable file for easy distribution

### Build Artifacts

- Windows executable (`MSR605.exe`)
- Debug symbols (if applicable)
- Installation logs

## Testing Strategy

### Unit Tests

- Located in `tests/unit/`
- Test individual components in isolation
- Fast execution (runs on every commit)

### Integration Tests

- Located in `tests/integration/`
- Test component interactions
- Includes hardware simulation tests

### Code Coverage

- Minimum coverage requirement: 80%
- Reports generated using `pytest-cov`
- Results uploaded to Codecov

### Linting and Code Quality

- Black code formatting
- isort import sorting
- flake8 linting
- mypy type checking

## Release Process

### Versioning

- Follows [Semantic Versioning](https://semver.org/)
- Version numbers updated in `script/version.py`
- Changelog maintained in `CHANGELOG.md`

### Creating a Release

1. Update the version in `script/version.py`
2. Update `CHANGELOG.md` with release notes
3. Create and push a version tag:

   ```bash
   git tag -a v2.4.5 -m "Version 2.4.5"
   git push origin v2.4.5
   ```

4. The CI/CD pipeline will automatically:
   - Run all tests
   - Build the Windows executable
   - Create a GitHub release
   - Upload the built artifacts

## Monitoring and Notifications

### Build Status

- [GitHub Actions Dashboard](https://github.com/Nsfr750/MSR605/actions)
- Email notifications for failed builds

### Coverage

- [Codecov Report](https://codecov.io/gh/Nsfr750/MSR605)
- Coverage trends and history

### Dependencies

- Dependabot for dependency updates
- Security vulnerability scanning

## Local Development

### Running Tests Locally

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run tests with coverage
pytest --cov=msr605 --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_module.py
```

### Building Locally

```bash
# Install build dependencies
pip install pyinstaller

# Build the application
python -m PyInstaller --onefile --name MSR605 --icon=assets/icon.ico main.py

# The executable will be in the dist/ directory
```

## Troubleshooting

### Common Issues

#### Build Failures

- Ensure all dependencies are installed
- Check Python version compatibility
- Verify file paths and configurations

#### Test Failures

- Run tests with `-v` for verbose output
- Check for environment-specific issues
- Ensure test data is available

#### Dependency Issues

- Clear pip cache: `pip cache purge`
- Reinstall dependencies: `pip install -r requirements.txt`

## Security Considerations

### Secrets Management

- Use GitHub Secrets for sensitive information
- Never commit API keys or credentials

### Dependency Security

- Regular dependency updates
- Security vulnerability scanning
- Pinned dependency versions

### Build Security

- Isolated build environments
- Artifact signing (future)
- Checksum verification

## Contact

For CI/CD related issues, please open an issue on [GitHub](https://github.com/Nsfr750/MSR605/issues) or contact the maintainers.
