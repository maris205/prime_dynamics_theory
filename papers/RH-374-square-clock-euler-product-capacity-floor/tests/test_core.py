from decimal import Decimal

from square_clock import (
    clock_row,
    euler_limit_diagnostic,
    first_odd_primes,
    formula_odd_run_count,
    phase_selector,
    recurrence_audit,
    verify_certificate,
)
from square_clock.core import (
    brute_phase_mwis_count,
    direct_run_counts,
    exact_run_counts_formula,
    universal_selector_audit,
)


def test_exact_rows_and_rh373_improvement():
    assert first_odd_primes(4) == (3, 5, 7, 11)
    assert clock_row(1) == {
        "y": 1, "largest_prime": 3, "P": 9, "q": 36,
        "A": 8, "O": 0, "L_even": 8,
        "selected_phase_count": 16, "pi2_times_B": "4",
    }
    assert clock_row(2)["pi2_times_B"] == "49/12"
    assert clock_row(3)["pi2_times_B"] == "593/144"
    assert clock_row(4) == {
        "y": 4, "largest_prime": 11, "P": 1334025, "q": 5336100,
        "A": 1105920, "O": 72440, "L_even": 838240,
        "selected_phase_count": 2284280,
        "pi2_times_B": "57107/13824",
    }


def test_run_formula_and_brute_mwis_for_first_three_clocks():
    for y in range(1, 4):
        assert direct_run_counts(y) == exact_run_counts_formula(y)
        assert max(length for length, count in direct_run_counts(y).items() if count) == 8
        assert formula_odd_run_count(y) == clock_row(y)["O"]
        assert brute_phase_mwis_count(y) == clock_row(y)["selected_phase_count"]


def test_recurrence_and_strictness():
    first = recurrence_audit(1)
    second = recurrence_audit(2)
    third = recurrence_audit(3)
    assert first["pass"] and first["L_even"] == 8
    assert second["pass"] and second["L_even"] == 160
    assert third["pass"] and third["L_even"] == 7160
    assert (
        first["exact_length_8_run"]
        and second["exact_length_8_run"]
        and third["exact_length_8_run"]
    )


def test_q900_selector_is_universally_safe():
    selected = phase_selector(2)
    assert len(selected) == 392
    assert not any((residue + 2) % 900 in selected for residue in selected)
    rows, passed = universal_selector_audit(2)
    assert rows == 8100
    assert passed


def test_direct_words_fail_closed_beyond_audited_range():
    from square_clock.core import positive_word

    try:
        positive_word(4)
    except ValueError as exc:
        assert "capped at y<=3" in str(exc)
    else:
        raise AssertionError("uncapped y=4 direct word generation")


def test_euler_diagnostic_is_conservative_and_contains_formal_crosscheck():
    diagnostic = euler_limit_diagnostic()
    coefficient = diagnostic["pi2_times_B_infinity_interval"]
    capacity = diagnostic["B_infinity_interval"]
    assert Decimal(coefficient["lower"]) < Decimal("4.16424714477670776087")
    assert Decimal(coefficient["upper"]) > Decimal("4.16424718319573851184")
    assert Decimal(capacity["lower"]) < Decimal("0.42192644968800153189")
    assert Decimal(capacity["upper"]) > Decimal("0.42192645358066320197")
    assert diagnostic["status"] == "diagnostic_only_not_theorem_evidence"


def test_complete_certificate():
    result = verify_certificate()
    assert result["all_pass"]
    assert result["q900_selector"]["even_phase_count"] == 192
    assert result["q900_selector"]["odd_phase_count"] == 200
    assert result["q900_selector"]["inactive_selected_phases"] == []
    assert result["q900_vs_rh373"]["difference"] == "1/24"
    assert result["finite_diagnostic"]["prefix_witness_rows"] == 2048
