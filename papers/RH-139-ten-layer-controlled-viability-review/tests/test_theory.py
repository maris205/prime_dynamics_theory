import numpy as np

from controlled_viability import controlled_support_floor, directional_candidate


def test_eventual_controlled_floor():
    tail_upper = 0.64
    base_lower = 0.02
    floor = controlled_support_floor(tail_upper, base_lower)
    tails = np.linspace(0.1, tail_upper, 128)
    bases = np.linspace(base_lower, 0.2, 128)
    assert min(directional_candidate(x, a) for x, a in zip(tails, bases)) >= floor - 1e-15


def test_tail_gap_is_architecture_sharp():
    values = [directional_candidate((1.0 - 1.0 / n) ** 2, 1.0) for n in range(2, 1002)]
    assert values[-1] < 2e-12
    assert controlled_support_floor(1.0, 1.0) == 0.0


def test_base_liminf_is_architecture_sharp():
    values = [directional_candidate(0.0, 1.0 / n) for n in range(1, 1002)]
    assert values[-1] < 0.001
    assert controlled_support_floor(0.0, 0.0) == 0.0


def test_per_step_contraction_is_not_necessary_for_one_safe_crossing():
    metric_base = 100.0
    source = 1e-5
    assert metric_base >= 1.0
    assert directional_candidate(metric_base * source, 0.1) > 0.0
