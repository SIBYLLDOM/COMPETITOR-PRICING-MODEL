import pandas as pd
from filters.competitor_filter import filter_competitors

# Read the CSV file
df = pd.read_csv("data/raw/scraper_single_bid_results_financial.csv")

print(f"Total records in dataset: {len(df)}")

# Test with "LIGATION CLIP"
user_input = "LIGATION CLIP"
print(f"\n🔍 Searching for: '{user_input}'")

filtered = filter_competitors(df, user_input)
print(f"✅ Found {len(filtered)} matching records\n")

# Show first 10 matches
if len(filtered) > 0:
    print("Sample matches:")
    print("-" * 100)
    for idx, row in filtered.head(10).iterrows():
        print(f"Seller: {row['Seller Name']}")
        print(f"Product: {row['Offered Item']}")
        print(f"Price: {row['Total Price']}")
        print("-" * 100)
else:
    print("❌ No matches found!")
