"""Hooks und Fixtures für die behave-Läufe des Kursprojekts.

Wichtig zur Ladereihenfolge von behave:
1. environment.py wird importiert,
2. danach werden die Module in features/steps/ importiert,
3. erst danach laufen before_all(), before_tag(), before_scenario().

Die Step-Module holen sich "shop.discount" und "shop.repository" bereits beim
Import. Der Pfad auf src/ muss deshalb schon in Schritt 1 stehen, also auf
Modulebene.
"""

import shutil
import sys
import tempfile
from pathlib import Path

from behave import fixture, use_fixture

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"


def use_src_on_path() -> None:
    """Legt src/ auf den Importpfad, damit "from shop... import ..." geht."""
    src = str(SRC_DIR)
    if src not in sys.path:
        sys.path.insert(0, src)


# -- Modulebene: läuft vor dem Import der Step-Module.
use_src_on_path()


@fixture
def repository(context):
    """Temporäre SQLite-Datei für genau ein Szenario.

    Alles vor dem yield ist Setup, alles danach Cleanup. behave ruft den
    Cleanup-Teil auf, wenn die Context-Schicht abgeräumt wird: bei einem
    Szenario-Tag also nach after_scenario, auch wenn ein Step fehlschlägt.

    Es ist dasselbe SqliteOrderRepository aus Lab 5. Es öffnet und schließt
    seine Verbindung je Aufruf selbst, deshalb genügt im Cleanup das Löschen
    des temporären Verzeichnisses.
    """
    # Import erst hier: src/ liegt zu diesem Zeitpunkt sicher auf sys.path.
    from shop.repository import SqliteOrderRepository

    tmp_dir = Path(tempfile.mkdtemp(prefix="shop-bdd-"))
    context.repository_path = tmp_dir / "orders.sqlite"
    context.repository = SqliteOrderRepository(context.repository_path)

    yield context.repository

    # -- CLEANUP-FIXTURE PART
    shutil.rmtree(tmp_dir, ignore_errors=True)


def before_all(context):
    """Einmal pro Testlauf."""
    use_src_on_path()


def before_tag(context, tag):
    """Wird je Tag aufgerufen, in der Reihenfolge der Tags in der Datei.

    Achtung: before_tag läuft vor before_scenario. Was die Fixture in den
    Context legt, darf before_scenario deshalb nicht wieder überschreiben.
    """
    if tag == "fixture.repository":
        use_fixture(repository, context)


def before_scenario(context, scenario):
    """Einmal pro Szenario: leerer Zustand, bevor die Given-Steps ihn füllen."""
    context.customer_type = None
    context.subtotal = None
    context.discount = None
    context.total = None
    context.coupon = None
    context.order_id = None
    context.stored_order = None
