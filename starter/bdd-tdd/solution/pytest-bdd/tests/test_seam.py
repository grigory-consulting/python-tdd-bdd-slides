"""Seam um den Remote-Aufruf.

Ein Seam ist eine Stelle, an der
Sie das Verhalten aendern koennen, ohne an dieser Stelle zu editieren.
https://martinfowler.com/bliki/LegacySeam.html

Zu jedem Seam gehoert ein Enabling Point: die Stelle, an der entschieden
wird, welches Verhalten gilt. Hier liegt er im Testcode.
"""

import pytest

from shop import legacy_pricing

ZWEI_ARTIKEL = [{"price": 10.0, "qty": 2}]


def test_ohne_seam_ist_der_code_nicht_testbar():
    """Zeigt zuerst, warum ein Seam ueberhaupt noetig ist."""
    with pytest.raises(RuntimeError):
        legacy_pricing.calculate_order_total(ZWEI_ARTIKEL, "regular")


def test_seam_als_parameter():
    """Parameter-Seam: einmal in die Signatur geschrieben, danach nie wieder."""
    result = legacy_pricing.calculate_order_total(
        ZWEI_ARTIKEL, "regular", shipping_fn=lambda region: 4.99
    )
    assert result == 28.79


def test_seam_als_parameter_mit_anderem_wert():
    """Der Enabling Point liegt im Test: neue Faelle ohne Eingriff im Modul."""
    result = legacy_pricing.calculate_order_total(
        ZWEI_ARTIKEL, "regular", shipping_fn=lambda region: 0.0
    )
    assert result == 23.8


def test_seam_ueber_den_modulnamen(monkeypatch):
    """Modul-Seam: kein Eingriff in die Signatur noetig.

    Der Name ``fetch_shipping_cost`` wird erst zur Laufzeit im Modul
    nachgeschlagen. In Python genuegt deshalb ``monkeypatch.setattr``.
    """
    monkeypatch.setattr(legacy_pricing, "fetch_shipping_cost", lambda region: 0.0)
    assert legacy_pricing.calculate_order_total(ZWEI_ARTIKEL, "regular") == 23.8


def test_der_seam_bekommt_die_region_zu_sehen(monkeypatch):
    gesehen = []

    def stub(region):
        gesehen.append(region)
        return 1.0

    monkeypatch.setattr(legacy_pricing, "fetch_shipping_cost", stub)
    legacy_pricing.calculate_order_total(ZWEI_ARTIKEL, "regular", region="CH")
    assert gesehen == ["CH"]


def test_der_echte_dienst_bleibt_nach_dem_test_unveraendert():
    with pytest.raises(RuntimeError):
        legacy_pricing.fetch_shipping_cost("DE")
