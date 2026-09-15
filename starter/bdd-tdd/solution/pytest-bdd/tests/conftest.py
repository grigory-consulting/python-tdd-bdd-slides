"""Gemeinsame Testdoubles, Fixtures und BDD-Steps.

Der Fake ist eine echte, aber vereinfachte Implementierung: er rechnet,
statt nur aufzuzeichnen. Deshalb pruefen Tests mit dem Fake den *Zustand*
(das Ergebnis), nicht die Interaktion.
"""

from decimal import Decimal

import pytest
from pytest_bdd import given, parsers, then, when

from shop.discount import calculate_discount, payable_total
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


# Gemeinsame BDD-Steps für alle Szenarien unter tests/.

@given(parsers.parse('ein Kunde vom Typ "{customer_type}"'), target_fixture="kundentyp")
def given_kundentyp(customer_type):
    return customer_type


@given(
    parsers.parse("ein Warenkorbwert von {amount} EUR"),
    target_fixture="warenkorbwert",
    converters={"amount": Decimal},
)
def given_warenkorbwert(amount):
    return amount


@when("der Rabatt berechnet wird", target_fixture="ergebnis")
def when_rabatt_berechnen(kundentyp, warenkorbwert, coupon):
    return {
        "rabatt": calculate_discount(kundentyp, warenkorbwert),
        "zahlbar": payable_total(kundentyp, warenkorbwert, coupon=coupon),
    }


@then(parsers.parse("beträgt der Rabatt {amount} EUR"), converters={"amount": Decimal})
def then_rabatt(ergebnis, amount):
    assert ergebnis["rabatt"] == amount, (
        f"Rabatt erwartet: {amount}, berechnet: {ergebnis['rabatt']}"
    )


@then(
    parsers.parse("beträgt der zahlbare Betrag {amount} EUR"),
    converters={"amount": Decimal},
)
def then_zahlbar(ergebnis, amount):
    assert ergebnis["zahlbar"] == amount, (
        f"Zahlbarer Betrag erwartet: {amount}, berechnet: {ergebnis['zahlbar']}"
    )


@pytest.fixture
def coupon():
    return None


@given(parsers.parse('ein Coupon "{code}"'), target_fixture="coupon")
def given_coupon(code):
    return code
