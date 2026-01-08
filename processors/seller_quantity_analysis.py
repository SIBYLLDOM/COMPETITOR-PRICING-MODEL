# processors/seller_quantity_analysis.py

import pandas as pd


def get_quantity_scaling_factor(
    basic_csv: str,
    filtered_financial_csv: str,
    user_quantity: int
) -> float:
    """
    Computes a GLOBAL quantity scaling factor.
    Uses linear scaling from available quantity & price data.
    RETURNS a multiplier (not stored anywhere).
    """

    basic_df = pd.read_csv(basic_csv, low_memory=False)
    fin_df = pd.read_csv(filtered_financial_csv, low_memory=False)

    # Normalize bid_no
    basic_df["bid_no"] = basic_df["bid_no"].astype(str)
    fin_df["bid_no"] = fin_df["bid_no"].astype(str)

    # Quantity lookup
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
        # No quantity data available → neutral scaling
        return 1.0

    # Compute unit prices
    merged["unit_price"] = merged["Total Price"] / merged["quantity"]

    # Estimate expected price for user quantity
    merged["expected_price"] = merged["unit_price"] * user_quantity

    # Compare against original prices
    scaling_factors = merged["expected_price"] / merged["Total Price"]

    # Return median factor (robust, audit-safe)
    return round(scaling_factors.median(), 3)
