import requests
from core.validator import validate_sqli, validate_xss

def scan_target(url):
    vulns = []

    payload_sqli = "' OR 1=1 --"
    payload_xss = "<script>alert(1)</script>"

    params = ["q", "search", "id", "user", "page"]

    for p in params:
        try:
            normal = requests.get(url, timeout=5)
            inj = requests.get(f"{url}?{p}={payload_sqli}", timeout=5)

            if validate_sqli(normal, inj):
                vulns.append({
                    "type": "SQLi Validated",
                    "param": p
                })

            rx = requests.get(f"{url}?{p}={payload_xss}", timeout=5)

            if validate_xss(rx, payload_xss):
                vulns.append({
                    "type": "XSS Validated",
                    "param": p
                })

            # header check
            if "Content-Security-Policy" not in rx.headers:
                vulns.append({
                    "type": "Header Missing",
                    "detail": "Content-Security-Policy"
                })

            if "X-Frame-Options" not in rx.headers:
                vulns.append({
                    "type": "Header Missing",
                    "detail": "X-Frame-Options"
                })

        except:
            continue

    return vulns
