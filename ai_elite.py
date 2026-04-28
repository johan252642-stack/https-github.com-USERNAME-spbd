def analyze_target(url, vulns):
    score = 0

    for v in vulns:
        if v["severity"] == "Critical":
            score += 70
        elif v["severity"] == "High":
            score += 50
        elif v["severity"] == "Medium":
            score += 30

    level = "LOW"
    if score > 50: level = "MEDIUM"
    if score > 100: level = "HIGH"
    if score > 150: level = "CRITICAL"

    return {"score": score, "level": level}
