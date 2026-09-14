"""Golden Master fuer einen mehrzeiligen Preisreport (ApprovalTests).

Ein Approval Test vergleicht eine ganze Ausgabe mit einer freigegebenen
Datei (``*.approved.txt``). Das lohnt sich, sobald ein Ergebnis aus vielen
Werten besteht: Sie schreiben einmal den Report, statt zwanzig einzelne
Assertions zu pflegen.
https://github.com/approvals/ApprovalTests.Python

Wichtig fuer den Kurs: Der Report wird hier im Test gebaut, nicht im
Legacy-Modul. Wer Legacy-Code anfassen will, braucht vorher Tests - also
fassen wir ihn zuerst nicht an.

Reporter: Standardmaessig oeffnet ApprovalTests bei einer Abweichung ein
Diff-Werkzeug. Das ist am Arbeitsplatz praktisch, in CI und in einer Sandbox
aber falsch. ``PythonNativeReporter`` gibt den Unterschied stattdessen als
Text in der Fehlermeldung aus.
"""

import pytest

from shop import legacy_pricing

approvaltests = pytest.importorskip(
    "approvaltests",
    reason="approvaltests nicht installiert: pip install approvaltests",
)

from approvaltests import Options, verify  # noqa: E402
from approvaltests.reporters import PythonNativeReporter  # noqa: E402

FAELLE = [
    ("zwei Artikel je 10.00", [{"price": 10.0, "qty": 2}], "regular", None, "DE"),
    ("ein Buch 10.00", [{"price": 10.0, "qty": 1, "category": "book"}], "regular", None, "DE"),
    ("VIP, Artikel 100.00", [{"price": 100.0, "qty": 1}], "vip", None, "DE"),
    ("Mitarbeitende, 100.00", [{"price": 100.0, "qty": 1}], "staff", None, "DE"),
    ("Buch mit SAVE20", [{"price": 10.0, "qty": 1, "category": "book"}], "regular", "SAVE20", "DE"),
    ("VIP mit SAVE20", [{"price": 100.0, "qty": 1}], "vip", "SAVE20", "DE"),
    ("FREESHIP auf 20.00", [{"price": 10.0, "qty": 2}], "regular", "FREESHIP", "DE"),
    ("Schweiz", [{"price": 10.0, "qty": 2}], "regular", None, "CH"),
    ("USA", [{"price": 10.0, "qty": 2}], "regular", None, "US"),
    ("unbekannte Region XX", [{"price": 10.0, "qty": 2}], "regular", None, "XX"),
    ("leerer Warenkorb", [], "regular", None, "DE"),
]

KOPF = (
    "Fall                      | Kunde   | Coupon   | Region | Preis\n"
    "--------------------------+---------+----------+--------+---------"
)


def preisreport() -> str:
    zeilen = ["Preisreport (legacy_pricing.calculate_price)", "=" * 43, "", KOPF]
    for name, items, customer_type, coupon, region in FAELLE:
        preis = legacy_pricing.calculate_price(items, customer_type, coupon, region)
        zeilen.append(
            "{:<25} | {:<7} | {:<8} | {:<6} | {:>7.2f}".format(
                name, customer_type, coupon or "-", region, preis
            )
        )
    return "\n".join(zeilen) + "\n"


def test_preisreport():
    """Vergleicht den Report mit test_approval_report.test_preisreport.approved.txt."""
    verify(preisreport(), options=Options().with_reporter(PythonNativeReporter()))
