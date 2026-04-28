import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

visited = set()

def crawl(url, depth=2):
    urls = []

    if depth == 0 or url in visited:
        return urls

    visited.add(url)
    urls.append(url)

    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")

        for a in soup.find_all("a", href=True):
            link = urljoin(url, a["href"])
            if link.startswith("http"):
                urls += crawl(link, depth-1)
    except:
        pass

    return list(set(urls))
