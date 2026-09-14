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

## 5. GitLab und Jenkins auf Windows mit Docker starten

Die Server laufen auf deiner Windows-Schulungsinstanz. Öffne **PowerShell auf dieser Instanz** im Ordner `starter/ci` mit `pyproject.toml`, `.gitlab-ci.yml` und `Jenkinsfile`. Die folgenden Docker-Befehle funktionieren auch in einem macOS- oder Linux-Terminal.

- **GitLab** speichert den Übungscode und plant die Jobs aus `.gitlab-ci.yml`. Der **Runner** führt diese Jobs in Python-Containern aus.
- **Jenkins** liest das `Jenkinsfile` aus demselben GitLab-Projekt und führt seine Pipeline ebenfalls in einem Python-Container aus.
- **setup** übernimmt die Einrichtung und überträgt deine Dateien. Die Tests laufen anschließend in den beiden CI-Systemen.

**Vorher durch den Techniker prüfen:** Docker Desktop läuft mit **Linux-Containern** und Compose v2. Für diesen gemeinsamen Schulungsstack sind 6 CPUs, 12 GB RAM für Docker und mindestens 50 GB freier Speicher eingeplant; Windows braucht zusätzlich eigene Ressourcen. In einer virtuellen Schulungsinstanz muss verschachtelte Virtualisierung funktionieren. Für Downloads werden Docker Hub, die Jenkins-Plugin-Server und PyPI benötigt. Images und Plugins am besten vor der Schulung laden.

```powershell
docker info --format '{{.OSType}}/{{.Architecture}}'
docker compose version
```

Erwartet: `linux/x86_64` und eine Compose-Version. `windows/...` bedeutet: in Docker Desktop auf **Linux containers** umschalten. Für den Aufbau sind auf Windows weder Python noch Java noch Git erforderlich; Python aus Abschnitt 2 brauchst du für die lokalen Tests.

**Dienste starten:**

```powershell
docker compose -f docker/compose.yaml up -d --build
```

Compose lädt GitLab CE und GitLab Runner, baut Jenkins mit den benötigten Plugins und legt Docker-Volumes für die Serverdaten an. `init` darf anschließend mit `Exited (0)` erscheinen: Es erzeugt einmalig die lokalen Passwörter. Der erste Aufbau kann je nach Downloadgeschwindigkeit deutlich länger als zehn Minuten dauern.

**Projekt, Runner und Zugang einrichten:**

```powershell
docker compose -f docker/compose.yaml run --rm setup configure
```

Der Befehl wartet auf beide Server, legt das lokale Projekt `root/rabattshop` an und verbindet den Docker-Runner. Er endet mit **Einrichtung abgeschlossen**. Ein erneuter Aufruf verwendet dasselbe Projekt und denselben Runner.

**Zugangsdaten anzeigen:**

```powershell
docker compose -f docker/compose.yaml run --rm setup credentials
```

Öffne die Links **im Browser der Windows-Schulungsinstanz**:

