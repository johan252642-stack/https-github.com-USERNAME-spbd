def analyze(base, response, param, payload, vtype):
    score = 0
    reason = []

    if payload in response:
        score += 50
        reason.append("reflected payload")

    errors = ["sql", "syntax", "mysql", "warning", "ORA-"]
    if any(e in response.lower() for e in errors):
        score += 40
        reason.append("sql error detected")

    if "root:x:" in response or "/bin/bash" in response:
        score += 60
        reason.append("sensitive file exposed")

    if "127.0.0.1" in response or "localhost" in response:
        score += 50
        reason.append("internal service response")

    if len(response) != len(base):
        score += 10

    if score >= 40:
        return {
            "type": vtype,
            "param": param,
            "payload": payload,
            "confidence": score,
            "severity": "Critical" if score >= 80 else "High" if score >= 60 else "Medium",
            "reason": ", ".join(reason)
        }

    return None


def payload_for(param):
    return {
        "type": "auto",
        "all": [
            "1 OR 1=1",
            "'--",
            "<script>alert(1)</script>",
            "../../etc/passwd",
            "http://127.0.0.1",
            "test123"
        ]
    }
