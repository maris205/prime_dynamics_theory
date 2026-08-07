import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _reject_duplicate_keys(pairs):
    output = {}
    for key, value in pairs:
        assert key not in output, f"duplicate JSON key: {key}"
        output[key] = value
    return output


def test_result_ledger_and_claim_boundary():
    payload = json.loads(
        (ROOT / "results" / "result.json").read_text(),
        object_pairs_hook=_reject_duplicate_keys,
    )
    assert payload["status"] == "RH-377_mixed_exponent_run_hierarchy_two_envelope_capacity"
    assert payload["source_locks"]["count"] == 13
    assert payload["source_locks"]["pass"]
    assert payload["certificate"]["all_pass"]
    assert payload["claim_boundary"]["route_a"] == "GO"
    assert payload["claim_boundary"]["route_b"] == "STOP_SCOPED"
    assert payload["claim_boundary"]["first_unresolved_object"] == "ordinary convergence of (U_N+abs(V_N))/N"
    assert not any(payload["gates"].values())


def test_result_matches_closed_shallow_schema_contract():
    schema = json.loads(
        (ROOT / "results" / "result.schema.json").read_text(),
        object_pairs_hook=_reject_duplicate_keys,
    )
    payload = json.loads(
        (ROOT / "results" / "result.json").read_text(),
        object_pairs_hook=_reject_duplicate_keys,
    )
    required = set(schema["required"])
    properties = schema["properties"]
    assert set(payload) == required == set(properties)
    assert payload["status"] == properties["status"]["const"]
    for key in required - {"status"}:
        assert properties[key]["type"] == "object"
        assert type(payload[key]) is dict
