"""Der Bugfix: ein Coupon darf den Preis nicht unter null druecken.

Reihenfolge im Lab: erst pinnen (test_characterization.py), dann klaeren
(Entscheidung der Fachseite), dann diesen Test schreiben - rot -, dann die
Implementierung aendern. Begruendung in BUGFIX.md.

Vor der Aenderung ergab der erste Fall -12.73.
"""

import pytest

from shop import legacy_pricing

BUCH = {"price": 10.0, "qty": 1, "category": "book"}


def test_coupon_groesser_als_warenkorb_ergibt_null():
    assert legacy_pricing.calculate_price([BUCH], "regular", "SAVE20", "DE") == 0.0


def test_coupon_genau_so_gross_wie_der_warenkorb_ergibt_null():
    assert legacy_pricing.calculate_price(
        [{"price": 20.0, "qty": 1}], "regular", "SAVE20", "DE"
    ) == 0.0


@pytest.mark.parametrize("region", ["DE", "CH", "US", "XX"])
def test_untergrenze_gilt_in_jeder_region(region):
    """Keine Region darf durch die Steuerrechnung ins Minus rutschen."""
    assert legacy_pricing.calculate_price([BUCH], "regular", "SAVE20", region) == 0.0


def test_kleinerer_coupon_wird_weiterhin_normal_abgezogen():
    """Die Untergrenze darf den gueltigen Fall nicht veraendern."""
    assert legacy_pricing.calculate_price(
        [{"price": 100.0, "qty": 1}], "vip", "SAVE20", "DE"
    ) == 83.3


def test_kein_preis_wird_negativ():
    """Breitere Absicherung ueber mehrere Warenkoerbe."""
    for preis in (0.0, 1.0, 5.0, 16.8, 19.99, 20.0, 25.0):
        ergebnis = legacy_pricing.calculate_price(
            [{"price": preis, "qty": 1}], "regular", "SAVE20", "DE"
        )
        assert ergebnis >= 0.0, f"negativer Preis bei {preis}"
