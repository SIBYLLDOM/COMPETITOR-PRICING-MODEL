# processors/seller_final_price.py

import pandas as pd

def enrich_with_final_price(company_check_csv):
    """
    Adds recommended_price column based on 4 checkpoints.
    Updates company_check.csv in-place.
    """

    df = pd.read_csv(company_check_csv)
    df.columns = df.columns.str.strip()

    final_prices = []

    for _, row in df.iterrows():
        average = row["average"]
        market_avg = row["market_average"]
        last_ranked = row["last_ranked_price"]
        least_price = row["least_price"]
        inflation = row["inflation_rate_percent"]

        # Step 1: Base anchor
        base_price = min(
            p for p in [average, last_ranked, market_avg]
            if pd.notna(p)
        )

        adjusted_price = base_price

        # Step 2: Inflation adjustment
        if inflation > 5:
            adjusted_price = base_price * 0.97  # reduce 3%

        # Step 3: Floor protection
        final_price = max(adjusted_price, least_price)

        final_prices.append(round(final_price, 2))

    df["recommended_price"] = final_prices

    df.to_csv(company_check_csv, index=False)
    return df
