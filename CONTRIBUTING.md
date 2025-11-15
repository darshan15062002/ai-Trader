# Contributing to AITrader

First off, thank you for considering contributing to AITrader! 🎉 It's people like you that make AITrader such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our commitment to providing a welcoming and inclusive environment. Please be respectful and constructive.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (code snippets, screenshots)
- **Describe the behavior you observed** and what you expected
- **Include your environment details** (Python version, OS, etc.)

**Bug Report Template:**
```markdown
## Bug Description
A clear description of the bug.

## Steps to Reproduce
1. Run command '...'
2. Click on '....'
3. See error

## Expected Behavior
What you expected to happen.

## Actual Behavior
What actually happened.

## Environment
- Python version:
- OS:
- Branch/Commit:

## Additional Context
Any other relevant information.
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful**
- **List any examples** of similar features in other projects

### Pull Requests

1. **Fork the repository** and create your branch from `main`
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Make your changes**
   - Write clear, commented code
   - Follow the existing code style
   - Add tests if applicable
   - Update documentation as needed

3. **Test your changes**
   - Run existing tests
   - Add new tests for your feature
   - Ensure all tests pass

4. **Commit your changes**
   - Use clear and meaningful commit messages
   - Reference issues if applicable
   ```bash
   git commit -m "Add amazing feature to improve X"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request**
   - Provide a clear description of the changes
   - Link related issues
   - Include screenshots/examples if relevant

## Development Setup

### Prerequisites
- Python 3.8+
- Git
- Virtual environment (recommended)

### Setup Instructions

1. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-Trader.git
   cd ai-Trader
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Gemini API key**
   - Get API key from [Google AI Studio](https://ai.google.dev/)
   - Update `agent/gemini_agent.py` with your key

5. **Run tests**
   ```bash
   python test.py
   ```

## Coding Standards

### Python Style Guide
- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise

### Code Example
```python
def calculate_rsi(prices: list, period: int = 14) -> float:
    """
    Calculate Relative Strength Index (RSI).
    
    Args:
        prices (list): List of closing prices
        period (int): RSI period (default: 14)
    
    Returns:
        float: RSI value between 0 and 100
    """
    # Implementation here
    pass
```

### Commit Message Guidelines

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and PRs when relevant

**Good commit messages:**
```
Add MACD indicator calculation
Fix portfolio value calculation bug (#123)
Update README with installation instructions
Refactor trade execution logic
```

## Project Structure

```
ai-Trader/
├── agent/              # AI trading agents
├── api/                # API endpoints
├── data/               # Market data
├── ReportEngine/       # Report generation
├── main.py             # Main entry point
├── strategy.py         # Trading strategies
├── indicators.py       # Technical indicators
└── tests/              # Test files (to be added)
```

## Areas for Contribution

### High Priority
- [ ] Add comprehensive unit tests
- [ ] Improve error handling
- [ ] Add more technical indicators
- [ ] Implement stop-loss mechanisms
- [ ] Add backtesting visualizations

### Medium Priority
- [ ] Create web dashboard improvements
- [ ] Add more trading strategies
- [ ] Improve documentation
- [ ] Add integration tests
- [ ] Performance optimizations

### Good First Issues
- [ ] Add docstrings to functions
- [ ] Improve code comments
- [ ] Fix typos in documentation
- [ ] Add example configurations
- [ ] Create tutorial notebooks

## Testing Guidelines

### Writing Tests
- Place tests in `tests/` directory
- Name test files `test_*.py`
- Use descriptive test names
- Test both success and failure cases

### Example Test
```python
import unittest
from indicators import calculate_sma

class TestIndicators(unittest.TestCase):
    def test_sma_calculation(self):
        prices = [10, 20, 30, 40, 50]
        result = calculate_sma(prices, period=3)
        self.assertEqual(result, 40.0)
```

## Documentation

- Update README.md for user-facing changes
- Add docstrings for all public functions
- Include code examples where appropriate
- Update API documentation for endpoint changes

## Questions?

Feel free to:
- Open an issue with the `question` label
- Reach out via GitHub discussions
- Contact the maintainer: darshanjain15062002@gmail.com

## Recognition

Contributors will be recognized in:
- README.md Contributors section
- Release notes
- Project documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to AITrader! 🚀
