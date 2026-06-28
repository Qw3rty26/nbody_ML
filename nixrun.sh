#!/usr/bin/env bash

MAIN="py/server.py"

nix-shell --run '
source .venv/bin/activate

if ! python -c "import rebound" 2>/dev/null; then
  pip install -r requirements.txt
fi

python '"$MAIN"'
'
