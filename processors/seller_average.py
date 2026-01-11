# processors/seller_average.py

import pandas as pd
from utils.price_cleaner import clean_price

def generate_seller_average(input_csv, output_csv):
    """
    🔥 L1-SPECIFIC LEARNING:
    - Uses BOTTOM 10th PERCENTILE instead of average
    - Focuses on L1-winning bid patterns
    - Ignores high-value/catalog prices
    
    CRITICAL: All prices here are TOTAL CONTRACT prices.
    """
    df = pd.read_csv(input_csv)
    df.columns = df.columns.str.strip()

    df["clean_price"] = df["Total Price"].apply(clean_price)
    df = df[df["clean_price"].notna()]

    # 🔑 L1 LOGIC: Use 10th percentile (bottom 10%) instead of mean
    # This captures L1-winning bid behavior
    l1_percentile_df = (
        df.groupby("Seller Name", as_index=False)["clean_price"]
        .quantile(0.10)  # Bottom 10% = L1-adjacent pricing
        .rename(columns={"clean_price": "average"})
    )

    meta_df = (
        df.groupby("Seller Name", as_index=False)
        .first()[["S.No.", "bid_no", "Seller Name"]]
    )

    result = meta_df.merge(l1_percentile_df, on="Seller Name")
    
    try:
        result.to_csv(output_csv, index=False)
    except PermissionError:
        print(f"\n❌ PERMISSION ERROR: Cannot write to {output_csv}")
        print("   Please close Excel or any program that has this file open.")
        raise
    except Exception as e:
        print(f"\n❌ ERROR saving {output_csv}: {e}")
        raise

    print(f"✅ L1-specific pricing generated using 10th percentile (not average)")
    return result

