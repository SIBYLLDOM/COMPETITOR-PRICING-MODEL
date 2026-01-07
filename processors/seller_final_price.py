# processors/seller_final_price.py

import pandas as pd


def enrich_with_final_price(company_check_csv):
    """
    Computes recommended_price using INTERNAL market_average.
    market_average is NOT saved.
    """

    df = pd.read_csv(company_check_csv)

    required = {
        "average",
        "inflation_rate_percent",
        "last_ranked_price",
        "least_price"
    }

    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # INTERNAL ONLY
    market_average = df["average"].mean()

    def compute_price(row):
        avg = row["average"]
        last_rank = row["last_ranked_price"]
        least = row["least_price"]
        inflation = row["inflation_rate_percent"]

        # Base anchored to competition + market center
        base = min(last_rank, avg, market_average)

        # Inflation correction
        if inflation > 0:
            base *= 0.97   # overpriced → push down
        else:
            base *= 1.01   # aggressive → small buffer

        # Safety floor
        final_price = max(base, least)

        return round(final_price, 2)

    df["recommended_price"] = df.apply(compute_price, axis=1)

    df.to_csv(company_check_csv, index=False)

    print("✅ Final recommended_price calculated (market_average internal)")
