from spectral_prefix import construct_prefix_spectrum, power_sum, squared_mass


def test_recursive_packets_match_every_prefix_moment():
    target = [0.0, 0.4, -0.2, 0.15, 0.07, -0.03]
    spectrum = construct_prefix_spectrum(target, 0.75)
    for order, expected in enumerate(target, start=1):
        assert abs(power_sum(spectrum, order) - expected) < 1e-8


def test_constructed_spectrum_respects_modulus_cap():
    spectrum = construct_prefix_spectrum([0.0, 0.5, 0.3, 0.2, 0.1], 0.6)
    assert max(abs(value) for value in spectrum) <= 0.6 * (1.0 + 1e-12)


def test_constructed_spectrum_has_finite_mass():
    spectrum = construct_prefix_spectrum([0.0, 0.2, 0.1, 0.05], 0.5)
    assert 0.0 < squared_mass(spectrum) < float("inf")


def test_nonzero_tiny_residual_is_not_discarded():
    target = [0.0, 1.0e-15]
    spectrum = construct_prefix_spectrum(target, 0.5)
    assert spectrum
    assert abs(power_sum(spectrum, 2) - target[1]) < 1.0e-28
