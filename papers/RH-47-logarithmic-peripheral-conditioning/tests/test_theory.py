from __future__ import annotations

import math

import numpy as np

from peripheral_conditioning import (
    anchored_bulk_ledger,
    contour_resolvent_lower,
    dyadic_lift_factors,
    endpoint_log_coefficient,
    endpoint_tail_constant,
    logarithmic_clock,
    low_rank_difference_frobenius,
    low_rank_frobenius,
    low_rank_singular_values,
    power_schedule_closes,
)


def test_endpoint_constants_are_consistent() -> None:
    constant = endpoint_tail_constant()
    assert 0.22 < constant < 0.23
    assert math.isclose(endpoint_log_coefficient(), constant * constant)


def test_logarithmic_clock() -> None:
    assert logarithmic_clock(1.0e-4) == math.sqrt(math.log(1.0e4))


def test_contour_lower_bound() -> None:
    assert contour_resolvent_lower(2.0, 0.05) == 40.0


def test_low_rank_norms_match_dense_matrix() -> None:
    left = np.asarray([[1.0, 0.2], [0.3, -0.4], [0.1, 0.7]])
    right = np.asarray([[0.5, -0.2], [0.1, 0.8], [-0.4, 0.6]])
    dense = left @ right.T
    assert math.isclose(low_rank_frobenius(left, right), np.linalg.norm(dense))
    assert np.allclose(
        low_rank_singular_values(left, right),
        np.linalg.svd(dense, compute_uv=False)[:2],
    )


def test_dyadic_lift_and_difference() -> None:
    left = np.asarray([1.0, -1.0])
    right = np.asarray([0.3, -0.2])
    lifted_left, lifted_right = dyadic_lift_factors(left, right)
    dense = lifted_left @ lifted_right.T
    expected = np.repeat(left, 2)[:, None] @ np.repeat(
        right / 2.0, 2
    )[None, :]
    assert np.allclose(dense, expected)
    assert low_rank_difference_frobenius(
        lifted_left, lifted_right, lifted_left, lifted_right
    ) < 1.0e-14


def test_anchored_bulk_power_thresholds() -> None:
    ledger = anchored_bulk_ledger(1.0e-3, 10_000_000)
    assert ledger.peripheral_hilbert_schmidt_upper < (
        ledger.markov_hilbert_schmidt_upper
    )
    assert not power_schedule_closes(2.0)["square_trace_norm_converges"]
    assert power_schedule_closes(2.25)["square_trace_norm_converges"]
