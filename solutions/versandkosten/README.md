# Lösung: Versandkosten nach Warenwert

Unter 50,00 € kostet der Versand 4,99 €. Ab einschließlich 50,00 € ist er kostenlos. Das Beispiel arbeitet mit nichtnegativen, ganzzahligen Centbeträgen.

Die [Feature-Datei](features/shipping.feature) prüft die drei Grenzfälle 4.999, 5.000 und 5.001 Cent. Die [Steps](features/steps/shipping_steps.py) werden einmal definiert und für jede Tabellenzeile verwendet. Die Berechnung steht in [`shipping.py`](shipping.py), die Then-Funktion vergleicht nur das Ergebnis.

## Ausführen

Vom Repository-Hauptordner in den Lösungsordner wechseln:

```text
cd solutions/versandkosten
```

Windows (PowerShell), mit Python 3.12:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m behave -f progress
```

macOS / Linux:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/python -m behave -f progress
```

**Erwartet: 2 Unit-Tests und 3 BDD-Szenarien bestanden.** Alle Befehle im Lösungsordner ausführen.
