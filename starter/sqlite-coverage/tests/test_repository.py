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
# Fixture mit function scope: frische Datenbank je Testfunktion
# ---------------------------------------------------------------------------

@pytest.fixture
def repo(tmp_path) -> SqliteOrderRepository:
    """``tmp_path`` ist selbst function-scoped und gibt je Test einen Pfad."""
    return SqliteOrderRepository(tmp_path / "orders.db")


def test_speichern_gibt_eine_id_zurueck(repo):
    order_id = repo.save(notebook_bestellung())
    assert isinstance(order_id, int)
    assert order_id > 0


def test_gespeicherte_bestellung_kommt_unveraendert_zurueck(repo):
    order_id = repo.save(notebook_bestellung())

    geladen = repo.get(order_id)

    assert geladen is not None
    assert geladen.customer_type == "vip"
    assert geladen.country == "DE"
    assert len(geladen.items) == 1


def test_betraege_sind_beim_lesen_wieder_decimal(repo):
    order_id = repo.save(notebook_bestellung())

    item = repo.get(order_id).items[0]

    assert item.unit_price == Decimal("100.00")
    assert isinstance(item.unit_price, Decimal)
    assert item.weight_kg == Decimal("1.5")
    assert isinstance(item.weight_kg, Decimal)


def test_rundungsfreier_betrag_ueberlebt_die_datenbank(repo):
    order = Order("regular", "DE", [LineItem("Kaffee", Decimal("0.10"), 3)])
    order_id = repo.save(order)

    geladen = repo.get(order_id)

    assert geladen.subtotal() == Decimal("0.30")


def test_liste_nach_kundentyp_filtert(repo):
    repo.save(notebook_bestellung())
    repo.save(Order("regular", "AT", [LineItem("Maus", Decimal("20.00"), 2)]))

    vips = repo.list_by_customer_type("vip")

    assert len(vips) == 1
    assert vips[0].country == "DE"


def test_liste_ohne_treffer_ist_leer(repo):
    repo.save(notebook_bestellung())
    assert repo.list_by_customer_type("regular") == []


def test_jede_testfunktion_bekommt_eine_leere_datenbank(repo):
    """Function scope heisst: der Test davor hat hier nichts hinterlassen."""
    assert repo.list_by_customer_type("vip") == []


# Jeder Test richtet seine eigenen Daten ein. Das absichtlich abhaengige
# module-scope-Gegenbeispiel steht nur in Lab 5 unter demos/test_shared_scope.py.

def test_speichern_in_frischer_datenbank(repo):
    repo.save(notebook_bestellung())
    assert len(repo.list_by_customer_type("vip")) == 1


def test_zwei_bestellungen_unabhaengig_von_anderen_tests(repo):
    assert repo.list_by_customer_type("vip") == []
    repo.save(notebook_bestellung())
    repo.save(Order("vip", "AT", [LineItem("Kabel", Decimal("9.00"))]))
    assert len(repo.list_by_customer_type("vip")) == 2
