from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str) -> dict[str, object]:
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_full_audit() -> None:
    summary = load("optimal_gauge_audit.json")["audit_summary"]
    assert summary["pair_count"] == 96
    assert summary["gram_alignment_failure_count"] == 0
    assert summary["tail_dominance_failure_count"] == 0
    assert summary["gamma_transfer_failure_count"] == 0
    assert summary["sampled_optimality_failure_count"] == 0


def test_smoke_and_boundary() -> None:
    assert load("optimal_gauge_smoke.json")["audit_summary"]["pair_count"] == 4
    boundary = load("optimal_gauge_audit.json")["theorem_boundary"]
    assert boundary["optimal_exact_gram_gauge_theorem"]
    assert boundary["five_scale_phase_pairing_audited"]
    assert not boundary["uniform_tail_inflation_proved"]
    assert not boundary["riemann_hypothesis"]

