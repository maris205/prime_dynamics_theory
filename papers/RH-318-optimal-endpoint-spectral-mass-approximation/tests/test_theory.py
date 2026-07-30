import math

from spectral_approximation import (
    LOG_BASE,
    SQRT_LOG_BASE,
    asymptotic_endpoint_energy,
    asymptotic_endpoint_norm,
    logarithmic_degree_clock,
)


def test_norm_and_energy_constants_agree():
    assert math.isclose(SQRT_LOG_BASE**2, LOG_BASE)


def test_mass_clock_inverts_exponential_growth():
    mass = math.exp(20.0 * LOG_BASE)
    assert math.isclose(logarithmic_degree_clock(mass), 20.0)


def test_asymptotic_norm_squares_to_energy():
    for mass in (1e3, 1e9):
        assert math.isclose(asymptotic_endpoint_norm(mass) ** 2, asymptotic_endpoint_energy(mass))


def test_scaled_norm_constant_is_mass_independent():
    for mass in (1e4, 1e12):
        scaled = asymptotic_endpoint_norm(mass) * math.sqrt(math.log(mass))
        assert math.isclose(scaled, SQRT_LOG_BASE)
