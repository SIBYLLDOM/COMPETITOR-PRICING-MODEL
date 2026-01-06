# processors/seller_inflation.py

import pandas as pd

def enrich_company_check_with_inflation(company_check_csv):
    """
    Adds market_average and inflation_rate_percent
    to company_check.csv (in-place update)
    """

    df = pd.read_csv(company_check_csv)
    df.columns = df.columns.str.strip()

    if "average" not in df.columns:
        raise ValueError("❌ 'average' column missing. Run Checkpoint 1 first.")

    # Market average across sellers
    market_average = df["average"].mean()

    df["market_average"] = market_average
    df["inflation_rate_percent"] = (
        (df["average"] - market_average) / market_average
    ) * 100

    df["inflation_rate_percent"] = df["inflation_rate_percent"].round(2)

    # Overwrite SAME file
    df.to_csv(company_check_csv, index=False)

    return df
