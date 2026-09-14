# Tests und Berichte in CI ausführen

Startprojekt für die CI-Übung: Shop-Code, 88 pytest-Tests, 10 ausführbare behave-Szenarien und ein mit `@wip` markiertes Szenario. Die Vorlagen für GitLab und Jenkins enthalten jeweils vier Platzhalter, die während der Übung ergänzt werden.

## 1. Projekt öffnen

Das Repository klonen oder auf GitHub über **Code → Download ZIP** herunterladen und entpacken. Im Terminal in diesen Ordner wechseln:

```bash
cd python-tdd-bdd-slides/starter/ci
```

Beim ZIP-Download heißt der oberste Ordner üblicherweise `python-tdd-bdd-slides-main`.

## 2. Umgebung einrichten

Voraussetzung: Python 3.12.

macOS / Linux:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/python -m behave --tags="not @wip" -f progress
```

Windows (PowerShell):

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m behave --tags="not @wip" -f progress
```

**Erwartet:** 88 Tests bestanden; 10 Szenarien bestanden, 1 übersprungen. In der IDE den Python-Interpreter aus diesem `.venv`-Ordner auswählen.

## 3. Berichte lokal erzeugen und prüfen

Unter Windows in den folgenden Befehlen `.venv/bin/python` durch `.\.venv\Scripts\python.exe` ersetzen.

Zunächst das Prüfskript ausführen:

```bash
.venv/bin/python scripts/check_reports.py
```

**Im frischen Startprojekt erwartet:** fehlende Berichte, Exitcode 1. Die vorherigen Testläufe haben noch keine XML-Dateien erzeugt.

Jetzt die Berichte schreiben und erneut prüfen:

```bash
.venv/bin/python -m pytest --junitxml=reports/pytest.xml --cov=shop --cov-branch --cov-report=term-missing --cov-report=xml:reports/coverage.xml
.venv/bin/python -m behave --tags="not @wip" --junit --junit-directory reports/behave
.venv/bin/python scripts/check_reports.py
```

**Erwartet:** pytest-JUnit, zwei behave-JUnit-Dateien und Coverage-XML sind vorhanden. Keine Fehler; Zeilen- und Zweigabdeckung jeweils 100 %. Das Prüfskript endet mit Exitcode 0.

Die erzeugten Dateien liegen in `reports/` und sind über `.gitignore` vom Commit ausgeschlossen.

## 4. Pipelines vervollständigen

Öffne `.gitlab-ci.yml` und `Jenkinsfile`. Ersetze in jeder Datei diese vier Platzhalter:

| Platzhalter | Aufgabe |
|---|---|
| `TODO_PYTEST_COMMAND` | pytest ausführen und JUnit sowie Coverage-XML erzeugen |
| `TODO_PYTEST_XML` | Pfad zum pytest-JUnit-Bericht angeben |
| `TODO_BEHAVE_COMMAND` | behave ohne WIP-Szenario ausführen und JUnit erzeugen |
| `TODO_BEHAVE_XML` | Alle JUnit-Dateien der Features erfassen |

Die vorbereiteten CI-Images enthalten Python. Übertrage die lokalen Aufrufe deshalb mit `python -m`; der lokale `.venv`-Pfad gehört nicht in die Pipeline.

Für einen CI-Lauf den vollständigen Inhalt dieses Starter-Ordners, einschließlich `.gitlab-ci.yml`, als Wurzel eines Übungsrepositories verwenden. Die Pfade in beiden Vorlagen beziehen sich auf diese Wurzel. Die GitLab-Pipeline braucht einen passenden Runner, die Jenkins-Pipeline einen Docker-fähigen Agenten sowie die Plugins Docker Pipeline, JUnit und Coverage.

Die Vorlagen werden nach dem Ergänzen auf den vorbereiteten CI-Servern ausgeführt. Die lokale Prüfung bestätigt Testkommandos und Berichte; Stage-Steuerung und Berichtsansichten werden im jeweiligen Serverlauf geprüft.
