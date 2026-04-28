import json
from urllib.parse import urlparse, parse_qs
from core.exploiter import auto_exploit
from web.dashboard import app


def scan(url):
    vulns = []

    if "?" not in url:
        return vulns

    for param in parse_qs(urlparse(url).query):
        print(f"[TEST] {param}")

        # dummy detection (ganti dengan AI kamu)
        vulns.append({
            "type": "xss",
            "param": param
        })

    return vulns


def main():
    target = input("Target: ")

    all_vulns = scan(target)

    exploits = auto_exploit(target, all_vulns)

    data = {
        "target": target,
        "vulns": all_vulns,
        "exploits": exploits,
        "analysis": {}
    }

    json.dump(data, open("session.json", "w"), indent=2)

    print("[✓] Scan selesai")
    print("[+] Jalankan dashboard: python3 spbd.py --web")


if __name__ == "__main__":
    import sys

    if "--web" in sys.argv:
        app.run(port=5000)
    else:
        main()
