from core.utils import get

HEADERS = ["X-Frame-Options", "Content-Security-Policy"]

def check_headers(url):
    issues = []

    r = get(url)
    if not r:
        return issues

    for h in HEADERS:
        if h not in r.headers:
            issues.append({
                "type": "Header Missing",
                "detail": h
            })

    return issues
