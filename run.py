# run.py

from utils.csv_loader import load_csv
from filters.item_filter import filter_by_item

from processors.seller_average import generate_seller_average
from processors.seller_inflation import enrich_company_check_with_inflation
from processors.seller_l1_price import enrich_with_last_ranked_price
from processors.seller_least_price import enrich_with_least_price
from processors.seller_final_price import enrich_with_final_price
from processors.l1_price_band import calculate_l1_price_band

from config.columns import FINANCIAL_COLUMNS

RAW_FILE = "data/raw/scraper_single_bid_results_financial.csv"
FILTERED_FILE = "data/processed/filtered_company.csv"
COMPANY_CHECK_FILE = "data/processed/company_check.csv"


def main():
    print("\n🚀 COMPETITOR PRICING MODEL")
    print("Phase 1 + Checkpoints 1–4 + Final Pricing + L1 Price Band\n")

    # ---------------- USER INPUT ----------------
    item_category = input("Enter Item Category: ").strip()
    if not item_category:
        print("❌ Item Category cannot be empty")
        return

    # ---------------- PHASE 1 ----------------
    df = load_csv(RAW_FILE)
    filtered_df = filter_by_item(df, item_category)

    if filtered_df.empty:
        print("⚠️ No competitors found for this item")
        return

    filtered_df = filtered_df[FINANCIAL_COLUMNS]
    filtered_df.to_csv(FILTERED_FILE, index=False)

    print(f"✅ Phase 1 completed → {FILTERED_FILE}")
    print(f"🏭 Competitors found: {len(filtered_df)}")

    # ---------------- CHECKPOINT 1 ----------------
    generate_seller_average(FILTERED_FILE, COMPANY_CHECK_FILE)
    print("✅ Checkpoint 1 → Seller average calculated")

    # ---------------- CHECKPOINT 2 ----------------
    enrich_company_check_with_inflation(COMPANY_CHECK_FILE)
    print("✅ Checkpoint 2 → Market average & inflation rate added")

    # ---------------- CHECKPOINT 3 ----------------
    enrich_with_last_ranked_price(FILTERED_FILE, COMPANY_CHECK_FILE)
    print("✅ Checkpoint 3 → Last ranked price (L1 priority, L2–L20 fallback) added")

    # ---------------- CHECKPOINT 4 ----------------
    enrich_with_least_price(FILTERED_FILE, COMPANY_CHECK_FILE)
    print("✅ Checkpoint 4 → Least price added")

    # ---------------- FINAL PRICE ----------------
    enrich_with_final_price(COMPANY_CHECK_FILE)
    print("✅ Final pricing → Recommended price calculated")

    # ---------------- L1 PRICE BAND (GAME CHANGER) ----------------
    low_price, high_price = calculate_l1_price_band(COMPANY_CHECK_FILE)

    print(f"\n🎯 SUGGESTED PRICING FOR THE PRODUCT - {item_category}")
    print(f"💰 Low Price  : {low_price}")
    print(f"💰 High Price : {high_price}")
    print("👉 Bidding within this range gives a HIGH probability of L1")


    print("\n📄 FINAL DATA FILE")
    print("➡ data/processed/company_check.csv")


if __name__ == "__main__":
    main()
