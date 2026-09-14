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
