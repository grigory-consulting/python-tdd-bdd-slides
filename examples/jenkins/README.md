# Jenkins-Beispiel: Versandkosten testen

Ein kleines, eigenständiges Beispiel mit Python, pytest und behave. Jenkins lädt den Code direkt von GitHub. GitLab wird nicht benötigt.

Die Regel: Unter 50 Euro fallen 4,99 Euro Versandkosten an, ab einschließlich 50 Euro ist der Versand kostenlos. Beträge werden als ganzzahlige Centwerte verarbeitet.

## Voraussetzungen

Ein laufender Jenkins mit den Plugins **Pipeline**, **Git**, **Docker Pipeline** und **JUnit**. Der ausführende Jenkins-Knoten braucht Zugriff auf eine Docker-Engine mit Linux-Containern. Python läuft im Container `python:3.12-slim`.

Der vorbereitete Seminar-Jenkins erfüllt diese Voraussetzungen. Der Jenkins-Job dieses Beispiels verwendet ausschließlich das öffentliche GitHub-Repository.

## Job einrichten

1. In Jenkins **New Item / Neues Element** öffnen.
2. Name: `versandkosten`. Typ: **Pipeline**. Mit **OK** bestätigen.
3. Im Abschnitt **Pipeline** als Definition **Pipeline script from SCM** auswählen.
4. Bei **SCM** die Option **Git** wählen und folgende Werte eintragen:

   | Feld | Wert |
   | --- | --- |
   | Repository URL | `https://github.com/grigory-consulting/python-tdd-bdd-slides.git` |
   | Credentials | keine; das Repository ist öffentlich |
   | Branch Specifier | `*/main` |
   | Script Path | `examples/jenkins/Jenkinsfile` |

5. **Save / Speichern**, anschließend **Build Now / Jetzt bauen** anklicken.

Jenkins checkt das Repository automatisch aus. Die Befehle wechseln mit `dir('examples/jenkins')` in diesen Beispielordner.

## Was die Pipeline macht

| Stage | Aufgabe | Erwartet |
| --- | --- | --- |
| Installation | Alte Berichte entfernen, eine virtuelle Umgebung anlegen, pytest und behave installieren | Installation erfolgreich |
| Unit-Tests | `test_shipping.py` ausführen und JUnit-XML erzeugen | 2 Tests bestanden |
| BDD-Tests | die drei Beispiele aus `features/shipping.feature` ausführen | 3 Szenarien bestanden |

Der komplette Build endet mit **SUCCESS**. Öffne den Build und anschließend **Console Output / Konsolenausgabe**, **Test Result / Testergebnis** oder die archivierten XML-Dateien.

Die Python-Berechnung steht in [`shipping.py`](shipping.py), die gemeinsamen BDD-Steps in [`features/steps/shipping_steps.py`](features/steps/shipping_steps.py), die Pipeline im [`Jenkinsfile`](Jenkinsfile).

## `post` und `always`

Nach jeder Test-Stage liest `post { always { junit ... } }` den erzeugten Bericht ein – auch wenn Tests fehlgeschlagen sind. Das abschließende `post` archiviert die XML-Dateien. `allowEmptyArchive: true` erlaubt, dass bei einem frühen Installationsfehler noch keine Berichte vorliegen.

Ein fehlgeschlagener Unit-Test macht den Build rot; die anschließende BDD-Stage wird übersprungen. Der Unit-Testbericht wird trotzdem eingelesen. `always` hebt den Testfehler nicht auf.

## Tests lokal ausführen

Im Terminal vom Repository-Hauptordner nach `examples/jenkins` wechseln. Unter Windows (PowerShell):

```powershell
cd examples/jenkins
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q --junitxml=reports/pytest.xml
.\.venv\Scripts\python.exe -m behave --junit --junit-directory reports/behave
```

Unter macOS/Linux die Umgebung mit `python3.12 -m venv .venv` anlegen und anschließend `.venv/bin/python` verwenden.

Jenkins-Dokumentation: [Pipeline aus Git laden](https://www.jenkins.io/doc/book/pipeline/getting-started/#defining-a-pipeline-in-scm), [Docker als Ausführungsumgebung](https://www.jenkins.io/doc/book/pipeline/docker/).
