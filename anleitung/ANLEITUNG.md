# TDD und BDD · Schritt für Schritt

Dr.-Ing. Grigory Devadze

Diese Anleitung führt dich vom ersten Import-Test bis zur CI-Pipeline. Du legst die Dateien selbst an, führst die Tests nach jeder Änderung aus und vergleichst das Ergebnis mit dem angegebenen Zwischenstand. Die Befehle im Haupttext sind für macOS; die wichtigsten Windows-Befehle stehen am Ende.

## Bevor du anfängst

Diese Anleitung beschreibt das vollständige Seminarpaket. Vier vorbereitete [Starter stehen auch im Repository](https://github.com/grigory-consulting/python-tdd-bdd-slides/tree/main/starter) bereit; die übrigen Vorlagen und die CI-Umgebung stellt der Trainer bereit. Das Beispiel [Agentische Entwicklung mit BDD und TDD](#agentische-entwicklung-mit-bdd-und-tdd) am Ende funktioniert eigenständig ohne Seminarvorlagen.

Die Beispiele verwenden eigene Übungsordner unter `uebungen/`. Kopiere die benötigten Startstände aus `labs/`, wie beim jeweiligen Lab beschrieben. Wenn du Lab 1 bereits in `src_live` gemacht hast, kannst du Lab 2 dort anschließen; überspringe dann das erneute Einrichten und behalte deine beiden Smoke-Tests.

**Immer dieselbe kleine Folge:** Datei ändern → Test ausführen → Ergebnis lesen → erst dann weiter. Bei einem roten Schritt ist ein Fehlschlag gewollt. Prüfe auch den Grund: Ein Importfehler ist etwas anderes als ein falscher Rabattbetrag. Die aufklappbaren Abschnitte enthalten den jeweils nächsten Lösungsstand; öffne sie nach dem eigenen Versuch.

Setze einmal im Terminal den Pfad zu deinem Seminarordner. Beispiel für macOS:

```bash
export SEMINAR="$HOME/Seminare/python-tdd-bdd"
```

Auf anderen Rechnern ersetzt du nur diesen Pfad. In einem neuen Terminal ist die Variable erneut zu setzen. Beginne jeden Lab-Aufruf im Ordner, in dem dessen `pyproject.toml` liegt. Mit `pwd` siehst du deinen aktuellen Ordner.

### Was die Testzahlen bedeuten

Lab 1 und 2 verwenden denselben selbst aufgebauten Ordner. Deshalb enthält der Endstand von Lab 2 **19 Tests: 17 fachliche Tests plus deine zwei Smoke-Tests**. Ab Lab 3 verwenden wir je Lab eine Kopie des bereitgestellten Startstands. Darin sind die beiden reinen Setup-Tests nicht mehr enthalten; die dort angegebenen Zahlen passen zu diesen Vorlagen. Das ist ein Wechsel des Arbeitsordners, kein Verlust deiner eigenen Arbeit.

| Lab | Thema | Ende dieses Durchlaufs |
|---|---|---|
| 1 | Umgebung, zwei Tests, Test Explorer, Debugger | 2 Tests |
| 2 | Rabattregeln mit TDD, unittest, Refactoring | 19 Tests inklusive Smoke-Tests |
| 3 | Fake, Mock, patch, Datum, monkeypatch | 41 Tests |
| 4 | Bestehendes Verhalten, Approval-Test, Seam, Bugfix | 68 Tests mit allen Vertiefungen |
| 5 | SQLite, Coverage und Fixture-Scope | 79 Tests |
| 6 | Discovery und vollständiger BDD-/TDD-Zyklus | 83 Tests und 5 Szenarien |
| 6b | Dieselben Features mit pytest-bdd, optional | 88 Tests, davon 5 BDD-Tests |
| 7 | Outline, Tags, Fixtures, Steuerfunktion, Berichte | 88 Tests, 10 Szenarien grün, 1 übersprungen |
| 8 | GitLab und Jenkins | Beide Suiten und ihre Berichte |

**Zum Zeitplan:** Die Anleitung enthält auch ausgearbeitete Vertiefungen. Im zweitägigen Seminar sind Lab 6b und der Approval-Test optional; die Zeit-/monkeypatch-Beispiele sowie die behave-Fixture können gemeinsam demonstriert werden. Für einen vollständigen eigenen Durchlauf bearbeitest du alle Schritte. Die ausführliche Anleitung ist kein zusätzlicher Zeitblock in der Agenda.

Laufzeiten, Warnungszahlen und Fortschrittspunkte unterscheiden sich je nach Werkzeugversion. Entscheidend sind die Testfälle, Status und genannten Beträge. Die Befehle verwenden `python -m pip`, damit pip zum ausgewählten Python gehört.

## Lab 1 · Umgebung und erste Tests

Am Ende kannst du zwei Tests im Terminal und in VS Code starten und einen Test im Debugger anhalten. Hier schreiben wir noch keine Rabattfunktion.

<a id="lab-1-schritt-1"></a>

### Schritt 1 · Projektordner und virtuelle Umgebung

Öffne ein Terminal. Lege für Lab 1 und 2 einen gemeinsamen Arbeitsordner an:

```bash
mkdir -p "$SEMINAR/uebungen/lab01-02"
cd "$SEMINAR/uebungen/lab01-02"
python3.12 -m venv .venv
source .venv/bin/activate
python --version
```

**Erwartet:** Python 3.12 und `(.venv)` in der Eingabezeile. Warte beim Anlegen der Umgebung, bis die Eingabezeile zurückkommt. Ein Abbruch mit Ctrl+C kann eine unvollständige Umgebung hinterlassen. Nach einem Abbruch führe `python3.12 -m venv .venv` noch einmal vollständig aus und aktiviere sie danach.

<a id="lab-1-schritt-2"></a>

### Schritt 2 · pytest installieren

Führe die Installation mit dem Python deiner Projektumgebung aus:

```bash
./.venv/bin/python -m pip install pytest pytest-cov
./.venv/bin/python -m pytest --version
```

**Erwartet:** pytest meldet eine Versionsnummer. Falls ein bloßes `pip install` mit `externally-managed-environment` endet, greift dieser Befehl auf die Systeminstallation zu. Der hier gezeigte direkte Aufruf wählt deine `.venv`. Falls darin selbst pip fehlt, ergänze es mit `./.venv/bin/python -m ensurepip --upgrade` und wiederhole die Installation. Für dieses Lab ist kein `--break-system-packages` nötig.

<a id="lab-1-schritt-3"></a>

### Schritt 3 · Ordner und Projektkonfiguration anlegen

```bash
mkdir -p src/shop tests
touch src/shop/__init__.py
```

Die leere `__init__.py` kennzeichnet `shop` als reguläres Python-Paket. Erstelle dann im Projektwurzelordner die Konfiguration:

Erstelle oder ersetze die Datei `pyproject.toml`:

```toml
[project]
name = "shop"
version = "0.1.0"
requires-python = ">=3.10"

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
```

`pythonpath` ergänzt `src/` als Suchordner, wenn pytest startet. Dadurch kann ein Test `shop` importieren, ohne unser eigenes Paket zu installieren. `testpaths` sagt pytest, wo die Tests liegen. Ein `[build-system]`-Abschnitt wird für diesen Ablauf nicht gebraucht.

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** Noch keine Tests gesammelt. pytest meldet `no tests ran` oder bei einer Warnung nur die Warnungszusammenfassung. Exitcode 5 ist an dieser Stelle normal.

Je nach pytest-Version erscheint zusätzlich eine Warnung, solange `tests/` leer ist. Sobald wir den ersten Test anlegen, verschwindet dieser Anlass.

<a id="lab-1-schritt-4"></a>

### Schritt 4 · Ersten Smoke-Test schreiben

Prüfe zunächst nur, ob Python unser Paket findet.

Erstelle oder ersetze die Datei `tests/test_smoke.py`:

```python
import shop


def test_shop_import():
    assert shop.__name__ == "shop"
```

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** `1 passed`.

<a id="lab-1-schritt-5"></a>

### Schritt 5 · Kaufmännische Rundung prüfen

Der zweite Smoke-Test prüft die Rundung, die wir später bei Geldbeträgen verwenden. Ersetze die Datei durch diesen Stand; der erste Test bleibt darin erhalten.

Erstelle oder ersetze die Datei `tests/test_smoke.py`:

```python
from decimal import Decimal, ROUND_HALF_UP

import shop


def test_shop_import():
    assert shop.__name__ == "shop"


def test_rounding():
    discount = Decimal("10.05") * Decimal("0.10")
    rounded = discount.quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    assert rounded == Decimal("1.01")
```

10 % von 10,05 € sind 1,0050 €. Auf Cent kaufmännisch gerundet sind das 1,01 €. Schreibe die Beträge als Strings in `Decimal(...)`, damit keine binäre Float-Näherung übernommen wird.

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** `2 passed`.

<a id="lab-1-schritt-6"></a>

### Schritt 6 · Dieselben Tests in VS Code ausführen

1. Öffne den Ordner `uebungen/lab01-02` in der **Mac-Version von VS Code** über „Datei → Ordner öffnen“.
2. Drücke **⌘⇧P** → **Python: Select Interpreter** → wähle `.venv/bin/python` aus diesem Projekt.
3. Falls die Python-Befehle fehlen: installiere die Erweiterung **Python** von Microsoft (`ms-python.python`).
4. **⌘⇧P** → **Python: Configure Tests** → **pytest** → Ordner **tests**.
5. **⌘⇧P** → **Testing: Focus on Test Explorer View**. Damit öffnest du die Testansicht auch dann, wenn das Bechersymbol nicht sichtbar ist.
6. Klicke auf **Run All Tests**.

**Erwartet:** `test_shop_import` und `test_rounding` erscheinen und werden grün. Unter Windows ist die Befehlspalette **Strg+Umschalt+P**. Eine über Parallels gestartete Windows-App verwendet die Windows-Tasten und benötigt eine eigene Windows-Projektumgebung.

Wenn der Assistent nicht erscheint, kannst du stattdessen diese Projektdatei anlegen:

Erstelle oder ersetze die Datei `.vscode/settings.json`:

```json
{
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.testing.pytestArgs": ["tests"]
}
```

Starte danach **Test: Refresh Tests**. Ein Terminal-Lauf mit zwei grünen Tests und ein leerer Test Explorer deuten meist auf einen anderen ausgewählten Interpreter oder einen falsch geöffneten Projektordner hin.

<a id="lab-1-schritt-7"></a>

### Schritt 7 · Debugger ausprobieren

1. Öffne `tests/test_smoke.py`.
2. Klicke links neben die Zeilennummer von `rounded = discount.quantize(`. Ein roter Haltepunkt erscheint.
3. Rechtsklick auf `test_rounding` in der Testansicht → **Debug Test**.
4. Der Debugger hält vor der Rundung. Unter **Variablen** steht `discount = Decimal('1.0050')`.
5. **F10**, auf manchen Mac-Tastaturen **fn + F10**, führt den nächsten Schritt aus. Gegebenenfalls nochmals drücken, bis die Zuweisung abgeschlossen ist. Danach steht `rounded = Decimal('1.01')`.
6. **Fortsetzen ▶** beendet den Test erfolgreich. Entferne den Haltepunkt danach durch erneutes Anklicken.

**Fertig, wenn:** beide Tests im Terminal und Test Explorer grün sind und du den Zwischenwert im Debugger gesehen hast. Jetzt geht es im selben Ordner mit Lab 2 weiter.

## Lab 2 · Rabattregeln testgetrieben entwickeln

Die Funktion berechnet den **Rabattbetrag**, nicht den Zahlbetrag. Die beiden Smoke-Tests aus Lab 1 bleiben bestehen. Verwende weiterhin denselben Projektordner und dieselbe virtuelle Umgebung.

<aside class="lesson-context" id="lab-2-folien">

### Einordnung: Ab „Fall 1: Der erste Test ist rot“

Hier beginnt die Vorführung der Rabattfunktion aus Lab 2. In dieser Anleitung findest du sie ab [Schritt 2](#lab-2-schritt-2). **„Fall“ bezeichnet ein Beispiel aus der Testfallliste; „Schritt“ bezeichnet einen Arbeitsschritt in der Anleitung.** Deshalb gehört Fall 1 zu den Schritten 2 und 3.

**Beim Vorführen und Mitmachen:**

1. Zeige [Folie 24: Fall 1: Der erste Test ist rot](../index.html?scrollActivationWidth=false#/3/20). Führe dann [Schritt 2](#lab-2-schritt-2) im Editor und Terminal aus. Halte beim roten Ergebnis an und lies den Fehler `NotImplementedError` gemeinsam mit der Gruppe.
2. Zeige [Folie 25: Fall 1: Eine feste Rückgabe genügt](../index.html?scrollActivationWidth=false#/3/21). Ändere die Rückgabe wie in [Schritt 3](#lab-2-schritt-3) und starte die Tests erneut. Der erste TDD-Durchlauf ist damit grün.
3. Mit [Folie 26: Rot und Grün, Fall 2](../index.html?scrollActivationWidth=false#/3/22) beginnt die nächste Anforderung. Fahre bei [Schritt 4](#lab-2-schritt-4) fort: neuer Test, rotes Ergebnis, kleine Änderung, grüner Lauf.

Wenn du parallel mitprogrammierst, arbeitest du im selben Übungsordner weiter. Bereits ausgeführte Schritte musst du anschließend nicht wiederholen. Wenn du nur zugeschaut hast, beginne danach selbst ab Schritt 2.

Die Folien fassen manche Zwischenstände zusammen. In der Anleitung bearbeitest du die Fälle einzeln und führst jeden angegebenen Testlauf aus.

<details>
<summary>Welche Folie gehört zu welchem Schritt?</summary>

| Präsentation | Passende Stelle in dieser Anleitung |
|---|---|
| [Folie 22: Testfallliste: Rabatt und Staffel](../index.html?scrollActivationWidth=false#/3/18) und [Folie 23: Testfallliste: Rundung und Fehlerfälle](../index.html?scrollActivationWidth=false#/3/19) | [Schritt 1: Testfallliste](#lab-2-schritt-1) |
| [Folie 24: Fall 1: Der erste Test ist rot](../index.html?scrollActivationWidth=false#/3/20) | [Schritt 2: Stub, Test und roter Lauf](#lab-2-schritt-2) |
| [Folie 25: Fall 1: Eine feste Rückgabe genügt](../index.html?scrollActivationWidth=false#/3/21) | [Schritt 3: erste grüne Rückgabe](#lab-2-schritt-3) |
| [Folie 26: Rot und Grün, Fall 2](../index.html?scrollActivationWidth=false#/3/22) | [Schritt 4: VIP-Rabatt](#lab-2-schritt-4) |
| [Folie 27: Fälle 3 und 4: die Staffelgrenze](../index.html?scrollActivationWidth=false#/3/23) und [Folie 28: Fälle 3 und 4: die Staffelregel](../index.html?scrollActivationWidth=false#/3/24) | [Schritt 5: regular an der Grenze](#lab-2-schritt-5), dann [Schritt 6: vip an der Grenze](#lab-2-schritt-6) |
| [Folie 29: Fälle 5 bis 9: Tests im Überblick](../index.html?scrollActivationWidth=false#/3/25) und [Folie 30: Fälle 5 bis 9: Die Tests bestehen](../index.html?scrollActivationWidth=false#/3/26) | Zweiter Teil von [Schritt 6](#lab-2-schritt-6): vip knapp unter 500; dann [Schritt 7: Rundung](#lab-2-schritt-7), [Schritt 8: negative Eingaben](#lab-2-schritt-8) und [Schritt 9: unbekannter Kundentyp](#lab-2-schritt-9) |
| Fall 10 aus der Testfallliste: Zahlbetrag; dafür gibt es keine eigene Codefolie | [Schritt 10: payable_total](#lab-2-schritt-10) |
| Die zusammengefassten Tests aus „Fälle 5 bis 9: Tests im Überblick“ | [Schritt 11: erst jetzt den Testcode parametrisieren und ergänzen](#lab-2-schritt-11) |
| [Folie 31: `unittest`: ein Beispiel](../index.html?scrollActivationWidth=false#/3/27) | [Schritt 12: drei eigene unittest-Fälle](#lab-2-schritt-12) |
| [Folie 34: Was Refactoring bedeutet](../index.html?scrollActivationWidth=false#/3/30) bis [Folie 40: Nach dem Refactoring](../index.html?scrollActivationWidth=false#/3/36) | [Schritt 13: Refactoring unter grünen Tests](#lab-2-schritt-13) |

</details>

</aside>

<a id="lab-2-schritt-1"></a>

### Schritt 1 · Testfallliste festhalten

Erstelle oder ersetze die Datei `TDD_LOG.md`:

```markdown
# Testfallliste

- [ ] regular, 100.00 → Rabatt 0.00
- [ ] vip, 100.00 → Rabatt 10.00
- [ ] regular, 500.00 → Rabatt 25.00
- [ ] vip, 500.00 → Rabatt 75.00
- [ ] vip, 499.99 → Rabatt 50.00
- [ ] vip, 33.33 → Rabatt 3.33
- [ ] vip, 10.05 → Rabatt 1.01
- [ ] Negativer Warenwert → ValueError
- [ ] Unbekannter Kundentyp → ValueError
- [ ] Zahlbetrag = Warenwert minus Rabatt

## Beobachtete Läufe

Notiere hier nach jeder Runde: neuer Fall, roter Fehler, Änderung und grüner Lauf.
```

Arbeite jeweils den nächsten Fall ab: **Rot → Grün → Refactoring prüfen**. Ein späterer Fall kann bereits grün sein, wenn die bisherige Implementierung ihn schon erfüllt. Erfinde dann keinen künstlichen Fehler in der Anwendung.

<a id="lab-2-schritt-2"></a>

### Schritt 2 · Fall 1: Der erste Test ist rot

Ein regulärer Kunde erhält bei 100,00 € Warenwert 0,00 € Rabatt. Zunächst fehlt die Berechnung.

**Passende Folie:** [Folie 24: Fall 1: Der erste Test ist rot](../index.html?scrollActivationWidth=false#/3/20)

Lege zuerst den Stub an. Er enthält bereits den Funktionsnamen und die Parameter, wirft aber noch `NotImplementedError`. So scheitert der anschließende Test an der fehlenden Berechnung.

Auf der Folie heißt der Test `test_stammkunde_bekommt_keinen_rabatt`, hier `test_regular_customer_gets_no_discount`. Beide prüfen denselben Fall. Verwende eine der beiden Varianten, damit du den Test nicht doppelt anlegst.

Erstelle oder ersetze die Datei `src/shop/discount.py`:

```python
from decimal import Decimal


def calculate_discount(customer_type: str, subtotal: Decimal) -> Decimal:
    raise NotImplementedError
```

Erstelle oder ersetze die Datei `tests/test_discount.py`:

```python
from decimal import Decimal

import pytest

from shop.discount import calculate_discount


def test_regular_customer_gets_no_discount():
    discount = calculate_discount("regular", Decimal("100.00"))
    assert discount == Decimal("0.00")
```

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** `1 failed, 2 passed`. Der Fehler ist `NotImplementedError`.

<a id="lab-2-schritt-3"></a>

### Schritt 3 · Fall 1: Eine feste Rückgabe genügt

Versuche zuerst selbst, die kleinste passende Implementierung zu schreiben.

**Passende Folie:** [Folie 25: Fall 1: Eine feste Rückgabe genügt](../index.html?scrollActivationWidth=false#/3/21)

Öffne den folgenden Lösungsstand erst, nachdem du die Änderung selbst versucht hast. Beim Vorführen kannst du hier gemeinsam vergleichen.

<details>
<summary>Lösungsstand: eine feste Rückgabe</summary>

Ersetze in `src/shop/discount.py` genau diesen Abschnitt:

```python
    raise NotImplementedError
```

durch:

```python
    return Decimal("0.00")
```

</details>

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** `3 passed`: ein fachlicher Test und zwei Smoke-Tests.

Die feste Rückgabe ist ein vorläufiger Schritt. Die nächste Anforderung wird zeigen, wann sie nicht mehr genügt. Prüfe jetzt Namen und Wiederholungen; hier gibt es noch wenig zu refaktorieren.

<a id="lab-2-schritt-4"></a>

### Schritt 4 · Fall 2: VIP-Rabatt zuerst testen

**Passende Folie:** [Folie 26: Rot und Grün, Fall 2](../index.html?scrollActivationWidth=false#/3/22)

Die feste Rückgabe genügt für den VIP-Fall noch nicht. Lass zuerst den neuen Test scheitern, bevor du die nächste Implementierung zeigst.

Ergänze am Ende von `tests/test_discount.py`:

```python
def test_vip_customer_gets_ten_percent():
    assert calculate_discount("vip", Decimal("100.00")) == Decimal("10.00")
```

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** `1 failed, 3 passed`: 0,00 statt 10,00.

<details>
<summary>Grün: Kundentyp berücksichtigen</summary>

Erstelle oder ersetze die Datei `src/shop/discount.py`:

```python
from decimal import Decimal


def calculate_discount(customer_type: str, subtotal: Decimal) -> Decimal:
    rate = Decimal("0.10") if customer_type == "vip" else Decimal("0.00")
    return subtotal * rate
```

</details>

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** `4 passed`.

<a id="lab-2-schritt-5"></a>

### Schritt 5 · Fall 3: Staffelgrenze für reguläre Kunden

Ergänze am Ende von `tests/test_discount.py`:

```python
def test_regular_customer_gets_volume_discount():
    assert calculate_discount("regular", Decimal("500.00")) == Decimal("25.00")
```

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** `1 failed, 4 passed`: 0,00 statt 25,00.

<details>
<summary>Grün: ab 500 € fünf Prozentpunkte ergänzen</summary>

Erstelle oder ersetze die Datei `src/shop/discount.py`:

```python
from decimal import Decimal


def calculate_discount(customer_type: str, subtotal: Decimal) -> Decimal:
    rate = Decimal("0.10") if customer_type == "vip" else Decimal("0.00")
    if subtotal >= Decimal("500.00"):
        rate += Decimal("0.05")
    return subtotal * rate
```

</details>

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** `5 passed`.

<a id="lab-2-schritt-6"></a>

### Schritt 6 · Fälle 4 und 5: VIP an der Grenze und knapp darunter

Ergänze am Ende von `tests/test_discount.py`:

```python
def test_vip_customer_combines_both_discounts():
    assert calculate_discount("vip", Decimal("500.00")) == Decimal("75.00")
```

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** `6 passed`. Dieser zusätzliche Fall ist bereits abgedeckt.

Ergänze am Ende von `tests/test_discount.py`:

```python
def test_vip_customer_below_volume_threshold():
    assert calculate_discount("vip", Decimal("499.99")) == Decimal("50.00")
```

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** `1 failed, 6 passed`: 49,9990 statt 50,00. Die Cent-Rundung fehlt.

<details>
<summary>Grün: zunächst auf Cent quantisieren</summary>

Erstelle oder ersetze die Datei `src/shop/discount.py`:

```python
from decimal import Decimal


def calculate_discount(customer_type: str, subtotal: Decimal) -> Decimal:
    rate = Decimal("0.10") if customer_type == "vip" else Decimal("0.00")
    if subtotal >= Decimal("500.00"):
        rate += Decimal("0.05")
    return (subtotal * rate).quantize(Decimal("0.01"))
```

</details>

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** `7 passed`.

<a id="lab-2-schritt-7"></a>

### Schritt 7 · Fälle 6 und 7: Die Rundungsregel präzisieren

Ergänze am Ende von `tests/test_discount.py`:

```python
def test_discount_rounds_down():
    assert calculate_discount("vip", Decimal("33.33")) == Decimal("3.33")
```

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** `8 passed`.

Ergänze am Ende von `tests/test_discount.py`:

```python
def test_discount_rounds_half_up():
    assert calculate_discount("vip", Decimal("10.05")) == Decimal("1.01")
```

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** `1 failed, 8 passed`: 1,00 statt 1,01. Die Standardrundung passt nicht zur vereinbarten Geldregel.

<details>
<summary>Grün: ROUND_HALF_UP verwenden</summary>

Erstelle oder ersetze die Datei `src/shop/discount.py`:

```python
from decimal import Decimal, ROUND_HALF_UP


def calculate_discount(customer_type: str, subtotal: Decimal) -> Decimal:
    rate = Decimal("0.10") if customer_type == "vip" else Decimal("0.00")
    if subtotal >= Decimal("500.00"):
        rate += Decimal("0.05")
    return (subtotal * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
```

</details>

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** `9 passed`. Der Smoke-Test aus Lab 1 hat die Bibliothek geprüft; dieser Test prüft jetzt unsere Anwendung.

<a id="lab-2-schritt-8"></a>

### Schritt 8 · Fall 8: Negative Eingaben ablehnen

Ergänze am Ende von `tests/test_discount.py`:

```python
def test_negative_subtotal_is_rejected():
    with pytest.raises(ValueError, match="negativ"):
        calculate_discount("vip", Decimal("-1.00"))
```

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** `1 failed, 9 passed`: die erwartete Ausnahme wurde nicht ausgelöst.

<details>
<summary>Grün: Wächterklausel am Funktionsanfang</summary>

Erstelle oder ersetze die Datei `src/shop/discount.py`:

```python
from decimal import Decimal, ROUND_HALF_UP


def calculate_discount(customer_type: str, subtotal: Decimal) -> Decimal:
    if subtotal < 0:
        raise ValueError(f"Warenkorbwert darf nicht negativ sein: {subtotal}")
    rate = Decimal("0.10") if customer_type == "vip" else Decimal("0.00")
    if subtotal >= Decimal("500.00"):
        rate += Decimal("0.05")
    return (subtotal * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
```

</details>

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** `10 passed`.

<a id="lab-2-schritt-9"></a>

### Schritt 9 · Fall 9: Unbekannte Kundentypen ablehnen

Ergänze am Ende von `tests/test_discount.py`:

```python
def test_unknown_customer_type_is_rejected():
    with pytest.raises(ValueError, match="gold"):
        calculate_discount("gold", Decimal("100.00"))
```

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** `1 failed, 10 passed`.

<details>
<summary>Grün: erlaubte Kundentypen festhalten</summary>

Erstelle oder ersetze die Datei `src/shop/discount.py`:

```python
from decimal import Decimal, ROUND_HALF_UP


CUSTOMER_TYPES = ("regular", "vip")


def calculate_discount(customer_type: str, subtotal: Decimal) -> Decimal:
    if subtotal < 0:
        raise ValueError(f"Warenkorbwert darf nicht negativ sein: {subtotal}")
    if customer_type not in CUSTOMER_TYPES:
        raise ValueError(f"unbekannter Kundentyp: {customer_type!r}")
    rate = Decimal("0.10") if customer_type == "vip" else Decimal("0.00")
    if subtotal >= Decimal("500.00"):
        rate += Decimal("0.05")
    return (subtotal * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
```

</details>

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** `11 passed`.

<a id="lab-2-schritt-10"></a>

### Schritt 10 · Fall 10: Den Zahlbetrag als neue Funktion testen

Ersetze in `tests/test_discount.py` genau diesen Abschnitt:

```python
from shop.discount import calculate_discount
```

durch:

```python
from shop.discount import calculate_discount, payable_total
```

Ergänze am Ende von `tests/test_discount.py`:

```python
def test_payable_total():
    assert payable_total("vip", Decimal("100.00")) == Decimal("90.00")
```

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** Ein Importfehler bei der Testsammlung: `payable_total` existiert noch nicht. Das ist rot aus dem erwarteten Grund; pytest endet mit Exitcode 2.

<details>
<summary>Grün: Warenwert minus Rabatt</summary>

Erstelle oder ersetze die Datei `src/shop/discount.py`:

```python
from decimal import Decimal, ROUND_HALF_UP


CUSTOMER_TYPES = ("regular", "vip")


def calculate_discount(customer_type: str, subtotal: Decimal) -> Decimal:
    if subtotal < 0:
        raise ValueError(f"Warenkorbwert darf nicht negativ sein: {subtotal}")
    if customer_type not in CUSTOMER_TYPES:
        raise ValueError(f"unbekannter Kundentyp: {customer_type!r}")
    rate = Decimal("0.10") if customer_type == "vip" else Decimal("0.00")
    if subtotal >= Decimal("500.00"):
        rate += Decimal("0.05")
    return (subtotal * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def payable_total(customer_type: str, subtotal: Decimal) -> Decimal:
    return subtotal - calculate_discount(customer_type, subtotal)
```

</details>

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** `12 passed`.

<a id="lab-2-schritt-11"></a>

### Schritt 11 · Testcode zusammenfassen und zusätzliche Fälle ergänzen

Die sieben Rabattprüfungen wiederholen denselben Ablauf. Fasse sie mit `parametrize` zusammen. Ergänze außerdem vier zusätzliche Prüfungen: die Zahl der Nachkommastellen, den negativen Warenwert auch für `regular` und zwei weitere Zahlbeträge. Parametrisierung allein verändert die Anzahl der geprüften Fälle nicht.

Der folgende komplette Dateistand ersetzt die bisherigen Einzeltests. Er importiert die bereits angelegte Konstante `CUSTOMER_TYPES`.

<details>
<summary>Vergleichsstand: parametrisierte Tests</summary>

Erstelle oder ersetze die Datei `tests/test_discount.py`:

```python
from decimal import Decimal

import pytest

from shop.discount import CUSTOMER_TYPES, calculate_discount, payable_total


@pytest.mark.parametrize(
    ("customer_type", "subtotal", "erwarteter_rabatt"),
    [
        ("regular", "100.00", "0.00"),
        ("vip", "100.00", "10.00"),
        ("regular", "500.00", "25.00"),
        ("vip", "500.00", "75.00"),
        ("vip", "499.99", "50.00"),
        ("vip", "33.33", "3.33"),
        ("vip", "10.05", "1.01"),
    ],
    ids=[
        "regular-100-kein-rabatt",
        "vip-100-zehn-prozent",
        "regular-500-staffel",
        "vip-500-staffel",
        "vip-499.99-knapp-darunter",
        "vip-33.33-abrunden",
        "vip-10.05-aufrunden",
    ],
)
def test_rabattbetrag(customer_type, subtotal, erwarteter_rabatt):
    assert calculate_discount(customer_type, Decimal(subtotal)) == Decimal(
        erwarteter_rabatt
    )


def test_rabatt_ist_immer_auf_cent_gerundet():
    rabatt = calculate_discount("vip", Decimal("33.33"))
    assert rabatt.as_tuple().exponent == -2


@pytest.mark.parametrize("customer_type", CUSTOMER_TYPES)
def test_negativer_warenkorb_wird_abgelehnt(customer_type):
    with pytest.raises(ValueError, match="negativ"):
        calculate_discount(customer_type, Decimal("-1.00"))


def test_unbekannter_kundentyp_wird_abgelehnt():
    with pytest.raises(ValueError, match="gold"):
        calculate_discount("gold", Decimal("100.00"))


@pytest.mark.parametrize(
    ("customer_type", "subtotal", "erwarteter_betrag"),
    [
        ("vip", "100.00", "90.00"),
        ("regular", "100.00", "100.00"),
        ("vip", "500.00", "425.00"),
    ],
    ids=["vip-100", "regular-100", "vip-500-staffel"],
)
def test_zahlbarer_betrag(customer_type, subtotal, erwarteter_betrag):
    assert payable_total(customer_type, Decimal(subtotal)) == Decimal(
        erwarteter_betrag
    )
```

</details>

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** `16 passed`: 14 fachliche pytest-Fälle plus zwei Smoke-Tests.

<a id="lab-2-schritt-12"></a>

### Schritt 12 · Drei bekannte Fälle mit unittest schreiben

Erstelle eine `unittest.TestCase` mit `setUp`, `assertEqual` und `assertRaises`. Verwende die Fälle regular/100, vip/100 und negativer Warenwert. pytest erkennt diese Klasse automatisch mit.

<details>
<summary>Vergleichsstand: unittest-Datei</summary>

Erstelle oder ersetze die Datei `tests/test_discount_unittest.py`:

```python
import unittest
from decimal import Decimal

from shop.discount import calculate_discount


class CalculateDiscountTest(unittest.TestCase):
    def setUp(self):
        self.warenkorb = Decimal("100.00")

    def test_stammkunde_bekommt_keinen_rabatt(self):
        self.assertEqual(
            calculate_discount("regular", self.warenkorb), Decimal("0.00")
        )

    def test_vip_bekommt_zehn_prozent(self):
        self.assertEqual(calculate_discount("vip", self.warenkorb), Decimal("10.00"))

    def test_negativer_warenkorb_wird_abgelehnt(self):
        with self.assertRaises(ValueError):
            calculate_discount("vip", Decimal("-1.00"))


if __name__ == "__main__":
    unittest.main()
```

</details>

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** `19 passed`: 14 pytest-Fälle, drei unittest-Fälle und zwei Smoke-Tests.

Führe im Terminal aus:

```bash
PYTHONPATH=src python tests/test_discount_unittest.py -v
```

**Erwartet:** `Ran 3 tests` und `OK` mit dem eigenständigen unittest-Runner.

Der `pythonpath`-Eintrag aus `pyproject.toml` gilt für pytest. Deshalb setzen wir beim direkten unittest-Aufruf den Suchpfad ausdrücklich. Die PowerShell-Variante steht im Anhang.

<a id="lab-2-schritt-13"></a>

### Schritt 13 · Refactoring unter grünen Tests

**Zu den Folien:** [Folie 37: Guard Clauses: Fehlerfälle zuerst](../index.html?scrollActivationWidth=false#/3/33) zeigt, wie verschachtelte Fehlerprüfungen nach vorne gezogen werden. In deinem bisherigen Code stehen sie bereits dort. Für **Extract Function** gibt es zwei Beispiele: [Folie 38: Extract Function: Rabattsatz auslagern](../index.html?scrollActivationWidth=false#/3/34) und [Folie 39: Extract Function: Rundung auslagern](../index.html?scrollActivationWidth=false#/3/35). Die Folie nennt die Rabattsatz-Funktion `_rate_for(...)`; im Arbeitsheft heißt sie `_discount_rate(...)`. Hier beginnen wir mit der Rundung und lagern anschließend den Rabattsatz aus.

Nimm dir drei kleine Umbauten vor. Führe nach **jedem** Umbau die Tests aus:

1. Die Rundung in `_to_cents(amount)` auslagern.
2. Die Wahl des Rabattsatzes in `_discount_rate(customer_type, subtotal)` auslagern und Schwelle/Raten benennen.
3. Die beiden Eingabeprüfungen in `_reject_invalid_input(...)` auslagern.

Die Berechnungsregel bleibt dabei gleich. Der folgende Vergleichsstand zeigt alle drei Umbauten zusammen. Wenn du selbst schrittweise umbaust, vergleiche am Ende damit.

<details>
<summary>Zwischenschritt: Rundung extrahieren</summary>

Erstelle oder ersetze die Datei `src/shop/discount.py`:

```python
from decimal import Decimal, ROUND_HALF_UP


CUSTOMER_TYPES = ("regular", "vip")


def calculate_discount(customer_type: str, subtotal: Decimal) -> Decimal:
    if subtotal < 0:
        raise ValueError(f"Warenkorbwert darf nicht negativ sein: {subtotal}")
    if customer_type not in CUSTOMER_TYPES:
        raise ValueError(f"unbekannter Kundentyp: {customer_type!r}")
    rate = Decimal("0.10") if customer_type == "vip" else Decimal("0.00")
    if subtotal >= Decimal("500.00"):
        rate += Decimal("0.05")
    return _to_cents(subtotal * rate)


def payable_total(customer_type: str, subtotal: Decimal) -> Decimal:
    return subtotal - calculate_discount(customer_type, subtotal)


def _to_cents(amount: Decimal) -> Decimal:
    return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
```

</details>

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** Weiterhin `19 passed`.

<details>
<summary>Endstand nach den übrigen Extraktionen</summary>

Erstelle oder ersetze die Datei `src/shop/discount.py`:

```python
from decimal import ROUND_HALF_UP, Decimal

CUSTOMER_TYPES = ("regular", "vip")

_BASE_RATES = {
    "regular": Decimal("0.00"),
    "vip": Decimal("0.10"),
}
_VOLUME_THRESHOLD = Decimal("500.00")
_VOLUME_BONUS_RATE = Decimal("0.05")
_CENT = Decimal("0.01")


def calculate_discount(customer_type: str, subtotal: Decimal) -> Decimal:
    _reject_invalid_input(customer_type, subtotal)
    return _to_cents(subtotal * _discount_rate(customer_type, subtotal))


def payable_total(customer_type: str, subtotal: Decimal) -> Decimal:
    return subtotal - calculate_discount(customer_type, subtotal)


def _reject_invalid_input(customer_type: str, subtotal: Decimal) -> None:
    if subtotal < 0:
        raise ValueError(f"Warenkorbwert darf nicht negativ sein: {subtotal}")
    if customer_type not in CUSTOMER_TYPES:
        raise ValueError(f"unbekannter Kundentyp: {customer_type!r}")


def _discount_rate(customer_type: str, subtotal: Decimal) -> Decimal:
    rate = _BASE_RATES[customer_type]
    if subtotal >= _VOLUME_THRESHOLD:
        rate += _VOLUME_BONUS_RATE
    return rate


def _to_cents(amount: Decimal) -> Decimal:
    return amount.quantize(_CENT, rounding=ROUND_HALF_UP)
```

</details>

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** Weiterhin `19 passed`.

Führe im Terminal aus:

```bash
python -m pytest -q --cov=shop --cov-branch --cov-report=term-missing
```

**Erwartet:** `19 passed`; die Rabattfunktion erreicht 100 % Zeilen- und Zweigüberdeckung.

**Fertig, wenn:** alle Regeln der Testfallliste geprüft sind, du einen roten und grünen Lauf erklären kannst und das Refactoring die Tests grün gelassen hat. Ergänze deine tatsächlichen Beobachtungen in `TDD_LOG.md`.

Die vorhandene Musterlösung von Lab 2 zählt 17 Tests, weil sie die beiden Smoke-Tests nicht enthält. Dein Durchlauf zählt deshalb korrekt 19. Lab 3 startet in einem anderen Ordner mit dem bereitgestellten fachlichen Stand.

## Lab 3 · Abhängigkeiten im Test ersetzen

Die Bestellung nutzt Versandtarife und das Datum. Der Anwendungscode ist vorbereitet. Du schreibst die Tests so, dass weder ein echter Versanddienst noch der heutige Tag ihr Ergebnis bestimmt.

<a id="lab-3-schritt-1"></a>

### Schritt 1 · Eigenen Arbeitsordner vorbereiten

Der Startstand für dieses Lab enthält 17 fertige Rabatt-Tests und 13 noch rote Aufgaben-Tests. Öffne einen neuen Übungsordner. Dein bisheriges Projekt bleibt erhalten. Verwende einen noch nicht vorhandenen Zielordner; wenn du wiederholen möchtest, hänge zum Beispiel `-zweiter-versuch` an.

```bash
cd "$SEMINAR/uebungen"
mkdir lab03
cp -R "$SEMINAR/labs/lab_3_testdoubles/start/." lab03/
cd lab03
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Öffne diesen Ordner auch in VS Code und wähle seinen `.venv`-Interpreter. In einem neuen Terminal setze `SEMINAR` erneut wie am Anfang der Anleitung. Alle folgenden Dateipfade beziehen sich auf diesen neuen Übungsordner.

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** `13 failed, 17 passed`. Die TODOs in den Testdateien sind der Grund für die roten Tests.

<a id="lab-3-schritt-2"></a>

### Schritt 2 · Bestellung und Abhängigkeit ansehen

Öffne `src/shop/order.py` und `src/shop/shipping.py`. Lies zunächst diese Schnittstellen:

- `Order.total(shipping, today=None)` bekommt den Versanddienst als Objekt.
- `shipping.cost_for(country, weight_kg)` liefert die Versandkosten.
- `Order.total_via_rate_lookup(...)` verwendet die importierte Funktion `fetch_rate`.
- Ab 200,00 € Warenwert und im Dezember ist der Versand kostenlos.

Die Standardbestellung ist VIP / DE / ein Notebook für 100,00 € / 1,5 kg. Im Juni lautet der Endbetrag **100,00 − 10,00 + 4,99 = 94,99 €**. Im Dezember sind es 90,00 €. Deshalb verwenden die folgenden Tests feste Datumswerte.

<a id="lab-3-schritt-3"></a>

### Schritt 3 · Fake mit fester Tariftabelle bauen

Führe im Terminal aus:

```bash
python -m pytest -q tests/test_order_fake.py
```

**Erwartet:** Die fünf vorgegebenen Fake-Tests scheitern, solange `cost_for` noch `NotImplementedError` wirft.

Ergänze in `tests/conftest.py` die Tabelle und `cost_for`: DE kostet 4,99 €, AT 7,99 €, ein unbekanntes Land löst `ValueError` aus. Der Fake ignoriert das Gewicht. Die Fixtures darunter bleiben erhalten.

<details>
<summary>Vergleichsstand: kompletter Fake mit Fixtures</summary>

Erstelle oder ersetze die Datei `tests/conftest.py`:

```python
from decimal import Decimal

import pytest

from shop.order import LineItem, Order


class FakeShippingService:

    RATES = {
        "DE": Decimal("4.99"),
        "AT": Decimal("7.99"),
    }

    def __init__(self):
        self.calls = []

    def cost_for(self, country: str, weight_kg: Decimal) -> Decimal:
        self.calls.append((country, weight_kg))
        try:
            return self.RATES[country]
        except KeyError:
            raise ValueError(f"kein Versandtarif fuer {country!r}") from None


@pytest.fixture
def fake_shipping() -> FakeShippingService:
    return FakeShippingService()


@pytest.fixture
def standardbestellung() -> Order:
    return Order(
        "vip",
        "DE",
        [LineItem("Notebook", Decimal("100.00"), 1, Decimal("1.5"))],
    )
```

</details>

Führe im Terminal aus:

```bash
python -m pytest -q tests/test_order_fake.py
```

**Erwartet:** `5 passed`, darunter der Juni-Endbetrag 94,99 €.

`fake_shipping` ist eine Fixture. pytest erstellt für jeden Test eine frische Instanz. Der Fake liefert echte Werte aus einer einfachen Tabelle.

<a id="lab-3-schritt-4"></a>

### Schritt 4 · Mit einem Mock den Aufruf prüfen

Führe im Terminal aus:

```bash
python -m pytest -q tests/test_order_mock.py
```

**Erwartet:** Die zwei vorbereiteten Aufgaben-Tests sind rot.

Erzeuge `Mock(spec=ShippingService)`. Gib für `cost_for` den Wert `Decimal("4.99")` vor. Prüfe zuerst den Endbetrag, dann den Aufruf mit Land und Gewicht. Bei kostenlosem Versand prüfst du, dass keine Tarifanfrage stattfindet.

Der dritte Test im Vergleichsstand zeigt, dass `spec` einen unbekannten Methodennamen zurückweist.

<details>
<summary>Vergleichsstand: Ergebnis, Aufruf und Tippfehler</summary>

Erstelle oder ersetze die Datei `tests/test_order_mock.py`:

```python
from datetime import date
from decimal import Decimal
from unittest.mock import Mock

import pytest

from shop.order import LineItem, Order
from shop.shipping import ShippingService

IM_JUNI = date(2026, 6, 15)


def test_versanddienst_wird_mit_land_und_gewicht_aufgerufen(standardbestellung):
    shipping = Mock(spec=ShippingService)
    shipping.cost_for.return_value = Decimal("4.99")

    result = standardbestellung.total(shipping, today=IM_JUNI)

    assert result == Decimal("94.99")
    shipping.cost_for.assert_called_once_with("DE", Decimal("1.5"))


def test_bei_freiem_versand_wird_der_dienst_gar_nicht_gefragt():
    order = Order(
        "regular",
        "DE",
        [LineItem("Monitor", Decimal("250.00"), 1, Decimal("5.0"))],
    )
    shipping = Mock(spec=ShippingService)

    result = order.total(shipping, today=IM_JUNI)

    assert result == Decimal("250.00")
    shipping.cost_for.assert_not_called()


def test_spec_schuetzt_vor_tippfehlern():
    shipping = Mock(spec=ShippingService)
    with pytest.raises(AttributeError):
        shipping.cost_for_country("DE", Decimal("1.5"))
```

</details>

Führe im Terminal aus:

```bash
python -m pytest -q tests/test_order_mock.py
```

**Erwartet:** `3 passed`.

<a id="lab-3-schritt-5"></a>

### Schritt 5 · Am verwendeten Namen patchen

In `order.py` steht `from shop.shipping import fetch_rate`. Die Bestellung verwendet daher den Namen **`shop.order.fetch_rate`**. Ersetze diesen Namen im Test. Ergänze die Gegenprobe am Definitionsort: Sie soll bestätigen, dass der echte Aufruf weiterhin `RuntimeError` auslöst.

Führe im Terminal aus:

```bash
python -m pytest -q tests/test_order_patch.py
```

**Erwartet:** Die beiden noch unvollständigen Patch-Tests sind rot.

<details>
<summary>Vergleichsstand: richtiger und falscher Patch-Ort</summary>

Erstelle oder ersetze die Datei `tests/test_order_patch.py`:

```python
from datetime import date
from decimal import Decimal
from unittest.mock import patch

import pytest

IM_JUNI = date(2026, 6, 15)


def test_patch_an_der_lookup_stelle_wirkt(standardbestellung):
    with patch("shop.order.fetch_rate", return_value=Decimal("4.99")) as rate:
        result = standardbestellung.total_via_rate_lookup(today=IM_JUNI)

    assert result == Decimal("94.99")
    rate.assert_called_once_with("DE")


def test_patch_an_der_definitionsstelle_wirkt_nicht(standardbestellung):
    with patch("shop.shipping.fetch_rate", return_value=Decimal("4.99")):
        with pytest.raises(RuntimeError):
            standardbestellung.total_via_rate_lookup(today=IM_JUNI)


def test_ohne_patch_schlaegt_der_netzzugriff_fehl(standardbestellung):
    with pytest.raises(RuntimeError):
        standardbestellung.total_via_rate_lookup(today=IM_JUNI)


def test_echter_shipping_service_ist_im_test_gesperrt(standardbestellung):
    from shop.shipping import ShippingService

    with pytest.raises(RuntimeError):
        standardbestellung.total(ShippingService(), today=IM_JUNI)


def test_bei_freiem_versand_wird_die_modulfunktion_nicht_gefragt():
    from shop.order import LineItem, Order

    order = Order(
        "regular",
        "DE",
        [LineItem("Monitor", Decimal("250.00"), 1, Decimal("5.0"))],
    )
    assert order.total_via_rate_lookup(today=IM_JUNI) == Decimal("250.00")
```

</details>

Führe im Terminal aus:

```bash
python -m pytest -q tests/test_order_patch.py
```

**Erwartet:** `5 passed`. Auch die Gegenprobe ist grün, weil sie die erwartete Ausnahme prüft.

<a id="lab-3-schritt-6"></a>

### Schritt 6 · Zeit und Versandgrenzen festlegen · gemeinsame Demo

Prüfe Dezember, Juni, genau 200,00 € und 199,99 €. Reiche das Datum als Parameter hinein. Die Tests sollen im Juni und im Dezember dasselbe Ergebnis liefern. Im Seminar kann dieser Abschnitt gemeinsam demonstriert werden.

<details>
<summary>Vergleichsstand: Datums- und Grenzfälle</summary>

Erstelle oder ersetze die Datei `tests/test_order_time.py`:

```python
from datetime import date
from decimal import Decimal

from shop.order import LineItem, Order, today_provider

IM_JUNI = date(2026, 6, 15)
IM_DEZEMBER = date(2026, 12, 5)


def test_ohne_injektion_liefert_die_standarduhr_ein_datum():
    assert isinstance(today_provider(), date)


def test_im_dezember_ist_der_versand_frei(standardbestellung, fake_shipping):
    assert standardbestellung.total(fake_shipping, today=IM_DEZEMBER) == Decimal("90.00")
    assert fake_shipping.calls == []


def test_ausserhalb_dezember_faellt_versand_an(standardbestellung, fake_shipping):
    assert standardbestellung.total(fake_shipping, today=IM_JUNI) == Decimal("94.99")


def test_ab_200_euro_ist_der_versand_frei(fake_shipping):
    order = Order(
        "regular",
        "DE",
        [LineItem("Monitor", Decimal("200.00"), 1, Decimal("5.0"))],
    )
    assert order.total(fake_shipping, today=IM_JUNI) == Decimal("200.00")


def test_knapp_unter_200_euro_faellt_versand_an(fake_shipping):
    order = Order(
        "regular",
        "DE",
        [LineItem("Monitor", Decimal("199.99"), 1, Decimal("5.0"))],
    )
    assert order.total(fake_shipping, today=IM_JUNI) == Decimal("204.98")


def test_beide_regeln_zusammen_geben_nur_einmal_frei_versand(fake_shipping):
    order = Order(
        "vip",
        "DE",
        [LineItem("Monitor", Decimal("250.00"), 1, Decimal("5.0"))],
    )
    assert order.total(fake_shipping, today=IM_DEZEMBER) == Decimal("225.00")
```

</details>

Führe im Terminal aus:

```bash
python -m pytest -q tests/test_order_time.py
```

**Erwartet:** `6 passed`. Unterhalb der Grenze sind es 204,98 €, an der Grenze 200,00 €.

<a id="lab-3-schritt-7"></a>

### Schritt 7 · Umgebung und Uhr mit monkeypatch ersetzen · gemeinsame Demo

Setze das Lieferland über `monkeypatch.setenv` und ersetze die Uhr mit `monkeypatch.setattr`. Bei der Uhr-Probe übergibst du bewusst kein `today`-Argument. pytest nimmt die Änderungen nach dem jeweiligen Test zurück.

<details>
<summary>Vergleichsstand: monkeypatch</summary>

Erstelle oder ersetze die Datei `tests/test_order_monkeypatch.py`:

```python
from datetime import date
from decimal import Decimal

import shop.order as order_module
import shop.shipping as shipping_module
from shop.shipping import COUNTRY_ENV, default_country

IM_JUNI = date(2026, 6, 15)
IM_DEZEMBER = date(2026, 12, 5)


def test_setenv_setzt_das_zielland(monkeypatch):
    monkeypatch.setenv(COUNTRY_ENV, "AT")
    assert default_country() == "AT"


def test_delenv_faellt_auf_de_zurueck(monkeypatch):
    monkeypatch.delenv(COUNTRY_ENV, raising=False)
    assert default_country() == "DE"


def test_setattr_ersetzt_die_uhr(monkeypatch, standardbestellung, fake_shipping):
    monkeypatch.setattr(order_module, "today_provider", lambda: IM_DEZEMBER)
    assert standardbestellung.total(fake_shipping) == Decimal("90.00")


def test_setattr_zurueck_auf_einen_normalen_tag(monkeypatch, standardbestellung, fake_shipping):
    monkeypatch.setattr(order_module, "today_provider", lambda: IM_JUNI)
    assert standardbestellung.total(fake_shipping) == Decimal("94.99")


def test_setattr_auf_die_modulfunktion_wirkt_nur_am_lookup_ort(
    monkeypatch, standardbestellung
):
    monkeypatch.setattr(order_module, "fetch_rate", lambda country: Decimal("4.99"))
    assert standardbestellung.total_via_rate_lookup(today=IM_JUNI) == Decimal("94.99")

    assert shipping_module.fetch_rate is not order_module.fetch_rate
```

</details>

Führe im Terminal aus:

```bash
python -m pytest -q tests/test_order_monkeypatch.py
```

**Erwartet:** `5 passed`.

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** `41 passed` im vollständigen Lab-3-Durchlauf.

**Fertig, wenn:** du Fake und Mock unterscheiden und den Patch-Ort begründen kannst. Zeige außerdem einen Test mit festem Datum. Lab 4 bringt diesen gesamten Stand in seinem eigenen Startordner mit.

## Lab 4 · Bestehenden Code absichern und ändern

Das Altmodul rechnet mit float und enthält ungeklärte Regeln. Zuerst beobachtest du sein Verhalten. Danach führst du einen Seam ein und refaktorierst. Eine beschlossene Regeländerung kommt erst zum Schluss.

<a id="lab-4-schritt-1"></a>

### Schritt 1 · Eigenen Arbeitsordner vorbereiten

Der Startstand für dieses Lab enthält 41 grüne Tests und das bisher ungeprüfte Modul `src/shop/legacy_pricing.py`. Öffne einen neuen Übungsordner. Dein bisheriges Projekt bleibt erhalten. Verwende einen noch nicht vorhandenen Zielordner; wenn du wiederholen möchtest, hänge zum Beispiel `-zweiter-versuch` an.

```bash
cd "$SEMINAR/uebungen"
mkdir lab04
cp -R "$SEMINAR/labs/lab_4_legacy/start/." lab04/
cd lab04
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Öffne diesen Ordner auch in VS Code und wähle seinen `.venv`-Interpreter. In einem neuen Terminal setze `SEMINAR` erneut wie am Anfang der Anleitung. Alle folgenden Dateipfade beziehen sich auf diesen neuen Übungsordner.

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** `41 passed`.

Führe im Terminal aus:

```bash
python -m pytest -q -k "legacy or characterization or approval or seam or bugfix"
```

**Erwartet:** `41 deselected`, keine ausgeführten Tests, Exitcode 5. Das Altmodul ist bisher nicht abgesichert.

<a id="lab-4-schritt-2"></a>

### Schritt 2 · Einen beobachtenden Test schreiben

Erstelle oder ersetze die Datei `tests/test_characterization.py`:

```python
from shop import legacy_pricing


def test_unbekanntes_verhalten():
    items = [{"price": 10.0, "qty": 2}]
    assert legacy_pricing.calculate_price(items, "regular") == 0
```

Führe im Terminal aus:

```bash
python -m pytest -q tests/test_characterization.py
```

**Erwartet:** `1 failed`: Der Code liefert 23,8. Die eingesetzte Null war ein Platzhalter zum Beobachten.

Erstelle oder ersetze die Datei `tests/test_characterization.py`:

```python
from shop import legacy_pricing


def test_zwei_artikel_mit_deutscher_steuer():
    items = [{"price": 10.0, "qty": 2}]
    assert legacy_pricing.calculate_price(items, "regular") == 23.8
```

Führe im Terminal aus:

```bash
python -m pytest -q tests/test_characterization.py
```

**Erwartet:** `1 passed`.

Du hast einen beobachteten Wert festgehalten. Das ist noch keine fachliche Freigabe. Lies den Code und erkläre, wie 20,00 € plus 19 % zu 23,80 € werden.

<a id="lab-4-schritt-3"></a>

### Schritt 3 · Weitere vorhandene Regeln festhalten

Wiederhole das Beobachten mit einem Buch, einem VIP-Kunden und einem zu großen Coupon. Die entscheidenden Ergebnisse sind **11,07**, **107,10** und **−12,73**. Auch den negativen Betrag halten wir zunächst fest: **pinned, not endorsed** – beobachtet, aber nicht als richtig bestätigt.

Der folgende Stand erweitert die Absicherung auf zwölf Fälle. Die Herkunft des alten negativen Ergebnisses bleibt im Kommentar sichtbar.

<details>
<summary>Vergleichsstand vor dem Bugfix</summary>

Erstelle oder ersetze die Datei `tests/test_characterization.py`:

```python
import pytest

from shop import legacy_pricing

BUCH = {"price": 10.0, "qty": 1, "category": "book"}
ZWEI_ARTIKEL = [{"price": 10.0, "qty": 2}]


@pytest.mark.parametrize(
    "case, items, customer_type, coupon, region, pinned",
    [
        ("plain_order", ZWEI_ARTIKEL, "regular", None, "DE", 23.8),
        ("book_gets_silent_discount", [BUCH], "regular", None, "DE", 11.07),
        ("vip_gets_ten_percent", [{"price": 100.0, "qty": 1}], "vip", None, "DE", 107.1),
        ("staff_pays_half", [{"price": 100.0, "qty": 1}], "staff", None, "DE", 59.5),
        ("freeship_reduces_goods_value", ZWEI_ARTIKEL, "regular", "FREESHIP", "DE", 17.86),
        ("unknown_region_falls_back_to_de", ZWEI_ARTIKEL, "regular", None, "XX", 23.8),
        ("swiss_vat_is_lower", ZWEI_ARTIKEL, "regular", None, "CH", 21.62),
        ("us_has_no_vat", ZWEI_ARTIKEL, "regular", None, "US", 20.0),
        # Pinned, not endorsed: beobachteter Altbestand, noch kein freigegebener Sollwert.
        ("coupon_can_make_price_negative", [BUCH], "regular", "SAVE20", "DE", -12.73),
        ("coupon_smaller_than_basket_still_applies",
         [{"price": 100.0, "qty": 1}], "vip", "SAVE20", "DE", 83.3),
    ],
)
def test_current_behaviour_is_pinned(case, items, customer_type, coupon, region, pinned):
    assert legacy_pricing.calculate_price(items, customer_type, coupon, region) == pinned


def test_leerer_warenkorb_kostet_nichts():
    assert legacy_pricing.calculate_price([], "regular", None, "DE") == 0.0


def test_unbekannter_coupon_wird_ignoriert():
    assert legacy_pricing.calculate_price(ZWEI_ARTIKEL, "regular", "HALLO", "DE") == 23.8
```

</details>

Führe im Terminal aus:

```bash
python -m pytest -q tests/test_characterization.py
```

**Erwartet:** `12 passed`.

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** `53 passed`.

<a id="lab-4-schritt-4"></a>

### Schritt 4 · Preisreport als Approval-Test · optionale Vertiefung

Ein Approval-Test vergleicht einen ganzen Report mit einer geprüften Referenzdatei. Der Report entsteht im Test; die Anwendung bleibt zunächst unverändert. Für diesen vollständigen Durchlauf wird die Vertiefung mit ausgeführt. Wenn du sie im Seminar auslässt, fehlt bis zum Lab-Ende jeweils ein Test.

Das Paket `approvaltests` kommt mit den Lab-Anforderungen. Falls nötig: `python -m pip install approvaltests`.

Erstelle oder ersetze die Datei `tests/test_approval_report.py`:

```python
import pytest

from shop import legacy_pricing

approvaltests = pytest.importorskip(
    "approvaltests",
    reason="approvaltests nicht installiert: pip install approvaltests",
)

from approvaltests import Options, verify  # noqa: E402
from approvaltests.reporters import PythonNativeReporter  # noqa: E402

FAELLE = [
    ("zwei Artikel je 10.00", [{"price": 10.0, "qty": 2}], "regular", None, "DE"),
    ("ein Buch 10.00", [{"price": 10.0, "qty": 1, "category": "book"}], "regular", None, "DE"),
    ("VIP, Artikel 100.00", [{"price": 100.0, "qty": 1}], "vip", None, "DE"),
    ("Mitarbeitende, 100.00", [{"price": 100.0, "qty": 1}], "staff", None, "DE"),
    ("Buch mit SAVE20", [{"price": 10.0, "qty": 1, "category": "book"}], "regular", "SAVE20", "DE"),
    ("VIP mit SAVE20", [{"price": 100.0, "qty": 1}], "vip", "SAVE20", "DE"),
    ("FREESHIP auf 20.00", [{"price": 10.0, "qty": 2}], "regular", "FREESHIP", "DE"),
    ("Schweiz", [{"price": 10.0, "qty": 2}], "regular", None, "CH"),
    ("USA", [{"price": 10.0, "qty": 2}], "regular", None, "US"),
    ("unbekannte Region XX", [{"price": 10.0, "qty": 2}], "regular", None, "XX"),
    ("leerer Warenkorb", [], "regular", None, "DE"),
]

KOPF = (
    "Fall                      | Kunde   | Coupon   | Region | Preis\n"
    "--------------------------+---------+----------+--------+---------"
)


def preisreport() -> str:
    zeilen = ["Preisreport (legacy_pricing.calculate_price)", "=" * 43, "", KOPF]
    for name, items, customer_type, coupon, region in FAELLE:
        preis = legacy_pricing.calculate_price(items, customer_type, coupon, region)
        zeilen.append(
            "{:<25} | {:<7} | {:<8} | {:<6} | {:>7.2f}".format(
                name, customer_type, coupon or "-", region, preis
            )
        )
    return "\n".join(zeilen) + "\n"


def test_preisreport():
    verify(preisreport(), options=Options().with_reporter(PythonNativeReporter()))
```

Führe im Terminal aus:

```bash
python -m pytest -q tests/test_approval_report.py
```

**Erwartet:** `1 failed`. Eine Datei `tests/test_approval_report.test_preisreport.received.txt` wurde erzeugt; die freigegebene Referenz fehlt noch.

Öffne die `.received.txt`. Prüfe die Zeilen anhand der bereits beobachteten Regeln. Der Buch-Coupon ist hier noch negativ. Erst nach dieser Prüfung gibst du den Report als Referenz frei:

```bash
cp tests/test_approval_report.test_preisreport.received.txt tests/test_approval_report.test_preisreport.approved.txt
```

Führe im Terminal aus:

```bash
python -m pytest -q tests/test_approval_report.py
```

**Erwartet:** `1 passed`.

<a id="lab-4-schritt-5"></a>

### Schritt 5 · Den benötigten Seam zuerst testen

`calculate_order_total` fragt einen nicht verfügbaren Versanddienst. Schreibe sowohl den Nachweis dieses Problems als auch Tests für einen austauschbaren Aufruf. `shipping_fn` soll die Funktion als Parameter aufnehmen; der Default-Aufruf bleibt erhalten.

Erstelle oder ersetze die Datei `tests/test_seam.py`:

```python
import pytest

from shop import legacy_pricing

ZWEI_ARTIKEL = [{"price": 10.0, "qty": 2}]


def test_ohne_seam_ist_der_code_nicht_testbar():
    with pytest.raises(RuntimeError):
        legacy_pricing.calculate_order_total(ZWEI_ARTIKEL, "regular")


def test_seam_als_parameter():
    result = legacy_pricing.calculate_order_total(
        ZWEI_ARTIKEL, "regular", shipping_fn=lambda region: 4.99
    )
    assert result == 28.79


def test_seam_als_parameter_mit_anderem_wert():
    result = legacy_pricing.calculate_order_total(
        ZWEI_ARTIKEL, "regular", shipping_fn=lambda region: 0.0
    )
    assert result == 23.8


def test_seam_ueber_den_modulnamen(monkeypatch):
    monkeypatch.setattr(legacy_pricing, "fetch_shipping_cost", lambda region: 0.0)
    assert legacy_pricing.calculate_order_total(ZWEI_ARTIKEL, "regular") == 23.8


def test_der_seam_bekommt_die_region_zu_sehen(monkeypatch):
    gesehen = []

    def stub(region):
        gesehen.append(region)
        return 1.0

    monkeypatch.setattr(legacy_pricing, "fetch_shipping_cost", stub)
    legacy_pricing.calculate_order_total(ZWEI_ARTIKEL, "regular", region="CH")
    assert gesehen == ["CH"]


def test_der_echte_dienst_bleibt_nach_dem_test_unveraendert():
    with pytest.raises(RuntimeError):
        legacy_pricing.fetch_shipping_cost("DE")
```

Führe im Terminal aus:

```bash
python -m pytest -q tests/test_seam.py
```

**Erwartet:** `2 failed, 4 passed`: Der neue Parameter `shipping_fn` wird noch nicht akzeptiert.

<details>
<summary>Grün: Versandfunktion als Parameter</summary>

Erstelle oder ersetze die Datei `src/shop/legacy_pricing.py`:

```python
VAT = {"DE": 0.19, "CH": 0.081, "US": 0.0}


def fetch_shipping_cost(region):
    raise RuntimeError(
        "shipping service not reachable - this is the dependency we need a seam for"
    )


def calculate_price(items, customer_type, coupon=None, region="DE"):
    total = 0.0
    for i in items:
        p = i["price"] * i.get("qty", 1)
        if i.get("category") == "book":
            p = p * 0.93              # implizite Buchpreisregel, nirgends dokumentiert
        total += p
    if customer_type == "vip":
        total = total - total * 0.1   # 10 Prozent, kumuliert mit Coupon
    elif customer_type == "staff":
        total = total * 0.5
    if coupon:
        if coupon.startswith("SAVE"):
            total = total - int(coupon[4:])   # Abzug VOR Steuer, ohne Untergrenze
        elif coupon == "FREESHIP":
            total = total - 4.99              # zieht vom Warenwert ab, nicht vom Versand
    total = total * (1 + VAT.get(region, 0.19))   # unbekannte Region faellt auf DE zurueck
    return round(total, 2)


def calculate_order_total(items, customer_type, coupon=None, region="DE", shipping_fn=None):
    shipping_fn = shipping_fn or fetch_shipping_cost
    return round(
        calculate_price(items, customer_type, coupon, region) + shipping_fn(region), 2
    )
```

</details>

Führe im Terminal aus:

```bash
python -m pytest -q tests/test_seam.py
```

**Erwartet:** `6 passed`: 28,79 € mit 4,99 € Versand und 23,80 € ohne Versand.

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** `60 passed`, wenn der Approval-Test dabei ist.

Der Seam ist der austauschbare Versandaufruf. Der Test entscheidet am Enabling Point, welche Funktion gilt: das Argument `shipping_fn=...` bzw. der `monkeypatch`-Aufruf.

<a id="lab-4-schritt-6"></a>

### Schritt 6 · Refaktorieren, ohne Preise zu verändern

Extrahiere in dieser Reihenfolge `_line_price`, `_items_total`, `_apply_customer_discount`, `_apply_coupon` und `_apply_vat`. Benenne `BOOK_FACTOR` und `DEFAULT_VAT`. Nach jeder eigenen Extraktion starte die gesamte Suite.

Behalte bei float die Reihenfolge der Operationen bei: `total - total * 0.1` wird nicht durch `total * 0.9` ersetzt. Die Preisuntergrenze wird hier noch nicht eingeführt.

<details>
<summary>Vergleichsstand: refaktoriert, bisheriges Verhalten erhalten</summary>

Erstelle oder ersetze die Datei `src/shop/legacy_pricing.py`:

```python
VAT = {"DE": 0.19, "CH": 0.081, "US": 0.0}

DEFAULT_VAT = 0.19

BOOK_FACTOR = 0.93



def fetch_shipping_cost(region):
    raise RuntimeError(
        "shipping service not reachable - this is the dependency we need a seam for"
    )


def _line_price(item):
    price = item["price"] * item.get("qty", 1)
    if item.get("category") == "book":
        price = price * BOOK_FACTOR
    return price


def _items_total(items):
    total = 0.0
    for item in items:
        total += _line_price(item)
    return total


def _apply_customer_discount(total, customer_type):
    if customer_type == "vip":
        return total - total * 0.1
    if customer_type == "staff":
        return total * 0.5
    return total


def _apply_coupon(total, coupon):
    if not coupon:
        return total
    if coupon.startswith("SAVE"):
        return total - int(coupon[4:])
    if coupon == "FREESHIP":
        return total - 4.99   # zieht vom Warenwert ab, nicht vom Versand
    return total


def _apply_vat(total, region):
    return total * (1 + VAT.get(region, DEFAULT_VAT))


def calculate_price(items, customer_type, coupon=None, region="DE"):
    total = _items_total(items)
    total = _apply_customer_discount(total, customer_type)
    total = _apply_coupon(total, coupon)
    total = _apply_vat(total, region)
    return round(total, 2)


def calculate_order_total(items, customer_type, coupon=None, region="DE",
                          shipping_fn=None):
    shipping_fn = shipping_fn or fetch_shipping_cost
    return round(
        calculate_price(items, customer_type, coupon, region) + shipping_fn(region), 2
    )
```

</details>

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** Weiterhin `60 passed`, einschließlich unverändertem Approval-Report.

<a id="lab-4-schritt-7"></a>

### Schritt 7 · Neue fachliche Entscheidung zuerst als Test

Die Fachseite entscheidet jetzt: Ein Coupon darf den Warenwert vor Steuer höchstens auf 0,00 senken. Ein Rest verfällt. Diese Entscheidung verändert Verhalten und ist deshalb ein Bugfix, kein Refactoring.

Erstelle oder ersetze die Datei `BUGFIX.md`:

```markdown
# Coupon-Untergrenze

Beobachtet: Ein Buch zu 10.00 mit SAVE20 lieferte -12.73.
Neue fachliche Regel: Der Nettowarenwert bleibt mindestens 0.00.
Der Coupon wird vor der Steuer angewendet; ein Rest verfällt.
```

Erstelle oder ersetze die Datei `tests/test_bugfix_floor.py`:

```python
from shop import legacy_pricing


def test_coupon_groesser_als_warenkorb_ergibt_null():
    book = {"price": 10.0, "qty": 1, "category": "book"}
    assert legacy_pricing.calculate_price([book], "regular", "SAVE20", "DE") == 0.0
```

Führe im Terminal aus:

```bash
python -m pytest -q tests/test_bugfix_floor.py
```

**Erwartet:** `1 failed`: −12,73 statt 0,00.

<details>
<summary>Grün: Untergrenze vor der Steuer anwenden</summary>

Ersetze in `src/shop/legacy_pricing.py` genau diesen Abschnitt:

```python
    total = _apply_vat(total, region)
```

durch:

```python
    total = max(total, 0.0)
    total = _apply_vat(total, region)
```

</details>

Führe im Terminal aus:

```bash
python -m pytest -q tests/test_bugfix_floor.py
```

**Erwartet:** `1 passed`.

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** `2 failed, 59 passed`: Der alte Charakterisierungstest und der Approval-Report erwarten noch das bisherige negative Ergebnis.

<a id="lab-4-schritt-8"></a>

### Schritt 8 · Alte Erwartungen nach der Entscheidung aktualisieren

Ersetze in `tests/test_characterization.py` genau diesen Abschnitt:

```python
        # Pinned, not endorsed: beobachteter Altbestand, noch kein freigegebener Sollwert.
        ("coupon_can_make_price_negative", [BUCH], "regular", "SAVE20", "DE", -12.73)
```

durch:

```python
        # Vorher -12.73; nach fachlicher Entscheidung Untergrenze 0.00, siehe BUGFIX.md.
        ("coupon_larger_than_basket_is_floored", [BUCH], "regular", "SAVE20", "DE", 0.0)
```

Führe im Terminal aus:

```bash
python -m pytest -q tests/test_characterization.py
```

**Erwartet:** `12 passed`.

Führe im Terminal aus:

```bash
python -m pytest -q tests/test_approval_report.py
```

**Erwartet:** Noch `1 failed`: Prüfe den Report-Diff. Die Buch-Coupon-Zeile ändert sich von −12,73 auf 0,00.

Vergleiche `.received.txt` und `.approved.txt`. Gib nur die beschlossene Änderung frei. Dann wiederhole den Kopierbefehl:

```bash
cp tests/test_approval_report.test_preisreport.received.txt tests/test_approval_report.test_preisreport.approved.txt
```

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** `61 passed`.

<a id="lab-4-schritt-9"></a>

### Schritt 9 · Bugfix an den Grenzen absichern

Ergänze Coupon gleich Warenwert, verschiedene Steuerregionen und einen kleineren Coupon. Der folgende komplette Testdateistand ersetzt den einzelnen ersten Bugfix-Test.

<details>
<summary>Vergleichsstand: alle Bugfix-Fälle</summary>

Erstelle oder ersetze die Datei `tests/test_bugfix_floor.py`:

```python
import pytest

from shop import legacy_pricing

BUCH = {"price": 10.0, "qty": 1, "category": "book"}


def test_coupon_groesser_als_warenkorb_ergibt_null():
    assert legacy_pricing.calculate_price([BUCH], "regular", "SAVE20", "DE") == 0.0


def test_coupon_genau_so_gross_wie_der_warenkorb_ergibt_null():
    assert legacy_pricing.calculate_price(
        [{"price": 20.0, "qty": 1}], "regular", "SAVE20", "DE"
    ) == 0.0


@pytest.mark.parametrize("region", ["DE", "CH", "US", "XX"])
def test_untergrenze_gilt_in_jeder_region(region):
    assert legacy_pricing.calculate_price([BUCH], "regular", "SAVE20", region) == 0.0


def test_kleinerer_coupon_wird_weiterhin_normal_abgezogen():
    assert legacy_pricing.calculate_price(
        [{"price": 100.0, "qty": 1}], "vip", "SAVE20", "DE"
    ) == 83.3


def test_kein_preis_wird_negativ():
    for preis in (0.0, 1.0, 5.0, 16.8, 19.99, 20.0, 25.0):
        ergebnis = legacy_pricing.calculate_price(
            [{"price": preis, "qty": 1}], "regular", "SAVE20", "DE"
        )
        assert ergebnis >= 0.0, f"negativer Preis bei {preis}"
```

</details>

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** `68 passed` im vollständigen Durchlauf; ohne Approval-Vertiefung 67.

**Fertig, wenn:** du erklären kannst, welche Tests den Altbestand festhalten, wo der Seam liegt und welche Änderung fachlich beschlossen wurde. Der negative Preis verschwindet erst nach dem neuen roten Test und der dokumentierten Entscheidung.

## Lab 5 · SQLite, Coverage und geteilte Testdaten

Diese Tests schreiben und lesen eine echte SQLite-Datei. Es ist kein Datenbankserver nötig. Du suchst eine ungeprüfte Zusage, ergänzt Tests und untersuchst ein absichtlich abhängiges Testpaar separat.

<a id="lab-5-schritt-1"></a>

### Schritt 1 · Eigenen Arbeitsordner vorbereiten

Der Startstand für dieses Lab enthält 77 grüne Tests, ein SQLite-Repository und vorgegebene Integrationstests. Öffne einen neuen Übungsordner. Dein bisheriges Projekt bleibt erhalten. Verwende einen noch nicht vorhandenen Zielordner; wenn du wiederholen möchtest, hänge zum Beispiel `-zweiter-versuch` an.

```bash
cd "$SEMINAR/uebungen"
mkdir lab05
cp -R "$SEMINAR/labs/lab_5_coverage/start/." lab05/
cd lab05
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Öffne diesen Ordner auch in VS Code und wähle seinen `.venv`-Interpreter. In einem neuen Terminal setze `SEMINAR` erneut wie am Anfang der Anleitung. Alle folgenden Dateipfade beziehen sich auf diesen neuen Übungsordner.

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** `77 passed`.

<a id="lab-5-schritt-2"></a>

### Schritt 2 · Repository und Fixture lesen

Öffne `src/shop/repository.py` und `tests/test_repository.py`. Verfolge `save`, `get` und `list_by_customer_type`.

Die Fixture `repo(tmp_path)` erzeugt eine SQLite-Datei im temporären Verzeichnis eines Tests. Jeder Test erhält eine frische Datenbank. Beträge werden als Text gespeichert und als `Decimal` rekonstruiert.

Starte einen vorhandenen Integrationstest einzeln:

Führe im Terminal aus:

```bash
python -m pytest -q tests/test_repository.py::test_gespeicherte_bestellung_kommt_unveraendert_zurueck
```

**Erwartet:** `1 passed`.

<a id="lab-5-schritt-3"></a>

### Schritt 3 · Coverage-Lücke finden

Führe im Terminal aus:

```bash
python -m pytest -q --cov=shop --cov-branch --cov-report=term-missing
```

**Erwartet:** 77 Tests grün. Im vorgegebenen Stand steht `repository.py` bei 95 %, TOTAL bei 99 %. Die fehlende Zeile ist `return None` in `get()`.

Lies die Spalte `Missing` und öffne die genannte Zeile. Zeilennummern verändern sich, wenn du Kommentare einfügst. Die fehlende Zusage lautet: Eine unbekannte Bestellnummer ergibt `None`. Dafür schreiben wir jetzt zwei Tests.

<a id="lab-5-schritt-4"></a>

### Schritt 4 · Unbekannte ID und leere Datenbank prüfen

Ergänze am Ende von `tests/test_repository.py`:

```python
def test_get_mit_unbekannter_id_gibt_none(repo):
    repo.save(notebook_bestellung())
    assert repo.get(999) is None


def test_get_auf_leerer_datenbank_gibt_none(repo):
    assert repo.get(1) is None
```

Führe im Terminal aus:

```bash
python -m pytest -q --cov=shop --cov-branch --cov-report=term-missing
```

**Erwartet:** `79 passed`; Repository und TOTAL bei 100 %. Die Anwendung erfüllte diese Fälle bereits, deshalb sind die neuen Tests sofort grün.

<a id="lab-5-schritt-5"></a>

### Schritt 5 · Eine Fixture-Abhängigkeit sichtbar machen

Kopiere ausschließlich die vorgegebene Demo in einen separaten Ordner deines Arbeitsprojekts:

```bash
mkdir -p demos
cp "$SEMINAR/labs/lab_5_coverage/demos/test_shared_scope.py" demos/
```

Führe im Terminal aus:

```bash
python -m pytest -q -c pyproject.toml demos/test_shared_scope.py
```

**Erwartet:** `2 passed`: Beide Tests teilen dieselbe Datenbank.

Führe im Terminal aus:

```bash
python -m pytest -q -c pyproject.toml demos/test_shared_scope.py::test_module_scope_sieht_den_vorigen_test
```

**Erwartet:** `1 failed`: Allein fehlt dem zweiten Test der Datensatz seines Vorgängers.

Öffne die Demo. `scope="module"` hält dieselbe Datenbank für beide Tests bereit. Der zweite Test verlässt sich auf Arbeit des ersten. Der reguläre Test unten richtet seine Daten dagegen selbst ein:

Führe im Terminal aus:

```bash
python -m pytest -q tests/test_repository.py::test_zwei_bestellungen_unabhaengig_von_anderen_tests
```

**Erwartet:** `1 passed`, auch allein.

Die Demo liegt außerhalb von `testpaths = ["tests"]` und wird im normalen Lauf nicht eingesammelt. Sie wird nicht in die nächste Übung übernommen.

<a id="lab-5-schritt-6"></a>

### Schritt 6 · Ein grüner Test ohne wirksame Prüfung

Ergänze am Ende von `tests/test_repository.py`:

```python
def test_ohne_zusicherung(repo, monkeypatch):
    repo.save(notebook_bestellung())
    monkeypatch.setattr(repo, "get", lambda order_id: None)
    repo.get(1)
    repo.list_by_customer_type("vip")
```

Führe im Terminal aus:

```bash
python -m pytest -q tests/test_repository.py::test_ohne_zusicherung
```

**Erwartet:** `1 passed`, obwohl `get` absichtlich einen falschen Wert liefert. Der Test enthält keine Assertion.

Dieser Test demonstriert die Lücke zwischen Ausführen und Prüfen. Entferne jetzt nur die gerade hinzugefügte Funktion `test_ohne_zusicherung`; die übrigen Repository-Tests bleiben erhalten.

Führe im Terminal aus:

```bash
python -m pytest -q --cov=shop --cov-branch --cov-report=term-missing
```

**Erwartet:** Wieder `79 passed`, 100 % Überdeckung.

**Fertig, wenn:** du den Fall hinter einer Coverage-Lücke erklären kannst und gesehen hast, warum ein abhängiger oder assertionsloser Test irreführend ist. 100 % Überdeckung bedeutet, dass alle gemessenen Zeilen und Zweige ausgeführt wurden. Es sagt nicht, ob alle Anforderungen und Kombinationen geprüft sind.

**Optionale Weiterführung:** Für PostgreSQL oder andere externe Dienste kann eine Testcontainers-Fixture einen echten Dienst in Docker starten. Das ist eine Erweiterung dieses SQLite-Labs und benötigt eine vorbereitete Docker-Umgebung; der hier beschriebene Durchlauf endet bei SQLite.

## Lab 6 · Eine neue Regel mit BDD und TDD entwickeln

Du klärst die Coupon-Regel, beschreibst sie als fachliches Beispiel und entwickelst sie dann mit Unit-Tests. Die bereits vorhandenen Rabattregeln dienen zuerst dazu, behave einzurichten.

<a id="lab-6-schritt-1"></a>

### Schritt 1 · Eigenen Arbeitsordner vorbereiten

Der Startstand für dieses Lab enthält 79 erfolgreiche pytest-Tests und noch keine ausführbaren Feature-Dateien. Öffne einen neuen Übungsordner. Dein bisheriges Projekt bleibt erhalten. Verwende einen noch nicht vorhandenen Zielordner; wenn du wiederholen möchtest, hänge zum Beispiel `-zweiter-versuch` an.

```bash
cd "$SEMINAR/uebungen"
mkdir lab06
cp -R "$SEMINAR/labs/lab_6_behave/start/." lab06/
cd lab06
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Öffne diesen Ordner auch in VS Code und wähle seinen `.venv`-Interpreter. In einem neuen Terminal setze `SEMINAR` erneut wie am Anfang der Anleitung. Alle folgenden Dateipfade beziehen sich auf diesen neuen Übungsordner.

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** 79 Tests bestanden.

<a id="lab-6-schritt-2"></a>

### Schritt 2 · Die Regel klären, bevor du programmierst

Spiele das Gespräch zu dritt: Eine Person vertritt die Fachseite, eine entwickelt, eine prüft. Allein beantwortest du dieselben Fragen schriftlich:

1. Gilt SAVE20 auch für Stammkunden?
2. Werden die 20 Euro vor oder nach dem Kundenrabatt abgezogen?
3. Was passiert, wenn weniger als 20 Euro übrig bleiben?
4. Was passiert bei einem unbekannten Coupon?

Für diesen Durchlauf gilt die folgende vereinbarte Regel. In einem echten Projekt muss die Fachseite offene Fragen beantworten; der Code legt die Regel nicht nebenbei fest.

Erstelle oder ersetze die Datei `DISCOVERY.md`:

```markdown
# Coupon SAVE20

- SAVE20 zieht nach dem Kundenrabatt 20.00 EUR ab.
- Der Coupon gilt für regular und vip.
- Der Zahlbetrag bleibt mindestens 0.00 EUR. Ein Rest verfällt.
- Unbekannte Coupons werden mit ValueError abgelehnt.
- Ohne Coupon bleibt die bisherige Berechnung erhalten.

| Kunde | Warenkorb | Coupon | Zahlbetrag |
|---|---|---|---|
| vip | 100.00 | SAVE20 | 70.00 |
| vip | 10.00 | SAVE20 | 0.00 |
| regular | 100.00 | SAVE20 | 80.00 |
| vip | 100.00 | keiner | 90.00 |
```

Lies die Beispiele laut vor. Die Spalten sollen auch ohne Kenntnis von Python verständlich sein.

<a id="lab-6-schritt-3"></a>

### Schritt 3 · Zwei bekannte Regeln als Gherkin schreiben

Lege im Projekt `features/steps/` an. Schreibe anschließend die beiden bereits implementierten Rabattfälle auf. Die englischen Schlüsselwörter gehören zur Gherkin-Syntax; die fachlichen Sätze bleiben deutsch.

Erstelle oder ersetze die Datei `features/rabatt.feature`:

```gherkin
Feature: Kundenrabatt
  Als Shop möchte ich Stammkunden und VIP-Kunden unterschiedlich belohnen.

  Scenario: Stammkunde erhält keinen Rabatt
    Given ein Kunde vom Typ "regular"
    And ein Warenkorbwert von 100.00 EUR
    When der Rabatt berechnet wird
    Then beträgt der Rabatt 0.00 EUR
    And beträgt der zahlbare Betrag 100.00 EUR

  Scenario: VIP-Kunde erhält zehn Prozent
    Given ein Kunde vom Typ "vip"
    And ein Warenkorbwert von 100.00 EUR
    When der Rabatt berechnet wird
    Then beträgt der Rabatt 10.00 EUR
    And beträgt der zahlbare Betrag 90.00 EUR
```

Lege `features/steps/rabatt_steps.py` zunächst als leere Datei an.

```python

```

Erstelle oder ersetze die Datei `behave.ini`:

```ini
[behave]
paths = features
show_timings = false
```

Führe im Terminal aus:

```bash
python -m behave
```

**Erwartet:** behave findet die Szenarien, aber meldet noch nicht gebundene Schritte (`undefined`). Das ist zunächst ein Einrichtungsproblem, noch kein fachlich roter Test.

<a id="lab-6-schritt-4"></a>

### Schritt 4 · Schritte an den Anwendungscode binden

Die Given-Schritte bereiten Daten vor. When ruft die Anwendung auf. Then vergleicht das Ergebnis mit dem Betrag aus dem Szenario. Lege zuerst den Importpfad fest: auf Modulebene in `environment.py`, damit `shop` schon beim Laden der Step-Datei gefunden wird.

Erstelle oder ersetze die Datei `features/environment.py`:

```python
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"


def use_src_on_path() -> None:
    src = str(SRC_DIR)
    if src not in sys.path:
        sys.path.insert(0, src)


use_src_on_path()


def before_all(context):
    use_src_on_path()


def before_scenario(context, scenario):
    context.customer_type = None
    context.subtotal = None
    context.discount = None
    context.total = None
    context.coupon = None
```

Erstelle oder ersetze die Datei `features/steps/rabatt_steps.py`:

```python
from decimal import Decimal

from behave import given, then, when

from shop.discount import calculate_discount, payable_total


@given('ein Kunde vom Typ "{customer_type}"')
def step_kundentyp(context, customer_type):
    context.customer_type = customer_type


@given("ein Warenkorbwert von {amount} EUR")
def step_warenkorbwert(context, amount):
    context.subtotal = Decimal(amount)


@when("der Rabatt berechnet wird")
def step_rabatt_berechnen(context):
    context.discount = calculate_discount(context.customer_type, context.subtotal)
    context.total = payable_total(
        context.customer_type, context.subtotal
    )


@then("beträgt der Rabatt {amount} EUR")
def step_rabatt_pruefen(context, amount):
    erwartet = Decimal(amount)
    assert context.discount == erwartet, (
        f"Rabatt erwartet: {erwartet}, berechnet: {context.discount}"
    )


@then("beträgt der zahlbare Betrag {amount} EUR")
def step_zahlbar_pruefen(context, amount):
    erwartet = Decimal(amount)
    assert context.total == erwartet, (
        f"Zahlbarer Betrag erwartet: {erwartet}, berechnet: {context.total}"
    )


@given('ein Coupon "{coupon}"')
def step_coupon(context, coupon):
    context.coupon = coupon
```

Führe im Terminal aus:

```bash
python -m behave
```

**Erwartet:** 2 Szenarien und 10 Schritte bestanden.

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** Die vorhandenen 79 pytest-Tests bleiben grün.

Die Regel wurde hier noch nicht verändert. Du hast zwei vorhandene Beispiele mit dem zweiten Testwerkzeug ausführbar gemacht.

<a id="lab-6-schritt-5"></a>

### Schritt 5 · Das erste neue Coupon-Szenario schreiben

Jetzt beginnt die neue Anforderung. Schreibe zunächst nur den Fall „VIP, 100 Euro, SAVE20 → 70 Euro“.

Erstelle oder ersetze die Datei `features/coupon.feature`:

```gherkin
@coupon
Feature: Coupon nach dem Kundenrabatt
  SAVE20 zieht nach dem Kundenrabatt 20.00 EUR ab.
  Der zahlbare Betrag wird nicht negativ; ein Rest verfällt.

  Scenario: VIP nutzt SAVE20
    Given ein Kunde vom Typ "vip"
    And ein Warenkorbwert von 100.00 EUR
    And ein Coupon "SAVE20"
    When der Rabatt berechnet wird
    Then beträgt der zahlbare Betrag 70.00 EUR
```

Übergib im When-Schritt jetzt auch den Coupon. Ersetze in `features/steps/rabatt_steps.py` die Argumentzeile des Aufrufs von `payable_total`:

```python
context.customer_type, context.subtotal
```

durch:

```python
context.customer_type, context.subtotal, coupon=context.coupon
```

Erweitere in `src/shop/discount.py` zunächst nur die Signatur von `payable_total`. Der Rumpf bleibt unverändert. So können die Steps den Coupon übergeben, aber die Anwendung ignoriert ihn noch:

```python
def payable_total(customer_type: str, subtotal: Decimal) -> Decimal:
```

durch:

```python
def payable_total(
    customer_type: str, subtotal: Decimal, *, coupon: str | None = None
) -> Decimal:
```

Führe im Terminal aus:

```bash
python -m behave --tags=@coupon
```

**Erwartet:** Das Szenario ist fachlich rot: erwartet 70.00, berechnet 90.00. Ein Importfehler oder ein nicht gebundener Schritt wäre hier der falsche Fehler.

Erstelle oder ersetze die Datei `BDD_LOG.md`:

```markdown
# Meine BDD-Schritte

Trage nach jedem Lauf ein: Befehl, beobachteter Fehler, nächste Änderung.

| Anforderung | Szenario rot | Unit-Test rot | Änderung | Beide grün |
|---|---|---|---|---|
| SAVE20 für VIP | | | | |
| Nullgrenze | | | | |
| SAVE20 für regular | | | | |
```

<a id="lab-6-schritt-6"></a>

### Schritt 6 · Den passenden Unit-Test hinzufügen

Lass das rote Szenario stehen. Schreibe nun denselben fachlichen Fall direkt gegen die Anwendungsfunktion.

Erstelle oder ersetze die Datei `tests/test_coupon.py`:

```python
from decimal import Decimal
import pytest
from shop.discount import payable_total


def test_vip_nutzt_save20():
    assert payable_total("vip", Decimal("100.00"), coupon="SAVE20") == Decimal("70.00")
```

Führe im Terminal aus:

```bash
python -m pytest tests/test_coupon.py -q
```

**Erwartet:** 1 fehlgeschlagener Test: 90.00 statt 70.00.

<a id="lab-6-schritt-7"></a>

### Schritt 7 · Nur den ersten Coupon-Fall implementieren

Versuche zuerst selbst, den Test grün zu bekommen. Den Betrag null abzusichern kommt im nächsten Durchlauf.

<details>
<summary>Nächster Lösungsstand: SAVE20 abziehen</summary>

Ersetze in `src/shop/discount.py` genau diesen Abschnitt:

```python
    return subtotal - calculate_discount(customer_type, subtotal)
```

durch:

```python
    total = subtotal - calculate_discount(customer_type, subtotal)
    if coupon == "SAVE20":
        total -= Decimal("20.00")
    return total
```

</details>

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** 80 Tests bestanden.

Führe im Terminal aus:

```bash
python -m behave
```

**Erwartet:** 3 Szenarien und 15 Schritte bestanden. Der äußere BDD-Test und die inneren Unit-Tests sind grün.

<a id="lab-6-schritt-8"></a>

### Schritt 8 · Die Nullgrenze zuerst als Szenario prüfen

Ergänze jetzt das zweite Szenario. Es benutzt dieselben Steps; neue Step-Funktionen sind dafür nicht nötig.

Erstelle oder ersetze die Datei `features/coupon.feature`:

```gherkin
@coupon
Feature: Coupon nach dem Kundenrabatt
  SAVE20 zieht nach dem Kundenrabatt 20.00 EUR ab.
  Der zahlbare Betrag wird nicht negativ; ein Rest verfällt.

  Scenario: VIP nutzt SAVE20
    Given ein Kunde vom Typ "vip"
    And ein Warenkorbwert von 100.00 EUR
    And ein Coupon "SAVE20"
    When der Rabatt berechnet wird
    Then beträgt der zahlbare Betrag 70.00 EUR

  Scenario: Coupon unterschreitet die Nullgrenze nicht
    Given ein Kunde vom Typ "vip"
    And ein Warenkorbwert von 10.00 EUR
    And ein Coupon "SAVE20"
    When der Rabatt berechnet wird
    Then beträgt der zahlbare Betrag 0.00 EUR
```

Führe im Terminal aus:

```bash
python -m behave --tags=@coupon
```

**Erwartet:** Das neue Szenario scheitert: nach 10 Prozent Rabatt bleiben 9 Euro; minus 20 ergibt derzeit −11.00 statt 0.00.

Ergänze am Ende von `tests/test_coupon.py`:

```python
def test_coupon_macht_zahlbetrag_nicht_negativ():
    assert payable_total("vip", Decimal("10.00"), coupon="SAVE20") == Decimal("0.00")
```

Führe im Terminal aus:

```bash
python -m pytest tests/test_coupon.py -q
```

**Erwartet:** 1 Test grün, der neue Test rot.

<details>
<summary>Nächster Lösungsstand: Betrag bei null begrenzen</summary>

Ersetze in `src/shop/discount.py` genau diesen Abschnitt:

```python
        total -= Decimal("20.00")
```

durch:

```python
        total = max(Decimal("0.00"), total - Decimal("20.00"))
```

</details>

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** 81 Tests bestanden.

Führe im Terminal aus:

```bash
python -m behave
```

**Erwartet:** 4 Szenarien und 20 Schritte bestanden.

<a id="lab-6-schritt-9"></a>

### Schritt 9 · Stammkunden und unbekannte Coupons ergänzen

Das dritte Szenario prüft dieselbe Regel für regular. Dieser Fall darf sofort grün sein: die vorhandene Lösung kann ihn bereits.

Erstelle oder ersetze die Datei `features/coupon.feature`:

```gherkin
@coupon
Feature: Coupon nach dem Kundenrabatt
  SAVE20 zieht nach dem Kundenrabatt 20.00 EUR ab.
  Der zahlbare Betrag wird nicht negativ; ein Rest verfällt.

  Scenario: VIP nutzt SAVE20
    Given ein Kunde vom Typ "vip"
    And ein Warenkorbwert von 100.00 EUR
    And ein Coupon "SAVE20"
    When der Rabatt berechnet wird
    Then beträgt der zahlbare Betrag 70.00 EUR

  Scenario: Coupon unterschreitet die Nullgrenze nicht
    Given ein Kunde vom Typ "vip"
    And ein Warenkorbwert von 10.00 EUR
    And ein Coupon "SAVE20"
    When der Rabatt berechnet wird
    Then beträgt der zahlbare Betrag 0.00 EUR

  Scenario: Auch Stammkunden nutzen SAVE20
    Given ein Kunde vom Typ "regular"
    And ein Warenkorbwert von 100.00 EUR
    And ein Coupon "SAVE20"
    When der Rabatt berechnet wird
    Then beträgt der zahlbare Betrag 80.00 EUR
```

Ergänze am Ende von `tests/test_coupon.py`:

```python
def test_regular_nutzt_save20():
    assert payable_total("regular", Decimal("100.00"), coupon="SAVE20") == Decimal("80.00")
```

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** 82 Tests bestanden.

Führe im Terminal aus:

```bash
python -m behave
```

**Erwartet:** 5 Szenarien und 25 Schritte bestanden.

Ergänze am Ende von `tests/test_coupon.py`:

```python
def test_unbekannter_coupon_wird_abgelehnt():
    with pytest.raises(ValueError, match="Coupon"):
        payable_total("vip", Decimal("100.00"), coupon="UNBEKANNT")
```

Führe im Terminal aus:

```bash
python -m pytest tests/test_coupon.py -q
```

**Erwartet:** Der neue Test scheitert, weil bisher kein ValueError ausgelöst wird.

<details>
<summary>Nächster Lösungsstand: unbekannten Coupon ablehnen</summary>

Ersetze in `src/shop/discount.py` genau diesen Abschnitt:

```python
    if coupon == "SAVE20":
```

durch:

```python
    if coupon is not None and coupon != "SAVE20":
        raise ValueError(f"unbekannter Coupon: {coupon}")
    if coupon == "SAVE20":
```

</details>

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** 83 Tests bestanden.

Führe im Terminal aus:

```bash
python -m behave
```

**Erwartet:** Die 5 Szenarien bleiben grün.

<a id="lab-6-schritt-10"></a>

### Schritt 10 · Die Coupon-Berechnung aufräumen

Ziehe die Coupon-Behandlung in `_apply_coupon` heraus. Fasse die drei erfolgreichen Coupon-Fälle in einem parametrisierten Unit-Test zusammen. Die Erwartungen und die Anzahl der Tests bleiben gleich.

<details>
<summary>Vollständiger Endstand zum Vergleichen</summary>

Erstelle oder ersetze die Datei `src/shop/discount.py`:

```python
from decimal import ROUND_HALF_UP, Decimal

CUSTOMER_TYPES = ("regular", "vip")

_BASE_RATES = {
    "regular": Decimal("0.00"),
    "vip": Decimal("0.10"),
}
_VOLUME_THRESHOLD = Decimal("500.00")
_VOLUME_BONUS_RATE = Decimal("0.05")
_CENT = Decimal("0.01")


def calculate_discount(customer_type: str, subtotal: Decimal) -> Decimal:
    _reject_invalid_input(customer_type, subtotal)
    return _to_cents(subtotal * _discount_rate(customer_type, subtotal))


def payable_total(
    customer_type: str, subtotal: Decimal, *, coupon: str | None = None
) -> Decimal:
    total = subtotal - calculate_discount(customer_type, subtotal)
    return _apply_coupon(total, coupon)


def _apply_coupon(total: Decimal, coupon: str | None) -> Decimal:
    if coupon is None:
        return total
    if coupon != "SAVE20":
        raise ValueError(f"unbekannter Coupon: {coupon}")
    return max(Decimal("0.00"), total - Decimal("20.00"))


def _reject_invalid_input(customer_type: str, subtotal: Decimal) -> None:
    if subtotal < 0:
        raise ValueError(f"Warenkorbwert darf nicht negativ sein: {subtotal}")
    if customer_type not in CUSTOMER_TYPES:
        raise ValueError(f"unbekannter Kundentyp: {customer_type!r}")


def _discount_rate(customer_type: str, subtotal: Decimal) -> Decimal:
    rate = _BASE_RATES[customer_type]
    if subtotal >= _VOLUME_THRESHOLD:
        rate += _VOLUME_BONUS_RATE
    return rate


def _to_cents(amount: Decimal) -> Decimal:
    return amount.quantize(_CENT, rounding=ROUND_HALF_UP)
```

Erstelle oder ersetze die Datei `tests/test_coupon.py`:

```python
from decimal import Decimal
import pytest
from shop.discount import payable_total

@pytest.mark.parametrize("customer,subtotal,expected", [
    ("vip", "100.00", "70.00"),
    ("vip", "10.00", "0.00"),
    ("regular", "100.00", "80.00"),
], ids=["vip-100", "nullgrenze", "regular-100"])
def test_coupon(customer, subtotal, expected):
    assert payable_total(customer, Decimal(subtotal), coupon="SAVE20") == Decimal(expected)

def test_unbekannter_coupon_wird_abgelehnt():
    with pytest.raises(ValueError, match="Coupon"):
        payable_total("vip", Decimal("100.00"), coupon="UNBEKANNT")
```

</details>

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** 83 Tests bestanden.

Führe im Terminal aus:

```bash
python -m behave
```

**Erwartet:** 5 Szenarien und 25 Schritte bestanden.

**Lab 6 ist fertig**, wenn du am ersten Coupon-Fall die Reihenfolge erklären kannst: fachliches Szenario rot → Unit-Test rot → Implementierung → beide grün → Refactoring. Ergänze deine tatsächlichen Beobachtungen in `BDD_LOG.md`.

## Lab 6b · Dieselben Szenarien mit pytest-bdd · optional

Du behältst die fünf Gherkin-Szenarien aus Lab 6 und bindest sie zusätzlich an pytest. Die Geschäftslogik bleibt dieselbe.

<a id="lab-6b-schritt-1"></a>

### Schritt 1 · Eigenen Arbeitsordner vorbereiten

Der Startstand für dieses Lab enthält deine fertigen 83 pytest-Tests und fünf behave-Szenarien aus Lab 6. Öffne einen neuen Übungsordner. Dein bisheriges Projekt bleibt erhalten. Verwende einen noch nicht vorhandenen Zielordner; wenn du wiederholen möchtest, hänge zum Beispiel `-zweiter-versuch` an.

Kopiere deinen fertigen Lab-6-Ordner in einen neuen Ordner `lab06b`. Mit diesen Befehlen werden die Projektdateien kopiert, die virtuelle Umgebung jedoch neu erstellt:

```bash
cd "$SEMINAR/uebungen"
mkdir lab06b
cp -R lab06/src lab06/tests lab06/features lab06/pyproject.toml lab06/behave.ini lab06/requirements.txt lab06b/
cd lab06b
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install pytest-bdd
```

Öffne diesen Ordner auch in VS Code und wähle seinen `.venv`-Interpreter. In einem neuen Terminal setze `SEMINAR` erneut wie am Anfang der Anleitung. Alle folgenden Dateipfade beziehen sich auf diesen neuen Übungsordner.

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** 83 Tests bestanden.

<a id="lab-6b-schritt-2"></a>

### Schritt 2 · Die Feature-Dateien an pytest binden

Lege diese Testdatei an. `scenarios()` macht aus jedem Szenario einen pytest-Test. Die zugehörigen Schritte fehlen hier noch.

Erstelle oder ersetze die Datei `tests/test_rabatt_bdd.py`:

```python
from pytest_bdd import scenarios

scenarios("../features/rabatt.feature", "../features/coupon.feature")
```

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** Die 83 bisherigen Tests bestehen; die fünf neuen BDD-Tests scheitern an fehlenden Step Definitions.

<a id="lab-6b-schritt-3"></a>

### Schritt 3 · Zustand über Fixtures weitergeben

Schreibe für die Given-Schritte Fixtures mit `target_fixture`: Kundentyp, Warenkorbwert und optionaler Coupon. Der When-Schritt liefert ein Ergebnis-Dictionary; die Then-Schritte vergleichen nur dessen Werte.

Versuche zuerst den Kundentyp selbst. Vergleiche dann mit dem folgenden vollständigen Stand. Die gewöhnliche Fixture `coupon()` liefert `None`, wenn das Szenario keinen Coupon nennt; der passende Given-Schritt ersetzt sie mit dem angegebenen Code.

<details>
<summary>Vollständige Step-Bindung für pytest-bdd</summary>

Erstelle oder ersetze die Datei `tests/test_rabatt_bdd.py`:

```python
from decimal import Decimal
import pytest

from pytest_bdd import given, parsers, scenarios, then, when

from shop.discount import calculate_discount, payable_total

scenarios("../features/rabatt.feature", "../features/coupon.feature")


@given(parsers.parse('ein Kunde vom Typ "{customer_type}"'), target_fixture="kundentyp")
def given_kundentyp(customer_type):
    return customer_type


@given(
    parsers.parse("ein Warenkorbwert von {amount} EUR"),
    target_fixture="warenkorbwert",
    converters={"amount": Decimal},
)
def given_warenkorbwert(amount):
    return amount


@when("der Rabatt berechnet wird", target_fixture="ergebnis")
def when_rabatt_berechnen(kundentyp, warenkorbwert, coupon):
    return {
        "rabatt": calculate_discount(kundentyp, warenkorbwert),
        "zahlbar": payable_total(kundentyp, warenkorbwert, coupon=coupon),
    }


@then(parsers.parse("beträgt der Rabatt {amount} EUR"), converters={"amount": Decimal})
def then_rabatt(ergebnis, amount):
    assert ergebnis["rabatt"] == amount, (
        f"Rabatt erwartet: {amount}, berechnet: {ergebnis['rabatt']}"
    )


@then(
    parsers.parse("beträgt der zahlbare Betrag {amount} EUR"),
    converters={"amount": Decimal},
)
def then_zahlbar(ergebnis, amount):
    assert ergebnis["zahlbar"] == amount, (
        f"Zahlbarer Betrag erwartet: {amount}, berechnet: {ergebnis['zahlbar']}"
    )


@pytest.fixture
def coupon():
    return None

@given(parsers.parse('ein Coupon "{code}"'), target_fixture="coupon")
def given_coupon(code):
    return code
```

</details>

Führe im Terminal aus:

```bash
python -m pytest tests/test_rabatt_bdd.py -q
```

**Erwartet:** 5 BDD-Tests bestanden.

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** 88 Tests bestanden: 83 vorhandene Tests plus 5 Szenarien.

<a id="lab-6b-schritt-4"></a>

### Schritt 4 · Beide Bindungen vergleichen

Öffne nebeneinander `features/steps/rabatt_steps.py` und `tests/test_rabatt_bdd.py`. Vergleiche Context und Fixtures, Parameterumwandlung und Assertions.

Führe im Terminal aus:

```bash
python -m behave
```

**Erwartet:** Die ursprüngliche behave-Bindung läuft weiter: 5 Szenarien bestanden.

**Lab 6b ist fertig**, wenn du denselben Szenariotext mit beiden Werkzeugen ausführen kannst. Lab 7 startet wieder aus der bereitgestellten behave-Vorlage mit 83 pytest-Tests. Die fünf zusätzlichen pytest-bdd-Tests gehören nur zu diesem optionalen Vergleich.

## Lab 7 · Szenarien variieren, auswählen und auswerten

Du ergänzt eine Beispieltabelle, wählst Szenarien über Tags aus, verwendest eine Datenbank-Fixture und erzeugst Berichte. Eine kleine Steuerfunktion zeigt nochmals, wo Anwendungslogik hingehört.

<a id="lab-7-schritt-1"></a>

### Schritt 1 · Eigenen Arbeitsordner vorbereiten

Der Startstand für dieses Lab enthält 83 pytest-Tests und die fünf Szenarien aus Lab 6; außerdem einen noch leeren Scenario Outline. Öffne einen neuen Übungsordner. Dein bisheriges Projekt bleibt erhalten. Verwende einen noch nicht vorhandenen Zielordner; wenn du wiederholen möchtest, hänge zum Beispiel `-zweiter-versuch` an.

```bash
cd "$SEMINAR/uebungen"
mkdir lab07
cp -R "$SEMINAR/labs/lab_7_tags_reports/start/." lab07/
cd lab07
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Öffne diesen Ordner auch in VS Code und wähle seinen `.venv`-Interpreter. In einem neuen Terminal setze `SEMINAR` erneut wie am Anfang der Anleitung. Alle folgenden Dateipfade beziehen sich auf diesen neuen Übungsordner.

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** 83 Tests bestanden.

<a id="lab-7-schritt-2"></a>

### Schritt 2 · Drei Fälle in einem Scenario Outline ausdrücken

Ersetze `features/rabatt.feature` durch diesen Stand. Die Tabelle enthält drei Datenzeilen; behave erzeugt daraus drei Szenarien. Die beiden normalen Szenarien und die separate `coupon.feature` bleiben erhalten.

Erstelle oder ersetze die Datei `features/rabatt.feature`:

```gherkin
Feature: Kundenrabatt
  Als Shop möchte ich Stammkunden und VIP-Kunden unterschiedlich belohnen.

  Scenario: Stammkunde erhält keinen Rabatt
    Given ein Kunde vom Typ "regular"
    And ein Warenkorbwert von 100.00 EUR
    When der Rabatt berechnet wird
    Then beträgt der Rabatt 0.00 EUR
    And beträgt der zahlbare Betrag 100.00 EUR

  Scenario: VIP-Kunde erhält zehn Prozent
    Given ein Kunde vom Typ "vip"
    And ein Warenkorbwert von 100.00 EUR
    When der Rabatt berechnet wird
    Then beträgt der Rabatt 10.00 EUR
    And beträgt der zahlbare Betrag 90.00 EUR

  Scenario Outline: Staffelrabatt
    Given ein Kunde vom Typ "<kundentyp>"
    And ein Warenkorbwert von <warenkorb> EUR
    When der Rabatt berechnet wird
    Then beträgt der Rabatt <rabatt> EUR

    Examples: Staffelgrenze 500.00
      | kundentyp | warenkorb | rabatt |
      | regular   | 500.00    | 25.00  |
      | vip       | 500.00    | 75.00  |
      | vip       | 499.99    | 50.00  |
```

Führe im Terminal aus:

```bash
python -m behave
```

**Erwartet:** 8 Szenarien und 37 Schritte bestanden: 2 normale Rabattfälle, 3 Tabellenzeilen und 3 Coupon-Fälle.

<a id="lab-7-schritt-3"></a>

### Schritt 3 · Tags setzen und unfertige Arbeit kennzeichnen

Markiere die beiden normalen Rabattfälle mit `@smoke`, den Outline mit `@staffel`. Ergänze ein ausdrücklich noch nicht spezifiziertes Versandgutschein-Szenario mit `@wip`. SAVE20 ist bereits implementiert; deshalb verwenden wir hier das noch offene FREESHIP-Beispiel.

Erstelle oder ersetze die Datei `features/rabatt.feature`:

```gherkin
Feature: Kundenrabatt
  Als Shop möchte ich Stammkunden und VIP-Kunden unterschiedlich belohnen.

  @smoke
  Scenario: Stammkunde erhält keinen Rabatt
    Given ein Kunde vom Typ "regular"
    And ein Warenkorbwert von 100.00 EUR
    When der Rabatt berechnet wird
    Then beträgt der Rabatt 0.00 EUR
    And beträgt der zahlbare Betrag 100.00 EUR

  @smoke
  Scenario: VIP-Kunde erhält zehn Prozent
    Given ein Kunde vom Typ "vip"
    And ein Warenkorbwert von 100.00 EUR
    When der Rabatt berechnet wird
    Then beträgt der Rabatt 10.00 EUR
    And beträgt der zahlbare Betrag 90.00 EUR

  @staffel
  Scenario Outline: Staffelrabatt
    Given ein Kunde vom Typ "<kundentyp>"
    And ein Warenkorbwert von <warenkorb> EUR
    When der Rabatt berechnet wird
    Then beträgt der Rabatt <rabatt> EUR

    Examples: Staffelgrenze 500.00
      | kundentyp | warenkorb | rabatt |
      | regular   | 500.00    | 25.00  |
      | vip       | 500.00    | 75.00  |
      | vip       | 499.99    | 50.00  |

  @wip
  Scenario: Versandgutschein ist noch nicht spezifiziert
    Given ein Kunde vom Typ "vip"
    And ein Warenkorbwert von 100.00 EUR
    And ein Versandgutschein "FREESHIP"
    When der Rabatt berechnet wird
    Then beträgt der zahlbare Betrag 90.00 EUR
```

Führe im Terminal aus:

```bash
python -m behave
```

**Erwartet:** Die 8 fertigen Szenarien bestehen. Das FREESHIP-Szenario scheitert an einem noch nicht gebundenen Schritt.

Führe im Terminal aus:

```bash
python -m behave --tags="not @wip"
```

**Erwartet:** 8 Szenarien bestanden, das eine WIP-Szenario übersprungen.

Ein Tag ist zunächst nur eine Markierung. Erst der Filter `not @wip` nimmt dieses Szenario aus dem Lauf. Verwende WIP nicht, um einen Fehler in einer bereits zugesagten Regel zu verstecken.

<a id="lab-7-schritt-4"></a>

### Schritt 4 · Gezielt auswählen

Führe die Filter einzeln aus und vergleiche die Auswahl. Die Anführungszeichen halten zusammengesetzte Ausdrücke zusammen.

Führe im Terminal aus:

```bash
python -m behave --tags=@smoke
```

**Erwartet:** 2 Smoke-Szenarien bestanden.

Führe im Terminal aus:

```bash
python -m behave --tags=@staffel
```

**Erwartet:** 3 Szenarien aus der Examples-Tabelle bestanden.

Führe im Terminal aus:

```bash
python -m behave --tags=@coupon
```

**Erwartet:** 3 Coupon-Szenarien bestanden.

Führe im Terminal aus:

```bash
python -m behave --tags="@smoke or @staffel"
```

**Erwartet:** 5 ausgewählte Szenarien bestanden.

<a id="lab-7-schritt-5"></a>

### Schritt 5 · Eine Datenbank für genau ein Szenario vorbereiten

Die Fixture erstellt vor dem markierten Szenario eine temporäre SQLite-Datenbank. Hinter `yield` räumt sie wieder auf. `before_tag` aktiviert sie für `@fixture.repository`.

Ersetze zuerst `features/environment.py`. Achte darauf, dass `before_scenario` das von der Fixture angelegte `context.repository` nicht auf `None` setzt.

Erstelle oder ersetze die Datei `features/environment.py`:

```python
import shutil
import sys
import tempfile
from pathlib import Path

from behave import fixture, use_fixture

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"


def use_src_on_path() -> None:
    src = str(SRC_DIR)
    if src not in sys.path:
        sys.path.insert(0, src)


use_src_on_path()


@fixture
def repository(context):
    from shop.repository import SqliteOrderRepository

    tmp_dir = Path(tempfile.mkdtemp(prefix="shop-bdd-"))
    context.repository_path = tmp_dir / "orders.sqlite"
    context.repository = SqliteOrderRepository(context.repository_path)

    yield context.repository

    shutil.rmtree(tmp_dir, ignore_errors=True)


def before_all(context):
    use_src_on_path()


def before_tag(context, tag):
    if tag == "fixture.repository":
        use_fixture(repository, context)


def before_scenario(context, scenario):
    context.customer_type = None
    context.subtotal = None
    context.discount = None
    context.total = None
    context.coupon = None
    context.order_id = None
    context.stored_order = None
```

Erstelle oder ersetze die Datei `features/steps/rabatt_steps.py`:

```python
from decimal import Decimal

from behave import given, then, when

from shop.discount import calculate_discount, payable_total
from shop.order import LineItem, Order

LAND = "DE"


@given('ein Kunde vom Typ "{customer_type}"')
def step_kundentyp(context, customer_type):
    context.customer_type = customer_type


@given("ein Warenkorbwert von {amount} EUR")
def step_warenkorbwert(context, amount):
    context.subtotal = Decimal(amount)


@when("der Rabatt berechnet wird")
def step_rabatt_berechnen(context):
    context.discount = calculate_discount(context.customer_type, context.subtotal)
    context.total = payable_total(
        context.customer_type, context.subtotal, coupon=context.coupon
    )


@then("beträgt der Rabatt {amount} EUR")
def step_rabatt_pruefen(context, amount):
    erwartet = Decimal(amount)
    assert context.discount == erwartet, (
        f"Rabatt erwartet: {erwartet}, berechnet: {context.discount}"
    )


@then("beträgt der zahlbare Betrag {amount} EUR")
def step_zahlbar_pruefen(context, amount):
    erwartet = Decimal(amount)
    assert context.total == erwartet, (
        f"Zahlbarer Betrag erwartet: {erwartet}, berechnet: {context.total}"
    )


@when("die Bestellung gespeichert wird")
def step_bestellung_speichern(context):
    bestellung = Order(
        customer_type=context.customer_type,
        country=LAND,
        items=[LineItem("Warenkorb", context.subtotal, 1)],
    )
    context.order_id = context.repository.save(bestellung)


@then("ist die Bestellung unter ihrer Nummer abrufbar")
def step_bestellung_lesen(context):
    context.stored_order = context.repository.get(context.order_id)
    assert context.stored_order is not None, (
        f"Keine Bestellung unter Nummer {context.order_id} gefunden"
    )
    assert context.stored_order.customer_type == context.customer_type, (
        f"Kundentyp erwartet: {context.customer_type}, "
        f"gelesen: {context.stored_order.customer_type}"
    )
    assert context.stored_order.subtotal() == context.subtotal, (
        f"Warenkorbwert erwartet: {context.subtotal}, "
        f"gelesen: {context.stored_order.subtotal()}"
    )


@then("beträgt der gespeicherte Rabatt {amount} EUR")
def step_gespeicherter_rabatt(context, amount):
    erwartet = Decimal(amount)
    gelesen = calculate_discount(
        context.stored_order.customer_type, context.stored_order.subtotal()
    )
    assert gelesen == erwartet, (
        f"Gespeicherter Rabatt erwartet: {erwartet}, berechnet: {gelesen}"
    )


@given('ein Coupon "{coupon}"')
def step_coupon(context, coupon):
    context.coupon = coupon
```

Erstelle oder ersetze die Datei `features/rabatt.feature`:

```gherkin
Feature: Kundenrabatt
  Als Shop möchte ich Stammkunden und VIP-Kunden unterschiedlich belohnen.

  @smoke
  Scenario: Stammkunde erhält keinen Rabatt
    Given ein Kunde vom Typ "regular"
    And ein Warenkorbwert von 100.00 EUR
    When der Rabatt berechnet wird
    Then beträgt der Rabatt 0.00 EUR
    And beträgt der zahlbare Betrag 100.00 EUR

  @smoke
  Scenario: VIP-Kunde erhält zehn Prozent
    Given ein Kunde vom Typ "vip"
    And ein Warenkorbwert von 100.00 EUR
    When der Rabatt berechnet wird
    Then beträgt der Rabatt 10.00 EUR
    And beträgt der zahlbare Betrag 90.00 EUR

  @staffel
  Scenario Outline: Staffelrabatt
    Given ein Kunde vom Typ "<kundentyp>"
    And ein Warenkorbwert von <warenkorb> EUR
    When der Rabatt berechnet wird
    Then beträgt der Rabatt <rabatt> EUR

    Examples: Staffelgrenze 500.00
      | kundentyp | warenkorb | rabatt |
      | regular   | 500.00    | 25.00  |
      | vip       | 500.00    | 75.00  |
      | vip       | 499.99    | 50.00  |

  @fixture.repository
  Scenario: Bestellung wird gespeichert
    Given ein Kunde vom Typ "vip"
    And ein Warenkorbwert von 100.00 EUR
    When der Rabatt berechnet wird
    And die Bestellung gespeichert wird
    Then ist die Bestellung unter ihrer Nummer abrufbar
    And beträgt der gespeicherte Rabatt 10.00 EUR

  @wip
  Scenario: Versandgutschein ist noch nicht spezifiziert
    Given ein Kunde vom Typ "vip"
    And ein Warenkorbwert von 100.00 EUR
    And ein Versandgutschein "FREESHIP"
    When der Rabatt berechnet wird
    Then beträgt der zahlbare Betrag 90.00 EUR
```

Führe im Terminal aus:

```bash
python -m behave --tags=@fixture.repository
```

**Erwartet:** 1 Szenario mit 6 Schritten bestanden. Die gespeicherte Bestellung wurde über ihre Nummer wieder gelesen.

Führe im Terminal aus:

```bash
python -m behave --tags="not @wip"
```

**Erwartet:** 9 Szenarien und 43 Schritte bestanden; 1 WIP-Szenario übersprungen.

Verfolge im Code: Fixture → `context.repository` → `save()` → `get()` → Assertions. Die Verbindung öffnet und schließt das Repository je Aufruf. Deshalb genügt es hier, nach dem Szenario das temporäre Verzeichnis zu entfernen.

<a id="lab-7-schritt-6"></a>

### Schritt 6 · Den Bruttobetrag als Anwendungsfunktion beginnen

Für dieses Rechenbeispiel gilt: Brutto = Netto × (1 + Steuersatz / 100), kaufmännisch auf Cent gerundet. Der Satz wird ausdrücklich übergeben. Diese Rechnung gehört in `src/shop/tax.py`.

Erstelle oder ersetze die Datei `src/shop/tax.py`:

```python
from decimal import Decimal, ROUND_HALF_UP


def gross_total(net: Decimal, tax_percent: Decimal) -> Decimal:
    raise NotImplementedError
```

Erstelle oder ersetze die Datei `tests/test_tax.py`:

```python
from decimal import Decimal
import pytest
from shop.tax import gross_total

@pytest.mark.parametrize("net,rate,expected", [
    ("90.00", "19", "107.10"),
    ("90.00", "7", "96.30"),
    ("0.05", "10", "0.06"),
])
def test_bruttobetrag(net, rate, expected):
    assert gross_total(Decimal(net), Decimal(rate)) == Decimal(expected)
```

Führe im Terminal aus:

```bash
python -m pytest tests/test_tax.py -q
```

**Erwartet:** 3 fehlgeschlagene Tests mit NotImplementedError. Die Erwartungen decken 19 Prozent, 7 Prozent und einen Rundungsfall ab.

<details>
<summary>Nächster Lösungsstand: Bruttobetrag berechnen</summary>

Ersetze in `src/shop/tax.py` genau diesen Abschnitt:

```python
    raise NotImplementedError
```

durch:

```python
    return (net * (Decimal("1") + tax_percent / Decimal("100"))).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
```

</details>

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** 86 Tests bestanden.

<a id="lab-7-schritt-7"></a>

### Schritt 7 · Ungültige Eingaben absichern

Ergänze die zwei negativen Eingaben. Prüfe erst den roten Lauf, dann ergänze die beiden Wächterklauseln.

Erstelle oder ersetze die Datei `tests/test_tax.py`:

```python
from decimal import Decimal
import pytest
from shop.tax import gross_total

@pytest.mark.parametrize("net,rate,expected", [
    ("90.00", "19", "107.10"),
    ("90.00", "7", "96.30"),
    ("0.05", "10", "0.06"),
])
def test_bruttobetrag(net, rate, expected):
    assert gross_total(Decimal(net), Decimal(rate)) == Decimal(expected)

@pytest.mark.parametrize("net,rate", [("-1", "19"), ("90", "-1")])
def test_negative_eingaben_werden_abgelehnt(net, rate):
    with pytest.raises(ValueError):
        gross_total(Decimal(net), Decimal(rate))
```

Führe im Terminal aus:

```bash
python -m pytest tests/test_tax.py -q
```

**Erwartet:** Die drei Berechnungen bestehen. Beide neuen Fehlerfälle scheitern, weil ValueError noch fehlt.

<details>
<summary>Nächster Lösungsstand: Eingaben prüfen</summary>

Erstelle oder ersetze die Datei `src/shop/tax.py`:

```python
from decimal import Decimal, ROUND_HALF_UP

def gross_total(net: Decimal, tax_percent: Decimal) -> Decimal:
    if net < 0:
        raise ValueError("Nettobetrag darf nicht negativ sein")
    if tax_percent < 0:
        raise ValueError("Steuersatz darf nicht negativ sein")
    return (net * (Decimal("1") + tax_percent / Decimal("100"))).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
```

</details>

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** 88 Tests bestanden.

<a id="lab-7-schritt-8"></a>

### Schritt 8 · Die Steuerfunktion aus einem Szenario aufrufen

Der When-Schritt ruft `gross_total` auf und speichert das Ergebnis. Then prüft dieses Ergebnis; dort steht keine nachgebaute Steuerrechnung. Der beispielhafte Steuersatz kommt aus `behave.ini`.

Erstelle oder ersetze die Datei `behave.ini`:

```ini
[behave]
paths = features
show_timings = false

[behave.userdata]
mwst = 19
```

Erstelle oder ersetze die Datei `features/steps/rabatt_steps.py`:

```python
from decimal import Decimal

from behave import given, then, when

from shop.discount import calculate_discount, payable_total
from shop.order import LineItem, Order
from shop.tax import gross_total

LAND = "DE"


@given('ein Kunde vom Typ "{customer_type}"')
def step_kundentyp(context, customer_type):
    context.customer_type = customer_type


@given("ein Warenkorbwert von {amount} EUR")
def step_warenkorbwert(context, amount):
    context.subtotal = Decimal(amount)


@when("der Rabatt berechnet wird")
def step_rabatt_berechnen(context):
    context.discount = calculate_discount(context.customer_type, context.subtotal)
    context.total = payable_total(
        context.customer_type, context.subtotal, coupon=context.coupon
    )


@then("beträgt der Rabatt {amount} EUR")
def step_rabatt_pruefen(context, amount):
    erwartet = Decimal(amount)
    assert context.discount == erwartet, (
        f"Rabatt erwartet: {erwartet}, berechnet: {context.discount}"
    )


@then("beträgt der zahlbare Betrag {amount} EUR")
def step_zahlbar_pruefen(context, amount):
    erwartet = Decimal(amount)
    assert context.total == erwartet, (
        f"Zahlbarer Betrag erwartet: {erwartet}, berechnet: {context.total}"
    )


@when("der Bruttobetrag berechnet wird")
def step_brutto_berechnen(context):
    context.tax_percent = Decimal(context.config.userdata.get("mwst", "0"))
    context.gross = gross_total(context.total, context.tax_percent)


@then("beträgt der Bruttobetrag {amount} EUR")
def step_brutto_pruefen(context, amount):
    erwartet = Decimal(amount)
    assert context.gross == erwartet, (
        f"Bruttobetrag erwartet: {erwartet}, berechnet: {context.gross} "
        f"(mwst={context.tax_percent}, netto={context.total})"
    )


@when("die Bestellung gespeichert wird")
def step_bestellung_speichern(context):
    bestellung = Order(
        customer_type=context.customer_type,
        country=LAND,
        items=[LineItem("Warenkorb", context.subtotal, 1)],
    )
    context.order_id = context.repository.save(bestellung)


@then("ist die Bestellung unter ihrer Nummer abrufbar")
def step_bestellung_lesen(context):
    context.stored_order = context.repository.get(context.order_id)
    assert context.stored_order is not None, (
        f"Keine Bestellung unter Nummer {context.order_id} gefunden"
    )
    assert context.stored_order.customer_type == context.customer_type, (
        f"Kundentyp erwartet: {context.customer_type}, "
        f"gelesen: {context.stored_order.customer_type}"
    )
    assert context.stored_order.subtotal() == context.subtotal, (
        f"Warenkorbwert erwartet: {context.subtotal}, "
        f"gelesen: {context.stored_order.subtotal()}"
    )


@then("beträgt der gespeicherte Rabatt {amount} EUR")
def step_gespeicherter_rabatt(context, amount):
    erwartet = Decimal(amount)
    gelesen = calculate_discount(
        context.stored_order.customer_type, context.stored_order.subtotal()
    )
    assert gelesen == erwartet, (
        f"Gespeicherter Rabatt erwartet: {erwartet}, berechnet: {gelesen}"
    )


@given('ein Coupon "{coupon}"')
def step_coupon(context, coupon):
    context.coupon = coupon
```

Erstelle oder ersetze die Datei `features/rabatt.feature`:

```gherkin
Feature: Kundenrabatt
  Als Shop möchte ich Stammkunden und VIP-Kunden unterschiedlich belohnen.

  @smoke
  Scenario: Stammkunde erhält keinen Rabatt
    Given ein Kunde vom Typ "regular"
    And ein Warenkorbwert von 100.00 EUR
    When der Rabatt berechnet wird
    Then beträgt der Rabatt 0.00 EUR
    And beträgt der zahlbare Betrag 100.00 EUR

  @smoke
  Scenario: VIP-Kunde erhält zehn Prozent
    Given ein Kunde vom Typ "vip"
    And ein Warenkorbwert von 100.00 EUR
    When der Rabatt berechnet wird
    Then beträgt der Rabatt 10.00 EUR
    And beträgt der zahlbare Betrag 90.00 EUR

  @smoke @mwst
  Scenario: Bruttobetrag zum zahlbaren Betrag
    Given ein Kunde vom Typ "vip"
    And ein Warenkorbwert von 100.00 EUR
    When der Rabatt berechnet wird
    And der Bruttobetrag berechnet wird
    Then beträgt der zahlbare Betrag 90.00 EUR
    And beträgt der Bruttobetrag 107.10 EUR

  @staffel
  Scenario Outline: Staffelrabatt
    Given ein Kunde vom Typ "<kundentyp>"
    And ein Warenkorbwert von <warenkorb> EUR
    When der Rabatt berechnet wird
    Then beträgt der Rabatt <rabatt> EUR

    Examples: Staffelgrenze 500.00
      | kundentyp | warenkorb | rabatt |
      | regular   | 500.00    | 25.00  |
      | vip       | 500.00    | 75.00  |
      | vip       | 499.99    | 50.00  |

  @fixture.repository
  Scenario: Bestellung wird gespeichert
    Given ein Kunde vom Typ "vip"
    And ein Warenkorbwert von 100.00 EUR
    When der Rabatt berechnet wird
    And die Bestellung gespeichert wird
    Then ist die Bestellung unter ihrer Nummer abrufbar
    And beträgt der gespeicherte Rabatt 10.00 EUR

  @wip
  Scenario: Versandgutschein ist noch nicht spezifiziert
    Given ein Kunde vom Typ "vip"
    And ein Warenkorbwert von 100.00 EUR
    And ein Versandgutschein "FREESHIP"
    When der Rabatt berechnet wird
    Then beträgt der zahlbare Betrag 90.00 EUR
```

Führe im Terminal aus:

```bash
python -m behave --tags=@mwst
```

**Erwartet:** 1 Szenario bestanden: 90.00 netto ergeben im Beispiel bei 19 Prozent 107.10 brutto.

Führe im Terminal aus:

```bash
python -m behave --tags=@mwst -D mwst=7
```

**Erwartet:** Bewusst rot: die Kommandozeile setzt 7 Prozent. Die Anwendung liefert 96.30, das unveränderte Szenario erwartet 107.10.

Führe im Terminal aus:

```bash
python -m behave --tags="not @wip"
```

**Erwartet:** Ohne Überschreibung gilt wieder der Wert aus behave.ini: 10 Szenarien, 49 Schritte bestanden, 1 Szenario und 5 Schritte übersprungen.

<a id="lab-7-schritt-9"></a>

### Schritt 9 · JUnit und JSON erzeugen

JUnit XML verwenden CI-Systeme für ihre Testansicht. JSON enthält die Szenarien und Schritte mit ihren Statuswerten. Erzeuge zuerst den vollständigen Lauf, dann einen gefilterten JSON-Bericht.

Führe im Terminal aus:

```bash
python -m behave --tags="not @wip" --junit --junit-directory reports/behave
```

**Erwartet:** 10 Szenarien bestanden, 1 übersprungen. Unter reports/behave liegen TESTS-rabatt.xml und TESTS-coupon.xml.

Führe im Terminal aus:

```bash
python -m behave --tags="@smoke or @staffel" -f json.pretty -o reports/behave.json
```

**Erwartet:** 6 ausgewählte Szenarien bestanden: drei Smoke-Fälle inklusive Steuer und drei Staffel-Fälle. Der JSON-Bericht liegt unter reports/behave.json.

Öffne die Dateien in VS Code. In `TESTS-rabatt.xml` stehen 8 Fälle, davon 1 übersprungen; `TESTS-coupon.xml` enthält 3 erfolgreiche Fälle. Im gefilterten JSON sind die nicht ausgewählten Szenarien als übersprungen enthalten. Suche nach `status`, `skipped` und `passed`.

Führe im Terminal aus:

```bash
python -m behave --tags="not @wip" -f progress
```

**Erwartet:** Die kompakte Ausgabe zeigt wieder 10 bestandene und 1 übersprungenes Szenario.

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** 88 pytest-Tests bestanden.

**Lab 7 ist fertig**, wenn du die Auswahl eines Tag-Ausdrucks vorhersagen, die Fixture zuordnen und einen fehlgeschlagenen Schritt im Bericht wiederfinden kannst.

## Lab 8 · Tests und Berichte in CI ausführen

Du ergänzt die Befehle in zwei vorbereiteten Pipelines. Zuerst erzeugst und prüfst du dieselben Berichte lokal. Danach vergleichst du die tatsächlichen Läufe auf den vorbereiteten Servern.

<a id="lab-8-schritt-1"></a>

### Schritt 1 · Eigenen Arbeitsordner vorbereiten

Der Startstand für dieses Lab enthält 88 pytest-Tests und 10 fertige behave-Szenarien plus 1 WIP-Szenario. Öffne einen neuen Übungsordner. Dein bisheriges Projekt bleibt erhalten. Verwende einen noch nicht vorhandenen Zielordner; wenn du wiederholen möchtest, hänge zum Beispiel `-zweiter-versuch` an.

```bash
cd "$SEMINAR/uebungen"
mkdir lab08
cp -R "$SEMINAR/labs/lab_8_ci/start/." lab08/
cd lab08
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Öffne diesen Ordner auch in VS Code und wähle seinen `.venv`-Interpreter. In einem neuen Terminal setze `SEMINAR` erneut wie am Anfang der Anleitung. Alle folgenden Dateipfade beziehen sich auf diesen neuen Übungsordner.

Führe im Terminal aus:

```bash
python -m pytest -q
```

**Erwartet:** 88 Tests bestanden.

Führe im Terminal aus:

```bash
python -m behave --tags="not @wip"
```

**Erwartet:** 10 Szenarien bestanden, 1 übersprungen.

<a id="lab-8-schritt-2"></a>

### Schritt 2 · Die noch fehlenden Berichte erkennen

Der Startstand enthält `scripts/check_reports.py`. Es liest die lokalen XML-Dateien. Ein grüner Konsolenlauf allein hat diese Dateien noch nicht erzeugt.

Führe im Terminal aus:

```bash
python scripts/check_reports.py
```

**Erwartet:** Das Skript meldet fehlende pytest-, behave- und Coverage-Berichte und endet mit Exitcode 1.

<a id="lab-8-schritt-3"></a>

### Schritt 3 · Die Berichtsbefehle lokal ausführen

Führe diese zwei Befehle aus dem Lab-8-Projektordner aus. Der erste schreibt Test- und Coverage-XML, der zweite eine JUnit-Datei je Feature.

Führe im Terminal aus:

```bash
python -m pytest --junitxml=reports/pytest.xml --cov=shop --cov-branch --cov-report=term-missing --cov-report=xml:reports/coverage.xml
```

**Erwartet:** 88 Tests bestanden, 100 Prozent Coverage. reports/pytest.xml und reports/coverage.xml wurden geschrieben.

Führe im Terminal aus:

```bash
python -m behave --tags="not @wip" --junit --junit-directory reports/behave
```

**Erwartet:** 10 Szenarien bestanden, 1 übersprungen; zwei XML-Dateien unter reports/behave.

Führe im Terminal aus:

```bash
python scripts/check_reports.py
```

**Erwartet:** Alle Berichte vorhanden; keine failures und keine errors. pytest: 88 Fälle. Rabatt-Feature: 8 Fälle, davon 1 übersprungen. Coupon-Feature: 3 Fälle. Zeilen- und Zweigabdeckung jeweils 1.0000.

<a id="lab-8-schritt-4"></a>

### Schritt 4 · Die vier Platzhalter in GitLab ersetzen

Öffne `.gitlab-ci.yml` in VS Code. Der Punkt am Anfang gehört zum Namen; im Finder ist die Datei gegebenenfalls ausgeblendet. Ersetze jeden Platzhalter genau einmal und behalte die YAML-Einrückung bei.

Die beiden Jobs liegen in derselben Stage. `artifacts: when: always` sorgt dafür, dass auch nach einem fehlgeschlagenen Test Berichte eingesammelt werden.

- `TODO_PYTEST_COMMAND` → `python -m pytest --junitxml=reports/pytest.xml --cov=shop --cov-branch --cov-report=term-missing --cov-report=xml:reports/coverage.xml`

- `TODO_PYTEST_XML` → `reports/pytest.xml`

- `TODO_BEHAVE_COMMAND` → `python -m behave --tags="not @wip" --junit --junit-directory reports/behave`

- `TODO_BEHAVE_XML` → `reports/behave/*.xml`

Die Befehle verwenden hier durchgehend `python -m`. Das ist dieselbe Modul-Ausführung wie im Terminal. Der bereits vorbereitete Installationsschritt versorgt das Python-Image mit den Abhängigkeiten.

<details>
<summary>GitLab-Datei nach den vier Ersetzungen</summary>

```yaml
# Lab 8: Vier TODO-Platzhalter mit Kommandos und JUnit-Pfaden ersetzen.
default:
  image: python:3.12
  before_script:
    - python -m pip install --upgrade pip
    - pip install -r requirements.txt

stages:
  - test

pytest:
  stage: test
  script:
    - python -m pytest --junitxml=reports/pytest.xml --cov=shop --cov-branch --cov-report=term-missing --cov-report=xml:reports/coverage.xml
  coverage: '/TOTAL.*? (100(?:\.0+)?\%|[1-9]?\d(?:\.\d+)?\%)$/'
  artifacts:
    when: always
    paths:
      - reports/
    reports:
      junit: reports/pytest.xml
      coverage_report:
        coverage_format: cobertura
        path: reports/coverage.xml

behave:
  stage: test
  script:
    - python -m behave --tags="not @wip" --junit --junit-directory reports/behave
  artifacts:
    when: always
    paths:
      - reports/behave/
    reports:
      junit: reports/behave/*.xml
```

</details>

<a id="lab-8-schritt-5"></a>

### Schritt 5 · Dieselben vier Platzhalter in Jenkins ersetzen

Öffne `Jenkinsfile` und führe dieselben Ersetzungen aus. Die einfachen Anführungszeichen um die `sh`- und `junit`-Argumente bleiben stehen. Die doppelten Anführungszeichen um `not @wip` gehören zum Shell-Befehl.

Der vorbereitete Docker-Agent braucht einen dafür eingerichteten Jenkins-Server. Jenkins wird im Seminar vom Trainer bereitgestellt; ein lokaler pytest-Lauf ersetzt diesen Server nicht.

- `TODO_PYTEST_COMMAND` → `python -m pytest --junitxml=reports/pytest.xml --cov=shop --cov-branch --cov-report=term-missing --cov-report=xml:reports/coverage.xml`

- `TODO_PYTEST_XML` → `reports/pytest.xml`

- `TODO_BEHAVE_COMMAND` → `python -m behave --tags="not @wip" --junit --junit-directory reports/behave`

- `TODO_BEHAVE_XML` → `reports/behave/*.xml`

<details>
<summary>Jenkinsfile nach den vier Ersetzungen</summary>

```groovy
// Lab 8: Vier TODO-Platzhalter mit Kommandos und JUnit-Pfaden ersetzen.
// Den vorbereiteten Stage- und Berichtsaufbau danach mit GitLab vergleichen.
pipeline {

    agent {
        docker {
            image 'python:3.12-slim'
            args '-v $HOME/.cache/pip:/root/.cache/pip'
        }
    }

    stages {

        stage('Install') {
            steps {
                sh 'python -m pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
                sh 'mkdir -p reports/behave'
            }
        }

        stage('Unit tests (pytest)') {
            steps {
                sh 'python -m pytest --junitxml=reports/pytest.xml --cov=shop --cov-branch --cov-report=term-missing --cov-report=xml:reports/coverage.xml'
            }
            post {
                always {
                    junit 'reports/pytest.xml'
                }
            }
        }

        stage('BDD tests (behave)') {
            steps {
                sh 'python -m behave --tags="not @wip" --junit --junit-directory reports/behave'
            }
            post {
                always {
                    junit 'reports/behave/*.xml'
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**/*.xml', fingerprint: true

            recordCoverage(
                tools: [[parser: 'COBERTURA', pattern: 'reports/coverage.xml']],
                id: 'python-coverage',
                name: 'Python Coverage',
                sourceCodeRetention: 'LAST_BUILD',
                qualityGates: [
                    [threshold: 60.0, metric: 'LINE',   baseline: 'PROJECT', criticality: 'UNSTABLE'],
                    [threshold: 50.0, metric: 'BRANCH', baseline: 'PROJECT', criticality: 'UNSTABLE']
                ]
            )

        }
    }
}
```

</details>

Führe im Terminal aus:

```bash
python -c "from pathlib import Path; assert all('TODO_' not in Path(p).read_text() for p in ['.gitlab-ci.yml', 'Jenkinsfile']); print('Keine Platzhalter mehr')"
```

**Erwartet:** Keine Platzhalter mehr. Diese kleine Prüfung ersetzt noch keinen YAML- oder Jenkins-Linter.

**Bei einem roten Test:** Jenkins bricht den normalen Ablauf beim nicht erfolgreichen `sh`-Befehl ab. Die nächste reguläre Stage wird übersprungen; `post { always { ... } }` sammelt weiterhin die vorgesehenen Berichte ein. Ein Coverage-Gate kann dagegen bei erfolgreichen Tests den Status UNSTABLE setzen. [Jenkins: Verhalten von sh](https://www.jenkins.io/doc/pipeline/steps/workflow-durable-task-step/#sh-shell-script).

GitLab führt die beiden Jobs derselben Stage unabhängig aus; ein roter pytest-Job verhindert deshalb nicht grundsätzlich einen erfolgreichen behave-Job. Die Kursdatei zeigt Coverage an, enthält aber kein Mindest-Gate. [GitLab: Stages und Artefakte](https://docs.gitlab.com/ci/yaml/).

<a id="lab-8-schritt-6"></a>

### Schritt 6 · Einen roten Unit-Test bis in den Bericht verfolgen

Lege nur für diesen Versuch die folgende zusätzliche Datei an. Die fachlichen Tests bleiben unverändert.

Erstelle oder ersetze die Datei `tests/test_ci_probe.py`:

```python
def test_ci_probe():
    assert False, "Absichtlicher Fehler für die Berichtsprüfung"
```

Führe im Terminal aus:

```bash
python -m pytest --junitxml=reports/pytest.xml --cov=shop --cov-branch --cov-report=term-missing --cov-report=xml:reports/coverage.xml
```

**Erwartet:** 1 fehlgeschlagener Test, 88 erfolgreiche Tests. pytest schreibt die XML-Datei trotz Exitcode 1.

Führe im Terminal aus:

```bash
python scripts/check_reports.py
```

**Erwartet:** Der Bericht enthält jetzt failures=1. Das Prüfskript meldet nicht in Ordnung.

Öffne `reports/pytest.xml` und suche `test_ci_probe`. Unter dem Testfall steht ein `failure`-Element mit der Fehlermeldung. Der behave-Bericht stammt noch aus dem vorigen Lauf; beim späteren grünen Abschluss erzeugst du beide Berichte erneut.

<a id="lab-8-schritt-7"></a>

### Schritt 7 · Den Versuch entfernen und den grünen Stand herstellen

Lösche ausschließlich die gerade angelegte Datei `tests/test_ci_probe.py` im Lab-8-Übungsordner. Starte anschließend beide Berichtsbefehle erneut.

Führe im Terminal aus:

```bash
python -m pytest --junitxml=reports/pytest.xml --cov=shop --cov-branch --cov-report=term-missing --cov-report=xml:reports/coverage.xml
```

**Erwartet:** Wieder 88 Tests bestanden.

Führe im Terminal aus:

```bash
python -m behave --tags="not @wip" --junit --junit-directory reports/behave
```

**Erwartet:** Wieder 10 Szenarien bestanden und 1 übersprungen.

Führe im Terminal aus:

```bash
python scripts/check_reports.py
```

**Erwartet:** Alle Berichte vorhanden, keine failures, keine errors.

<a id="lab-8-schritt-8"></a>

### Schritt 8 · Die vorbereiteten CI-Server öffnen

Dieser Teil findet am Trainerrechner oder auf einer vom Trainer freigegebenen Seminarinstanz statt. Die unten genannten Loopback-Adressen funktionieren nur auf dem Mac, auf dem die vorbereitete Umgebung läuft. Auf einem anderen Teilnehmerrechner brauchst du die vom Trainer genannte Serveradresse.

Falls die vorhandene Umgebung auf dem Trainer-Mac gestoppt ist, startet der Trainer sie so in einem separaten Terminal:

```bash
cd "$SEMINAR/ci-local"
colima start tdd-bdd-ci --activate=false --ssh-config=false
docker --context colima-tdd-bdd-ci compose start
python3 manage.py status
```

Warte, bis beide Dienste bereit sind. Öffne dann GitLab (`http://127.0.0.1:18781/root/rabattshop`) und Jenkins (`http://127.0.0.1:18780/`). Zugangsdaten kommen vom Trainer. Die privaten Betriebsdateien gehören nicht in das Teilnehmerpaket.

Die Umgebung enthält bereits vier Vergleichsfälle. Das bloße Wiederholen dieser Läufe prüft die dort gespeicherten Quellen. Um deine lokal bearbeiteten Pipeline-Dateien zu prüfen, müssen sie vorher in eine eigene Branch des Seminar-Repositories übernommen werden; das erfolgt mit dem Trainer. Kontrolliere im Build immer Branch und Commit.

<a id="lab-8-schritt-9"></a>

### Schritt 9 · Den grünen Lauf auf beiden Servern wiederholen

1. Öffne in GitLab das Projekt **root/rabattshop** und dort **Build → Pipelines**.
2. Wähle **New pipeline** bzw. **Run pipeline**, wähle die Branch **main** und starte den Lauf.
3. Warte auf das Ende beider Jobs. Öffne **pytest** und **behave** und vergleiche die Testzahlen mit dem lokalen Lauf.
4. Öffne die Testübersicht und die Job-Artefakte. Finde `pytest.xml`, `coverage.xml` und die beiden behave-XML-Dateien.
5. Öffne in Jenkins den Job rabattshop-green (`http://127.0.0.1:18780/job/rabattshop-green/`).
6. Wähle **Build Now / Jetzt bauen**. Öffne den neuen Build, dann **Console Output / Konsolenausgabe**.
7. Prüfe **SUCCESS**, beide ausgeführte Teststages, die Testübersicht und die archivierten XML-Dateien.

Erwartet sind in beiden Systemen 88 pytest-Tests und 10 erfolgreiche BDD-Szenarien bei einem übersprungenen WIP-Szenario. Menübezeichnungen können je nach Sprache und Serverversion abweichen.

<a id="lab-8-schritt-10"></a>

### Schritt 10 · Fehler und Coverage-Gate vergleichen

Starte in GitLab jeweils eine Pipeline für die vorhandene Branch. In Jenkins startest du den gleichnamigen vorbereiteten Job. Warte jeden Lauf ab und prüfe zuerst den Gesamtstatus, dann die betroffene Stage und zuletzt die Berichte.

| Fall | GitLab-Branch | Jenkins-Job | Was du beobachten sollst |
|---|---|---|---|
| Unit-Test rot | `unit-red` | `rabattshop-unit-red` | GitLab: pytest rot, behave kann grün laufen. Jenkins: FAILURE; BDD-Stage übersprungen, pytest-Fehlerbericht vorhanden. |
| BDD-Szenario rot | `bdd-red` | `rabattshop-bdd-red` | pytest bleibt grün. Der BDD-Fehler erscheint in der Testübersicht und im XML. |
| Coverage niedrig | `coverage-low` | `rabattshop-coverage-low` | Tests bleiben grün. GitLab zeigt niedrige Coverage; Jenkins wird durch sein Gate UNSTABLE. |

Die vorbereiteten Serverläufe wurden am 6. September 2026 dokumentiert: Ergebnisse und Build-Links in `ci-local/RESULTS.md` im Seminarpaket. Dieser Nachweis stammt aus jener Prüfung. Für deinen neuen Durchlauf zählen die gerade gestarteten Builds.

**Lab 8 ist fertig**, wenn lokal beide Suiten grün sind, die Berichte geprüft wurden und du an den Serverläufen den Unterschied zwischen Testfehler, übersprungener Stage und Coverage-Gate erklären kannst. Ohne verfügbare Serverinstanz ist der lokale Teil abgeschlossen; die Server-Schritte bleiben eine gemeinsame Demonstration.

## Wenn etwas nicht passt

| Meldung oder Beobachtung | Nächster konkreter Schritt |
|---|---|
| `externally-managed-environment` trotz `(.venv)` | Nutze im Projekt `./.venv/bin/python -m pip install pytest pytest-cov`. Prüfe `python -c "import sys; print(sys.executable)"`. Die Anzeige im Prompt allein beweist nicht, welches pip aufgerufen wird. |
| `No module named pip` in der venv | `./.venv/bin/python -m ensurepip --upgrade`, danach den Installationsbefehl wiederholen. |
| `no tests ran` | Bist du im Ordner mit `pyproject.toml`? Heißt die Datei `test_…py` und die Funktion `test_…`? In Lab 1 vor dem ersten Test ist diese Meldung erwartet. |
| `ModuleNotFoundError: shop` bei pytest | Wähle die venv des richtigen Labs. Prüfe `pythonpath = ["src"]` in `pyproject.toml` und den Ordner `src/shop`. |
| `ModuleNotFoundError: shop` bei behave | Prüfe den Pfadaufbau auf Modulebene in `features/environment.py`. Ein Eintrag erst in `before_all` kommt für Step-Imports zu spät. |
| `undefined` bei behave | Vergleiche den Satz einschließlich Umlauten, Anführungszeichen und Step-Typ mit dem Decorator. Ein `And` übernimmt den Typ des vorherigen Given/When/Then. |
| Test Explorer zeigt keine Tests | VS Code: richtige Projektmappe, richtiger `.venv`-Interpreter, **Python: Configure Tests → pytest → tests**, anschließend Testansicht aktualisieren. |
| Debugger hält nicht | Starte den Test mit **Debug Test**, setze den Breakpoint auf eine ausführbare Zeile und speichere die Datei vorher. |
| Zwei Tests mehr als in der Musterlösung | Prüfe, ob du die beiden Smoke-Tests aus Lab 1 behalten hast. In diesem Lab-2-Durchlauf ist das richtig: 19 statt 17. |
| Fehler an einem anderen Punkt als beschrieben | Stoppe dort. Lies zuerst den tatsächlichen Fehlertyp; ändere keine fachliche Erwartung, nur um grün zu bekommen. |

## Windows · PowerShell

Python-Code, Dateiinhalte und Befehle wie `python -m pytest` bleiben gleich. Ersetze die macOS-Befehle zum Einrichten, Aktivieren und Kopieren wie folgt.

Setze zuerst deinen tatsächlichen Seminarpfad:

```powershell
$env:SEMINAR = "C:\Seminare\python-tdd-bdd"
```

Für Lab 1:

```powershell
New-Item -ItemType Directory -Force "$env:SEMINAR\uebungen" | Out-Null
Set-Location "$env:SEMINAR\uebungen"
New-Item -ItemType Directory lab01-02 | Out-Null
Set-Location lab01-02
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install pytest pytest-cov
```

Falls die PowerShell das Aktivierungsskript blockiert, kannst du Python direkt aufrufen; die Aktivierung ist dann nicht erforderlich:

```powershell
.\.venv\Scripts\python.exe -m pip install pytest pytest-cov
.\.venv\Scripts\python.exe -m pytest -q
```

Nutze dann diesen expliziten Python-Pfad auch bei den weiteren Python-Aufrufen. Du musst dafür keine systemweite Skriptrichtlinie ändern.

Für einen neuen vorbereiteten Lab-Ordner, hier Lab 3:

```powershell
Set-Location "$env:SEMINAR\uebungen"
New-Item -ItemType Directory lab03 | Out-Null
Get-ChildItem -Force "$env:SEMINAR\labs\lab_3_testdoubles\start" | Copy-Item -Destination lab03 -Recurse
Set-Location lab03
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Passe Zielordner und Lab-Verzeichnis für die übrigen Labs an. `Get-ChildItem -Force` nimmt auch Dateien wie `.gitlab-ci.yml` mit. Die Verzeichnisse `src/shop`, `tests` und einzelne Dateien kannst du direkt im Explorer von VS Code anlegen.

Für das optionale Lab 6b kopierst du aus deinem fertigen `lab06` nur die Projektdateien, bevor du eine neue venv erstellst:

```powershell
Set-Location "$env:SEMINAR\uebungen"
New-Item -ItemType Directory lab06b | Out-Null
Copy-Item lab06\src,lab06\tests,lab06\features,lab06\pyproject.toml,lab06\behave.ini,lab06\requirements.txt -Destination lab06b -Recurse
Set-Location lab06b
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install pytest-bdd
```

Weitere Übersetzungen:

| macOS | PowerShell |
|---|---|
| `pwd` | `Get-Location` |
| `mkdir -p src/shop tests` | `New-Item -ItemType Directory -Force src/shop, tests` |
| `cp quelle ziel` | `Copy-Item quelle ziel` |
| `PYTHONPATH=src python tests/test_discount_unittest.py -v` | `$env:PYTHONPATH = "src"`, dann `python tests/test_discount_unittest.py -v`; anschließend `Remove-Item Env:PYTHONPATH` |
| `Cmd+Shift+P` | `Ctrl+Shift+P` |

## Nachschlagen

Die Anleitung arbeitet mit den Start- und Lösungsständen des Seminarpakets. Bei Abweichungen vergleiche zuerst das passende Lab-Verzeichnis, nicht eine Lösung aus einem späteren Lab.

- Originalaufgaben und Lab-Übersicht: `LABS.md` im Seminarpaket
- Referenzergebnisse: `EXPECTED_RESULTS.md` im Seminarpaket
- [Python-Tests in VS Code](https://code.visualstudio.com/docs/python/testing)
- [behave: Szenarien, Schritte und Context](https://behave.readthedocs.io/en/stable/tutorial/)
- [GitLab: CI-Konfiguration](https://docs.gitlab.com/ci/yaml/)
- [Jenkins: Shell-Schritte und Exitcodes](https://www.jenkins.io/doc/pipeline/steps/workflow-durable-task-step/#sh-shell-script)

**Prüfumfang dieser Anleitung:** Die automatisierbaren Code- und Testschritte werden in temporären Übungsordnern geprüft, einschließlich der absichtlich roten Zwischenstände. Paketinstallation, VS-Code-Klickfolgen und Windows-Befehle benötigen einen Probelauf auf dem jeweiligen Teilnehmerrechner. Die CI-Server-Schritte beziehen sich auf die vorbereitete Umgebung und ihre separat dokumentierten Läufe.

## Refactoring-Katalog

**Alle 66 Haupteinträge des offiziellen Online-Katalogs zu „Refactoring, 2. Auflage“, einschließlich der dort zugeordneten Aliasnamen.** Stand: 13. September 2026. Die Themenbereiche folgen der ersten Themenzuordnung im Katalog; ihre Überschriften sind hier ins Deutsche übersetzt.

In den Folien verwenden wir **Replace Nested Conditional with Guard Clauses** und **Extract Function**. Die Tabellen führen jeden Haupteintrag einmal auf und verlinken sein Originalbeispiel. Namen wie **Extract Method** sind Aliasnamen und werden nicht als zusätzliche Technik gezählt.

Quelle: [Offizieller Refactoring-Katalog](https://refactoring.com/catalog/). Suche mit **⌘F** bzw. **Strg+F** nach einem Fachbegriff oder Aliasnamen.

Die passende Änderung hängt vom Code ab. Refactorings wie Extract Function und Inline Function wirken in entgegengesetzte Richtungen; beide können den Code verständlicher machen. Nach jeder Änderung führen wir die vorhandenen Tests aus.

### Grundlegende Refactorings · 10 Einträge

| Fachbegriff und Originalbeispiel | Weitere Katalognamen |
|---|---|
| [Change Function Declaration](https://refactoring.com/catalog/changeFunctionDeclaration.html) | Add Parameter; Change Signature; Remove Parameter; Rename Function; Rename Method |
| [Combine Functions into Class](https://refactoring.com/catalog/combineFunctionsIntoClass.html) | — |
| [Combine Functions into Transform](https://refactoring.com/catalog/combineFunctionsIntoTransform.html) | — |
| [Encapsulate Variable](https://refactoring.com/catalog/encapsulateVariable.html) | Encapsulate Field; Self-Encapsulate Field |
| [Extract Function](https://refactoring.com/catalog/extractFunction.html) | Extract Method |
| [Extract Variable](https://refactoring.com/catalog/extractVariable.html) | Introduce Explaining Variable |
| [Inline Function](https://refactoring.com/catalog/inlineFunction.html) | Inline Method |
| [Inline Variable](https://refactoring.com/catalog/inlineVariable.html) | Inline Temp |
| [Introduce Parameter Object](https://refactoring.com/catalog/introduceParameterObject.html) | — |
| [Rename Variable](https://refactoring.com/catalog/renameVariable.html) | — |

### Kapselung · 9 Einträge

| Fachbegriff und Originalbeispiel | Weitere Katalognamen |
|---|---|
| [Encapsulate Collection](https://refactoring.com/catalog/encapsulateCollection.html) | — |
| [Encapsulate Record](https://refactoring.com/catalog/encapsulateRecord.html) | Replace Record with Data Class |
| [Extract Class](https://refactoring.com/catalog/extractClass.html) | — |
| [Hide Delegate](https://refactoring.com/catalog/hideDelegate.html) | — |
| [Inline Class](https://refactoring.com/catalog/inlineClass.html) | — |
| [Remove Middle Man](https://refactoring.com/catalog/removeMiddleMan.html) | — |
| [Replace Primitive with Object](https://refactoring.com/catalog/replacePrimitiveWithObject.html) | Replace Data Value with Object; Replace Type Code with Class |
| [Replace Temp with Query](https://refactoring.com/catalog/replaceTempWithQuery.html) | — |
| [Substitute Algorithm](https://refactoring.com/catalog/substituteAlgorithm.html) | — |

### Funktionen und Anweisungen verschieben · 10 Einträge

| Fachbegriff und Originalbeispiel | Weitere Katalognamen |
|---|---|
| [Move Field](https://refactoring.com/catalog/moveField.html) | — |
| [Move Function](https://refactoring.com/catalog/moveFunction.html) | Move Method |
| [Move Statements into Function](https://refactoring.com/catalog/moveStatementsIntoFunction.html) | — |
| [Move Statements to Callers](https://refactoring.com/catalog/moveStatementsToCallers.html) | — |
| [Remove Dead Code](https://refactoring.com/catalog/removeDeadCode.html) | — |
| [Replace Inline Code with Function Call](https://refactoring.com/catalog/replaceInlineCodeWithFunctionCall.html) | — |
| [Replace Loop with Pipeline](https://refactoring.com/catalog/replaceLoopWithPipeline.html) | — |
| [Slide Statements](https://refactoring.com/catalog/slideStatements.html) | Consolidate Duplicate Conditional Fragments |
| [Split Loop](https://refactoring.com/catalog/splitLoop.html) | — |
| [Split Phase](https://refactoring.com/catalog/splitPhase.html) | — |

### Daten und Variablen organisieren · 6 Einträge

| Fachbegriff und Originalbeispiel | Weitere Katalognamen |
|---|---|
| [Change Reference to Value](https://refactoring.com/catalog/changeReferenceToValue.html) | — |
| [Change Value to Reference](https://refactoring.com/catalog/changeValueToReference.html) | — |
| [Rename Field](https://refactoring.com/catalog/renameField.html) | — |
| [Replace Derived Variable with Query](https://refactoring.com/catalog/replaceDerivedVariableWithQuery.html) | — |
| [Replace Magic Literal](https://refactoring.com/catalog/replaceMagicLiteral.html) | Replace Magic Number with Symbolic Constant |
| [Split Variable](https://refactoring.com/catalog/splitVariable.html) | Remove Assignments to Parameters; Split Temp |

### Bedingungen vereinfachen · 7 Einträge

| Fachbegriff und Originalbeispiel | Weitere Katalognamen |
|---|---|
| [Consolidate Conditional Expression](https://refactoring.com/catalog/consolidateConditionalExpression.html) | — |
| [Decompose Conditional](https://refactoring.com/catalog/decomposeConditional.html) | — |
| [Introduce Assertion](https://refactoring.com/catalog/introduceAssertion.html) | — |
| [Introduce Special Case](https://refactoring.com/catalog/introduceSpecialCase.html) | Introduce Null Object |
| [Replace Conditional with Polymorphism](https://refactoring.com/catalog/replaceConditionalWithPolymorphism.html) | — |
| [Replace Control Flag with Break](https://refactoring.com/catalog/replaceControlFlagWithBreak.html) | Remove Control Flag |
| [Replace Nested Conditional with Guard Clauses](https://refactoring.com/catalog/replaceNestedConditionalWithGuardClauses.html) | — |

### Funktionsschnittstellen gestalten · 13 Einträge

| Fachbegriff und Originalbeispiel | Weitere Katalognamen |
|---|---|
| [Parameterize Function](https://refactoring.com/catalog/parameterizeFunction.html) | Parameterize Method |
| [Preserve Whole Object](https://refactoring.com/catalog/preserveWholeObject.html) | — |
| [Remove Flag Argument](https://refactoring.com/catalog/removeFlagArgument.html) | Replace Parameter with Explicit Methods |
| [Remove Setting Method](https://refactoring.com/catalog/removeSettingMethod.html) | — |
| [Replace Command with Function](https://refactoring.com/catalog/replaceCommandWithFunction.html) | — |
| [Replace Constructor with Factory Function](https://refactoring.com/catalog/replaceConstructorWithFactoryFunction.html) | Replace Constructor with Factory Method |
| [Replace Error Code with Exception](https://refactoring.com/catalog/replaceErrorCodeWithException.html) | — |
| [Replace Exception with Precheck](https://refactoring.com/catalog/replaceExceptionWithPrecheck.html) | Replace Exception with Test |
| [Replace Function with Command](https://refactoring.com/catalog/replaceFunctionWithCommand.html) | Replace Method with Method Object |
| [Replace Parameter with Query](https://refactoring.com/catalog/replaceParameterWithQuery.html) | Replace Parameter with Method |
| [Replace Query with Parameter](https://refactoring.com/catalog/replaceQueryWithParameter.html) | — |
| [Return Modified Value](https://refactoring.com/catalog/returnModifiedValue.html) | — |
| [Separate Query from Modifier](https://refactoring.com/catalog/separateQueryFromModifier.html) | — |

### Vererbung und Delegation · 11 Einträge

| Fachbegriff und Originalbeispiel | Weitere Katalognamen |
|---|---|
| [Collapse Hierarchy](https://refactoring.com/catalog/collapseHierarchy.html) | — |
| [Extract Superclass](https://refactoring.com/catalog/extractSuperclass.html) | — |
| [Pull Up Constructor Body](https://refactoring.com/catalog/pullUpConstructorBody.html) | — |
| [Pull Up Field](https://refactoring.com/catalog/pullUpField.html) | — |
| [Pull Up Method](https://refactoring.com/catalog/pullUpMethod.html) | — |
| [Push Down Field](https://refactoring.com/catalog/pushDownField.html) | — |
| [Push Down Method](https://refactoring.com/catalog/pushDownMethod.html) | — |
| [Remove Subclass](https://refactoring.com/catalog/removeSubclass.html) | Replace Subclass with Fields |
| [Replace Subclass with Delegate](https://refactoring.com/catalog/replaceSubclassWithDelegate.html) | — |
| [Replace Superclass with Delegate](https://refactoring.com/catalog/replaceSuperclassWithDelegate.html) | Replace Inheritance with Delegation |
| [Replace Type Code with Subclasses](https://refactoring.com/catalog/replaceTypeCodeWithSubclasses.html) | Extract Subclass; Replace Type Code with State/Strategy |

## Agentische Entwicklung mit BDD und TDD

**Ein eigenständiges Beispiel ohne Starter:** Ein Coding-Agent bearbeitet Dateien und führt Tests aus. Du klärst die fachliche Regel und prüfst seine Änderungen. BDD liefert die gemeinsam bestätigten Beispiele; TDD führt die Implementierung in kleinen Schritten.

### 1. Regel klären und Arbeitsordner anlegen

Die Anforderung lautet: „Ab 50 Euro soll der Versand kostenlos sein.“ Der Agent kann Rückfragen und Grenzfälle vorschlagen. Du bestätigst hier: **Unter 50,00 € kostet der Versand 4,99 €, ab einschließlich 50,00 € kostet er 0,00 €.** Wir verwenden nichtnegative, ganzzahlige Centbeträge; Rabatte und andere Länder gehören nicht zu diesem Beispiel.

| Warenwert | Versandkosten | Warum dieser Fall? |
|---|---|---|
| 49,99 € | 4,99 € | direkt unter der Grenze |
| 50,00 € | 0,00 € | genau auf der Grenze |
| 50,01 € | 0,00 € | direkt über der Grenze |

Lege einen leeren Ordner an und öffne ihn in deiner Entwicklungsumgebung mit Coding-Agent. Auf macOS / Linux:

```bash
mkdir agent-tdd-bdd
cd agent-tdd-bdd
python3.12 -m venv .venv
.venv/bin/python -m pip install pytest==9.1.1 behave==1.3.3
```

Unter Windows erstellst du die Umgebung mit `py -3.12 -m venv .venv` und verwendest danach `.\.venv\Scripts\python.exe` statt `.venv/bin/python`. Alle folgenden Befehle laufen aus `agent-tdd-bdd/`.

### 2. Den äußeren BDD-Zyklus starten

Gib dem Agenten diesen Auftrag zusammen mit den vier Dateiinhalten darunter:

```text
Lege diese vier Dateien unverändert im aktuellen Arbeitsordner an.
Führe zuerst pytest, dann behave mit dem Python aus .venv aus.
Zeige die tatsächlich beobachteten Ergebnisse und erkläre den Fehler.
Ändere noch keine Implementierung und halte danach an.
```

`shipping.py` – die bisherige Berechnung kennt nur die Versandpauschale:

```python
def shipping_cost(subtotal_cents: int) -> int:
    return 499
```

`test_shipping.py` – der vorhandene Test sichert diese Pauschale ab:

```python
from shipping import shipping_cost


def test_versand_unter_50_euro():
    assert shipping_cost(4999) == 499
```

`features/shipping.feature` – die bestätigten Beispiele aus dem Gespräch:

```gherkin
Feature: Versandkosten nach Warenwert
  Scenario Outline: Die Grenze für kostenlosen Versand
    Given ein Warenwert von <warenwert> Cent
    When die Versandkosten berechnet werden
    Then betragen die Versandkosten <versand> Cent

    Examples:
      | warenwert | versand |
      | 4999      | 499     |
      | 5000      | 0       |
      | 5001      | 0       |
```

`features/steps/shipping_steps.py` – die Steps rufen die Anwendung auf und vergleichen ihr Ergebnis:

```python
from behave import given, when, then
from shipping import shipping_cost


@given("ein Warenwert von {amount:d} Cent")
def given_subtotal(context, amount):
    context.subtotal = amount


@when("die Versandkosten berechnet werden")
def when_calculating(context):
    context.actual = shipping_cost(context.subtotal)


@then("betragen die Versandkosten {expected:d} Cent")
def then_shipping(context, expected):
    assert context.actual == expected, f"{context.actual} != {expected}"
```

Der Agent führt aus:

```bash
.venv/bin/python -m pytest -q
.venv/bin/python -m behave -f progress
```

**Erwartet:** pytest `1 passed`; behave `1 scenario passed, 2 failed`. Bei 5.000 und 5.001 Cent meldet die Anwendung noch **499 statt 0**. Das ist der fachliche Fehler, der die Entwicklung auslöst. Ein Importfehler oder ein undefinierter Step wäre zuerst zu beheben.

### 3. Den inneren TDD-Zyklus rot starten

Nächster Auftrag an den Agenten:

```text
Ergänze in test_shipping.py genau einen Test für die Grenze:
shipping_cost(5000) muss 0 ergeben. Führe pytest aus und zeige den
Assertion-Fehler. Ändere shipping.py noch nicht. Halte danach an.
```

Der zusätzliche Test lautet:

```python
def test_versand_ab_50_euro_kostenlos():
    assert shipping_cost(5000) == 0
```

**Erwartet:** `1 failed, 1 passed`, wegen **499 statt 0**. Prüfe den tatsächlichen Testlauf. Ein nachträglich formulierter Test würde nicht zeigen, dass er die fehlende Regel zuvor erkannt hat.

### 4. Implementieren, bis beide Ebenen grün sind

Gib jetzt frei:

```text
Ändere nur shipping.py so weit, dass die beiden Unit-Tests bestehen.
Führe danach pytest und behave aus. Verändere keine erwarteten Werte,
entferne keine Tests und überspringe keine Szenarien. Zeige die Änderung
und beide Testergebnisse. Halte danach an.
```

Eine passende Implementierung:

```python
def shipping_cost(subtotal_cents: int) -> int:
    if subtotal_cents >= 5000:
        return 0
    return 499
```

**Erwartet:** pytest `2 passed`; behave `3 scenarios passed`. Die vorhandene Pauschale bleibt abgesichert, die neue Regel gilt auch direkt über der Grenze. Die Geschäftslogik steht in `shipping.py`; der Then-Step prüft ausschließlich das Ergebnis.

### 5. Refactoring und menschliches Review

Zum Abschluss:

```text
Ersetze die beiden festen Zahlen in shipping.py durch benannte Konstanten.
Verändere weder Verhalten noch Tests. Führe beide Suiten erneut aus und
zeige den Unterschied vor und nach dem Refactoring.
```

Möglicher Endstand:

```python
FREE_SHIPPING_FROM = 5000
SHIPPING_FEE = 499


def shipping_cost(subtotal_cents: int) -> int:
    if subtotal_cents >= FREE_SHIPPING_FROM:
        return 0
    return SHIPPING_FEE
```

**Weiterhin erwartet:** 2 Unit-Tests und 3 BDD-Szenarien grün. Prüfe im Review insbesondere `>=`: Die bestätigte Regel schließt genau 50 Euro ein. Vergleiche auch Feature-Datei und Assertions mit der ursprünglichen Tabelle.

**Das Zusammenspiel:** Du bestätigst die Regel und beurteilst das Ergebnis. Der Agent übernimmt Dateiänderungen und Testläufe. Das zunächst rote BDD-Szenario hält das fachliche Ziel fest; der rote Unit-Test leitet die Codeänderung an. Grüne Tests sichern die geprüften Beispiele ab – ob diese Beispiele die Anforderung richtig beschreiben, bleibt Teil eures Reviews.
