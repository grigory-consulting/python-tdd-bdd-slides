"""Integrationstests gegen eine echte SQLite-Datei.

Keine Testdoubles: hier wird die Datenbank wirklich beschrieben und wieder
gelesen. Genau das ist der Punkt eines Integrationstests. Die Datei liegt in
``tmp_path``, wird also je Test frisch angelegt und danach aufgeraeumt.
"""

from decimal import Decimal

import pytest

from shop.order import LineItem, Order
from shop.repository import SqliteOrderRepository


def notebook_bestellung() -> Order:
    return Order(
        "vip",
        "DE",
        [LineItem("Notebook", Decimal("100.00"), 1, Decimal("1.5"))],
    )


# ---------------------------------------------------------------------------
# Zum Vergleich: dieselbe Fixture mit module scope
# ---------------------------------------------------------------------------
# ``tmp_path`` hat function scope und laesst sich hier nicht anfordern.
# Fuer breitere Scopes gibt es ``tmp_path_factory``.
# Ein breiter Scope spart Setup-Zeit, teilt aber Zustand zwischen Tests.
# Die beiden folgenden Tests haengen deshalb voneinander ab - das ist hier
# Absicht und dient der Demonstration, nicht als Vorbild.

@pytest.fixture(scope="module")
def gemeinsames_repo(tmp_path_factory) -> SqliteOrderRepository:
    pfad = tmp_path_factory.mktemp("gemeinsam") / "orders.db"
    return SqliteOrderRepository(pfad)


def test_module_scope_schreibt(gemeinsames_repo):
    gemeinsames_repo.save(notebook_bestellung())
    assert len(gemeinsames_repo.list_by_customer_type("vip")) == 1


def test_module_scope_sieht_den_vorigen_test(gemeinsames_repo):
    # Anders als bei function scope ist der Datensatz von oben noch da.
    assert len(gemeinsames_repo.list_by_customer_type("vip")) == 1
    gemeinsames_repo.save(Order("vip", "AT", [LineItem("Kabel", Decimal("9.00"))]))
    assert len(gemeinsames_repo.list_by_customer_type("vip")) == 2
