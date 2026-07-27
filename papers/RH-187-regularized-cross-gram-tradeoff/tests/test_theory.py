from cross_gram_regularization import (
    clipped_cross_gram_budget,
    clipped_gate_infimum,
    directionwise_clipped_budget,
)


def test_pareto_identity_below_and_above_cross_angle():
    good = clipped_gate_infimum(0.2, 0.1)
    assert good["strict_contraction_exists"]
    assert good["gate_infimum"] == 0.5
    bad = clipped_gate_infimum(0.1, 0.2)
    assert not bad["strict_contraction_exists"]
    assert bad["gate_infimum"] == 1.0


def test_clipping_tradeoff_formula():
    result = clipped_cross_gram_budget(0.1, 0.2, 0.4)
    assert abs(result["duality_defect"] - 0.75) < 1e-12
    assert abs(result["combined_regularized_gate"] - 1.25) < 1e-12
    assert not result["strict_contraction"]


def test_directionwise_criterion_is_exact():
    good = directionwise_clipped_budget([0.5, 0.2], [0.1, 0.05], 0.1)
    assert good["strict_contraction_in_every_direction"]
    assert good["exact_directionwise_criterion"]
    bad = directionwise_clipped_budget([0.5, 0.2], [0.1, 0.25], 1.0)
    assert not bad["strict_contraction_in_every_direction"]
    assert not bad["exact_directionwise_criterion"]
