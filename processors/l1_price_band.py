# processors/l1_price_band.py



import pandas as pd


def calculate_l1_price_band(company_check_csv):
    """
    Calculates L1 price band using INTERNAL market_average.
    market_average is NOT saved.
    """

    df = pd.read_csv(company_check_csv)

    required = {
        "recommended_price",
        "last_ranked_price",
        "least_price",
        "average"
    }

    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # INTERNAL ONLY
    market_average = df["average"].mean()

    min_last_rank = df["last_ranked_price"].min()
    min_least = df["least_price"].min()
    min_recommended = df["recommended_price"].min()

    # Low price: must beat competition but not crash market
    low_price = min(min_last_rank, min_least, market_average)

    # High price: safe competitive ceiling
    high_price = min(min_recommended, market_average)

    low_price = round(low_price, 2)
    high_price = round(high_price, 2)

    if high_price < low_price:
        high_price = low_price

    return low_price, high_price
