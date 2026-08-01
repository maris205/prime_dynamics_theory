from decimal import Decimal, localcontext
from fractions import Fraction

import pytest

from critical_orbit_atom import (
    boundary_orbit,
    boundary_point,
    complete_orbit_row,
    ledger_fixture,
    physical_constants,
)


def test_physical_constants_have_source_locked_ordering():
    constants = physical_constants()
    assert Decimal(1) < constants["u_c"] < Decimal(2)
    assert Decimal(1) < constants["lambda"] < Decimal(2)
    assert constants["r"] < constants["b"] < Decimal(1)
    assert constants["beta"] * Decimal("1.4") > 1


def test_complete_folded_orbit_has_exact_marked_count_and_closes():
    for k in (2, 4, 8, 16, 32):
        row = complete_orbit_row(k)
        assert row["complete_count"] == 2 * k
        assert row["distinct_folded_count"] == 2 * k
        assert row["orbit_closure_error"] < Decimal("1e-70")


def test_eventual_cell_counts_have_only_left_or_far_critical_point():
    for k in (4, 8, 16, 32):
        row = complete_orbit_row(k)
        assert row["left_count"] == row["epsilon"]
        assert row["right_count"] == 0
        assert row["far_count"] == 2 * k - row["epsilon"]
        assert row["cell_count_identity"] == 2 * k


def test_epsilon_is_exactly_the_inclusive_q_b_threshold():
    for k in (2, 4, 8, 16):
        row = complete_orbit_row(k)
        assert row["epsilon"] == int(row["critical_q_b"] <= row["window_A"])


def test_full_atom_and_missing_point_identities_are_exact():
    with localcontext() as context:
        context.prec = 100
        for k in (2, 4, 8, 16, 32):
            row = complete_orbit_row(k)
            assert row["full_atom"] == Decimal(2 * k) * row["point_weight"]
            assert row["far_atom"] == Decimal(2 * k - 1) * row["point_weight"]
            assert abs(
                row["full_atom"] - row["far_atom"] - row["point_weight"]
            ) < Decimal("1e-95")
            assert abs(
                row["full_over_far"] - Decimal(2 * k) / Decimal(2 * k - 1)
            ) < Decimal("1e-95")


def test_missing_point_is_super_target_in_finite_diagnostics():
    rows = [complete_orbit_row(k) for k in (4, 8, 16, 32)]
    assert rows[-1]["point_over_target"] > rows[0]["point_over_target"]
    assert rows[-1]["point_over_target"] > Decimal(1000)


def test_complete_atom_approaches_alias_and_double_packet_scale():
    rows = [complete_orbit_row(k) for k in (4, 8, 16, 32)]
    full_errors = [abs(row["full_over_alias"] - 1) for row in rows]
    double_errors = [abs(row["sum_over_alias"] - 2) for row in rows]
    assert full_errors[-1] < full_errors[0]
    assert double_errors[-1] < double_errors[0]
    assert rows[-1]["full_over_target"] > Decimal(1000000)


def test_phase_fixture_changes_only_the_left_far_allocation():
    rows = [complete_orbit_row(16, phase_eta=eta) for eta in (-1, 0, 1)]
    for row in rows:
        assert row["right_count"] == 0
        assert row["left_count"] + row["far_count"] == 32


def test_rational_typed_ledger_is_exact():
    fixture = ledger_fixture(
        raw_rest=Fraction(31, 7),
        parity=Fraction(13, 5),
        alias=Fraction(17, 6),
        full_atom=Fraction(19, 8),
        head_defect=Fraction(23, 11),
    )
    assert fixture["raw_identity_residual"] == 0
    assert fixture["direct_identity_residual"] == 0
    assert fixture["p"] == fixture["compensation_residual"]


def test_invalid_domains_fail_closed():
    with pytest.raises(ValueError):
        physical_constants(40)
    with pytest.raises(ValueError):
        boundary_point(0)
    with pytest.raises(ValueError):
        boundary_orbit(1)
    with pytest.raises(ValueError):
        complete_orbit_row(1)
    with pytest.raises(ValueError):
        complete_orbit_row(2, window_A=0)
    with pytest.raises(TypeError):
        complete_orbit_row(2, phase_eta=0.5)
