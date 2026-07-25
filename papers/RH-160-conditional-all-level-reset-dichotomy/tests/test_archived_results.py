import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def data() -> dict:
    return json.loads((ROOT / "results/conditional_audit.json").read_text())


def test_finite_native_and_directional_clauses() -> None:
    payload = data()
    summary = payload["audit_summary"]
    checklist = payload["finite_checklist"]
    assert summary["all_native_finite_checks_pass"]
    assert summary["all_directional_finite_checks_pass"]
    assert checklist["overlap_positive_count"] == checklist["overlap_count"] == 120
    assert checklist["native_subunit_count"] == checklist["native_snapshot_count"] == 130
    assert checklist["lagged_four_mode_count"] == checklist["lagged_target_count"] == 120
    assert checklist["positive_lag_path_count"] == 120


def test_global_finite_calibration_is_positive() -> None:
    constants = data()["constants"]
    assert constants["selected_eigenvalue_to_twice_tail_global_margin"] > 1.0
    assert constants["native_global_support_floor"] > 0.0
    assert constants["native_interface_support_floor"] > 0.0
    assert constants["directional_observed_path_floor"] > 0.0
    assert constants["directional_consecutive_overlap_floor"] > 0.0
    assert constants["native_global_support_floor"] <= constants["minimum_local_native_support_floor"]


def test_omission_witnesses_and_archive() -> None:
    payload = data()
    assert payload["audit_summary"]["omission_witness_count"] == 5
    for values in payload["omission_witnesses"].values():
        assert values[-1] < values[0]
        assert values[-1] > 0.0
    assert payload["audit_summary"]["archive_verified_paper_count"] == 9
    assert payload["audit_summary"]["archive_publication_hash_count"] == 108
    assert payload["audit_summary"]["archive_publication_hash_failure_count"] == 0


def test_boundary_is_conditional() -> None:
    boundary = data()["theorem_boundary"]
    assert boundary["conditional_native_all_level_floor"]
    assert boundary["conditional_directional_all_level_floor"]
    assert not boundary["any_eventual_interface_proved_for_the_prime_dynamics_sequence"]
    assert not boundary["typed_downstream_assembly_proved"]
    assert not boundary["stage_A"]
