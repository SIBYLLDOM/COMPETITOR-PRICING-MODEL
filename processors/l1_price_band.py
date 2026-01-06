# processors/l1_price_band.py

import pandas as pd

def calculate_l1_price_band(company_check_csv):
    """
    Returns a govt-safe low & high price band for L1.
    """

    df = pd.read_csv(company_check_csv)
    df.columns = df.columns.str.strip()

    market_avg = df["market_average"].iloc[0]

    min_last_ranked = df["last_ranked_price"].min()
    min_least_price = df["least_price"].min()
    min_recommended = df["recommended_price"].min()

    # ----- LOW PRICE (aggressive but safe) -----
    low_price = max(
        min_last_ranked,
        min_least_price,
        market_avg * 0.95
    )

    # ----- HIGH PRICE (upper L1 boundary) -----
    high_price = min(
        min_recommended,
        market_avg,
        market_avg * 1.02
    )

    # ----- Safety correction -----
    if low_price >= high_price:
        high_price = low_price * 1.03

    return round(low_price, 2), round(high_price, 2)
