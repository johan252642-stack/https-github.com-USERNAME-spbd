def analyze(base, new, param, payload, ptype):
    score = 0
    reasons = []

    if base != new:
        score += 2
        reasons.append("Response changed")

    if payload in new:
        score += 3
        reasons.append("Payload reflected")

    errors = ["sql", "syntax", "mysql", "warning"]
    if any(e in new.lower() for e in errors):
        score += 4
        reasons.append("SQL error detected")

    if "root:x" in new:
        score += 5
        reasons.append("LFI detected")

    if score >= 5:
        return {
            "param": param,
            "payload": payload,
            "type": ptype,
            "severity": "CRITICAL" if score >= 7 else "HIGH",
            "score": score,
            "reason": ", ".join(reasons)
        }

    return None
