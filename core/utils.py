import requests

def get(url, session=None):
    try:
        s = session or requests
        return s.get(url, timeout=5)
    except:
        return None
