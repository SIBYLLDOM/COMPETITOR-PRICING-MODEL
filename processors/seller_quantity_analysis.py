# processors/seller_quantity_analysis.py

import pandas as pd
from processors.product_fingerprint import fingerprint


def _detect_bid_column(df):
    """
    Detect bid number column in basic CSV.
    """
    for col in ["bid_no", "Bid No", "Bid Number"]:
        if col in df.columns:
            return col
    raise ValueError(f"Bid number column not found. Columns: {list(df.columns)}")


def enrich_with_quantity_adjusted_price(
    company_check_csv,
    basic_csv,
    user_product,
    user_quantity
):
    """
    Adds quantity_adjusted_price using BID-LEVEL quantity logic.
    """

    company_df = pd.read_csv(company_check_csv)
    basic_df = pd.read_csv(basic_csv, low_memory=False)

    bid_col = _detect_bid_column(basic_df)

    # Fingerprint user products
    user_products = [p.strip() for p in user_product.split(",") if p.strip()]
    user_fps = {fingerprint(p) for p in user_products if fingerprint(p)}

    adjusted_prices = []

    for _, row in company_df.iterrows():
        bid_no = row["bid_no"]

        bid_rows = basic_df[
            (basic_df[bid_col] == bid_no)
            & (basic_df["quantity"].notna())
        ]

        if bid_rows.empty:
            adjusted_prices.append(None)
            continue

        matched_rows = []

        for _, r in bid_rows.iterrows():
            offered = str(r.get("Offered Item", "")).replace("Item Categories :", "")
            for item in offered.split(","):
                if fingerprint(item) in user_fps:
                    matched_rows.append(r)
                    break

        if not matched_rows:
            adjusted_prices.append(None)
            continue

        temp_df = pd.DataFrame(matched_rows)

        # Ensure numeric
        temp_df["quantity"] = pd.to_numeric(temp_df["quantity"], errors="coerce")
        temp_df["Total Price"] = pd.to_numeric(temp_df["Total Price"], errors="coerce")
        temp_df = temp_df.dropna(subset=["quantity", "Total Price"])

        if temp_df.empty:
            adjusted_prices.append(None)
            continue

        # Unit price
        temp_df["unit_price"] = temp_df["Total Price"] / temp_df["quantity"]

        # Nearest quantity logic
        temp_df["qty_diff"] = abs(temp_df["quantity"] - user_quantity)
        nearest = temp_df.sort_values("qty_diff").iloc[0]

        est_price = nearest["unit_price"] * user_quantity
        adjusted_prices.append(round(est_price, 2))

    company_df["quantity_adjusted_price"] = adjusted_prices
    company_df.to_csv(company_check_csv, index=False)

    print("✅ Quantity-based price adjustment complete (bid-level)")
