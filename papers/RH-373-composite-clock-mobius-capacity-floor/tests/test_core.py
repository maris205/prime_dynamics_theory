from fractions import Fraction

from composite_clock import (
    I_EVEN,
    I_ODD,
    Q,
    density_coefficient,
    mobius_prefix,
    selector_score,
    verify_certificate,
)
from composite_clock.core import one_site, path_capacity, safe_transducer


def test_phase_witness_is_independent_and_has_expected_counts():
    selected = set(I_EVEN + I_ODD)
    assert len(selected) == 80
    assert not any((r + 2) % Q in selected for r in selected)
    assert sum(density_coefficient(r) == Fraction(5, 96) for r in selected) == 68
    assert sum(density_coefficient(r) == Fraction(1, 24) for r in selected) == 12
    assert sum(density_coefficient(r) for r in selected) == Fraction(97, 24)


def test_universal_completion_and_one_site():
    assert safe_transducer()
    assert one_site()


def test_selector_is_a_capacity_witness_on_prefixes():
    mu = mobius_prefix(2048)
    assert abs(selector_score(mu)) <= path_capacity(mu)


def test_result_contract():
    result = verify_certificate()
    assert result["all_pass"]
    assert result["density_constant"] == "97/(24*pi^2)"
    assert result["density_numerator_over_96_pi2"] == 388
    assert result["universal_rows"] == 3240
    assert result["prefix_witness_rows"] == 2048
