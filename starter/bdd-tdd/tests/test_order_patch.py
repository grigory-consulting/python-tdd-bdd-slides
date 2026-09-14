"""Aufgabe c: patch() an der Lookup-Stelle.

Regel aus der Python-Dokumentation ("Where to patch"):
Sie patchen den Namen dort, wo er *nachgeschlagen* wird, nicht dort, wo er
definiert ist. https://docs.python.org/3/library/unittest.mock.html#where-to-patch

``shop/order.py`` enthaelt ``from shop.shipping import fetch_rate``. Damit
existiert der Name ``fetch_rate`` ein zweites Mal, naemlich im Modul
``shop.order``. Genau dieser zweite Name wird beim Aufruf benutzt.
"""

from datetime import date
from decimal import Decimal
from unittest.mock import patch

import pytest

IM_JUNI = date(2026, 6, 15)


def test_patch_an_der_lookup_stelle_wirkt(standardbestellung):
    with patch("shop.order.fetch_rate", return_value=Decimal("4.99")) as rate:
        result = standardbestellung.total_via_rate_lookup(today=IM_JUNI)

    assert result == Decimal("94.99")
    rate.assert_called_once_with("DE")


def test_patch_an_der_definitionsstelle_wirkt_nicht(standardbestellung):
    """Derselbe Patch am falschen Ort laesst den echten Aufruf durch.

    ``shop.order`` hat den Namen beim Import gebunden. Wer ``shop.shipping``
    patcht, tauscht ein Etikett aus, das niemand mehr liest. Der echte
    ``fetch_rate`` laeuft weiter und wirft ``RuntimeError``.
    """
    with patch("shop.shipping.fetch_rate", return_value=Decimal("4.99")):
        with pytest.raises(RuntimeError):
            standardbestellung.total_via_rate_lookup(today=IM_JUNI)


def test_ohne_patch_schlaegt_der_netzzugriff_fehl(standardbestellung):
    with pytest.raises(RuntimeError):
        standardbestellung.total_via_rate_lookup(today=IM_JUNI)


def test_echter_shipping_service_ist_im_test_gesperrt(standardbestellung):
    from shop.shipping import ShippingService

    with pytest.raises(RuntimeError):
        standardbestellung.total(ShippingService(), today=IM_JUNI)


def test_bei_freiem_versand_wird_die_modulfunktion_nicht_gefragt():
    """Ohne Patch: wuerde ``fetch_rate`` laufen, gaebe es einen RuntimeError."""
    from shop.order import LineItem, Order

    order = Order(
        "regular",
        "DE",
        [LineItem("Monitor", Decimal("250.00"), 1, Decimal("5.0"))],
    )
    assert order.total_via_rate_lookup(today=IM_JUNI) == Decimal("250.00")
