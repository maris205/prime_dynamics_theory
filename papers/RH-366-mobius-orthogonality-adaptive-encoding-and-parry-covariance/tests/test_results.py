from __future__ import annotations

import json
from pathlib import Path

from experiments.build_result import build_payload, validate_payload_shape


ROOT = Path(__file__).resolve().parents[1]


def test_source_foundation_and_finite_checks_pass() -> None:
    payload = build_payload()
    assert payload["source_audit"]["pass"] is True
    assert len(payload["source_audit"]["rows"]) == 23
    assert payload["four_volume_foundation_audit"]["pass"] is True
    finite = payload["finite_checks"]
    assert finite["graph_equivalence"]["pass"] is True
    assert finite["exceptional_prefix"]["identity_pass"] is True
    assert finite["all_capacity_rows_pass"] is True
    assert finite["all_variance_rows_pass"] is True


def test_route_gate_and_forbidden_claim_firewall() -> None:
    payload = build_payload()
    route = payload["route"]
    assert route["route_A"] == "GO"
    assert route["route_B"] == "STOP_SCOPED"
    assert route["trigger_5_independent_theorem_edge"] is True
    assert route["triggers_1_to_4_touched"] is False
    assert route["physical_route_coordinate"] == (
        "actual_same_clock_unnormalized_head_transport_open"
    )
    assert len(payload["false_claims"]) == 17
    assert not any(payload["gates"].values())
    assert not any(payload["false_claims"].values())


def test_r001_scoped_negative_and_numeric_boundary() -> None:
    diagnostic = build_payload()["r001_diagnostic"]
    assert diagnostic["N"] == 2**20
    assert diagnostic["exceptional_raw_sum"] == 425025
    assert diagnostic["open_minimum_raw_sum"] == -516163
    assert diagnostic["open_maximum_raw_sum"] == 515983
    assert diagnostic["surrogate_count"] == 1023
    assert diagnostic["surrogate_exceedances"] == 420
    assert diagnostic["rank_p_value"] == 421 / 1024
    assert diagnostic["rank_test_significant_at_0p01"] is False
    assert diagnostic["finite_ordering_result"] == "SCOPED_NEGATIVE"
    assert diagnostic["variance_evaluation_mode"] == "floating_geometric_cutoff_diagnostic"
    assert diagnostic["geometric_omission_bound_per_N_before_roundoff"] < 1.3e-15


def test_result_schema_and_persisted_payload() -> None:
    payload = build_payload()
    validate_payload_shape(payload)
    schema = json.loads((ROOT / "results/result.schema.json").read_text())
    assert schema["type"] == "object"
    assert schema["additionalProperties"] is False
    assert set(schema["required"]) == set(payload)
    persisted = json.loads((ROOT / "results/result.json").read_text())
    assert persisted == payload
