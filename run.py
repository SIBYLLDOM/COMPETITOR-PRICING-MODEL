# run.py

import sys
import os

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8')

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

    # No minimum price enforcement - use actual calculated values

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
    
    
    # Display relevant competitors (exclude outliers, prioritize experienced bidders)
    print("\n🏆 TOP 5 REALISTIC COMPETITORS (Within Competitive Range):")
    print("-" * 60)
    
    # Filter out extreme outliers - keep only prices within competitive range
    # Competitive range = 5th to 20th percentile (realistic L1-adjacent pricing)
    p5 = df_check['recommended_price'].quantile(0.05)
    p20 = df_check['recommended_price'].quantile(0.20)
    
    # Filter competitors within realistic range
    df_realistic = df_check[
        (df_check['recommended_price'] >= p5 * 0.95) &  # Allow 5% below 5th percentile
        (df_check['recommended_price'] <= p20 * 1.1)     # Allow 10% above 20th percentile
    ].copy()
    
    # 🔥 PRIORITIZE EXPERIENCED BIDDERS (2+ bids)
    # Check if bid_count column exists
    if 'bid_count' in df_realistic.columns:
        df_experienced = df_realistic[df_realistic['bid_count'] >= 2].copy()
        
        if len(df_experienced) >= 5:
            df_sorted = df_experienced.sort_values('recommended_price').head(5)
            show_experienced_note = True
        else:
            # Not enough experienced bidders, show all
            df_sorted = df_realistic.sort_values('recommended_price').head(5)
            show_experienced_note = False
            if not df_realistic.empty:
                print("⚠️ Limited experienced bidders - showing all available competitors")
                print()
    else:
        # No bid_count column (legacy data)
        df_sorted = df_realistic.sort_values('recommended_price').head(5)
        show_experienced_note = False
    
    if df_sorted.empty:
        print("\n⚠️ No realistic competitors found in competitive range")
        print(f"   (This may indicate data quality issues)")
    else:
        for idx, (i, row) in enumerate(df_sorted.iterrows(), 1):
            print(f"\n{idx}. {row['Seller Name']}")
            print(f"   Recommended Price       : ₹{row['recommended_price']:,.2f} ⭐")
            
            # Show bid count if available
            if 'bid_count' in row.index:
                bid_count = int(row['bid_count'])
                experience_indicator = "🎯" if bid_count >= 3 else "📊" if bid_count == 2 else "⚡"
                print(f"   Bidding History         : {bid_count} bids {experience_indicator}")
            
            print(f"   Average Bidding Price   : ₹{row['average']:,.2f}")
            print(f"   Inflation Rate          : {row['inflation_rate_percent']:.2f}%")
            print(f"   Last L1 Price           : ₹{row['last_ranked_price']:,.2f}")
            print(f"   Least Quoted Price      : ₹{row['least_price']:,.2f}")
    
    print("\n" + "-" * 60)
    print(f"📊 Competitive Range: ₹{p5:,.2f} - ₹{p20:,.2f} (5th-20th percentile)")
    if show_experienced_note:
        print(f"💡 Showing experienced bidders only (2+ bids for reliable patterns)")
    else:
        print(f"💡 These competitors represent realistic L1-adjacent pricing")
    
    print("\n👉 Bid within this range for high L1 win probability")
    
    print("\n📄 Detailed Report:")
    print("   ➡ data/processed/company_check.csv")
    
    print("\n📤 JSON Output:")
    print(json.dumps(result, indent=2))
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()

