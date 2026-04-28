#!/bin/bash
DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"

# activate venv
if [ -f "$DIR/venv/bin/activate" ]; then
    source "$DIR/venv/bin/activate"
fi

# mode switch
if [[ "$1" == "--web" ]]; then
    echo "[+] Starting Web Dashboard..."
    python3 "$DIR/spbd.py" --web
else
    python3 "$DIR/spbd.py" "$@"
fi
