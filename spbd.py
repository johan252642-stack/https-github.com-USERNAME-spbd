#!/usr/bin/env python3

# ===== CORE =====
from core.crawler import crawl
from core.scanner import scan_target
from core.intruder import intruder_scan
from core.recon import recon_scan
from core.js_crawler import crawl_js
from core.header_check import check_headers
from core.threads import run_threads
from core.printer import process_vuln, print_clean

# ===== WEB =====
from web.dashboard import run, socketio

# ===== LIB =====
from colorama import Fore, init
import threading, requests, sys

init(autoreset=True)

# ===== LIVE DASHBOARD =====
LIVE = {
    "vulns": [],
    "stats": {"SQLi":0, "XSS":0, "HEADERS":0}
}

# ===== BANNER (FIX SPBD) =====
def banner():
    print(Fore.RED + r"""
███████╗ ██████╗ ██████╗ ██████╗
██╔════╝██╔═══██╗██╔══██╗██╔══██╗
███████╗██║   ██║██████╔╝██████╔╝
╚════██║██║   ██║██╔═══╝ ██╔══██╗
███████║╚██████╔╝██║     ██████╔╝
╚══════╝ ╚═════╝ ╚═╝     ╚═════╝

██████╗ ██████╗ ██████╗ ██████╗
██╔══██╗██╔══██╗██╔══██╗██╔══██╗
██████╔╝██████╔╝██████╔╝██████╔╝
██╔═══╝ ██╔══██╗██╔══██╗██╔══██╗
██║     ██║  ██║██████╔╝██████╔╝
╚═╝     ╚═╝  ╚═╝╚═════╝ ╚═════╝
""")
    print(Fore.CYAN + "\n🔥 SPBD FINAL AI SCANNER 🔥\n")
    print(Fore.YELLOW + "⚠️ hasil = indikasi / validasi ringan\n")


# ===== MAIN =====
def main():
    banner()

    # ===== MODE =====
    if "--auto" in sys.argv:
        url = "https://example.com"
        mode = "full"
        print("[AUTO MODE]\n")
    else:
        url = input("Target: ").strip()
        mode = input("Mode(scan/intruder/full): ").strip()

    if not url or " " in url:
        print(Fore.RED + "[!] URL tidak valid")
        return

    session = requests.Session()

    # ===== DASHBOARD =====
    threading.Thread(target=run, daemon=True).start()
    print("[+] Dashboard: http://127.0.0.1:5000")

    # ===== RECON =====
    print(Fore.BLUE + "\n[RECON]")
    try:
        for r in recon_scan(url):
            print(r)
    except:
        print("[!] Recon error")

    # ===== JS =====
    print(Fore.BLUE + "\n[JS]")
    try:
        js = crawl_js(url)
        for j in js:
            print(j)
    except:
        js = []

    # ===== TARGET =====
    targets = crawl(url)
    targets += [j.get("url") for j in js if "url" in j]

    print(Fore.GREEN + f"\n[+] Total target: {len(targets)}")
    print("[+] Scanning...\n")

    # ===== WORKER =====
    def worker(t):
        res = []
        try:
            if mode in ["scan","full"]:
                res += scan_target(t, session)

            if mode in ["intruder","full"]:
                res += intruder_scan(t, session)

            res += check_headers(t)
        except:
            pass

        return res

    # ===== RUN THREAD =====
    results = run_threads(targets, worker, max_threads=5)

    # ===== PROCESS =====
    for r in results:
        if not r:
            continue

        for v in r:
            process_vuln(v)

            t = v.get("type","")

            if "SQLi" in t:
                LIVE["stats"]["SQLi"] += 1
            elif "XSS" in t:
                LIVE["stats"]["XSS"] += 1
            elif "Header" in t:
                LIVE["stats"]["HEADERS"] += 1

            LIVE["vulns"].append(v)

            socketio.emit("update", LIVE)

    # ===== CLEAN OUTPUT =====
    print_clean()

    print(Fore.GREEN + "\n[✓] DONE\n")


# ===== RUN =====
if __name__ == "__main__":
    main()
