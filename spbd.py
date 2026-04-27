#!/usr/bin/env python3
import os, argparse, re, json, time, random, threading, zipfile, shutil, tempfile
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse, urljoin

import requests
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, jsonify, render_template_string

init(autoreset=True)

# ===== AI =====
from ai import analyze, payload_for
from ai_elite import analyze_target

# ===== CONFIG =====
SESSION_FILE = "session.json"
LOCAL_VERSION_FILE = "version.json"

# 👉 GANTI INI DENGAN REPO KAMU
VERSION_URL = "https://raw.githubusercontent.com/USERNAME/spbd/main/version.json"
ZIP_URL = "https://github.com/USERNAME/spbd/archive/refs/heads/main.zip"

MODE = {
    "fast": {"timeout":3, "threads":5},
    "deep": {"timeout":8, "threads":3},
    "stealth": {"timeout":10, "threads":2}
}

RATE = {
    "fast": (0.2, 0.5),
    "deep": (0.5, 1.5),
    "stealth": (1.5, 3.0)
}

# ===== ARG =====
ap = argparse.ArgumentParser()
ap.add_argument("--mode", default="fast", choices=["fast","deep","stealth"])
ap.add_argument("--web", action="store_true")
ap.add_argument("--update", action="store_true")
ap.add_argument("--update-ng", action="store_true")
ap.add_argument("--update-pro", action="store_true")
args = ap.parse_args()

cfg = MODE[args.mode]
session = requests.Session()

LIVE = {"status":"idle","progress":0,"results":{}}

# ===== BANNER =====
def banner():
    print(Fore.RED + """
███████╗██████╗ ██████╗ ██████╗
██╔════╝██╔══██╗██╔══██╗██╔══██╗
███████╗██████╔╝██████╔╝██║  ██║
╚════██║██╔═══╝ ██╔══██╗██║  ██║
███████║██║     ██████╔╝██████╔╝
╚══════╝╚═╝     ╚═════╝ ╚═════╝
""")
    print(Fore.YELLOW + "⚡ SPBD ELITE FINAL\n")

# =========================
# 🔥 UPDATE MODES
# =========================

def auto_update_git():
    print("[+] Git update...")
    if not os.path.exists(".git"):
        print("[!] Not git repo")
        return
    os.system("git fetch")
    status = os.popen("git status -uno").read()
    if "up to date" in status.lower():
        print("[✓] Already latest")
        return
    os.system("git stash")
    os.system("git pull origin spbd")
    os.system("pip install -r requirements.txt")
    print("[✓] Done")


def auto_update_no_git():
    print("[+] Updating (no git)...")

    tmp = tempfile.mkdtemp()
    zip_path = os.path.join(tmp, "update.zip")

    try:
        r = requests.get(ZIP_URL)
        open(zip_path, "wb").write(r.content)

        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(tmp)

        extracted = [d for d in os.listdir(tmp) if d.startswith("spbd-")][0]
        extracted = os.path.join(tmp, extracted)

        for root, dirs, files in os.walk(extracted):
            for f in files:
                src = os.path.join(root, f)
                rel = os.path.relpath(src, extracted)
                dst = os.path.join(os.getcwd(), rel)

                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)

        os.system("pip install -r requirements.txt")

        print("[✓] Update complete")

    except Exception as e:
        print("[!] Failed:", e)

    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def get_local_version():
    if not os.path.exists(LOCAL_VERSION_FILE):
        return "0.0.0"
    try:
        return json.load(open(LOCAL_VERSION_FILE))["version"]
    except:
        return "0.0.0"


def get_remote_version():
    try:
        r = requests.get(VERSION_URL)
        data = r.json()
        return data["version"], data.get("changelog", [])
    except:
        return None, []


def auto_update_pro():
    print("[+] Checking version...")

    local = get_local_version()
    remote, changelog = get_remote_version()

    if not remote:
        print("[!] Failed version check")
        return

    print(f"LOCAL  : {local}")
    print(f"REMOTE : {remote}")

    if local == remote:
        print("[✓] Already latest")
        return

    print("\n[+] Update available!")
    for c in changelog:
        print(" -", c)

    if input("Update? (y/n): ").lower() != "y":
        return

    backup = "backup_old"
    if os.path.exists(backup):
        shutil.rmtree(backup)
    shutil.copytree(os.getcwd(), backup, dirs_exist_ok=True)

    try:
        auto_update_no_git()
        print("[✓] Update success")

    except:
        print("[!] Failed → rollback")
        shutil.copytree(backup, os.getcwd(), dirs_exist_ok=True)


# ===== DELAY =====
def delay():
    low, high = RATE[args.mode]
    time.sleep(random.uniform(low, high))

# ===== REQUEST =====
def safe_get(url):
    for _ in range(3):
        try:
            delay()
            return session.get(url, timeout=cfg["timeout"]).text
        except:
            time.sleep(1)
    return ""

# ===== INJECT =====
def inject(url, param, payload):
    p = urlparse(url)
    qs = parse_qs(p.query)
    qs[param] = payload
    new = urlunparse(p._replace(query=urlencode(qs, doseq=True)))
    return safe_get(new)

# ===== SCAN =====
def scan(url):
    vulns = []
    base = safe_get(url)

    if "?" not in url:
        return vulns

    for param in parse_qs(urlparse(url).query):
        pdata = payload_for(param)

        for payload in pdata["all"]:
            print(Fore.CYAN + f"[TEST] {param} → {payload}")

            txt = inject(url, param, payload)
            ai = analyze(base, txt, param, payload, pdata["type"])

            if ai:
                print(Fore.RED + f"[{ai['severity']}] {param}")
                print(Fore.YELLOW + ai["reason"])
                vulns.append(ai)
                break

    return vulns

# ===== THREAD =====
def run_scan(targets):
    LIVE["status"] = "running"
    total = len(targets)

    def worker(url):
        v = scan(url)
        LIVE["results"][url] = {
            "vulns": v,
            "elite": analyze_target(url, v)
        }

    with ThreadPoolExecutor(max_workers=cfg["threads"]) as exe:
        for i, _ in enumerate(exe.map(worker, targets)):
            LIVE["progress"] = int((i+1)/total*100)

    LIVE["status"] = "done"

# ===== RECON =====
def expand(url):
    return list(set([url] + [urljoin(url,p) for p in ["admin","login","api","dashboard"]]))

# ===== WEB =====
app = Flask(__name__)

@app.route("/")
def home():
    return jsonify(LIVE)

def start_web():
    app.run(port=5000)

# ===== MAIN =====
def main():
    banner()

    if args.update:
        auto_update_git()
        return

    if args.update_ng:
        auto_update_no_git()
        return

    if args.update_pro:
        auto_update_pro()
        return

    url = input("Target: ")
    targets = expand(url)

    if args.web:
        threading.Thread(target=start_web).start()
        print("[+] Web UI: http://127.0.0.1:5000")

    run_scan(targets)

    json.dump(LIVE, open(SESSION_FILE,"w"), indent=2)

    print("\n[✓] DONE")

if __name__ == "__main__":
    main()
