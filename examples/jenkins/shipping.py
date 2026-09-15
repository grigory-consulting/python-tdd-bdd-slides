FREE_SHIPPING_FROM = 5000
SHIPPING_FEE = 499


def shipping_cost(subtotal_cents: int) -> int:
    if subtotal_cents >= FREE_SHIPPING_FROM:
        return 0
    return SHIPPING_FEE
