#!/bin/bash

echo "[SPBD] AUTO GIT SYNC 🔥"

# ===== CEK INTERNET =====
echo "[+] Checking internet..."

if ! ping -c 1 8.8.8.8 >/dev/null 2>&1; then
    echo "[!] Internet bermasalah (lanjut paksa...)"
fi

# ===== ADD =====
echo "[+] Adding files..."
git add -A

# ===== COMMIT =====
MSG=${1:-"auto update"}

git commit -m "$MSG" >/dev/null 2>&1

# ===== PULL =====
echo "[+] Sync dengan remote..."
git pull origin spbd --no-edit

# ===== PUSH =====
echo "[+] Push ke GitHub..."

if git push origin spbd; then
    echo "[✓] Push berhasil"
else
    echo "[!] Push gagal → mencoba force..."
    git push origin spbd -f
fi

echo "[✓] DONE"
