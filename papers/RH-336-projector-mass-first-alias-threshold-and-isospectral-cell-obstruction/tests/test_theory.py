from fractions import Fraction

import pytest

from projector_mass import (
    E_MINUS_BASE,
    K_BASE,
    SUFFICIENT_LOWER,
    SUFFICIENT_UPPER,
    audited_family_formula,
    audited_projector_formula,
    corrected_cell_drift,
    corrected_cell_formula,
    corrected_cells,
    exponent_separation_certificate,
    family_audit,
    identity,
    in_sufficient_positivity_interval,
    lambda_polynomial,
    matrix_multiply,
    matrix_power,
    matrix_scale,
    matrix_trace,
    positivity_factor_ledger,
    power_trace_formula,
    projector_family,
    projector_mass_drift,
    projector_mass_formula,
    projector_masses,
    shear,
    shear_inverse,
    similarity_family,
    strictly_positive,
    vector_sum,
)


F = Fraction


def test_exact_exponent_separation_certificate_uses_only_rational_signs():
    certificate = exponent_separation_certificate()
    assert lambda_polynomial(F(17, 10)) == F(473, 1000)
    assert certificate["lambda_upper_bound"] == F(17, 10)
    assert certificate["polynomial_at_upper"] == F(473, 1000)
    assert certificate["R_squared_over_r_H"] == F(196, 85)
    assert certificate["squared_comparison_gap"] == F(116783, 289000)
    assert certificate["squared_comparison_gap"] > 0
    assert certificate["conclusion"] == "kappa_proj>gamma_star_RH325"


def test_shear_inverse_and_constant_vector_are_exact():
    for t in (F(-1, 100), F(0), F(1, 100), F(2, 5)):
        assert matrix_multiply(shear_inverse(t), shear(t)) == identity(3)
        assert tuple(vector_sum(row) for row in shear(t)) == (F(1), F(1), F(1))
    with pytest.raises(ValueError):
        shear_inverse(F(1))


def test_displayed_K_t_formula_matches_similarity_exactly():
    for t in (F(-1, 100), F(0), F(1, 100), F(1, 3), F(7, 10)):
        assert similarity_family(t) == audited_family_formula(t)


def test_convenient_interval_is_sufficient_for_strict_positive_markov_rows():
    for t in (F(-1, 100), F(0), F(1, 100), F(1, 3), F(49, 100)):
        assert SUFFICIENT_LOWER < t < SUFFICIENT_UPPER
        assert in_sufficient_positivity_interval(t) is True
        assert strictly_positive(t) is True
        assert tuple(vector_sum(row) for row in similarity_family(t)) == (
            F(1),
            F(1),
            F(1),
        )


def test_sufficient_interval_is_not_promoted_to_maximal():
    t = F(3, 5)
    assert t > SUFFICIENT_UPPER
    assert in_sufficient_positivity_interval(t) is False
    assert strictly_positive(t) is True
    assert strictly_positive(SUFFICIENT_LOWER) is False


def test_positivity_factor_ledger_locks_the_lower_endpoint():
    factors = positivity_factor_ledger(SUFFICIENT_LOWER)
    assert factors["row3_col2_numerator"] == 0
    for key, value in factors.items():
        if key != "row3_col2_numerator":
            assert value > 0


def test_isospectral_all_power_traces_are_exact_for_many_orders():
    for t in (F(-1, 100), F(0), F(1, 100), F(2, 5)):
        k_t = similarity_family(t)
        for exponent in range(1, 16):
            assert matrix_trace(matrix_power(k_t, exponent)) == power_trace_formula(
                exponent
            )
    with pytest.raises(ValueError):
        power_trace_formula(0)


def test_projector_similarity_formula_and_intertwining_are_exact():
    for t in (F(-1, 100), F(0), F(1, 100), F(2, 5)):
        k_t = similarity_family(t)
        e_t = projector_family(t)
        assert e_t == audited_projector_formula(t)
        assert matrix_multiply(e_t, e_t) == e_t
        assert matrix_multiply(k_t, e_t) == matrix_scale(-F(2, 5), e_t)
        assert matrix_multiply(e_t, k_t) == matrix_scale(-F(2, 5), e_t)
        assert matrix_trace(e_t) == 1


def test_projector_mass_formula_and_zero_sum_drift_are_exact():
    for t in (F(-1, 100), F(0), F(1, 100), F(2, 5)):
        masses = projector_masses(t)
        assert masses == projector_mass_formula(t)
        assert tuple(masses[i] - projector_masses(F(0))[i] for i in range(3)) == (
            projector_mass_drift(t)
        )
        assert vector_sum(masses) == 1
        assert vector_sum(projector_mass_drift(t)) == 0


def test_corrected_cell_formula_total_and_drift_are_exact():
    for t in (F(-1, 100), F(0), F(1, 100), F(2, 5)):
        cells = corrected_cells(t)
        assert cells == corrected_cell_formula(t)
        assert vector_sum(cells) == F(48, 17)
        assert tuple(cells[i] - corrected_cells(F(0))[i] for i in range(3)) == (
            corrected_cell_drift(t)
        )
        assert vector_sum(corrected_cell_drift(t)) == 0


def test_one_percent_fixture_has_the_required_exact_cell_drift():
    t = F(1, 100)
    assert corrected_cell_drift(t) == (
        -F(288, 24565),
        F(288, 24565),
        F(0),
    )
    assert corrected_cells(t) == (
        F(33712, 24565),
        F(2288, 24565),
        F(6672, 4913),
    )


def test_audit_is_exact_and_fixed_order_only():
    audit = family_audit(F(1, 100), max_power=12)
    assert audit["K_t"] == audit["K_formula"]
    assert audit["E_minus_t"] == audit["E_minus_formula"]
    assert audit["projector_masses"] == audit["projector_mass_formula"]
    assert audit["corrected_cells"] == audit["corrected_cell_formula"]
    assert audit["corrected_drift"] == audit["corrected_drift_formula"]
    assert all(row["direct_trace"] == row["spectral_trace"] for row in audit["power_rows"])
    assert len(audit["power_rows"]) == 12
