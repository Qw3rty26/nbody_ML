#!/usr/bin/env bash

MAIN="py/launch.py"

nix-shell --run "
if [ ! -d .venv ]; then
  python -m venv .venv
  source .venv/bin/activate
  pip install --upgrade pip
  pip install numpy scipy rebound
fi

source .venv/bin/activate
python $MAIN $*
"
