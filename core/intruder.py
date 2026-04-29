from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from core.utils import get

PAYLOADS = ["' OR 1=1 --", "../../etc/passwd"]

def inject(url, param, payload):
    p = urlparse(url)
    qs = parse_qs(p.query)
    qs[param] = payload
    return urlunparse(p._replace(query=urlencode(qs, doseq=True)))

def intruder_scan(url, session=None):
    results = []

    parsed = urlparse(url)
    if not parsed.query:
        return results

    base = get(url, session)
    if not base:
        return results

    base_len = len(base.text)

    for param in parse_qs(parsed.query):
        for payload in PAYLOADS:
            r = get(inject(url, param, payload), session)

            if not r:
                continue

            if abs(len(r.text) - base_len) > 50:
                results.append({
                    "type": "Intruder Hit",
                    "param": param,
                    "payload": payload,
                    "status": r.status_code
                })

    return results
