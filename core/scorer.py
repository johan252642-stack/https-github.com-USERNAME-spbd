def calculate_score(vulns):
    score = 0

    for v in vulns:
        if v["severity"] == "Critical":
            score += 70
        elif v["severity"] == "High":
            score += 50
        elif v["severity"] == "Medium":
            score += 30

    return min(score, 100)
