"""Aufgabe a: Fake statt Mock. Geprueft wird der Zustand, also das Ergebnis.

Diese Tests sind vollstaendig vorgegeben. Sie werden gruen, sobald
``FakeShippingService`` in ``conftest.py`` fertig ist.
"""

from datetime import date
from decimal import Decimal

import pytest

from shop.order import LineItem, Order

# Ein Datum ausserhalb des Dezembers, damit die Dezember-Regel nicht greift.
IM_JUNI = date(2026, 6, 15)


def test_standardbestellung_kostet_94_99(standardbestellung, fake_shipping):
    # 100.00 Warenwert - 10.00 VIP-Rabatt + 4.99 Versand DE
    assert standardbestellung.total(fake_shipping, today=IM_JUNI) == Decimal("94.99")


def test_lieferung_nach_at_kostet_mehr(fake_shipping):
    order = Order(
        "vip",
        "AT",
        [LineItem("Notebook", Decimal("100.00"), 1, Decimal("1.5"))],
    )
    # 100.00 - 10.00 + 7.99
    assert order.total(fake_shipping, today=IM_JUNI) == Decimal("97.99")


def test_regular_zahlt_ohne_rabatt(fake_shipping):
    order = Order(
        "regular",
        "DE",
        [LineItem("Maus", Decimal("20.00"), 2, Decimal("0.2"))],
    )
    # 40.00 - 0.00 + 4.99
    assert order.total(fake_shipping, today=IM_JUNI) == Decimal("44.99")


def test_fake_kennt_nur_die_eigene_tabelle(fake_shipping):
    order = Order("vip", "CH", [LineItem("Kabel", Decimal("9.00"), 1)])
    with pytest.raises(ValueError):
        order.total(fake_shipping, today=IM_JUNI)


def test_leere_bestellung_hat_keinen_warenwert(fake_shipping):
    order = Order("regular", "DE", [])
    assert order.subtotal() == Decimal("0.00")
    assert order.total_weight() == Decimal("0")
    assert order.total(fake_shipping, today=IM_JUNI) == Decimal("4.99")
