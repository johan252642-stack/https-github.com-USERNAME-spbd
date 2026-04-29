#!/bin/bash

echo "[SPBD] ULTIMATE INSTALLER 🔥"

LOG="install.log"
exec > >(tee -a $LOG) 2>&1

silent() {
    eval "$1" >/dev/null 2>&1
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

else
    echo "[+] Linux/macOS detected"
    PKG="apt"
    PY="python3"
    PIP="pip3"
    BIN="/usr/bin"
fi

# ===== INSTALL SYSTEM =====
echo "[+] Install sistem tools..."

silent "$PKG update -y"
silent "$PKG install -y python3 python3-pip git curl unzip"

# sqlmap + nuclei
if ! command -v sqlmap >/dev/null; then
    silent "$PKG install -y sqlmap"
fi

if ! command -v go >/dev/null; then
    silent "$PKG install -y golang"
fi

silent "go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest"
[ -f ~/go/bin/nuclei ] && silent "cp ~/go/bin/nuclei $BIN/"

echo "[✓] Tools siap"

# ===== PYTHON DEP =====
echo "[+] Install Python dependency..."

$PIP install --upgrade pip >/dev/null 2>&1

$PIP install \
flask flask-socketio requests bs4 colorama >/dev/null 2>&1

echo "[✓] Dependency siap"

# ===== RUNNER =====
cat <<EOF > run_spbd.sh
#!/bin/bash
DIR="\$(cd "\$(dirname "\$(readlink -f "\$0")")" && pwd)"
python3 "\$DIR/spbd.py" "\$@"
EOF

chmod +x run_spbd.sh

# ===== SYMLINK =====
echo "[+] Setup command spbd..."

TARGET_PATH="$(pwd)/run_spbd.sh"

if [[ "$OS" == "Windows_NT" ]]; then
    echo "[!] Windows terdeteksi"
    echo "[✓] Jalankan: python spbd.py"
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
echo "[+] Menjalankan SPBD Demo..."

sleep 2

if command -v spbd >/dev/null 2>&1; then
    spbd --auto
else
    python3 spbd.py --auto
fi
