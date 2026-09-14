"""Aufgabe e: monkeypatch als pytest-eigene Alternative zu patch().

``monkeypatch`` setzt Attribute, Dictionary-Eintraege und Umgebungsvariablen
und macht alles nach dem Test wieder rueckgaengig.
https://docs.pytest.org/en/stable/how-to/monkeypatch.html
"""

from datetime import date
from decimal import Decimal

import pytest

import shop.order as order_module
from shop.shipping import COUNTRY_ENV, default_country

IM_DEZEMBER = date(2026, 12, 5)


def test_setenv_setzt_das_zielland(monkeypatch):
    # TODO Aufgabe e, Schritt 1: COUNTRY_ENV per monkeypatch.setenv auf "AT"
    #      setzen und default_country() pruefen.
    assert default_country() == "AT"


def test_setattr_ersetzt_die_uhr(monkeypatch, standardbestellung, fake_shipping):
    """Ohne ``today``-Argument fragt der Code ``today_provider()``."""
    # TODO Aufgabe e, Schritt 2: order_module.today_provider per
    #      monkeypatch.setattr durch eine Funktion ersetzen, die IM_DEZEMBER
    #      liefert. Danach total() OHNE today-Argument aufrufen.
    assert standardbestellung.total(fake_shipping) == Decimal("90.00")
