import math

from parity_alias_packet import (
    CLEARANCE_CONSTANT,
    COUNTERLOOP_BETA_LIMIT,
    C_STAR,
    HARDY_RADIUS,
    LAMBDA,
    MULTIPLIER_CONSTANT,
    SCALAR_BALANCE_CLEARANCE,
    SCALAR_BALANCE_PHASE,
    alias_impulse,
    asymptotic_beta_k,
    clearance_ratio_from_phase,
    counterloop_defect,
    counterloop_moment,
    first_alias_identity,
    hardy_bulk_difference,
    limiting_pole_moment,
    natural_phase,
    packet_row,
    parity_linear_term,
    parity_packet,
    parity_remainder_bound,
    phase_row,
    radial_counterloop_correction,
    scalar_balance_ratio,
    sigma_from_phase,
    sign_rows,
)


def test_counterloop_defect_has_exact_radial_plus_alias_decomposition():
    for k in range(2, 9):
        beta_k = asymptotic_beta_k(k)
        for order in range(1, 4 * k + 1):
            direct = counterloop_moment(k, order, beta_k) - limiting_pole_moment(
                order
            )
            split = radial_counterloop_correction(
                k, order, beta_k
            ) + alias_impulse(k, order, beta_k)
            assert math.isclose(direct, split, rel_tol=2e-14, abs_tol=2e-14)
            assert math.isclose(
                counterloop_defect(k, order, beta_k),
                split,
                rel_tol=2e-14,
                abs_tol=2e-14,
            )


def test_first_alias_counterloop_formula_is_exact():
    for k in (2, 5, 11, 23):
        beta_k = asymptotic_beta_k(k)
        expected = (
            (2 * k - 2) * beta_k ** (2 * k)
            + 2 * COUNTERLOOP_BETA_LIMIT ** (2 * k)
        )
        assert math.isclose(
            counterloop_defect(k, 2 * k, beta_k),
            expected,
            rel_tol=2e-14,
        )


def test_parity_packet_has_exact_sign_and_uniform_quadratic_remainder():
    for order in range(2, 25):
        for delta in (1e-5, 1e-3, 0.02, 0.2):
            packet = parity_packet(order, delta)
            leading = parity_linear_term(order, delta)
            assert (packet > 0.0) == (order % 2 == 0)
            assert abs(packet - leading) <= parity_remainder_bound(
                order, delta
            ) * (1.0 + 1e-12) + 2e-15


def test_hardy_bulk_and_first_alias_residual_keep_the_actual_signs():
    k = 7
    order = 2 * k
    raw = -0.004
    delta = 0.03
    beta_k = asymptotic_beta_k(k)
    identity = first_alias_identity(raw, k, delta, beta_k)
    bulk = hardy_bulk_difference(raw, order, delta)
    assert identity["parity_packet"] > 0.0
    assert identity["counterloop_defect"] > 0.0
    assert math.isclose(
        bulk,
        identity["raw_hardy_packet"] + identity["parity_packet"],
        rel_tol=1e-15,
    )
    assert math.isclose(
        identity["residual"],
        bulk - identity["counterloop_defect"],
        rel_tol=1e-15,
    )


def test_clock_phase_and_clearance_dictionary_is_exact():
    for k, phase in ((8, -0.75), (12, 0.0), (20, 0.9)):
        sigma = sigma_from_phase(k, phase)
        assert math.isclose(natural_phase(sigma, k), phase, abs_tol=2e-14)
        assert math.isclose(
            clearance_ratio_from_phase(phase),
            CLEARANCE_CONSTANT * LAMBDA ** (-2.0 * phase),
            rel_tol=1e-15,
        )
    row = phase_row(0.5)
    assert row["retained_coordinates"] == ["V", "U", "W"]
    assert row["orientation"] == ["positive", "negative", "positive"]


def test_unique_scalar_balance_phase_and_canonical_phase_obstruction():
    assert math.isclose(scalar_balance_ratio(SCALAR_BALANCE_PHASE), 1.0)
    assert math.isclose(
        SCALAR_BALANCE_CLEARANCE,
        CLEARANCE_CONSTANT * (C_STAR * MULTIPLIER_CONSTANT) ** 2,
        rel_tol=1e-15,
    )
    assert 3.06 < SCALAR_BALANCE_PHASE < 3.07
    assert scalar_balance_ratio(1.0) < 0.344
    assert scalar_balance_ratio(-1.0) > 0.122
    assert clearance_ratio_from_phase(1.0) > SCALAR_BALANCE_CLEARANCE


def test_packet_rows_converge_to_the_phase_ratio_but_not_to_target_scale():
    rows = [packet_row(k, 0.0) for k in (8, 16, 32, 64)]
    target_ratio = scalar_balance_ratio(0.0)
    assert abs(rows[-1]["parity_to_alias_ratio"] - target_ratio) < abs(
        rows[0]["parity_to_alias_ratio"] - target_ratio
    )
    assert rows[-1]["absolute_residual_to_target"] > rows[0][
        "absolute_residual_to_target"
    ]
    assert math.isclose(
        COUNTERLOOP_BETA_LIMIT,
        1.0 / (HARDY_RADIUS * math.sqrt(LAMBDA)),
        rel_tol=1e-15,
    )


def test_sign_rows_record_odd_zero_defect_and_even_alias_impulses():
    rows = {row["label"]: row for row in sign_rows(6, 0.02, asymptotic_beta_k(6))}
    assert rows["odd_pre_alias"]["parity_packet"] < 0.0
    assert rows["odd_pre_alias"]["counterloop_defect"] == 0.0
    assert rows["first_alias"]["parity_packet"] > 0.0
    assert rows["first_alias"]["alias_impulse"] > 0.0
    assert rows["second_alias"]["alias_impulse"] > 0.0
