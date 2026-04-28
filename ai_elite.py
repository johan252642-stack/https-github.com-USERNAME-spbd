def analyze_target(url, vulns):
    score = 0

    for v in vulns:
        if v["type"] == "sqli":
            score += 50
        elif v["type"] == "xss":
            score += 30
        elif v["type"] == "lfi":
            score += 40
        elif v["type"] == "ssrf":
            score += 60

    level = "LOW"
    if score > 50: level = "MEDIUM"
    if score > 100: level = "HIGH"
    if score > 150: level = "CRITICAL"

    return {"score": score, "level": level}
