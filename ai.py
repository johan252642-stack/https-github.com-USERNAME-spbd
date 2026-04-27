import re

def payload_for(param):
    p = param.lower()

    if "id" in p or "user" in p:
        return {
            "type": "SQLi",
            "all": ["' OR 1=1--", "' OR 'a'='a"]
        }

    if "q" in p or "search" in p:
        return {
            "type": "XSS",
            "all": ["<script>alert(1)</script>"]
        }

    return {
        "type": "Generic",
        "all": ["test123"]
    }


def analyze(base, injected, param, payload, typ):
    if not base or not injected:
        return None

    diff = abs(len(base) - len(injected))

    # error detection
    errors = ["sql", "mysql", "error", "warning", "syntax"]

    err_flag = any(e in injected.lower() for e in errors)

    if diff > 50 or err_flag:
        return {
            "type": typ,
            "param": param,
            "severity": "HIGH" if err_flag else "MEDIUM",
            "reason": "Response anomaly detected"
        }

    return None
