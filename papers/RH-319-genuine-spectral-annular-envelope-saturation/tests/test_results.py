import json
from pathlib import Path


def test_result_firewall():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["genuine_spectral_saturation_proved"] is True
    assert data["coefficient_envelope_only"] is False
    assert data["actual_noisy_rate_sharpness_proved"] is False
    assert not any(data["gates"].values())
