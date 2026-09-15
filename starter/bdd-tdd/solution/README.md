# Lösung: behave-Anbindung

Diese beiden Dateien richten behave für die bestehenden Rabattregeln ein. Zum Verwenden aus diesem Lösungsordner in den BDD/TDD-Starter kopieren:

| Lösungsdatei | Ziel im Starter |
| --- | --- |
| [`features/environment.py`](features/environment.py) | `features/environment.py` |
| [`features/steps/rabatt_steps.py`](features/steps/rabatt_steps.py) | `features/steps/rabatt_steps.py` |

`environment.py` setzt den Importpfad bereits beim Laden der Datei, damit die Step-Definitionen `shop.discount` importieren können. Vor jedem Szenario werden die verwendeten Kontextwerte zurückgesetzt.

`rabatt_steps.py` ruft die Rabattberechnung auf und prüft Rabatt und Zahlbetrag. Der Given-Step für den Coupon speichert zunächst nur den Code im Kontext. Die Coupon-Berechnung wird anschließend mit BDD und TDD entwickelt.

Die Gherkin-Szenarien unter `features/` im Starter ergänzen und behave aus dem Starter-Ordner ausführen:

```powershell
.\.venv\Scripts\python.exe -m behave
```

Unter macOS/Linux: `.venv/bin/python -m behave`.

## Optional: dieselben Szenarien mit pytest-bdd

Die [vollständige pytest-bdd-Lösung](pytest-bdd/) enthält die fertige Coupon-Regel, beide Feature-Dateien und beide Step-Bindungen. Sie lässt sich direkt aus ihrem eigenen Ordner ausführen: 88 pytest-Tests und fünf behave-Szenarien.
