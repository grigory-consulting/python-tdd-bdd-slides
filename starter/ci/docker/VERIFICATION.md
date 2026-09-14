# Prüfung des Docker-Starters

Stand: 15. September 2026.

Der Starter wurde mit neuen Docker-Volumes auf einer getrennten Linux-Engine aufgebaut: 6 CPUs, 12 GB RAM, Linux arm64 unter Colima auf macOS. Das festgelegte GitLab-amd64-Image lief mit Emulation. Jenkins einschließlich der Plugins wurde aus dem mitgelieferten Dockerfile gebaut. Bereits vorhandene offizielle Basisimages wurden als Download-Cache übernommen; Serverdaten und Zugangsdaten wurden neu erzeugt.

**Windows-Abgrenzung:** Die PowerShell-Befehle sind für Docker Desktop mit Linux-Containern ausgelegt. Ein Durchlauf auf der konkreten Windows-Schulungsinstanz wurde hier nicht ausgeführt. Dafür vor dem Seminar `setup run --demo` verwenden; insbesondere verschachtelte Virtualisierung, RAM und Downloads auf dieser Instanz prüfen.

## Tatsächliche Serverläufe

| Fall | GitLab-Pipeline | Jenkins-Build | Ergebnis |
|---|---|---|---|
| Unveränderter Starter mit `--demo` | 1 | `rabattshop-demo` #1 | `success` / `SUCCESS` |
| Ausgefüllte Übungsdateien ohne `--demo` | 2 | `rabattshop-green` #1 | `success` / `SUCCESS` |
| Zusätzlicher roter Unit-Test | 4 | `rabattshop-unit-red` #2 | `failed` / `FAILURE`; GitLab-behave grün, Jenkins-BDD übersprungen |
| Zusätzliches rotes BDD-Szenario | 5 | `rabattshop-bdd-red` #1 | `failed` / `FAILURE`; pytest auf beiden Servern grün |
| Niedrige Coverage | 6 | `rabattshop-coverage-low` #1 | `success` / `UNSTABLE`; alle Tests grün |

Die IDs gehören zur lokalen Testinstanz; auf einer neuen Schulungsinstanz entstehen eigene IDs und Build-Links.

- Beide Server verwendeten je Vergleich denselben Commit. Der Prüfassistent kontrollierte auch die tatsächlich von Jenkins ausgecheckte Revision.
- Grün: 88 pytest-Tests, 10 bestandene BDD-Szenarien und 1 übersprungenes WIP-Szenario; Zeilen- und Zweigabdeckung jeweils 100 %.
- Die Testansichten beider Server enthielten insgesamt 98 bestandene und 1 übersprungenen Fall.
- Unit-Test rot: pytest-XML mit 89 Fällen und genau einem Fehler. GitLab erzeugte weiterhin beide regulären behave-Berichte. Jenkins meldete die übersprungene Stage ausdrücklich im Log und erzeugte keinen BDD-Bericht.
- BDD rot: zusätzlicher Bericht `TESTS-ci_probe.xml` mit genau einem fehlgeschlagenen Szenario; die regulären Tests blieben grün.
- Coverage niedrig: Zeilenabdeckung 29,84 %, Zweigabdeckung 7,834 %. Die XML-Werte stimmten zwischen den Servern überein.
- GitLab-CI-Linter und Jenkins Declarative Linter akzeptierten die jeweils hochgeladenen Pipeline-Dateien.
- Die lokalen Übungsdateien waren für den Assistenten ausschließlich lesbar eingebunden.
- GitLab- und Jenkins-Container wurden anschließend mit `up -d --force-recreate gitlab jenkins` neu erstellt. `setup configure` lief erneut erfolgreich: Projekt 1 mit `main`, genau derselbe eine Runner und alle fünf Jenkins-Jobs samt Builds blieben erhalten. Es entstanden keine doppelten Projekte oder Runner; die gespeicherten Zugangsdaten funktionierten weiter.

Die erste Auswertung des roten Unit-Tests wurde korrigiert: Jenkins' Stage-API liefert auch für die übersprungene BDD-Stage den geerbten Status `FAILED`. Der Assistent prüft deshalb die ausdrückliche Skip-Meldung und die Abwesenheit eines BDD-Artefakts. Pipeline 4 / Jenkins-Build #2 bestätigten diese korrigierte Prüfung.

## Offline-Prüfungen des Assistenten

```text
python -m unittest discover -s docker/tools -p "test_*.py" -v
```

Acht Prüfungen: Abbruch bei offenen TODOs; Demo ohne lokale Änderungen; Ausschluss privater und erzeugter Dateien; Schutz gegen Uploads über symbolische Links; unabhängige Vergleichsfälle; JUnit-/Cobertura-Auswertung; Windows-BOM und Zeilenenden; eigene `main`-Branch nach einem ersten Demo-Lauf.

Die Compose-Konfiguration wurde ebenfalls validiert. Das lokale Arbeitsheft wurde neu gerendert; die Befehle der CI-Schritte wurden mit Markdown verglichen und die Darstellung im Browser geprüft.
