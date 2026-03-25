#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo
echo "== Jerry LLM Workbench: Unix Setup =="

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "Python 3 not found. Install Python 3.11+ and rerun." >&2
  exit 1
fi

echo "Using $($PYTHON_BIN --version 2>&1)"

if [[ ! -x .venv/bin/python ]]; then
  echo "Creating virtual environment (.venv)..."
  "$PYTHON_BIN" -m venv .venv
else
  echo "Virtual environment already exists. Reusing .venv"
fi

echo "Upgrading pip (optional)..."
if ! ./.venv/bin/python -m pip install --upgrade pip; then
  echo "Warning: pip upgrade failed, continuing with current pip version."
fi

echo "Installing requirements.txt..."
./.venv/bin/python -m pip install -r requirements.txt

if [[ ! -f .env && -f .env.example ]]; then
  cp .env.example .env
  echo "Created .env from .env.example"
else
  echo ".env already exists or .env.example is missing"
fi

echo
echo "Setup complete."
echo "Run:"
echo "  ./.venv/bin/python scripts/system_check.py"
