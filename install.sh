#!/bin/bash

echo "[SPBD] ULTIMATE INSTALLER 🔥"

LOG="install.log"
exec > >(tee -a $LOG) 2>&1

echo "[+] Checking internet..."
ping -c 1 google.com >/dev/null 2>&1 || { echo "[!] No internet"; exit 1; }

# ===== DETECT OS =====
if [ -d "/data/data/com.termux/files/usr" ]; then
    echo "[+] Termux detected"
    PKG="pkg"
    PY="python"
    BIN="$PREFIX/bin"
else
    echo "[+] Linux/macOS detected"
    PKG="apt"
    PY="python3"
    BIN="/usr/bin"
fi

# ===== INSTALL SYSTEM =====
echo "[+] Install sistem tools..."

$PKG update -y >/dev/null 2>&1
$PKG install -y python3 python3-pip git curl unzip >/dev/null 2>&1

# optional tools
if ! command -v sqlmap >/dev/null; then
    $PKG install -y sqlmap >/dev/null 2>&1
fi

if ! command -v go >/dev/null; then
    $PKG install -y golang >/dev/null 2>&1
fi

go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest >/dev/null 2>&1
[ -f ~/go/bin/nuclei ] && cp ~/go/bin/nuclei $BIN/ >/dev/null 2>&1

echo "[✓] Tools siap"

# ===== FIX CORE STRUCTURE =====
echo "[+] Fix core structure..."

if [ -d "core/core" ]; then
    find core -type f -name "*.py" -exec mv -t core {} +
    rm -rf core/core
    echo "[✓] Core diperbaiki"
fi

# ===== CLEAN CACHE =====
rm -rf core/__pycache__ 2>/dev/null

# ===== VENV SETUP =====
echo "[+] Setup Python environment..."

if [ ! -d "venv" ]; then
    $PY -m venv venv
fi

source venv/bin/activate

# ===== INSTALL PYTHON DEP =====
echo "[+] Install Python dependency..."

pip install --upgrade pip >/dev/null 2>&1

pip install \
flask \
flask-socketio \
requests \
bs4 \
colorama >/dev/null 2>&1

echo "[✓] Python siap"

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

# ===== SYMLINK =====
echo "[+] Setup command spbd..."

TARGET_PATH="$(pwd)/run_spbd.sh"

if [[ "$OS" == "Windows_NT" ]]; then
    echo "[!] Windows terdeteksi"
    echo "[✓] Jalankan manual: python spbd.py"
else
    rm -f "$BIN/spbd" 2>/dev/null
    ln -s "$TARGET_PATH" "$BIN/spbd" 2>/dev/null

    if command -v spbd >/dev/null 2>&1; then
        echo "[✓] spbd siap"
    else
        echo "[!] Fix dengan sudo..."
        sudo ln -sf "$TARGET_PATH" /usr/bin/spbd 2>/dev/null
    fi
fi

# ===== AUTO DEMO =====
echo ""
echo "[+] Menjalankan SPBD..."

sleep 2

if command -v spbd >/dev/null 2>&1; then
    spbd --auto
else
    python3 spbd.py --auto
fi

echo ""
echo "==============================="
echo "[✓] INSTALL COMPLETE 🔥"
echo "==============================="
