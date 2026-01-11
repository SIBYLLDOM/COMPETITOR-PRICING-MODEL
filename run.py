# run.py

import pandas as pd
import json

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

MIN_TENDER_PRICE = 50000  # Sanity check


def main():
    print("\n🚀 COMPETITOR PRICING MODEL (L1-OPTIMIZED)\n")
    print("=" * 60)
    print("🔥 USING L1-SPECIFIC LEARNING (Bottom Percentile Pricing)")
    print("=" * 60)

    user_product = input("\nEnter Item Category: ").strip()
    user_quantity = int(input("Enter Quantity: ").strip())

    # Phase 1: Filter competitors
    print("\n📂 Phase 1: Filtering Competitors...")
    
    try:
        df = pd.read_csv(RAW_FILE, low_memory=False)
    except FileNotFoundError:
        print(f"\n❌ ERROR: Data file not found: {RAW_FILE}")
        print("   Please ensure the raw data file exists.")
        return
    except Exception as e:
        print(f"\n❌ ERROR reading data file: {e}")
        return
    
    filtered_df = filter_competitors(df, user_product)

    if filtered_df.empty:
        print("⚠️ No competitors found")
        return

    try:
        filtered_df.to_csv(FILTERED_FILE, index=False)
    except PermissionError:
        print(f"\n❌ PERMISSION ERROR: Cannot write to {FILTERED_FILE}")
        print("\n📋 TROUBLESHOOTING:")
        print("   1. Close Excel if you have this file open")
        print("   2. Close any text editors viewing this file")
        print("   3. Check file is not read-only")
        print("\n   Then run the script again.")
        return
    except Exception as e:
        print(f"\n❌ ERROR saving filtered data: {e}")
        return
    print(f"✅ Phase 1 complete | Competitors found: {len(filtered_df)}")

    # Phase 2: Generate L1-specific pricing
    print("\n📈 Phase 2: Calculating L1-Specific Pricing...")
    generate_seller_average(FILTERED_FILE, COMPANY_CHECK_FILE)
    enrich_company_check_with_inflation(COMPANY_CHECK_FILE)
    enrich_with_last_ranked_price(FILTERED_FILE, COMPANY_CHECK_FILE)
    enrich_with_least_price(FILTERED_FILE, COMPANY_CHECK_FILE)

    # Phase 3: Quantity context (NO rescaling)
    print("\n📊 Phase 3: Analyzing Quantity Context...")
    quantity_factor = get_quantity_scaling_factor(
        BASIC_FILE,
        FILTERED_FILE,
        user_quantity
    )
    print(f"   Quantity scaling factor: {quantity_factor} (neutral = 1.0)")

    # Phase 4: Final price calculation
    print("\n💰 Phase 4: Computing Final L1 Recommendations...")
    enrich_with_final_price(
        COMPANY_CHECK_FILE,
        quantity_factor
    )

    # Phase 5: L1 Band calculation
    low, high = calculate_l1_price_band(COMPANY_CHECK_FILE)

    # 🔥 SANITY CHECKS
    if low < MIN_TENDER_PRICE or high < MIN_TENDER_PRICE:
        print(f"\n⚠️ WARNING: Price below tender minimum (₹{MIN_TENDER_PRICE:,})")
        low = max(low, MIN_TENDER_PRICE)
        high = max(high, MIN_TENDER_PRICE)

    # Calculate confidence
    df_check = pd.read_csv(COMPANY_CHECK_FILE)
    data_points = len(df_check)
    confidence = min(95, 50 + (data_points * 5))

    # 🎯 OUTPUT (JSON FORMAT)
    result = {
        "product": user_product,
        "quantity": user_quantity,
        "low_price": low,
        "high_price": high,
        "price_type": "TOTAL_CONTRACT",
        "confidence": f"{confidence}%",
        "basis": "filtered_company.csv (L1 percentile pricing)",
        "competitors_analyzed": data_points
    }

    print("\n" + "=" * 60)
    print("🎯 L1 PRICING RECOMMENDATION")
    print("=" * 60)
    print(f"\n📦 Product  : {user_product}")
    print(f"� Quantity : {user_quantity}")
    print(f"\n💰 L1 PRICE BAND (TOTAL CONTRACT):")
    print(f"   Low Price  : ₹{low:,.2f}")
    print(f"   High Price : ₹{high:,.2f}")
    print(f"\n📈 Confidence : {confidence}% (based on {data_points} competitors)")
    print(f"🔍 Basis      : L1 percentile pricing from filtered_company.csv")
    print(f"📋 Price Type : TOTAL CONTRACT (NOT unit price)")
    
    print("\n👉 Bid within this range for high L1 win probability")
    
    print("\n📄 Detailed Report:")
    print("   ➡ data/processed/company_check.csv")
    
    print("\n📤 JSON Output:")
    print(json.dumps(result, indent=2))
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()

