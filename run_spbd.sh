#!/bin/bash
DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"

if [ -f "$DIR/venv/bin/activate" ]; then
    source "$DIR/venv/bin/activate"
fi

python3 "$DIR/spbd.py" "$@"
