"""Step Definitions für features/rabatt.feature.

Der Standard-Matcher von behave ist "parse": {name} in der Musterzeichenkette
wird als benanntes Feld extrahiert und als Argument übergeben. Die Umwandlung
in Decimal passiert im Step, damit die Feature-Datei fachlich lesbar bleibt.

Der Scenario Outline braucht keine eigenen Steps: behave setzt die Werte aus der
Examples-Tabelle in die Schritttexte ein, danach passen dieselben Muster.
"""

from decimal import Decimal

from behave import given, then, when

from shop.discount import calculate_discount, payable_total
from shop.order import LineItem, Order
from shop.tax import gross_total

#: Lieferland der Beispielbestellung. Es spielt fuer den Rabatt keine Rolle,
#: gehoert aber zu einer vollstaendigen Bestellung.
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
    """context.repository stammt aus der Fixture zum Tag @fixture.repository.

    Gespeichert wird die Bestellung selbst, also dieselbe Order aus Lab 3 mit
    demselben SqliteOrderRepository aus Lab 5. Der Warenkorbwert des Szenarios
    steckt in einer einzigen Position.
    """
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
    """Rechnet den Rabatt aus der gelesenen Bestellung neu.

    Das Repository speichert Kundentyp und Positionen, nicht das Ergebnis der
    Rabattrechnung. Ein abgeleiteter Wert gehoert nicht in die Datenbank: er
    waere dort nur so lange richtig, wie sich die Regel nicht aendert.
    """
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
