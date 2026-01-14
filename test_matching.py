from processors.product_fingerprint import fingerprint

# Test cases
test_cases = [
    ("LIGATION CLIP", "MIRUS LIGATION CLIP MLT-300"),
    ("LIGATION CLIP", "V SHAPE LIGATION CLIP VMLT-400"),
    ("LIGATION CLIP", "Ligation Clips"),
    ("SYPHILIS TEST KIT", "Syphilis Total Antibody Test Elisa Kit"),
    ("PCR MACHINE", "Real Time PCR Machine"),
]

print("=" * 80)
print("🧪 TESTING PARTIAL MATCHING LOGIC")
print("=" * 80)

for user_input, product in test_cases:
    # Get fingerprints
    user_fp = fingerprint(user_input)
    product_fp = fingerprint(product)
    
    # Convert to token sets
    user_tokens = set(user_fp.split()) if user_fp else set()
    product_tokens = set(product_fp.split()) if product_fp else set()
    
    # Check if user tokens are a subset of product tokens
    is_match = user_tokens.issubset(product_tokens)
    
    # Display results
    print(f"\n📝 User Input: '{user_input}'")
    print(f"   Fingerprint: {user_fp}")
    print(f"   Tokens: {user_tokens}")
    
    print(f"\n📦 Product: '{product}'")
    print(f"   Fingerprint: {product_fp}")
    print(f"   Tokens: {product_tokens}")
    
    print(f"\n{'✅ MATCH' if is_match else '❌ NO MATCH'}")
    print(f"   User tokens subset of product tokens: {is_match}")
    print("-" * 80)
