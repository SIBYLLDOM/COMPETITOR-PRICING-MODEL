# processors/seller_average.py

import pandas as pd
from utils.price_cleaner import clean_price

def generate_seller_average(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    df.columns = df.columns.str.strip()

    df["clean_price"] = df["Total Price"].apply(clean_price)
    df = df[df["clean_price"].notna()]

    avg_df = (
        df.groupby("Seller Name", as_index=False)["clean_price"]
        .mean()
        .rename(columns={"clean_price": "average"})
    )

    meta_df = (
        df.groupby("Seller Name", as_index=False)
        .first()[["S.No.", "bid_no", "Seller Name"]]
    )

    result = meta_df.merge(avg_df, on="Seller Name")
    result.to_csv(output_csv, index=False)

    return result
