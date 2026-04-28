import json, requests, sys
from urllib.parse import urlparse, parse_qs
from concurrent.futures import ThreadPoolExecutor

from ai import analyze, payload_for
from ai_elite import analyze_target

from core.crawler import crawl
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
        pdata = payload_for(param)

        for payload in pdata["all"]:
            try:
                test_url = url.replace(f"{param}=", f"{param}={payload}")
                res = requests.get(test_url, timeout=5).text

                ai = analyze(base, res, param, payload, pdata["type"])

                if ai:
                    print(f"[!] {ai['type']} → {param}")
                    vulns.append(ai)
                    break

            except:
                pass

    return vulns


def main():
    target = input("Target: ")

    print("[+] Crawling...")
    urls = crawl(target)

    all_vulns = []

    def worker(u):
        all_vulns.extend(scan_url(u))

    with ThreadPoolExecutor(max_workers=5) as exe:
        exe.map(worker, urls)

    waf = detect_waf(target)
    exploits = auto_exploit(target, all_vulns)
    score = calculate_score(all_vulns)
    analysis = analyze_target(target, all_vulns)

    data = {
        "target": target,
        "urls": urls,
        "vulns": all_vulns,
        "exploits": exploits,
        "waf": waf,
        "risk_score": score,
        "analysis": analysis
    }

    json.dump(data, open("session.json","w"), indent=2)

    print("\n[✓] DONE")
    print("Run dashboard: python3 spbd.py --web")


if __name__ == "__main__":
    if "--web" in sys.argv:
        app.run(port=5000)
    else:
        main()
