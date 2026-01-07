# run.py

import pandas as pd

from filters.competitor_filter import filter_competitors

from processors.seller_average import generate_seller_average
from processors.seller_inflation import enrich_company_check_with_inflation
from processors.seller_l1_price import enrich_with_last_ranked_price
from processors.seller_least_price import enrich_with_least_price
from processors.seller_final_price import enrich_with_final_price
from processors.l1_price_band import calculate_l1_price_band

RAW_FILE = "data/raw/scraper_single_bid_results_financial.csv"
FILTERED_FILE = "data/processed/filtered_company.csv"
COMPANY_CHECK_FILE = "data/processed/company_check.csv"


def main():
    print("\n🚀 COMPETITOR PRICING MODEL (OPTIMIZED)\n")

    user_product = input("Enter Item Category: ").strip()
    if not user_product:
        print("❌ Product cannot be empty")
        return

    # ---------------- PHASE 1: FILTER ----------------
    df = pd.read_csv(RAW_FILE, low_memory=False)

    filtered_df = filter_competitors(df, user_product)

    if filtered_df.empty:
        print("⚠️ No competitors found for this product")
        return

    filtered_df.to_csv(FILTERED_FILE, index=False)

    print(f"✅ Phase 1 complete | Competitors found: {len(filtered_df)}")

    # ---------------- CHECKPOINTS ----------------
    generate_seller_average(FILTERED_FILE, COMPANY_CHECK_FILE)
    enrich_company_check_with_inflation(COMPANY_CHECK_FILE)
    enrich_with_last_ranked_price(FILTERED_FILE, COMPANY_CHECK_FILE)
    enrich_with_least_price(FILTERED_FILE, COMPANY_CHECK_FILE)
    enrich_with_final_price(COMPANY_CHECK_FILE)

    # ---------------- FINAL OUTPUT ----------------
    low, high = calculate_l1_price_band(COMPANY_CHECK_FILE)

    print(f"\n🎯 SUGGESTED PRICING FOR THE PRODUCT - {user_product}")
    print(f"💰 Low Price  : {low}")
    print(f"💰 High Price : {high}")
    print("👉 Bid in this range for high L1 probability")

    print("\n📄 Output File:")
    print("➡ data/processed/company_check.csv")


if __name__ == "__main__":
    main()
