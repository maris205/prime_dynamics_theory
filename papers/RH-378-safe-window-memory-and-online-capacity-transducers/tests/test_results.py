import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _reject_duplicate_keys(pairs):
    output = {}
    for key, value in pairs:
        assert key not in output, f"duplicate JSON key: {key}"
        output[key] = value
    return output


def test_result_ledger_and_claim_boundary() -> None:
    payload = json.loads(
        (ROOT / "results" / "result.json").read_text(),
        object_pairs_hook=_reject_duplicate_keys,
    )
    assert payload["status"] == "RH-378_safe_window_memory_and_online_capacity_transducers"
    assert payload["source_locks"]["count"] == 33
    assert payload["source_locks"]["pass"]
    assert payload["certificate"]["all_pass"]
    assert payload["claim_boundary"]["route_a"] == "GO"
    assert payload["claim_boundary"]["route_b"] == "STOP_SCOPED"
    assert not any(payload["gates"].values())


def test_result_matches_closed_shallow_schema_contract() -> None:
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


def test_frozen_counts_and_boundaries() -> None:
    certificate = json.loads((ROOT / "results" / "result.json").read_text())["certificate"]
    assert certificate["lag_two_census"]["safe_table_count"] == 13
    assert certificate["graph_lift_safety"]["total_cases"] == 486
    assert certificate["orientation_mealy"]["safety_case_count"] == 72
    assert certificate["exhaustive_prefix_extrema"]["word_count"] == 88572
    assert certificate["online_single_policy_obstruction"]["first_zero_horizon"] == 4
    assert certificate["mobius_finite_reproduction"]["prefix_extrema_equality_count"] == 2097152
