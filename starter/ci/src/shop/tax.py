"""Bruttobetrag aus einem Nettobetrag und einem expliziten Steuersatz."""
from decimal import Decimal, ROUND_HALF_UP

def gross_total(net: Decimal, tax_percent: Decimal) -> Decimal:
    if net < 0:
        raise ValueError("Nettobetrag darf nicht negativ sein")
    if tax_percent < 0:
        raise ValueError("Steuersatz darf nicht negativ sein")
    return (net * (Decimal("1") + tax_percent / Decimal("100"))).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
