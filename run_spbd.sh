#!/bin/bash
DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
python3 "$DIR/spbd.py" "$@"
