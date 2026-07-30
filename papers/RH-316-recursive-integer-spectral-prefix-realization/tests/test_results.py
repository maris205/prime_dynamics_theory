import json
from pathlib import Path


def test_result_firewall():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["exact_finite_prefix_realization_proved"] is True
    assert data["finite_normal_spectrum_constructed"] is True
    assert data["actual_noisy_spectrum_identified"] is False
    assert data["numerical_anchor_source"].startswith("RH-263-")
    assert not any(data["gates"].values())
