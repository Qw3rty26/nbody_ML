#!/usr/bin/env bash

MAIN="py/main.py"

nix-shell --run "python ${MAIN}"
