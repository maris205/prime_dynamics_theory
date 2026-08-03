from decimal import Decimal
from fractions import Fraction

import pytest

from post_alias_crossover import (
    FIXTURE_LAMBDA,
    LAMBDA_LOWER,
    LAMBDA_UPPER,
    R,
    R_H,
    exact_alias_budget,
    exact_constants,
    exact_post_budget,
    exact_ratio_certificate,
    phase_diagnostic,
)


def test_exact_physical_constants_are_strict():
    data = exact_constants()
    assert R_H == Fraction(17, 20)
    assert R == Fraction(7, 5)
    assert LAMBDA_LOWER < FIXTURE_LAMBDA < LAMBDA_UPPER
    assert data["x"] == Fraction(2352, 1445)
    assert data["x_identity"] is True
    assert data["x_is_superunit"] is True


@pytest.mark.parametrize("k,L", [(4, 1), (8, 3), (16, 5), (32, 9)])
def test_exact_alias_post_and_ratio_identities(k, L):
    row = exact_ratio_certificate(k, L)
    assert row["alias_budget"] == exact_alias_budget(k)
    assert row["post_budget"] == exact_post_budget(k, L)
    assert row["ratio"] == row["post_budget"] / row["alias_budget"]
    assert row["ratio_identity"] is True
    assert row["ratio_over_proxy"] > 0
    assert row["finite_formula_only"] is True


def test_uniform_proxy_improves_on_sublinear_depths():
    rows = [
        exact_ratio_certificate(64, 6),
        exact_ratio_certificate(256, 12),
        exact_ratio_certificate(1024, 24),
    ]
    errors = [abs(float(row["ratio_over_proxy"]) - 1.0) for row in rows]
    assert errors[0] > errors[1] > errors[2]


def test_fixed_depth_keeps_geometric_correction():
    row = exact_ratio_certificate(512, 1)
    x_value = exact_constants()["x"]
    assert row["uniform_proxy"] == x_value / 512
    assert abs(float(row["ratio_over_proxy"]) - 1.0) < 0.01


def test_fixed_depth_rejects_the_growing_depth_simplification():
    k = 4096
    row = exact_ratio_certificate(k, 1)
    x_value = exact_constants()["x"]
    growing_proxy = x_value**2 / (k * (x_value - 1))
    observed = row["ratio"] / growing_proxy
    limiting_mismatch = (x_value - 1) / x_value
    assert abs(float(observed - limiting_mismatch)) < 0.001


def test_floor_phase_rows_stay_inside_the_cluster_interval():
    for k in (128, 256, 512, 1024):
        row = phase_diagnostic(k, "0")
        assert 1 <= row["L"] <= k - 1
        assert Decimal("0") <= Decimal(row["integer_phase"]) < Decimal("1")
        assert row["phase_law_inside_closed_cluster"] is True
        assert row["finite_formula_only"] is True
        assert row["synthetic_multiplier_law"] is True
        assert "ratio_inside_cluster_bounds" not in row


def test_floor_phase_law_ratio_tends_toward_one():
    rows = [phase_diagnostic(k, "0") for k in (128, 512, 2048)]
    errors = [abs(float(row["ratio_over_phase_law"]) - 1.0) for row in rows]
    assert errors[0] > errors[1] > errors[2]


@pytest.mark.parametrize("bad", [True, 2.0, "2"])
def test_integer_fields_reject_non_exact_types(bad):
    with pytest.raises(TypeError):
        exact_alias_budget(bad)
    with pytest.raises(TypeError):
        exact_post_budget(8, bad)


@pytest.mark.parametrize("k,L", [(1, 1), (8, 0), (8, 8), (8, -1)])
def test_domain_failures_are_closed(k, L):
    with pytest.raises(ValueError):
        exact_post_budget(k, L)


@pytest.mark.parametrize("bad_lambda", [LAMBDA_LOWER, LAMBDA_UPPER, 1, 2, True])
def test_lambda_domain_fails_closed(bad_lambda):
    with pytest.raises((TypeError, ValueError)):
        exact_constants(bad_lambda)


def test_phase_decimal_inputs_are_strict():
    with pytest.raises(TypeError):
        phase_diagnostic(64, 0)
    with pytest.raises(ValueError):
        phase_diagnostic(3, "-100")
