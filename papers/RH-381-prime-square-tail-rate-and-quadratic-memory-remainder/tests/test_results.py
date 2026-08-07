import copy
import json
from pathlib import Path
import re
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from experiments.build_result import (  # noqa: E402
    EXPECTED_ALL_SOURCE_DIGEST,
    EXPECTED_GROUP_DIGESTS,
    SOURCE_COMMITS,
    SOURCE_FILES,
    SOURCE_GROUPS,
    WORKSPACE,
    build_payload,
    build_source_locks,
    digest,
    lines_digest,
    source_digest_lines,
)


def _reject_duplicate_keys(pairs):
    output = {}
    for key, value in pairs:
        assert key not in output, f"duplicate JSON key: {key}"
        output[key] = value
    return output


def test_result_regenerates_with_25_release_blob_locks() -> None:
    stored = (ROOT / "results/result.json").read_text()
    regenerated = build_payload()
    assert json.dumps(regenerated, indent=2, sort_keys=True) + "\n" == stored
    locks = build_source_locks()
    assert locks["count"] == len(SOURCE_FILES) == 25
    assert len(set(SOURCE_FILES)) == 25
    assert locks["group_digests"] == EXPECTED_GROUP_DIGESTS
    assert locks["all_source_digest"] == EXPECTED_ALL_SOURCE_DIGEST
    assert locks["release_blob_identity_pass"] and locks["pass"]
    for entry in locks["entries"]:
        assert entry["sha256"] == digest(WORKSPACE / entry["path"])
        assert "AGENTS.md" not in entry["path"]
        assert "RH_HANDOFF.md" not in entry["path"]


def test_source_commit_membership_path_and_digest_mutations_fail_closed() -> None:
    bad_commits = dict(SOURCE_COMMITS)
    bad_commits["rh380_release"] = "0" * 40
    with pytest.raises(ValueError, match="commits were rebound"):
        build_source_locks(source_commits=bad_commits)

    bad_groups = copy.deepcopy(SOURCE_GROUPS)
    bad_groups["rh374_release"] = bad_groups["rh374_release"][:-1]
    with pytest.raises(ValueError, match="membership was rebound"):
        build_source_locks(source_groups=bad_groups)

    entries = build_source_locks()["entries"]
    unsafe = copy.deepcopy(entries)
    unsafe[0]["path"] = "prime_dynamics_theory/../RH_HANDOFF.md"
    with pytest.raises(ValueError, match="unsafe"):
        source_digest_lines(unsafe)

    mutated_lines = list(source_digest_lines(entries))
    mutated_lines[0] = mutated_lines[0][:-1] + ("0" if mutated_lines[0][-1] != "0" else "1")
    assert lines_digest(mutated_lines) != EXPECTED_ALL_SOURCE_DIGEST


def test_result_boundaries_and_frozen_interval_digest() -> None:
    payload = json.loads(
        (ROOT / "results/result.json").read_text(), object_pairs_hook=_reject_duplicate_keys
    )
    certificate = payload["certificate"]
    assert certificate["canonical_fixture_sha256"] == (
        "d55fd48071eb5b88c054f3d34329f274f792f2bbd859b4ab98e31b5b7020beb8"
    )
    assert certificate["interval_fixture_sha256"] == (
        "e0342f871b1f952039da2b1025fa7598771b9fa089295f07cb60b11f70cee15c"
    )
    assert certificate["interval_digest_matches_independent_plan"]
    assert payload["claim_boundary"]["route_a"] == "GO"
    assert payload["claim_boundary"]["route_b"] == "STOP_SCOPED"
    assert not any(payload["gates"].values())


def test_schema_is_recursively_closed() -> None:
    schema = json.loads(
        (ROOT / "results/result.schema.json").read_text(), object_pairs_hook=_reject_duplicate_keys
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
    assert schema["$defs"]["sourceLocks"]["properties"]["entries"]["minItems"] == 25


def test_payload_matches_closed_schema_primitives() -> None:
    schema = json.loads((ROOT / "results/result.schema.json").read_text())
    payload = json.loads((ROOT / "results/result.json").read_text())

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
            if node.get("uniqueItems"):
                assert len({json.dumps(child, sort_keys=True) for child in value}) == len(value)
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


def test_manuscript_has_required_declarations_and_scope_language() -> None:
    manuscript = (ROOT / "main.tex").read_text()
    for phrase in (
        "Data and code availability",
        "Author contributions",
        "Funding",
        "Competing interests",
        "Ethics and human participants",
        "AI assistance disclosure",
        "No prime number theorem",
        "Gates A--E remain false/open",
    ):
        assert phrase in manuscript
    assert "\\label{eq:EL}\\\\\n" in manuscript
