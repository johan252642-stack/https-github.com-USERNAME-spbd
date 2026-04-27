def analyze_target(url, vulns):
    score = 0
    chain = []

    for v in vulns:
        if v["severity"] == "CRITICAL":
            score += 5
            chain.append("Critical exploit possible")
        elif v["severity"] == "HIGH":
            score += 3
            chain.append("High risk vulnerability")
        elif v["severity"] == "MEDIUM":
            score += 2
        else:
            score += 1

    # level score
    if score >= 10:
        level = "🔥 CRITICAL"
    elif score >= 6:
        level = "⚠ HIGH"
    elif score >= 3:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "score": {
            "value": score,
            "level": level
        },
        "chain": chain
    }
