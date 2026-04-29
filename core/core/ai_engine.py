KEYWORDS = ["sql", "error", "warning", "exception"]

def ai_score(text):
    score = 0
    for k in KEYWORDS:
        if k in text.lower():
            score += 2
    return score
