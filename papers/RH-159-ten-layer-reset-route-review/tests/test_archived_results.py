import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def data() -> dict:
    return json.loads((ROOT / "results/route_audit.json").read_text())


def test_all_eight_archives_reverified() -> None:
    summary = data()["audit_summary"]
    assert summary["paper_count"] == 8
    assert summary["archive_verified_paper_count"] == 8
    assert summary["publication_file_count"] == 96
    assert summary["hash_check_count"] == 319
    assert summary["hash_failure_count"] == 0
    assert summary["internal_dependency_edge_count"] == 16
    assert summary["internal_dependency_graph_acyclic"]


def test_ten_gate_and_route_classification() -> None:
    payload = data()
    summary = payload["audit_summary"]
    assert summary["gate_count"] == 10
    assert summary["finite_certified_gate_count"] == 7
    assert summary["exact_obstruction_gate_count"] == 1
    assert summary["open_gate_count"] == 2
    assert summary["finite_closed_route_count"] == 2
    assert summary["program_closed_route_count"] == 0
    states = {route["name"]: route["finite_seed_state"] for route in payload["routes"]}
    assert states == {
        "recursive": "rejected",
        "native": "finite_closed",
        "contemporaneous": "rejected",
        "lagged": "finite_closed",
    }


def test_key_finite_counts_and_typed_floor() -> None:
    metrics = data()["metrics"]
    assert metrics["reset_snapshots_certified"] == 130
    assert metrics["transition_overlap_certified"] == 120
    assert metrics["native_subunit_count"] == 130
    assert metrics["native_support_positive_count"] == 120
    assert metrics["contemporaneous_exact_zero_count"] == 50
    assert metrics["lagged_four_mode_count"] == 120
    assert metrics["lagged_cross_implied_native_fourth_floor"] > 0.0


def test_claim_boundary() -> None:
    boundary = data()["theorem_boundary"]
    assert boundary["positive_block_directional_to_native_theorem"]
    assert boundary["eight_paper_archive_reverified"]
    assert not boundary["uniform_all_level_reset_theorem"]
    assert not boundary["stage_A"]
