from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from ai import analyze
from core.payloads import get_payloads
from core.waf import detect_waf, bypass_payload
from core.proxy import session


def inject(url, param, payload):
    p = urlparse(url)
    qs = parse_qs(p.query)
    qs[param] = payload

    new_url = urlunparse(p._replace(query=urlencode(qs, doseq=True)))
    return session.get(new_url, timeout=5).text


def scan(url):
    vulns = []

    try:
        base = session.get(url, timeout=5).text
    except:
        return vulns

    waf = detect_waf(base)
    if waf:
        print(f"[!] WAF Detected: {waf}")

    if "?" not in url:
        return vulns

    for param in parse_qs(urlparse(url).query):

        for vuln_type in ["sqli", "xss", "lfi", "ssrf"]:
            payloads = get_payloads(vuln_type)

            for payload in payloads:
                if waf:
                    payload = bypass_payload(payload)

                print(f"[TEST] {param} → {payload}")

                try:
                    res = inject(url, param, payload)
                except:
                    continue

                ai = analyze(base, res, param, payload, vuln_type)

                if ai:
                    print(f"[VULN] {param} → {ai['reason']}")
                    vulns.append(ai)
                    break

    return vulns
