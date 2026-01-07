# product_items_run.py

from processors.extract_product_items import extract_raw_product_items

RAW_INPUT = "data/raw/scraper_single_bid_results_financial.csv"
RAW_OUTPUT = "data/processed/product_items_raw.csv"


def main():
    print("\n⚡ PRODUCT ITEM RAW NORMALIZATION\n")

    extract_raw_product_items(
        RAW_INPUT,
        RAW_OUTPUT
    )

    print("✅ product_items_raw.csv generated")
    print(f"➡ {RAW_OUTPUT}")


if __name__ == "__main__":
    main()
