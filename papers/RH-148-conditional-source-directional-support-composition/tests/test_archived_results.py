from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_readiness_archive_and_synthetic_composition() -> None:
    data = json.loads((ROOT / "results/source_support_composition_audit.json").read_text())
    summary = data["audit_summary"]
    assert summary["upstream_archive_count"] == 8
    assert summary["upstream_archive_verification_count"] == 8
    assert summary["synthetic_composition_count"] == 4096
    assert summary["synthetic_composition_failure_count"] == 0
    assert summary["omission_witness_count"] == 4
    assert summary["omission_witness_pass_count"] == 4
    assert summary["missing_all_level_interface_count"] == 3


def test_no_end_to_end_overclaim() -> None:
    data = json.loads((ROOT / "results/source_support_composition_audit.json").read_text())
    boundary = data["theorem_boundary"]
    assert boundary["conditional_source_to_support_theorem"]
    assert not boundary["finite_end_to_end_interval_source_to_support_closed"]
    assert not boundary["all_level_directional_support_proved"]
    assert not boundary["uniform_stage_A_closed"]
    assert not boundary["riemann_hypothesis"]

