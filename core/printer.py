RESULTS = {
    "SQLi": set(),
    "XSS": set(),
    "HEADERS": set()
}

SEEN = set()


def is_duplicate(v):
    key = (v.get("type"), v.get("param"), v.get("detail"))
    if key in SEEN:
        return True
    SEEN.add(key)
    return False


def process_vuln(v):
    if is_duplicate(v):
        return

    t = v.get("type", "")
    param = v.get("param")
    detail = v.get("detail")

    if "SQLi Validated" in t:
        RESULTS["SQLi"].add(param)

    elif "XSS Validated" in t:
        RESULTS["XSS"].add(param)

    elif "Header Missing" in t:
        RESULTS["HEADERS"].add(detail)


def print_clean():
    print("\n🔥 SPBD RESULT 🔥\n")

    if RESULTS["SQLi"]:
        print(f"[MEDIUM] SQL Injection → {', '.join(RESULTS['SQLi'])}")

    if RESULTS["XSS"]:
        print(f"[MEDIUM] XSS → {', '.join(RESULTS['XSS'])}")

    if RESULTS["HEADERS"]:
        print(f"[LOW] Missing headers → {', '.join(RESULTS['HEADERS'])}")

    print("\n=== SUMMARY ===")
    print(f"SQLi: {len(RESULTS['SQLi'])}")
    print(f"XSS: {len(RESULTS['XSS'])}")
    print(f"Headers: {len(RESULTS['HEADERS'])}")
