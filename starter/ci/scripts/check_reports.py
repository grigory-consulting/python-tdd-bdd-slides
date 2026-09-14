#!/usr/bin/env python3
"""Prueft die Berichte, die die Pipeline einsammelt, lokal nach.

Aufruf aus dem Projektverzeichnis, nachdem pytest und behave gelaufen sind:

    python scripts/check_reports.py

Gelesen werden:

* ``reports/pytest.xml``      JUnit XML von pytest (--junitxml)
* ``reports/behave/*.xml``    JUnit XML von behave (--junit --junit-directory)
* ``reports/coverage.xml``    Cobertura XML von pytest-cov (--cov-report=xml:...)

Ausgabe je JUnit-Datei: tests, failures, errors, skipped.
Ausgabe fuer Cobertura: line-rate und branch-rate.

Exitcode 1, wenn eine erwartete Datei fehlt oder failures/errors groesser 0
sind, sonst 0. Das Skript prüft lokale Berichtsdaten. Es prüft weder Pipeline-Syntax noch
Stage-Steuerung, Plugins, Berechtigungen oder den Status eines CI-Servers.

Nur Standardbibliothek (xml.etree), damit es ueberall laeuft, wo Python laeuft.
"""

from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORTS = PROJECT_ROOT / "reports"

PYTEST_JUNIT = REPORTS / "pytest.xml"
BEHAVE_JUNIT_DIR = REPORTS / "behave"
COVERAGE_XML = REPORTS / "coverage.xml"

LINE = "-" * 72


def _int(value: str | None) -> int:
    """JUnit-Zaehler als int; fehlende Attribute zaehlen als 0."""
    try:
        return int(value) if value else 0
    except ValueError:
        return 0


def read_junit(path: Path) -> dict:
    """Summiert die Zaehler einer JUnit-Datei.

    pytest schreibt <testsuites><testsuite .../></testsuites>, behave schreibt
    ein einzelnes <testsuite> je Feature. Beide Formen werden unterstuetzt.
    """
    root = ET.parse(path).getroot()
    suites = root.iter("testsuite") if root.tag == "testsuites" else [root]

    summary = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0}
    for suite in suites:
        for key in summary:
            summary[key] += _int(suite.get(key))
    return summary


def read_cobertura(path: Path) -> dict:
    """Liest line-rate und branch-rate aus dem Wurzelelement <coverage>."""
    root = ET.parse(path).getroot()
    return {
        "line-rate": float(root.get("line-rate", "0")),
        "branch-rate": float(root.get("branch-rate", "0")),
    }


def report_junit(path: Path, problems: list) -> None:
    if not path.is_file():
        print(f"FEHLT   {path.relative_to(PROJECT_ROOT)}")
        problems.append(f"{path.name}: Datei fehlt")
        return

    summary = read_junit(path)
    print(
        f"JUNIT   {path.relative_to(PROJECT_ROOT)}: "
        f"tests={summary['tests']} "
        f"failures={summary['failures']} "
        f"errors={summary['errors']} "
        f"skipped={summary['skipped']}"
    )
    if summary["failures"] or summary["errors"]:
        problems.append(
            f"{path.name}: {summary['failures']} failures, {summary['errors']} errors"
        )


def main() -> int:
    problems: list = []

    print(LINE)
    print(f"Berichte unter {REPORTS.relative_to(PROJECT_ROOT)}/")
    print(LINE)

    # -- 1. pytest
    report_junit(PYTEST_JUNIT, problems)

    # -- 2. behave: eine XML-Datei je Feature, deshalb ueber das Verzeichnis
    behave_files = sorted(BEHAVE_JUNIT_DIR.glob("*.xml"))
    if not behave_files:
        print(f"FEHLT   {BEHAVE_JUNIT_DIR.relative_to(PROJECT_ROOT)}/*.xml")
        problems.append("reports/behave/*.xml: keine Datei gefunden")
    for path in behave_files:
        report_junit(path, problems)

    # -- 3. Coverage
    if not COVERAGE_XML.is_file():
        print(f"FEHLT   {COVERAGE_XML.relative_to(PROJECT_ROOT)}")
        problems.append(f"{COVERAGE_XML.name}: Datei fehlt")
    else:
        rates = read_cobertura(COVERAGE_XML)
        print(
            f"COBERTURA {COVERAGE_XML.relative_to(PROJECT_ROOT)}: "
            f"line-rate={rates['line-rate']:.4f} "
            f"({rates['line-rate'] * 100:.2f} Prozent) "
            f"branch-rate={rates['branch-rate']:.4f} "
            f"({rates['branch-rate'] * 100:.2f} Prozent)"
        )

    print(LINE)
    if problems:
        for problem in problems:
            print(f"PROBLEM {problem}")
        print("ERGEBNIS: nicht in Ordnung")
        return 1

    print("ERGEBNIS: alle Berichte vorhanden, keine failures, keine errors")
    return 0


if __name__ == "__main__":
    sys.exit(main())
