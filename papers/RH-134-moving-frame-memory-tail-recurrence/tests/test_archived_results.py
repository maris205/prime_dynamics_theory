import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_audit():
    data = load("memory_tail_audit.json")
    summary = data["audit_summary"]
    assert summary["chain_count"] == 30
    assert summary["transition_count"] == 330
    assert summary["birth_transition_count"] == 24
    assert summary["tail_identity_failure_count"] == 0
    assert summary["raw_loewner_failure_count"] == 0
    assert summary["weighted_loewner_failure_count"] == 0
    assert summary["birth_dominant_transition_count"] == 240
    assert summary["frame_dominant_transition_count"] == 0
    assert summary["maximum_weighted_multiplicative_factor"] < 0.004


def test_boundary_and_smoke():
    data = load("memory_tail_audit.json")
    assert data["theorem_boundary"]["exact_memory_tail_birth_identity"]
    assert not data["theorem_boundary"]["relative_gram_normalized_recurrence_proved"]
    assert not data["theorem_boundary"]["riemann_hypothesis"]
    assert load("memory_tail_smoke.json")["audit_summary"]["transition_count"] == 8
