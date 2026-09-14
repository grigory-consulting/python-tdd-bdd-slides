from decimal import Decimal
import pytest
from shop.tax import gross_total

@pytest.mark.parametrize("net,rate,expected", [
    ("90.00", "19", "107.10"),
    ("90.00", "7", "96.30"),
    ("0.05", "10", "0.06"),
])
def test_bruttobetrag(net, rate, expected):
    assert gross_total(Decimal(net), Decimal(rate)) == Decimal(expected)

@pytest.mark.parametrize("net,rate", [("-1", "19"), ("90", "-1")])
def test_negative_eingaben_werden_abgelehnt(net, rate):
    with pytest.raises(ValueError):
        gross_total(Decimal(net), Decimal(rate))
