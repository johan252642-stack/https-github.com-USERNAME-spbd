#!/usr/bin/env python3
import re, json, os, random, html

MEMORY_FILE = "ai_memory.json"

# =========================
# MEMORY SYSTEM
# =========================
def load_memory():
    if os.path.exists(MEMORY_FILE):
        return json.load(open(MEMORY_FILE))
    return {}

def save_memory(mem):
    with open(MEMORY_FILE, "w") as f:
        json.dump(mem, f, indent=2)

def learn(param, payload):
    mem = load_memory()
    mem.setdefault(param, [])
    if payload not in mem[param]:
        mem[param].append(payload)
    save_memory(mem)

# =========================
# PAYLOAD BASE
# =========================
SQLI = ["' OR 1=1--", "' UNION SELECT NULL--"]
XSS = ["<script>alert(1)</script>", "<img src=x onerror=alert(1)>"]
LFI = ["../../../../etc/passwd"]
GENERIC = ["test123"]

# =========================
# PAYLOAD MUTATION
# =========================
def mutate(payload):
    return list(set([
        payload,
        html.escape(payload),
        payload.replace(" ", "/**/"),
        payload.upper()
    ]))

# =========================
# PAYLOAD SELECTOR
# =========================
def payload_for(param):
    p = param.lower()
    mem = load_memory()

    if "id" in p or "user" in p:
        base, t = SQLI, "SQLi"
    elif "q" in p or "search" in p:
        base, t = XSS, "XSS"
    elif "file" in p:
        base, t = LFI, "LFI"
    else:
        base, t = GENERIC, "Generic"

    payloads = base + mem.get(param, [])
    final = []

    for p in payloads:
        final.extend(mutate(p))

    return {
        "payload": random.choice(final),
        "all": final,
        "type": t
    }

# =========================
# CONTEXT DETECTION
# =========================
def detect_context(resp):
    r = resp.lower()
    if r.strip().startswith("{"):
        return "json"
    if "<html" in r:
        return "html"
    return "text"

# =========================
# PATTERN DETECTION
# =========================
def detect_patterns(resp):
    r = resp.lower()

    return {
        "sqli": any(x in r for x in ["sql syntax","mysql","database error"]),
        "xss": any(x in r for x in ["<script>","onerror="]),
        "lfi": any(x in r for x in ["root:x:","boot loader"]),
        "waf": any(x in r for x in ["access denied","forbidden","blocked"])
    }

# =========================
# STRUCTURAL DIFFERENCE
# =========================
def structure_diff(a, b):
    tags_a = len(re.findall("<", a))
    tags_b = len(re.findall("<", b))
    return abs(tags_a - tags_b) / max(tags_a,1)

# =========================
# SIMILARITY
# =========================
def similarity(a, b):
    same = sum(1 for x,y in zip(a,b) if x==y)
    return same / max(len(a),1)

# =========================
# CORE ANALYSIS
# =========================
def analyze_response(base, injected):
    if not base or not injected:
        return 0

    sim = similarity(base, injected)
    diff = abs(len(base)-len(injected)) / max(len(base),1)
    struct = structure_diff(base, injected)
    ctx = detect_context(injected)
    patt = detect_patterns(injected)

    score = 0

    # pattern boost
    if patt["sqli"]: score += 0.6
    if patt["xss"]: score += 0.6
    if patt["lfi"]: score += 0.6

    # anomaly
    score += (1 - sim) * 0.4
    score += diff * 0.2
    score += struct * 0.2

    # context tweak
    if ctx == "html": score += 0.1
    if ctx == "json": score += 0.05

    # waf penalty
    if patt["waf"]: score -= 0.3

    return max(0, min(score,1))

# =========================
# DEDUPLICATION
# =========================
def is_duplicate(prev, current):
    return similarity(prev, current) > 0.95

# =========================
# EXPLAIN ENGINE
# =========================
def explain(data):
    score = data["score"]

    if score > 0.8:
        sev = "CRITICAL"
    elif score > 0.6:
        sev = "HIGH"
    elif score > 0.4:
        sev = "MEDIUM"
    else:
        sev = "LOW"

    reasons = {
        "SQLi": "Database behavior anomaly detected",
        "XSS": "Reflected script detected",
        "LFI": "File disclosure pattern detected",
        "Generic": "Unusual response difference"
    }

    return {
        "type": data["type"],
        "param": data["param"],
        "severity": sev,
        "confidence": round(score,2),
        "reason": reasons.get(data["type"])
    }

# =========================
# FINAL PIPELINE
# =========================
def analyze(base, injected, param, payload, ptype, history=None):
    if history and is_duplicate(history, injected):
        return None

    score = analyze_response(base, injected)

    if score < 0.35:
        return None

    learn(param, payload)

    return explain({
        "type": ptype,
        "param": param,
        "score": score
    })
