# processors/product_fingerprint.py

import re

STOPWORDS = {
    "PACK", "PCS", "NOS", "NO", "UNIT", "UNITS",
    "SET", "SETS", "BOX", "BOTTLE", "VIAL",
    "ML", "MG", "GM", "KG", "OF", "AND", "WITH"
}

def fingerprint(name) -> str:
    if name is None:
        return ""

    name = str(name).strip()
    if not name or name.lower() == "nan":
        return ""

    name = name.upper()

    name = re.sub(r"\(.*?\)", "", name)
    name = re.sub(r"\b\d+(\.\d+)?\b", "", name)

    tokens = re.split(r"[\s,/]+", name)

    clean_tokens = [
        t for t in tokens
        if t and t not in STOPWORDS and len(t) > 2
    ]

    clean_tokens.sort()

    return " ".join(clean_tokens)
