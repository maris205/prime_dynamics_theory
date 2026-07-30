import json
from pathlib import Path


def test_result_firewall():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["exact_logarithmic_singularity_proved"] is True
    assert data["analytic_remainder_beyond_unit_circle_proved"] is True
    assert data["actual_endpoint_h2_convergence_proved"] is False
    assert not any(data["gates"].values())
