from processors.seller_inflation import calculate_seller_inflation

INPUT_FILE = "data/processed/company_check.csv"
OUTPUT_FILE = "data/processed/seller_inflation.csv"

def main():
    print("\n📊 CHECKPOINT 2 – SELLER INFLATION RATE\n")

    result = calculate_seller_inflation(INPUT_FILE, OUTPUT_FILE)

    print(f"✅ seller_inflation.csv generated")
    print(f"🏭 Sellers analyzed: {len(result)}")

if __name__ == "__main__":
    main()
