"""Preis-Code aus dem Altbestand, nach Lab 4.

Stand nach den fuenf Schritten des Labs:

1. Verhalten festgenagelt (``tests/test_characterization.py``).
2. Golden Master fuer den Preisreport (``tests/test_approval_report.py``).
3. Seam eingeführt: ``calculate_order_total(..., shipping_fn=None)``.
4. Unter gruener Suite refaktoriert (Extract Function, siehe REFACTORING.md).
5. Erst danach der Bugfix: Untergrenze 0.00 beim Coupon (siehe BUGFIX.md).

Das Modul rechnet weiterhin mit ``float``, nicht mit ``Decimal``. Das ist
Absicht: der Umbau auf ``Decimal`` wuerde Zahlen aendern und braucht eine
eigene fachliche Entscheidung. Die Reihenfolge der Rechenschritte ist beim
Refactoring unveraendert geblieben, damit die gepinnten Werte gelten.
"""

VAT = {"DE": 0.19, "CH": 0.081, "US": 0.0}

#: Rueckfall fuer unbekannte Regionen (Verhalten des Altbestands).
DEFAULT_VAT = 0.19

#: Stiller Nachlass auf Buecher. Beim Charakterisieren gefunden, nicht erfunden.
BOOK_FACTOR = 0.93

#: Untergrenze fuer den Warenwert vor Steuer (Bugfix, Schritt 5).
MINIMUM_NET_TOTAL = 0.0


def fetch_shipping_cost(region):
    """Steht fuer einen langsamen, teuren Remote-Aufruf.

    Im Testlauf ist der Dienst nicht erreichbar. Genau deshalb brauchen wir
    einen Seam, um das Verhalten an dieser Stelle zu ersetzen, ohne an
    dieser Stelle zu editieren.
    """
    raise RuntimeError(
        "shipping service not reachable - this is the dependency we need a seam for"
    )


def _line_price(item):
    """Preis einer Zeile inklusive der impliziten Buchpreisregel."""
    price = item["price"] * item.get("qty", 1)
    if item.get("category") == "book":
        price = price * BOOK_FACTOR
    return price


def _items_total(items):
    total = 0.0
    for item in items:
        total += _line_price(item)
    return total


def _apply_customer_discount(total, customer_type):
    """VIP 10 Prozent, Mitarbeitende 50 Prozent, alle anderen nichts."""
    if customer_type == "vip":
        return total - total * 0.1
    if customer_type == "staff":
        return total * 0.5
    return total


def _apply_coupon(total, coupon):
    """Coupon-Abzug VOR der Steuer."""
    if not coupon:
        return total
    if coupon.startswith("SAVE"):
        return total - int(coupon[4:])
    if coupon == "FREESHIP":
        return total - 4.99   # zieht vom Warenwert ab, nicht vom Versand
    return total


def _apply_vat(total, region):
    return total * (1 + VAT.get(region, DEFAULT_VAT))


def calculate_price(items, customer_type, coupon=None, region="DE"):
    """Bruttopreis eines Warenkorbs, auf zwei Stellen gerundet."""
    total = _items_total(items)
    total = _apply_customer_discount(total, customer_type)
    total = _apply_coupon(total, coupon)
    # Bugfix (Schritt 5): der Coupon darf den Warenwert nicht unter null
    # druecken. Vorher wurde die Mehrwertsteuer auf einen negativen Betrag
    # gerechnet. Begruendung in BUGFIX.md.
    total = max(total, MINIMUM_NET_TOTAL)
    total = _apply_vat(total, region)
    return round(total, 2)


def calculate_order_total(items, customer_type, coupon=None, region="DE",
                          shipping_fn=None):
    """Warenwert plus Versand.

    ``shipping_fn`` ist der eingeführte Seam. Er wurde einmal in die Signatur
    geschrieben; ab jetzt liegt der Enabling Point im Testcode, und der
    Produktionscode muss dafuer nicht mehr angefasst werden. Ohne Argument
    bleibt das Verhalten des Altbestands unveraendert. Weil der Name
    ``fetch_shipping_cost`` erst zur Laufzeit im Modul nachgeschlagen wird,
    funktioniert alternativ auch der Modul-Seam per ``monkeypatch.setattr``.
    """
    shipping_fn = shipping_fn or fetch_shipping_cost
    return round(
        calculate_price(items, customer_type, coupon, region) + shipping_fn(region), 2
    )
