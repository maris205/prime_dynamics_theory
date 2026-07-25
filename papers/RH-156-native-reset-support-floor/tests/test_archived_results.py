import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_support_audit() -> None:
    summary = json.loads((ROOT / "results/support_audit.json").read_text())["audit_summary"]
    assert summary["transition_count"] == 120
    assert summary["positive_support_count"] == 120
    assert summary["minimum_support_lower"] > 3.2e-8
    assert summary["support_above_1e_8_count"] == 120
    assert summary["support_above_1e_6_count"] == 111
    assert summary["support_above_1e_4_count"] == 74
    assert summary["half_suffix_transition_count"] == 62
    assert summary["half_suffix_positive_support_count"] == 62


def test_boundary() -> None:
    boundary = json.loads((ROOT / "results/support_audit.json").read_text())["theorem_boundary"]
    assert boundary["all_frozen_transition_support_positive"]
    assert boundary["half_suffix_common_native_support_tube"]
    assert not boundary["directional_cross_action_bridge"]
