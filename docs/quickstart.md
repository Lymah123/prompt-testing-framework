# Quick Start Guide

## Installation (5 minutes)

### Step 1: Prerequisites
- Python 3.8 or higher installed
- Claude API key (get one at https://console.anthropic.com)

### Step 2: Clone and Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd prompt-testing-framework

# Run the setup script
chmod +x run.sh  # Unix/Mac
./run.sh         # Unix/Mac
# or
run.bat          # Windows
```

### Step 3: Add Your API Key
Edit `.env` file:
```
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

### Step 4: Launch
```bash
streamlit run ui/app.py
```

## Your First Test (5 minutes)

### 1. Create a Test Case
1. Navigate to **Test Cases** page (sidebar)
2. Fill in:
   - **Name**: "My First Test"
   - **Prompt**: "Explain quantum computing in one sentence"
   - **Model**: claude-sonnet-4-20250514
3. Add an Expectation:
   - Type: `contains`
   - Value: `quantum`
4. Click **Save Test Case**

### 2. Run the Test
1. Go to **Run Tests** page
2. Select "My First Test"
3. Click **Run Selected Tests**
4. Watch the results appear!

### 3. View Results
1. Go to **Results** page
2. See your test execution history
3. Click to expand and view details

## What's Next?

### Try Different Models
Compare results across models:
- claude-sonnet-4-20250514 (balanced)
- claude-opus-4-20250514 (most capable)

### Add More Expectations
Try different assertion types:
- `length_max: 200` - Keep responses concise
- `regex: \d+` - Ensure numbers are included
- `not_contains: error` - Avoid error messages

### Organize with Tags
Tag tests by:
- Feature: `summarization`, `code-gen`, `translation`
- Priority: `critical`, `nice-to-have`
- Model: `claude`, `gpt4`

### Batch Testing
1. Create multiple related tests
2. Use tags to group them
3. Run all at once with "Run All Tests"

## Common Patterns

### Testing Summarization
```python
{
  "name": "Summary Test",
  "prompt": "Summarize: [long text]",
  "expectations": [
    {"type": "length_max", "value": 500},
    {"type": "contains", "value": "key point"}
  ]
}
```

### Testing Code Generation
```python
{
  "name": "Code Test",
  "prompt": "Write a Python function to [task]",
  "expectations": [
    {"type": "contains", "value": "def"},
    {"type": "regex", "value": "def\\s+\\w+\\("}
  ]
}
```

### Testing Tone/Style
```python
{
  "name": "Tone Test",
  "prompt": "Write professionally about [topic]",
  "system_prompt": "You are a professional writer",
  "expectations": [
    {"type": "not_contains", "value": "slang"},
    {"type": "manual", "value": "Check formality"}
  ]
}
```

## Tips for Success

1. **Start Simple**: Basic contains checks first
2. **Iterate Quickly**: Run tests frequently
3. **Use System Prompts**: Control behavior consistently
4. **Temperature Matters**: 
   - 0.3 for factual/code
   - 1.0 for creative
5. **Tag Everything**: Makes filtering easier

## Troubleshooting

### "API Key Error"
- Check `.env` file exists
- Verify key starts with `sk-ant-`
- No quotes around key in .env

### "Module Not Found"
```bash
pip install -r requirements.txt
```

### "Cannot Connect"
- Check internet connection
- Verify API key is valid
- Try again (rate limiting)

## Need Help?

- Check [README.md](../README.md) for full docs
- Open an issue on GitHub
- Review sample tests in `tests/sample_tests.json`