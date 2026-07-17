from __future__ import annotations

import numpy as np

from iterated_grid import propagate_resolvent_bound


def test_block_inverse_propagation_bounds_dense_inverse() -> None:
    rng = np.random.default_rng(3779)
    dimension = 4
    coarse = rng.normal(size=(dimension, dimension)) / 13.0
    error = rng.normal(size=(dimension, dimension)) / 900.0
    coarse_to_detail = rng.normal(size=(dimension, dimension)) / 120.0
    detail_to_coarse = rng.normal(size=(dimension, dimension)) / 110.0
    detail = rng.normal(size=(dimension, dimension)) / 700.0
    zeta = -0.41 - 0.68j
    coarse_inverse = np.linalg.inv(zeta * np.eye(dimension) - coarse)
    detail_inverse = np.linalg.inv(zeta * np.eye(dimension) - detail)
    coarse_upper = np.linalg.norm(coarse_inverse, 2) * (1.0 + 1.0e-13)
    detail_upper = np.linalg.norm(detail_inverse, 2) * (1.0 + 1.0e-13)
    epsilon = (
        np.linalg.norm(error, 2)
        + np.linalg.norm(detail_to_coarse, 2)
        * detail_upper
        * np.linalg.norm(coarse_to_detail, 2)
    ) * (1.0 + 1.0e-13)
    bound = propagate_resolvent_bound(
        coarse_upper,
        first_effective_perturbation_upper=epsilon,
        first_detail_resolvent_upper=detail_upper,
        first_coarse_to_detail_upper=np.linalg.norm(coarse_to_detail, 2)
        * (1.0 + 1.0e-13),
        first_detail_to_coarse_upper=np.linalg.norm(detail_to_coarse, 2)
        * (1.0 + 1.0e-13),
        second_effective_perturbation_upper=1.0e-3,
    )
    block = np.block(
        [
            [coarse + error, detail_to_coarse],
            [coarse_to_detail, detail],
        ]
    )
    exact = np.linalg.norm(
        np.linalg.inv(zeta * np.eye(2 * dimension) - block), 2
    )
    assert bound.first_gate_closed
    assert bound.fine_resolvent_upper >= exact
    assert bound.second_gate_closed
    assert bound.second_continuation_product_upper == np.nextafter(
        bound.fine_resolvent_upper * 1.0e-3, np.inf
    )


def test_failed_first_gate_returns_infinite_bound() -> None:
    bound = propagate_resolvent_bound(
        4.0,
        first_effective_perturbation_upper=0.25,
        first_detail_resolvent_upper=2.0,
        first_coarse_to_detail_upper=0.1,
        first_detail_to_coarse_upper=0.2,
        second_effective_perturbation_upper=0.01,
    )
    assert not bound.first_gate_closed
    assert np.isinf(bound.first_effective_resolvent_upper)
    assert np.isinf(bound.fine_resolvent_upper)
    assert not bound.second_gate_closed
