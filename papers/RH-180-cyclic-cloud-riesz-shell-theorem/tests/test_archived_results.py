import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_cycle_riesz_archive():
    payload = json.loads((ROOT / "results/cycle_riesz_audit.json").read_text())
    assert payload["matrix_case_count"] == 192
    assert payload["shell_case_count"] == 1248
    assert payload["rank_failure_count"] == 0
    assert payload["certificate_failure_count"] == 0
    assert payload["maximum_directed_schur_product"] < 1.0
    assert not payload["theorem_boundary"]["physical_transfer_operator_budget"]
