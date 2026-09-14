"""Aufgabe b: Mock mit spec. Geprueft wird die Interaktion, also der Aufruf."""

from datetime import date
from decimal import Decimal
from unittest.mock import Mock

import pytest

from shop.order import LineItem, Order
from shop.shipping import ShippingService

IM_JUNI = date(2026, 6, 15)


def test_versanddienst_wird_mit_land_und_gewicht_aufgerufen(standardbestellung):
    # TODO Aufgabe b, Schritt 1: Mock(spec=ShippingService) erzeugen.
    # TODO Aufgabe b, Schritt 2: cost_for.return_value auf Decimal("4.99") setzen.
    shipping = None

    result = standardbestellung.total(shipping, today=IM_JUNI)

    # Zustand: das Ergebnis stimmt.
    assert result == Decimal("94.99")
    # TODO Aufgabe b, Schritt 3: Interaktion pruefen mit
    #      shipping.cost_for.assert_called_once_with("DE", Decimal("1.5"))


def test_bei_freiem_versand_wird_der_dienst_gar_nicht_gefragt():
    order = Order(
        "regular",
        "DE",
        [LineItem("Monitor", Decimal("250.00"), 1, Decimal("5.0"))],
    )
    shipping = Mock(spec=ShippingService)

    result = order.total(shipping, today=IM_JUNI)

    assert result == Decimal("250.00")
    # TODO Aufgabe b, Schritt 4: zeigen, dass der Dienst nicht gefragt wurde.
    pytest.fail("TODO Aufgabe b: passende Zusicherung fuer 'nicht aufgerufen' ergaenzen")
