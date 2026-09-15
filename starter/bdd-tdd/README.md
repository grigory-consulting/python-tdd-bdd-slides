# Eine neue Regel mit BDD und TDD entwickeln

Startprojekt für die Coupon-Übung: Shop-Code und 79 bestehende pytest-Tests. Die Rabattregeln sind bereits umgesetzt. Die Coupon-Regel, Gherkin-Szenarien und Step-Definitionen entstehen während der Übung.

Die [Lösungsdateien für die behave-Anbindung](solution/) enthalten `environment.py` und `rabatt_steps.py` zum Nachschlagen oder Übernehmen.

## 1. Projekt öffnen

Das Repository klonen oder auf GitHub über **Code → Download ZIP** herunterladen und entpacken. Im Terminal in diesen Ordner wechseln:

```bash
cd python-tdd-bdd-slides/starter/bdd-tdd
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

**Erwartet: `79 passed`.** In der IDE den Python-Interpreter aus diesem `.venv`-Ordner auswählen.

## 3. behave starten

```bash
.venv/bin/python -m behave
```

Unter Windows `.venv/bin/python` durch `.\.venv\Scripts\python.exe` ersetzen.

**Im Startstand erwartet:** behave meldet fehlende Feature-Dateien. Der Ordner `features/steps/` ist vorbereitet, enthält aber noch keine Step-Definitionen. Die ausführbaren Szenarien werden erst in der Übung angelegt.

## 4. In der Übung weiterarbeiten

1. Die Coupon-Regel gemeinsam klären und die bestätigten Beispiele in `DISCOVERY.md` festhalten.
2. Mit den bekannten Rabattfällen den Runner einrichten: `features/rabatt.feature`, `features/steps/rabatt_steps.py` und `features/environment.py` erstellen; `behave.ini` ergänzen. Hooks und Steps können aus [`solution/`](solution/) übernommen werden.
3. Das erste neue Beispiel in `features/coupon.feature` aufnehmen. Das Szenario soll am falschen Zahlbetrag scheitern. Fehlende Steps und Importfehler zuerst beheben.
4. Einen passenden Unit-Test in `tests/test_coupon.py` schreiben und rot sehen. Die Regel implementieren, bis Unit-Test und Szenario grün sind.
5. Weitere bestätigte Fälle ergänzen und anschließend refaktorieren. Die beobachteten roten und grünen Zustände in `BDD_LOG.md` festhalten.

Beide Ebenen während der Entwicklung regelmäßig ausführen:

```bash
.venv/bin/python -m pytest -q
.venv/bin/python -m behave
```
