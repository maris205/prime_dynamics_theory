import json
from pathlib import Path


def test_result_firewall():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["exact_moment_packet_proved"] is True
    assert data["conjugate_closed_for_real_moments"] is True
    assert data["actual_noisy_spectrum_constructed"] is False
    assert not any(data["gates"].values())
