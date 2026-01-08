# processors/seller_final_price.py

import pandas as pd


def enrich_with_final_price(
    company_check_csv: str,
    quantity_factor: float
):
    """
    Computes recommended_price using INTERNAL quantity factor.
    Does NOT store any quantity column.
    """

    df = pd.read_csv(company_check_csv)

    recommended_prices = []

    for _, row in df.iterrows():
        avg_price = row["average"]
        inflation = row["inflation_rate_percent"]
        least_price = row["least_price"]

        # Base pricing
        price = avg_price * (1 + inflation / 100)

        # Apply quantity impact
        price = price * quantity_factor

        # Safety floor
        price = max(price, least_price)

        recommended_prices.append(round(price, 2))

    df["recommended_price"] = recommended_prices
    df.to_csv(company_check_csv, index=False)

    print("✅ Final recommended_price calculated (quantity applied internally)")
