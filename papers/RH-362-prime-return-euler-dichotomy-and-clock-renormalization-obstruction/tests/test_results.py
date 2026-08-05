from __future__ import annotations

import json
from pathlib import Path

from experiments.build_result import build_payload


ROOT = Path(__file__).resolve().parents[1]


def test_built_payload_passes_source_and_finite_checks() -> None:
    payload = build_payload()
    assert payload["source_audit"]["pass"] is True
    finite = payload["finite_checks"]
    assert finite["a0_escape_prefix_pass"] is True
    assert finite["return_divisibility_primes_through_43_indices_through_12"] is True
    assert finite["low_rank_primes_from_product"] == [2, 3, 5]
    assert finite["low_rank_primes_from_direct_ranks"] == [2, 3, 5]


def test_all_gate_and_forbidden_claim_values_are_false() -> None:
    payload = build_payload()
    assert payload["gates"]
    assert payload["false_claims"]
    assert not any(payload["gates"].values())
    assert not any(payload["false_claims"].values())


def test_persisted_result_matches_builder() -> None:
    persisted = json.loads((ROOT / "results" / "result.json").read_text())
    assert persisted == build_payload()


def test_four_volume_foundation_is_explicitly_preserved() -> None:
    payload = build_payload()
    foundation = payload["four_volume_foundation_audit"]
    assert foundation == {
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
    assert payload["route"]["physical_route_coordinate"] == (
        "actual_same_clock_unnormalized_head_transport_open"
    )
    assert payload["route"]["trigger_5_independent_theorem_edge"] is True
    assert payload["route"]["triggers_1_to_4_touched"] is False
