import re
from core.utils import get
from urllib.parse import urljoin

def crawl_js(url):
    results = []

    r = get(url)
    if not r:
        return results

    js = re.findall(r'src=["\'](.*?\.js)', r.text)

    for j in js:
        full = urljoin(url, j)
        r2 = get(full)

        if not r2:
            continue

        eps = re.findall(r'["\'](/api/.*?)["\']', r2.text)

        for e in eps:
            results.append({"url": urljoin(url, e)})

    return results
