# StyleScope + ToolWise

A two-milestone Python project combining **CSS Intelligence Studio** (Milestone 1) and **Reliable AI Agent Lab** (Milestone 2).

---

## Project Structure

```
StyleScope_ToolWise/
├── src/
│   ├── __init__.py
│   ├── css_parser.py       # CSS parsing using tinycss2
│   ├── css_analyzer.py     # CSS statistics and report generation
│   ├── tools.py            # Calculator, text & file analysis tools
│   └── agent.py            # Rule-based AI agent controller
├── tests/
│   ├── __init__.py
│   ├── test_css_parser.py
│   ├── test_css_analyzer.py
│   ├── test_tools.py
│   └── test_agent.py
├── examples/
│   └── demo_requests.md
├── sample_styles.css
├── requirements.txt
├── .gitignore
├── README.md
└── app.py                  # Streamlit web application
```

---

## Milestone 1 — CSS Intelligence Studio

**Features:**
- Parse CSS text or files using `tinycss2`
- Extract: rules, selectors, declarations, at-rules, CSS variables, comments, parse errors
- Generate summary statistics (rule count, unique properties, media queries, keyframes, etc.)
- Export results as JSON
- Generate human-readable text reports

**Modules:**
- `src/css_parser.py` — Core CSS parsing logic
- `src/css_analyzer.py` — Analysis and reporting

---

## Milestone 2 — Reliable AI Agent Lab

**Features:**
- **Calculator Tool** — Safe arithmetic evaluation (no `eval` injection)
- **Text Analysis Tool** — Word count, sentence count, reading time, top words
- **File Analysis Tool** — Read and summarize local text/CSS/Markdown files
- **Agent Controller** — Rule-based intent detection and tool routing
- Full execution history with timestamps

**Modules:**
- `src/tools.py` — Individual tool implementations
- `src/agent.py` — Agent routing and orchestration

---

## Installation

```bash
pip install -r requirements.txt
```

## Running the App

```bash
streamlit run app.py
```

## Running Tests

```bash
pytest tests/ -v
```

---

## Usage Examples

### CSS Parser
```python
from src.css_parser import parse_css, result_to_json

result = parse_css("body { color: red; margin: 0; }")
print(result_to_json(result))
```

### CSS Analyzer
```python
from src.css_parser import parse_css
from src.css_analyzer import analyze, generate_report

result = parse_css("body { color: red; } .container { max-width: 1200px; }")
stats = analyze(result)
print(generate_report(result, stats))
```

### Agent
```python
from src.agent import Agent

agent = Agent(base_dir=".")
response = agent.process("calculate: (100 + 50) / 2")
print(response["response_text"])

response = agent.process("analyze text: Hello world, this is a test.")
print(response["response_text"])
```

---

## License

MIT
