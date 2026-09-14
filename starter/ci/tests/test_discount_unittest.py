"""Dieselben Fälle noch einmal mit unittest, zum direkten Vergleich (Lab 2).

Fachlich identisch zu den Fällen 1, 2 und 5 aus ``test_discount.py``.
Unterschiedlich ist nur die Mechanik:

===========================  ==========================================
pytest                       unittest
===========================  ==========================================
Modulfunktion ``test_...``   Methode in einer ``unittest.TestCase``
Fixture als Parameter        ``setUp`` (und ``tearDown``)
``assert x == y``            ``self.assertEqual(x, y)``
``pytest.raises``            ``self.assertRaises``
``@pytest.mark.parametrize`` ``subTest`` oder eine eigene Schleife
===========================  ==========================================

pytest sammelt und startet diese Klasse mit, ohne dass etwas umgestellt werden
muss. Umgekehrt gilt das nicht: die parametrisierten Tests der anderen Datei
sind für den unittest-Runner unsichtbar.

Eigenständig ausführbar, ohne pytest. ``pythonpath`` aus ``pyproject.toml``
gilt nur für pytest, deshalb wird der Suchpfad hier von Hand gesetzt:

    macOS, Linux:       PYTHONPATH=src python tests/test_discount_unittest.py -v
    Windows PowerShell: $env:PYTHONPATH="src"; python tests\test_discount_unittest.py -v

Oder über die Testerkennung von unittest (``-t tests``, weil ``tests/`` kein
``__init__.py`` hat):

    macOS, Linux:       PYTHONPATH=src python -m unittest discover -s tests -t tests
    Windows PowerShell: $env:PYTHONPATH="src"; python -m unittest discover -s tests -t tests

Beide Aufrufe melden ``Ran 3 tests ... OK``.
"""

import unittest
from decimal import Decimal

from shop.discount import calculate_discount


class CalculateDiscountTest(unittest.TestCase):
    def setUp(self):
        self.warenkorb = Decimal("100.00")

    def test_stammkunde_bekommt_keinen_rabatt(self):
        self.assertEqual(
            calculate_discount("regular", self.warenkorb), Decimal("0.00")
        )

    def test_vip_bekommt_zehn_prozent(self):
        self.assertEqual(calculate_discount("vip", self.warenkorb), Decimal("10.00"))

    def test_negativer_warenkorb_wird_abgelehnt(self):
        with self.assertRaises(ValueError):
            calculate_discount("vip", Decimal("-1.00"))


if __name__ == "__main__":
    unittest.main()
