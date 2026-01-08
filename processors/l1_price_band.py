# processors/l1_price_band.py

import pandas as pd


def calculate_l1_price_band(company_check_csv: str):
    """
    Calculates TRUE L1-winning price band.
    Band is defined as a controlled undercut of current L1.
    """

    df = pd.read_csv(company_check_csv)

    if "recommended_price" not in df.columns:
        raise ValueError("recommended_price column missing")

    # 🔑 Current market L1
    current_l1 = df["recommended_price"].min()

    # 🔥 L1-winning band (government-safe)
    low_price = round(current_l1 * 0.98, 2)    # aggressive
    high_price = round(current_l1 * 0.995, 2)  # conservative

    return low_price, high_price
