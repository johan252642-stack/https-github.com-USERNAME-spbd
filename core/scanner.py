from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from core.ai_engine import ai_score
from core.utils import get

PAYLOADS = ["' OR 1=1 --", "<script>alert(1)</script>"]

def inject(url, param, payload):
    p = urlparse(url)
    qs = parse_qs(p.query)
    qs[param] = payload
    return urlunparse(p._replace(query=urlencode(qs, doseq=True)))

def scan_target(url, session=None):
    results = []

    parsed = urlparse(url)

    for param in parse_qs(parsed.query):
        for payload in PAYLOADS:
            test = inject(url, param, payload)
            r = get(test, session)

            if not r:
                continue

            score = ai_score(r.text)

            if score > 2:
                results.append({
                    "type": "AI Suspicious",
                    "param": param,
                    "payload": payload,
                    "score": score
                })

    return results
