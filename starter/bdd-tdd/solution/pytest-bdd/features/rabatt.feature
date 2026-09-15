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
