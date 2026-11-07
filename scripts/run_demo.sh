#!/usr/bin/env bash
# Launch the integrated demo. Owner: Jawad.
# Usage: bash scripts/run_demo.sh        (creates .venv on first run, then starts the app)
set -euo pipefail
cd "$(dirname "$0")/.."

PY="${PYTHON:-python3}"
if [ ! -x .venv/bin/python ]; then
  echo "Creating .venv with $($PY --version)..."
  "$PY" -m venv .venv
fi
.venv/bin/pip install -q --upgrade pip >/dev/null
.venv/bin/pip install -q -r requirements.txt

if [ ! -f app/app.py ]; then
  echo "app/app.py is not merged yet. Checking the engine contract instead:"
  exec .venv/bin/python scripts/check_contract.py
fi

export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}"
exec .venv/bin/streamlit run app/app.py
