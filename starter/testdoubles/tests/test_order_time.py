"""Aufgabe d: Zeit ist ein Kollaborator wie jeder andere.

Statt die Uhr zu patchen, wird das Datum hereingereicht. Der Test wird
dadurch deterministisch und lesbar.
"""

from datetime import date
from decimal import Decimal

from shop.order import LineItem, Order

IM_JUNI = date(2026, 6, 15)
IM_DEZEMBER = date(2026, 12, 5)


def test_im_dezember_ist_der_versand_frei(standardbestellung, fake_shipping):
    # TODO Aufgabe d, Schritt 1: total() mit today=IM_DEZEMBER aufrufen.
    #      Erwartung: 100.00 - 10.00 + 0.00 = Decimal("90.00").
    #      Zusatz: pruefen Sie ueber fake_shipping.calls, dass der Dienst
    #      gar nicht erst gefragt wurde.
    result = None
    assert result == Decimal("90.00")


def test_ab_200_euro_ist_der_versand_frei(fake_shipping):
    order = Order(
        "regular",
        "DE",
        [LineItem("Monitor", Decimal("200.00"), 1, Decimal("5.0"))],
    )
    # TODO Aufgabe d, Schritt 2: Erwartung fuer die Grenze 200.00 formulieren.
    #      Schreiben Sie danach den Gegentest fuer 199.99.
    result = None
    assert result == Decimal("200.00")
