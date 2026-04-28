def detect_vuln(base, response):
    vulns = []

    if base != response:
        if "<script>" in response:
            vulns.append("xss")

        if "sql" in response.lower():
            vulns.append("sqli")

        if "root:x" in response:
            vulns.append("lfi")

        if "127.0.0.1" in response:
            vulns.append("ssrf")

    return vulns
