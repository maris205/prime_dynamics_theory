import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_audit() -> None:
    summary = json.loads((ROOT / "results/memory_pair_audit.json").read_text())["audit_summary"]
    assert summary["snapshot_count"] == 130
    assert summary["tail_active_snapshot_count"] == 80
    assert summary["subunit_recent_tail_count"] == 130
    assert summary["half_suffix_snapshot_count"] == 62
    assert summary["half_suffix_subunit_count"] == 62
    assert summary["maximum_recent_tail_ratio_upper"] < 0.225
    assert summary["minimum_selected_eigenvalue_to_twice_tail_margin"] > 2.72
    assert summary["bound_dominance_failure_count"] == 0


def test_boundary() -> None:
    boundary = json.loads((ROOT / "results/memory_pair_audit.json").read_text())["theorem_boundary"]
    assert boundary["all_frozen_native_pairs_subunit"]
    assert not boundary["directional_cross_action_identified"]
    assert not boundary["uniform_all_level_packet_eigenvalue_lower"]
