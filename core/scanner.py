import requests, time
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

PAYLOADS = {
    "SQL Injection": ["' OR 1=1 --", "' OR SLEEP(5)--"],
    "XSS": ["<script>alert(1)</script>"],
}

def inject(url, param, payload):
    p = urlparse(url)
    qs = parse_qs(p.query)
    qs[param] = payload
    return urlunparse(p._replace(query=urlencode(qs, doseq=True)))

def scan_target(url):
    results = []

    try:
        requests.get(url, timeout=5)
    except:
        return results

    parsed = urlparse(url)
    if not parsed.query:
        return results

    for param in parse_qs(parsed.query):
        for t in PAYLOADS:
            for payload in PAYLOADS[t]:
                try:
                    test = inject(url, param, payload)

                    start = time.time()
                    r = requests.get(test, timeout=5)
                    delay = time.time() - start

                    if "sql" in r.text.lower() or delay > 5:
                        results.append({
                            "type":"SQL Injection",
                            "severity":"CRITICAL",
                            "param":param,
                            "payload":payload
                        })

                    if payload in r.text:
                        results.append({
                            "type":"XSS",
                            "severity":"HIGH",
                            "param":param,
                            "payload":payload
                        })

                except:
                    continue

    return results
