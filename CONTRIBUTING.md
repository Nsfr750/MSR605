# Contributing to MSR605

Thank you for your interest in contributing to the MSR605 project! We welcome all contributions, whether they're bug reports, feature requests, documentation improvements, or code contributions.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Feature Requests](#feature-requests)
  - [Code Contributions](#code-contributions)
- [Development Guidelines](#development-guidelines)
  - [Code Style](#code-style)
  - [Testing](#testing)
  - [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Getting Help](#getting-help)
- [License](#license)

## 👥 Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before making any contributions.

## 🚀 How to Contribute

### 🐛 Reporting Bugs

1. **Check Existing Issues**: Before creating a new issue, please search the [issues](https://github.com/Nsfr750/MSR605/issues) to see if a similar issue already exists.
2. **Create a New Issue**: If you've found a bug, please create a new issue with the following details:
   - A clear and descriptive title (e.g., "Error when reading card with special characters")
   - Steps to reproduce the issue
   - Expected vs. actual behavior
   - Screenshots or error messages if applicable
   - Your system information (OS, Python version, hardware details)
   - Any relevant logs (check the `logs/` directory)

### 💡 Feature Requests

1. **Check Existing Features**: Before requesting a new feature, check the [ROADMAP.md](ROADMAP.md) and existing issues to see if it's already planned.
2. **Create a Feature Request**: If you have an idea for a new feature, please create a new issue with the following details:
   - A clear and descriptive title (e.g., "Add support for batch processing")
   - A detailed description of the feature
   - Use cases and examples
   - Any potential drawbacks or considerations
   - Screenshots or mockups if applicable

### 💻 Code Contributions

1. **Set Up Development Environment**:
   ```bash
   # Fork and clone the repository
   git clone https://github.com/your-username/MSR605.git
   cd MSR605
   
   # Set up virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   
   # Install development dependencies
   pip install -e ".[dev]"
   pre-commit install
   ```

2. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**:
   - Follow the code style guidelines below
   - Add tests for new features
   - Update documentation as needed

4. **Run Tests and Linters**:
   ```bash
   # Run tests
   pytest
   
   # Run type checking
   mypy msr605/
   
   # Run linters
   black .
   flake8
   ```

5. **Commit Your Changes**:
   ```bash
   git add .
   git commit -m "feat: add your feature"
   ```
   
   Use [conventional commit messages](https://www.conventionalcommits.org/):
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `style:` for formatting changes
   - `refactor:` for code changes that neither fix bugs nor add features
   - `test:` for adding or modifying tests
   - `chore:` for maintenance tasks

6. **Push Your Changes**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**:
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
   - Join our [Discord server](https://discord.gg/BvvkUEP9)
   - Email: nsfr750@yandex.com

## 📄 License

By contributing to MSR605, you agree that your contributions will be licensed under the [GNU General Public License v3.0](LICENSE).
By contributing, you agree that your contributions will be licensed under the [GPLv3 License](LICENSE)
