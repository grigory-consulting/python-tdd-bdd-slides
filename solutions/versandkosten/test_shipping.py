from shipping import shipping_cost


def test_versand_unter_50_euro():
    assert shipping_cost(4999) == 499


def test_versand_ab_50_euro_kostenlos():
    assert shipping_cost(5000) == 0
