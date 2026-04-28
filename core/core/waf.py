def detect_waf(response):
    waf_signatures = [
        "cloudflare",
        "sucuri",
        "akamai",
        "incapsula"
    ]

    for w in waf_signatures:
        if w in response.lower():
            return w

    return None


def bypass_payload(payload):
    # simple bypass
    return payload.replace(" ", "/**/")
