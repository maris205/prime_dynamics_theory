import json
from pathlib import Path


def test_conditional_boundary():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["uniform_variable_rank_certificate"] is False
    assert data["gate_A"] is False
