# run_engine.py

import pandas as pd

from filters.competitor_filter import filter_competitors
from processors.seller_average import generate_seller_average
from processors.seller_inflation import enrich_company_check_with_inflation
from processors.seller_l1_price import enrich_with_last_ranked_price
from processors.seller_least_price import enrich_with_least_price
from processors.seller_quantity_analysis import get_quantity_scaling_factor
from processors.seller_final_price import enrich_with_final_price
from processors.l1_price_band import calculate_l1_price_band

RAW_FILE = "data/raw/scraper_single_bid_results_financial.csv"
BASIC_FILE = "data/raw/scraper_single_bid_results_basic.csv"

FILTERED_FILE = "data/processed/filtered_company.csv"
COMPANY_CHECK_FILE = "data/processed/company_check.csv"


def run_pricing_engine(product: str, quantity: int):
    df = pd.read_csv(RAW_FILE, low_memory=False)

    filtered_df = filter_competitors(df, product)
    if filtered_df.empty:
        return None

    filtered_df.to_csv(FILTERED_FILE, index=False)

    # Core pipeline
    generate_seller_average(FILTERED_FILE, COMPANY_CHECK_FILE)
    enrich_company_check_with_inflation(COMPANY_CHECK_FILE)
    enrich_with_last_ranked_price(FILTERED_FILE, COMPANY_CHECK_FILE)
    enrich_with_least_price(FILTERED_FILE, COMPANY_CHECK_FILE)

    # Quantity logic (IN MEMORY)
    quantity_factor = get_quantity_scaling_factor(
        BASIC_FILE,
        FILTERED_FILE,
        quantity
    )

    enrich_with_final_price(
        COMPANY_CHECK_FILE,
        quantity_factor
    )

    low, high = calculate_l1_price_band(COMPANY_CHECK_FILE)

    # 🔥 TOP 5 SELLERS (MOST COMPETITIVE)
    company_df = pd.read_csv(COMPANY_CHECK_FILE)

    top_5_sellers = (
        company_df
        .sort_values("recommended_price")
        .head(5)["Seller Name"]
        .tolist()
    )

    return {
        "product": product,
        "quantity": quantity,
        "low_price": low,
        "high_price": high,
        "top_5_sellers": top_5_sellers
    }
