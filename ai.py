import re

def analyze(base, response, param, payload, vuln_type):
    if base == response:
        return None

    confidence = 0
    reason = []

    if payload in response:
        confidence += 50
        reason.append("Payload reflected")

    if "sql" in response.lower():
        confidence += 40
        reason.append("SQL error detected")

    if "root:x:" in response:
        confidence += 60
        reason.append("Sensitive file exposed")

    if "127.0.0.1" in response:
        confidence += 50
        reason.append("Internal response")

    if confidence >= 40:
        return {
            "type": vuln_type,
            "param": param,
            "payload": payload,
            "confidence": confidence,
            "severity": "High" if confidence >= 60 else "Medium",
            "reason": ", ".join(reason)
        }

    return None


def payload_for(param):
    p = param.lower()

    if "id" in p:
        return {"type": "sqli", "all": ["1 OR 1=1", "'--"]}

    if "search" in p or "q" in p:
        return {"type": "xss", "all": ["<script>alert(1)</script>"]}

    if "file" in p:
        return {"type": "lfi", "all": ["../../etc/passwd"]}

    if "url" in p:
        return {"type": "ssrf", "all": ["http://127.0.0.1"]}

    return {"type": "generic", "all": ["test123"]}
