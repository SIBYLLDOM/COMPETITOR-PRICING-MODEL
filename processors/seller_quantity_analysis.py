# processors/seller_quantity_analysis.py

import pandas as pd


def get_quantity_scaling_factor(
    basic_csv: str,
    filtered_financial_csv: str,
    user_quantity: int
) -> float:
    """
    ⚠️ CRITICAL: filtered_company.csv contains TOTAL CONTRACT PRICES.
    
    HARD RULES:
    - NEVER divide prices by quantity
    - Quantity is for CONTEXT ONLY (to find similar tender sizes)
    - Prices in CSV are NOT unit prices
    
    This function now returns a contextual weight factor based on
    quantity similarity, NOT a price rescaling factor.
    
    RETURNS: Always 1.0 (neutral) - prices should NOT be rescaled.
    """

    # Read CSVs with error handling for malformed rows
    basic_df = pd.read_csv(
        basic_csv, 
        low_memory=False,
        on_bad_lines='skip',
        encoding='latin-1',
        quoting=1,
        escapechar='\\'
    )
    fin_df = pd.read_csv(
        filtered_financial_csv, 
        low_memory=False,
        on_bad_lines='skip',
        encoding='latin-1',
        quoting=1,
        escapechar='\\'
    )

    # Normalize bid_no
    basic_df["bid_no"] = basic_df["bid_no"].astype(str)
    fin_df["bid_no"] = fin_df["bid_no"].astype(str)

    # Quantity lookup (for context/filtering only)
    qty_df = basic_df[["bid_no", "quantity"]].dropna().copy()
    qty_df["quantity"] = (
        qty_df["quantity"]
        .astype(str)
        .str.extract(r"(\d+\.?\d*)")[0]
        .astype(float)
    )
    qty_df = qty_df[qty_df["quantity"] > 0]

    # Price lookup
    price_df = fin_df[["bid_no", "Total Price"]].dropna().copy()
    price_df["Total Price"] = pd.to_numeric(
        price_df["Total Price"], errors="coerce"
    )
    price_df = price_df.dropna()

    merged = qty_df.merge(price_df, on="bid_no", how="inner")

    if merged.empty:
        print("⚠️ No quantity+price data available → using neutral factor")
        return 1.0

    # 🔥 NEW LOGIC: Use quantity for CONTEXT, not rescaling
    # Filter tenders with similar quantity range (±50% of user quantity)
    qty_lower = user_quantity * 0.5
    qty_upper = user_quantity * 1.5
    
    similar_qty = merged[
        (merged["quantity"] >= qty_lower) & 
        (merged["quantity"] <= qty_upper)
    ]
    
    if not similar_qty.empty:
        print(f"✅ Found {len(similar_qty)} tenders with similar quantity context")
    else:
        print(f"⚠️ No tenders in quantity range [{qty_lower}-{qty_upper}]")

    # 🔑 CRITICAL: Return 1.0 (neutral factor)
    # Prices in filtered_company.csv are TOTAL CONTRACT prices
    # They should NOT be rescaled by quantity
    return 1.0
