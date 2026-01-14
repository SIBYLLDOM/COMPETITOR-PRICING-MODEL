# filters/competitor_filter.py

from processors.product_fingerprint import fingerprint


def filter_competitors(df, user_input):
    """
    Filters competitors using partial token matching.
    Supports SINGLE and MULTI product input.
    User input tokens are matched as a subset of product tokens.
    """

    # 1️⃣ Split user input (supports single or comma-separated)
    user_products = [
        p.strip()
        for p in user_input.split(",")
        if p.strip()
    ]

    # 2️⃣ Create token sets for each user product
    user_token_sets = []
    for p in user_products:
        fp = fingerprint(p)
        if fp:
            # Convert fingerprint (space-separated tokens) to a set
            tokens = set(fp.split())
            user_token_sets.append(tokens)

    if not user_token_sets:
        return df.iloc[0:0]  # empty dataframe

    matched_indices = []

    # 3️⃣ Scan each tender row
    for idx, row in df.iterrows():
        offered = str(row.get("Offered Item", ""))
        offered = offered.replace("Item Categories :", "")

        offered_items = [
            item.strip()
            for item in offered.split(",")
            if item.strip()
        ]

        # 4️⃣ Check if ANY user product tokens are a subset of ANY offered item
        for item in offered_items:
            item_fp = fingerprint(item)
            if item_fp:
                item_tokens = set(item_fp.split())
                
                # Check if any user product matches (partial match)
                for user_tokens in user_token_sets:
                    # All user tokens must be present in item tokens
                    if user_tokens.issubset(item_tokens):
                        matched_indices.append(idx)
                        break
                else:
                    continue
                break

    return df.loc[matched_indices]
