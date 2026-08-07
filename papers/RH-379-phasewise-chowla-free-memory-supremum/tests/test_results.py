import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from experiments.build_result import SOURCE_FILES, WORKSPACE, build_payload, digest  # noqa: E402


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
    assert payload["status"] == "RH-379_phasewise_chowla_free_memory_supremum"
    assert payload["source_locks"]["count"] == 28
    assert payload["source_locks"]["pass"]
    assert payload["certificate"]["all_pass"]
    assert payload["claim_boundary"]["route_a"] == "GO"
    assert payload["claim_boundary"]["route_b"] == "STOP_SCOPED"
    assert not any(payload["gates"].values())


def test_full_payload_regeneration_and_source_digests() -> None:
    stored_text = (ROOT / "results" / "result.json").read_text()
    regenerated = build_payload()
    regenerated_text = json.dumps(regenerated, indent=2, sort_keys=True) + "\n"
    assert regenerated_text == stored_text
    locks = regenerated["source_locks"]
    assert set(locks["files"]) == set(SOURCE_FILES)
    assert locks["count"] == len(SOURCE_FILES)
    for relative in SOURCE_FILES:
        assert locks["files"][relative] == digest(WORKSPACE / relative)


def test_result_matches_closed_top_level_schema_contract() -> None:
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
        assert properties[key]["additionalProperties"] is False
        assert set(payload[key]) == set(properties[key]["required"])


def test_schema_declares_every_nested_collection_shape() -> None:
    schema = json.loads((ROOT / "results" / "result.schema.json").read_text())

    def visit(node):
        if not isinstance(node, dict):
            return
        node_type = node.get("type")
        if node_type == "object":
            assert "additionalProperties" in node
        if node_type == "array" or (
            isinstance(node_type, list) and "array" in node_type
        ):
            assert "items" in node
        for value in node.values():
            if isinstance(value, dict):
                visit(value)
            elif isinstance(value, list):
                for item in value:
                    visit(item)

    visit(schema)
    source_files = schema["properties"]["source_locks"]["properties"]["files"]
    assert source_files["minProperties"] == source_files["maxProperties"] == 28


def test_frozen_exact_rows() -> None:
    certificate = json.loads((ROOT / "results" / "result.json").read_text())["certificate"]
    assert certificate["census"]["c11_zero_tables"] == 192
    assert certificate["census"]["reflection_neighbor_pair_checks"] == 512 * 512
    assert certificate["census"]["reflection_neighbor_pair_failures"] == 0
    assert all(row["all_pass"] for row in certificate["density_aggregation"])
    assert all(row["all_pass"] for row in certificate["cofinal_protocol_rows"])
    rows = {row["q"]: row for row in certificate["fixture_clocks"]}
    assert rows[36]["G"] == {"inv_pi2": "9/2", "kappa2": "-1/7"}
    assert rows[180]["G"] == {"inv_pi2": "73/16", "kappa2": "-25/161"}
    assert rows[900]["G"] == {"inv_pi2": "73/16", "kappa2": "-1/7"}
    assert rows[44100]["G"] == {"inv_pi2": "1177/256", "kappa2": "-1105/7567"}
