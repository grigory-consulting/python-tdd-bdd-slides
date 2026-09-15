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
