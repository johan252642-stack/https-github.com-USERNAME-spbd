import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def crawl(url):
    urls = set()

    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")

        for a in soup.find_all("a", href=True):
            full = urljoin(url, a["href"])
            if "?" in full:
                urls.add(full)
    except:
        pass

    for p in ["id","page","q","search"]:
        urls.add(url + f"?{p}=1")

    return list(urls)
