from fractions import Fraction

import pytest

from near_alias_tail import (
    FIXTURE_LAMBDA,
    LAMBDA_LOWER,
    LAMBDA_UPPER,
    Q,
    R,
    R_H,
    alias_tail_majorant,
    linear_root_diagnostic,
    rate_certificate,
    raw_method_certificate,
    threshold_diagnostics,
)


def test_physical_constants_and_fixture_are_strict():
    assert R_H == Fraction(17, 20)
    assert Q == Fraction(1, 2)
    assert R == Fraction(7, 5)
    assert LAMBDA_LOWER == Fraction(28, 17)
    assert LAMBDA_UPPER == Fraction(17, 10)
    assert LAMBDA_LOWER < FIXTURE_LAMBDA < LAMBDA_UPPER


def test_exact_geometric_scale_identities():
    data = rate_certificate()
    assert data["s"] == Fraction(7, 10)
    assert data["t"] == Fraction(84, 85)
    assert data["x"] == Fraction(2352, 1445)
    assert data["u_squared"] == data["s"] ** 2 / data["x"]
    assert data["v_squared"] == data["t"] ** 2 / data["x"]


def test_exact_root_rate_identities_and_ordering():
    data = rate_certificate()
    assert data["rho_noisy_identity"] is True
    assert data["rho_target_identity"] is True
    assert data["rho_noisy_dominates"] is True
    assert data["rates_subunit"] is True


def test_global_rate_certificates_are_strict():
    data = rate_certificate()
    assert data["rho_noisy"] < data["rho_noisy_upper"] < 1
    assert data["rho_target"] < data["rho_target_upper"] < 1


@pytest.mark.parametrize("depth,parity", [(4, "even"), (5, "odd")])
def test_alias_majorant_covers_both_lower_cut_parities(depth, parity):
    data = alias_tail_majorant(24, depth)
    assert data["N"] == 48 - depth
    assert data["N_parity"] == parity
    assert data["noisy_majorant"] > 0
    assert data["target_majorant"] > 0
    assert data["total_majorant"] == data["noisy_majorant"] + data["target_majorant"]
    assert data["finite_formula_only"] is True


def test_sublinear_fixture_majorant_decays_between_scales():
    first = alias_tail_majorant(32, 5)["total_majorant"]
    second = alias_tail_majorant(64, 8)["total_majorant"]
    third = alias_tail_majorant(128, 11)["total_majorant"]
    assert first > second > third > 0


def test_bounded_phase_is_an_exact_fixed_factor():
    zero = alias_tail_majorant(24, 4, eta=0)
    one = alias_tail_majorant(24, 4, eta=1)
    assert one["noisy_majorant"] == zero["noisy_majorant"] / FIXTURE_LAMBDA**2
    assert one["target_majorant"] == zero["target_majorant"]


def test_linear_root_diagnostics_match_zero_depth_rates():
    rates = rate_certificate()
    for normalization in ("natural_bottom", "alias_clock"):
        row = linear_root_diagnostic(0, normalization)
        assert row["noisy_root"] == pytest.approx(float(rates["rho_noisy"]))
        assert row["target_root"] == pytest.approx(float(rates["rho_target"]))
        assert row["finite_formula_only"] is True


def test_alias_root_crosses_one_between_two_rational_depths():
    below = linear_root_diagnostic(Fraction(2, 5), "alias_clock")
    above = linear_root_diagnostic(Fraction(3, 5), "alias_clock")
    assert below["root_ceiling"] < 1
    assert above["root_ceiling"] > 1


def test_natural_root_crosses_one_before_alias_root():
    natural = linear_root_diagnostic(Fraction(3, 10), "natural_bottom")
    alias = linear_root_diagnostic(Fraction(3, 10), "alias_clock")
    assert natural["root_ceiling"] > 1
    assert alias["root_ceiling"] < 1


def test_physical_threshold_diagnostics_are_in_declared_windows():
    data = threshold_diagnostics()
    assert 0.263 < data["alpha_natural"] < 0.265
    assert 0.441 < data["alpha_alias"] < 0.443
    assert data["alpha_natural"] < data["alpha_alias"] < 2


def test_raw_method_certificate_is_strictly_superunit():
    data = raw_method_certificate()
    assert data["strict_global_lower"] == Fraction(9604, 7225)
    assert data["global_lower_is_superunit"] is True
    assert data["fixture_is_superunit"] is True
    assert data["method_boundary_only"] is True


@pytest.mark.parametrize("bad_lambda", [LAMBDA_LOWER, LAMBDA_UPPER, 1, 2])
def test_lambda_domain_fails_closed(bad_lambda):
    with pytest.raises(ValueError):
        rate_certificate(bad_lambda)
    with pytest.raises(ValueError):
        alias_tail_majorant(8, 1, lambda_value=bad_lambda)


@pytest.mark.parametrize("bad", [True, 2.0, "2"])
def test_integer_fields_reject_non_exact_types(bad):
    with pytest.raises(TypeError):
        alias_tail_majorant(bad, 1)
    with pytest.raises(TypeError):
        alias_tail_majorant(8, bad)


@pytest.mark.parametrize("k,depth", [(1, 0), (8, -1), (8, 15)])
def test_depth_domain_fails_closed(k, depth):
    with pytest.raises(ValueError):
        alias_tail_majorant(k, depth)


def test_invalid_normalization_fails_closed():
    with pytest.raises(ValueError):
        linear_root_diagnostic(0, "local")


def test_invalid_depth_ratio_fails_closed():
    with pytest.raises(ValueError):
        linear_root_diagnostic(Fraction(-1, 10), "alias_clock")
    with pytest.raises(ValueError):
        linear_root_diagnostic(Fraction(21, 10), "alias_clock")


def test_boolean_lambda_is_not_integer_coerced():
    with pytest.raises(TypeError):
        rate_certificate(True)
    with pytest.raises(TypeError):
        threshold_diagnostics(True)
