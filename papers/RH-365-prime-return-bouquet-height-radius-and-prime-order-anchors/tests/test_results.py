from __future__ import annotations

import json
from pathlib import Path

from experiments.build_result import build_payload, validate_payload_shape


ROOT = Path(__file__).resolve().parents[1]


def test_built_payload_passes_sources_foundation_and_finite_checks() -> None:
    payload = build_payload()
    assert payload["source_audit"]["pass"] is True
    assert payload["four_volume_foundation_audit"]["pass"] is True
    finite = payload["finite_checks"]
    assert finite["all_midpoint_rows_pass"] is True
    assert finite["all_height_rows_pass"] is True
    assert finite["all_gcd_height_bounds_pass"] is True
    assert finite["all_odd_prime_anchor_rows_pass"] is True
    assert finite["all_raw_coefficient_firewalls_pass"] is True


def test_route_gate_and_fifteen_forbidden_claim_firewall() -> None:
    payload = build_payload()
    route = payload["route"]
    assert route["route_A"] == "GO"
    assert route["route_B"] == "STOP_SCOPED"
    assert route["trigger_5_independent_theorem_edge"] is True
    assert route["triggers_1_to_4_touched"] is False
    assert route["physical_route_coordinate"] == (
        "actual_same_clock_unnormalized_head_transport_open"
    )
    assert len(payload["false_claims"]) == 15
    assert not any(payload["gates"].values())
    assert not any(payload["false_claims"].values())


def test_result_schema_and_exact_coefficient_rows() -> None:
    payload = build_payload()
    validate_payload_shape(payload)
    schema = json.loads((ROOT / "results" / "result.schema.json").read_text())
    assert schema["type"] == "object"
    assert schema["additionalProperties"] is False
    assert set(schema["required"]) == set(payload)
    type_names = {
        str: "string",
        dict: "object",
        bool: "boolean",
    }
    for key, value in payload.items():
        assert schema["properties"][key]["type"] == type_names[type(value)]
    finite = payload["finite_checks"]
    assert finite["primitive_rank_counts_c_1_to_12"] == [0, 0, 1, 2, 1, 1, 1, 2, 1, 2, 4, 3]
    assert finite["bouquet_traces_T_1_to_12"] == [0, 0, 3, 8, 5, 9, 7, 24, 12, 25, 44, 53]
    assert finite["zeta_coefficients_q_0_to_12"][7] == 3
    assert finite["zeta_coefficients_q_0_to_12"][11] == 13


def test_persisted_result_matches_builder() -> None:
    persisted = json.loads((ROOT / "results" / "result.json").read_text())
    assert persisted == build_payload()
