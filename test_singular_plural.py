from processors.product_fingerprint import fingerprint

# Test singular/plural matching
test_cases = [
    ("LIGATION CLIP", "MIRUS LIGATION CLIPS POLY-400"),
    ("LIGATION CLIP", "LIGATION CLIPS"),
    ("TEST KIT", "TEST KITS"),
    ("SYRINGE", "SYRINGES 10ML"),
]

print("=" * 80)
print("🧪 TESTING SINGULAR/PLURAL MATCHING")
print("=" * 80)

for user_input, product in test_cases:
    user_fp = fingerprint(user_input)
    product_fp = fingerprint(product)
    
    user_tokens = set(user_fp.split()) if user_fp else set()
    product_tokens = set(product_fp.split()) if product_fp else set()
    
    is_match = user_tokens.issubset(product_tokens)
    
    print(f"\n📝 User: '{user_input}' → {user_tokens}")
    print(f"📦 Product: '{product}' → {product_tokens}")
    print(f"{'✅ MATCH' if is_match else '❌ NO MATCH'}")
    print("-" * 80)
