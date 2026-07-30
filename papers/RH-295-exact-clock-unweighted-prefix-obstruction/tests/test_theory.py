from prefix_obstruction import escaping_spike, minimal_clock


def test_spike_has_opposite_limits():
    small_amplitude, large_budget = escaping_spike(120)
    big_amplitude, small_budget = escaping_spike(20)
    assert small_amplitude < big_amplitude
    assert large_budget > small_budget


def test_minimal_clock_grows():
    assert minimal_clock(1e-8) > minimal_clock(1e-4)
