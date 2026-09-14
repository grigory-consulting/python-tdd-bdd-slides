"""Aufgabe d: Zeit ist ein Kollaborator wie jeder andere.

Statt die Uhr zu patchen, wird das Datum hereingereicht. Der Test wird
dadurch deterministisch und lesbar: Man sieht am Aufruf, welcher Tag gilt.
"""

from datetime import date
from decimal import Decimal

from shop.order import LineItem, Order, today_provider

IM_JUNI = date(2026, 6, 15)
IM_DEZEMBER = date(2026, 12, 5)


def test_ohne_injektion_liefert_die_standarduhr_ein_datum():
    """Der Standardweg bleibt das Systemdatum; nur der Test hebelt ihn aus."""
    assert isinstance(today_provider(), date)


def test_im_dezember_ist_der_versand_frei(standardbestellung, fake_shipping):
    # 100.00 - 10.00 + 0.00
    assert standardbestellung.total(fake_shipping, today=IM_DEZEMBER) == Decimal("90.00")
    assert fake_shipping.calls == []


def test_ausserhalb_dezember_faellt_versand_an(standardbestellung, fake_shipping):
    assert standardbestellung.total(fake_shipping, today=IM_JUNI) == Decimal("94.99")


def test_ab_200_euro_ist_der_versand_frei(fake_shipping):
    order = Order(
        "regular",
        "DE",
        [LineItem("Monitor", Decimal("200.00"), 1, Decimal("5.0"))],
    )
    assert order.total(fake_shipping, today=IM_JUNI) == Decimal("200.00")


def test_knapp_unter_200_euro_faellt_versand_an(fake_shipping):
    order = Order(
        "regular",
        "DE",
        [LineItem("Monitor", Decimal("199.99"), 1, Decimal("5.0"))],
    )
    assert order.total(fake_shipping, today=IM_JUNI) == Decimal("204.98")


def test_beide_regeln_zusammen_geben_nur_einmal_frei_versand(fake_shipping):
    order = Order(
        "vip",
        "DE",
        [LineItem("Monitor", Decimal("250.00"), 1, Decimal("5.0"))],
    )
    # 250.00 - 25.00 (VIP 10 Prozent) + 0.00
    assert order.total(fake_shipping, today=IM_DEZEMBER) == Decimal("225.00")
