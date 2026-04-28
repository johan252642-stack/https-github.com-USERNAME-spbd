#!/usr/bin/env python3

from core.crawler import crawl
from core.crawler_adv import crawl_advanced
from core.scanner import scan_target
from core.printer import print_vuln, print_summary
from core.threads import run_threads
from core.scorer import sort_vulns
from core.analyzer import analyze_target
from report import generate_report
from web.dashboard import run, socketio
from colorama import Fore, init
import threading, time

init(autoreset=True)

LIVE = {
    "target":"",
    "vulns":[],
    "stats":{"CRITICAL":0,"HIGH":0,"MEDIUM":0,"LOW":0}
}

def banner():
    print(Fore.RED + r"""
 ███████╗██████╗ ██████╗ 
 ██╔════╝██╔══██╗██╔══██╗
 ███████╗██████╔╝██████╔╝
 ╚════██║██╔═══╝ ██╔══██╗
 ███████║██║     ██████╔╝
 ╚══════╝╚═╝     ╚═════╝ 
""")
    print(Fore.CYAN + "🔥 SPBD ULTIMATE SCANNER 🔥\n")

def main():
    banner()

    mode = input("Mode (cli/web): ")
    level = input("Level (basic/elite/advanced): ")
    url = input("Target: ")

    LIVE["target"] = url

    if mode == "web":
        threading.Thread(target=run, daemon=True).start()
        print("[+] Dashboard: http://127.0.0.1:5000")

    # ===== MODE =====
    if level == "basic":
        targets = crawl(url)

    elif level == "elite":
        targets = crawl(url)

    elif level == "advanced":
        items = crawl_advanced(url)

        print("[+] Analisis target...")
        for i in items:
            a = analyze_target(i)
            print(f"{a['url']} → {a['risk']}")

        targets = [i["url"] for i in items]

    else:
        print("Level tidak valid")
        return

    print(f"\n[+] Total target: {len(targets)}")
    print("[+] Scanning...\n")

    def worker(t):
        print(Fore.CYAN + f"[SCAN] {t}")
        return scan_target(t)

    results = run_threads(targets, worker, max_threads=10)
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
