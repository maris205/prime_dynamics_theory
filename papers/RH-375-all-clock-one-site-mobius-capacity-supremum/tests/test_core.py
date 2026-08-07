from fractions import Fraction

from all_clock_capacity import (
    bounded_clock_scan,
    clock_pi2_coefficient,
    cofinal_lift_audit,
    density_pi2,
    divisibility_audit,
    exhaustive_factor_optimum,
    exhaustive_subset_optimum,
    verify_certificate,
    weighted_phase_mwis,
)


def test_exact_squarefree_progression_coefficients():
    assert density_pi2(1, 0) == Fraction(6)
    assert density_pi2(3, 0) == Fraction(3, 2)
    assert density_pi2(3, 1) == Fraction(9, 4)
    assert density_pi2(4, 0) == 0
    assert density_pi2(4, 1) == 2
    assert density_pi2(180, 1) == Fraction(5, 96)
    assert density_pi2(180, 5) == Fraction(1, 24)


def test_q1_q2_self_loop_degeneracy():
    assert weighted_phase_mwis(1) == (Fraction(0), ())
    assert weighted_phase_mwis(2) == (Fraction(0), ())


def test_factor_table_exhaustion_first_four_clocks():
    rows = [exhaustive_factor_optimum(q) for q in range(1, 5)]
    assert [row["total_tables"] for row in rows] == [8, 64, 512, 4096]
    assert [row["safe_tables"] for row in rows] == [1, 1, 22, 225]
    assert all(row["pass"] for row in rows)


def test_subset_exhaustion_through_q10():
    rows = [exhaustive_subset_optimum(q) for q in range(1, 11)]
    assert all(row["pass"] for row in rows)
    assert rows[3]["mwis_pi2_F"] == "4"
    assert rows[9]["mwis_pi2_F"] == "5/2"


def test_density_aggregation_and_divisibility_monotonicity():
    rows = [
        divisibility_audit(q, Q)
        for q, Q in ((1, 2), (2, 4), (3, 12), (4, 36), (6, 180), (25, 900))
    ]
    assert all(row["aggregation_pass"] for row in rows)
    assert all(row["lift_safe"] for row in rows)
    assert all(row["monotonicity_pass"] for row in rows)


def test_special_cofinal_lifts_and_high_exponents():
    rows = [cofinal_lift_audit(q) for q in (3, 8, 16, 25, 27, 125, 343)]
    assert all(row["pass"] for row in rows)
    assert rows[-1]["Q"] == 308700
    assert rows[-1]["R"] == 7
    assert rows[-1]["support_mwis_count"] == 132832
    assert rows[-1]["pi2_F_Q"] == "593/144"


def test_square_clock_values_match_rh374_formulas():
    assert clock_pi2_coefficient(1) == 4
    assert clock_pi2_coefficient(2) == Fraction(49, 12)
    assert clock_pi2_coefficient(3) == Fraction(593, 144)
    assert weighted_phase_mwis(36)[0] == 4
    assert weighted_phase_mwis(900)[0] == Fraction(49, 12)


def test_bounded_scan_is_labeled_reproduction_only():
    scan = bounded_clock_scan(256)
    assert scan["label"] == "bounded_reproduction_only_not_all_clock_evidence"
    assert scan["maximum_pi2_F"] == "97/24"
    assert scan["maximizing_clocks"] == [180]
    assert [row["q"] for row in scan["record_rows"]] == [1, 3, 4, 180]


def test_complete_certificate():
    result = verify_certificate()
    assert result["all_pass"]
    assert len(result["factor_exhaustion"]) == 4
    assert len(result["subset_exhaustion"]) == 10
    assert len(result["divisibility_checks"]) == 8
    assert len(result["cofinal_lift_checks"]) == 10
