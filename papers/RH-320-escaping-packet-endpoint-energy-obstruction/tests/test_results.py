import json
from pathlib import Path


def test_result_firewall():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["escaping_spectral_packet_counterexample_proved"] is True
    assert data["strict_annulus_convergence_with_endpoint_failure_proved"] is True
    assert data["actual_endpoint_nonconvergence_proved"] is False
    assert all(row["endpoint_coefficient"] == 1.0 for row in data["rows"])
    assert all(row["squared_mass"] <= row["mass_upper"] for row in data["rows"])
    assert not any(data["gates"].values())
