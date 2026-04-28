def score_vuln(v):
    score_map = {
        "CRITICAL": 100,
        "HIGH": 70,
        "MEDIUM": 40,
        "LOW": 10
    }

    base = score_map.get(v["severity"], 0)

    if "SQL" in v["type"]:
        base += 20
    if "XSS" in v["type"]:
        base += 10

    return base

def sort_vulns(vulns):
    return sorted(vulns, key=score_vuln, reverse=True)
