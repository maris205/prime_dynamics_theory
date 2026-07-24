import math
import itertools

import numpy as np

from finite_horizon_tail import fixed_point, greedy_step, optimal_young_step, safety_radius


def test_closed_form_matches_dense_young_search():
    rng = np.random.default_rng(137)
    grid = np.logspace(-8, 8, 20001)
    for _ in range(64):
        a, b, q, x = 10.0 ** rng.uniform(-5, 3, size=4)
        result = optimal_young_step(a, b, q, x)
        brute = np.min(a * (1.0 + grid) * x + q + b * (1.0 + 1.0 / grid))
        assert result["envelope"] <= brute * (1.0 + 2e-6)


def test_safety_radius_is_sharp():
    a, b, q = 3.5, 0.04, 0.1
    radius = safety_radius(a, b, q)
    assert optimal_young_step(a, b, q, radius * (1.0 - 1e-8))["envelope"] < 1.0
    assert optimal_young_step(a, b, q, radius * (1.0 + 1e-8))["envelope"] > 1.0


def test_fixed_point_and_long_run_obstruction():
    a, b, q = 0.3, 0.02, 0.01
    point = fixed_point(a, b, q)
    assert abs(optimal_young_step(a, b, q, point)["envelope"] - point) < 1e-12
    assert math.isinf(fixed_point(1.0, b, q))


def test_greedy_step_selects_smallest_map():
    candidates = [(0.2, 0.1, 0.01), (2.0, 1e-5, 0.01), (0.7, 0.04, 0.0)]
    source = 1e-4
    result = greedy_step(candidates, source)
    direct = [optimal_young_step(*candidate, source)["envelope"] for candidate in candidates]
    assert result["index"] == int(np.argmin(direct))
    assert result["envelope"] == min(direct)


def test_greedy_propagation_is_horizon_optimal_for_monotone_candidate_maps():
    families = [
        [(0.2, 0.1, 0.01), (2.0, 1e-5, 0.01)],
        [(0.8, 0.02, 0.0), (0.1, 0.2, 0.0)],
        [(1.4, 1e-4, 0.02), (0.4, 0.03, 0.02)],
    ]
    greedy = 1e-5
    for family in families:
        greedy = greedy_step(family, greedy)["envelope"]
    terminals = []
    for choices in itertools.product(*families):
        value = 1e-5
        for candidate in choices:
            value = optimal_young_step(*candidate, value)["envelope"]
        terminals.append(value)
    assert abs(greedy - min(terminals)) < 1e-14
