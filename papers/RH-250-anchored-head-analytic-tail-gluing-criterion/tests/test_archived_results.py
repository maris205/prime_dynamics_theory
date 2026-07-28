import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_gluing_certificate_is_missing_for_current_head():
    payload = json.loads((ROOT / "results/head_tail_audit.json").read_text())
    assert payload["head_endpoint_count"] == 32
    assert payload["tail_endpoint_count"] == 17
    assert payload["head_pass_count"] == 0
    assert payload["complete_gluing_certificate_count"] == 0
    assert payload["head_minimum_to_tail_bound_ratio"] > 8000.0
    boundary = payload["theorem_boundary"]
    assert boundary["finite_head_plus_tail_log_gluing_theorem"] is True
    assert boundary["uniform_tail_constants"] is False
    assert boundary["gate_A"] is False
