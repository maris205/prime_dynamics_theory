import json
from pathlib import Path


def test_result_scope():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["annular_hinfty_criterion_proved"] is True
    assert data["annular_hardy_criterion_proved"] is True
    assert data["endpoint_hardy_implication_false"] is True
    assert data["actual_noisy_annular_convergence_proved"] is False
    assert data["direct_weighted_prefix_activated"] is False
    assert not any(data["gates"].values())
