from fractions import Fraction

import pytest

from finite_clock_gap import (
    deletion_ledger,
    lcm_gap_row,
    run_statistics,
    same_support_saturation,
    square_run_counts,
    square_transition,
    verify_certificate,
)
from finite_clock_gap.core import (
    EulerValue,
    _exact_integer,
    phasewise_optimum,
    square_parameters,
    value_compare,
)


def test_locked_square_run_rows() -> None:
    expected_runs = (
        {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 1},
        {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 17},
        {1: 154, 2: 148, 3: 142, 4: 136, 5: 130, 6: 124, 7: 118, 8: 697},
    )
    expected_parameters = ((8, 7), (192, 161), (9216, 7567))
    expected_statistics = (
        {"E": 1, "L": 8, "M": 0, "X": 6},
        {"E": 23, "L": 160, "M": 24, "X": 114},
        {"E": 1105, "L": 7160, "M": 1512, "X": 4950},
    )
    for y in (1, 2, 3):
        assert square_run_counts(y) == expected_runs[y - 1]
        parameters = square_parameters(y)
        assert (parameters["A"], parameters["D"]) == expected_parameters[y - 1]
        statistics = run_statistics(y)
        for key, value in expected_statistics[y - 1].items():
            assert statistics[key] == value


def test_deletion_ledger_checks_both_parity_fixtures() -> None:
    rows = deletion_ledger()
    assert len(rows) == 8
    assert all(row["all_pass"] for row in rows)
    assert all(row["expected_formula"] == "s-2" for row in rows if row["parity"] == "even")
    assert all(row["expected_formula"] == "ell-1" for row in rows if row["parity"] == "odd")


def test_even_run_recurrence_and_increment_fixtures() -> None:
    rows = [square_transition(y) for y in (1, 2, 3)]
    assert rows[0]["mathcal_E_next"] == rows[0]["mathcal_E_recurrence_rhs"] == 23
    assert rows[1]["mathcal_E_next"] == rows[1]["mathcal_E_recurrence_rhs"] == 1105
    expected = (
        EulerValue(Fraction(1, 16), 0).exact_dict(),
        EulerValue(Fraction(9, 256), Fraction(-24, 7567)).exact_dict(),
        EulerValue(Fraction(443, 30720), Fraction(-216, 128639)).exact_dict(),
    )
    assert tuple(row["increment_direct"] for row in rows) == expected
    assert all(row["increment_identity_pass"] and row["X_at_least_6_pass"] for row in rows)


def test_same_support_saturation_has_independent_certificates() -> None:
    expected = {
        72: {"inv_pi2": "9/2", "kappa2": "-1/7"},
        108: {"inv_pi2": "9/2", "kappa2": "-1/7"},
        144: {"inv_pi2": "9/2", "kappa2": "-1/7"},
        216: {"inv_pi2": "9/2", "kappa2": "-1/7"},
        288: {"inv_pi2": "9/2", "kappa2": "-1/7"},
        324: {"inv_pi2": "9/2", "kappa2": "-1/7"},
        1800: {"inv_pi2": "73/16", "kappa2": "-1/7"},
        2700: {"inv_pi2": "73/16", "kappa2": "-1/7"},
        4500: {"inv_pi2": "73/16", "kappa2": "-1/7"},
    }
    rows = [
        *(same_support_saturation(1, multiplier) for multiplier in (2, 3, 4, 6, 8, 9)),
        *(same_support_saturation(2, multiplier) for multiplier in (2, 3, 5)),
    ]
    assert {row["Q"]: row["G_Q"] for row in rows} == expected
    assert all(row["density_scaling_pass"] for row in rows)
    assert all(row["run_replication_pass"] for row in rows)
    assert all(row["direct_dp_pass"] for row in rows)
    assert all(row["fine_separator_certificate"]["all_pass"] for row in rows)


def test_new_prime_multiplier_is_rejected_and_changes_G() -> None:
    with pytest.raises(ValueError, match="identical prime support"):
        same_support_saturation(1, 5)
    value, _ = phasewise_optimum(180)
    assert value.exact_dict() == {"inv_pi2": "73/16", "kappa2": "-25/161"}
    assert value.exact_dict() != {"inv_pi2": "9/2", "kappa2": "-1/7"}


def test_lcm_gap_denominator_and_exponent_scope() -> None:
    row = lcm_gap_row(44100, 3)
    parameters = square_parameters(3)
    next_prime = square_parameters(4)["primes"][-1]
    expected = Fraction(12, parameters["A"] * (next_prime * next_prime - 1))
    assert row["gap_lower_inv_pi2"] == str(expected)
    assert row["Q"] % 44100 == 0 and row["same_support_as_q_y"]
    assert lcm_gap_row(2**11 * 3**7 * 5, 2)["all_pass"]


def test_fraction_count_conversion_fails_closed() -> None:
    assert _exact_integer(Fraction(7), "fixture") == 7
    with pytest.raises(ArithmeticError, match="not integral"):
        _exact_integer(Fraction(7, 2), "fixture")


def test_euler_comparison_fails_closed_inside_interval() -> None:
    with pytest.raises(ArithmeticError, match="unresolved"):
        value_compare(EulerValue(Fraction(-637, 200), 1), EulerValue())


def test_full_core_certificate() -> None:
    certificate = verify_certificate()
    assert certificate["all_pass"]
    assert certificate["claim_boundary"]["gates_A_through_E"] == [False] * 5
