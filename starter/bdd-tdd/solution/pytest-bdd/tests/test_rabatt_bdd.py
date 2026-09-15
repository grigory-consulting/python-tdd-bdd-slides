"""Dieselbe Feature-Datei wie behave, nur unter pytest.

pytest-bdd braucht keinen eigenen Runner: `scenarios()` erzeugt aus jedem
Szenario der Feature-Datei eine ganz normale pytest-Testfunktion. Zustand wandert
nicht über ein Context-Objekt, sondern über Fixtures (`target_fixture`), die
pytest per Dependency Injection an die folgenden Steps weitergibt.
"""

from decimal import Decimal
import pytest

from pytest_bdd import given, parsers, scenarios, then, when

from shop.discount import calculate_discount, payable_total

# Bindet alle Szenarien der Datei an Testfunktionen dieses Moduls.
scenarios("../features/rabatt.feature", "../features/coupon.feature")


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
