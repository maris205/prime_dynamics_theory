import json
from pathlib import Path


def test_result_firewall():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["mass_to_norm_lower_bound_proved"] is True
    assert data["rate_variable"] == "complement_hilbert_schmidt_mass"
    assert data["hinfinity_mass_power_rate_above_ceiling_excluded"] is True
    assert data["h2_mass_power_rate_above_ceiling_excluded"] is True
    assert data["actual_annular_convergence_excluded"] is False
    assert not any(data["gates"].values())
