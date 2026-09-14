# Abhängigkeiten im Test ersetzen

Startprojekt für die Übung mit Fake, Mock, `patch` und `monkeypatch`. Die Bestellung berechnet Versandkosten und berücksichtigt das Datum. Der Anwendungscode ist vorbereitet; die Tests und der Fake enthalten die Aufgaben.

## 1. Projekt öffnen

Das Repository klonen oder auf GitHub über **Code → Download ZIP** herunterladen und entpacken. Im Terminal in diesen Ordner wechseln:

```bash
cd python-tdd-bdd-slides/starter/testdoubles
```

Beim ZIP-Download heißt der oberste Ordner üblicherweise `python-tdd-bdd-slides-main`.

## 2. Umgebung einrichten

Voraussetzung: Python 3.12.

macOS / Linux:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
```

Windows (PowerShell):

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
```

**Erwarteter Startzustand: `13 failed, 17 passed`.** Die 17 Rabatt-Tests sind bereits fertig. Die 13 roten Tests gehören zu den noch offenen Aufgaben. In der IDE den Python-Interpreter aus diesem `.venv`-Ordner auswählen.

## 3. Mit dem Fake beginnen

Lies zunächst `src/shop/order.py` und `src/shop/shipping.py`. `Order.total()` bekommt den Versanddienst als Objekt; `total_via_rate_lookup()` verwendet die importierte Funktion `fetch_rate`.

Starte dann nur die Fake-Tests:

```bash
.venv/bin/python -m pytest -q tests/test_order_fake.py
```

Unter Windows `.venv/bin/python` durch `.\.venv\Scripts\python.exe` ersetzen.

**Erwartet: fünf rote Tests.** Vervollständige `FakeShippingService` in `tests/conftest.py` anhand der TODOs. Die vorgegebenen Fake-Tests prüfen anschließend die berechneten Endbeträge und den Fehlerfall für ein unbekanntes Land.

## 4. Die weiteren Aufgaben bearbeiten

| Reihenfolge | Datei | Aufgabe |
|---|---|---|
| a | `tests/conftest.py`, `tests/test_order_fake.py` | Fake mit fester Tariftabelle bauen |
| b | `tests/test_order_mock.py` | Mock mit `spec` konfigurieren und relevante Aufrufe prüfen |
| c | `tests/test_order_patch.py` | `fetch_rate` an der verwendeten Stelle patchen und eine Gegenprobe schreiben |
| d | `tests/test_order_time.py` | Feste Datumswerte sowie die Versandgrenze prüfen |
| e | `tests/test_order_monkeypatch.py` | Umgebungsvariable und Datumsanbieter mit `monkeypatch` ersetzen |

Führe zuerst die jeweilige Testdatei aus und danach wieder die gesamte Suite:

```bash
.venv/bin/python -m pytest -q
```

Die TODOs werden während der Übung ausgefüllt. Versandkosten und Datum sollen im Test kontrolliert sein, damit das Ergebnis reproduzierbar bleibt.
