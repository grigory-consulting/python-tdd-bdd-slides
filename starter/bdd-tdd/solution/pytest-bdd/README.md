# Dieselben Szenarien mit pytest-bdd · optional

Vollständige, ausführbare Lösung: dieselben fünf Gherkin-Szenarien laufen mit behave und mit pytest-bdd. Der Shop enthält hier bereits die fertige Coupon-Regel `SAVE20`.

## Ausführen

Im Terminal in diesen Ordner wechseln. Vom Repository-Hauptordner aus:

```powershell
cd starter/bdd-tdd/solution/pytest-bdd
```

Windows (PowerShell), mit Python 3.12:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest tests/test_rabatt_bdd.py -q
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m behave
```

macOS / Linux:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest tests/test_rabatt_bdd.py -q
.venv/bin/python -m pytest -q
.venv/bin/python -m behave
```

Erwartet: **5 BDD-Tests**, **88 pytest-Tests insgesamt** und **5 bestandene behave-Szenarien**.

Mit den festgelegten Versionen meldet pytest-bdd 36 Deprecation-Warnungen zur pytest-Fixture-API. Die Tests bestehen; die Warnungen bleiben sichtbar.

## Die Bindungen vergleichen

- [`features/rabatt.feature`](features/rabatt.feature) und [`features/coupon.feature`](features/coupon.feature): gemeinsame Szenarien für beide Werkzeuge.
- [`tests/test_rabatt_bdd.py`](tests/test_rabatt_bdd.py): `scenarios()` bindet die Szenarien an pytest. Given-Steps stellen Werte über `target_fixture` bereit; der When-Step ruft die Anwendung auf, die Then-Steps prüfen das Ergebnis.
- [`features/steps/rabatt_steps.py`](features/steps/rabatt_steps.py): dieselben Schritte mit behave und `context`.
- [`src/shop/discount.py`](src/shop/discount.py): gemeinsame Rabatt- und Coupon-Berechnung.

Die Fixture `coupon()` liefert standardmäßig `None`. Nennt ein Szenario einen Coupon, ersetzt dessen Given-Step diesen Wert. So funktionieren Szenarien mit und ohne Coupon mit derselben When-Funktion.

Wer schon die fertige Coupon-Übung besitzt, kann nur `tests/test_rabatt_bdd.py` in deren `tests/`-Ordner übernehmen und `pytest-bdd==8.1.0` installieren. Voraussetzung sind beide Feature-Dateien und die fertige Funktion `payable_total(..., coupon=...)`.
