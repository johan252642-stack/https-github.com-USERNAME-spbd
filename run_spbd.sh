#!/bin/bash

DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"

# aktifkan venv
if [ -f "$DIR/venv/bin/activate" ]; then
    source "$DIR/venv/bin/activate"
fi

# jalankan tool (FIX PATH)
python3 "$DIR/spbd.py" "$@"
