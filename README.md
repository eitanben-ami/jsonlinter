# jsonlinter

A lightweight JSON linter CLI that catches common formatting and structural mistakes without enforcing a strict JSON schema.

## About

Real JSON files in the wild accumulate small, mechanical issues: trailing commas, tabs instead of spaces, trailing whitespace, duplicate keys, or too many blank lines. These don't always break parsing, but they create noisy diffs and fragile automation. `jsonlinter` reports those issues with file names and line numbers so they can be fixed quickly.

## Features

- Trailing comma detection in arrays and objects.
- Tab character detection.
- Trailing whitespace detection.
- Excess blank line detection inside arrays and objects.
- Duplicate top-level key detection.
- Multiple output modes: plain and JSON.
- Recursive directory scanning.
- Deterministic, file-order output.
- Stdlib-only implementation.

## Installation

```bash
git clone https://github.com/eitanben-ami/jsonlinter.git
cd jsonlinter
python -m pip install -e .
```

## Usage

```bash
# Lint a single file
jsonlinter README.json

# Lint recursively
jsonlinter --recursive .

# JSON output
jsonlinter --format json configs/
```

### Exit codes

- `0` — no issues found.
- `1` — one or more lint issues found.
- `2` — invalid arguments or read error.

### Output modes

- `plain` — compact lines like `file:line:col: message`.
- `json` — machine-readable JSON array of issue objects.

## Project structure

```
jsonlinter/
├── README.md
├── pyproject.toml
├── .gitignore
├── jsonlinter/
│   ├── __init__.py
│   ├── cli.py
│   ├── linter.py
│   └── model.py
└── tests/
    ├── __init__.py
    ├── test_cli.py
    └── test_linter.py
```

## Tags / keywords

json, linter, cli, developer-tools, stdlib, formatting
