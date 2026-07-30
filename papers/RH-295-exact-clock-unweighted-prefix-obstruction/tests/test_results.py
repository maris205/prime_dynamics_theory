import json
from pathlib import Path


def test_result_scope():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["exact_clock_uniform_error_vanishes"] is True
    assert data["weighted_prefix_diverges"] is True
    assert data["physical_noisy_spike_claimed"] is False
    assert data["global_nonexistence_claimed"] is False
    assert not any(data["gates"].values())
