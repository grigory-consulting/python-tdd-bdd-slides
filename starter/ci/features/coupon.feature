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
