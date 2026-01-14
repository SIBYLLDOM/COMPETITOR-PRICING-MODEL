# processors/seller_final_price.py

import pandas as pd




def enrich_with_final_price(
    company_check_csv: str,
    quantity_factor: float
):
    """
    🔥 CRITICAL CHANGE:
    - Treats all prices as TOTAL CONTRACT prices
    - Quantity factor is now neutral (1.0) and has NO effect
    - Applies inflation to base prices
    - Uses least_price as floor (actual market minimum)
    """

    df = pd.read_csv(company_check_csv)

    recommended_prices = []

    for _, row in df.iterrows():
        avg_price = row["average"]  # This is 10th percentile (L1-adjacent)
        inflation = row["inflation_rate_percent"]
        least_price = row["least_price"]

        # Base pricing with inflation
        price = avg_price * (1 + inflation / 100)

        # 🔥 REMOVED: price = price * quantity_factor
        # Reason: Prices are TOTAL CONTRACT, not unit prices

        # Safety floor (use least_price from historical data as minimum)
        price = max(price, least_price)

        recommended_prices.append(round(price, 2))

    df["recommended_price"] = recommended_prices
    df.to_csv(company_check_csv, index=False)

    print("✅ Final recommended_price calculated (TOTAL CONTRACT basis)")

