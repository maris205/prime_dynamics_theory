import json
from pathlib import Path


def test_result_boundary_and_activation():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["uniform_variable_rank_certificate"] is True
    assert data["physical_riesz_quotient_certificate"] is False
    assert data["counterloop_spectral_identification"] is False
    assert data["root_rate_limit_upper"] < 1.0
    assert data["gate_A"] is False
