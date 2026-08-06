from __future__ import annotations

from fractions import Fraction

from branch_markov import finite_checks, mobius_prefix, parameter_checks, variance_formula


def test_parameter_identities() -> None:
    for t in (Fraction(1, 2), Fraction(2, 3), Fraction(3, 4)):
        row = parameter_checks(t)
        assert row["pass"] is True
        assert row["p4_positive"] is True
        assert row["odd_covariance_residual"] == "0"


def test_exact_variance_formula() -> None:
    values = mobius_prefix(14)
    for t in (Fraction(1, 2), Fraction(2, 3), Fraction(3, 4)):
        value = variance_formula(values, t)
        assert value >= 0
        assert value <= (Fraction(2 - t, t) * len(values))


def test_finite_audit() -> None:
    checks = finite_checks()
    assert checks["all_pass"] is True
    assert len(checks["parameter_rows"]) == 3
    assert len(checks["variance_rows"]) == 14 * 3
