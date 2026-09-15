"""Hooks fuer die behave-Laeufe des Kursprojekts.

Wichtig zur Ladereihenfolge von behave:
1. environment.py wird importiert,
2. danach werden die Module in features/steps/ importiert,
3. erst danach laeuft der Hook before_all().

Die Step-Module holen sich "shop.discount" bereits beim Import. Der Pfad auf
src/ muss deshalb schon in Schritt 1 stehen, also auf Modulebene. before_all()
ruft dieselbe Funktion noch einmal auf: sie ist idempotent und zeigt, wo die
Vorbereitung eines ganzen Testlaufs normalerweise hingehoert.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"


def use_src_on_path() -> None:
    """Legt src/ auf den Importpfad, damit "from shop.discount import ..." geht."""
    src = str(SRC_DIR)
    if src not in sys.path:
        sys.path.insert(0, src)


# -- Modulebene: laeuft vor dem Import der Step-Module.
use_src_on_path()


def before_all(context):
    """Einmal pro Testlauf."""
    use_src_on_path()


def before_scenario(context, scenario):
    """Einmal pro Szenario: leerer Zustand, bevor die Given-Steps ihn fuellen.

    behave verwirft Werte, die ein Szenario in den Context schreibt, am Ende des
    Szenarios ohnehin wieder. Der Hook macht die erwarteten Namen sichtbar und
    verhindert, dass ein Step versehentlich auf Daten des Vorgaengers zugreift.
    """
    context.customer_type = None
    context.subtotal = None
    context.discount = None
    context.total = None
    context.coupon = None
