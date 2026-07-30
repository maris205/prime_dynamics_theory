from det2_tail import derivative_constant, derivative_envelope, power_gain


def test_power_gain_is_positive():
    assert power_gain() > 0.0


def test_derivative_envelopes_decay_for_fixed_orders():
    for order in range(4):
        values = [derivative_envelope(sigma, order) for sigma in (1e-2, 1e-4, 1e-8)]
        assert values[0] > values[1] > values[2] > 0.0


def test_geometric_constant_at_order_zero():
    assert abs(derivative_constant(0, 0.7) - 1.0 / 0.3) < 1e-12
