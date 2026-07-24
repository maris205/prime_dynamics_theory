from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_full_archive_has_all_transitions_and_no_failures() -> None:
    data = json.loads((ROOT / "results/projective_gram_audit.json").read_text())
    summary = data["audit_summary"]
    assert summary["chain_count"] == 30
    assert summary["transition_count"] == 330
    assert summary["one_step_failure_count"] == 0
    assert summary["cumulative_failure_count"] == 0
    assert summary["minimum_projective_distance"] > 0.0


def test_claim_boundary_is_explicit() -> None:
    data = json.loads((ROOT / "results/projective_gram_audit.json").read_text())
    boundary = data["theorem_boundary"]
    assert boundary["projective_base_recurrence_proved"]
    assert not boundary["projective_variation_summable_for_model"]
    assert not boundary["positive_normalized_base_liminf"]
    assert not boundary["riemann_hypothesis"]

