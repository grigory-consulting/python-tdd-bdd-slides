"""Gemeinsame Testdoubles und Fixtures.

AUFGABE a: Vervollstaendigen Sie ``FakeShippingService``.
Ein Fake ist eine echte, aber vereinfachte Implementierung. Er rechnet,
statt nur aufzuzeichnen.
"""

from decimal import Decimal

import pytest

from shop.order import LineItem, Order


class FakeShippingService:
    """Feste Preistabelle statt HTTP. Das Gewicht spielt bewusst keine Rolle."""

    # TODO Aufgabe a: Tabelle fuellen. DE kostet 4.99, AT kostet 7.99.
    #                 Betraege als Decimal, nicht als float.
    RATES: dict = {}

    def __init__(self):
        self.calls = []

    def cost_for(self, country: str, weight_kg: Decimal) -> Decimal:
        self.calls.append((country, weight_kg))
        # TODO Aufgabe a: Tarif aus RATES liefern.
        #                 Unbekanntes Land: ValueError werfen.
        raise NotImplementedError("TODO Aufgabe a: FakeShippingService.cost_for")


@pytest.fixture
def fake_shipping() -> FakeShippingService:
    return FakeShippingService()


@pytest.fixture
def standardbestellung() -> Order:
    """VIP, Lieferung nach DE, ein Notebook zu 100.00 EUR mit 1.5 kg."""
    return Order(
        "vip",
        "DE",
        [LineItem("Notebook", Decimal("100.00"), 1, Decimal("1.5"))],
    )
