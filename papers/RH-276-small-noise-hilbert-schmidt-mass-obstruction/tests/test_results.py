import json
from pathlib import Path


def test_scope_flags():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["raw_S2_zero_noise_convergence"] is False
    assert data["rank_growing_quotient_excluded"] is False
    assert data["gate_A"] is False
