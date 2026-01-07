# filters/competitor_filter.py

from processors.product_fingerprint import fingerprint


def filter_competitors(df, user_input):
    """
    Filters competitors using token fingerprinting.
    Supports SINGLE and MULTI product input.
    """

    # 1️⃣ Split user input (supports single or comma-separated)
    user_products = [
        p.strip()
        for p in user_input.split(",")
        if p.strip()
    ]

    # 2️⃣ Fingerprint each user product
    user_fps = set()
    for p in user_products:
        fp = fingerprint(p)
        if fp:
            user_fps.add(fp)

    if not user_fps:
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

        # 4️⃣ Match ANY product
        for item in offered_items:
            if fingerprint(item) in user_fps:
                matched_indices.append(idx)
                break

    return df.loc[matched_indices]
