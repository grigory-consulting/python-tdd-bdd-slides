# SQLite, Coverage und geteilte Testdaten

Startprojekt für die Übung: Shop-Code, 77 bestehende Tests und eine separate Demo zu gemeinsam genutzten Fixture-Daten. SQLite gehört zur Python-Standardbibliothek; ein Datenbankserver ist nicht erforderlich.

## 1. Projekt herunterladen

Das Repository klonen oder auf GitHub über **Code → Download ZIP** herunterladen und entpacken. Im Terminal in diesen Ordner wechseln:

```bash
cd python-tdd-bdd-slides/starter/sqlite-coverage
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

**Erwartet: `77 passed`.** In der IDE den Python-Interpreter aus diesem `.venv`-Ordner auswählen.

## 3. Coverage untersuchen

```bash
.venv/bin/python -m pytest -q --cov=shop --cov-branch --cov-report=term-missing --cov-report=html
```

Unter Windows in den folgenden Befehlen `.venv/bin/python` durch `.\.venv\Scripts\python.exe` ersetzen.

**Erwartet: `repository.py` bei 95 %, insgesamt 99 %.** Den Bericht `htmlcov/index.html` im Browser öffnen. In `src/shop/repository.py` und `tests/test_repository.py` nachsehen, welches Verhalten noch nicht geprüft wird. Die fehlenden Fälle in der Übung selbst ergänzen.

## 4. Geteilte Testdaten untersuchen

Beide Demo-Tests zusammen ausführen:

```bash
.venv/bin/python -m pytest -q -c pyproject.toml demos/test_shared_scope.py
```

**Erwartet: `2 passed`.** Anschließend nur den zweiten starten:

```bash
.venv/bin/python -m pytest -q -c pyproject.toml demos/test_shared_scope.py::test_module_scope_sieht_den_vorigen_test
```

**Erwartet: `1 failed`.** Der zweite Test benötigt Daten, die der erste angelegt hat. Die Demo zeigt absichtlich diese Abhängigkeit und gehört nicht zum normalen Testlauf.

Zum Vergleich einen unabhängigen Test einzeln starten:

```bash
.venv/bin/python -m pytest -q tests/test_repository.py::test_zwei_bestellungen_unabhaengig_von_anderen_tests
```

**Erwartet: `1 passed`.** Dieser Test richtet seine Daten selbst ein.
