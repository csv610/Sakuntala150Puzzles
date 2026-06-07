# Sakuntala 150 Puzzles

[![CI](https://github.com/csv610/Sakuntala150Puzzles/actions/workflows/ci.yml/badge.svg)](https://github.com/csv610/Sakuntala150Puzzles/actions/workflows/ci.yml)

Solve Shakuntala Devi's 150 mathematical puzzles using AI via LiteLLM.

## Features

- **CLI** — Batch-solve all 150 puzzles via `puzzles_cli.py` using Gemini 2.5 Flash
- **Streamlit UI** — Interactive puzzle browser with TTS via `sl_Shakuntala150.py`
- **Image support** — Puzzles with diagrams embedded as base64 and sent to the model
- **Multiple backends** — CLI uses Gemini; Streamlit supports any LiteLLM-compatible model (Ollama, etc.)

## Quick Start

```bash
pip install -e ".[dev]"
export GEMINI_API_KEY="your-key-here"
python puzzles_cli.py
```

For the Streamlit app:

```bash
pip install -e ".[streamlit]"
streamlit run sl_Shakuntala150.py
```

## Project Structure

```
├── puzzles_cli.py          # CLI: batch-solve with Gemini via LiteLLM
├── sl_Shakuntala150.py     # Streamlit: interactive puzzle UI
├── puzzles.json            # 150 puzzles with optional image refs
├── puzzles.tex             # LaTeX source for the book
├── images/                 # 11 diagram images for specific puzzles
├── tests/
│   ├── test_data_integrity.py    # JSON schema & file integrity
│   ├── test_puzzles_cli.py       # CLI function unit tests
│   └── test_sl_shakuntala.py     # Streamlit helper tests
├── pyproject.toml          # Project metadata & tool config
├── .github/workflows/ci.yml
└── .pre-commit-config.yaml
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all checks
pytest -v          # tests
ruff check .       # linting
mypy puzzles_cli.py  # type checking

# Install pre-commit hooks
pre-commit install
```
