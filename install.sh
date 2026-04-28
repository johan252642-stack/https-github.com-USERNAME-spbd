#!/bin/bash

LOG="install.log"

echo "[SPBD] PRO INSTALLER" | tee $LOG

run() {
    eval "$1" >>$LOG 2>&1
}

check_cmd() {
    command -v "$1" >/dev/null 2>&1
}

# =========================
# 🌐 CHECK INTERNET
# =========================
echo "[+] Checking internet..."
ping -c 1 google.com >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "[!] No internet connection"
    exit 1
fi

# =========================
# 🧠 DETECT OS
# =========================
OS="$(uname -s)"
echo "[+] OS: $OS"

# =========================
# 📦 DETECT PYTHON
# =========================
if check_cmd python3; then
    PY="python3"
elif check_cmd python; then
    PY="python"
else
    echo "[!] Python not found. Install Python first."
    exit 1
fi

# =========================
# 📦 DETECT PIP
# =========================
if check_cmd pip3; then
    PIP="pip3"
elif check_cmd pip; then
    PIP="pip"
else
    echo "[!] pip not found. Installing..."
    run "$PY -m ensurepip"
    PIP="pip"
fi

# =========================
# 📱 TERMUX
# =========================
if [ -d "/data/data/com.termux/files/usr" ]; then
    echo "[+] Termux detected"

    run "pkg update -y"
    run "pkg upgrade -y"
    run "pkg install python git curl unzip golang -y"

    BIN="$PREFIX/bin"

    read -p "Install sqlmap? (y/n): " opt
    [[ $opt == "y" ]] && run "pkg install sqlmap -y"

    read -p "Install nuclei? (y/n): " opt
    if [[ $opt == "y" ]]; then
        run "go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest"
        [ -f ~/go/bin/nuclei ] && run "install -m 755 ~/go/bin/nuclei $BIN/"
    fi

# =========================
# 🐧 LINUX / WSL
# =========================
elif [[ "$OS" == "Linux" ]]; then
    echo "[+] Linux detected"

    run "sudo apt update -y"
    run "sudo apt install python3 python3-venv python3-pip git curl unzip -y"

    BIN="/usr/local/bin"

    read -p "Install sqlmap? (y/n): " opt
    [[ $opt == "y" ]] && run "sudo apt install sqlmap -y"

    read -p "Install nuclei? (y/n): " opt
    if [[ $opt == "y" ]]; then
        run "curl -L https://github.com/projectdiscovery/nuclei/releases/latest/download/nuclei-linux-amd64.zip -o nuclei.zip"
        run "unzip -o nuclei.zip"
        run "chmod +x nuclei"
        run "sudo mv nuclei $BIN/"
        run "rm -f nuclei.zip"
    fi

# =========================
# 🪟 WINDOWS (GIT BASH)
# =========================
elif [[ "$OS" == "MINGW"* ]] || [[ "$OS" == "CYGWIN"* ]]; then
    echo "[+] Windows detected"

    echo "[!] Make sure Python is installed"
    echo "[!] Recommended: use WSL for full features"

else
    echo "[!] Unsupported OS"
fi

# =========================
# 📁 CHECK FILES
# =========================
echo "[+] Checking project files..."

FILES=("spbd.py" "ai.py" "ai_elite.py")

for f in "${FILES[@]}"; do
    if [ ! -f "$f" ]; then
        echo "[!] Missing: $f"
    fi
done

# =========================
# 🐍 VENV
# =========================
echo "[+] Creating virtual environment..."

if [ ! -d "venv" ]; then
    run "$PY -m venv venv"
fi

source venv/bin/activate 2>/dev/null

# =========================
# 📦 INSTALL DEPENDENCIES
# =========================
echo "[+] Installing Python packages..."

$PIP install --upgrade pip >>$LOG 2>&1

$PIP install \
requests \
beautifulsoup4 \
flask \
colorama \
urllib3 >>$LOG 2>&1

# =========================
# 🔧 PERMISSIONS
# =========================
chmod +x spbd.py 2>/dev/null
chmod +x ai.py 2>/dev/null
chmod +x ai_elite.py 2>/dev/null

# =========================
# ▶️ RUN SCRIPT
# =========================
echo "[+] Creating runner..."

cat <<EOF > run_spbd.sh
#!/bin/bash
DIR="\$(cd "\$(dirname "\$0")" && pwd)"

if [ -f "\$DIR/venv/bin/activate" ]; then
    source "\$DIR/venv/bin/activate"
fi

if [[ "\$1" == "--web" ]]; then
    python3 "\$DIR/spbd.py" --web
else
    python3 "\$DIR/spbd.py" "\$@"
fi
EOF

chmod +x run_spbd.sh

# =========================
# 🌍 GLOBAL COMMAND
# =========================
echo "[+] Creating global command..."

if [ -w "/usr/bin" ]; then
    run "sudo ln -sf \$(pwd)/run_spbd.sh /usr/bin/spbd"
elif [ -n "$PREFIX" ]; then
    run "ln -sf \$(pwd)/run_spbd.sh $PREFIX/bin/spbd"
fi

# =========================
# 📄 SUMMARY
# =========================
echo ""
echo "==============================="
echo "[✓] INSTALL COMPLETE"
echo ""
echo "Run:"
echo "  ./run_spbd.sh"
echo "  spbd"
echo "  spbd --web"
echo ""
echo "Log saved to: $LOG"
echo "==============================="
