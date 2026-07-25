import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_half_suffix() -> None:
    summary = json.loads((ROOT / "results/suffix_audit.json").read_text())["audit_summary"]
    assert summary["full_transition_count"] == 120
    assert summary["half_suffix_transition_count"] == 62
    assert summary["half_suffix_common_overlap_floor"] > 0.066
    assert summary["half_suffix_inverse_overlap_upper"] < 15.1
    assert summary["half_suffix_maximum_log_inverse_drawdown"] < 9.0
    assert summary["half_suffix_minimum_correlated_base_floor"] > 2e-7


def test_boundary() -> None:
    boundary = json.loads((ROOT / "results/suffix_audit.json").read_text())["theorem_boundary"]
    assert boundary["half_suffix_frozen_certificate"]
    assert not boundary["uniform_all_level_suffix_floor"]
    assert not boundary["native_reset_tail_assembly"]
