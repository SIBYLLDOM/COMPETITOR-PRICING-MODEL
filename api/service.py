from run_engine import run_pricing_engine


def get_pricing(product: str, quantity: int):
    """
    Thin service layer.
    Keeps API clean and engine reusable.
    """
    return run_pricing_engine(product, quantity)
