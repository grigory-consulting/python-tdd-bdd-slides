"""Rabattregeln des Kursprojekts "Rabattshop".

Beträge sind immer ``Decimal``, niemals ``float``: in Geldrechnungen ist
``0.1 + 0.2 != 0.3`` kein akademisches Problem, sondern ein Cent im Beleg.
Gerundet wird kaufmännisch, also ``ROUND_HALF_UP`` auf zwei Nachkommastellen,
und nicht mit dem Standardmodus ``ROUND_HALF_EVEN``.

Fachliche Regeln:

* ``regular`` bekommt keinen Grundrabatt.
* ``vip`` bekommt 10 Prozent Grundrabatt.
* Staffel: ab einem Warenkorbwert von 500.00 (einschließlich) kommen
  5 Prozentpunkte hinzu, für beide Kundentypen.
* Ein negativer Warenkorbwert und ein unbekannter Kundentyp sind Fehler.

Dieses Modul ist testgetrieben entstanden. Die sieben Schritte stehen in
``TDD_LOG.md``, der Refactoring-Schritt am Ende in ``REFACTORING.md``.
"""

from decimal import ROUND_HALF_UP, Decimal

CUSTOMER_TYPES = ("regular", "vip")

_BASE_RATES = {
    "regular": Decimal("0.00"),
    "vip": Decimal("0.10"),
}
_VOLUME_THRESHOLD = Decimal("500.00")
_VOLUME_BONUS_RATE = Decimal("0.05")
_CENT = Decimal("0.01")


def calculate_discount(customer_type: str, subtotal: Decimal) -> Decimal:
    """Rabattbetrag (nicht der Endpreis), auf Cent gerundet (ROUND_HALF_UP).

    :raises ValueError: bei unbekanntem Kundentyp oder negativem Warenkorbwert.
    """
    _reject_invalid_input(customer_type, subtotal)
    return _to_cents(subtotal * _discount_rate(customer_type, subtotal))


def payable_total(customer_type: str, subtotal: Decimal) -> Decimal:
    """subtotal minus Rabatt."""
    return subtotal - calculate_discount(customer_type, subtotal)


def _reject_invalid_input(customer_type: str, subtotal: Decimal) -> None:
    """Wächterklauseln: ungültige Eingaben verlassen die Funktion sofort.

    Die Reihenfolge stammt aus der Entstehung des Moduls und bleibt bewusst
    erhalten. Beobachtbar ist sie nur bei doppelt ungültiger Eingabe, etwa
    ``("gold", Decimal("-1.00"))``, und dafür gibt es keine Anforderung.
    Siehe REFACTORING.md, Abschnitt "Was bewusst nicht geändert wurde".
    """
    if subtotal < 0:
        raise ValueError(f"Warenkorbwert darf nicht negativ sein: {subtotal}")
    if customer_type not in CUSTOMER_TYPES:
        raise ValueError(f"unbekannter Kundentyp: {customer_type!r}")


def _discount_rate(customer_type: str, subtotal: Decimal) -> Decimal:
    """Rabattsatz als Anteil, zum Beispiel Decimal("0.15") für 15 Prozent."""
    rate = _BASE_RATES[customer_type]
    if subtotal >= _VOLUME_THRESHOLD:
        rate += _VOLUME_BONUS_RATE
    return rate


def _to_cents(amount: Decimal) -> Decimal:
    """Kaufmännisch auf zwei Nachkommastellen runden."""
    return amount.quantize(_CENT, rounding=ROUND_HALF_UP)
