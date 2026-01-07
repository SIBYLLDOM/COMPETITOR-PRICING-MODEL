# processors/fast_canonicalizer.py

import pandas as pd
from processors.product_fingerprint import fingerprint

def fast_canonicalize(input_csv, output_csv):
    df = pd.read_csv(input_csv)

    groups = {}

    for product in df["raw_product"]:
        key = fingerprint(product)

        # Skip empty fingerprints
        if not key:
            continue

        groups.setdefault(key, []).append(str(product).upper().strip())

    canonical = []

    for variants in groups.values():
        # Choose longest & most descriptive variant
        best = max(variants, key=len)
        canonical.append(best)

    out = pd.DataFrame(
        sorted(set(canonical)),
        columns=["product_item"]
    )

    out.to_csv(output_csv, index=False)

    print("⚡ FAST canonicalization complete")
    print(f"📄 Canonical products: {len(out)}")

    return out
