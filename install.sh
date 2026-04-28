#!/bin/bash

echo "[SPBD] PRO INSTALLER AUTO-REPAIR 🔥"

LOG="install.log"
exec > >(tee -a $LOG) 2>&1

run() {
    eval "$1"
}

echo "[+] Checking internet..."
ping -c 1 google.com >/dev/null 2>&1 || { echo "[!] No internet"; exit 1; }

# ===== DETECT OS =====
if [ -d "/data/data/com.termux/files/usr" ]; then
    echo "[+] Termux detected"
    PKG="pkg"
    PY="python"
    PIP="pip"
    BIN="$PREFIX/bin"

    run "pkg update -y"
    run "pkg upgrade -y"
    run "pkg install python git curl unzip -y"

else
    echo "[+] Linux detected"
    PKG="apt"
    PY="python3"
    PIP="pip3"
    BIN="/usr/bin"

    run "apt update -y"
    run "apt install -y python3 python3-venv python3-pip git curl unzip"
fi

# ===== OPTIONAL TOOLS =====
read -p "Install sqlmap? (y/n): " sqlmap_install
if [[ "$sqlmap_install" == "y" ]]; then
    run "$PKG install -y sqlmap"
fi

read -p "Install nuclei? (y/n): " nuclei_install
if [[ "$nuclei_install" == "y" ]]; then
    if command -v go >/dev/null; then
        run "go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest"
        run "cp ~/go/bin/nuclei $BIN/"
    else
        echo "[!] Go not installed, skipping nuclei"
    fi
fi

# ===== CHECK FILE =====
echo "[+] Checking project files..."

REQUIRED=("spbd.py" "ai.py" "ai_elite.py")

for f in "${REQUIRED[@]}"; do
    if [ ! -f "$f" ]; then
        echo "[!] Missing $f → cloning fresh repo..."
        rm -rf *
        git clone https://github.com/johan252642-stack/spbd.git .
        break
    fi
done

# ===== FIX BROKEN CORE =====
echo "[+] Checking core structure..."

if [ -d "core/core" ]; then
    echo "[!] Broken core detected → repairing..."

    find core -type f -name "*.py" -exec mv -t core {} +
    rm -rf core/core

    echo "[✓] Core repaired"
fi

# ===== SETUP VENV =====
echo "[+] Creating virtual environment..."

if [ ! -d "venv" ]; then
    $PY -m venv venv
fi

source venv/bin/activate

echo "[+] Installing Python packages..."
$PIP install --upgrade pip

$PIP install \
requests \
flask \
flask-socketio \
colorama \
reportlab \
matplotlib \
urllib3 \
beautifulsoup4

# ===== FIX PERMISSION =====
chmod +x *.py 2>/dev/null

# ===== CREATE RUNNER =====
echo "[+] Creating runner..."

cat <<EOF > run_spbd.sh
#!/bin/bash
DIR="\$(cd "\$(dirname "\$(readlink -f "\$0")")" && pwd)"

if [ -f "\$DIR/venv/bin/activate" ]; then
    source "\$DIR/venv/bin/activate"
fi

python3 "\$DIR/spbd.py" "\$@"
EOF

chmod +x run_spbd.sh

# ===== FIX SYMLINK (AUTO REPAIR) =====
echo "[+] Fixing global command..."

rm -f $BIN/spbd

ln -s $(pwd)/run_spbd.sh $BIN/spbd

# ===== VERIFY =====
if [ -L "$BIN/spbd" ]; then
    echo "[✓] Command fixed: spbd"
else
    echo "[!] Failed to create command"
fi

# ===== DONE =====
echo ""
echo "==============================="
echo "[✓] INSTALL COMPLETE 🔥"
echo ""
echo "Run:"
echo "  spbd"
echo "  spbd --web"
echo ""
echo "Log: install.log"
echo "==============================="
