def validate_sqli(r1, r2):
    if not r1 or not r2:
        return False

    # beda panjang response
    if abs(len(r1.text) - len(r2.text)) > 50:
        return True

    # error database
    errors = ["sql", "mysql", "syntax", "warning"]
    for e in errors:
        if e in r2.text.lower():
            return True

    return False


def validate_xss(response, payload):
    if not response:
        return False

    return payload in response.text
