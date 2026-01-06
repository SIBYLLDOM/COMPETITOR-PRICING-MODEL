# processors/seller_l1_price.py

import pandas as pd
from utils.price_cleaner import clean_price

MAX_RANK = 20  # supports L1 to L20


def enrich_with_last_ranked_price(filtered_csv, company_check_csv):
    """
    Adds last_ranked_price column to company_check.csv.
    Priority:
      - If L1 exists → take last L1 price
      - Else → take last available price from L2 to L20
    """

    filtered_df = pd.read_csv(filtered_csv)
    company_df = pd.read_csv(company_check_csv)

    filtered_df.columns = filtered_df.columns.str.strip()
    company_df.columns = company_df.columns.str.strip()

    # Clean prices
    filtered_df["clean_price"] = filtered_df["Total Price"].apply(clean_price)

    # Normalize Rank (L1, L2, ..., L20)
    filtered_df["Rank"] = (
        filtered_df["Rank"]
        .astype(str)
        .str.upper()
        .str.strip()
    )

    last_price_map = {}

    for seller in company_df["Seller Name"]:
        seller_rows = filtered_df[
            (filtered_df["Seller Name"] == seller) &
            (filtered_df["clean_price"].notna())
        ]

        last_price = None

        # 1️⃣ First priority: L1
        l1_rows = seller_rows[seller_rows["Rank"] == "L1"]
        if not l1_rows.empty:
            last_price = l1_rows.iloc[-1]["clean_price"]
        else:
            # 2️⃣ Fallback: L2 to L20
            for i in range(2, MAX_RANK + 1):
                rank = f"L{i}"
                rank_rows = seller_rows[seller_rows["Rank"] == rank]
                if not rank_rows.empty:
                    last_price = rank_rows.iloc[-1]["clean_price"]
                    break

        last_price_map[seller] = last_price

    # Add column
    company_df["last_ranked_price"] = company_df["Seller Name"].map(last_price_map)

    # Save IN-PLACE
    company_df.to_csv(company_check_csv, index=False)

    return company_df
