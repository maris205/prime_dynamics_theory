from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_review_archive() -> None:
    data = json.loads((ROOT / "results/ten_layer_source_support_review.json").read_text())
    summary = data["audit_summary"]
    assert summary["upstream_paper_count"] == 9
    assert summary["upstream_archive_verification_count"] == 9
    assert summary["truth_table_case_count"] == 8
    assert summary["truth_table_closed_case_count"] == 1
    assert summary["minimal_open_interface_count"] == 3
    assert summary["claim_boundary_violation_count"] == 0
    assert summary["top_priority_interface"] == "E-update"


def test_program_boundary() -> None:
    data = json.loads((ROOT / "results/ten_layer_source_support_review.json").read_text())
    boundary = data["theorem_boundary"]
    assert boundary["inclusion_minimal_three_interface_frontier"]
    assert boundary["correlated_cocycle_is_primary_route"]
    assert not boundary["finite_end_to_end_interval_bridge_closed"]
    assert not boundary["all_level_directional_support_proved"]
    assert not boundary["riemann_hypothesis"]

