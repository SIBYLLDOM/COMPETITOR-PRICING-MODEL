# utils/price_cleaner.py

import pandas as pd
import re

def clean_price(value):
    if pd.isna(value):
        return None

    value = str(value)

    value = (
        value.replace("`", "")
        .replace("₹", "")
        .replace("INR", "")
        .replace(",", "")
        .strip()
    )

    match = re.search(r"\d+(\.\d+)?", value)
    if not match:
        return None

    return float(match.group())
