# AI Test Case Generator

Generates comprehensive QA test cases from plain English feature descriptions using Claude AI.

## What this does

Takes a feature description as input and uses Claude AI to generate structured test cases covering Functional, Negative, Boundary, Security, UI-UX, and Integration scenarios. Outputs a formatted CSV ready to import into any test management tool like Qase, TestRail, or Jira.

## Demo

Input: User Login Feature - Users can log in with email and password. After 3 failed attempts the account locks for 15 minutes.

Output: 40 structured test cases in CSV format in under 15 seconds.

## Tech stack

- Python 3.10
- Claude AI (Anthropic API)
- python-dotenv
- pytest + pytest-html

## How to run

1. Clone the repo
   git clone https://github.com/thila98/ai-test-case-generator

2. Create virtual environment
   python3 -m venv venv
   source venv/bin/activate

3. Install dependencies
   pip install -r requirements.txt

4. Add your API key
   cp .env.example .env
   Then edit .env and add your ANTHROPIC_API_KEY

5. Run
   python main.py "Your feature description here"

## Test coverage generated

Each run covers Functional, Negative, Boundary, Security, UI-UX, and Integration scenarios.

## What I learned

- How to integrate Claude AI API into a Python CLI tool
- Prompt engineering for structured QA output
- Building secure Python projects with environment variable management
- CSV generation and output formatting for test management tools

## Author

Thilangi Uththara De Silva - Senior QA Engineer
GitHub: https://github.com/thila98
