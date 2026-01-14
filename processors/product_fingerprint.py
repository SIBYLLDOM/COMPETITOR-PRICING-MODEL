# processors/product_fingerprint.py

import re

STOPWORDS = {
    "PACK", "PCS", "NOS", "NO", "UNIT", "UNITS",
    "SET", "SETS", "BOX", "BOTTLE", "VIAL",
    "ML", "MG", "GM", "KG", "OF", "AND", "WITH"
}

def normalize_word(word: str) -> str:
    """
    Normalize a word by converting common plurals to singular.
    This helps match 'CLIP' with 'CLIPS', 'KIT' with 'KITS', etc.
    """
    if len(word) <= 3:
        return word
    
    # Simple plural removal (handles most medical/surgical terms)
    if word.endswith('S') and not word.endswith('SS'):
        # Don't singularize words ending in double S (GLASS, PASS)
        return word[:-1]
    
    return word

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
        normalize_word(t) for t in tokens
        if t and t not in STOPWORDS and len(t) > 2
    ]
    
    clean_tokens.sort()
    
    return " ".join(clean_tokens)
