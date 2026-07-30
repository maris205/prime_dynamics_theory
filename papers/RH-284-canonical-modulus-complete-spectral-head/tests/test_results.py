import json
from pathlib import Path


def test_result_canonical_scope():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["canonical_relative_to_cutoff"] is True
    assert data["cutoff_intrinsic_to_dynamics"] is False
    assert data["threshold_tie_left_in_tail"] is True
    assert data["gate_A"] is False
