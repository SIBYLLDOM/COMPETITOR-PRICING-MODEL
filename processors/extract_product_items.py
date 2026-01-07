# processors/extract_product_items.py

import pandas as pd
import re


def singularize_word(word: str) -> str:
    """
    Safely convert plural to singular for tender product words.
    Conservative rules to avoid meaning damage.
    """

    # Do not touch very short words
    if len(word) < 4:
        return word

    # Avoid breaking words like GLASS, CLASS, BOSS, VIRUS
    if word.endswith(("SS", "US", "IS")):
        return word

    # IES -> Y  (BATTERIES -> BATTERY)
    if word.endswith("IES"):
        return word[:-3] + "Y"

    # ES -> remove ES (INJECTIONS -> INJECTION)
    if word.endswith("ES"):
        return word[:-2]

    # Simple plural S
    if word.endswith("S"):
        return word[:-1]

    return word


def normalize_for_raw(name: str) -> str:
    """
    Fast, deterministic, future-proof normalization.
    NO GPT.
    """

    name = name.upper().strip()

    # Remove version markers like (V2), (V10)
    name = re.sub(r"\(V\d+\)", "", name)

    # Remove extra spaces
    name = re.sub(r"\s+", " ", name).strip()

    words = name.split(" ")
    words = [singularize_word(word) for word in words]

    return " ".join(words)


def extract_raw_product_items(input_csv: str, output_csv: str):
    """
    Generates a CLEAN, DE-DUPLICATED product_items_raw.csv
    """

    df = pd.read_csv(input_csv, on_bad_lines="skip", low_memory=False)
    df.columns = df.columns.str.strip()

    if "Offered Item" not in df.columns:
        raise ValueError("❌ 'Offered Item' column not found")

    unique_products = set()

    for value in df["Offered Item"].dropna():
        clean_value = str(value).replace("Item Categories :", "").strip()

        for item in clean_value.split(","):
            item = item.strip()
            if not item:
                continue

            normalized = normalize_for_raw(item)
            unique_products.add(normalized)

    out_df = pd.DataFrame(
        sorted(unique_products),
        columns=["raw_product"]
    )

    out_df.to_csv(output_csv, index=False)

    print(f"📄 Unique normalized raw products: {len(out_df)}")

    return out_df
