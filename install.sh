#!/bin/bash

echo "[SPBD] Installing..."

run() {
    eval "$1" >/dev/null 2>&1
}

# ===== DETECT OS =====
if [ -d "/data/data/com.termux/files/usr" ]; then
    echo "[+] Termux detected"

    run "pkg update -y"
    run "pkg upgrade -y"
    run "pkg install python git curl unzip golang -y"

    PIP="pip"
    PY="python"
    BIN="$PREFIX/bin"

    run "pkg install sqlmap -y"

    echo "[+] Installing nuclei..."
    run "go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest"

    if [ -f ~/go/bin/nuclei ]; then
        run "install -m 755 ~/go/bin/nuclei $BIN/"
    else
        echo "[!] nuclei install failed"
    fi

else
    echo "[+] Linux detected"

    export DEBIAN_FRONTEND=noninteractive

    run "sudo apt-get -qq update"
    run "sudo apt-get -y -qq install python3 python3-venv python3-pip git curl unzip"

    PIP="pip3"
    PY="python3"
    BIN="/usr/local/bin"

    run "sudo apt-get -y -qq install sqlmap"

    echo "[+] Installing nuclei..."
    run "curl -L https://github.com/projectdiscovery/nuclei/releases/latest/download/nuclei-linux-amd64.zip -o nuclei.zip"
    run "unzip -o nuclei.zip"
    run "chmod +x nuclei"
    run "sudo mv nuclei $BIN/"
    run "rm -f nuclei.zip"
fi

# ===== CHECK FILE CORE =====
echo "[+] Checking core files..."

FILES=("spbd.py" "ai.py" "ai_elite.py")

for f in "${FILES[@]}"; do
    if [ ! -f "$f" ]; then
        echo "[!] Missing file: $f"
    fi
done

# ===== SETUP VENV =====
echo "[+] Setup Python environment..."

if [ ! -d "venv" ]; then
    $PY -m venv venv
fi

source venv/bin/activate

echo "[+] Installing Python dependencies..."
$PIP install --upgrade pip

$PIP install \
requests \
flask \
flask-socketio \
colorama \
reportlab \
matplotlib \
urllib3

# ===== NUCLEI TEMPLATE =====
echo "[+] Updating nuclei templates..."
run "nuclei -update-templates"

# ===== FIX PERMISSION =====
chmod +x spbd.py 2>/dev/null
chmod +x spbd_dashboard_pro.py 2>/dev/null
chmod +x ai.py 2>/dev/null
chmod +x ai_elite.py 2>/dev/null

# ===== CREATE RUN SCRIPT =====
echo "[+] Creating runner..."

cat <<EOF > run_spbd.sh
#!/bin/bash
DIR="\$(cd "\$(dirname "\$(readlink -f "\$0")")" && pwd)"

# activate venv
if [ -f "\$DIR/venv/bin/activate" ]; then
    source "\$DIR/venv/bin/activate"
fi

# mode switch
if [[ "\$1" == "--web" ]]; then
    echo "[+] Starting Web Dashboard..."
    python3 "\$DIR/spbd.py" --web
else
    python3 "\$DIR/spbd.py" "\$@"
fi
EOF

chmod +x run_spbd.sh

# ===== GLOBAL COMMAND =====
echo "[+] Creating global command..."

if [ -w "/usr/bin" ]; then
    run "sudo ln -sf \$(pwd)/run_spbd.sh /usr/bin/spbd"
elif [ -n "$PREFIX" ]; then
    run "ln -sf \$(pwd)/run_spbd.sh $PREFIX/bin/spbd"
else
    echo "[!] Could not create global command"
fi

# ===== FINAL =====
echo ""
echo "==============================="
echo "[✓] INSTALL COMPLETE"
echo ""
echo "Usage:"
echo "  CLI : spbd"
echo "  WEB : spbd --web"
echo ""
echo "==============================="
