# 🧪 Prompt Testing Framework

A comprehensive testing framework for AI prompts with support for multiple LLM providers (Claude, OpenAI). Built with Python and Streamlit for rapid prompt testing and evaluation.

## Features

- ✅ **Multi-Provider Support** - Test prompts across [Claude](https://claude.com/product/overview), [goose](https://github.com/block/goose) and [OpenAI models](https://platform.openai.com/docs/models).
- 📝 **Test Case Management** - Create, edit, and organize test cases
- 🔍 **Automated Evaluation** - Built-in assertions (contains, regex, length checks, etc.)
- 📊 **Results Tracking** - View historical results and analytics
- 🎯 **Easy UI** - Streamlit-based interface for quick iteration
- 💾 **JSON Storage** - Simple file-based storage (easy to version control)

## Installation

### Prerequisites
- Python 3.8+
- API keys for Claude and/or OpenAI

### Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd prompt-testing-framework
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```
ANTHROPIC_API_KEY=your_claude_api_key
OPENAI_API_KEY=your_openai_api_key
```

## Usage

### Start the application
```bash
streamlit run ui/app.py
```

The app will open in your browser at `http://localhost:8501`

### Creating Test Cases

1. Navigate to **Test Cases** page
2. Fill in the form:
   - **Test Name**: Descriptive name for your test
   - **Provider**: Choose Claude or OpenAI
   - **Model**: Specify model (e.g., `claude-sonnet-4-20250514`)
   - **Prompt**: Your test prompt
   - **System Prompt** (optional): System instructions
   - **Temperature**: Control randomness (0.0 - 2.0)
   - **Max Tokens**: Response length limit
   - **Tags**: Organize tests with tags

3. Add **Expectations** (automated checks):
   - `contains`: Response must contain text
   - `not_contains`: Response must NOT contain text
   - `regex`: Response must match pattern
   - `length_min`: Minimum response length
   - `length_max`: Maximum response length
   - `manual`: Requires manual review

4. Click **Save Test Case**

### Running Tests

1. Navigate to **Run Tests** page
2. Select tests to run (or run all)
3. Click **Run Selected Tests**
4. View results in real-time

### Viewing Results

1. Navigate to **Results** page
2. Filter by status, test name, or model
3. Expand results to see:
   - Full prompt and response
   - Evaluation results
   - Execution time
   - Pass/fail status
4. Export results as JSON

## Project Structure
```
prompt-testing-framework/
├── src/
│   ├── core/
│   │   ├── models.py          # Pydantic data models
│   │   ├── runner.py          # Test execution engine
│   │   └── evaluator.py       # Response evaluation logic
│   ├── api/
│   │   └── providers/
│   │       ├── claude.py      # Claude API integration
│   │       └── openai.py      # OpenAI API integration
│   ├── storage/
│   │   └── manager.py         # JSON-based storage
│   └── utils/
│       └── helpers.py         # Utility functions
├── ui/
│   ├── app.py                 # Main Streamlit app
│   └── pages/
│       ├── 1_test_cases.py   # Test case management
│       ├── 2_run_tests.py    # Test execution
│       └── 3_results.py      # Results viewer
├── data/
│   ├── test_cases.json       # Stored test cases
│   └── results.json          # Test results
├── requirements.txt
├── .env.example
└── README.md
```

## Data Storage

All data is stored in JSON files in the `data/` directory:
- `test_cases.json` - Your test case definitions
- `results.json` - Historical test results

These files are plain JSON and can be:
- Version controlled with git
- Manually edited if needed
- Backed up easily
- Shared with team members

## Evaluation Types

### Contains
Checks if response contains specific text (case-insensitive)
```python
Expectation(type="contains", value="hello world")
```

### Not Contains
Checks if response does NOT contain text
```python
Expectation(type="not_contains", value="error")
```

### Regex
Matches response against regex pattern
```python
Expectation(type="regex", value=r"\d{3}-\d{3}-\d{4}")  # Phone number
```

### Length Min/Max
Validates response length
```python
Expectation(type="length_min", value=100)
Expectation(type="length_max", value=500)
```

### Manual
Requires human review (no automated check)
```python
Expectation(type="manual", value="Check for tone")
```

## Example Test Case
```json
{
  "id": "test-001",
  "name": "Summarization Test",
  "prompt": "Summarize the following in 3 bullet points:\n\nAI is transforming...",
  "provider": "claude",
  "model": "claude-sonnet-4-20250514",
  "temperature": 0.7,
  "max_tokens": 500,
  "expectations": [
    {
      "type": "contains",
      "value": "bullet",
      "description": "Response uses bullet points"
    },
    {
      "type": "length_max",
      "value": 500,
      "description": "Summary is concise"
    }
  ],
  "tags": ["summarization", "formatting"]
}
```

## Tips & Best Practices

1. **Start Simple**: Begin with basic contains/length checks before complex regex
2. **Use Tags**: Organize tests by feature, model, or team
3. **Iterate**: Run tests frequently during prompt development
4. **Version Control**: Commit `data/` folder to track test evolution
5. **Multiple Models**: Compare same prompt across different models
6. **Temperature Testing**: Test same prompt with different temperatures

## Troubleshooting

### API Key Errors
- Verify `.env` file exists and contains valid keys
- Check key format (starts with `sk-ant-` for Anthropic)

### Import Errors
- Ensure you're in the project root when running
- Try: `python -m streamlit run ui/app.py`

### Storage Issues
- Check `data/` directory exists and is writable
- Verify JSON files are valid (use JSON validator)

## Extending the Framework

### Adding a New Provider

1. Create `src/api/providers/your_provider.py`:
```python
class YourProvider:
    def __init__(self, api_key):
        self.api_key = api_key
    
    def generate(self, prompt, model, **kwargs):
        # Implement API call
        return response_text
```

2. Update `src/core/runner.py` to include your provider

3. Add provider option in UI forms

### Adding New Evaluation Types

1. Add to `EvaluationType` enum in `src/core/models.py`
2. Implement logic in `src/core/evaluator.py`
3. Update UI dropdowns

## Roadmap

- [ ] OpenAI provider implementation
- [ ] Batch test execution
- [ ] Result comparison (A/B testing)
- [ ] Cost tracking per test
- [ ] Database storage option
- [ ] API for CI/CD integration
- [ ] Test scheduling
- [ ] Slack/Email notifications

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - feel free to use this for your projects!

## Support

For issues or questions:
- Open a GitHub issue
- Check documentation at [your-docs-url]

---

**Happy Testing! 🧪**