from core.utils import get

PATHS = ["/admin", "/login", "/api", "/.env"]

def recon_scan(base):
    results = []

    for p in PATHS:
        url = base.rstrip("/") + p
        r = get(url)

        if r and r.status_code in [200, 403]:
            results.append({
                "type": "Recon",
                "url": url,
                "status": r.status_code
            })

    return results
