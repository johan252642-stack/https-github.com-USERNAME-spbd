#!/usr/bin/env python3

from core.crawler import crawl
from core.scanner import scan_target
from core.intruder import intruder_scan
from core.recon import recon_scan
from core.js_crawler import crawl_js
from core.header_check import check_headers
from core.threads import run_threads

from web.dashboard import run, socketio

from colorama import Fore, init
import threading, requests, sys

init(autoreset=True)

LIVE={"vulns":[]}

def banner():
    print(Fore.RED + r"""
███████╗██████╗ ██████╗ ██████╗
██╔════╝██╔══██╗██╔══██╗██╔══██╗
███████╗██████╔╝██████╔╝██║  ██║
╚════██║██╔═══╝ ██╔══██╗██║  ██║
███████║██║     ██████╔╝██████╔╝
╚══════╝╚═╝     ╚═════╝ ╚═════╝
""")
    print("🔥 SPBD FINAL AI SCANNER 🔥\n")

def main():
    banner()

    # ===== AUTO MODE =====
    if "--auto" in sys.argv:
        print("[AUTO MODE]\n")
        url = "https://example.com"
        mode = "full"
    else:
        url = input("Target: ")
        mode = input("Mode(scan/intruder/full): ")

    session = requests.Session()

    threading.Thread(target=run, daemon=True).start()
    print("[+] Dashboard: http://127.0.0.1:5000")

    print("\n[RECON]")
    for r in recon_scan(url):
        print(r)

    print("\n[JS]")
    js = crawl_js(url)
    for j in js:
        print(j)

    targets = crawl(url)
    targets += [j["url"] for j in js]

    def worker(t):
        res = []
        if mode in ["scan","full"]:
            res += scan_target(t,session)
        if mode in ["intruder","full"]:
            res += intruder_scan(t,session)
        res += check_headers(t)
        return res

    results = run_threads(targets,worker)

    for r in results:
        print(r)
        LIVE["vulns"].append(r)
        socketio.emit("update",LIVE)

    print("\n[✓ DONE]")

if __name__ == "__main__":
    main()
