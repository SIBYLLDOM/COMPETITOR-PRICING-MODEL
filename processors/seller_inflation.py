# processors/seller_inflation.py

import pandas as pd


def enrich_company_check_with_inflation(company_check_csv):
    """
    Computes inflation_rate_percent using INTERNAL market_average.
    market_average is NOT stored in CSV.
    """

    df = pd.read_csv(company_check_csv)

    if "average" not in df.columns:
        raise ValueError("Missing 'average' column")

    # INTERNAL ONLY
    market_average = df["average"].mean()

    df["inflation_rate_percent"] = (
        (df["average"] - market_average) / market_average
    ) * 100

    df["inflation_rate_percent"] = df["inflation_rate_percent"].round(2)

    df.to_csv(company_check_csv, index=False)

    print("✅ Checkpoint 2 complete | Inflation calculated (market_average internal)")
