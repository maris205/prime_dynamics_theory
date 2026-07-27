import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_physical_calibration():
    payload = json.loads((ROOT / "results/bi_krylov_audit.json").read_text())
    assert payload["window_count"] == 126
    assert payload["biorthogonality_failure_count"] == 0
    assert payload["local_sigma_0_01_length_4_two_sided_gate_count"] > 0
    assert payload["length_3_two_sided_gate_count"] == 0
