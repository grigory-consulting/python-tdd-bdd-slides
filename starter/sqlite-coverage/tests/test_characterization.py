"""Characterization Tests fuer shop.legacy_pricing.

Diese Tests pruefen NICHT, ob der Code richtig ist. Sie halten fest, was er
tatsaechlich tut, damit ein Refactoring auffaellt, sobald es das Verhalten
aendert. Michael Feathers nennt das Verfahren Characterization Testing:
https://michaelfeathers.silvrback.com/characterization-testing

Vorgehen: Test mit dem Namen ``x`` schreiben, einen Dummy-Erwartungswert
einsetzen, den Test laufen lassen, den tatsaechlichen Wert aus der
Fehlermeldung uebernehmen und den Test danach nach dem verstandenen
Verhalten benennen.
"""

import pytest

from shop import legacy_pricing

BUCH = {"price": 10.0, "qty": 1, "category": "book"}
ZWEI_ARTIKEL = [{"price": 10.0, "qty": 2}]


@pytest.mark.parametrize(
    "case, items, customer_type, coupon, region, pinned",
    [
        # Einfachster Fall: zwei Artikel, Privatkunde, deutsche Mehrwertsteuer.
        ("plain_order", ZWEI_ARTIKEL, "regular", None, "DE", 23.8),
        # Ueberraschung 1: Buecher bekommen still 7 Prozent Nachlass.
        ("book_gets_silent_discount", [BUCH], "regular", None, "DE", 11.07),
        # Kundenrabatt vor Steuer.
        ("vip_gets_ten_percent", [{"price": 100.0, "qty": 1}], "vip", None, "DE", 107.1),
        ("staff_pays_half", [{"price": 100.0, "qty": 1}], "staff", None, "DE", 59.5),
        # Ueberraschung 2: FREESHIP zieht 4.99 vom Warenwert ab, nicht vom Versand.
        ("freeship_reduces_goods_value", ZWEI_ARTIKEL, "regular", "FREESHIP", "DE", 17.86),
        # Ueberraschung 3: eine unbekannte Region faellt still auf DE zurueck.
        ("unknown_region_falls_back_to_de", ZWEI_ARTIKEL, "regular", None, "XX", 23.8),
        ("swiss_vat_is_lower", ZWEI_ARTIKEL, "regular", None, "CH", 21.62),
        ("us_has_no_vat", ZWEI_ARTIKEL, "regular", None, "US", 20.0),
        # Ueberraschung 4 (PINNED, NOT ENDORSED): der Coupon kannte keine
        # Untergrenze. Der Warenwert wurde negativ, die Mehrwertsteuer wurde
        # auf den negativen Betrag gerechnet, und die Funktion gab -12.73
        # zurueck. Beim Charakterisieren wurde dieser Wert festgehalten, ohne
        # ihn zu billigen: zu diesem Zeitpunkt wusste niemand, ob ein Aufrufer
        # sich darauf verlaesst. Erst klaeren, dann aendern.
        # Nach der Entscheidung der Fachseite (Untergrenze 0.00, siehe
        # BUGFIX.md) steht hier bewusst der neue Wert. Ein Characterization
        # Test darf sich aendern - aber nur absichtlich und dokumentiert.
        ("coupon_larger_than_basket_is_floored", [BUCH], "regular", "SAVE20", "DE", 0.0),
        ("coupon_smaller_than_basket_still_applies",
         [{"price": 100.0, "qty": 1}], "vip", "SAVE20", "DE", 83.3),
    ],
)
def test_current_behaviour_is_pinned(case, items, customer_type, coupon, region, pinned):
    assert legacy_pricing.calculate_price(items, customer_type, coupon, region) == pinned


def test_leerer_warenkorb_kostet_nichts():
    assert legacy_pricing.calculate_price([], "regular", None, "DE") == 0.0


def test_unbekannter_coupon_wird_ignoriert():
    assert legacy_pricing.calculate_price(ZWEI_ARTIKEL, "regular", "HALLO", "DE") == 23.8
