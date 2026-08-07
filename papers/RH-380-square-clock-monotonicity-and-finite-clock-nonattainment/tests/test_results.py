import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from experiments.build_result import (  # noqa: E402
    SOURCE_FILES,
    WORKSPACE,
    build_payload,
    build_source_locks,
    digest,
)


def _reject_duplicate_keys(pairs):
    output = {}
    for key, value in pairs:
        assert key not in output, f"duplicate JSON key: {key}"
        output[key] = value
    return output


def test_result_regenerates_and_release_locks_are_exact() -> None:
    stored_text = (ROOT / "results" / "result.json").read_text()
    regenerated = build_payload()
    assert json.dumps(regenerated, indent=2, sort_keys=True) + "\n" == stored_text
    entries, release_pass = build_source_locks()
    assert release_pass
    assert len(entries) == len(SOURCE_FILES) == 24
    assert len({entry["path"] for entry in entries}) == 24
    for entry in entries:
        assert entry["sha256"] == digest(WORKSPACE / entry["path"])
        assert "AGENTS.md" not in entry["path"] and "RH_HANDOFF.md" not in entry["path"]


def test_result_boundaries_and_negative_control() -> None:
    payload = json.loads(
        (ROOT / "results" / "result.json").read_text(),
        object_pairs_hook=_reject_duplicate_keys,
    )
    assert payload["certificate"]["all_pass"]
    assert payload["source_locks"]["release_blob_identity_pass"]
    negative = payload["predecessor_checks"]["negative_control"]
    assert negative["q180"] != negative["q36"]
    assert "not a same-prime-support cover" in negative["scope"]
    assert negative["sign_from_h_upper_bound_pass"]
    assert payload["claim_boundary"]["route_a"] == "GO"
    assert payload["claim_boundary"]["route_b"] == "STOP_SCOPED"
    assert not any(payload["gates"].values())


def test_schema_is_recursively_closed() -> None:
    schema = json.loads(
        (ROOT / "results" / "result.schema.json").read_text(),
        object_pairs_hook=_reject_duplicate_keys,
    )

    def visit(node):
        if not isinstance(node, dict):
            return
        if node.get("type") == "object":
            assert node.get("additionalProperties") is False
            if "properties" in node:
                assert set(node.get("required", ())) <= set(node["properties"])
        if node.get("type") == "array":
            assert "items" in node
        for value in node.values():
            if isinstance(value, dict):
                visit(value)
            elif isinstance(value, list):
                for item in value:
                    visit(item)

    visit(schema)
    assert schema["properties"]["source_locks"]["properties"]["entries"]["minItems"] == 24


def test_payload_matches_closed_schema_membership_and_primitives() -> None:
    schema = json.loads((ROOT / "results" / "result.schema.json").read_text())
    payload = json.loads((ROOT / "results" / "result.json").read_text())

    def resolve(node):
        if "$ref" not in node:
            return node
        target = schema
        for piece in node["$ref"].removeprefix("#/").split("/"):
            target = target[piece]
        return target

    def check(value, raw_node):
        node = resolve(raw_node)
        if "const" in node:
            assert value == node["const"]
        if "enum" in node:
            assert value in node["enum"]
        kind = node.get("type")
        if kind == "object":
            assert type(value) is dict
            assert set(node.get("required", ())) <= set(value) <= set(node.get("properties", ()))
            assert node["additionalProperties"] is False
            for key, child in value.items():
                check(child, node["properties"][key])
        elif kind == "array":
            assert type(value) is list
            assert len(value) >= node.get("minItems", 0)
            assert len(value) <= node.get("maxItems", len(value))
            for child in value:
                check(child, node["items"])
        elif kind == "string":
            assert type(value) is str
            if "pattern" in node:
                assert re.fullmatch(node["pattern"], value)
        elif kind == "integer":
            assert type(value) is int
            assert value >= node.get("minimum", value)
            assert value <= node.get("maximum", value)
        elif kind == "boolean":
            assert type(value) is bool

    check(payload, schema)
