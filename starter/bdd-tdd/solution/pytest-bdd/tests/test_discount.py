"""Rabattregeln, testgetrieben entwickelt (Lab 2).

Die Reihenfolge unten entspricht der Testfallliste aus der Lab-Anleitung.
Jeder dieser Tests war einmal rot, bevor eine Zeile Produktivcode entstand;
der Weg dorthin steht Schritt für Schritt in ``TDD_LOG.md``.

Die Einzeltests aus dem Zyklus sind am Ende zu parametrisierten Tests
zusammengezogen worden. Das ist selbst ein Refactoring-Schritt, und zwar am
Testcode: gleiche Prüfung, viele Daten, ein Name je Datensatz.
"""

from decimal import Decimal

import pytest

from shop.discount import CUSTOMER_TYPES, calculate_discount, payable_total


@pytest.mark.parametrize(
    ("customer_type", "subtotal", "erwarteter_rabatt"),
    [
        # Fall 1: Stammkunde bekommt nichts.
        ("regular", "100.00", "0.00"),
        # Fall 2: VIP bekommt zehn Prozent.
        ("vip", "100.00", "10.00"),
        # Fall 3: Staffel ab 500.00 einschließlich, fünf Prozentpunkte mehr.
        ("regular", "500.00", "25.00"),
        ("vip", "500.00", "75.00"),
        ("vip", "499.99", "50.00"),
        # Fall 4: kaufmännische Rundung auf Cent.
        ("vip", "33.33", "3.33"),
        ("vip", "10.05", "1.01"),
    ],
    ids=[
        "regular-100-kein-rabatt",
        "vip-100-zehn-prozent",
        "regular-500-staffel",
        "vip-500-staffel",
        "vip-499.99-knapp-darunter",
        "vip-33.33-abrunden",
        "vip-10.05-aufrunden",
    ],
)
def test_rabattbetrag(customer_type, subtotal, erwarteter_rabatt):
    assert calculate_discount(customer_type, Decimal(subtotal)) == Decimal(
        erwarteter_rabatt
    )


def test_rabatt_ist_immer_auf_cent_gerundet():
    """Decimal("1.01") == Decimal("1.0100"), die Stellenzahl also extra prüfen."""
    rabatt = calculate_discount("vip", Decimal("33.33"))
    assert rabatt.as_tuple().exponent == -2


# Fall 5: negativer Warenkorb.
@pytest.mark.parametrize("customer_type", CUSTOMER_TYPES)
def test_negativer_warenkorb_wird_abgelehnt(customer_type):
    with pytest.raises(ValueError, match="negativ"):
        calculate_discount(customer_type, Decimal("-1.00"))


# Fall 6: unbekannter Kundentyp.
def test_unbekannter_kundentyp_wird_abgelehnt():
    with pytest.raises(ValueError, match="gold"):
        calculate_discount("gold", Decimal("100.00"))


# Fall 7: zahlbarer Betrag.
@pytest.mark.parametrize(
    ("customer_type", "subtotal", "erwarteter_betrag"),
    [
        ("vip", "100.00", "90.00"),
        ("regular", "100.00", "100.00"),
        ("vip", "500.00", "425.00"),
    ],
    ids=["vip-100", "regular-100", "vip-500-staffel"],
)
def test_zahlbarer_betrag(customer_type, subtotal, erwarteter_betrag):
    assert payable_total(customer_type, Decimal(subtotal)) == Decimal(
        erwarteter_betrag
    )
