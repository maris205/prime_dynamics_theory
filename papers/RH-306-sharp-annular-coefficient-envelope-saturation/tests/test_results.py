import json
from pathlib import Path


def test_result_firewall():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["coefficient_envelope_information_class_power_exponent_sharp"] is True
    assert data["coefficient_envelope_information_class_logarithmic_factor_sharp"] is True
    assert data["actual_noisy_complement_function_realization"] is False
    assert data["spectral_power_sum_realization"] is False
    assert data["actual_annular_convergence_rate_sharp"] is False
    assert data["actual_annular_convergence_proved"] is False
    assert not any(data["gates"].values())
