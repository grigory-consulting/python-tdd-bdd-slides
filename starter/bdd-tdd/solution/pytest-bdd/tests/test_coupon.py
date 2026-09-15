"""Die neue Regel aus Discovery; die ersten drei Fälle stehen auch in Gherkin."""
from decimal import Decimal
import pytest
from shop.discount import payable_total

@pytest.mark.parametrize("customer,subtotal,expected", [
    ("vip", "100.00", "70.00"),
    ("vip", "10.00", "0.00"),
    ("regular", "100.00", "80.00"),
], ids=["vip-100", "nullgrenze", "regular-100"])
def test_coupon(customer, subtotal, expected):
    assert payable_total(customer, Decimal(subtotal), coupon="SAVE20") == Decimal(expected)

def test_unbekannter_coupon_wird_abgelehnt():
    with pytest.raises(ValueError, match="Coupon"):
        payable_total("vip", Decimal("100.00"), coupon="UNBEKANNT")
