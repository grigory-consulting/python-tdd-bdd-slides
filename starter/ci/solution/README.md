# Lösung: Tests und Berichte in CI ausführen

Die beiden Dateien enthalten die fertigen Pipelines für den [CI-Starter](../). Alle acht Platzhalter sind ausgefüllt. Shop-Code, Tests, Features und Docker-Einrichtung liegen bereits im übergeordneten Starter.

- [`.gitlab-ci.yml`](.gitlab-ci.yml): pytest und behave als zwei Jobs; JUnit- und Coverage-Berichte als Artefakte.
- [`Jenkinsfile`](Jenkinsfile): gemeinsamer Python-Agent, Installation, pytest und behave; anschließend Berichte und Coverage auswerten.

## Lösung übernehmen

Alle folgenden Befehle im Ordner `starter/ci` ausführen. Zuerst die beiden Pipeline-Vorlagen durch die Lösungsdateien ersetzen.

Windows (PowerShell):

```powershell
Copy-Item .\solution\.gitlab-ci.yml .\.gitlab-ci.yml
Copy-Item .\solution\Jenkinsfile .\Jenkinsfile
```

macOS / Linux:

```bash
cp solution/.gitlab-ci.yml .gitlab-ci.yml
cp solution/Jenkinsfile Jenkinsfile
```

## Auf GitLab und Jenkins ausführen

Die Docker-Umgebung aus [Abschnitt 5 der Starter-Anleitung](../README.md#5-gitlab-und-jenkins-auf-windows-mit-docker-starten) einrichten. Falls die Server bereits laufen und eingerichtet sind, genügt der letzte Befehl:

```powershell
docker compose -f docker/compose.yaml up -d --build
docker compose -f docker/compose.yaml run --rm setup configure
docker compose -f docker/compose.yaml run --rm setup run
```

Hier ist kein `--demo` erforderlich: Beide Pipeline-Dateien sind vollständig. Der letzte Befehl überträgt den Starter auf das lokale GitLab und prüft beide CI-Läufe auf demselben Commit.

**Erwartet:** GitLab `success`, Jenkins `SUCCESS`; 88 pytest-Tests, 10 bestandene behave-Szenarien und ein übersprungenes WIP-Szenario. Zeilen- und Zweigabdeckung: jeweils 100 %.

Die Berichte heißen `reports/pytest.xml`, `reports/coverage.xml` und `reports/behave/*.xml`. Die Pipeline-Testbefehle erzeugen sie; `scripts/check_reports.py` kann diese XML-Dateien zusätzlich lokal prüfen.

Die ausgefüllten Befehle entsprechen der bereits geprüften Docker-Demovariante. Die bisherigen Server-Prüfungen sind im [Prüfprotokoll](../docker/VERIFICATION.md) dokumentiert. Die Fehlerfälle aus [Abschnitt 7](../README.md#7-fehler-und-coverage-vergleichen) können auch mit diesen Lösungsdateien ausgeführt werden.
