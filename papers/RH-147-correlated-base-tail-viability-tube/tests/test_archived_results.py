from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_full_tube_archive() -> None:
    data = json.loads((ROOT / "results/correlated_tube_audit.json").read_text())
    summary = data["audit_summary"]
    assert summary["chain_count"] == 30
    assert summary["transition_count"] == 330
    assert summary["positive_tube_chain_count"] == 28
    assert summary["common_1e_10_tube_chain_count"] == 28
    assert summary["clean_suffix_chain_count"] == 18
    assert summary["clean_suffix_minimum_tube_beta"] > 1.5e-10
    assert summary["support_recomputation_failure_count"] == 0


def test_boundary_flags() -> None:
    data = json.loads((ROOT / "results/correlated_tube_audit.json").read_text())
    boundary = data["theorem_boundary"]
    assert boundary["sharp_correlated_tube_multiplier_proved"]
    assert boundary["lower_bounded_log_cocycle_support_theorem"]
    assert not boundary["all_level_support_cocycle_verified"]
    assert not boundary["uniform_stage_A_closed"]
    assert not boundary["riemann_hypothesis"]