| Dienst | Adresse | Benutzer |
|---|---|---|
| GitLab | [127.0.0.1:18781](http://127.0.0.1:18781/) | `root` |
| Jenkins | [127.0.0.1:18780](http://127.0.0.1:18780/) | `seminar` |

Die Passwörter werden zufällig erzeugt und bleiben in einem lokalen Docker-Volume. Kein GitLab.com-Konto, keine manuelle Token-Erstellung und kein Jenkins-Setup-Assistent sind erforderlich. Das Projekt wird erst beim ersten Lauf mit Dateien gefüllt.

## 6. Beide eigenen Pipelines ausführen

Wenn die Platzhalter aus Abschnitt 4 ergänzt sind:

```powershell
docker compose -f docker/compose.yaml run --rm setup run
```

Der Befehl prüft beide Pipeline-Dateien mit den Server-Lintern. Dann übernimmt er den aktuellen Shop-Code, die Tests, Features und Pipeline-Dateien in die Branch `main` des **lokalen** GitLab-Projekts. Er startet die GitLab-Pipeline und den Jenkins-Job `rabattshop-green` auf **demselben Commit**, wartet auf beide Ergebnisse und prüft die XML-Artefakte. Die direkten Build-Links erscheinen im Terminal.

Es werden nur die vorgesehenen Quell- und Konfigurationsdateien übernommen. `.venv`, `.env`, lokale Berichte, Zugangsdaten, die Docker-Einrichtung und die Präsentation werden nicht hochgeladen. Dateien im lokalen Übungsordner werden nicht verändert. Die Branches im lokalen GitLab sind Arbeitskopien; bearbeite den Code im Starter und führe `setup run` nach Änderungen erneut aus.

**Erwartet:** GitLab `success`, Jenkins `SUCCESS`; jeweils 88 pytest-Tests sowie 10 bestandene BDD-Szenarien und 1 übersprungenes Szenario. Zeilen- und Zweigabdeckung: jeweils 100 %. Jede erfolgreiche Prüfung endet mit **CI-Prüfung abgeschlossen**.

1. GitLab: Build-Link öffnen → Jobs **pytest** und **behave** → Konsolenausgaben, **Tests** und Artefakte ansehen.
2. Jenkins: Build-Link öffnen → **Console Output**, **Test Result**, **Python Coverage** und Artefakte ansehen.
3. `reports/pytest.xml`, `reports/coverage.xml` und die beiden Dateien unter `reports/behave/` wiederfinden.

### Funktionstest vor der Übung

Der Techniker kann den unveränderten Starter prüfen, ohne die Übung vorweg auszufüllen:

```powershell
docker compose -f docker/compose.yaml run --rm setup run --demo
```

`--demo` ersetzt die vier bekannten Platzhalter ausschließlich in der hochgeladenen Kopie. Der Lauf verwendet die Branch `demo` und den Jenkins-Job `rabattshop-demo`. Das bestätigt den Aufbau der Umgebung; für die eigenen bearbeiteten Dateien danach **ohne `--demo`** starten.

## 7. Fehler und Coverage vergleichen

Nach dem erfolgreichen eigenen Lauf diese Befehle einzeln ausführen und jeweils das Ergebnis abwarten:

```powershell
docker compose -f docker/compose.yaml run --rm setup run --case unit-red
docker compose -f docker/compose.yaml run --rm setup run --case bdd-red
docker compose -f docker/compose.yaml run --rm setup run --case coverage-low
```

Die zusätzlichen Fehler entstehen nur in eigenen Branches des lokalen GitLab. Deine Dateien und `main` bleiben dabei erhalten. Jeder Befehl zeigt die passenden Build-Links. Beim technischen Vorabtest kann jeweils zusätzlich `--demo` verwendet werden.

| Fall | GitLab | Jenkins | Beobachtung |
|---|---|---|---|
| `unit-red` | `failed` | `FAILURE` | pytest meldet einen zusätzlichen Fehler. GitLab führt behave trotzdem aus; Jenkins überspringt die BDD-Stage. |
| `bdd-red` | `failed` | `FAILURE` | pytest bleibt grün; das zusätzliche BDD-Szenario schlägt fehl und erscheint im Bericht. |
| `coverage-low` | `success` | `UNSTABLE` | Tests bestehen. Zusätzlicher ungetesteter Code senkt die Coverage unter die Jenkins-Grenzwerte. GitLab zeigt den Wert, hat hier aber kein Coverage-Gate. |

Die Branches heißen wie die Fälle, Jenkins-Jobs `rabattshop-unit-red`, `rabattshop-bdd-red` und `rabattshop-coverage-low`. Bei `--demo` steht zusätzlich `demo-` vor dem Fall. Der Prüfbefehl endet bei einem **erwarteten** roten Vergleichsfall mit Exitcode 0; die eigentliche Pipeline bleibt rot.

## 8. Stoppen und später weiterarbeiten

```powershell
docker compose -f docker/compose.yaml stop
```

Projekte, Builds und Passwörter bleiben erhalten. Später dieselben Befehle wie beim Aufbau verwenden:

```powershell
docker compose -f docker/compose.yaml up -d
docker compose -f docker/compose.yaml run --rm setup configure
```

`configure` erneuert auch den lokalen API-Zugang, der nach sieben Tagen abläuft. Während laufender Pipelines weder `stop` noch `configure` ausführen.

<details>
<summary>Nur bei gewünschtem vollständigem Neustart: alle Daten dieser Schulungsumgebung löschen</summary>

Der folgende Befehl löscht auch GitLab-Projekte, Jenkins-Builds und Passwörter dieses Compose-Projekts. Lokale Starter-Dateien bleiben erhalten. Danach Abschnitt 5 erneut ausführen.

```powershell
docker compose -f docker/compose.yaml down --volumes
```

</details>

## Wenn etwas nicht startet

```powershell
docker compose -f docker/compose.yaml ps -a
docker compose -f docker/compose.yaml logs --tail 60 gitlab jenkins runner
```

| Beobachtung | Nächster Schritt |
|---|---|
| Docker-Engine nicht erreichbar | Docker Desktop auf der Schulungsinstanz starten; `docker info` erneut prüfen. |
| Nur Windows-Container verfügbar | Linux-Engine/WSL2 durch den Techniker einrichten lassen. Auf Windows Server eine Linux-VM mit Docker Engine verwenden; Docker Desktop unterstützt Windows Server nicht. |
| WSL2/Hyper-V startet in der Schulungs-VM nicht | Verschachtelte Virtualisierung im Hypervisor prüfen lassen. Eine installierte Docker-Oberfläche allein genügt nicht. |
| Port 18780 oder 18781 belegt | Den anderen Dienst identifizieren und dessen Port ändern oder beenden lassen; danach `up -d` wiederholen. |
| GitLab zeigt anfangs 502 | `setup configure` weiter warten lassen. Bei Zeitlimit RAM, freien Speicher und Container-Logs prüfen. |
| `config.toml` fehlt beim Runner | Vor `configure` normal. Der Einrichtungsbefehl erzeugt die Datei und startet den Runner neu. |
| GitLab-Job bleibt `pending` | `setup configure` nach Ende anderer Läufe wiederholen; GitLab → Settings → CI/CD → Runners auf `online` prüfen. |
| HTTP 401 beim erneuten Lauf | `setup configure` erneuert den lokalen GitLab-API-Zugang. |
| TLS-/Downloadfehler hinter Firmenproxy | Proxy und vertrauenswürdige Firmenzertifikate für Docker, Jenkins-Downloads und Python durch den Techniker konfigurieren lassen. |
| `TODO_`-Fehler | Beide Pipeline-Dateien aus Abschnitt 4 ergänzen oder bewusst den separaten Demo-Aufruf verwenden. |
| Berichte oder Status unerwartet | Die im Terminal ausgegebenen **neuen** Build-Links öffnen und den ersten Fehler im Job-Log lesen. |

Diese Umgebung ist für lokale Übungen mit vertrauenswürdigem Kurscode gedacht. Die Ports sind an `127.0.0.1` gebunden; Runner und Jenkins können über den Docker-Socket Container starten. Nicht als öffentlich erreichbaren Produktivserver verwenden.

GitLab unterstützt Docker auf Windows offiziell nicht. Hier laufen die Dienste in der Linux-Engine mit benannten Docker-Volumes, um Windows-Dateirechte für Serverdaten zu vermeiden. Der konkrete Windows-Schulungsrechner braucht deshalb vor dem Kurs den beschriebenen Demo-Probelauf. Siehe [GitLab Docker](https://docs.gitlab.com/install/docker/installation/), [GitLab-Ressourcen](https://docs.gitlab.com/install/requirements/), [Docker Desktop unter Windows](https://docs.docker.com/desktop/setup/install/windows-install/) und [Jenkins mit Docker](https://www.jenkins.io/doc/book/pipeline/docker/).

[Prüfprotokoll des Starters](docker/VERIFICATION.md): tatsächliche GitLab-/Jenkins-Läufe, Berichte und Grenzen der Windows-Prüfung.
