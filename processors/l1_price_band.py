# processors/l1_price_band.py

import pandas as pd




def calculate_l1_price_band(company_check_csv: str):
    """
    🔥 L1-SPECIFIC LEARNING:
    - Uses BOTTOM 5-10 PERCENTILE (not minimum)
    - L1 floor = aggressive undercut
    - L1 ceiling = conservative undercut
    
    - Validate band makes sense
    
    RETURNS: (low_price, high_price) as TOTAL CONTRACT prices
    """

    df = pd.read_csv(company_check_csv)

    if "recommended_price" not in df.columns:
        raise ValueError("recommended_price column missing")

    # 🔑 L1 LOGIC: Use 5th and 10th percentiles (bottom tier)
    # This captures true L1-winning behavior, not outliers
    l1_floor = df["recommended_price"].quantile(0.05)   # Bottom 5%
    l1_ceiling = df["recommended_price"].quantile(0.10) # Bottom 10%

    # If data is too sparse, fall back to min/mean approach
    if len(df) < 3:
        current_l1 = df["recommended_price"].min()
        l1_floor = current_l1 * 0.98
        l1_ceiling = current_l1 * 0.995
    
    # 🔥 L1-winning band (aggressive but safe)
    low_price = round(l1_floor * 0.98, 2)   # 2% undercut of 5th percentile
    high_price = round(l1_ceiling * 0.995, 2)  # 0.5% undercut of 10th percentile

    # Price band is ready - no artificial minimum enforced

    # Sanity check: high >= low
    if high_price < low_price:
        high_price = low_price * 1.02  # 2% margin

    # Calculate confidence based on data quality
    data_points = len(df)
    confidence = min(95, 50 + (data_points * 5))  # Cap at 95%

    print(f"\n📊 L1 PRICE BAND ANALYSIS:")
    print(f"   Data points: {data_points} competitors")
    print(f"   5th percentile: ₹{l1_floor:,.2f}")
    print(f"   10th percentile: ₹{l1_ceiling:,.2f}")
    print(f"   Confidence: {confidence}%")
    print(f"   Price type: TOTAL_CONTRACT")

    return low_price, high_price

