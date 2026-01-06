# processors/seller_least_price.py

import pandas as pd
from utils.price_cleaner import clean_price

def enrich_with_least_price(filtered_csv, company_check_csv):
    """
    Adds least_price column to company_check.csv (in-place).
    Least price = minimum price quoted by the seller.
    """

    filtered_df = pd.read_csv(filtered_csv)
    company_df = pd.read_csv(company_check_csv)

    filtered_df.columns = filtered_df.columns.str.strip()
    company_df.columns = company_df.columns.str.strip()

    # Clean Total Price
    filtered_df["clean_price"] = filtered_df["Total Price"].apply(clean_price)

    # Compute least price per seller
    least_price_map = (
        filtered_df
        .dropna(subset=["clean_price"])
        .groupby("Seller Name")["clean_price"]
        .min()
        .to_dict()
    )

    # Add column
    company_df["least_price"] = company_df["Seller Name"].map(least_price_map)

    # Save IN-PLACE
    company_df.to_csv(company_check_csv, index=False)

    return company_df
