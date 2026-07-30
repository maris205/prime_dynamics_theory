import json
from pathlib import Path


def test_result_firewall():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["paper_numbers"] == list(range(302, 312))
    assert data["actual_annular_convergence_proved"] is False
    assert data["endpoint_hardy_convergence_proved"] is False
    assert data["first_alias_joint_boundary_layer_proved"] is False
    assert data["growing_clock_head_transport_proved"] is False
    assert data["spectral_score"] == 4
    assert data["counterloop_score"] == 4
    assert data["complete_count"] == 0
    assert not any(data["gates"].values())
