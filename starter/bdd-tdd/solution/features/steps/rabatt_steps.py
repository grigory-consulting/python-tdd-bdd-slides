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
    context.total = payable_total(context.customer_type, context.subtotal)


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
