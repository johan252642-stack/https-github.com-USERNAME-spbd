#!/usr/bin/env python3

from core.crawler import crawl
from core.scanner import scan_target
from core.printer import print_vuln, print_summary
from core.threads import run_threads
from core.scorer import sort_vulns
from report import generate_report
from web.dashboard import run, socketio
from colorama import Fore, init
import threading, time

init(autoreset=True)

LIVE = {"target":"","vulns":[],"stats":{"CRITICAL":0,"HIGH":0,"MEDIUM":0,"LOW":0}}

def banner():
    print(Fore.RED + r"""
 ███████╗██████╗ ██████╗ ██████╗ 
 ██╔════╝██╔══██╗██╔══██╗██╔══██╗
 ███████╗██████╔╝██████╔╝██║  ██║
 ╚════██║██╔═══╝ ██╔══██╗██║  ██║
 ███████║██║     ██████╔╝██████╔╝
 ╚══════╝╚═╝     ╚═════╝ ╚═════╝ 
""")
    print(Fore.CYAN + "🔥 SPBD ELITE SCANNER 🔥\n")

def loading():
    print("[*] Loading engine...", end="", flush=True)
    time.sleep(1)
    print(" OK\n")

def main():
    banner()
    loading()

    mode = input("Mode (cli/web): ")
    url = input("Target: ")

    LIVE["target"] = url

    if mode == "web":
        threading.Thread(target=run, daemon=True).start()
        print("[+] Dashboard: http://127.0.0.1:5000")

    targets = crawl(url) if "?" not in url else [url]

    def worker(t):
        print(Fore.CYAN + f"[SCAN] {t}")
        return scan_target(t)

    results = run_threads(targets, worker)
    results = sort_vulns(results)

    for v in results:
        print_vuln(url, v)

        LIVE["vulns"].append(v)
        LIVE["stats"][v["severity"]] += 1

        socketio.emit("update", LIVE)

    print_summary(LIVE["stats"])
    generate_report(LIVE)

    print("\n[✓] SELESAI")

if __name__ == "__main__":
    main()
