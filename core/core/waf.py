import requests

def detect_waf(url):
    try:
        r = requests.get(url, timeout=5)
        h = str(r.headers).lower()

        if "cloudflare" in h:
            return "Cloudflare"
        if "sucuri" in h:
            return "Sucuri"
        if "akamai" in h:
            return "Akamai"

    except:
        pass

    return "Unknown"
