"""Bestellung mit externen Kollaboratoren (Versandkosten, Datum).

Drei Seams fuer den Test:

1. ``Order.total(shipping, today)`` bekommt den Versanddienst als Parameter.
   Fake oder Mock werden einfach hereingereicht.
2. ``Order.total_via_rate_lookup(today)`` benutzt die Modulfunktion
   ``fetch_rate``, die dieses Modul per ``from``-Import gebunden hat.
   Gepatcht wird deshalb ``shop.order.fetch_rate``.
3. ``today_provider()`` kapselt die Uhr. Wer kein ``today`` uebergibt,
   bekommt das Systemdatum; im Test genuegt ``monkeypatch.setattr``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import List, Optional

from shop.discount import calculate_discount
from shop.shipping import ShippingService, fetch_rate  # Lookup-Stelle: "shop.order.fetch_rate"

#: Ab diesem Warenkorbwert (inklusive) ist der Versand frei.
FREE_SHIPPING_FROM = Decimal("200.00")

#: Im Dezember ist der Versand frei.
FREE_SHIPPING_MONTH = 12

ZERO = Decimal("0.00")


def today_provider() -> date:
    """Ersetzbare Zeitquelle.

    Im Test: ``monkeypatch.setattr(shop.order, "today_provider", lambda: date(...))``.
    """
    return date.today()


@dataclass(frozen=True)
class LineItem:
    name: str
    unit_price: Decimal
    quantity: int = 1
    weight_kg: Decimal = Decimal("0")


@dataclass
class Order:
    customer_type: str
    country: str
    items: List[LineItem] = field(default_factory=list)

    def subtotal(self) -> Decimal:
        return sum((item.unit_price * item.quantity for item in self.items), ZERO)

    def total_weight(self) -> Decimal:
        return sum((item.weight_kg * item.quantity for item in self.items), Decimal("0"))

    def shipping_is_free(self, today: Optional[date] = None) -> bool:
        """Versand frei ab 200.00 oder im Dezember."""
        day = today if today is not None else today_provider()
        return self.subtotal() >= FREE_SHIPPING_FROM or day.month == FREE_SHIPPING_MONTH

    def total(self, shipping: ShippingService, today: Optional[date] = None) -> Decimal:
        """subtotal - Rabatt + Versand.

        Versand entfaellt bei subtotal >= 200.00 oder im Dezember.
        """
        subtotal = self.subtotal()
        discount = calculate_discount(self.customer_type, subtotal)
        if self.shipping_is_free(today):
            return subtotal - discount
        return subtotal - discount + shipping.cost_for(self.country, self.total_weight())

    def total_via_rate_lookup(self, today: Optional[date] = None) -> Decimal:
        """Wie ``total``, aber der Versandpreis kommt aus der Modulfunktion.

        Kein Kollaborator wird hereingereicht. Ersetzt wird deshalb der Name,
        den *dieses* Modul gebunden hat: ``shop.order.fetch_rate``.
        """
        subtotal = self.subtotal()
        discount = calculate_discount(self.customer_type, subtotal)
        if self.shipping_is_free(today):
            return subtotal - discount
        return subtotal - discount + fetch_rate(self.country)
