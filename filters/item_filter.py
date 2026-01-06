# filters/item_filter.py

import pandas as pd
from config.columns import OFFERED_ITEM_COLUMN

def clean_item(value):
    if pd.isna(value):
        return ""
    return (
        str(value)
        .replace("Item Categories :", "")
        .strip()
        .lower()
    )

def filter_by_item(df: pd.DataFrame, item_category: str) -> pd.DataFrame:
    item_category = item_category.strip().lower()

    df["__clean_item"] = df[OFFERED_ITEM_COLUMN].apply(clean_item)

    result = df[df["__clean_item"] == item_category].copy()

    result.drop(columns=["__clean_item"], inplace=True)

    return result
