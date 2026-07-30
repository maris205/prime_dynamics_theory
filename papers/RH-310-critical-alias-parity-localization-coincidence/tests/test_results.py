import json
from pathlib import Path


def test_result_firewall():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["critical_asymptotic_slope_coincidence_proved"] is True
    assert data["first_alias_matching_law_proved"] is True
    assert data["separate_alias_parity_majorant_decays"] is False
    assert data["joint_boundary_layer_trace_law_proved"] is False
    assert data["actual_full_trace_divergence_proved"] is False
    assert abs(data["first_alias_clearance_exponent"]) < 1e-15
    assert not any(data["gates"].values())
