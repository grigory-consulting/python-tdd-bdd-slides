"""Persistenz fuer Bestellungen auf SQLite (Standardbibliothek, kein Server).

Betraege werden als TEXT gespeichert und als ``Decimal`` gelesen. SQLite
kennt keinen Dezimaltyp; ein REAL-Feld wuerde aus 0.1 stillschweigend
0.1000000000000000055... machen. Der Umweg ueber die Zeichenkette haelt den
Betrag exakt.
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from decimal import Decimal
from pathlib import Path
from typing import Iterator, List, Optional

from shop.order import LineItem, Order

SCHEMA = """
CREATE TABLE IF NOT EXISTS orders (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_type TEXT NOT NULL,
    country       TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS line_items (
    order_id   INTEGER NOT NULL,
    name       TEXT    NOT NULL,
    unit_price TEXT    NOT NULL,
    quantity   INTEGER NOT NULL,
    weight_kg  TEXT    NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders (id)
);
"""


class SqliteOrderRepository:
    """Legt die Tabellen beim Erzeugen an, falls sie noch fehlen."""

    def __init__(self, path: Path):
        self.path = Path(path)
        with self._connection() as conn:
            conn.executescript(SCHEMA)

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.path)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def save(self, order: Order) -> int:
        """Speichert die Bestellung und gibt die vergebene ID zurueck."""
        with self._connection() as conn:
            cursor = conn.execute(
                "INSERT INTO orders (customer_type, country) VALUES (?, ?)",
                (order.customer_type, order.country),
            )
            order_id = cursor.lastrowid
            conn.executemany(
                "INSERT INTO line_items"
                " (order_id, name, unit_price, quantity, weight_kg)"
                " VALUES (?, ?, ?, ?, ?)",
                [
                    (
                        order_id,
                        item.name,
                        str(item.unit_price),
                        item.quantity,
                        str(item.weight_kg),
                    )
                    for item in order.items
                ],
            )
        return order_id

    def get(self, order_id: int) -> Optional[Order]:
        """Bestellung zur ID, oder ``None``, wenn es sie nicht gibt."""
        with self._connection() as conn:
            row = conn.execute(
                "SELECT customer_type, country FROM orders WHERE id = ?",
                (order_id,),
            ).fetchone()
            if row is None:
                return None
            return Order(row[0], row[1], self._items_for(conn, order_id))

    def list_by_customer_type(self, customer_type: str) -> List[Order]:
        """Alle Bestellungen eines Kundentyps, nach ID sortiert."""
        with self._connection() as conn:
            rows = conn.execute(
                "SELECT id, customer_type, country FROM orders"
                " WHERE customer_type = ? ORDER BY id",
                (customer_type,),
            ).fetchall()
            return [
                Order(row[1], row[2], self._items_for(conn, row[0])) for row in rows
            ]

    @staticmethod
    def _items_for(conn: sqlite3.Connection, order_id: int) -> List[LineItem]:
        rows = conn.execute(
            "SELECT name, unit_price, quantity, weight_kg FROM line_items"
            " WHERE order_id = ? ORDER BY rowid",
            (order_id,),
        ).fetchall()
        return [
            LineItem(name, Decimal(unit_price), int(quantity), Decimal(weight_kg))
            for name, unit_price, quantity, weight_kg in rows
        ]
