from __future__ import annotations

import math

import numpy as np
import pytest

from block_schur_budget import (
    block_budget_product,
    block_endpoint_tail_bound,
    block_geometric_mean,
    blocks_for_tolerance,
    coercive_defect,
    coercive_secular_surplus,
    relative_snapshot_bound,
    schur_trial_form,
)


def test_block_product_and_mean() -> None:
    factors = (0.75, 0.14, 0.12, 0.23)
    assert block_budget_product(factors) >= math.prod(factors)
    assert block_geometric_mean(factors) >= math.prod(factors) ** 0.25
    with pytest.raises(ValueError):
        block_budget_product(())


def test_block_bootstrap() -> None:
    factor = 0.24**4
    assert block_endpoint_tail_bound(2.0, factor, 3) >= 2.0 * factor**3
    assert blocks_for_tolerance(1.0 / 512.0, factor, 1e-6) == 5
    assert relative_snapshot_bound(1.0 / 512.0, factor, 5) < 1e-6


def test_coercive_defect_identity() -> None:
    matrix = np.array([[3.0, 0.4], [0.4, 2.0]])
    coupling = np.array([0.5, -0.2])
    delta = 0.03
    exact = np.linalg.solve(matrix, coupling)
    trial = exact + np.array([0.01, -0.02])
    phi = schur_trial_form(matrix, coupling, delta, trial)
    surplus = coercive_secular_surplus(matrix, coupling, delta)
    defect = coercive_defect(matrix, coupling, trial)
    assert abs(phi - (-surplus + defect)) < 1e-12


def test_coercive_rejects_nonpositive_matrix() -> None:
    matrix = np.diag([1.0, 0.0])
    with pytest.raises(ValueError):
        coercive_secular_surplus(matrix, np.ones(2), 0.1)
