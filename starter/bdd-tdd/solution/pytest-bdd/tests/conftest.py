"""Gemeinsame Testdoubles und Fixtures.

Der Fake ist eine echte, aber vereinfachte Implementierung: er rechnet,
statt nur aufzuzeichnen. Deshalb pruefen Tests mit dem Fake den *Zustand*
(das Ergebnis), nicht die Interaktion.
"""

from decimal import Decimal

import pytest

from shop.order import LineItem, Order


class FakeShippingService:
    """Feste Preistabelle statt HTTP. Das Gewicht spielt bewusst keine Rolle."""

    RATES = {
        "DE": Decimal("4.99"),
        "AT": Decimal("7.99"),
    }

    def __init__(self):
        #: nur zur Anschauung; ein Fake darf mitschreiben, muss aber nicht
        self.calls = []

    def cost_for(self, country: str, weight_kg: Decimal) -> Decimal:
        self.calls.append((country, weight_kg))
        try:
            return self.RATES[country]
        except KeyError:
            raise ValueError(f"kein Versandtarif fuer {country!r}") from None


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
