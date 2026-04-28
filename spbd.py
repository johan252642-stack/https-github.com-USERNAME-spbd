import json
import requests
from urllib.parse import urlparse, parse_qs
from concurrent.futures import ThreadPoolExecutor

from core.crawler import crawl
from core.detector import detect_vuln
from core.exploiter import auto_exploit
from core.waf import detect_waf
from core.scorer import calculate_score
from web.dashboard import app


def scan_url(url):
    vulns = []

    if "?" not in url:
        return vulns

    try:
        base = requests.get(url, timeout=5).text
    except:
        return vulns

    for param in parse_qs(urlparse(url).query):
        try:
            test_url = url.replace(f"{param}=", f"{param}=test123")
            res = requests.get(test_url, timeout=5).text

            detected = detect_vuln(base, res)

            for d in detected:
                vulns.append({
                    "type": d,
                    "param": param
                })
        except:
            pass

    return vulns


def main():
    target = input("Target: ")

    print("[+] Crawling...")
    urls = crawl(target)

    print(f"[+] Found {len(urls)} URLs")

    all_vulns = []

    def worker(u):
        v = scan_url(u)
        all_vulns.extend(v)

    with ThreadPoolExecutor(max_workers=5) as exe:
        exe.map(worker, urls)

    print("[+] Detecting WAF...")
    waf = detect_waf(target)

    print("[+] Exploiting...")
    exploits = auto_exploit(target, all_vulns)

    score = calculate_score(all_vulns)

    data = {
        "target": target,
        "urls": urls,
        "vulns": all_vulns,
        "exploits": exploits,
        "waf": waf,
        "risk_score": score
    }

    json.dump(data, open("session.json","w"), indent=2)

    print("\n[✓] DONE")
    print(f"Risk Score: {score}/100")
    print("Run dashboard: python3 spbd.py --web")


if __name__ == "__main__":
    import sys

    if "--web" in sys.argv:
        app.run(port=5000)
    else:
        main()
