import json
from pathlib import Path


def test_all_gate_boundaries():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert all(value is False for value in data["macro_gates"].values())
    assert data["hilbert_polya_operator"] is False
    assert data["riemann_zero_identification"] is False
    assert data["zeta_divisor_equality"] is False
    assert data["rh_implication"] is False
