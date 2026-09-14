"""Externe Versandkosten. Im Test darf hier nichts wirklich laufen.

Beide Formen kommen in echten Projekten vor und werden im Test
unterschiedlich ersetzt:

* ``ShippingService`` ist ein Kollaborator-Objekt. Es wird von aussen
  hereingereicht und laesst sich deshalb durch einen Fake oder einen Mock
  ersetzen, ohne dass irgendwo gepatcht werden muss.
* ``fetch_rate`` ist eine Modulfunktion. ``order.py`` holt sie per
  ``from``-Import. Ersetzt wird sie deshalb an der Stelle, an der sie
  nachgeschlagen wird: ``shop.order.fetch_rate``.
"""

import os
from decimal import Decimal

#: Umgebungsvariable fuer das Standard-Zielland (Beispiel fuer monkeypatch.setenv).
COUNTRY_ENV = "SHOP_COUNTRY"


class ShippingService:
    """Stellvertreter fuer einen HTTP-Dienst. Ein echter Aufruf ist im Test verboten."""

    def cost_for(self, country: str, weight_kg: Decimal) -> Decimal:
        raise RuntimeError("Netzwerkzugriff: im Test nicht erlaubt")


def fetch_rate(country: str) -> Decimal:
    """Modulfunktion, ebenfalls 'extern'; wird von order.py per from-Import geholt."""
    raise RuntimeError("Netzwerkzugriff: im Test nicht erlaubt")


def default_country() -> str:
    """Zielland aus der Umgebung, sonst ``DE``.

    Bewusst klein gehalten: Diese Funktion ist das Beispiel fuer
    ``monkeypatch.setenv`` im Lab.
    """
    return os.environ.get(COUNTRY_ENV, "DE")
