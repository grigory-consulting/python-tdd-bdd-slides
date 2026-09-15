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
