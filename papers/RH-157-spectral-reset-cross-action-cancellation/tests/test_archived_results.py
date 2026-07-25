import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_cross_audit() -> None:
    summary = json.loads((ROOT / "results/cross_audit.json").read_text())["audit_summary"]
    assert summary["snapshot_count"] == 130
    assert summary["tail_inactive_exact_zero_count"] == 50
    assert summary["tail_active_snapshot_count"] == 80
    assert summary["active_four_mode_coupling_certificate_count"] == 54
    assert summary["active_four_mode_coupling_failure_count"] == 26
    assert summary["half_suffix_snapshot_count"] == 62
    assert summary["half_suffix_four_mode_coupling_certificate_count"] == 30
    assert summary["terminal_four_mode_coupling_certificate_count"] == 2
    assert summary["complete_active_channel_count"] == 2


def test_boundary() -> None:
    boundary = json.loads((ROOT / "results/cross_audit.json").read_text())["theorem_boundary"]
    assert boundary["exact_cross_action_tail_cancellation"]
    assert not boundary["direct_native_to_directional_bridge"]
    assert not boundary["lagged_reset_bridge"]
