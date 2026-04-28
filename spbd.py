import json, requests, sys, time
from urllib.parse import urlparse, parse_qs
from concurrent.futures import ThreadPoolExecutor

from ai import analyze, payload_for
from ai_elite import analyze_target

from core.crawler import crawl
from core.exploiter import auto_exploit
from core.waf import detect_waf
from core.scorer import calculate_score
from web.dashboard import app


def inject(url, payload):
    p = urlparse(url)
    qs = parse_qs(p.query)

    if not qs:
        return url + "?test=" + payload

    for k in qs:
        qs[k] = payload

    query = "&".join(f"{k}={v}" for k,v in qs.items())
    return f"{p.scheme}://{p.netloc}{p.path}?{query}"


def scan(url):
    vulns = []

    try:
        base = requests.get(url, timeout=5).text
    except:
        return vulns

    params = parse_qs(urlparse(url).query)
    if not params:
        params = {"test":["1"]}

    for param in params:
        for payload in payload_for(param)["all"]:
            try:
                u = inject(url, payload)
                res = requests.get(u, timeout=5).text

                ai = analyze(base, res, param, payload, "auto")

                if ai:
                    print(f"[{ai['severity']}] {param}")
                    vulns.append(ai)
                    break

                time.sleep(0.3)

            except:
                pass

    return vulns


def main():
    target = input("Target: ")

    print("[+] Crawling...")
    urls = crawl(target)

    all_vulns = []

    def worker(u):
        all_vulns.extend(scan(u))

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
