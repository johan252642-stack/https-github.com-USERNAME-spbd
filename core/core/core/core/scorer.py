def calculate_score(vulns):
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

    return min(score, 100)
