from __future__ import annotations

import json
from pathlib import Path

from experiments.build_result import build_payload


ROOT = Path(__file__).resolve().parents[1]


def test_built_payload_passes_sources_foundation_and_finite_checks() -> None:
    payload = build_payload()
    assert payload["source_audit"]["pass"] is True
    assert payload["four_volume_foundation_audit"]["pass"] is True
    finite = payload["finite_checks"]
    assert finite["rank_bound_pass"] is True
    assert finite["entropy_prefix_strictly_increasing_in_level"] is True
    assert finite["all_first_defect_rows_match"] is True
    assert finite["all_inversion_truncation_errors_below_1e_minus_18"] is True


def test_route_and_claim_firewall() -> None:
    payload = build_payload()
    route = payload["route"]
    assert route["route_A"] == "GO"
    assert route["route_B"] == "STOP_SCOPED"
    assert route["trigger_5_independent_theorem_edge"] is True
    assert route["triggers_1_to_4_touched"] is False
    assert route["physical_route_coordinate"] == (
        "actual_same_clock_unnormalized_head_transport_open"
    )
    assert payload["gates"]
    assert payload["false_claims"]
    assert not any(payload["gates"].values())
    assert not any(payload["false_claims"].values())


def test_four_volume_foundation_is_frozen() -> None:
    payload = build_payload()
    assert payload["four_volume_foundation_audit"] == {
        "archive_member_count": 73,
        "dependency_hash_count": 1548,
        "failure_count": 0,
        "manifest_sha256":
            "24dcf3c6e74c5252e7e278d9141a656c6b97bb30fad6578da8c193cc1063a897",
        "numbered_source_count": 361,
        "pass": True,
        "result_hash_count": 8,
        "volume_count": 4,
    }
    assert payload["route"]["four_volume_foundation_preserved"] is True


def test_persisted_result_matches_builder() -> None:
    persisted = json.loads((ROOT / "results" / "result.json").read_text())
    assert persisted == build_payload()
