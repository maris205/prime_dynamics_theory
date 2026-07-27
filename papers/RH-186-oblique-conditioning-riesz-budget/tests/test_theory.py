from oblique_conditioning import conditioned_residual_budget, oblique_condition_number, projector_perturbation_bound


def test_conditioning_budget():
    assert oblique_condition_number(0.2) == 5.0
    result = conditioned_residual_budget(0.2, 0.1, 0.05)
    assert result["amplified_maximum_residual"] == 0.5
    assert result["conditioned_contraction_gate"]


def test_projector_perturbation_pole():
    assert projector_perturbation_bound(4.0, 0.1) > 0.0
    assert projector_perturbation_bound(4.0, 0.25) == float("inf")
