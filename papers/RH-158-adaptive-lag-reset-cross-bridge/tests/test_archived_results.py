import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_complete_eight_lag_atlas() -> None:
    summary = json.loads((ROOT / "results/lag_audit.json").read_text())["audit_summary"]
    assert summary["target_count"] == 120
    assert summary["candidate_count"] == 694
    assert summary["certificate_counts_by_lag_horizon"] == {
        "1": 76, "2": 84, "3": 92, "4": 101,
        "5": 106, "6": 112, "7": 117, "8": 120,
    }
    assert summary["uncentered_certificate_counts_by_lag_horizon"]["8"] == 118
    assert summary["scalar_centering_recovered_target_count_at_maximum_lag"] == 2
    assert summary["adaptive_four_mode_certificate_count"] == 120
    assert summary["adaptive_failure_count"] == 0
    assert summary["maximum_first_certifying_lag"] == 8


def test_suffix_and_terminal_closure() -> None:
    summary = json.loads((ROOT / "results/lag_audit.json").read_text())["audit_summary"]
    assert summary["half_suffix_target_count"] == 62
    assert summary["half_suffix_certificate_counts_by_lag_horizon"]["8"] == 62
    assert summary["terminal_target_count"] == 10
    assert summary["terminal_certificate_counts_by_lag_horizon"]["8"] == 10
    assert summary["minimum_selected_normalized_base_lower"] > 0.0
    assert summary["minimum_selected_path_overlap_lower"] > 0.0


def test_boundary_is_finite_not_all_level() -> None:
    boundary = json.loads((ROOT / "results/lag_audit.json").read_text())["theorem_boundary"]
    assert boundary["all_frozen_update_targets_four_mode_certified_with_lag_at_most_eight"]
    assert boundary["all_terminal_targets_four_mode_certified"]
    assert not boundary["uniform_all_level_bounded_lag_law"]
    assert not boundary["complete_outward_directional_assembly"]
    assert not boundary["stage_A"]
