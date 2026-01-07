#!/usr/bin/env python3
"""
FAST GROUP-BASED GPT PRODUCT NORMALIZER
--------------------------------------
• Uses GPT ONLY for ambiguous product groups
• Deterministic pre-grouping
• Very fast (seconds)
• Safe for large tender datasets
"""

from openai import OpenAI
import pandas as pd
import re
import json
import sys
import os
from dotenv import load_dotenv

# ================= CONFIG =================
MODEL = "gpt-4.1-nano"
INPUT_CSV = "data/processed/product_items_raw.csv"
OUTPUT_CSV = "data/processed/product_items.csv"

# ================= INIT =================
load_dotenv()
client = OpenAI()

if not os.path.exists(INPUT_CSV):
    print(f"❌ Missing file: {INPUT_CSV}")
    sys.exit(1)

# ================= LOAD DATA =================
df = pd.read_csv(INPUT_CSV)
products = df["raw_product"].dropna().astype(str).tolist()

print(f"⚡ Processing {len(products)} normalized products")

# ================= SIMPLIFICATION LOGIC =================
def simplify(name: str) -> str:
    """
    Aggressive but safe simplification to form real groups.
    This step is CRITICAL to reduce GPT calls.
    """
    name = name.upper()

    # Remove anything inside brackets
    name = re.sub(r"\(.*?\)", "", name)

    # Remove numbers (pack sizes, versions, quantities)
    name = re.sub(r"\b\d+(\.\d+)?\b", "", name)

    # Remove common packaging / unit words
    name = re.sub(
        r"\b(PACK|PCS|NOS|NO|UNIT|UNITS|SET|SETS|BOX|BOTTLE|VIAL|ML|MG|GM|KG)\b",
        "",
        name
    )

    # Normalize spaces
    name = re.sub(r"\s+", " ", name).strip()

    return name

# ================= GROUP PRODUCTS =================
groups = {}

for product in products:
    key = simplify(product)
    groups.setdefault(key, []).append(product)

print(f"📦 Groups formed: {len(groups)}")

# ================= CANONICALIZATION =================
canonical_products = set()
gpt_groups_used = 0

for key, variants in groups.items():
    # If only one variant → already canonical
    if len(variants) == 1:
        canonical_products.add(variants[0])
        continue

    # GPT only for true ambiguity
    gpt_groups_used += 1
    print(f"🧠 GPT resolving group {gpt_groups_used} | Variants: {variants}")

    response = client.responses.create(
        model=MODEL,
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "You are a government tender product normalization engine.\n"
                            "From the given list of product name variants, choose ONE\n"
                            "canonical product name.\n\n"
                            "RULES:\n"
                            "- Ignore packaging, quantities, versions\n"
                            "- Ignore abbreviations if full form exists\n"
                            "- Do NOT invent new names\n"
                            "- Return ONLY the canonical product name\n"
                            "- No explanations, no JSON, no markdown"
                        )
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": json.dumps(variants)
                    }
                ]
            }
        ]
    )

    canonical = response.output_text.strip().upper()
    canonical_products.add(canonical)

# ================= SAVE FINAL OUTPUT =================
final_df = pd.DataFrame(
    sorted(canonical_products),
    columns=["product_item"]
)

final_df.to_csv(OUTPUT_CSV, index=False)

print("\n✅ product_items.csv generated")
print(f"📄 Canonical products count: {len(final_df)}")
print(f"🧠 GPT used for {gpt_groups_used} ambiguous groups")
print(f"➡ Output file: {OUTPUT_CSV}")
