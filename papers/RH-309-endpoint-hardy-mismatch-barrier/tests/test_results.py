import json
from pathlib import Path


def test_result_firewall():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["mismatch_belongs_to_endpoint_h2"] is True
    assert data["mismatch_belongs_to_endpoint_hinfinity"] is False
    assert data["endpoint_h2_convergence_proved"] is False
    assert data["endpoint_h2_nonconvergence_proved"] is False
    assert data["mass_logarithmic_rate_barrier_proved"] is True
    assert data["small_noise_logarithmic_rate_barrier_proved"] is True
    assert not any(data["gates"].values())
