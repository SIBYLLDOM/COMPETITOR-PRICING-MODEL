from processors.fast_canonicalizer import fast_canonicalize

INPUT = "data/processed/product_items_raw.csv"
OUTPUT = "data/processed/product_items.csv"

if __name__ == "__main__":
    fast_canonicalize(INPUT, OUTPUT)
