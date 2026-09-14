"""Aufgabe b: Mock mit spec. Geprueft wird die Interaktion, also der Aufruf.

``spec=ShippingService`` sorgt dafuer, dass ein Tippfehler im Methodennamen
sofort einen ``AttributeError`` ausloest, statt still einen neuen Mock zu
erfinden.
"""

from datetime import date
from decimal import Decimal
from unittest.mock import Mock

import pytest

from shop.order import LineItem, Order
from shop.shipping import ShippingService

IM_JUNI = date(2026, 6, 15)


def test_versanddienst_wird_mit_land_und_gewicht_aufgerufen(standardbestellung):
    shipping = Mock(spec=ShippingService)
    shipping.cost_for.return_value = Decimal("4.99")

    result = standardbestellung.total(shipping, today=IM_JUNI)

    # Zustand: das Ergebnis stimmt.
    assert result == Decimal("94.99")
    # Interaktion: der Dienst wurde genau einmal und mit den richtigen
    # Argumenten gefragt. Diese Zusicherung ist hier fachlich, weil ein
    # falsches Land oder ein falsches Gewicht einen falschen Preis erzeugt.
    shipping.cost_for.assert_called_once_with("DE", Decimal("1.5"))


def test_bei_freiem_versand_wird_der_dienst_gar_nicht_gefragt():
    order = Order(
        "regular",
        "DE",
        [LineItem("Monitor", Decimal("250.00"), 1, Decimal("5.0"))],
    )
    shipping = Mock(spec=ShippingService)

    result = order.total(shipping, today=IM_JUNI)

    assert result == Decimal("250.00")
    shipping.cost_for.assert_not_called()


def test_spec_schuetzt_vor_tippfehlern():
    shipping = Mock(spec=ShippingService)
    with pytest.raises(AttributeError):
        shipping.cost_for_country("DE", Decimal("1.5"))
