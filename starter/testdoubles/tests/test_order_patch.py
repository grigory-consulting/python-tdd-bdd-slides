"""Aufgabe c: patch() an der Lookup-Stelle.

Regel aus der Python-Dokumentation ("Where to patch"):
Sie patchen den Namen dort, wo er *nachgeschlagen* wird, nicht dort, wo er
definiert ist. https://docs.python.org/3/library/unittest.mock.html#where-to-patch

Sehen Sie sich vorher den Importkopf von ``src/shop/order.py`` an.
"""

from datetime import date
from decimal import Decimal
from unittest.mock import patch

import pytest

IM_JUNI = date(2026, 6, 15)


def test_patch_an_der_lookup_stelle_wirkt(standardbestellung):
    # TODO Aufgabe c, Schritt 1: den richtigen Patch-Pfad einsetzen.
    #      Erwartetes Ergebnis: Decimal("94.99").
    with patch("shop.???.fetch_rate", return_value=Decimal("4.99")) as rate:
        result = standardbestellung.total_via_rate_lookup(today=IM_JUNI)

    assert result == Decimal("94.99")
    rate.assert_called_once_with("DE")


def test_patch_an_der_definitionsstelle_wirkt_nicht(standardbestellung):
    """Derselbe Patch am falschen Ort laesst den echten Aufruf durch."""
    # TODO Aufgabe c, Schritt 2: denselben Patch auf shop.shipping.fetch_rate
    #      setzen und zeigen, dass jetzt der echte Aufruf laeuft.
    #      Tipp: pytest.raises(RuntimeError).
    pytest.fail("TODO Aufgabe c: Gegenprobe mit shop.shipping.fetch_rate schreiben")
