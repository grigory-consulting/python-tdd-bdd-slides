"""Aufgabe e: monkeypatch als pytest-eigene Alternative zu patch().

``monkeypatch`` setzt Attribute, Dictionary-Eintraege und Umgebungsvariablen
und macht alles nach dem Test wieder rueckgaengig. Es braucht keinen
``with``-Block und keinen Dekorator.
"""

from datetime import date
from decimal import Decimal

import shop.order as order_module
import shop.shipping as shipping_module
from shop.shipping import COUNTRY_ENV, default_country

IM_JUNI = date(2026, 6, 15)
IM_DEZEMBER = date(2026, 12, 5)


def test_setenv_setzt_das_zielland(monkeypatch):
    monkeypatch.setenv(COUNTRY_ENV, "AT")
    assert default_country() == "AT"


def test_delenv_faellt_auf_de_zurueck(monkeypatch):
    monkeypatch.delenv(COUNTRY_ENV, raising=False)
    assert default_country() == "DE"


def test_setattr_ersetzt_die_uhr(monkeypatch, standardbestellung, fake_shipping):
    """Ohne ``today``-Argument fragt der Code ``today_provider()``."""
    monkeypatch.setattr(order_module, "today_provider", lambda: IM_DEZEMBER)
    assert standardbestellung.total(fake_shipping) == Decimal("90.00")


def test_setattr_zurueck_auf_einen_normalen_tag(monkeypatch, standardbestellung, fake_shipping):
    monkeypatch.setattr(order_module, "today_provider", lambda: IM_JUNI)
    assert standardbestellung.total(fake_shipping) == Decimal("94.99")


def test_setattr_auf_die_modulfunktion_wirkt_nur_am_lookup_ort(
    monkeypatch, standardbestellung
):
    """Dieselbe Regel wie bei patch(): der gebundene Name zaehlt."""
    monkeypatch.setattr(order_module, "fetch_rate", lambda country: Decimal("4.99"))
    assert standardbestellung.total_via_rate_lookup(today=IM_JUNI) == Decimal("94.99")

    # Zur Gegenprobe das Original im Definitionsmodul: unveraendert und laut.
    assert shipping_module.fetch_rate is not order_module.fetch_rate
