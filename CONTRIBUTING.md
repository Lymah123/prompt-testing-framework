# Contributing to Prompt Testing Framework

Thank you for your interest in contributing! 🎉

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/prompt-testing-framework.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test thoroughly
6. Commit: `git commit -m "Add: your feature description"`
7. Push: `git push origin feature/your-feature-name`
8. Open a Pull Request

## Development Setup
```bash
# Install in development mode
pip install -e .

# Install dev dependencies
pip install pytest black flake8 mypy
```

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small

## Running Tests
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## Pull Request Guidelines

- Describe what your PR does
- Link related issues
- Add tests for new features
- Update documentation
- Ensure all tests pass

## Feature Ideas

Check our [Roadmap](README.md#roadmap) for ideas or propose your own!

## Questions?

Open an issue with the `question` label.